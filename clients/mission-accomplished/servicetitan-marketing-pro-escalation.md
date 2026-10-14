# ServiceTitan Marketing Pro + Google Ads — Escalation & Project Summary

**Client:** Mission Accomplished (HVAC) — owner **Brian C.**
**Trigger:** Bad review call **2026-07-07** (Mia Kelly, Eduardo Marinho, Brian C.). Brian paused spend.
**Scope:** How ServiceTitan Marketing Pro actually talks to Google Ads, the account diagnosis, the internal process escalation from leadership, and the open technical questions.

> Companion docs in this folder: `google-ads-log.md` (running session log, account IDs, script commands) and `google-ads-deep-analysis.md` (2026-07-02 deep-dive). This doc is the ServiceTitan/escalation thread specifically.

---

## 1. ServiceTitan Marketing Pro Ads — What It Actually Does

Marketing Pro Ads connects Google Ads + Google Analytics to ServiceTitan job/revenue data so you can see which campaigns/ad groups/keywords convert into actual booked jobs and dollars, not just clicks or calls.

**Core pieces:**
- **Google Ads + Analytics integration** — links campaigns/keywords/ad groups to jobs and revenue.
- **Dynamic Call Tracking (DNI)** — unique phone numbers per ad source, auto-attributes inbound calls (and resulting job/revenue) to the exact campaign/ad group/keyword.
- **Ads Optimizer** (paid add-on, $5.25/Qualified Lead pay-as-you-go or subscription) — imports revenue from booked jobs into Google Ads as Conversion Value ("Revenue Import"), and sends a **daily customer list** to Google to enrich targeting. This is **Customer Match** (audience enrichment), *not* Enhanced Conversions.
- **Job Value Predictor (JVP)** — per-campaign, sends *predicted* job value to Google to feed Smart Bidding before the job is even completed.

**How conversion data physically gets to Google:**
- Primarily via **Google's offline conversion upload API**, matched by **GCLID** when one exists (someone clicked an ad, landed on the site, and converted with a click ID attached).
- For **call extension clicks specifically**, there is no GCLID at all — Google doesn't pass one for a phone call. ServiceTitan instead matches by **phone number + timestamp** against what Google captured when the call extension was clicked. This is a proxy match, not a deterministic one.
- **What is NOT sent:** hashed first-party identity data (name, email, phone) tied to the conversion event itself. That's a different Google feature — **Enhanced Conversions** — and Marketing Pro does not implement it.

