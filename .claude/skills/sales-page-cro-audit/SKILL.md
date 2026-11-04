---
name: sales-page-cro-audit
description: Audit a sales page, landing page, homepage, pricing page, or signup/lead form for conversion rate optimization (CRO) and deliver specific, prioritized fixes for the headline, CTA buttons, forms, trust signals, objections, and friction, including rewritten headline and button copy. Follows the 7-dimension CRO framework from Corey Haines' open-source marketing skills library. Use this whenever the user shares a page URL, HTML, screenshot, or pasted copy and wants it reviewed, says a page "isn't converting" or "sucks", asks for CRO, landing page feedback, headline/button/form advice, or wants more signups, leads, demos, or sales from an existing page, even if they do not use the term CRO.
metadata:
  adapted_from: coreyhaines31/marketingskills (cro skill, MIT license)
---

# Sales page CRO audit

A sales page has one job: get the right visitor to take the next step. This skill audits a
page the way a conversion specialist would, in order of impact, and returns fixes concrete
enough to ship today: rewritten headlines, new button copy, a shorter form, and the reasons
behind each. The framework is adapted from the `cro` skill in Corey Haines'
[marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). If the user wants the
full original library, it installs with `npx skills add coreyhaines31/marketingskills --skill cro`.

## Step 0: get the page and the context

Get the page in front of you, in this order of preference:

1. Fetch the URL. If the result is an empty shell (JavaScript-rendered), use a browser tool
   if one is available to load it and take a screenshot, or ask the user for the HTML or a
   full-page screenshot. Screenshots are good input: read them with the file reading tool.
2. Pasted copy or an HTML file from the user.

