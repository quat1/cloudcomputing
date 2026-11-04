#!/usr/bin/env python3
"""
organize_invoices.py - scan a folder of receipts/invoices, extract the key
fields, copy + rename the files into an organized folder, and write a
spreadsheet of the amounts.

Originals are never modified, moved, or deleted. Everything is a copy.

Two-phase workflow (so Claude can fix anything the heuristics got wrong):

    1. scan   - read every receipt, extract fields, write a manifest.json
    2. apply  - read the (possibly hand-corrected) manifest, copy/rename the
                files into <dest>/YYYY/MM/, and write the spreadsheet

    python3 organize_invoices.py scan  ~/Receipts --manifest manifest.json
    python3 organize_invoices.py apply manifest.json --dest ~/Receipts-Organized

Or do both in one go when you trust the extraction:

    python3 organize_invoices.py run ~/Receipts --dest ~/Receipts-Organized

Dependencies: Python 3.9+ standard library. Optional extras that improve
extraction when installed: pdfplumber or pypdf (PDF text), the `pdftotext`
CLI (poppler), pytesseract + Pillow (OCR for image receipts).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RECEIPT_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff",
    ".heic", ".bmp", ".txt", ".md", ".eml", ".html", ".htm",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".heic", ".bmp"}

CURRENCY_SYMBOLS = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY", "₹": "INR", "₸": "KZT", "₽": "RUB"}
CURRENCY_CODES = {"USD", "EUR", "GBP", "CAD", "AUD", "NZD", "CHF", "JPY", "INR", "KZT", "RUB", "SGD", "HKD", "SEK", "NOK", "DKK", "PLN", "MXN", "BRL", "ZAR", "AED", "TRY", "CNY"}

# Phrases that usually sit right next to the number we want. Ordered from
# most to least trustworthy: "amount due"/"grand total" beat a bare "total",
# which in turn beats "subtotal" (which we actively avoid).
TOTAL_LABELS = [
    r"amount\s+(?:due|paid|charged|billed)", r"total\s+(?:due|paid|charged|amount)",
    r"grand\s+total", r"balance\s+due", r"order\s+total", r"invoice\s+total",
    r"you\s+paid", r"charged", r"payment\s+received", r"total",
]
NUMBER = r"(?:\d{1,3}(?:[,\s]\d{3})+|\d+)(?:[.,]\d{2})?"

CATEGORY_KEYWORDS = {
    "Software & SaaS": ["subscription", "saas", "license", "cloud", "hosting", "domain", "api", "plan renewal", "github", "notion", "slack", "zoom", "adobe", "google workspace", "microsoft 365", "aws", "amazon web services", "openai", "anthropic", "vercel", "figma", "canva"],
    "Advertising & Marketing": ["ads", "advertising", "campaign", "meta platforms", "facebook", "google ads", "linkedin", "tiktok", "mailchimp", "klaviyo"],
    "Travel": ["flight", "airline", "hotel", "airbnb", "booking.com", "uber", "lyft", "taxi", "train", "rail", "parking", "rental car", "hertz", "avis"],
    "Meals & Entertainment": ["restaurant", "cafe", "coffee", "starbucks", "lunch", "dinner", "doordash", "ubereats", "grubhub", "bar & grill"],
    "Office Supplies & Equipment": ["office depot", "staples", "amazon", "apple store", "best buy", "monitor", "keyboard", "printer", "ink", "toner", "paper"],
    "Utilities & Telecom": ["electric", "utility", "internet", "broadband", "mobile", "phone bill", "verizon", "at&t", "t-mobile", "comcast"],
    "Professional Services": ["consulting", "legal", "attorney", "accounting", "bookkeeping", "cpa", "freelance", "contractor", "retainer"],
    "Shipping & Postage": ["ups", "fedex", "usps", "dhl", "shipping", "postage", "courier"],
    "Education & Training": ["course", "udemy", "coursera", "workshop", "conference", "ticket", "training", "book"],
}

# ----------------------------------------------------------------------------
# Text extraction
# ----------------------------------------------------------------------------

def extract_text(path: Path) -> tuple[str, str]:
    """Return (text, method). method describes how the text was obtained so
    the manifest can say how much to trust it. Empty text is a normal outcome
    for scanned images when no OCR engine is installed."""
    ext = path.suffix.lower()
    if ext in {".txt", ".md", ".eml", ".html", ".htm"}:
        try:
            raw = path.read_text(errors="replace")
        except OSError:
            return "", "unreadable"
        if ext in {".html", ".htm", ".eml"}:
            raw = re.sub(r"<style.*?</style>|<script.*?</script>", " ", raw, flags=re.S | re.I)
            raw = re.sub(r"<[^>]+>", " ", raw)
        return raw, "plain-text"

    if ext == ".pdf":
        text = ""
        method = "none"
        try:
            import pdfplumber  # type: ignore
            with pdfplumber.open(str(path)) as pdf:
                text = "\n".join((page.extract_text() or "") for page in pdf.pages[:5])
            method = "pdfplumber"
        except Exception:
            pass
        if not text.strip():
            try:
                from pypdf import PdfReader  # type: ignore
                reader = PdfReader(str(path))
                text = "\n".join((p.extract_text() or "") for p in reader.pages[:5])
                method = "pypdf"
            except Exception:
                pass
        if not text.strip() and shutil.which("pdftotext"):
            try:
                out = subprocess.run(["pdftotext", "-layout", "-l", "5", str(path), "-"],
                                     capture_output=True, text=True, timeout=60)
                text = out.stdout
                method = "pdftotext"
            except Exception:
                pass
        if not text.strip():
            # Scanned PDF with no text layer. Try OCR on the first page.
            ocr = _ocr_pdf_first_page(path)
            if ocr:
                return ocr, "ocr"
            return "", "no-text-layer"
        return text, method

    if ext in IMAGE_EXTENSIONS:
        ocr = _ocr_image(path)
        return (ocr, "ocr") if ocr else ("", "no-ocr-available")

    return "", "unsupported"


def _ocr_image(path: Path) -> str:
    try:
        import pytesseract  # type: ignore
        from PIL import Image  # type: ignore
        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        return ""


def _ocr_pdf_first_page(path: Path) -> str:
    try:
        import pytesseract  # type: ignore
        import pdfplumber  # type: ignore
        with pdfplumber.open(str(path)) as pdf:
            img = pdf.pages[0].to_image(resolution=200).original
        return pytesseract.image_to_string(img)
    except Exception:
        return ""

# ----------------------------------------------------------------------------
# Field extraction heuristics
# ----------------------------------------------------------------------------

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9

DATE_PATTERNS = [
    # 2024-03-15, 2024/03/15, 2024.03.15
    (re.compile(r"\b(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})\b"), "ymd"),
    # 15 March 2024, 15 Mar 2024, 15th March, 2024
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\.?,?\s+(20\d{2})\b"), "dmy_name"),
    # March 15, 2024 / Mar 15 2024
    (re.compile(r"\b([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})\b"), "mdy_name"),
    # 03/15/2024, 15.03.2024, 3-15-24
    (re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](20\d{2}|\d{2})\b"), "ambiguous"),
]

DATE_LABEL_HINT = re.compile(r"(invoice\s+date|date\s+of\s+issue|issued|receipt\s+date|order\s+date|transaction\s+date|payment\s+date|date\s+paid|\bdate\b)", re.I)


def _mk_date(y: int, m: int, d: int):
    if y < 100:
        y += 2000
    try:
        return dt.date(y, m, d)
    except ValueError:
        return None


def find_dates(text: str, day_first: bool = False) -> list[tuple[dt.date, int]]:
    """Return a list of (date, score). Higher score = sits next to a label like
    'Invoice date'. Future dates and dates before 2000 are discarded."""
    results = []
    today = dt.date.today()
    for pat, kind in DATE_PATTERNS:
        for m in pat.finditer(text):
            g = m.groups()
            date = None
            if kind == "ymd":
                date = _mk_date(int(g[0]), int(g[1]), int(g[2]))
            elif kind == "dmy_name":
                mon = MONTHS.get(g[1].lower()[:4]) or MONTHS.get(g[1].lower()[:3])
                if mon:
                    date = _mk_date(int(g[2]), mon, int(g[0]))
            elif kind == "mdy_name":
                mon = MONTHS.get(g[0].lower()[:4]) or MONTHS.get(g[0].lower()[:3])
                if mon:
                    date = _mk_date(int(g[2]), mon, int(g[1]))
            elif kind == "ambiguous":
                a, b, y = int(g[0]), int(g[1]), int(g[2])
                if a > 12 and b <= 12:
                    date = _mk_date(y, b, a)
                elif b > 12 and a <= 12:
                    date = _mk_date(y, a, b)
                elif day_first:
                    date = _mk_date(y, b, a)
                else:
                    date = _mk_date(y, a, b)
            if not date or date > today + dt.timedelta(days=1) or date.year < 2000:
                continue
            window = text[max(0, m.start() - 40):m.start()]
            score = 2 if DATE_LABEL_HINT.search(window) else 1
            if re.search(r"due", window, re.I):
                score -= 1  # "Due date" is not the purchase date
            results.append((date, score))
    return results


def pick_date(text: str, path: Path, day_first: bool) -> tuple[str, str]:
    candidates = find_dates(text, day_first)
    if candidates:
        candidates.sort(key=lambda c: (-c[1], c[0]))  # best label score, then earliest
        best = candidates[0]
        return best[0].isoformat(), "text" if best[1] >= 2 else "text-unlabelled"
    # Try the filename (e.g. "receipt_2024-03-15.pdf")
    fn_dates = find_dates(path.name.replace("_", " "), day_first)
    if fn_dates:
        return fn_dates[0][0].isoformat(), "filename"
    # Fall back to the file's modification time, clearly flagged
    mtime = dt.date.fromtimestamp(path.stat().st_mtime)
    return mtime.isoformat(), "file-mtime"


def _to_float(num: str) -> float | None:
    s = num.replace(" ", "")
    # European style 1.234,56 -> 1234.56 ; US style 1,234.56 -> 1234.56
    if s.count(",") == 1 and s.count(".") == 0 and len(s.split(",")[1]) == 2:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def pick_amount(text: str) -> tuple[float | None, str, str]:
    """Return (amount, currency, method)."""
    currency = detect_currency(text)
    # 1. Labelled totals, in priority order. Skip anything on a 'subtotal' line.
    for label in TOTAL_LABELS:
        pat = re.compile(rf"(?<!sub)(?<!sub-)(?<!sub\s){label}\s*[:\-]?\s*(?:[A-Z]{{3}}\s*)?[$€£¥₹₸₽]?\s*({NUMBER})", re.I)
        found = []
        for m in pat.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line = text[line_start: text.find("\n", m.end()) if text.find("\n", m.end()) != -1 else len(text)]
            if re.search(r"sub\s*-?\s*total|tax\s+total|total\s+tax|total\s+items|total\s+qty", line, re.I):
                continue
            val = _to_float(m.group(1))
            if val is not None and 0 < val < 10_000_000:
                found.append(val)
        if found:
            # If a label appears several times (line items + summary) the
            # summary line is almost always the largest one.
            return max(found), currency, f"label:{label}"
    # 2. Largest currency-prefixed number in the document
    sym_pat = re.compile(rf"(?:[$€£¥₹₸₽]|(?:{'|'.join(CURRENCY_CODES)})\s?)\s*({NUMBER})")
    vals = [v for v in (_to_float(m.group(1)) for m in sym_pat.finditer(text)) if v]
    if vals:
        return max(vals), currency, "largest-currency-number"
    # 3. Largest number with two decimals anywhere
    dec_pat = re.compile(r"\b(\d{1,3}(?:,\d{3})*\.\d{2}|\d+\.\d{2})\b")
    vals = [v for v in (_to_float(m.group(1)) for m in dec_pat.finditer(text)) if v]
    if vals:
        return max(vals), currency, "largest-decimal"
    return None, currency, "not-found"


def detect_currency(text: str) -> str:
    codes = re.findall(r"\b(" + "|".join(CURRENCY_CODES) + r")\b", text)
    if codes:
        return max(set(codes), key=codes.count)
    syms = [c for c in text if c in CURRENCY_SYMBOLS]
    if syms:
        return CURRENCY_SYMBOLS[max(set(syms), key=syms.count)]
    return ""


VENDOR_SKIP = re.compile(r"^(invoice|receipt|tax invoice|bill|statement|order|thank you|thanks|date|total|amount|page \d|\d+[/.-]\d+|paid|customer|bill to|ship to|from|to)\b", re.I)


def pick_vendor(text: str, path: Path) -> tuple[str, str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # 1. Explicit labels
    for pat in (r"(?:merchant|vendor|seller|sold by|billed by|from|payee|store)\s*[:\-]\s*(.+)",):
        m = re.search(pat, text, re.I)
        if m and len(m.group(1).strip()) > 2:
            return clean_vendor(m.group(1)), "label"
    # 2. First plausible line (company names usually top the page)
    for line in lines[:12]:
        if len(line) < 3 or len(line) > 60:
            continue
        if VENDOR_SKIP.search(line):
            continue
        if re.search(r"\d{3,}", line):  # addresses, phone numbers, ids
            continue
        if sum(ch.isalpha() for ch in line) < 3:
            continue
        return clean_vendor(line), "first-line"
    # 3. Email domain anywhere in the doc (support@stripe.com -> Stripe)
    m = re.search(r"[\w.+-]+@([\w-]+)\.(?:com|net|org|io|co|ai|app|dev|kz|uk|de|fr)\b", text, re.I)
    if m and m.group(1).lower() not in {"gmail", "yahoo", "hotmail", "outlook", "icloud", "example"}:
        return m.group(1).capitalize(), "email-domain"
    # 4. Filename
    stem = re.sub(r"[\d_\-]+", " ", path.stem).strip()
    stem = re.sub(r"\b(invoice|receipt|inv|rcpt|scan|img|image|copy)\b", "", stem, flags=re.I).strip()
    if len(stem) >= 3:
        return clean_vendor(stem), "filename"
    return "Unknown", "none"


def clean_vendor(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip(" .,:;-|")
    name = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|co|gmbh|plc|pty|llp|s\.a\.|b\.v\.)\.?$", "", name, flags=re.I).strip(" .,")
    return name[:40].title() if name.isupper() or name.islower() else name[:40]


INVOICE_NO_PAT = re.compile(
    r"(?:invoice|receipt|order|reference|ref|transaction|confirmation|payment)\s*"
    r"(?:number|no\.?|num|#|id)?\s*[:#]?\s*(?=[A-Z0-9\-_/]{0,30}\d)([A-Z0-9][A-Z0-9\-_/]{3,30})", re.I)


def pick_invoice_number(text: str) -> str:
    """First thing after an 'Invoice #'-style label that actually looks like an
    identifier: it has a digit, and it is not a date."""
    for m in INVOICE_NO_PAT.finditer(text):
        cand = m.group(1).strip("-_/")
        if not re.search(r"\d", cand):
            continue  # matched a word like 'Invoice' or 'date', not an id
        if re.fullmatch(r"(?:20\d{2}|\d{1,2})[-/.]\d{1,2}[-/.]\d{2,4}", cand):
            continue  # that is a date sitting next to the word 'Receipt'
        return cand
    return ""


def guess_category(text: str, vendor: str) -> str:
    hay = (vendor + "\n" + text[:3000]).lower()
    best, best_hits = "Uncategorized", 0
    for cat, kws in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in hay)
        if hits > best_hits:
            best, best_hits = cat, hits
    return best

# ----------------------------------------------------------------------------
# Manifest
# ----------------------------------------------------------------------------

def safe_slug(s: str, maxlen: int = 40) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U).strip()
    s = re.sub(r"[\s_]+", "-", s)
    return (s[:maxlen].strip("-") or "unknown")


def file_hash(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:10]


def scan_folder(src: Path, day_first: bool, recursive: bool, default_currency: str = "") -> list[dict]:
    files = sorted((p for p in (src.rglob("*") if recursive else src.glob("*"))
                    if p.is_file() and p.suffix.lower() in RECEIPT_EXTENSIONS and not p.name.startswith(".")),
                   key=lambda p: (len(p.parts), str(p).lower()))
    seen_hashes: dict[str, str] = {}
    records = []
    for p in files:
        text, method = extract_text(p)
        date, date_src = pick_date(text, p, day_first)
        amount, currency, amount_src = pick_amount(text)
        currency = currency or default_currency
        vendor, vendor_src = pick_vendor(text, p)
        inv = pick_invoice_number(text)
        category = guess_category(text, vendor)
        h = file_hash(p)
        duplicate_of = seen_hashes.get(h, "")
        seen_hashes.setdefault(h, str(p))

        reasons = []
        if not text.strip():
            reasons.append(f"no text extracted ({method}) - open the file and fill in the fields by eye")
        if amount is None:
            reasons.append("amount not found")
        elif amount_src.startswith("largest"):
            reasons.append("amount is a guess (no 'total' label found)")
        if date_src == "file-mtime":
            reasons.append("date taken from file modification time, not the receipt")
        if vendor_src in {"filename", "none"}:
            reasons.append("vendor guessed from filename")
        if duplicate_of:
            reasons.append(f"identical content to {duplicate_of}")

        records.append({
            "source": str(p),
            "date": date,
            "vendor": vendor,
            "amount": amount,
            "currency": currency,
            "category": category,
            "invoice_number": inv,
            "notes": "",
            "needs_review": bool(reasons),
            "review_reasons": reasons,
            "duplicate_of": duplicate_of,
            "extraction": {
                "text_method": method,
                "date_source": date_src,
                "amount_source": amount_src,
                "vendor_source": vendor_src,
                "text_preview": re.sub(r"\s+", " ", text)[:400],
            },
        })
    return records


def target_name(rec: dict, ext: str, used: set[str]) -> str:
    amount = rec.get("amount")
    amt = f"{amount:.2f}" if isinstance(amount, (int, float)) else "unknown"
    cur = rec.get("currency") or ""
    base = f"{rec['date']}_{safe_slug(rec['vendor'])}_{amt}{('-' + cur) if cur else ''}"
    name = base + ext
    i = 2
    while name.lower() in used:
        name = f"{base}_{i}{ext}"
        i += 1
    used.add(name.lower())
    return name


def apply_manifest(records: list[dict], dest: Path, layout: str, dry_run: bool) -> list[dict]:
    used: set[str] = set()
    rows = []
    for rec in records:
        src = Path(rec["source"])
        if not src.exists():
            print(f"  ! missing source, skipped: {src}", file=sys.stderr)
            continue
        if rec.get("skip"):
            continue
        rec.setdefault("date", dt.date.today().isoformat())
        rec.setdefault("vendor", "Unknown")
        y, m = rec["date"][:4], rec["date"][5:7]
        if layout == "year-month":
            sub = dest / y / m
        elif layout == "year":
            sub = dest / y
        elif layout == "vendor":
            sub = dest / safe_slug(rec["vendor"])
        elif layout == "category":
            sub = dest / safe_slug(rec.get("category") or "Uncategorized")
        else:
            sub = dest
        new_name = target_name(rec, src.suffix.lower(), used)
        target = sub / new_name
        if not dry_run:
            sub.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)  # copy, never move
        rec["organized_path"] = str(target)
        rows.append(rec)
        print(f"  {'[dry-run] ' if dry_run else ''}{src.name}  ->  {target.relative_to(dest)}")
    return rows


SHEET_COLUMNS = ["Date", "Vendor", "Amount", "Currency", "Category", "Invoice #",
                 "Needs review", "Review reasons", "Notes", "Organized file", "Original file"]


def write_spreadsheet(rows: list[dict], out: Path) -> Path:
    data = [[r["date"], r["vendor"], r.get("amount"), r.get("currency", ""), r.get("category", ""),
             r.get("invoice_number", ""), "yes" if r.get("needs_review") else "",
             "; ".join(r.get("review_reasons", [])), r.get("notes", ""),
             r.get("organized_path", ""), r["source"]] for r in rows]
    data.sort(key=lambda d: (d[0] or "", d[1] or ""))
    if out.suffix.lower() == ".xlsx":
        try:
            from openpyxl import Workbook  # type: ignore
            from openpyxl.styles import Font  # type: ignore
            from openpyxl.utils import get_column_letter  # type: ignore
            wb = Workbook()
            ws = wb.active
            ws.title = "Receipts"
            ws.append(SHEET_COLUMNS)
            for c in ws[1]:
                c.font = Font(bold=True)
            for d in data:
                ws.append(d)
            n = len(data)
            ws.append([])
            ws.append(["TOTAL", "", f"=SUM(C2:C{n + 1})" if n else 0])
            ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
            for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
                for c in row:
                    c.number_format = "#,##0.00"
            for i, col in enumerate(SHEET_COLUMNS, start=1):
                width = max([len(col)] + [len(str(d[i - 1] or "")) for d in data]) if data else len(col)
                ws.column_dimensions[get_column_letter(i)].width = min(max(10, width + 2), 60)
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = f"A1:{get_column_letter(len(SHEET_COLUMNS))}{n + 1}"
            # Second sheet: totals by month and by category
            summ = wb.create_sheet("Summary")
            summ.append(["Month", "Count", "Total"])
            for c in summ[1]:
                c.font = Font(bold=True)
            by_month: dict[str, list[float]] = {}
            by_cat: dict[str, list[float]] = {}
            for d in data:
                if isinstance(d[2], (int, float)):
                    by_month.setdefault((d[0] or "")[:7], []).append(d[2])
                    by_cat.setdefault(d[4] or "Uncategorized", []).append(d[2])
            for k in sorted(by_month):
                summ.append([k, len(by_month[k]), round(sum(by_month[k]), 2)])
            summ.append([])
            summ.append(["Category", "Count", "Total"])
            summ.cell(row=summ.max_row, column=1).font = Font(bold=True)
            for k in sorted(by_cat):
                summ.append([k, len(by_cat[k]), round(sum(by_cat[k]), 2)])
            summ.column_dimensions["A"].width = 30
            wb.save(out)
            return out
        except ImportError:
            out = out.with_suffix(".csv")
            print(f"  openpyxl not installed; writing CSV instead: {out}", file=sys.stderr)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(SHEET_COLUMNS)
        w.writerows(data)
        total = sum(d[2] for d in data if isinstance(d[2], (int, float)))
        w.writerow(["TOTAL", "", round(total, 2)])
    return out


def summarize(rows: list[dict]) -> None:
    total = sum(r["amount"] for r in rows if isinstance(r.get("amount"), (int, float)))
    review = [r for r in rows if r.get("needs_review")]
    print(f"\n{len(rows)} receipts organized, total {total:,.2f}. {len(review)} flagged for review.")
    for r in review:
        print(f"  - {Path(r['source']).name}: {'; '.join(r.get('review_reasons', []))}")

# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="extract fields from every receipt and write a manifest")
    s.add_argument("source", type=Path)
    s.add_argument("--manifest", type=Path, default=Path("manifest.json"))
    s.add_argument("--day-first", action="store_true", help="read 03/04/2024 as 3 April (default: March 4)")
    s.add_argument("--no-recursive", action="store_true")
    s.add_argument("--currency", default="", help="currency code to assume when a receipt shows none, e.g. USD")

    a = sub.add_parser("apply", help="copy/rename files per manifest and write the spreadsheet")
    a.add_argument("manifest", type=Path)
    a.add_argument("--dest", type=Path, required=True)
    a.add_argument("--layout", choices=["year-month", "year", "vendor", "category", "flat"], default="year-month")
    a.add_argument("--sheet", type=Path, help="spreadsheet path (default <dest>/receipts.xlsx)")
    a.add_argument("--dry-run", action="store_true")

    r = sub.add_parser("run", help="scan + apply in one step")
    r.add_argument("source", type=Path)
    r.add_argument("--dest", type=Path, required=True)
    r.add_argument("--layout", choices=["year-month", "year", "vendor", "category", "flat"], default="year-month")
    r.add_argument("--sheet", type=Path)
    r.add_argument("--manifest", type=Path, help="also save the manifest here")
    r.add_argument("--day-first", action="store_true")
    r.add_argument("--no-recursive", action="store_true")
    r.add_argument("--currency", default="")
    r.add_argument("--dry-run", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd in {"scan", "run"}:
        src = args.source.expanduser().resolve()
        if not src.is_dir():
            print(f"not a folder: {src}", file=sys.stderr)
            return 2
        records = scan_folder(src, args.day_first, not args.no_recursive, args.currency.upper())
        if not records:
            print(f"no receipts found in {src} (looked for {', '.join(sorted(RECEIPT_EXTENSIONS))})")
            return 1
        manifest = args.manifest
        if args.cmd == "scan" or manifest:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text(json.dumps(records, indent=2, ensure_ascii=False))
            print(f"scanned {len(records)} files -> {manifest}")
        flagged = [r for r in records if r["needs_review"]]
        print(f"{len(records)} receipts scanned, {len(flagged)} need review")
        for rec in records:
            flag = " (REVIEW)" if rec["needs_review"] else ""
            amt = f"{rec['amount']:.2f}" if isinstance(rec["amount"], (int, float)) else "?"
            print(f"  {Path(rec['source']).name}: {rec['date']} | {rec['vendor']} | {amt} {rec['currency']}{flag}")
        if args.cmd == "scan":
            return 0
    else:
        records = json.loads(args.manifest.read_text())

    dest = args.dest.expanduser().resolve()
    src_root = Path(records[0]["source"]).parent if records else None
    if src_root and (dest == src_root or src_root in dest.parents):
        print("destination must be outside the source folder so the originals stay untouched", file=sys.stderr)
        return 2
    print(f"\norganizing into {dest} ({args.layout}):")
    rows = apply_manifest(records, dest, args.layout, args.dry_run)
    sheet = args.sheet or dest / "receipts.xlsx"
    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)
        written = write_spreadsheet(rows, sheet)
        print(f"\nspreadsheet: {written}")
    summarize(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
