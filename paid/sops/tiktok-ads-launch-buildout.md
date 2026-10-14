# TikTok Ads — New Campaign Launch & Buildout (One-Time Process)

**Owner:** Paid Ads Division (Eduardo)
**Built in:** AT
**Version:** 1.0 — Jul 2026
**Scope:** Two scenarios — a **Conversion** campaign (Instant Form or Call Ads) and an **Awareness / brand recall** campaign.

<p class="note">TikTok is an Accelerator / Dominator deliverable. Platform minimums: $50/day at campaign level, $20/day at ad group level — a TikTok build below that floor is not a campaign, it is a donation.</p>

---

## Stage map

| # | Stage | Owner | Blocks the next stage? | Target time |
|---|---|---|---|---|
| 1 | Client Info | Account Manager | Yes — hard gate | 3 business days |
| 2 | Access, Billing & Account Health | Paid Ads | Yes | 1 business day |
| 3 | Tracking + **End-to-End Lead Flow Test** | Paid Ads + Mo (GHL) | Yes — **hard gate** | 2–3 business days |
| 4 | Angle, Offer & Creative Brief | Paid Ads | Yes | 1 business day |
| 5 | Creative Production (video) | Video (Vince) · Design (Héctor) | No — parallel to 6 | Per Video SLA |
| 6 | Destination — Instant Form / Call / Page | Paid Ads · Web/Mo (page, when applicable) | Yes | 1 day (native) / 4 days (page) |
| 7 | Campaign Buildout | Paid Ads | Yes | 1 business day |
| 8 | Pre-Launch QA | Paid Ads | Yes — **hard gate** | 1 business day |
| 9 | Launch | Paid Ads | — | Same day |
| 10 | 3-Day Check (one-time) | Paid Ads | — | Day 3 |
| 11 | 7-Day Check (one-time) | Paid Ads | — | Day 7 |

**Critical path:** 1 → 2 → 3 → 4 → (5 ‖ 6) → 7 → 8 → 9.

**Creative is the constraint on TikTok.** Not budget, not targeting. The platform is an attention auction, and a repurposed 16:9 ad with a logo in the corner loses it in the first second. Everything Paid can do without the video is done while Video is producing.

---

## The two rules that govern this process

**1. Fix the measurement before you spend the money.** Same hard gate as every channel.

**2. The two campaigns are read on different scoreboards.** The Conversion campaign is judged on leads and CPL. The Awareness campaign is judged on reach, frequency and focused views — never on CPL, and never on a recall number we did not measure.

---

## Awareness on TikTok: what the platform actually sells

**TikTok has no Ad Recall Lift optimization goal.** Recall there is **measured**, not optimized, and only through a **Brand Lift Study** — which carries minimums far outside any budget we run: roughly **$25k–$100k+ in campaign spend, or 500,000 impressions**, depending on market and measurement partner.

So the awareness campaign buys the closest available proxy — **attention and repetition** — and is read on what TikTok actually measures: reach, frequency, focused views (6s/15s), view rate and completion (see Stage 7.1).

**We do not report an ad recall number for TikTok.** We did not measure one. If a client wants measured recall, that is Meta, where the objective exists.

---

## STAGE 1 — Client Info
**Owner:** Account Manager · **Blocks everything downstream**

### 1.0 — Start from AT
The AM opens the client record in AT, confirms what's already there is current, and collects whatever is missing from the client.

The fields below are the full requirement. The stage cannot close with anything still missing.

### 1A. Business & offer
- **Services to advertise**, in priority order. Specific, not "HVAC."
- **The offer**, exactly as it can appear in the ad. If there is no offer, say so.
- **Average ticket.**
- **What the client will NOT say.**
- **Proof:** reviews, rating, years in business, licenses, warranty, financing.

### 1B. Service area
- **Service hubs** and how far the crews actually drive. TikTok targets by region, city and proximity — the geo is built around the hubs.
- **Areas they refuse to serve.**

