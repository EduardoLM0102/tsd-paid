# YouTube Ads — New Campaign Launch & Buildout (One-Time Process)

**Owner:** Paid Ads Division (Eduardo)
**Built in:** AT
**Version:** 1.0 — Jul 2026
**Scope:** Two campaigns, launched together — a **Conversion** campaign and a **Video Views** campaign built for **Ad Recall Lift**.

<p class="note">YouTube is an Accelerator / Dominator deliverable. The video itself is produced and uploaded by the Video division (Vince) — Paid Ads does not produce it, and cannot launch without it.</p>

---

## Stage map

| # | Stage | Owner | Blocks the next stage? | Target time |
|---|---|---|---|---|
| 1 | Client Info | Account Manager | Yes — hard gate | 3 business days |
| 2 | Access, Billing & Channel Check | Paid Ads | Yes | 1 business day |
| 3 | Conversion Tracking + **End-to-End Lead Flow Test** | Paid Ads + Mo (GHL) | Yes — **hard gate** | 2–3 business days |
| 4 | Audience, Offer & Video Brief | Paid Ads | Yes | 1 business day |
| 5 | **Video production + YouTube upload** | Video (Vince) | Yes — **the critical path** | Per Video SLA |
| 6 | Cutdowns & Destination | Paid Ads · Web/Mo (page, when applicable) | Yes | 1 business day |
| 7 | Campaign Buildout | Paid Ads | Yes | 1 business day |
| 8 | Pre-Launch QA | Paid Ads | Yes — **hard gate** | 1 business day |
| 9 | Launch | Paid Ads | — | Same day |
| 10 | 3-Day Check (one-time) | Paid Ads | — | Day 3 |
| 11 | 7-Day Check (one-time) | Paid Ads | — | Day 7 |

**Critical path:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9.

**The video is the constraint.** Unlike Search and Meta, this process cannot be parallelized around its creative: there is no campaign without a video, and no campaign activation until that video is **live on the client's YouTube channel** (per MasterOps: YouTube upload is owned by the Video team, 48h from Green Light; campaign activation is 48h from the upload). Everything Paid Ads can do without the video — tracking, audiences, destination, account setup — is done *while* Video is producing, so that the day the upload lands, the build is one day from live.

---

## The two rules that govern this process

**1. Fix the measurement before you spend the money.** Same hard gate as every other channel. YouTube makes this worse, not better: it is the easiest channel in the account to fool yourself with. We have seen an account where YouTube traffic "converted" on a web form at 2.67% for an HVAC company — that was not performance, it was a broken tag, and a real budget was being steered by it.

**2. The two campaigns are read on different scoreboards.** The Conversion campaign is judged on leads and CPL. The Video Views campaign is judged on recall, views and reach. Never average them, never let the awareness campaign's cheap views flatter a blended CPV, and never let anyone read the Video Views campaign as a lead engine because it happened to catch a view-through.

---

## STAGE 1 — Client Info
**Owner:** Account Manager · **Blocks everything downstream**

### 1.0 — Start from AT
The AM opens the client record in AT, confirms what's already there is current, and collects whatever is missing from the client.

The fields below are the full requirement. The stage cannot close with anything still missing.

