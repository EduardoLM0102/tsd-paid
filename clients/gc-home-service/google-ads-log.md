# GC Home Service — Google Ads change log

Account `2375064049` (under Topservdigital MCC `4155514468`). Newest actions at top.

---

## 2026-08-28 — LSA low-impression diagnosis + AM ticket submitted

**Trigger:** Edu flagged GC's LSA as barely getting impressions.

**Account identified:** GC's LSA runs under a separate, unnamed customer_id `2974002658` (not
in `contas.yaml`, not in `lsa_report.py`'s hardcoded list, no LOCAL_SERVICES campaign inside the
main PPC account `2375064049`). Found by matching a phone number Edu supplied (297-400-2658)
against an old Proud Pops audit doc (`clients/proud-pops/budget-analysis-2025-2026.md`) that had
already surfaced this account and excluded it for Proud Pops — geo targets (Boone/Campbell/Kenton
KY + Butler/Clermont/Hamilton OH) match GC's Cincinnati tri-state area exactly. **Worth registering
this ID somewhere durable (contas.yaml or this doc) so it doesn't need re-discovering.**

**Ruled out:**
- Campaign: `ENABLED`, `primary_status: ELIGIBLE`, `serving_status: SERVING`.
- Verification artifacts all current: license (KY State Master HVAC Contractor) renewed 2026-07-28,
  valid to 2027-06-28 (a prior license had lapsed 2026-06-28 → 2026-07-28, since fixed); insurance
  renewed 2026-08-13, valid to 2027-08-31; background check PASSED.
- Geo targeting: reasonable 6-county Cincinnati metro coverage. Only gap: no Indiana counties, even
  though GC markets itself as covering SE Indiana too — minor, not the main driver.

**Root cause found:** ad schedule is **Monday–Friday, 8am–4pm only** (40 hrs/week of eligibility,
no evenings, no weekends). Checked two comparable healthy dedicated-LSA accounts (Proud Pops - LSA
San Antonio [1] and [2]) for reference — both run 7 days/week with wide hours (9am–6pm / 7am–7pm +
Saturday) and get real volume (one spent $662 on 1,306 impressions in the last 30 days). GC's LSA
spent **$0** and got **32–98 impressions/month** over Jun–Aug, with only **2 leads in 90 days** (1
booked). GC's own site pitches 24/7 emergency HVAC service, but the LSA ad schedule cuts it out of
evening/weekend searches — exactly when HVAC emergency demand peaks.

**Budget:** campaign_budget reads as $385.71/day-equivalent = **$2,700/week**.

