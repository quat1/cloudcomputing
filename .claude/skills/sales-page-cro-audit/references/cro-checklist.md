# CRO audit checklist

Detailed checks per dimension, plus the headline, button, and form rules. Adapted from the
methodology in Corey Haines' open-source `cro` skill (coreyhaines31/marketingskills, MIT) and
written in our own words. Use it as a checklist, not a script; skip what does not apply.

## 1. Value proposition clarity (highest impact)

- [ ] A stranger can say what the product is, who it is for, and the main benefit in five seconds.
- [ ] The benefit is specific (outcome, number, timeframe) rather than a category label
      ("the all-in-one platform").
- [ ] It is differentiated: a competitor could not paste the same sentence on their page.
- [ ] The hero image or video shows the product or the outcome, not a stock photo.
- [ ] The audience is named or unmistakable from the copy.
- [ ] The promise matches where the traffic came from (ad, search term, email subject).

## 2. Headline effectiveness

- [ ] Leads with the outcome the visitor wants, or the pain they want gone.
- [ ] Specific: numbers, timeframes, named audience, named result.
- [ ] Written in the customer's language, not internal jargon.
- [ ] Short enough to read in one glance (roughly under 12 words).
- [ ] Subheadline explains how, or adds proof; it does not repeat the headline.
- [ ] No clever-but-unclear wordplay; clarity beats cleverness every time.

Headline patterns that work:

| Pattern | Shape |
|---|---|
| Outcome without pain | "Get [result] without [the thing they hate]" |
| Specific result | "[Do X] in [timeframe]" / "[Number] [audience] use it to [result]" |
| Audience + outcome | "[Product] for [audience] who want [result]" |
| Question they already ask | "Still [doing painful thing] by hand?" |
| Proof-led | "The [category] behind [known customer or number]" |
| Contrast | "[Old way] is slow. [New way] takes [time]." |

## 3. CTA placement, copy, and hierarchy

- [ ] One primary action per page; it is obvious which button is primary.
- [ ] Primary CTA visible without scrolling, on mobile too.
- [ ] CTA repeated after each major section of argument (benefits, proof, pricing, FAQ).
- [ ] Button copy names what the visitor gets: `[Action] + [What they get]`.
- [ ] Weak defaults replaced: "Submit", "Sign up", "Learn more", "Click here", "Send".
- [ ] Microcopy under or beside the button answers the top hesitation
      ("No credit card", "Free 14 days", "Takes 2 minutes", "Reply within 1 business day").
- [ ] Contrast: the button is the most visually distinct element in its section.
- [ ] Secondary CTAs (watch demo, see pricing) look secondary (text link, outline style).
- [ ] Sticky or floating CTA on long pages, especially on mobile.

Button copy examples:

| Weak | Stronger |
|---|---|
| Submit | Get my free quote |
| Sign up | Start my free trial |
| Learn more | See how it works (2 min) |
| Download | Download the checklist |
| Contact us | Book a 15-minute call |
| Buy now | Get [product], ships today |

## 4. Visual hierarchy and scannability

- [ ] Reading only the headings tells the whole story.
- [ ] Paragraphs are short (2 to 3 lines on mobile); long blocks are broken into bullets.
- [ ] Whitespace separates sections; nothing competes with the primary CTA for attention.
- [ ] Images show the product in use or the result; captions carry a benefit.
- [ ] Consistent type scale: one H1, clear H2s, body text at a readable size (16px+ mobile).
- [ ] Order of the page follows the argument: promise → proof → how it works → objections → offer → CTA.
- [ ] Nothing important sits inside a carousel, accordion, or tab that most visitors never open.

## 5. Trust signals and social proof

- [ ] Customer logos (if B2B) near the top, recognizable to the audience.
- [ ] Testimonials are named, with role or company, and contain a specific result or a
      before/after, not "great service!".
- [ ] Numbers: customers, results, ratings, years, volume.
- [ ] Reviews from third parties (G2, Trustpilot, Google, app stores) with the score shown.
- [ ] Guarantee stated plainly, near the price or the CTA.
- [ ] Security and compliance signals where money or data is involved (payment badges, SOC 2,
      GDPR, HIPAA), placed by the form or checkout, not in the footer only.
- [ ] Proof placed right after big claims and right next to CTAs, where doubt peaks.
- [ ] Founder or team presence where trust in people matters (services, coaching, health).

## 6. Objection handling

Common objections and the page elements that answer them:

| Objection | Answer with |
|---|---|
| "Too expensive" | value anchoring, ROI math, cost of the problem, plan comparison, monthly option |
| "Will it work for me?" | use cases by segment, testimonials from similar customers, a quiz or fit checklist |
| "Too hard to set up / switch" | onboarding steps, time to value, migration help, "done for you" |
| "What if it doesn't work?" | guarantee, trial, cancel-anytime, support promise |
| "Why you and not them?" | comparison table, unique mechanism, honest "not for you if" |
| "Can I trust you?" | proof (dimension 5), real contact info, real people |
| "Not now" | reason to act now that is true (deadline, cohort, price change), or a low-commitment next step |

- [ ] An FAQ exists and answers real objections, not softballs.
- [ ] Guarantee and refund terms are easy to find.
- [ ] A "who this is not for" line, where honesty increases trust.

## 7. Friction

- [ ] Form fields: see the form section below.
- [ ] Next step after the CTA is clear ("You'll get an email in 2 minutes", "Pick a time").
- [ ] Navigation: landing pages from ads have no distracting menu; homepages keep it minimal.
- [ ] Load time is acceptable on mobile (check large hero videos and uncompressed images).
- [ ] Mobile layout: tap targets at least 44px, no horizontal scroll, CTA reachable with a thumb.
- [ ] Popups do not block the first read; exit-intent or scroll-depth only.
- [ ] No dead ends: every section leads somewhere.
- [ ] Price is findable if the audience expects it; hidden pricing is friction for most buyers.
- [ ] Required account creation before value is delivered is a major friction point.

## Forms: the detailed pass

**Field cost rule of thumb** (from the source methodology): about three fields is the
baseline; four to six fields typically cuts completions by a noticeable margin; seven or more
cuts them severely. Every field has to earn its place.

For each field ask:
1. Is it absolutely necessary before we can help this person?
2. Could we get it another way (enrichment, inference, a later step)?
3. Could we ask it later, after they have gotten value?

Field-by-field guidance:

| Field | Guidance |
|---|---|
| Email | Single field, no "confirm email"; inline validation; catch typos ("gmial.com"). |
| Name | One "Name" field usually beats First/Last; test it. Ask only if you will use it. |
| Phone | Optional unless sales will call; explain why you want it; auto-format. |
| Company | Auto-suggest or enrich from the email domain instead of asking. |
| Job title / size | Ask only for routing; use dropdowns with few options, or ask later. |
| Message | Optional; give a prompt ("What are you hoping to solve?"). |
| Dropdowns | "Select one..." placeholder; fewer than five options → use radio buttons. |
| Checkboxes | Unchecked by default; plain-language labels. |

Layout and behavior:

- [ ] Labels stay visible; placeholders are examples, not labels (they vanish on focus).
- [ ] Single column unless two fields are short and related.
- [ ] Easiest fields first, sensitive ones (phone, budget) last.
- [ ] Validate when the visitor leaves a field, not on every keystroke; errors are specific
      ("Please enter a valid email, like name@company.com", not "Invalid input").
- [ ] On submit errors, focus the first problem and keep everything they typed.
- [ ] Multi-step when there are more than five or six fields, distinct sections, or branching;
      show progress, allow going back, mark required vs optional.
- [ ] Submit button: `[Action] + [What they get]`, full width on mobile, sticky if the form is long.
- [ ] Reassurance beside the button: privacy line, response time, "no spam", "no credit card".
- [ ] Mobile: correct keyboard types (email, tel, number), autofill enabled, 44px targets.
- [ ] After submit: a confirmation that says what happens next, and a next step (book a time,
      read this, check your inbox).

Measure: form start rate, completion rate, drop-off by field, error rate by field, time to
complete, mobile vs desktop.

## Experiment ideas by page type

Write each as a hypothesis: "If we [change], [metric] will improve because [reason]."

- **Hero**: specific vs abstract headline; product screenshot vs illustration; video vs static;
  single CTA vs two; social proof in the hero vs below.
- **Pricing**: monthly vs annual default; three plans vs two; "most popular" badge; showing the
  price vs "contact sales"; adding a guarantee near the price.
- **Form / demo request**: fewer fields; two-step form; calendar embed instead of a form;
  "what happens next" copy; removing phone.
- **Landing page**: ad-copy headline match; removing navigation; shorter vs longer page;
  testimonial placement next to the CTA.
- **Site-wide**: sticky CTA; exit-intent offer; live chat vs none; trust badges near CTAs.