### 1C. Budget, goal & capacity
- **Monthly TikTok spend, with written client approval.** Hard rule. **Check it against the platform floor:** $50/day campaign, $20/day ad group. Below that, we tell the AM the channel is not viable at this budget instead of launching something that cannot learn.
- **Target cost per lead**, or close rate + job value so we can derive it.
- **Primary conversion: Instant Form or phone call?** This decides the whole build (Stage 6).
- **Phone answering hours.** Decisive if we run Call Ads — a call ad pointing at a phone nobody answers is money on fire.
- **Lead capacity** per week.

### 1D. Creative & brand
- **Real footage:** crew, trucks, jobs, before/after, the owner on camera. TikTok punishes polished corporate video and rewards native, human, handheld.
- **Who can be on camera**, and are they willing.
- **Logo, brand colors, brand guide.**
- **TikTok account:** does the client have one? Do we have access? Needed for Spark Ads (see 7.4).

### 1E. Tracking, CRM & destination
- **TikTok Ads Manager + Business Center access.** TikTok Pixel / Events API — exists, installed where?
- **CRM:** GHL / ServiceTitan / other. Which system owns a call, which owns a form.
- **Call tracking** number for TikTok.
- **Destination:** Instant Form (default), call, existing page, or a page we need to build.
- **Who receives the lead notification.**

**Closeout:** AM marks complete. Paid Ads reviews within 24h and either accepts or bounces it back with the specific missing fields (bounce goes to the AM, never to the client).

---

## STAGE 2 — Access, Billing & Account Health
**Owner:** Paid Ads

1. **Business Center + Ad Account access**, at admin level. Access to the Pixel/dataset and, if the client has one, the TikTok account (needed for Spark Ads).
2. **Billing alive**, no payment hold, no account restriction or review.
3. **Account inventory:** existing campaigns, anything enabled with a live budget that shouldn't be, existing audiences.
4. **90-day history** if the account ran before: what ran, what the CPL was, what the conversion events were. Screenshot for the record.
5. **Billing on paid accounts is the Division Head's** — flag holds and declined cards to Eduardo.

**Closeout:** access confirmed, billing verified live, baseline in the client folder.

---

## STAGE 3 — Tracking + End-to-End Lead Flow Test
**Owner:** Paid Ads · **Dependency:** Mo (GHL), requested at the **start** of this stage · **HARD GATE**

Runs while creative is in production. Never last.

### 3.1 — One source of truth per lead type
- **Calls:** one system owns the connected call. One.
- **Forms:** one system owns the genuine form lead.
- Everything else demoted. The same call in two pipes double-counts and understates the true CPA.

### 3.2 — Events & optimization goal
- **Pixel / Events API** installed and firing. Verify with real test events, not by assumption.
- One event per real conversion. No page-view-as-conversion, no micro-click as a lead.
- The campaign's optimization event = the real lead event. Not "any event in the account."

### 3.3 — The Instant Form trap (the most common way a TikTok launch quietly fails)
**TikTok stores Instant Form leads for 90 days, and then they are gone.** A lead sitting inside TikTok's Leads Center that nobody exported is a lead we did not deliver.

- **Leads must flow into the CRM automatically** — native CRM integration, Zapier/LeadsBridge, or the API. Manual export is not a lead flow, it is a promise to remember.
- The routing is set up **here**, and tested in 3.4.
- **Website-form leads do not land in Leads Center** the way Instant Form leads do. If we ever run both, they are two separate workflows and both get tested.

