# Four Claude Code skills for running a small business

Four ready-to-use [Claude Code](https://claude.ai/code) skills that cover the marketing and
admin jobs most small businesses repeat every month:

| # | Skill | What it does | Try saying |
|---|---|---|---|
| 1 | **`industry-questions-research`** | Finds what people in your industry have been asking in the last 30 days (Reddit, Quora, forums, Google "People also ask", YouTube, LinkedIn, review sites) and turns the questions into a ranked list of content ideas with titles, formats, hooks, and source links. Saves a report and a CSV. | "What are ecommerce sellers asking about bookkeeping lately? Give me content ideas for LinkedIn and the blog." |
| 2 | **`competitor-ads-analyst`** | Breaks competitors' ads (Meta Ad Library, Google Ads Transparency Center, TikTok, LinkedIn, or screenshots you give it) into hooks, offers, formats, angles, proof, and CTAs, finds the patterns, and writes original ad concepts for your business. Saves a report and a CSV swipe file. | "Look at the Facebook ads Factor and HelloFresh are running and break them down. What can we learn?" |
| 3 | **`sales-page-cro-audit`** | Audits a sales or landing page with the seven-dimension CRO framework from Corey Haines' open-source marketing skills, and gives specific fixes: three rewritten headlines, new button copy, a shorter form, trust and objection fixes, and test ideas. | "Our landing page isn't converting. Here's the URL. Tell me exactly what to change." |
| 4 | **`invoice-organizer`** | Point it at a folder of receipts (PDFs, photos, scans, email exports). It copies them into `YYYY/MM/` folders, renames each copy `date_vendor_amount`, and writes an Excel or CSV spreadsheet with monthly and category totals. Originals are never touched. | "Organize ~/Receipts for my accountant and put the amounts in a spreadsheet." |

Each skill lives in `.claude/skills/<skill-name>/` as a `SKILL.md` with its instructions, a
`references/` folder with the detailed checklists and source lists, an `assets/` folder with
report templates, and an `evals/` folder with a sample test case.

## Installation guide

### Option A: use this repo as a project (fastest)

Claude Code loads project skills from `.claude/skills/` automatically.

```bash
git clone https://github.com/quat1/cloudcomputing.git
```

```bash
cd cloudcomputing && claude
```

Type `/` and the four skills appear in the list, or just describe the job in plain words.

### Option B: install the skills into your own account (works in every project)

Copy the skill folders into your personal skills directory. Claude Code reads
`~/.claude/skills/` in every session.

```bash
git clone https://github.com/quat1/cloudcomputing.git /tmp/cloud-skills
```

```bash
mkdir -p ~/.claude/skills && cp -R /tmp/cloud-skills/.claude/skills/* ~/.claude/skills/
```

Restart Claude Code. On Windows the directory is `%USERPROFILE%\.claude\skills`.

### Option C: add them to one existing project

```bash
mkdir -p .claude/skills && cp -R /tmp/cloud-skills/.claude/skills/* .claude/skills/
```

Commit the folder and your whole team gets the skills.

### Option D: Claude.ai (desktop or web)

Zip a skill folder (for example `invoice-organizer/`) so that `SKILL.md` sits at the top level
of the zip, then upload it under **Settings → Capabilities → Skills**. Skills 1 to 3 work
anywhere Claude can search the web. Skill 4 needs a Claude Code session with access to your
files.

## Requirements

- Claude Code (any recent version). Skills 1 to 3 use web search and page fetching; skill 3
  can also read a screenshot or pasted copy.
- Python 3.9 or newer for the invoice organizer. The core runs on the standard library.
  Optional extras improve it:

```bash
pip install pdfplumber pypdf openpyxl
```

  gives PDF text extraction and Excel output (without `openpyxl` you get CSV). For photos and
  scans, install the Tesseract OCR engine (`brew install tesseract` on macOS,
  `sudo apt install tesseract-ocr` on Debian/Ubuntu) and then:

```bash
pip install pytesseract pillow
```

  Without OCR the script flags image receipts and Claude reads them by eye, which works fine
  for small batches.

## How to use each skill

**Industry questions research.** Tell Claude your industry, your audience, and where you
publish. It searches for recent questions, clusters them into themes, scores them, and writes
`content-ideas-<industry>-<date>.md` and `.csv`. Every idea links to the question that inspired
it. If it could not reach a source (private groups, X without login), it says so.

**Competitor ads analyst.** Give it competitor names or ad-library links. Ad libraries are
JavaScript apps and sometimes cannot be read with a plain fetch; when that happens, drop in
screenshots or an export and it works from those. The report lists every ad with its hook,
offer, format, angle, awareness level, proof, and CTA, then the patterns and 6 to 10 original
concepts for your business. It never invents ads it did not see.

**Sales page CRO audit.** Give it a URL, the page HTML, a screenshot, or pasted copy, plus
where the traffic comes from and what the page should make people do. It runs a five-second
test, scores seven dimensions (value proposition, headline, CTAs, visual hierarchy, trust,
objections, friction), and writes findings as Issue → Why → Fix → Priority → Effort, with
rewritten headlines and buttons and a recommended form. The methodology is adapted from the
`cro` skill in [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
(MIT license). The original library installs with
`npx skills add coreyhaines31/marketingskills --skill cro` if you want all of Corey's skills.

**Invoice organizer.** Say where the receipts are and where the organized copies should go.
Claude runs the script's `scan` step, reviews anything flagged (unreadable photos, missing
amounts, duplicates), edits the manifest, then runs `apply`. You get the organized folder, the
spreadsheet, a total, and a list of anything still needing a human look. The script can also be
run by hand:

```bash
python3 .claude/skills/invoice-organizer/scripts/organize_invoices.py run ~/Receipts --dest ~/Receipts-Organized --day-first --currency EUR
```

## Testing the skills

Each skill ships with a test case under `evals/` in the format `claude plugin eval` reads.
From a skill folder:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash --scaffold
```

These are real model runs and are billed to your account. The invoice organizer's case includes
sample receipts, so it also serves as a demo folder.

## Credits

- Skill 3's framework is adapted from Corey Haines' open-source marketing skills
  ([coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), MIT).
- Built with the Claude Code skill-creator workflow.
