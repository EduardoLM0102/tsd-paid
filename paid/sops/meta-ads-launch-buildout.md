# Meta Ads — New Campaign Launch & Buildout (One-Time Process)

**Owner:** Paid Ads Division (Eduardo)
**Built in:** AT
**Version:** 1.2 — Jul 2026

---

## Stage map

| # | Stage | Owner | Blocks the next stage? | Target time |
|---|---|---|---|---|
| 1 | Client Info | Account Manager | Yes — hard gate | 3 business days |
| 2 | Access & Assets Check | Paid Ads | Yes | 1 business day |
| 3 | Tracking & Lead Flow Setup | Paid Ads + Mo (GHL) | Yes | 2 business days |
| 4 | Market, Offer & Audience Research | Paid Ads | Yes | 2 business days |
| 5 | Creative Production (conversion + awareness) | Design (Héctor) · Video (Vince) | No — runs parallel to 6 | 2 business days |
| 6 | Destination — Native Form or Landing Page | Paid Ads (native form) · Web/Mo (page, **when applicable**) | Yes | 1 day (native) / 4 days (page) |
| 7 | Campaign Buildout in Meta | Paid Ads | Yes | 1 business day |
| 8 | Pre-Launch QA + Lead Flow Test | Paid Ads + Mo | Yes — hard gate | 1 business day |
| 9 | Launch | Paid Ads | — | Same day |
| 10 | 3-Day Check (one-time) | Paid Ads | — | Day 3 |
| 11 | 7-Day Check (one-time) | Paid Ads | — | Day 7 |

Stages 5 and 6 run in parallel once Stage 4 closes. Stage 7 cannot start until both are done.

**Critical path:** 1 → 2 → 3 → 4 → (5 ‖ 6) → 7 → 8 → 9.

**Launch window:** the destination decides it. A native Meta lead form build (our default in most accounts) has no Web dependency and lands in roughly 6–8 business days from a complete intake. A build that needs a new landing page adds the Web/GHL lead time on top. *(These durations are Paid Ads estimates, not measured cycle times — they should be re-baselined once we have real data from the first builds.)*

---

## STAGE 1 — Client Info
**Owner:** Account Manager · **Blocks everything downstream**

### 1.0 — Start from AT
The AM opens the client record in AT, confirms what's already there is current, and collects whatever is missing from the client.

The fields below are the full requirement. The stage cannot close with anything still missing — with every field filled, the ads team builds the campaign end to end without going back to the client or the AM.