### 3.4 — End-to-end lead flow test (the gate)
- [ ] **Test lead** submitted through the real destination (the Instant Form itself, if that's the route).
- [ ] It lands in the **CRM automatically**, not just in TikTok.
- [ ] **Test call** through the tracking number lands in the CRM, attributable to TikTok — if we're running Call Ads.
- [ ] The event fires in TikTok as the optimization event.
- [ ] The client's team receives the notification they'll get in production.
- [ ] Test lead removed / marked as test in the CRM.
- [ ] Screenshot into the AT task. No screenshot, no gate.

### 3.5 — GHL gate
Any GHL component in the path → **Mo runs the joint test and marks Verified Live**. Nothing is called "live" to the client before that.

**Closeout:** one source of truth per lead type, automatic CRM routing proven, end-to-end test passed and screenshotted, Mo's Verified Live if GHL is in the path.

---

## STAGE 4 — Angle, Offer & Creative Brief
**Owner:** Paid Ads · **Output: the Campaign Brief + the creative brief for Video**

1. **Who we're talking to**, and the fact that they were not looking for us. TikTok is interruption. The first second is the whole game.
2. **The angles.** Each angle is a distinct offer or promise. **One angle = one ad group** (Stage 7.3).
3. **The hypothesis per angle**, written before launch: *"We believe [audience] responds to [angle] because [reason]. We'll know we're right if [metric] beats [threshold]."*
4. **Creative brief — conversion:** **3 video iterations per angle** — different executions of the same promise, same format. Native, vertical, hook in the first second, real people, real jobs. No repurposed 16:9 corporate cut.
5. **Creative brief — awareness (separate, not recycled):** built to be **remembered**, not clicked. Brand, face, trucks, market position. A conversion ad running on an awareness objective is a wasted impression.
6. **Destination route:** Instant Form (default), Call Ads, or a page.
7. **Budget split** between the Conversion and Awareness campaigns, checked against the platform floor.

**Closeout:** brief approved by Eduardo. Fires Stages 5 and 6.

---

## STAGE 5 — Creative Production (parallel)
**Owner:** Video (Vince) for video · Design (Héctor) for statics/overlays

- **Conversion:** 3 videos per angle, iterations of that one angle, 9:16 native.
- **Awareness:** separate videos built for recall — brand-first, no hard offer.
- Hook lands in the **first second**. Focused view starts counting at 6 seconds, and interactions in the first second aren't even counted — the platform is literally telling us where the fight is.
- Naming follows the TSD convention so we can read performance without opening the ad.

**Closeout:** creatives delivered to the client's asset folder + the AT task, with headroom before the buildout date for one round of fixes.

---

## STAGE 6 — Destination: Instant Form, Call, or Page
**Owner:** Paid Ads · Web/Mo for a page, **when applicable**

**Route A — Instant Form (the default).** Native, loads faster than a page, prefills known fields, higher completion.
- Fields: name, phone, ZIP, service needed. Nothing else — every extra field costs leads.
- One qualifying question maximum, and only if it changes how the client works the lead.
- **CRM integration live and automatic** (Stage 3.3). This is non-negotiable.

**Route B — Call Ads.** When the client's primary conversion is the phone.
- The call button sits on the in-feed ad or on an Instant Page.
- **Only viable if the client actually answers** during the hours we run (Stage 1C). Otherwise we restrict delivery to the hours they do.
- The call must be trackable back to TikTok.

**Route C — Landing page (when applicable).** Only when the offer genuinely needs a page. Web (Justin) or Mo builds it; same minimal-field rule; tracking on the page and the thank-you; its form gets its own test when it goes live.

**Closeout:** the destination exists, tracking verified, leads reach the CRM automatically.

---

## STAGE 7 — Campaign Buildout

### 7.1 — Two campaigns

**Campaign 1 — Conversion**
- Objective: **Lead Generation** (Instant Form) or **Call Ads**, per Stage 6.
- Optimizing for the real lead event verified in Stage 3.
- No target cost at launch on a fresh account — let it find the real CPL before we hand it a number it may not be able to hit. A target below the achievable CPL is a target the algorithm refuses to bid into.

**Campaign 2 — Awareness / brand recall**
- **There is no recall-lift objective to select** (see the top of this doc). We buy the proxy:
  - **Reach objective** when what we want is coverage of the service area with a **controlled frequency** — Reach is the objective where the frequency cap is actually ours to set.
  - **Video Views objective** when what we want is attention — it optimizes for **focused view** (6s / 15s). Note its frequency is auto-capped under ~7 per 7 days and cannot be tuned like Reach's.
- **Read it on reach, frequency, focused views, view rate and completion.** Never on CPL. Never on an invented recall figure.

### 7.2 — Targeting
- **Geo:** the service area, built around the hubs from Stage 1B.
- **Broad, and let the platform's ML find the buyer.** Same doctrine as Meta: we do not stack interest and behavior filters on top of a system that is better at this than our hunches. Age only as a light signal if the client's customer profile genuinely calls for it.
- Exclude the refused areas.

<p class="note">Doctrine carried over from the Meta SOP (leverage the platform's ML, geo only, no interest stacking). Confirm before this becomes the division standard for TikTok specifically.</p>

### 7.3 — One angle = one ad group
Same method as Meta, translated to TikTok's ad structure:
- **One ad group per angle.** The angles compete against each other for budget.
- Inside it, the **3 video iterations of that angle** plus the ad texts for that angle — all arguing the same promise. Copy from another angle inside the ad group destroys the read.
- **Spend is the vote.** The angle that doesn't attract delivery lost. A creative that doesn't spend, barely spends, or spends while returning 1–2 leads, dies.

### 7.4 — Spark Ads for winners
When a creative wins, run it as a **Spark Ad** off the published post so it keeps its accumulated social proof — likes, comments, shares, follows. Rebuilding a winner as a fresh ad throws that away.

<p class="note">This is the TikTok analogue of the post-ID isolation we do on Meta. Confirm.</p>

### 7.5 — Buildout checklist
1. Conversion campaign built on the right objective (Lead Gen / Call Ads), optimizing for the Stage 3 event.
2. **One ad group per angle**, 3 video iterations + matching ad texts inside each.
3. Awareness campaign built on Reach (with frequency cap) or Video Views, with the **separate recall creative** — never the conversion videos.
4. Geo per Stage 1B, refused areas excluded.
5. Instant Form / Call / page wired, with **automatic CRM routing proven in Stage 3**.
6. Budgets respect the platform floor ($50/day campaign, $20/day ad group) and the written client approval.
7. Delivery hours restricted to the client's answering hours if we're running Call Ads.
8. **Everything built PAUSED.** Nothing serves before Stage 8.

**Closeout:** both campaigns built and paused, with the revert path logged.

---

## STAGE 8 — Pre-Launch QA
**Owner:** Paid Ads · **HARD GATE**

The lead flow was proven in Stage 3. This checks the build. QA is done by **someone other than the person who built it**.

- [ ] Conversion and Awareness are **separate campaigns**, on separate objectives.
- [ ] **Nobody attached a CPL goal to the Awareness campaign**, and nobody is expecting a recall number from it.
- [ ] Each ad group carries **one angle only** — its videos and texts argue the same promise.
- [ ] The awareness creative is the recall creative, not a recycled conversion ad.
- [ ] Geo correct, refused areas excluded.
- [ ] Frequency cap set on the Reach campaign.
- [ ] Budgets clear the platform floor and match the written client approval.
- [ ] Instant Form fields are minimal; **leads route to the CRM automatically** (verified, Stage 3).
- [ ] Call Ads (if used) only run during the client's answering hours, and calls are attributable to TikTok.
- [ ] Ads approved, not stuck in review. Videos are vertical, native, hook in the first second.
- [ ] Stage 3's end-to-end test is signed off with the screenshot in the AT task; **Mo's Verified Live** if GHL is in the path.

**Closeout:** QA checklist signed in AT. Nothing launches with an open box.

---

## STAGE 9 — Launch
**Owner:** Paid Ads

1. Enable. Record the launch date/time in the AT task and in the client's TikTok log.
2. Log the hypotheses from Stage 4, so the 3- and 7-day checks are read against something written before we knew the answer.
3. **Brief the AM in writing, the same day** — including the honest framing on the awareness campaign: we are buying attention and repetition, and we will report reach, frequency and views, **not a recall number**.
4. The AM communicates to the client. Paid does not.

**Closeout:** live, logged, AM briefed in writing.

---

## STAGE 10 — 3-Day Check (one-time)
**Owner:** Paid Ads · Fires 3 days after launch

Delivery and signal only. Not a performance read.

- Is it spending? Any ad stuck in review, any ad group with no delivery?
- Are conversions being **recorded**? Spend with zero recorded events = broken tracking = Critical, fix today.
- **Are Instant Form leads actually reaching the CRM?** Check the CRM, not TikTok's Leads Center. A lead that only exists inside TikTok is on a 90-day fuse.
- CPM, CTR, view rate sane vs. the account's history?
- Frequency on the Awareness campaign already running hot?

**Action rule:** fix delivery, tracking and routing. Do not touch creative or budget for performance reasons yet — judging creative at day 3 is judging noise.

**Closeout:** logged in the client's TikTok log. Slack DM the AM within 2h if anything needs the client to know.

---

## STAGE 11 — 7-Day Check (one-time) — closes the launch process
**Owner:** Paid Ads · Fires 7 days after launch

**Conversion campaign**
- CPL vs. the target from Stage 1C.
- **Read the spend distribution at ad group level first** — that is the platform voting on which *angle* deserves the money. Then read inside the surviving angles, creative by creative.
- **Kill** what didn't spend, barely spent, or spent while returning only 1–2 leads.
- **Scale the winner as a Spark Ad**, off the published post, so the social proof travels with it.
- **Lead quality check with the AM.** Instant Form leads are cheap to submit and easy to regret — if the leads are junk, the fix is a qualifying question or a harder offer in the creative, not a bid change.
- Write the next hypothesis and open the creative task for the next round.

**Awareness campaign**
- Reach and frequency in the service area. Focused views (6s/15s), view rate, completion.
- **No CPL. No recall number.** If the client wants measured recall, the honest answer is that TikTok only sells it at a spend level they are not buying — and Meta measures it at their budget.

**Timing:** a bid change reads in 3–7 days; creative and structural changes take longer. One change at a time, so each is attributable.

**Closeout:** the launch process ends here. The recurring **7 / 14 / 30-day optimization processes** take over, plus the division SOPs (A1 Weekly Optimization, A4 Friday Pulse).

---

## Dependency summary (for the AT build)

| Dependency | Who | Needed by | Lead time |
|---|---|---|---|
| Client info complete | Account Manager | Stage 2 | Blocks the whole build |
| Budget clears the platform floor ($50/day campaign, $20/day ad group) | Client, via AM | Stage 1 | Blocks the build — flag early if it doesn't |
| Clean event + **automatic CRM routing**, end-to-end tested | Paid Ads + Mo | Stage 4 | **Hard gate** |
| Conversion videos (3 per angle) | Video (Vince) | Stage 7 | Headroom for one round of fixes |
| Awareness videos (recall creative, separate brief) | Video (Vince) | Stage 7 | Same window — never recycled conversion ads |
| Written budget approval | Client, via AM ticket | Stage 7 | Blocks launch |
| Landing page — **when applicable** | Web (Justin) or Mo | Stage 8 | Before QA |

**Escalation:** a missed dependency goes to the AM, who coordinates cross-division work. A slip that moves a launch date the client already knows about goes to the COO.

---

## Open items this SOP depends on
- **Campaign naming convention** — division-wide standard still being finalized.
- **CPL / CPM benchmarks per trade and tier** — do not exist yet. The target comes from the client's own economics, never from a guess.
- **Confirm the two carried-over calls:** broad-and-let-the-ML-work targeting, and Spark Ads as the winner-isolation mechanism.
