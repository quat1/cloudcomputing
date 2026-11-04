---
name: invoice-organizer
description: Organize a folder of receipts and invoices (PDFs, photos, screenshots, scans, text or email exports) by copying them into a dated folder structure, renaming each copy to date_vendor_amount, and writing an Excel or CSV spreadsheet with date, vendor, amount, currency, category, and invoice number plus monthly and category totals. Originals are never moved, renamed, or deleted. Use this whenever the user mentions receipts, invoices, expenses, bookkeeping, tax prep, reimbursements, "organize my receipts folder", pulling amounts out of a pile of documents, or wants a spreadsheet of what they spent, even if they only point at a folder and say "sort this out".
---

# Invoice organizer

Give it a folder of receipts, get back a tidy copy of that folder and a spreadsheet of the
amounts. The bundled script does the deterministic parts (reading PDFs, finding totals and
dates, copying, renaming, writing the spreadsheet). You do the judgment parts: reading the
receipts the script could not parse, fixing wrong guesses, and confirming duplicates. Nothing
touches the original files, so a mistake costs a rerun, not a receipt.

## What the user gets

```
Receipts-Organized/
├── 2024/
│   ├── 01/2024-01-20_Staples_38.90-USD.jpg
│   ├── 03/2024-03-15_Acme-Cloud-Services_92.23-USD.pdf
│   └── 04/2024-04-09_Uber_23.47-USD.pdf
└── receipts.xlsx        (sheet "Receipts": one row per file + TOTAL;
                          sheet "Summary": totals by month and by category)
```

Other layouts are available (`--layout year`, `vendor`, `category`, `flat`), and the
spreadsheet can be CSV instead of XLSX by giving the sheet path a `.csv` extension.

## Workflow

### 1. Confirm the inputs

- **Source folder**: where the receipts are. Subfolders are included by default.
- **Destination**: default to a sibling folder named `<source>-Organized`. It must be outside
  the source folder (the script refuses otherwise, to keep originals pristine).
- **Date convention**: numeric dates like `03/04/2024` are ambiguous. Default to month-first
  (US). Pass `--day-first` for users in Europe, the UK, Australia, Kazakhstan, and most of the
  rest of the world. If the user's location is unknown, look at a couple of receipts: a date
  like `25/03/2024` settles it.
- **Default currency** for receipts that show an amount with no symbol (`--currency USD`).

State the assumptions you make rather than waiting; the user can rerun.

### 2. Scan

```bash
python3 <skill-dir>/scripts/organize_invoices.py scan "<source>" --manifest manifest.json [--day-first] [--currency USD]
```

The script prints one line per receipt and writes `manifest.json`, one record per file with
the extracted fields, where each came from, a short text preview, and a `needs_review` flag
with reasons. See `references/manifest-format.md` for the fields.

Put `manifest.json` in the scratchpad or working directory, not inside the source folder.

### 3. Review what the script flagged

This is the step that makes the result trustworthy. For every record with `needs_review`:

- **No text extracted** (photos, scans, image-only PDFs when no OCR engine is installed):
  open the file with the file reading tool. You can read images and PDFs directly. Fill in
  `date`, `vendor`, `amount`, `currency`, and `category` from what you see, and put a short
  note in `notes` ("read by eye from photo").
- **Amount is a guess**: check the preview or open the file. The script prefers lines
  labelled total / amount due / grand total and avoids subtotals, but handwritten receipts,
  multi-currency invoices, and statements confuse it.
- **Date from file modification time**: the receipt had no readable date. Read it by eye or,
  if it truly has none, leave the mtime date and say so in `notes`.
- **Vendor guessed from filename**: fix it if the file shows the merchant.
- **Duplicate of another file** (identical bytes): confirm, then set `"skip": true` on the
  copy so it is not organized twice. Do not skip near-duplicates (same vendor and amount,
  different file) without checking; two coffees on the same day are not duplicates.

Also skim the records that were not flagged. Common silent errors worth a glance: a vendor
that is really the customer's own name (invoices addressed to the user), a "total" that is a
year-to-date figure on a statement, and a due date mistaken for the invoice date.

Edit the manifest with the file editing tool. It is plain JSON; only the fields you change
need touching. Set `needs_review` to `false` once a record is fixed so the spreadsheet shows
it as clean.

### 4. Apply

Dry-run first to see the renames, then run for real:

```bash
python3 <skill-dir>/scripts/organize_invoices.py apply manifest.json --dest "<destination>" --dry-run
python3 <skill-dir>/scripts/organize_invoices.py apply manifest.json --dest "<destination>"
```

Add `--layout vendor|category|year|flat` if the user prefers, and `--sheet path.csv` for CSV.

When the scan looks clean and the user wants speed, `run` does scan and apply in one step
(`run "<source>" --dest "<destination>" --manifest manifest.json`). Still read the flagged
lines it prints and fix anything wrong by editing the manifest and rerunning `apply`.

### 5. Report back

Tell the user, briefly:

- Where the organized copies and the spreadsheet are.
- Totals: number of receipts, grand total, and the monthly or category totals if the set is
  small enough to show in a short table.
- Anything still flagged (unreadable files, missing amounts, suspected duplicates), each with
  the filename and what is needed.
- Any assumption that could change the numbers (date convention, default currency, a
  receipt you read by eye).

If the user wants the data in Google Sheets, Notion, or accounting software, the XLSX or CSV
imports directly; use a connected tool for that only if the user asks.

## Handling the awkward cases

| Situation | What to do |
|---|---|
| Photos and scans with no OCR available | Read them yourself, record by record. For large batches, suggest installing `tesseract` plus `pytesseract` so the script can OCR them (`references/manifest-format.md` has the commands). |
| Scanned PDF, no text layer | Same as photos; the script says `no-text-layer`. |
| European number format (`1.234,56`) | Handled. Check the preview if the amount looks off by a factor of 1000. |
| Multi-page invoices | Script reads the first five pages; totals are usually on page one or the last page. Open the file if the amount is missing. |
| Email exports (`.eml`, `.html`) | Supported; HTML is stripped. Vendor is usually the sender. |
| Several receipts in one PDF | Not split automatically. Note it in the report and suggest splitting with a PDF tool first. |
| Credit notes and refunds | Enter the amount as negative in the manifest and note it. |
| Foreign currency | Keep the receipt's currency in the Currency column; do not convert unless the user asks and gives a rate. |
| Receipt folder on a cloud drive (Google Drive, Dropbox) | Work on a local sync folder or download copies first; never organize in place. |

## Privacy

Receipts hold names, addresses, card fragments, and spending history. Keep everything local:
the script makes no network calls, and you should not send receipt contents to any external
service unless the user explicitly asks for that. When summarizing in chat, totals and vendor
names are fine; avoid repeating card numbers, addresses, or personal details.