Look at it on mobile too if you can (narrow viewport or the user's phone screenshot). Most
traffic is mobile and most sales pages are reviewed on desktop.

Then collect context. Ask, but do not block; state assumptions if the user is not around:

- Page type (homepage, landing page from ads, pricing, feature, long-form sales letter, lead form)
- The one conversion goal (trial, demo, purchase, lead, call)
- Where traffic comes from (cold ads, search, email, referral) and what that traffic was promised
- Current conversion rate and the goal, if known
- What happens after the click (checkout, calendar, onboarding)
- What they already tried
- Any product-context file in the project (`product-marketing.md`, a brand or positioning doc).
  Read it first if it exists; it tells you who the page is for.

## Step 1: the five-second test

Before auditing anything, read only what is visible without scrolling and answer, as a cold
visitor: What is this? Who is it for? What do I get? What do I do next? If any answer takes
more than a glance, that is finding number one, and most of the other findings follow from it.

## Step 2: audit the seven dimensions, in order of impact

Work through `references/cro-checklist.md`, which has the detailed checks and the rules of
thumb. The dimensions, highest impact first:

1. **Value proposition clarity**. Can a stranger say what it is and why they should care in
   five seconds? Is the benefit specific to this audience, or could any competitor claim it?
2. **Headline effectiveness**. Outcome-focused, specific, in the customer's words, matched to
   the traffic source. Subheadline adds the "how" or the proof, not a restatement.
3. **CTA placement, copy, and hierarchy**. One primary action, visible above the fold,
   repeated at natural decision points, with copy that names what the visitor gets. "Submit",
   "Sign up", and "Learn more" are the weak defaults. Secondary actions must look secondary.
4. **Visual hierarchy and scannability**. Does the eye land on headline → benefit → proof →
   CTA? Headings that tell the story on their own, short paragraphs, whitespace, images that
   show the product or the outcome rather than decoration.
5. **Trust signals and social proof**. Logos, named testimonials with specifics, numbers,
   review scores, guarantees, security badges, placed next to CTAs and right after big claims.
6. **Objection handling**. Price, "will it work for me", "how hard is it to set up", "what if
   it doesn't work", "why you and not them". FAQ, comparison, guarantee, process transparency.
7. **Friction**. Form length, required fields, unclear next step, navigation that leaks
   visitors, load time, mobile layout, popups that interrupt.

For each dimension, note what is working as well as what is not. A good audit tells the user
what to keep.

## Step 3: headlines, buttons, and forms get their own pass

These three are what the user asked for and where the fastest wins live.

**Headlines.** Rewrite the main headline three ways, each with a different mechanism:
outcome ("Get X without Y"), specificity (a number, a timeframe, a named audience), and
proof-led ("Join 2,400 clinics that…"). Keep each under about 12 words. Give a matching
subheadline for the one you recommend. Explain the choice in one line.

**Buttons.** Audit every CTA for copy, placement, contrast, and the microcopy under it.
Rewrite the primary button copy as `[Action] + [What they get]` ("Start my free trial",
"Get the pricing guide", "Book a 15-minute demo"). Propose microcopy that kills the biggest
hesitation ("No credit card", "Cancel anytime", "Takes 2 minutes", "We reply within a day").

**Forms.** Count the fields and apply the cost rule from the checklist: three fields is the
baseline, four to six costs real completions, seven or more costs a lot. For every field ask
whether it is needed before you can help the person, whether it can be collected later, and
whether it can be inferred. Check labels (visible, not placeholder-only), order (easy first,
sensitive last), layout (single column), validation (inline, specific error text), the submit
button (same `[Action] + [What they get]` rule), mobile touch targets, and the trust line next
to the button. Propose the recommended form: fields, order, labels, button, microcopy.

## Step 4: write the report

Use `assets/audit-report-template.md`. The structure is fixed so findings are easy to act on:

1. **Snapshot**: page, goal, traffic, date, how the page was captured.
2. **Five-second test** result.
3. **Scorecard**: each of the seven dimensions rated 1 to 5 with a one-line reason. The rating
   is a communication device, not a measurement; say so.
4. **Quick wins (ship now)**: copy and layout changes that need no design or engineering.
5. **High-impact changes (prioritize)**: bigger changes to structure, offer, proof, or form.
6. **Headline, button, and form fixes**: the rewrites from step 3.
7. **Test ideas**: 3 to 6 hypotheses in the form "If we change X, then Y will improve,
   because Z", for when the user has enough traffic to test.
8. **Questions**: anything that would change the recommendations.

Write each finding as **Issue → Why it matters → Fix (specific, with the rewritten copy) →
Priority (High / Medium / Low) → Effort (copy / design / dev)**. Vague advice ("make the CTA
stronger") is the failure mode; the fix must be something a person can paste in.

Save the report as `cro-audit-<page-slug>-<YYYY-MM-DD>.md` in the working directory or where
the user asked, then summarize in chat: the five-second test verdict, the top three fixes,
and the recommended headline and button.

## Page-type addenda

- **Homepage**: cold visitors need positioning in the first screen; give both the ready-to-buy
  visitor and the researcher an obvious path.
- **Landing page (ads / email)**: message must match the ad or email that sent them; one CTA,
  no navigation, the complete argument on one page.
- **Pricing page**: easy plan comparison, a recommended plan, and an answer to "which plan is
  right for me"; handle the anxiety around commitment (trial, monthly, cancel).
- **Feature page**: connect the feature to the outcome and a use case, then a clear path to try.
- **Long-form sales letter**: check the sequence (problem → agitation → solution → proof →
  offer → guarantee → CTA) and that CTAs appear at every point a reader might be convinced.
- **Lead or contact form page**: the form is the page; apply the form pass in full and put the
  reassurance (response time, privacy, what happens next) beside the button.

## Ground rules

- Base findings on the page you actually saw. If you could only read the HTML and not see the
  layout, say which findings are inferred from markup.
- Rewrites must fit the brand voice visible on the page; do not turn a calm B2B page into
  hype. Offer one bolder option and label it.
- Do not promise lift numbers. Prioritize by reasoning, not invented percentages.
- Respect what works. Flag the strongest existing element so it survives the redesign.

## Related skills

- `competitor-ads-analyst` when the page needs to match what the ads promise.
- `industry-questions-research` to source objections and the customer's own words for copy.
