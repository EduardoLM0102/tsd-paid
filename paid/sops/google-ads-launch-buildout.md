# Google Ads (PPC) — New Campaign Launch & Buildout (One-Time Process)

**Owner:** Paid Ads Division (Eduardo)
**Built in:** AT
**Version:** 1.0 — Jul 2026
**Scope:** Search PPC (Branded + Non-Branded).

<p class="note">Performance Max is not part of the initial launch (see Stage 7.7).</p>

---

## Stage map

| # | Stage | Owner | Blocks the next stage? | Target time |
|---|---|---|---|---|
| 1 | Client Info | Account Manager | Yes — hard gate | 3 business days |
| 2 | Access, Billing & Account Health | Paid Ads | Yes | 1 business day |
| 3 | Conversion Tracking + **End-to-End Lead Flow Test** | Paid Ads + Mo (GHL) | Yes — **hard gate** | 2–3 business days |
| 4 | Keyword, Offer & Competitor Research | Paid Ads | Yes | 1 business day |
| 5 | Ad Copy & Assets (RSAs, extensions) | Paid Ads | No — parallel to 6 | 1 business day |
| 6 | Landing Page / Destination | Web (Justin) or Mo | Yes | 4 business days (**when applicable**) |
| 7 | Campaign Buildout in Google Ads | Paid Ads | Yes | 1 business day |
| 8 | Pre-Launch QA | Paid Ads | Yes — **hard gate** | 1 business day |
| 9 | Launch | Paid Ads | — | Same day |
| 10 | 3-Day Check (one-time) | Paid Ads | — | Day 3 |
| 11 | 7-Day Check (one-time) | Paid Ads | — | Day 7 |

Stages 5 and 6 run in parallel once Stage 4 closes. Stage 7 cannot start until both are done.

**Critical path:** 1 → 2 → 3 → 4 → (5 ‖ 6) → 7 → 8 → 9.

**Launch window:** roughly 7–10 business days from a complete intake when the client already has a working destination. A client who needs a new landing page adds the Web lead time on top — Search cannot run without a destination. *(Estimates, not measured cycle times — re-baseline after the first builds.)*

---

## The two rules that govern this whole process

**1. Fix the measurement before you spend the money.** No bidding strategy, no scaling, no budget move until the conversion signal is trustworthy. A campaign optimizing toward a polluted goal will faithfully buy the wrong thing, and it will look like it's working. Stage 3 is a hard gate for exactly this reason.

**2. Never read or report a blended number.** Branded and non-branded get split before any CPL is spoken out loud, internally or to the client. A blended CPL sells the client a number that is structurally unrepeatable — brand converts cheap and always would; it hides whether non-brand is alive or dead.

---

## STAGE 1 — Client Info
**Owner:** Account Manager · **Blocks everything downstream**

### 1.0 — Start from AT
The AM opens the client record in AT, confirms what's already there is current, and collects whatever is missing from the client.

The fields below are the full requirement. The stage cannot close with anything still missing.

