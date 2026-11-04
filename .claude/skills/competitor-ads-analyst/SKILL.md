---
name: competitor-ads-analyst
description: Break down competitors' ads into hooks, offers, formats, angles, CTAs, proof, and landing-page promises, then turn the patterns into a swipe file and ad concepts adapted for the user's own business. Works from Meta (Facebook/Instagram) Ad Library, Google Ads Transparency Center, TikTok Creative Center, LinkedIn Ad Library, YouTube, pasted ad copy, screenshots, or video transcripts. Use this whenever the user mentions competitor ads, ad library, swipe file, "what ads is X running", ad creative or hook analysis, ad angles, why a competitor's ads work, or wants ad ideas informed by what others in the market are doing, even if they just drop a competitor name and say "look at their ads".
---

# Competitor ads analyst

Competitors' ads are a free, public record of what they believe persuades their market, and
ads that have been running for months are evidence of what actually works. This skill reads
that record systematically. The output is not "copy their ad"; it is a breakdown of the
mechanics (hook, offer, format, angle, proof, CTA) so the user can learn the pattern and make
something better for their own offer.

## Inputs to pin down (assume and state when missing)

- **Competitors**: names, websites, or ad library URLs. If the user only names the market, find
  3 to 5 competitors first and confirm them in the report.
- **Platforms**: default to Meta and Google; add TikTok, LinkedIn, or YouTube when the niche
  lives there (B2B → LinkedIn; consumer and creator products → TikTok).
- **The user's own offer and audience**, so the final concepts are adapted, not generic.
- **Scope**: how many ads per competitor. Default 10 to 20 each, favoring the longest-running.

## Workflow

### 1. Collect the ads

Follow `references/ad-libraries.md` for each platform: it has the URLs, what each library
exposes, and what to do when a library will not load through a fetch (most are JavaScript
apps). Order of preference:

1. Ad library pages fetched directly, or driven with a browser tool if one is available.
2. Exports, screenshots, or links the user supplies. Read images with the file reading tool;
   ad screenshots are perfectly fine input.
3. Third-party coverage (search for `"<competitor>" ads` with the current month and year, press
   coverage, creator breakdowns) as a fallback, clearly labelled as secondhand.

For every ad record: competitor, platform, format, first-seen or start date, whether it is still
active, how many variations exist, headline, primary text (verbatim, trimmed), visual
description, CTA button, and landing URL. Run length is the most useful signal you will get:
an ad live for 90+ days is paying for itself.

If you can reach nothing (login walls, blocked fetches) say so plainly and ask for screenshots
or exports instead of filling gaps from memory. Never describe an ad you did not see.

### 2. Break each ad down

Use the taxonomy in `references/hooks-offers-formats.md` and fill one row per ad
(`assets/ad-breakdown-template.md` has the table). Per ad:

- **Hook**: the first line or first 3 seconds. Classify it (question, callout, bold claim, pain,
  curiosity, social proof, contrarian, "POV", before/after, number). Quote it.
- **Offer**: what is actually being exchanged. Free trial, discount, bundle, guarantee, lead
  magnet, demo, consultation, "book a call", price anchor, bonus stack, urgency.
- **Format**: static image, carousel, short video, UGC testimonial, talking head, screen
  recording, meme, text-only, long-form, comparison table.
- **Angle / persuasion mechanism**: the core argument (save time, save money, status, fear of
  missing out, authority, simplicity, "for people like you", identity).
- **Awareness level** the ad speaks to (unaware, problem-aware, solution-aware, product-aware,
  most-aware). Different hooks work at different levels, and this is where most of the lessons
  come from.
- **Proof**: numbers, logos, testimonials, reviews, press, demonstrations, or none.
- **CTA**: button and the text around it.
- **Landing promise**: does the landing page headline match the ad? Note mismatches; they are a
  weakness in the competitor and an opening for the user.
- **Signal strength**: run length, number of variations (they are testing it), and whether it
  appears on more than one platform.

### 3. Find the patterns

Across the full set, answer:

- Which hooks and offers dominate, and which are tied to the longest-running ads?
- What formats does each competitor rely on? Who is testing (many short-lived variations) and
  who has found a winner (few, long-running)?
- Which awareness levels are crowded and which are empty? An empty level is usually the
  cheapest place for the user to show up.
- Which objections do the ads pre-empt (price, trust, time, "will it work for me")?
- Are there seasonal or launch-driven bursts?
- What is nobody saying? Gaps in angle, audience, proof, or format.

### 4. Lessons and the swipe file

Turn the patterns into two things:

1. **Lessons**: 5 to 10 statements of the form "Competitors do X because Y; for us this means
   Z." Separate "adopt", "adapt", and "avoid".
2. **Ad concepts for the user**: 6 to 10 concepts, each with hook (written out), offer, format,
   angle, awareness level, proof to include, CTA, and a one-line note on which competitor
   pattern it draws on. Write original copy; do not reuse competitor sentences.

Save `competitor-ads-<market-slug>-<YYYY-MM-DD>.md` (report) and
`competitor-ads-<market-slug>-<YYYY-MM-DD>.csv` (one row per ad, columns from the template)
in the working directory or where the user asks. Summarize in chat: the single strongest
pattern, the biggest gap, and the top 3 concepts.

## Ground rules

- Analyze, do not plagiarize. Copy is quoted for analysis only; concepts for the user are
  written fresh.
- Keep claims about performance honest. Run length and variation count are signals, not
  proof of ROI. Say "likely working" not "their best ad".
- Date everything. An ad library snapshot is a point in time; name the day you looked.
- If the user's own ads are available (they can export them), include them as a baseline so the
  comparison is concrete.

## Related skills

- `industry-questions-research` for what customers are asking, which often supplies better
  hooks than competitors do.
- `sales-page-cro-audit` for the landing page the new ads will send traffic to.