### 1A. Business & offer
- **Services to advertise**, in priority order. Specific: "AC replacement," not "HVAC."
- **The offer**, exactly as it can appear in the ad. If there is no offer, say so.
- **Average ticket** for the advertised service.
- **What the client will NOT say** (claims, pricing, guarantees they won't back).
- **Proof assets:** reviews and rating, years in business, licenses, warranty, financing.
- **Top competitors by name.**

### 1B. Service area
- **Service hubs** and how far the crews actually drive. Geo is built as proximity around the hubs, not a blob over a metro.
- **Areas they refuse to serve.**

### 1C. Budget, goal & capacity
- **Monthly YouTube spend**, with **written client approval**. Hard rule — no budget moves without it.
- **Target cost per lead** for the Conversion campaign, or the client's close rate and job value so we can derive it.
- **Primary lead type:** calls or form fills.
- **Phone answering hours.** If nobody answers, clicks bought then cannot convert.
- **Lead capacity** per week.

### 1D. Video, channel & brand
- **The client's YouTube channel:** does it exist, and do we have access? The ad video has to live somewhere.
- **The person on camera.** YouTube in home services works when the owner or the crew is on screen. Who is available, and are they willing?
- **Shoot footage / existing video** the client already has.
- **Brand:** logo, colors, brand guide.

### 1E. Tracking, CRM & destination
- **Google Ads account** access (MCC), **GA4** access.
- **CRM:** ServiceTitan / GHL / other. Which system owns a call, which owns a form.
- **Call tracking:** CallRail / ServiceTitan numbers.
- **Destination:** existing landing page, or one we need to build.
- **Who receives the lead notification.**

**Closeout:** AM marks complete. Paid Ads reviews within 24h and either accepts or bounces it back with the specific missing fields (bounce goes to the AM, never to the client).

---

## STAGE 2 — Access, Billing & Channel Check
**Owner:** Paid Ads

1. **MCC access** to the Google Ads account. **GA4** access. Access to the conversion source.
2. **The YouTube channel is linked to the Google Ads account.** Without the link, we cannot run the video as an ad, cannot build view-based audiences, and cannot read earned actions. This link is the single most common reason a YouTube launch stalls on day one.
3. **Billing is alive.** `customer.status`, billing setup, and the date of the last impression. An account can look active in the UI and be serving nothing.
4. **Account inventory:** existing campaigns, zombie campaigns (ENABLED with a live budget, not serving only because of an end date), existing exclusion lists.
5. **Billing on paid accounts is the Division Head's.** Payment holds, declined cards, stopped accounts → flag to Eduardo.

**Closeout:** access confirmed, channel linked, billing verified live, baseline in the client folder.

---

## STAGE 3 — Conversion Tracking + End-to-End Lead Flow Test
**Owner:** Paid Ads · **Dependency:** Mo (GHL), requested at the **start** of this stage · **HARD GATE**

Runs while Video is producing. It is never the thing we do last.

### 3.1 — One source of truth per lead type
- **Calls:** one system owns the connected call (ServiceTitan / CallRail). One.
- **Forms:** one system owns the genuine form lead (GHL / ServiceTitan).
- Everything else is demoted. The same call flowing through two or three pipes double-counts and understates the true CPA.

### 3.2 — Primary vs Secondary, and the YouTube-specific trap
- **Primary = the real lead action, click-through only.** That is what smart bidding optimizes toward.
- **View-through conversions are NOT a lead.** They are **Secondary — awareness reporting only**, and they never feed bidding. A view-through says someone saw a video and later showed up; it does not say the video bought the lead. Counting it as a conversion is how a video campaign gets credit for demand that Search already captured.
- Also Secondary: Google Business "Local actions," GA4 micro-clicks, and every duplicate call pipe.
- Lead actions count **ONE_PER_CLICK**. Correct category on each action.
- Delete conversion actions that have **never fired**.

### 3.3 — End-to-end lead flow test (the gate)
- [ ] **Test form** submitted through the real destination. It lands in the CRM.
- [ ] **Test call** through the tracking number. It lands in the CRM, attributable to Google.
- [ ] Both appear in Google Ads as the **Primary** action.
- [ ] The client's team receives the notification they'll get in production.
- [ ] Test lead removed / marked as test in the CRM.
- [ ] Screenshot into the AT task. No screenshot, no gate.

### 3.4 — Reconcile against the CRM
Pull the real lead count from the CRM for a known window and compare it to what Google reports. **An implausible conversion rate on video traffic is a broken tag, not a miracle.** If the numbers don't reconcile, we do not have a performance story and no bidding decision may be built on top of it.

### 3.5 — GHL gate
Any GHL component in the path → **Mo runs the joint test and marks Verified Live**. Nothing is called "live" to the client before that.

**Closeout:** one Primary per lead type, view-through demoted to Secondary, ONE_PER_CLICK set, end-to-end test passed and screenshotted, CRM reconciliation done, Mo's Verified Live if GHL is in the path.

---

## STAGE 4 — Audience, Offer & Video Brief
**Owner:** Paid Ads · **Output: the Campaign Brief + the Video Brief for Vince**

The brief has to be written *early*, because it is what unblocks Stage 5, which is the critical path.

1. **Who we're talking to**, and what state they're in when the ad interrupts them. On YouTube, nobody came looking for us. The video earns the next three seconds or it doesn't.
2. **The angle and the offer** for the Conversion campaign.
3. **The audience build** (see 7.2): the in-market and custom segments we'll target, and the intent keywords the custom segments are built from.
4. **Video brief for Vince — two distinct videos, not one video used twice:**
   - **Conversion video:** hook in the first 3 seconds, the problem, the proof, the offer, a clear CTA. Built to make someone act now.
   - **Recall video:** built to be *remembered*, not clicked. The brand, the face, the trucks, the market position. No hard offer, no discount chase. A conversion ad running on a recall objective is a wasted impression.
   - Formats: **16:9 master with cutdowns to 4:5 and 9:16** (division standard).
5. **Destination decision:** existing landing page, or one we need built.
6. **Budget split** between the Conversion campaign and the Video Views campaign.

**Closeout:** brief approved by Eduardo, video brief handed to Video (Vince) — this is what starts Stage 5's clock.

---

## STAGE 5 — Video Production + YouTube Upload
**Owner:** Video division (Vince) · **THE CRITICAL PATH**

Paid Ads does not produce the video and cannot substitute for it. What we own here is making sure the dependency is visible and dated.

- Video produces and edits both videos from the Stage 4 brief.
- **The video must be uploaded to the client's YouTube channel** — per MasterOps, YouTube upload is owned by the Video team (48h from Green Light). **Campaign activation is 48h from that upload.**
- Paid Ads needs the **YouTube URL** for each video. Not a file, not a Drive link. The ad runs from the hosted video.
- Video visibility must allow it to serve as an ad (public or unlisted, per the channel's setup).

**If Video slips, the launch date slips.** That is not a Paid Ads failure and it is not absorbed silently — the AM is told the same day, because the client's launch date moves with it.

**Closeout:** both videos live on the client's channel, URLs delivered into the AT task.

---

## STAGE 6 — Cutdowns & Destination
**Owner:** Paid Ads · Web (Justin) or Mo for a page, **when applicable**

- **Cutdowns:** Paid Ads cuts the master to the platform aspect ratios needed (4:5, 9:16 for Shorts/in-feed). This is our job, per the division playbook — not Video's.
- **Destination — Route A:** existing landing page, verified. Service-specific, click-to-call above the fold, fast on mobile, form works, tracking fires.
- **Destination — Route B (when applicable):** new page. Paid writes the requirements, Web or Mo builds it. Tracking on the page and the thank-you. If a new page is built, its form gets its own test when it goes live (a delta test on the new page, not a repeat of Stage 3).

**Closeout:** cutdowns ready, destination live and verified.

---

## STAGE 7 — Campaign Buildout
**Owner:** Paid Ads

### 7.1 — Two campaigns, launched together

**Campaign 1 — Conversion**
- **Video Action / Demand Gen**, optimizing for the Primary conversion action verified in Stage 3.
- **Maximize Conversions, no target CPA at launch.** With no conversion history on this channel, a target is a guess, and a target the algorithm cannot hit is a target it refuses to bid into — it self-throttles, and we pay for the education anyway. Let it find the real CPL first.
- Add a tCPA later, once the account has real data, and **never below the CPL actually achieved**. A target is a guardrail above reality, not a wish.
- **View-through conversions do not feed this campaign's bidding** (Stage 3.2). Click-through only.

**Campaign 2 — Video Views (Ad Recall Lift)**
- **Video Views campaign**, running the recall video from Stage 5.
- **Ad Recall Lift is measured with a Brand Lift study when the budget clears Google's minimum.** Below that threshold, we read CPV, view rate, reach and frequency in the service area — and we say so plainly, rather than inventing a recall number we didn't measure.
- **Frequency management matters here.** Recall needs repetition; annoyance needs none. Cap it.
- **This campaign has no CPL and is not judged on one.** Its job is to make the brand familiar, so that the Conversion campaign and Search convert into a warmer market. Brandformance: the ad does not create the authority, it amplifies it.

### 7.2 — Targeting
- **Geo:** proximity around the service hubs from Stage 1B. **Presence only** — people who live there, not people "interested in" the area.
- **Audiences: in-market and custom segments.** In-market segments matching the service (e.g. HVAC services, home improvement), plus **custom segments built from the intent keywords** in the Stage 4 brief — the terms these people actually search before they buy.
- Exclude the areas the client refuses to serve.
- Standard content exclusions for brand safety. We are putting a home-services brand in front of homeowners, not chasing the cheapest inventory on the platform.

<p class="note">Remarketing, customer match, keyword and placement targeting are not part of the default build. They are layers we add deliberately, with a reason, not because the interface offers them.</p>

### 7.3 — Budget
- Split between the two campaigns per the Stage 4 brief. Total = the client-approved monthly figure ÷ 30.4.
- Never above what the client approved **in writing**.

### 7.4 — Automation off
- **Auto-generated assets: OFF. Auto-apply recommendations: OFF.** Google's automation silently edits live ads. We own the account.

### 7.5 — Buildout checklist
1. Conversion campaign built: Video Action / Demand Gen, **Maximize Conversions with no target**, Primary action from Stage 3.
2. Video Views campaign built with the recall video. Frequency capped.
3. YouTube URLs from Stage 5 attached; cutdowns loaded for the placements that need them.
4. Geo = proximity around hubs, **presence only**; refused areas excluded.
5. Audiences: in-market + custom segments from the intent keywords.
6. **View-through conversions are Secondary**, not a bidding signal.
7. Final URLs correct, with UTMs. Companion CTA / end screen points to the destination.
8. Content exclusions applied.
9. Auto-assets and auto-apply **OFF**.
10. Budgets match the written client approval.
11. **Everything built PAUSED.** Nothing serves before Stage 8.

**Closeout:** both campaigns built and paused. Every change logged with its revert path.

---

## STAGE 8 — Pre-Launch QA
**Owner:** Paid Ads · **HARD GATE**

The lead flow was proven in Stage 3. This stage checks the build. QA is done by **someone other than the person who built it**.

**Structure & settings**
- [ ] Two campaigns, separate: Conversion and Video Views. Not one campaign doing both jobs.
- [ ] Conversion campaign = Maximize Conversions, **no target CPA**. No tCPA set from a guess.
- [ ] Video Views campaign is not optimizing for conversions, and nobody has attached a CPL goal to it.
- [ ] Geo = proximity around the hubs, **presence only**. Refused areas excluded.
- [ ] Audiences = in-market + custom segments from the intent keywords.
- [ ] Frequency cap set on the Video Views campaign.
- [ ] Content exclusions applied.
- [ ] Budgets match the written client approval.
- [ ] **Auto-generated assets OFF. Auto-apply recommendations OFF.**

**Creative & conversions**
- [ ] The right video is on the right campaign. **The conversion video is not running on the recall campaign, and the recall video is not running on the conversion campaign.**
- [ ] Videos are **live on the client's YouTube channel** and playable, at the correct visibility.
- [ ] Ads are approved, not stuck in policy review.
- [ ] Only the real lead action is **Primary**. **View-through is Secondary.** Lead actions are ONE_PER_CLICK.
- [ ] Final URLs land on the right page and load fast on mobile.

**Lead flow (carried from Stage 3)**
- [ ] Stage 3's end-to-end test is signed off, with the screenshot in the AT task.
- [ ] **Mo's Verified Live** on the ticket, if GHL is in the path.
- [ ] If Stage 6 built a new destination, its own form test passed on that page.

**Closeout:** QA checklist signed in AT. Nothing launches with an open box.

---

## STAGE 9 — Launch
**Owner:** Paid Ads

1. Enable both campaigns. Record the launch date/time in the AT task and in the client's Google Ads log.
2. Log the baseline and what we expect: the Conversion campaign will be read on leads and CPL; the Video Views campaign will not.
3. **Brief the AM in writing, the same day.** Specifically: YouTube conversion volume ramps slower than Search, because we are interrupting demand instead of catching it. If that expectation is not written down before launch, week one gets read as failure.
4. The AM communicates to the client. Paid does not.

**Closeout:** live, logged, AM briefed with the expectation in writing.

---

## STAGE 10 — 3-Day Check (one-time)
**Owner:** Paid Ads · Fires 3 days after launch

Delivery and signal only. **Not a performance read.**

- Is it spending? Are the videos actually serving, or is an ad stuck in review?
- Are conversions being **recorded**? Spend with zero recorded conversions = broken tracking = Critical, fix today.
- **Sanity-check the conversion mix.** If YouTube is suddenly producing form fills at a rate that would embarrass a Search campaign, that is a tag problem, not a win. Check it before anyone celebrates it.
- CPV, view rate and CTR sane vs. the account's history?
- Frequency on the Video Views campaign not already running hot?
- **Do not read today's data, and do not read intraday.** Call conversions carry a reporting lag; the current day is structurally understated.

**Action rule:** fix delivery and tracking. Do not touch bidding for performance reasons yet.

**Closeout:** logged in the client's Google Ads log. Slack DM the AM within 2h if anything found needs the client to know.

---

## STAGE 11 — 7-Day Check (one-time) — closes the launch process
**Owner:** Paid Ads · Fires 7 days after launch

**Conversion campaign**
- CPL vs. the target from Stage 1C — **click-through conversions only**. View-through does not enter this number.
- CPV, view rate, CTR, and where the drop-off happens in the video. A video losing everyone at second 5 is a creative problem, and no bid change fixes a bad hook.
- Which audience segments are actually producing, and which are only producing views.
- **Bidding:** if the conversion signal is clean and there is real data, consider a tCPA — calibrated **above** the CPL actually achieved, never below.

**Video Views campaign**
- Views, view rate, CPV, reach and frequency in the service area.
- **Brand Lift study:** if the spend cleared Google's minimum, read the Ad Recall Lift. If it didn't, say that plainly. We do not report a recall number we did not measure.
- **Do not judge this campaign on CPL.** It doesn't have one, by design.

**Timing discipline**
- A **bid change** reads in 3–7 days. A **creative change** (new hook, new video) takes longer, and video creative is expensive to iterate — which is exactly why the brief in Stage 4 has to be right.
- One change at a time, separated so each is attributable.

**Closeout:** the launch process ends here. The recurring **7 / 14 / 30-day optimization processes** take over, plus the division SOPs (A1 Weekly Optimization — YouTube checklist reads CPV, CTR and conversions; A4 Friday Pulse).

---

## Dependency summary (for the AT build)

| Dependency | Who | Needed by | Lead time |
|---|---|---|---|
| Client info complete | Account Manager | Stage 2 | Blocks the whole build |
| YouTube channel linked to Google Ads | Paid Ads (client access via AM) | Stage 7 | Blocks the build |
| Clean conversion signal + end-to-end lead test | Paid Ads + Mo | Stage 4 | **Hard gate** |
| **Conversion video + recall video, live on the channel** | **Video (Vince)** | **Stage 6** | **The critical path** — 48h upload SLA from Green Light; activation 48h from upload |
| Written budget approval | Client, via AM ticket | Stage 7 | Blocks launch |
| Landing page — **when applicable** | Web (Justin) or Mo | Stage 8 | Before QA |

**Escalation:** a missed dependency goes to the AM, who coordinates cross-division work — not to the other division head. A video slip that moves a launch date the client already knows about goes to the COO.

---

## Open items this SOP depends on
- **Campaign naming convention** — division-wide standard still being finalized. Use the de facto `TSD_MM.DD_...` format.
- **CPV and CPL benchmarks per trade and tier** — do not exist yet. Until they do, the target comes from the client's own economics, never from a guess.