### 1A. Services & offer
- **Services to advertise, in priority order.** These become the ad groups. Be specific: "AC replacement," "furnace repair," "water heater install" — not "HVAC."
- **Services the client does NOT want leads for.** These become negative keywords on day one.
- **The offer**, exactly as it can appear in an ad (promo, financing, guarantee, free estimate). If there is no offer, say so.
- **Average ticket** per advertised service.
- **What the client will NOT say** (claims, pricing, guarantees they won't back).
- **Brand terms:** every way people spell or misspell the client's name, plus any DBA. Needed to build the branded campaign and to cross-negative it.
- **Top competitors by name.** Used for the negative list, and later for conquesting.

### 1B. Service area
- **Service hubs:** the cities/addresses the crews actually dispatch from, and how far each will realistically drive. Radius targeting is built as **proximity circles around hubs**, not one blob over a metro.
- **Areas they refuse to serve.**

### 1C. Budget, goal & capacity
- **Monthly Google Ads spend**, with **written client approval**. Hard rule — no budget moves without it.
- **Target cost per lead.** If unknown: close rate and value of a job, so we can derive it.
- **Primary lead type:** phone calls or form fills. Decides what we optimize for.
- **PHONE ANSWERING HOURS — mandatory, no default.** Exact days and hours a human answers, including weekends. This is a **required** field: the build does not close without it. If nobody answers at a given time, clicks bought at that time structurally cannot convert, and the fix is an **ad-schedule restriction** (smart bidding ignores schedule bid modifiers — a restriction is the only lever that works).
- **Lead capacity:** how many leads per week can they actually work?

### 1D. Tracking, CRM & destination
- **Google Ads account:** exists? Access grantable to the MCC? If not → fires "Create Google Ads account" process.
- **CRM:** ServiceTitan / GHL / other. **Which system is the source of truth for a call, and which for a form.**
- **Call tracking:** CallRail / ServiceTitan numbers, and who owns them.
- **GA4 property** and access.
- **Destination:** existing landing page(s) for each service, or "we need to build one."
- **Who receives the lead notification** (name, phone, email).

**Closeout:** AM marks complete. Paid Ads reviews within 24h and either accepts or bounces it back with the specific missing fields (bounce goes to the AM, never to the client).

---

## STAGE 2 — Access, Billing & Account Health
**Owner:** Paid Ads (media buyer)

1. **MCC access** to the Google Ads account, at the right level. Confirm access to GA4 and to the conversion tracking source.
2. **Billing is alive.** Check `customer.status`, the billing setup, and the **date of the last impression**. An account can sit "active" in the UI while serving nothing because of a payment hold — and budget increases pushed into a dark account do nothing at all. This check exists because it has already happened to us.
3. **Account inventory.** List every campaign, including paused ones. Look specifically for:
   - **Zombie campaigns:** ENABLED with a live budget but not serving only because of an end date or a disapproval. One date edit and they outspend the account. Flag and pause.
   - Dead campaigns from a previous agency, to be archived (with client/AM awareness).
   - Existing shared negative lists, and whether they are actually attached to anything.
4. **90-day history:** what ran, what the CPL was, what the conversion actions were. Screenshot for the record. This is the baseline we will be judged against.
5. **Billing on paid accounts is the Division Head's.** Payment holds, declined cards, stopped accounts → flag to Eduardo. Do not delegate the check.

**Branch:** no account or no access → fire the "Create Google Ads Account / Request Access" process and hold this one.

**Closeout:** access confirmed, billing verified live, account inventory and 90-day baseline in the client folder.

---

## STAGE 3 — Conversion Tracking + End-to-End Lead Flow Test
**Owner:** Paid Ads · **Dependency:** Mo (GHL) — requested at the **start** of this stage · **HARD GATE**

The deepest doctrine in the division. Smart bidding will optimize toward whatever we tell it a conversion is. If we lie to it, it will efficiently buy garbage, and the report will look fine.

**The lead flow is tested here, not at the end.** We prove the whole path works — click to lead to CRM to the client's phone — *before* anyone writes an ad or builds a campaign. Testing it at the end means discovering a broken path after a week of work is already sunk into it.

### 3.1 — One source of truth per lead type
- **Calls:** one system owns the connected call (ServiceTitan connected call, or CallRail). One.
- **Forms:** one system owns the genuine form lead (GHL / ServiceTitan booked job).
- Everything else gets demoted. Never leave the same phone call flowing through two or three parallel pipes — it double or triple counts, inflates the conversion number, and understates the true CPA.

### 3.2 — Primary vs Secondary
- **Primary = the real lead action only.** These are the actions smart bidding optimizes toward.
- **Secondary (reporting only):** Google Business "Local actions" (website visits, directions, map taps), GA4 micro-clicks (`phone_link_click`, `button_click`, page views), and any duplicate call pipe. These are not leads.
- An account where micro-clicks are Primary and the CRM call is Secondary is not "working" — it works by luck of which action fires first, and it will break.

### 3.3 — Counting rules
- Lead actions count **ONE_PER_CLICK**. MANY_PER_CLICK lets repeat callers inflate the signal.
- Correct **category** on each action (a form fill is not a PURCHASE).
- Delete or disable conversion actions that **have never fired**. They are noise pretending to be signal.

### 3.4 — End-to-end lead flow test (the gate)
Division hard rule: **the lead flow is verified end to end before any lead-gen campaign goes live.** We do it here.

- [ ] **Test form:** submit a real lead through the destination that will receive the traffic. It lands in the CRM.
- [ ] **Test call:** place a real call through the tracking number. It lands in the CRM and is attributable to Google.
- [ ] Both appear in Google Ads as the **Primary** action — the one smart bidding will optimize toward.
- [ ] The client's team receives the notification they'll get in production.
- [ ] Test lead removed / marked as test in the CRM.
- [ ] Screenshot the test conversions into the AT task. No screenshot, no gate.

### 3.5 — Verify against physical reality
- **Reconcile against the CRM.** Pull the real lead count from ServiceTitan/GHL for a known window and compare it to what Google reports. If Google says 390 and the CRM says 40, we do not have a performance story — we have a tracking failure, and no bidding decision may be made on top of it.
- Sanity-check plausibility: an implausible conversion rate is a broken tag, not a miracle.
- **Call conversions carry a reporting lag.** Same-day data is structurally understated. Never read today.

### 3.6 — GHL gate
Any GHL component in the lead path → **Mo runs the joint test and marks Verified Live** in the ticket. Nothing is called "live" to the client before that.

**Closeout:** one Primary action per lead type, everything else demoted, ONE_PER_CLICK set, **end-to-end test passed and screenshotted**, CRM reconciliation done, Mo's Verified Live if GHL is in the path. **Stage 4 does not open without this.**

> **If Stage 6 builds a NEW destination**, that page carries its own tracking. Re-test that page's form when it goes live (Stage 6 closeout) — it's a delta test on the new page, not a repeat of this whole stage.

---

## STAGE 4 — Keyword, Offer & Competitor Research
**Owner:** Paid Ads · **Output: the Campaign Brief**

Deliverable is a brief in the client folder containing:

1. **Keyword research** (Keyword Planner): volume, CPC and competition per service, for the actual service area — not national estimates.
2. **The ad group themes.** One theme per service intent, **8–10 keywords each**. Themes are what the RSAs will be written against. Never one mega ad group blending services — that is what craters ad relevance and produces Quality Score 3 on a core term.
3. **Match types per keyword: PHRASE and EXACT only.** No broad. Broad is a defect we keep finding in inherited accounts (it is how an auto-glass campaign buys car-window leads for a home-window client, and how a "branded" campaign spends 79% of its budget on $30 generic clicks). Reject near-duplicates: `hvac service near me` EXACT is already covered by `hvac service` PHRASE.
4. **Brand keyword list:** every spelling/misspelling of the client's name, EXACT match. These build the branded campaign and become negatives on the non-branded one.
5. **The negative keyword list, built before launch.** Standard home-services base list — `job / jobs / career / hiring / salary`, `DIY / how to / diagram / manual`, `parts / capacitor / filter` (unless they sell them), `free / cheap`, `rental / warranty / recall`, competitor brand names — plus the client-specific ones from Stage 1A (services they don't want) and any off-service category to blanket-block.
   - **Negative match type follows purpose:** PHRASE for pattern killers (`cost`, `distributor`, brand-of-equipment names), EXACT for specific known zero-conversion spenders, BROAD to blanket-block an entire off-service category (`car`, `auto`, `windshield`).
   - **Do not over-negative.** A word that appears in both bad and good queries stays. Blocking `glass` would have killed legitimate `glass window replacement` jobs that converted.
6. **Competitor scan:** who is bidding, on what, with what offer.
7. **Landing page assessment** per service: does a page exist, does it convert, is it fast on mobile, is there a click-to-call above the fold? This decides Stage 6. **We do not scale non-branded search onto a bad post-click experience** — non-branded clicks are expensive and a weak page burns them.
8. **Campaign structure and budget split** for this client (see Stage 7).

**Closeout:** brief approved by Eduardo. AT fires Stages 5 and 6 in parallel.

---

## STAGE 5 — Ad Copy & Assets (parallel)
**Owner:** Paid Ads · **Input:** the Campaign Brief

- **One RSA per themed ad group**, written to that theme. **15 headlines / 4 descriptions.** A single RSA covering every service is how ad relevance dies.
- The offer appears exactly as the client gave it in Stage 1A. Nothing the client said they won't say.
- **Extensions:** sitelinks, callouts, structured snippets, call extension. Attach account-level assets where they exist.
- Copy tracks reality: if the client dropped a service line, its assets come out — while keeping the ad above serving minimums.
- Proofread. A typo in the client's own brand name has shipped before.

**Closeout:** RSAs and extensions ready. The copy lives in the AT task, not in Slack.

---

## STAGE 6 — Landing Page / Destination (parallel)
**Owner:** Web (Justin) for a site page · Mo for a GHL funnel · **when applicable**

Unlike Meta, Search has no native form to fall back on. There is always a destination, and its quality is a hard ceiling on non-branded performance.

**Route A — Existing page, verified.** Paid Ads checks it: service + location + **click-to-call above the fold**, fast mobile load, trust signals, form that works, tracking firing. If it fails, it becomes Route B.

**Route B — New page (when applicable).** Paid Ads writes the requirements; Web or Mo builds it.
- Service-specific, matching the ad group theme and the ad copy. A generic homepage destination is a Quality Score problem and a conversion-rate problem at once.
- Click-to-call above the fold, mobile load under 3 seconds, form fields kept minimal.
- Conversion tracking firing on the page and on the thank-you.
- **Dependency deadline:** live **4 business days before** the buildout date, so Stage 8 tests the real flow.

**Closeout:** destination live, tracking verified, leads reaching the CRM, Mo's Verified Live if GHL is in the path.

---

## STAGE 7 — Campaign Buildout in Google Ads
**Owner:** Paid Ads · Requires Stages 5 and 6 complete

### 7.1 — Campaign split (non-negotiable)

**Branded and non-branded are always separate campaigns.** Always. Brand converts cheap and always would; left inside the non-branded campaign it inflates the read, hides whether prospecting is alive, and shares a budget with it.

- **`TSD_MM.DD_Search_Branded_Evergreen`** — the client's brand terms, EXACT.
- **`TSD_MM.DD_Search_NonBranded_<Theme>`** — the prospecting campaign, themed ad groups.
- **Cross-negation, both directions:** brand terms go in as EXACT **negatives** on the non-branded campaign, so brand queries route to the brand campaign. Non-brand generics never live in the branded campaign.

**Naming convention:** `TSD_MM.DD_<Type>_<Brand|NonBranded>_<Theme>`. **The name must describe reality.** A campaign called "WindowSiding" for a siding-only client, or "Branded" for a campaign that is 79% generics, is a defect — not a cosmetic issue. *(The division-wide naming standard is still being finalized; this is the de facto convention in use.)*

### 7.2 — Ad groups
- **Themed, 8–10 keywords each**, one intent per ad group (AC Repair / Heating & Furnace / AC Installation / HVAC Service / Plumbing).
- **One matching RSA per ad group.**
- **PHRASE + EXACT only. No broad match.**
- No near-duplicate keywords across match types.

### 7.3 — Bidding at launch (new campaign, no conversion history)

**Launch on Maximize Clicks.** With no conversion history, smart bidding has nothing to learn from, and a target set from a guess is worse than no target at all. Max Clicks buys the data we need to bid intelligently later.

- Keep it bounded: set a **max CPC ceiling** so Max Clicks cannot buy junk volume at any price.
- **Watch the search terms hard during this phase.** Max Clicks with a thin negative list is how money disappears. The negative list from Stage 4 must be attached **before launch** (see 7.6).
- **Migrate to Maximize Conversions once the account has real conversion data** (the conversion signal from Stage 3 must be clean first — that gate never lifts).
- **Then, and only then, consider a target CPA — and never set it below the CPL the account actually achieves.** This is the single most expensive mistake in our book: a target the algorithm cannot hit is a target it refuses to bid into. It shows up as impression share lost to **rank** at 70–85% while the budget sits half-spent. The campaign is not budget-limited, it is target-throttled. A target works as a **guardrail above the achieved CPL**, not as a wish.
- **Changing the target (not the strategy type) does not reset learning.** Changing the strategy type does.

**Branded campaign:** Maximize Conversions, **no target** — brand converts cheap and does not need a ceiling. Small budget of its own.

### 7.4 — Geo
- **Proximity circles around the service hubs** from Stage 1B, sized per market. Not one radius over a whole metro.
- **Presence only.** Target *people in or regularly in your targeted locations* — never "also people interested in." We are buying homeowners who are physically there, not people daydreaming about the city.
- Exclude the areas the client refuses to serve, as **negative locations**.
- Language, network and geo settings on a new campaign replicate the campaign it splits from, deliberately — not by default.

### 7.5 — Ad schedule
**No default. It comes from Stage 1C.** Build the schedule to the client's actual phone-answering hours. If nobody answers Saturday, we do not buy Saturday clicks for a call-driven business.

- Use an **ad-schedule restriction**, never a bid modifier: **smart bidding ignores schedule bid modifiers.**
- If the client answers 24/7, the campaign runs 24/7. That is a decision, not an omission.

### 7.6 — Negatives at launch
**A campaign never goes live naked.** The shared negative list from Stage 4 is attached **before** the campaign is enabled. We have inherited a campaign that launched with zero negatives and it ran unprotected for months.

- Apply as a **shared negative list** at account level, plus campaign-level negatives where needed.
- Campaign-level negatives also neutralize re-activation risk: if a paused ad group is ever re-enabled by mistake, its traffic is still blocked.

### 7.7 — Performance Max: not at launch
**PMax is not part of the initial build.** Search goes up first, and PMax is only considered once there is a clean conversion signal and a stable non-branded read to compare against. PMax without query control, launched on top of a fresh account, buys volume we cannot inspect and cannibalizes brand.

When it is added later, these are mandatory:
- **Brand exclusions**, so it doesn't absorb branded traffic Search should own.
- **Multiple asset groups**, one per service line — never a single "Services" asset group.
- **Audience signals:** customer list upload + in-market.
- Full asset set (15 headlines, 5 descriptions, image set, 1+ video), **Ad Strength ≥ Good**.
- **Maximum 5–10% of budget. PMax-only is forbidden** by the division standard.
- Watch its channel mix. A PMax that dumps 98% of spend into YouTube at $0.21 CPC is not a lead engine, and must not be called one.

### 7.8 — Automation off
- **Auto-generated assets: OFF.**
- **Auto-apply recommendations: OFF.**
Google's automation silently edits live RSAs and applies changes we did not decide. We own the account; the account does not own itself.

### 7.9 — Buildout checklist
1. Build the branded and non-branded campaigns per 7.1, with the correct naming.
2. Themed ad groups, 8–10 PHRASE/EXACT keywords each, one RSA each (7.2).
3. Cross-negatives: brand terms EXACT-negative on non-branded.
4. **Attach the shared negative list before enabling anything** (7.6).
5. Bidding: Max Clicks with a max-CPC ceiling on non-branded; Max Conversions no-target on branded (7.3).
6. Geo: proximity circles, **presence only**, negative locations set (7.4).
7. Ad schedule per the client's answering hours (7.5).
8. Auto-assets and auto-apply **OFF** (7.8).
9. Conversion goal = the Primary action verified in Stage 3. Campaign-level goal override where needed, so the campaign optimizes to the real lead and nothing else.
10. Extensions attached; final URLs correct, with UTMs.
11. Daily budget = approved monthly ÷ 30.4, split between branded (small) and non-branded. Never above what the client approved in writing.
12. **Everything built PAUSED.** Nothing serves before Stage 8.

**Closeout:** built, paused, ready for QA. Every change logged with its **reversibility** — the exact revert path, written down before we need it.

---

## STAGE 8 — Pre-Launch QA
**Owner:** Paid Ads · **HARD GATE**

The lead flow was already proven in Stage 3. This stage checks the **build**: that what we assembled matches the method and the intake, and that none of the defects we keep inheriting from other agencies are present in our own work. QA is done by **someone other than the person who built it**.

**Structure**
- [ ] Branded and non-branded are separate campaigns. Brand terms are EXACT-negatives on non-branded.
- [ ] No broad match keywords anywhere.
- [ ] Ad groups are themed, 8–10 keywords, one matching RSA each. No mega ad group.
- [ ] Campaign names describe what the campaigns actually do.
- [ ] **Shared negative list is attached.** No campaign is going live naked.
- [ ] No zombie campaign left ENABLED with a live budget elsewhere in the account.

**Settings**
- [ ] Geo = proximity circles around the hubs, **presence only**, negative locations applied.
- [ ] Ad schedule matches the client's actual answering hours (Stage 1C).
- [ ] Bidding = Max Clicks with a CPC ceiling (non-branded), Max Conversions no-target (branded). **No tCPA set from a guess.**
- [ ] Budgets match the written client approval.
- [ ] **Auto-generated assets OFF. Auto-apply recommendations OFF.**

**Ads & conversions**
- [ ] RSAs **APPROVED** (not disapproved on policy) and **Ad Strength ≥ Good**.
- [ ] Extensions attached and serving.
- [ ] Only the real lead action is **Primary**; local actions and micro-clicks are Secondary; lead actions are **ONE_PER_CLICK**.
- [ ] Final URLs land on the right service page, and the page loads fast on mobile.

**Lead flow (carried from Stage 3)**
- [ ] Stage 3's end-to-end test is **signed off, with the screenshot** in the AT task.
- [ ] **Mo's Verified Live** is on the ticket, if GHL is in the path.
- [ ] If Stage 6 built a **new destination**, its own form test passed on that page.

**Closeout:** QA checklist signed in AT. Nothing launches with an open box.

---

## STAGE 9 — Launch
**Owner:** Paid Ads

1. Enable. Record the exact launch date/time in the AT task and in the client's Google Ads log.
2. Log the **baseline** (the 90-day history from Stage 2) and what we expect to happen. We will be measured against this.
3. **Set expectations with the AM, in writing, the same day.** Especially when this launch replaces an inherited setup: a cleaned account often looks *worse* before it looks better, because the old number was inflated by a polluted goal or by brand hiding inside non-brand. That drop is the measurement becoming honest for the first time. **If nobody wrote that down beforehand, the first quiet week gets read as failure and panic-reverted.**
4. The AM communicates to the client. Paid does not.

**Closeout:** live, logged, AM briefed with the expectation in writing.

---

## STAGE 10 — 3-Day Check (one-time)
**Owner:** Paid Ads · Fires 3 days after launch

Purpose: is it delivering, and is the signal landing? **Not a performance read.**

- **Do not read today's data, and do not read intraday.** Impression share is unreliable until the day closes, and call conversions carry a reporting lag that makes the current day structurally understated.
- Is it spending? If not, is it lost to **rank** or lost to **budget**? This is the triage that decides every lever:
  - **Lost to budget** → there is real demand and money is the constraint. That is the trigger to request a client-approved budget increase.
  - **Lost to rank** → money is *not* the lever. The ceiling is relevance, assets, landing page or signal. **Raising the budget will do nothing, and nobody gets to tell the client the budget bump was the fix.**
- Are conversions being **recorded** (not "are they good")? Spend with zero recorded conversions = broken tracking = Critical, fix today.
- First search-term sweep. Max Clicks bites early: kill the obvious waste, add negatives.
- Any disapproved ad, any keyword with a Quality Score of 3 (that's a structural signal, not a keyword problem).

**Action rule:** fix delivery, tracking and waste. Do not touch bidding for performance reasons yet.

**Closeout:** logged in the client's Google Ads log. Slack DM the AM within 2h if anything found needs the client to know.

---

## STAGE 11 — 7-Day Check (one-time) — closes the launch process
**Owner:** Paid Ads · Fires 7 days after launch

- **Search-term sweep, properly this time.** Compute cost on zero-conversion search terms, **net of the client's own brand**, and negative the genuine waste. Match type follows purpose (PHRASE for patterns, EXACT for known spenders, BROAD to blanket an off-service category).
- **Watch-list discipline:** a core service term with 0 conversions and 5 clicks is not a loser, it's an unknown. Give it volume before cutting it. Cutting good intent on thin data is how accounts get slowly strangled.
- **Branded vs non-branded, read separately.** Never one blended CPL. The question is always: is non-brand alive?
- **Bidding migration:** if the conversion signal is clean and the account now has real conversion data, move non-branded from Max Clicks to **Maximize Conversions**. Add a tCPA only later, calibrated **above** the CPL actually achieved — never below it.
- Quality Score and Ad Strength on the themed ad groups.
- Lead quality check with the AM: are they real leads, and is the client calling them back?

**Timing discipline:**
- A **bid change** reads in **3–7 days**.
- A **structural change** (new ad groups, new RSAs, landing pages) takes **2–3 weeks**. A CVR fix reads slower than a bid fix. Do not judge it early, and do not stack changes — separate them by ~48h so each one is attributable.

**Closeout:** the launch process ends here. The recurring **7 / 14 / 30-day optimization processes** take over, plus the standard division SOPs (A1 Weekly Optimization with the weekly search-term review, A4 Friday Pulse).

---

## Dependency summary (for the AT build)

| Dependency | Who | Needed by | Lead time |
|---|---|---|---|
| Client info complete, incl. **phone answering hours** | Account Manager | Stage 2 | Blocks the whole build |
| Written budget approval | Client, via AM ticket | Stage 7 | Blocks launch |
| Clean conversion signal + CRM reconciliation | Paid Ads | Stage 4 | **Hard gate — blocks everything** |
| GHL offline import + Verified Live | Mo | Stage 3 and Stage 8 | 2 days |
| Landing page — **when applicable** | Web (Justin) or Mo | Stage 8 | 4 days before buildout |

**Escalation:** a missed dependency goes to the AM, who coordinates cross-division work — not to the other division head. A dependency blocking a launch date the client already knows about goes to the COO.

---

## Open items this SOP depends on
- **Campaign naming convention** — division-wide standard still being finalized. This SOP uses the de facto `TSD_MM.DD_...` format.
- **CPL benchmarks per trade and tier** — do not exist yet. Until they do, the target CPL comes from the client's own economics (Stage 1C), never from a guess.