**AM ticket submitted by Edu** (per doctrine — budget changes need written client approval; the
schedule/bio items aren't budget but bundled into the same ticket) asking for:
1. Change working hours to 24/7.
2. Bump weekly budget — $2,700/week flagged as low.
3. Add profile "bio" features: Locally-owned & operated • Discounts available • Military discount
   available • Eco-friendly • Workmanship guarantee • Professional service.

**Status:** ticket submitted, awaiting client/AM action. None of these three are executable via the
Ads API (LSA schedule/budget/profile live in the Local Services app, not standard Google Ads
campaign controls) — nothing to verify by read-back until the AM confirms the changes are made.

---

## 2026-08-24 — Re-enabled Calls from ads as a biddable goal (both live campaigns)

**Context:** last 7 days, standard `conversions` metric read 0 on both live campaigns. Real activity
was there (`[TSD] Website Call Link` tel-taps: 13/4/6/5/1/6/5 on Aug 17–23; one verified connected
call via `Calls from ads [1]` on Aug 21) but none of it counted — First Time/Repeat Phone Call and
Form Submision [Landing Page] (the only biddable goals since the Jul 28 rebuild) have fired **zero**
times in 30+ days. Both live campaigns had zero biddable signal; Smart Bidding was optimizing blind.

**Change:** `campaign_conversion_goal.biddable` set to **TRUE** for category `PHONE_CALL_LEAD` /
origin `CALL_FROM_ADS` on `TSD_PMAX_Calls` (23511318927) and `TSD_Leads_Search_Branded_08.06`
(23921909024). Verified by read-back on both.

**Known tradeoff — flagged to Edu before executing, confirmed:** this bucket is shared by two
conversion actions — `Calls from ads [1]` (real connected call, 15s threshold) and
`[TSD] Website Call Link` (tap on a call link, not a verified call) — categorized together as
`PHONE_CALL_LEAD`/`CALL_FROM_ADS` with no way to split them via goals (same class of limitation as
Repeat Phone Call riding along with First Time). Turning the bucket on re-admits the tap-click volume
the Jul 28 rebuild deliberately excluded (audit finding #2). Accepted anyway: diluted signal beats the
literal zero the account has been bidding on for a month. Revisit once website call-tracking
(First Time/Repeat Phone Call) is confirmed live and firing — at that point this bucket should likely
go back off.

**Post-change goal state, both live campaigns (read-back verified):** DEFAULT/WEBSITE,
PHONE_CALL_LEAD/CALL_FROM_ADS, SUBMIT_LEAD_FORM/WEBSITE, QUALIFIED_LEAD/WEBSITE all biddable.

**Learning period restarted again** on both campaigns (bid target changed) — third time since Jul 28.

⚠️ Not a budget change, so the AM-ticket doctrine gap doesn't technically apply here — but worth a
heads-up to Eve/AM given the account already has 2 unticketed budget changes outstanding (Jul 28 cut,
Aug 10 ramp) and this is another live mutation with no client-facing paper trail.

---

## 2026-08-10 — Budget ramp across all 3 live campaigns, targeting ~$5,530 EOM spend

**Authority:** Edu, in-session. **DOCTRINE: budget changes require written client approval via an AM
ticket — not yet logged. Same gap as the Jul 28 PMax cut; needs papering.**

**Context:** MTD spend through Aug 10 was $446.33 across the 3 active campaigns ($336.09 PMax /
$67.76 Branded Search / $42.48 Awareness-YouTube). Target: land August at ~$5,530 total. Remaining
need = $5,083.67 over the 21 days left (Aug 11–31) ≈ $242/day combined, up from $80/day combined.

**Budgets changed (all verified live by read-back):**

| Campaign | Budget resource | Before | After |
|---|---|---|---|
| `TSD_PMAX_Calls` (23511318927) | 15337617979 | $20/day | **$135/day** |
| `TSD_Leads_Search_Branded_08.06` (23921909024) | 15640007176 | $40/day | **$50/day** |
| `TSD - Awareness (ZIP Codes)` (24116591977, YouTube) | 15769412354 | $20/day | **$57/day** |

$135 + $50 + $57 = $242/day × 21 days = $5,082 + $446.33 MTD = **$5,528.33** projected EOM.

**Note found while pulling current budgets:** PMax had been running at $20/day, not the $50/day set
on Jul 28 (see 2026-07-28 entry below) — no record in this log of when/who dropped it further. Not
chased down before this change; flagging so it doesn't look like a silent discrepancy later.

**Split logic:** PMax carries the largest share (broadest inventory, historical primary spend
driver). Awareness/YouTube gets the second-largest raise, tying directly to this week's
mailer-support recall push (see `GC-Home-Service-Weekly-Update_2026-08-07`). Branded Search gets
the smallest bump — it's already at 82%+ impression share, so it's capped by real branded query
volume rather than budget; a big raise there would mostly go unspent until mailer-driven search
demand shows up.

**Caveat not resolved before executing:** PMax still has zero biddable conversions since the Jul 28
goal rebuild, and its asset group still points at the ServiceTitan booking portal, not the new
`/gc-heating-and-cooling/` landing page. A 6.75x budget increase there buys more reach on an
account that hasn't proven it can convert yet — executed per Edu's direct call, but this is the
change most worth a written client approval record given the size of the jump.

---

## 2026-08-07 — Landing page swap: early check-in (2 days post-swap)

**Trigger:** Edu asked to check how the Aug 5 landing-page swap (below) is performing so far.

**New page confirmed live:** `gchomeservice.com/gc-heating-and-cooling/` returns HTTP 200.

**Daily, `TSD_Leads_Search_Branded_08.06` (23921909024), Jul 30–Aug 6:**

| Date | Clicks | Conv | Cost |
|---|---|---|---|
| 07-30 | 1 | 0 | $31.35 |
| 07-31 | 1 | 0 | $31.80 |
| 08-01 | 1 | 0 | $6.43 |
| 08-04 | 2 | 0 | $2.24 |
| 08-05 (swap day) | — | — | — |
| 08-06 | 1 | 0 | $59.09 |

**Read: no signal, nothing to compare against.** This branded campaign runs ~1 click/day both before and after the swap, and 0 conversions throughout — consistent with what the Aug 5 entry already flagged: the account's correctly-typed lead-form conversion action has zero conversions ever recorded. There isn't a working baseline to measure a lift or drop against yet. Nothing broke (page resolves fine), but at this volume it'd take weeks, not days, to see anything meaningful.

**Next check:** revisit alongside the still-open items from Aug 5 — the missing heating/furnace ad-group coverage and the nonbranded campaign reactivation decision, since branded alone won't generate enough volume to judge the new page.

---

## 2026-08-05 — New landing page swap: EXECUTED (Search/Branded only)

**Authority:** Edu, in-session. New page built by Edu on gchomeservice.com, tracking confirmed
live and set up by Edu himself before the swap (same standard as the Proud Pops HVAC page swap
the same day).

**What changed:** the one ad in the live `TSD_Leads_Search_Branded_08.06` campaign (id
`23921909024`, ad `812175098592`) — final URL switched from the homepage
(`https://gchomeservice.com/`) to `https://gchomeservice.com/gc-heating-and-cooling/`.

**Scoped out on purpose:** `TSD_PMAX_Calls` (the other live campaign) still points its asset
group at `https://book.gchomeservice.com/Home` — ServiceTitan's own booking portal, not the
marketing site. Decided not to touch it: moving PMax off a direct-booking flow onto a marketing
landing page is a behavior change, not a like-for-like URL swap, and PMax final URLs live on
`asset_group` (different resource/tooling than `ad_group_ad`/`Ad`) so it wasn't a quick add-on
anyway.

**Diagnosed before the swap, why this account needed more scrutiny than Proud Pops:** the
correctly-typed webpage conversion action `[TSD] Lead Form [LP]` has **zero conversions ever**.
A second action, `Form Submision [Landing Page]`, also shows 0 — but that one is typed
`UPLOAD_CLICKS`, so zero is structurally expected (it only counts a manual/API upload, never a
live form fill) and isn't itself evidence of anything broken. Proceeded on Edu's direct
confirmation that he personally set up and verified tracking on this specific page.

**Campaign-creation question, checked and answered:** confirmed **no new campaign is needed**.
`TSD_07.05_Search_Nonbranded_Cooling` (id `23828854286`, $60/day, currently PAUSED) already
exists with 3 built ad groups — AC Repair (real history: 37 clicks/1 conversion), AC Emergency,
AC Maintenance — and is the natural one to reactivate for nonbranded search traffic to this page.

**Gap found while checking:** that campaign, and the only other nonbranded one
(`TSD_Leads_Search_Nonbranded_07Jun2026`, PAUSED, 0 clicks), are **cooling/AC only** — there are
no heating/furnace ad groups anywhere in this account. The new page is titled "heating and
cooling," so nonbranded searchers looking for furnace/heating repair currently have nowhere to
land. Reactivating the existing cooling campaign is a **budget decision** (new $60/day spend),
not a URL tweak — flagged separately rather than bundled into today's change, especially since
this account already has an overdue budget-approval-ticket gap from the Jul 28 PMax change (see
below). Needs: (1) client budget approval to reactivate, (2) a heating/furnace ad group built
before nonbranded coverage actually matches the page.

---

## 2026-07-28 — PMax budget cut + conversion-goal rebuild (both live campaigns)

**Context:** follows the 2026-07-27 audit (`google-ads-audit-2026-07-27.md`). Two live campaigns
only: `TSD_PMAX_Calls` (PMax, id `23511318927`) and `TSD_Leads_Search_Branded_08.06`
(Search, id `23921909024`). Both on Maximize Conversions.

### 1. PMax budget $155 → $50/day
- `TSD_PMAX_Calls` budget resource `15337617979`: **$155 → $50/day.** Verified by read-back.
- Reverses the Jul 16 3x bump that was bleeding (~$963 for 1 conv Jul 18–26; 59% of account spend).
- ⚠️ **DOCTRINE:** budget changes require written client approval via an AM ticket. This was executed
  on Edu's direct instruction ahead of the ticket — **the AM client-budget-change ticket still needs
  to be logged to paper it.**

### 2. Conversion goals — off the call-button clicks, onto real calls + form
The account runs Google's **conversion-goals** model. Biddability lives in `campaign_conversion_goal`
(category/origin level), **not** `conversion_action.primary_for_goal` (mutating that succeeds silently
and does nothing). Both campaigns were bidding on **only `PHONE_CALL_LEAD / CALL_FROM_ADS`** = the
call-*button* click, not a connected call. That's the audit's finding #2.

`campaign_conversion_goal.biddable` set on **both** live campaigns (verified by read-back):

| Goal (category / origin) | Was | Now | Actions in this bucket |
|---|---|---|---|
| DEFAULT / WEBSITE | off | **biddable** | First Time Phone Call (13/90d), Repeat Phone Call (8/90d) |
| QUALIFIED_LEAD / WEBSITE | off | **biddable** | Form Submision [Landing Page] (0/90d) |
| PHONE_CALL_LEAD / CALL_FROM_ADS | biddable | **off** | Calls from ads [1] (29/90d), [TSD] Website Call Link (4/90d) |

FieldMask written with an explicit `paths=["biddable"]` (the `field_mask` helper drops `False`).

**Repeat Phone Call rides along.** First Time and Repeat share the exact same bucket (DEFAULT/WEBSITE);
goals can't separate them. Chose to accept Repeat (only 8/90d, and a repeat call to an HVAC shop is
still real service demand) rather than recategorize First Time — keeps the change fully reversible and
gives the thin campaigns more volume to learn on. If Repeat proves low-value, recategorize First Time
Phone Call into its own lead category and turn DEFAULT off.

### Consequences to watch
- **Learning period restarted** on both campaigns (bid target changed).
- **Thin signal:** live biddable volume is now ~First Time (13/90d) since **Form fires 0/90d** — it's
  the right category (QUALIFIED_LEAD) but currently dead. **Verify the landing-page form tag** — if it's
  broken, fixing it is the highest-value next step.
- The real fix is still **ServiceTitan offline import** (booked-job + revenue). GC has **zero**
  ServiceTitan/upload-origin conversion actions today — needs building, same play as Mission Accomplished.
  Confirm GC has Marketing Pro / offline-conversion access + GCLID capture with the AM.
