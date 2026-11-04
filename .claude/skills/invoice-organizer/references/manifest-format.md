# manifest.json format and script reference

## Record fields

The `scan` command writes a JSON list. One record per receipt:

| Field | Type | Meaning |
|---|---|---|
| `source` | string | Absolute path of the original file. Never modified by the script. |
| `date` | `YYYY-MM-DD` | Purchase or invoice date. Drives the folder and filename. |
| `vendor` | string | Merchant name. Slugified into the filename. |
| `amount` | number or null | Total paid. `null` means not found. Use a negative number for refunds. |
| `currency` | string | ISO code such as `USD`, `EUR`; empty if unknown and no default given. |
| `category` | string | Keyword guess: Software & SaaS, Advertising & Marketing, Travel, Meals & Entertainment, Office Supplies & Equipment, Utilities & Telecom, Professional Services, Shipping & Postage, Education & Training, Uncategorized. Change freely. |
| `invoice_number` | string | Invoice, receipt, or order id if found. |
| `notes` | string | Free text; shows up in the spreadsheet. |
| `needs_review` | bool | True when any `review_reasons` exist. Set to false after fixing. |
| `review_reasons` | list of strings | Why it was flagged. |
| `duplicate_of` | string | Path of an earlier file with identical bytes, or empty. |
| `skip` | bool (optional) | Add `"skip": true` to leave a record out of the organized folder and spreadsheet. |
| `extraction` | object | How each field was obtained; useful when deciding what to trust. |

`extraction` sub-fields:

- `text_method`: `pdfplumber`, `pypdf`, `pdftotext`, `plain-text`, `ocr`, `no-text-layer`,
  `no-ocr-available`, `unsupported`, `unreadable`.
- `date_source`: `text` (next to a label like "Invoice date"), `text-unlabelled`,
  `filename`, `file-mtime`.
- `amount_source`: `label:<pattern>` (found next to a total-style label), `largest-currency-number`,
  `largest-decimal`, `not-found`.
- `vendor_source`: `label`, `first-line`, `email-domain`, `filename`, `none`.
- `text_preview`: first 400 characters of extracted text, whitespace collapsed.

## Naming and layout

Filename: `YYYY-MM-DD_<Vendor-Slug>_<amount>-<CUR><ext>`, for example
`2024-03-15_Acme-Cloud-Services_92.23-USD.pdf`. Collisions get `_2`, `_3`. Missing amounts
become `unknown`.

Layouts (`--layout`): `year-month` (default, `2024/03/`), `year`, `vendor`, `category`, `flat`.

## Spreadsheet

Sheet **Receipts**: Date, Vendor, Amount, Currency, Category, Invoice #, Needs review,
Review reasons, Notes, Organized file, Original file; sorted by date; a TOTAL row with a SUM
formula; header frozen and filterable.

Sheet **Summary**: count and total by month, then by category.

CSV output (when the sheet path ends in `.csv` or openpyxl is missing) has the same columns and
a TOTAL row, without the summary sheet.

## Commands

```bash
# scan only
python3 scripts/organize_invoices.py scan SOURCE --manifest manifest.json [--day-first] [--currency USD] [--no-recursive]

# apply a reviewed manifest
python3 scripts/organize_invoices.py apply manifest.json --dest DEST [--layout year-month|year|vendor|category|flat] [--sheet DEST/receipts.xlsx] [--dry-run]

# both at once
python3 scripts/organize_invoices.py run SOURCE --dest DEST [--manifest manifest.json] [same options]
```

Exit codes: 0 success, 1 no receipts found, 2 bad arguments (missing folder, destination inside source).

## Dependencies

Standard library only, for the core. Optional, each improves extraction when present:

```bash
pip install pdfplumber pypdf openpyxl        # PDF text layers, Excel output
pip install pytesseract pillow               # OCR for photos and scans, needs the tesseract binary:
#   macOS: brew install tesseract   Debian/Ubuntu: sudo apt install tesseract-ocr   Windows: https://github.com/UB-Mannheim/tesseract/wiki
```

Without `openpyxl` the script writes CSV. Without any PDF library it tries the `pdftotext`
command (poppler). Without OCR, image receipts are flagged for manual reading.