### 1A. Business & offer
- **Services to advertise on Meta** (be specific: "AC replacement" not "HVAC")
- **The offer.** Exact promo, discount, financing, or guarantee we can put in the ad. If there is no offer, write "no offer — advertise service only." Vague is not acceptable ("great service" is not an offer).
- **Offer expiration / seasonality**, if any.
- **Average ticket** for the advertised service.
- **What the client will NOT say** in an ad (compliance, brand, price claims they won't back).
- **Top 3 competitors** and what the client believes makes them different.
- **Proof assets:** review count and rating, years in business, licenses, awards, warranty terms, financing partner.

### 1B. Targeting
- **Service area:** ZIP codes or cities the client will actually drive to. Not "the whole metro."
- **Any area they refuse to serve.**
- **Customer profile:** homeowners only? Age of homes? Commercial included? *(Context for the offer and the creative. It does not become an audience filter — see the targeting doctrine in 7.2: geo only, Advantage+ everywhere.)*

### 1C. Budget & goal
- **Monthly Meta ad spend** (written client approval — this is the hard rule; no budget moves without it).
- **Target cost per lead**, or, if unknown, the client's close rate and what a lead is worth.
- **Primary goal:** phone calls or form leads. Pick one as primary.
- **Lead capacity:** how many leads per week can they actually handle and call back? Do they answer the phone on weekends?

### 1D. Assets & access
- **Meta Business Manager + Ad Account access confirmed** (yes/no). If no → fires "Create Meta Ads Account" process.
- **Facebook Page and Instagram account** connected to the ad account.
- **Meta Pixel / Conversions API** — exists? installed where?
- **Photos and video from the client:** real job photos, trucks, crew, before/after, owner on camera. Ask for the raw folder — this is what makes Meta work in home services.
- **Logo, brand colors, brand guide.**
- **Destination:** native Meta lead form (our default), an existing landing page URL, or a page we need to build. Paid Ads makes this call in Stage 4 — the AM only needs to say whether a page already exists.
- **CRM:** GHL sub-account confirmed? Who receives the lead notification (name, phone, email)?

**Closeout:** AM marks complete. AT fires Stage 2 to the Paid Ads division. Paid Ads reviews the form within 24h and either accepts it or bounces it back with the specific missing fields (bounce goes to the AM, not the client).

---

## STAGE 2 — Access & Assets Check
**Owner:** Paid Ads (media buyer)

1. Log into Meta Business Manager. Confirm we have **Admin** on the Ad Account, the Facebook Page, the Instagram account and the Pixel/Dataset. Partner access, not personal access.
2. Confirm the ad account has a **valid payment method** and no spend limit or policy restriction blocking us. *(Billing on paid accounts is the Division Head's — flag to Eduardo, do not ask another team to check it.)*
3. Confirm the ad account is not **restricted or in review**. If it is, that's a Critical ticket, escalate same day.
4. Download the client's photo/video folder into the client's asset drive.
5. Check the account history: what ran before, what worked, what the previous CPL was. Screenshot the last 90 days for the record.

**Branch:** any missing access or missing account → fire the "Create Meta Ads Account / Request Access" process and put this task on hold. Do not skip forward.

**Closeout:** checklist all green, 90-day history screenshotted into the client folder.

---

## STAGE 3 — Tracking & Lead Flow Setup
**Owner:** Paid Ads · **Dependency:** Mo (GHL) — must be requested at the start of this stage, not at the end

This stage exists because a launched campaign with broken tracking is worse than no campaign.

1. **Pixel / Conversions API** installed on the site and firing. Verify with Meta Events Manager (Test Events), not by assumption.
2. **Standard events defined:** `Lead` for form submits, `Contact` for calls. One event per real conversion. No duplicate events, no page-view-as-conversion.
3. **Call tracking:** CallRail (or ServiceTitan) number provisioned for Meta and passed back into the CRM. Calls from Meta must be identifiable as Meta.
4. **Lead routing:** form submits land in GHL, notify the right person, and trigger the client's follow-up automation.
5. **Conversion goal in the ad account** points to the correct event. Not "any lead event in the account."

**GHL gate:** if any part of the lead flow touches GHL, Mo runs the joint test and marks **Verified Live** in the ticket. Nothing gets called "live" to the client before that.

**Closeout:** a screenshot of a test event firing in Events Manager + Mo's Verified Live on the ticket. This is a hard gate — Stage 4 does not open without it.

---

## STAGE 4 — Market, Offer & Audience Research
**Owner:** Paid Ads · **Output: the Campaign Brief** — this is what Design works from, and what the ad copy is written against in Stage 7

Deliverable is a one-page brief in the client folder, containing:

1. **Does this account already have proven winners?** Check for isolated post IDs from previous campaigns that still perform. This single answer decides the whole build:
   - **No proven winners** → the account launches **100% testing** (see Stage 7).
   - **Proven winners exist** → the winners keep running in their isolated ad sets and testing runs alongside them, on a smaller share of budget.
2. **Who we're talking to** and what state they're in when they see the ad (emergency need vs. planning a replacement vs. no idea they need us yet).
3. **The angles we're testing.** Each angle is a distinct offer or promise — price/financing, speed of service, trust/local proof, pain, seasonal urgency. **One angle = one DCT ad set.** The angles compete against each other as parallel ad sets inside the CBO. This is what we're actually testing: which offer/angle the market wants. We are not testing layouts.
4. **The hypothesis, one per angle.** Written as: *"We believe [audience] responds to [angle] because [reason]. We'll know we're right if [metric] beats [threshold]."*
5. **Competitor scan:** pull the client's top competitors in the Meta Ad Library. What are they running, how long has it been running (long-running = it works), what are they promising.
6. **Proof to put in the creative:** the specific reviews, numbers, photos we'll use.
7. **Budget split** for this client (see the Stage 7 standard).
8. **Conversion creative spec for Héctor:** **3 creatives per angle**, all in the same format. The 3 are *iterations of that one angle* — different executions of the same promise, not three different promises. Total = 3 × number of angles. Specify which photos to use for each.
9. **Awareness creative spec (separate brief):** video and statics built specifically for **branding and brand recall**, never recycled conversion ads. Video comes from Vince, statics from Héctor.
10. **Destination route** (native form / existing page / new page) — this is what branches Stage 6.

**Closeout:** brief approved by Eduardo. AT fires Stages 5 and 6 in parallel.

---

## STAGE 5 — Creative Production (parallel)
**Owner:** Design (Héctor) · Video for awareness: Vince · **Input:** the Campaign Brief from Stage 4

Two distinct creative sets come out of this stage. They are not interchangeable.

### 5A — Conversion creative (for the DCT ad sets)
- **3 creatives per angle, all in the same format.** The 3 are iterations of the same angle — different executions of one promise, not three different promises. The angle is what we're testing; the iterations exist so the algorithm can find the best expression of it.
- Format is fixed across the test. Mixing formats turns format into an uncontrolled variable and contaminates the read.
- Real photos of the client's crew, trucks and jobs beat stock. Always.
- Text on image stays short and readable on a phone.

### 5B — Awareness creative (for the Ad Recall Lift campaign)
- **Purpose-built for branding and brand recall.** Video (Vince) plus statics (Héctor), designed to be remembered, not to be clicked.
- **Never a recycled conversion ad.** A discount ad running on a recall objective is a wasted impression.
- Carries the brand: name, face, trucks, market position. No hard offer.
- Formats per the division standard: 16:9 master with cutdowns to 4:5 and 9:16.

Both sets: creative naming follows the TSD convention so we can read performance without opening the ad. Delivered to the client's asset folder + AT task.

**Target:** 2 business days from the brief. Delivery must land with at least **1 business day of headroom** before the buildout date, so Paid can review and request one round of fixes.

**Closeout:** files delivered in the required formats, named correctly, in the client's asset folder and on the AT task.

---

## STAGE 6 — Destination: Native Lead Form or Landing Page (parallel)
**Owner:** depends on the route below · Paid Ads picks the route in Stage 4

Three routes. AT branches the task accordingly.

### Route A — Native Meta lead form (the default)
Most of our builds run on Meta's native form. No Web dependency, no page to wait on, and the lead flow is shorter.

- **Owner:** Paid Ads. Built inside Meta as part of the campaign.
- Form fields: name, phone, ZIP, service needed. Nothing else — every extra field costs leads.
- Use the **higher-intent** form type, not the fastest one. Add a review/confirm step so we don't buy misdials.
- One qualifying question max, and only if it actually changes how the client works the lead.
- Custom thank-you screen with a click-to-call button — a lead that calls immediately closes at a different rate than one we call back.
- **Leads must flow into the CRM automatically.** Native form leads that sit inside Meta are lost leads. The GHL (or CallRail/ServiceTitan) integration is set up here and tested in Stage 8. If GHL is in the path, Mo runs the joint test and marks **Verified Live**.

### Route B — Existing landing page
Stage 1D says a page already exists and it converts. Paid Ads verifies it: mobile speed, click-to-call, form fields, and tracking firing. If it fails any of those, it becomes Route C.

### Route C — New landing page (**when applicable**)
Only when the offer genuinely needs a page (high-ticket, financing, long proof, or the client wants the traffic on their site).

- **Owner:** Web (Justin) for a site page, Mo for a GHL funnel.
- Paid Ads writes the requirements: offer, headline, proof, form fields, thank-you behavior, tracking to install.
- Same form-field rule as Route A. Mobile load under 3 seconds. Click-to-call in the header.
- Pixel + Conversions API firing on the page and on the thank-you.
- **Dependency deadline:** page live **4 business days before** the buildout date, so Stage 8 tests the real flow and not a mockup.

**Closeout (any route):** the destination exists, tracking is verified, leads reach the CRM, and Mo's Verified Live is on the ticket if GHL is in the path.

---

## STAGE 7 — Campaign Buildout in Meta
**Owner:** Paid Ads · Requires Stages 5 and 6 complete · **Ad copy is written in this stage**

### 7.1 — The TSD Meta method

**Budget is always CBO.** Campaign-level budget, never ad-set budgets. The algorithm decides where the money goes, and that decision is itself the test signal (see 7.5).

**One angle = one DCT ad set.** This is the core of the method. Each Dynamic Creative ad set carries **a single angle**, expressed in:

- **3 creatives** — same format, three *iterations of that one angle*
- **2 headlines** — for that angle
- **2 primary texts** — for that angle

Inside the ad set, Meta finds the best expression of the angle. Across ad sets, the CBO decides **which angle deserves the money**. That's the question we're actually paying to answer: **which offer/promise the market responds to.** We are not optimizing layouts — aiming that small tells us nothing worth scaling.

Angles run **alongside each other** as parallel DCT ad sets in the same CBO campaign, and compete for the budget.

**The account starts in one of two states**, per Stage 4:

**State A — No proven winners in the account (a fresh account, or nothing from past campaigns is worth keeping).**
The account runs **100% testing**. There is nothing to scale yet, so we don't pretend there is.

- One CBO conversion campaign, optimizing for the conversion event verified in Stage 3.
- One DCT ad set per angle, running in parallel.
- Targeting and placements: per 7.2 — geo only, Advantage+ everywhere.

**State B — The account already has isolated winners.**
The proven post IDs keep running in their own isolated ad sets inside the CBO. New DCT ad sets (one per new angle) run alongside them on a smaller share of budget, feeding the next generation of winners.

### 7.2 — Targeting doctrine: Advantage+ everywhere, geo only

**Advantage+ on everything. No exceptions.** Audience, placements, campaign-level automation. The platform's machine learning finds the buyer far better than a manual guess does, and every manual restriction we add is a constraint on a system that is better at this than we are. Leveraging Meta's AI is not a preference here, it's the doctrine.

**Never use interest targeting, behaviors, or any detailed targeting.** Not as a "starting point," not "just to narrow it a bit." An interest layer tells the algorithm to look in a box we drew from a hunch, and it will obey — that's exactly the problem.

What we are allowed to define:

- **Geo** — the service area from Stage 1B. **People living in this location**, never "recently in."
- **Age — as a suggestion only** (Advantage+ audience suggestion), and only when the client's customer profile genuinely calls for it. Advantage+ treats it as a signal and is free to go outside it when the data says so. That's intended.

That's the whole targeting spec. If a campaign is underperforming, the fix is the offer, the angle or the creative — never a tighter audience.

### 7.3 — Ad copy (written in this stage)
Copy is not a separate hand-off. Written by the media buyer here, against the Campaign Brief, while building the ads. The method dictates the quantity:

- **Exactly 2 primary texts and 2 headlines per angle** — i.e. per DCT ad set. Three angles means three sets of 2+2. Not one, not five: the Dynamic Creative matrix is built on this.
- Both must argue **the same angle** as that ad set's creatives. Copy from another angle inside the ad set destroys the read — the ad set must win or lose on one promise.
- Within the angle, the two must be genuinely different takes, not the same sentence reworded. Two versions of the same line waste a test slot.
- Written for the awareness state in the brief, not generic.
- The offer appears exactly as the client gave it in Stage 1A. No invented claims, no invented pricing.
- Nothing the client said they will not say (Stage 1A).
- CTA matches the primary goal (call vs. form).
- The copy lives in the AT task, not in Slack.

### 7.4 — Isolating winners (post ID isolation)
This is how a test becomes a scaling asset, and it happens **after** the test has collected enough data to be meaningful (first read at Stage 11).

- Pull the **post IDs** of the winning combinations out of the Dynamic Creative ad set.
- Launch each winner as its own ad, using the same post ID, so it keeps its accumulated social proof (likes, comments, shares). **Never rebuild a winner as a new ad — that throws away the engagement and restarts the learning.**
- The isolated winners keep running in the CBO. New testing continues in parallel, on a smaller budget share, and every new winner gets isolated the same way.

### 7.5 — Kill rules (how the algorithm votes)
In a CBO, **spend is the vote** — at both levels. Meta has already decided what deserves to be shown, and we read that decision instead of arguing with it.

**Level 1 — the angle (the ad set).** The CBO distributes budget across the DCT ad sets. The angle that doesn't attract spend lost to the others. That is the answer to the question we asked.

**Level 2 — the combination (inside the surviving ad set).** Within an angle that is taking budget, the winning creative/headline/copy combinations are the ones the algorithm feeds.

At either level, it **dies** when:
- **It didn't spend.** The algorithm found it irrelevant next to the others. No spend, no case.
- **It spent very little.** Same verdict, weaker version.
- **It spent but produced only 1–2 leads** — or, in an account that already has isolated post IDs running, produced few leads relative to the account's total lead volume.

It **survives and gets isolated** when it took real spend and produced lead volume that stands up next to the rest of the account.

**Read window:** the first read happens at Stage 11 (day 7). Do not kill or isolate before the data can carry the decision — an early kill is just noise with a confident tone.

### 7.6 — Awareness campaign (always on, in parallel)
Every account runs an **Awareness campaign alongside the conversion CBO**. This is not optional and it is not a leftover budget line — it's the Brandformance layer: the ads don't create the authority, they amplify it, and the conversion campaign converts cheaper into a market that already recognizes the brand.

- **Objective: Awareness, optimized for Ad Recall Lift.** Not reach, not impressions, not traffic. We are buying the memory, so we optimize for the metric that measures it (Estimated Ad Recall Lift).
- **Budget:** 5–10% of total, per the division standard. Accelerator and Dominator can carry a heavier BED overlay per the Brandformance rules.
- **Creative is purpose-built for branding and brand recall** — video plus statics designed for it. This is a **separate creative brief for Héctor and Vince**, not the conversion creatives recycled. A direct-response ad optimized for recall is a wasted impression.
- Brand assets carry the things a recall ad must land: the name, the face, the trucks, the market position. No hard offer, no discount chase.
- Retargeting (site visitors, video viewers, engagers, customer list) also lives here, running proof and trust.
- **Do not judge this campaign by CPL.** It has none, by design. It's read on recall lift, frequency and reach in the service area — and indirectly, on what happens to the conversion campaign's CPL over time.

**Naming convention:** every campaign, ad set and ad follows the TSD standard so an AM or the client can read the account without a translator. *(Note: the division-wide naming convention is still being finalized — this SOP will point to it once locked.)*

### 7.7 — Buildout checklist
1. Build the **conversion CBO**. Campaign-level budget, never ad-set budgets.
2. **One DCT ad set per angle**, each loaded with 3 creatives (same format, iterations of that angle), 2 headlines and 2 primary texts **of that angle**. No cross-contamination between ad sets.
3. If the account has proven post IDs, rebuild their isolated ad sets in the CBO **with the original post IDs**.
4. Build the **Awareness campaign** in parallel: objective Awareness, optimized for **Ad Recall Lift**, with the branding creative (7.6).
5. Geo set to the exact ZIPs/cities from Stage 1B. **People living in this location**, not "recently in."
6. Exclude the areas the client refuses to serve.
7. Conversion event = the one verified in Stage 3.
8. Every ad has the correct destination and UTMs.
9. Schedule: if the client doesn't answer the phone on weekends (Stage 1C), restrict the schedule accordingly.
10. Budget split: 90–95% conversion, 5–10% awareness. Total = the approved monthly figure ÷ 30.4. Nothing above what the client approved in writing.
11. Leave everything **paused**. Nothing goes live before Stage 8.

**Closeout:** both campaigns built and paused, ready for QA.

---

## STAGE 8 — Pre-Launch QA + End-to-End Lead Flow Test
**Owner:** Paid Ads · **Dependency:** Mo, if GHL is in the flow · **Hard gate — nothing launches without it**

This is a TSD hard rule: **the lead flow is verified end to end before any lead-gen campaign goes live.**

**QA checklist (a second set of eyes, not the person who built it):**
- [ ] Ad preview renders correctly on mobile, feed, reels and stories.
- [ ] Every link works and carries UTMs.
- [ ] Geo, budget, schedule and conversion event match the intake form.
- [ ] **No interest or detailed targeting anywhere.** Geo only, Advantage+ on. Age present only as a suggestion, if at all.
- [ ] Budget sits at the **campaign** level (CBO). No ad-set budgets.
- [ ] Each DCT ad set carries **one angle only** — its creatives, headlines and primary texts all argue the same promise.
- [ ] Offer in the ad matches the offer from the intake. Word for word.
- [ ] Naming convention is correct.
- [ ] No ad is stuck in policy review.

**Live lead test:**
- [ ] Submit a real test lead through the actual ad destination — the native form itself if that's the route, not a page we didn't build.
- [ ] Lead lands in GHL / CRM. **Native form leads must arrive in the CRM automatically** — a lead sitting inside Meta is a lost lead, and this is the single most common way a native-form launch quietly fails.
- [ ] The client's team gets the notification they'll get in production.
- [ ] The conversion event fires in Events Manager and shows up in the ad account.
- [ ] Test call placed through the tracking number, shows as a Meta call.
- [ ] Test lead deleted / marked as test in the CRM.
- [ ] **Mo marks Verified Live** if GHL is involved.

**Closeout:** QA checklist signed in AT with the screenshot of the test conversion. No screenshot, no launch.

---

## STAGE 9 — Launch
**Owner:** Paid Ads

1. Unpause. Record the exact launch date/time in the AT task and in the client's Meta log.
2. Log the hypotheses from Stage 4 in the client's Meta log, so the 3-day and 7-day checks are measured against something we wrote down before we knew the answer.
3. **Notify the AM in Slack** the same day: live, budget, what we're testing, when the first read happens, what they can tell the client. The AM communicates to the client — Paid does not.

**Closeout:** live, logged, AM notified.

---

## STAGE 10 — 3-Day Check (one-time, attached to this build)
**Owner:** Paid Ads · Fires 3 days after launch

Purpose: confirm delivery is healthy. **Do not judge creative winners yet — there isn't enough data.**

- Is it spending the daily budget? If not: budget too low, audience too narrow, or ads in review.
- Is it out of the learning phase, or on track to exit?
- Are conversions being *recorded* (not "are they good")? If we have spend and zero recorded events, tracking is broken — that's a Critical, fix it today.
- Frequency, CPM and CTR sane vs. the account's history?
- Any ad rejected or ad set with zero delivery?

**Action rule:** fix delivery and tracking problems. Do not touch creative or budget for performance reasons yet — resetting learning at day 3 destroys the test.

**Closeout:** log the read in the client's Meta log. Slack DM the AM within 2h if anything found needs the client to know.

---

## STAGE 11 — 7-Day Check (one-time, attached to this build)
**Owner:** Paid Ads · Fires 7 days after launch · **This closes the launch process**

Purpose: the first real read on the Dynamic Creative test, using the kill rules in 7.4.

- CPL vs. the target from Stage 1C.
- **Read the spend distribution first — at the ad set level.** The CBO already voted on which *angle* deserves the money. That's the primary answer: which offer/promise the market wants.
- Then read **inside** the surviving angles: which creative / headline / primary text combinations the algorithm fed.
- **Kill** at both levels, per 7.5: didn't spend, barely spent, or spent while returning only 1–2 leads (or few leads relative to the account's total volume, when isolated post IDs are already running).
- **Isolate** the winners: pull their post IDs into their own ad sets inside the CBO, reusing the original post ID so the accumulated social proof comes with them (7.4).
- One change at a time, so we know what caused what.
- **Write the next hypothesis** and open the Design task for the next round — new angles to test as new DCT ad sets, or new iterations of the angle that won.
- **Awareness campaign:** do not read it on CPL. Check Estimated Ad Recall Lift, reach and frequency in the service area.
- Lead quality check with the AM: are the leads real, and is the client calling them back?

**If the data can't carry the decision yet, do not force it.** Extend the test rather than isolate a winner that isn't one. A premature isolation is how an account ends up scaling noise.

**Closeout:** the launch process ends here. The recurring **7 / 14 / 30-day optimization processes** take over from this point, plus the standard division SOPs (A1 Weekly Optimization, A4 Friday Pulse).

---

## Dependency summary (for the AT build)

| Dependency | Who | Needed by | Lead time |
|---|---|---|---|
| Client info complete (AT + any gaps collected) | Account Manager | Stage 2 | Blocks the whole build |
| Written budget approval | Client, via AM ticket | Stage 7 | Blocks launch |
| GHL lead flow + Verified Live | Mo | Stage 3 and Stage 8 | 2 days |
| Conversion creatives (3 per angle) | Design (Héctor) | Stage 7 | 2 days from the brief, 1 day of headroom before buildout |
| Awareness creatives (branding video + statics) | Vince (video) · Héctor (statics) | Stage 7 | Same window — separate brief, not recycled conversion ads |
| Landing page — **only when applicable** (Route C) | Web (Justin) or Mo | Stage 8 | 4 days before buildout |

Most builds run on the native Meta lead form and carry **no Web dependency at all**. Only Route C in Stage 6 pulls Web into the critical path.

**Escalation:** any dependency that misses its deadline goes to the AM (not to the other division head) per MasterOps — the AM coordinates cross-division work. A dependency blocking a launch date the client already knows about is escalated to the COO.