**Requirements/limits:** Full Marketing Pro suite package required for Ads Measurement. Only Google Ads + Google Analytics are supported (no other ad platforms yet, per ServiceTitan's public docs as of mid-2026).

---

## 2. The Data Gap: Enhanced Conversions vs. What ServiceTitan Sends

Two Google Ads features get conflated constantly. This exact confusion caused the blowup on the 7/7 call.

| | **What ServiceTitan/Marketing Pro does today** | **Enhanced Conversions (separate Google feature)** |
|---|---|---|
| Purpose | Tell Google *which click became a job/revenue* | Improve *matching* of a conversion to a real person via hashed identity |
| Data sent | GCLID (or phone+timestamp proxy) + revenue value | SHA-256 hashed name, email, phone, address |
| Where it's configured | Native to the ServiceTitan → Google Ads integration | Must be built separately — website tag/GTM (Enhanced Conversions for Web) or API/offline import (Enhanced Conversions for Leads) |
| Effect | Tells Google "this was a good/bad lead," ties $ to campaigns | Lets Google cross-reference the click to a signed-in Google Account for better bidding, especially on cookieless/iOS traffic and phone leads with no GCLID |

**Bottom line:** Even with the deepest possible conversion goal set as Primary (Completed Jobs, revenue, JVP), the only things reaching Google for optimization are click ID (or a phone/time approximation) and dollar amount — never who the person actually is. **Goal depth and data quality are two independent problems; fixing one doesn't fix the other.**

---

## 3. Case Study: Mission Accomplished Account Diagnosis

### 3.1 Source: 7/7/2026 client call (Mia Kelly, Eduardo Marinho, Brian C.)
- Brian: "all my PPC calls are spammers... I shoo every one of them out."
- Eduardo raised the Enhanced Conversions gap (hashed data not being sent), proposed fixing it.
- Brian pushed back: he already has Marketing Pro → PPC integration feeding job quality info to Google — is this duplicated effort?
- **Both were right, talking about different layers.** Marketing Pro *does* feed job outcomes to Google (true). Marketing Pro does *not* send hashed identity data (also true, and that's the separate gap Eduardo was flagging).
- Eduardo admitted the team hadn't audited how ServiceTitan specifically integrates with Google (iframe/same-origin issue blocks reading user-entered data directly off the page).
- Performance data Brian gave: **$28,000 spent, 36 opportunities, since January** → ~$1,000 CPA (by Brian's own definition: booked call/opportunity, not necessarily a completed job).
- Call ended badly. Brian paused spend, frustrated at lack of preparedness from the agency team.

### 3.2 Root cause analysis (from account audit)
- **Configuration gap (primary driver):** ServiceTitan was already sending Booked Job, Completed Jobs, and JVP data into Google Ads as conversion actions. **None were set to Primary.** Only "any unbooked call over 60 seconds, not marked Excused" was live for bidding — meaning every spam call Brian hung up on counted as a win and trained Smart Bidding to find more of the same.
- **Completed Jobs conversion action has been live since December — in 8 months it fed exactly 1 counted conversion.** Good data existed the whole time; nobody wired it into bidding.
- **Data gap (secondary, smaller issue):** Enhanced Conversions (hashed identity) is not implemented — separate fix, separate layer, per Section 2.

### 3.3 Performance numbers (YTD through 7/7/2026)
- Spend **$20.9k**, Google-reported conversions **295** → reported CPA ≈ **$71**.
- Brian's real opportunities in the same window: **36** → actual cost per real opportunity ≈ **$580**.
- June was the "best" month by Google's own metric: 100 conversions at $56 CPA — and is also the month that pushed Brian to pause, because none of those "conversions" were real leads.
- Landing page split: **99% of clicks land on the homepage**, which converts at **0.69%**; service-specific pages run **9–27%**.
- Search term leakage: irrelevant queries slipping through ("rv ac repair near me," "auto ac servicing near me") — a missing negative keywords problem, not just a tracking problem.
- Branded search is the strongest asset in the account: **12 conversions off 42 clicks, $79 CPA**, though CPC is high ($22.71). The "Mix" campaign leaks into non-branded terms — small (14 clicks/month) but worth keeping to defend the brand name.

### 3.4 Recommended plan (drafted, NOT yet sent to client)
1. Shift most budget to **LSA** (Local Services Ads) — fastest way to stabilize lead flow while the Google Ads account is fixed.
2. Keep a small **branded-only search campaign** running (best performer in the account).
3. Use the pause window to fix conversion-action configuration and negative keywords before turning PPC back up.
4. Client already paused spend — this buys time to work fixes while he gets "guaranteed" volume through LSA + remaining branded PPC.

---

## 4. Internal Process Escalation (Post Client Call)

### 4.1 Original escalation note (from leadership)
> Following the recent client escalation, we need to establish a documented process for how ServiceTitan, including Marketing Pro, will be incorporated into campaign optimization and reporting. At this time, there is no defined internal process, and the team does not currently have sufficient knowledge of ServiceTitan Marketing Pro to effectively leverage the data clients are providing.
>
> **Action Required:**
> 1. Coordinate with Ryan to determine the long-term process for monitoring and utilizing ServiceTitan data.
> 2. Identify how Marketing Pro data will be used to improve campaign performance and reporting.
> 3. Determine who will be responsible for monitoring ServiceTitan data on an ongoing basis.
> 4. Document the workflow so Client Success can accurately communicate expectations to clients.

### 4.2 Status of each item

| # | Item | Status |
|---|---|---|
| 1 | Coordinate with Ryan | **Pending** — meeting being scheduled for Friday (see Section 6) |
| 2 | Identify how Marketing Pro data will be used | **Root cause identified**, standard checklist not yet built (see Section 5) |
| 3 | Determine ownership | **Open/undecided** — proposal: PPC leads own conversion-action config day-to-day; need a dedicated owner for ServiceTitan/Marketing Pro specifically |
| 4 | Document workflow for Client Success | **Not started** — blocked on 1–3 |
| + | *(Added)* Audit other ServiceTitan/Marketing Pro clients for the same "data live, never wired to bidding" issue | **Not started** — flagged as likely not isolated to this one account |

### 4.3 Reply drafted to leadership (two tone variants prepared)
- **"Own the gap, then plan"** — leads with direct acknowledgment that the gap is real and on the team, then works through each item with status + proposed next step.
- **"Crisp status update"** — tight bullet-point status per item, root cause condensed to a short paragraph, minimal narrative.

Both cover: Ryan sync not scheduled, the two-layer root cause (config gap vs. Enhanced Conversions gap), ownership proposal, CS documentation blocked on the above, and the audit addition.

---

## 5. Resolution for Item #2: Campaign Optimization Approach

Follow-up message drafted, framed as a follow-up to the escalation reply, referencing items 2 and 3 by number.

**On conversion goal depth (topics A & B):**
- Use the **deepest Primary goal each account can support** — prioritize revenue-level conversion actions (Completed Jobs, Booked Jobs, JVP) as Primary once they clear enough volume (**~30 conversions/30 days** is the rule-of-thumb threshold for Smart Bidding to optimize reliably), rather than defaulting to contact-level signals (calls, form fills).
- **This does not mean the datastream is clean.** For job/revenue conversions, only GCLID + revenue value reach Google — not identity. Call-based conversions are weaker still, since most call-extension clicks carry no GCLID and rely on a phone-number/timestamp match. Either way, no hashed user data goes back — campaign-level optimization runs on click ID (or a phone/time approximation) and dollar amount, never on who the person actually is.
- **Goal depth and data quality are two separate levers.** Fixing conversion-action hierarchy (which goal is Primary) does not fix the identity-matching gap (Enhanced Conversions). Both need to be worked, independently.

**On Enhanced Conversions (topic C):**
- Meeting with Ryan Friday to scope what's actually possible given the ServiceTitan iframe/same-origin constraint — see Section 6.

**Process addition:**
- Add **ServiceTitan conversion event verification to the 14-day post-launch checklist** for every new Google Ads account — confirm which conversion actions are live, which are set to Primary, and whether volume is actually accruing. Goal: catch this at launch instead of 8 months in, as happened here.

---

## 6. Research: Can ServiceTitan Send User Data Around the iframe/Same-Origin Block?

**Question investigated:** Does ServiceTitan document a `postMessage`-based bridge from their scheduler widget (loaded as an iframe/overlay via `scheduler-v1.js`) to the parent page's `dataLayer`, so hashed user data (name/email/phone) could be captured as the customer fills out the ServiceTitan form and pushed into GTM for Enhanced Conversions?

**Finding: no documented postMessage feature.** Checked both help.servicetitan.io (install/config docs) and developer.servicetitan.io (API reference). Public docs cover installation only (script tags, CTA buttons, domain whitelisting) — no client-side event or postMessage hook for developers to read form field values out of the widget in real time. Cannot rule out an undocumented/partner-only feature — worth asking Ryan directly.

**Better alternative found: server-side, via the Scheduling Pro API.**
- Base URL: `api.servicetitan.io/schedulingpro/v2/{tenant}/`
- Every widget interaction is stored as a **session** in ServiceTitan, including drop-offs.
- Documented use case: *"Get a list of customers by name, phone number and/or email address that either completed their request to book through Scheduling Pro or stopped short of fully booking."*
- So the customer data isn't trapped in the iframe — it's retrievable **server-side, after the fact**, sidestepping the same-origin problem instead of fighting it client-side.

**Proposed pipeline pattern:**
1. Capture GCLID on the agency's own domain at ad-click landing (same-origin, no iframe involved — feasible today).
2. Customer completes booking inside the ServiceTitan widget as normal.
3. Server-side job pulls the completed session's customer record (name/email/phone) via the Scheduling Pro API.
4. Hash (SHA-256) and push to Google via **Enhanced Conversions for Leads**, matched to the GCLID + timestamp from step 1.

**Caveat on real-time-ness:** ServiceTitan's webhook system is mid-transition — v1 closed to new subscriptions, v2 still in development. ServiceTitan's own docs currently recommend **polling with `modifiedOnOrAfter` filters** as the interim pattern rather than relying on real-time webhook push. This affects how fast Enhanced Conversions data could reach Google after a booking — raise with Ryan.

**Scope implication:** this is a real integration build (API credentials, a server-side job, hashing pipeline), not a settings toggle. Worth widening Friday's Ryan conversation from "what does Marketing Pro send" to "do we have Scheduling Pro API access already, and what would it take to stand up a hashed-match job."

---

## 7. Full List of Open / Pending Items

1. **Ryan meeting** — Friday; agenda: (a) whether ServiceTitan has any undocumented postMessage/identity-passing option, (b) Scheduling Pro API access and feasibility of the server-side Enhanced Conversions pipeline, (c) webhook v1/v2 status and its effect on data freshness.
2. **Standard Marketing Pro audit checklist** — not yet built; per client should capture: which conversion actions exist, which are Primary, count method (One vs. Every), volume/eligibility for bidding, and whether Enhanced Conversions is worth building for that account.
3. **Ownership of ongoing ServiceTitan/Marketing Pro monitoring** — undecided; proposal on the table (PPC leads own Google Ads-side config; need a dedicated ServiceTitan-side owner).
4. **Client Success documentation/playbook** — not started, blocked on the above.
5. **Audit of other ServiceTitan-connected clients** for the same "data live, never wired to bidding" issue — not yet scoped.
6. **14-day post-launch checklist update** — add ServiceTitan conversion-event verification as a standard step (agreed, not yet implemented in the checklist doc).
7. **Mission Accomplished client plan** — LSA shift + branded-only search recommendation drafted but not yet sent to Brian; pending internal fixes to conversion-action config before re-engaging.

---

## 7b. 2026-07-21 — Decisions Made + Reply Sent to CS

Session on 2026-07-21 closed several of the open items above. **These supersede the "pending/undecided" statuses in Sections 4.2 and 7.**

### 7b.1 The exchange that triggered it
Edu posted a budget recommendation to the task (thread with **Eve**, CS; **Mia** also on it):
> "Connecting all the dots and analyzing their performance from 06/01 to today, the best and safest move is to move most of his budget to LSA (~80%), since in his AT account LSA yielded very positive results (last month's investment $2,757.26; reported revenue in ST $21,002.78). The other 20% split 50/50 between awareness (ad recall lift) on Meta and branded search on Google."

Mia pushed back: the task is about the **long-term ServiceTitan strategy**, not budget allocation. Brian wants a documented plan covering (1) how we use ServiceTitan/Marketing Pro data, (2) how it feeds optimization and reporting, (3) who monitors it, (4) how CS communicates it. She also asked whether the Ryan sync happened.

**Useful new data point from that post:** LSA on Mission Accomplished ran **$2,757.26 spend → $21,002.78 ServiceTitan-reported revenue** last month (~7.6x). That is the evidence behind the 80% LSA recommendation.

### 7b.2 Decisions locked (Edu, after speaking with Ryan)

| Item | Decision |
|---|---|
| **Ownership** (was §7 item 3, "undecided") | **The Media Buyer on the account owns ServiceTitan monitoring.** Checking ST data (revenue per campaign, per ad set) becomes part of the **optimization checklist**, so it lives inside work that already happens each cycle instead of being a standalone duty. This **replaces** the old "PPC leads own config + need a dedicated ST owner" proposal. |
| **Enhanced Conversions path** (was §6, Scheduling Pro API build) | **Peach AI.** They support Enhanced Conversions where ServiceTitan doesn't. This **retires** the server-side Scheduling Pro API pipeline as the plan of record — no API credentials, no hashing job to build. The Section 6 research stays on file in case anyone asks why we didn't build it in-house. Scope still to be brought separately; not yet approved/paid. |
| **Framing of Enhanced Conversions** | Deliberately positioned as **important but not a blocker**. The conversion-goal fix (layer one) is the immediate action and is expected to be enough to get Brian's account healthy. EC is a refinement on top. |
| **Conversion-goal rule** | "Use the deepest conversion action the account can still get ~30 conversions in 30 days on, since that's roughly what Smart Bidding needs to learn. Completed Jobs or Booked Job wherever there's enough volume, calls or form fills only on accounts too small for that." |
| **Reporting** (was not answered at all in the first drafts) | **We report off ServiceTitan numbers, not Google's.** Booked jobs + revenue from ST lead the report; Google's conversion count sits below as a platform metric. Client sees cost per real job. Note: this commits paid to pulling ST numbers into every report for ST-connected accounts — ongoing work, changes the report template. |
| **Budget rec** | Kept, but demoted to a one-line preamble: a short-term stabilizer while the account gets fixed, explicitly *not* the strategy answer. |

Open questions that **fell away** once Peach AI became the path: Scheduling Pro API access, webhook v1/v2 status, undocumented `postMessage` bridge.

### 7b.3 Final message (approved wording, sent to Eve)

> Hey Eve, for these specific points:
>
> Quick note on budget first: the LSA shift is a short term stabilizer while we fix the account, not the strategy answer. Leaving it aside for the rest of this.
>
> **1. How we use ServiceTitan and Marketing Pro data**
>
> Two layers, and they get mixed up a lot. That's part of what went sideways on the 7/7 call.
>
> Layer one is conversion depth, and this is the one that actually moves performance. Marketing Pro already sends Booked Job, Completed Jobs and Job Value Predictor into Google Ads. On Brian's account all three existed and none were set as Primary, so bidding was optimizing on "unbooked call over 60 seconds." Completed Jobs has been live since December and counted one conversion in eight months. The data was there the whole time, we just never wired it into bidding. The rule going forward is simple: we use the deepest conversion action the account can still get around 30 conversions in 30 days on, since that's roughly what Smart Bidding needs to learn. So Completed Jobs or Booked Job wherever there's enough volume, and calls or form fills only on the accounts too small for that. Fixing this on Brian's account is the immediate action and it should be enough to get the account pointed at real jobs instead of spam calls.
>
> Layer two is identity matching. Marketing Pro sends the click ID and a dollar amount, never hashed customer data. That's Enhanced Conversions, a separate Google feature that ServiceTitan doesn't offer. It's worth doing and I want it sorted so the whole picture is clean, but it's a refinement on top of layer one, not a blocker for getting Brian back to a healthy account. The path we're looking at is Peach AI, since they support Enhanced Conversions where ServiceTitan doesn't. I'll bring a scope on that separately.
>
> **2. How that data gets into optimization and reporting**
>
> During optimization, the Media Buyer will pull ServiceTitan's estimated revenue by campaign and ad group and work from that, instead of looking at Google's conversion count in isolation. Budget will move towards the campaigns producing booked jobs and revenue, away from the ones producing calls that never turn into jobs. Search terms that bring in calls but no booked work will get negated. Same logic on Meta at the ad set level. And once a revenue level conversion action has enough volume behind it, we set it as Primary so Smart Bidding optimizes straight to job value.
>
> On reporting, we report off ServiceTitan numbers, not Google's. Booked jobs and revenue from ServiceTitan lead the report, Google's conversion count sits below it as a platform metric. So the client sees cost per real job. That's the exact gap Brian ran into, Google was showing 295 conversions at $71 while he counted 36 real opportunities.
>
> On process, each ServiceTitan account gets a standard Marketing Pro audit: which conversion actions exist, which are Primary, count method, whether volume is actually coming in, and whether Enhanced Conversions is worth it there. ServiceTitan conversion checks also get added to the 14 day post launch checklist so we catch this at launch, not eight months in.
>
> **3. Ownership**
>
> The Media Buyer on the account owns it. Checking ServiceTitan data during optimization becomes part of the checklist, so it sits inside work that already happens every cycle rather than being a separate task someone has to remember.
>
> **4. Client Success**
>
> I'll put together a one pager for you two, plain language, explaining what ServiceTitan does and doesn't do, so you have something solid to point at when a client asks.
>
> Last thing, this is probably not just Brian. Worth auditing the other ServiceTitan accounts for the same "data live, never used for bidding" gap. I can scope that once the checklist is done.

### 7b.4 Drafting notes worth keeping
- Edu's edits pulled the message consistently toward **casual, connected prose** — no em dashes, no agency register, cause-and-effect spelled out rather than asserted.
- Eve and Mia **are** the CS team, so never write "a one pager CS can use" (third person about them). Write "for you two."
- "Estimated revenue" in point 2 is Edu's wording. Technically JVP is predicted and Completed Jobs is actual; he chose to keep "estimated." Not worth re-litigating.
- The first drafts answered "optimization" and silently skipped "reporting." Both were explicitly asked for. Check the ask line by line.
- Concrete verbs beat "review the data": move budget, negate search terms, set the Primary goal.

### 7b.5 Still open after this
1. **Peach AI scope** — to be brought separately; not approved, not priced, unclear whether Brian's account only or agency-wide.
2. **One-pager for CS** (Eve + Mia) — promised in the message, not written.
3. **Standard Marketing Pro audit checklist** — still not built.
4. **Audit of other ServiceTitan clients** — offered, blocked on the checklist.
5. **14-day post-launch checklist update** — agreed, not implemented.
6. **Mission Accomplished conversion-action config fix** — the actual Google Ads change; still the immediate action.
7. **Client plan to Brian** (LSA ~80% / 10% Meta ad recall lift / 10% branded search) — not sent.

---

## 8. Quick Reference / Definitions

- **GCLID** — Google Click ID; the identifier that lets Google tie a conversion back to the specific ad click, when present.
- **Enhanced Conversions for Web** — hashed first-party data sent via a website tag/GTM at the moment of conversion.
- **Enhanced Conversions for Leads** — hashed first-party data sent via API/offline import, supplementing GCLID-based offline conversion import; designed for exactly the "we have a CRM lead outside the click flow" scenario.
- **Customer Match** — a different Google feature; uploads a hashed customer list to build/enrich an *audience* for targeting. This is what Ads Optimizer's "daily customer list" send actually is — not Enhanced Conversions.
- **DNI (Dynamic Number Insertion)** — unique phone numbers assigned per ad source so inbound calls can be attributed to a specific campaign/ad group/keyword.
- **JVP (Job Value Predictor)** — ServiceTitan feature that sends *predicted* job value to Google per campaign to feed Smart Bidding before a job is completed.
