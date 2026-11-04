---
name: industry-questions-research
description: Research what people in an industry or niche are actually asking right now (default window is the last 30 days) across Reddit, Quora, Google "People also ask", forums, YouTube, X, LinkedIn, and review sites, then turn those real questions into a prioritized list of content ideas with titles, formats, angles, and source links. Use this whenever the user wants content ideas, blog/video/newsletter/social topics, "what should I post about", trending questions, audience pain points, FAQ research, customer questions, or market research for content, even if they never say the word "research". Also use it when the user names an industry and asks what people are talking about or struggling with.
---

# Industry questions research → content ideas

People tell you exactly what content they want by asking questions in public. This skill
collects those questions from the places people actually ask them, keeps only the recent ones,
and turns them into content you can make this week. The value is in the sourcing: every idea
traces back to a real question a real person asked, with a link and a date, so the user is
never guessing what their audience cares about.

## Inputs to pin down (ask if missing, but do not block on them)

- **Industry / niche** and, if known, the **audience** (role, company size, consumer vs B2B).
  Treat "my industry" as a prompt to check the repo or project context files for the business
  first, then ask.
- **The user's offer**, so ideas can be ranked by how close they sit to what the business sells.
- **Time window**: default to the last 30 days from today. Say the actual date range in the report.
- **Platforms**: default to all of the sources in `references/question-sources.md`; narrow if the
  user only cares about one or two.
- **Content formats they publish** (blog, YouTube, short video, newsletter, LinkedIn, podcast).
  Default to a mix.

If something is missing, state the assumption you are making and keep going.

## Workflow

### 1. Gather questions (breadth first)

Work through `references/question-sources.md`. It has query recipes per source. The important
habits:

- Use the web search tool with recency built into the query (month and year, "this week",
  `site:reddit.com`, and so on) and prefer the extended search mode when standard results come
  back stale or thin. Fetch the actual thread or page when a result looks promising, because the
  comments usually hold the better questions.
- Capture questions **verbatim** in the asker's words. The phrasing is the content hook; cleaning
  it up loses the signal.
- For each question record: source, URL, date (as best you can tell), engagement (upvotes,
  replies, views), and who asked (a beginner, a practitioner, a buyer).
- Aim for 40 to 80 raw questions before you stop. Fewer than 20 means the niche is too narrow
  or the searches are wrong; try adjacent phrasing and the audience's own jargon.
- Skip anything older than the window unless it is clearly still active (new replies inside the
  window count). Flag evergreen questions separately so they are not confused with what is hot now.

### 2. Cluster and score

Group the raw questions into themes (usually 6 to 12). Within each theme, note how many distinct
people asked, the total engagement, how recent the newest one is, and the intent:

| Intent | What it looks like | Content it wants |
|---|---|---|
| Learning | "how do I", "what is", "beginner" | tutorials, explainers, checklists |
| Choosing | "X vs Y", "best", "is it worth it", "alternatives" | comparisons, buyer guides, reviews |
| Fixing | "why does", "not working", "keeps happening" | troubleshooting, teardown, case study |
| Deciding / buying | "pricing", "should I hire", "how much does" | offer-adjacent content, calculators, FAQs |
| Venting / trend | "anyone else", "is it just me", news reactions | opinion, hot take, roundup |

Score each theme 1 to 5 on **volume**, **recency**, **engagement**, and **fit to the user's
offer**. Rank by the sum. Fit matters because the goal is content that brings the right people,
not just traffic.

### 3. Turn questions into content ideas

For each of the top themes, write 2 to 4 ideas. Each idea gets:

- **Working title**, written as a promise or the question itself. Give one alternative title.
- **Format** that suits the question (a "which is better" question wants a comparison table, a
  "why does this keep happening" question wants a short diagnostic video, and so on).
- **Angle / hook**: the specific tension, mistake, number, or contrarian take that makes it
  worth clicking. Quote the real question that inspired it.
- **Key points to cover**, 3 to 6 bullets, pulled from what the askers were confused about.
- **Funnel stage** and a natural **call to action** that fits the user's offer.
- **Source links** for the questions behind it.

Prefer ideas the user can produce from their own expertise. Flag ideas that need original data,
interviews, or tools so they are planned, not promised.

### 4. Deliver

Write the report with `assets/content-ideas-template.md` as the structure, and save two files
in the working directory (or where the user asked):

- `content-ideas-<industry-slug>-<YYYY-MM-DD>.md` with the full report
- `content-ideas-<industry-slug>-<YYYY-MM-DD>.csv` with one row per idea
  (title, format, theme, score, funnel stage, source URLs) so it drops into a content calendar

Then give the user a short summary in chat: the top 5 ideas, the one surprising theme, and
where the questions were loudest. If the user has a Notion, Google Sheets, or similar tool
connected and asks for it, put the table there too.

## Quality bar

- **Never invent a question or a source.** If a search tool returns nothing dated inside the
  window, say so and widen the window explicitly rather than quietly using old material.
- Dates matter. If a source does not show one, say "undated" instead of guessing.
- Short quotes only when quoting a thread; paraphrase the rest. Link to the original.
- Keep the ideas specific to the niche. "10 tips for X" with no real question behind it is
  what this skill exists to avoid.
- Note the limits of what you could reach: some platforms block automated reading (private
  groups, X without login). Tell the user which sources were covered and which were not.

## Related skills

- `competitor-ads-analyst` when the user wants to see what competitors are promoting, not what
  customers are asking.
- `sales-page-cro-audit` when the research should feed a landing page rather than content.
