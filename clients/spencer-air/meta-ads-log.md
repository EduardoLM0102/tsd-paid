# Spencer Air — Meta Ads Log

**Ad account:** Spencer Air `1845825982372184` (Topservdigital BM, ACTIVE, USD). All spend is here. A second account,
"Spencer Air - Topservdigital" `1900919440286623`, is ACTIVE but spent $0 in the last 30 days.
Pixel/dataset "Spencer Air's Pixel" `1258997717469696` (CAPI dead since 2023, see memory/older notes).

> Running log of paid-social work on this account. Newest entry on top. One entry per work session: what we looked at,
> what we found, what we changed, and what's still open.

---

## 2026-10-06 — Weekly 7-day check (Agency Titan task), setup fixes logged for Edu

**Read-only. Nothing changed in the account.** AT task "7-Day Meta Ads Optimization" (`1febc3d0`) closed with a note;
KPI - Meta entry 10-06 added (Account Health "Mixed").

### What's live
Campaign `Spencer Air | Awareness | ABO | Videos | 30Jun2026` (`120253326490610155`), objective Awareness. Ad set
`Spencer Air | TX | Broad | 22-64 | Awareness` (`120253326490730155`), $40/day on the ad set. 9 videos ("Awareness Video
02–10"). The lead-gen campaign isn't spending.

### Last 7 days (09-29 → 10-05)

| Spend | Impressions | Reach | Frequency | CPM | CTR | Cost per 1,000 reached | Leads |
|---|---|---|---|---|---|---|---|
| $280.21 | 119,683 | 91,802 | 1.30 | $2.34 | 0.16% | $3.05 | 0 (awareness) |

By ad: Video 05 $105.44, Video 10 $75.01, Video 06 $54.04 (84% of spend together); Video 06 has the best CTR (0.37%) and
the lowest CPM ($1.66). Videos 02, 03, 04, 07, 08, 09 got $1–18 each. Meta opportunity score 93; its only
recommendation is mixing image ads in with the videos (+5).

### What's off vs the TSD Meta method (same pattern as All Seasons, 10-05)
1. **Optimization goal is Reach**, not Ad Recall Lift.
2. **Frequency cap: 2 impressions per 7 days.** The ~3x/week awareness target can't be reached; actual 1.30.
3. **Geo:** the 16 service cities (Addison, Allen, Bedford, Carrollton, Coppell, Dallas, Farmers Branch, Flower Mound,
   Grand Prairie, Grapevine, Highland Village, Irving, Lewisville, Plano, Southlake, The Colony), each at a 25-mile
   radius, location type "home + recent". 25 miles around Grapevine/Southlake/Dallas covers most of DFW including Fort
   Worth. A long exclusion list of other Texas cities sits on top. Advantage+ geo expansion is off.
4. **ABO:** budget on the ad set, the TSD method is CBO.

### To do (Edu)
- [ ] Switch to Ad Recall Lift (likely a duplicated ad set, same post IDs), inside a CBO campaign.
- [ ] Raise or remove the frequency cap so it can reach ~3x/week.
- [ ] Geo: people living in the service area only, not 25-mile circles + "recently in".
- [ ] Consider adding a couple of brand-recall statics (Meta's mixed-formats suggestion fits the method: purpose-built
      awareness creative, not conversion creative).

## 2026-10-13 — Weekly 7-day Meta (AT task 2938e9db closed, KPI 75e0da94)

Only the awareness campaign spent (`Spencer Air | Awareness | ABO | Videos | 30Jun2026`, 120253326490610155): $277.85, reach 100,543, impressions 130,592, frequency 1.30, CPM $2.13, CTR 0.19%, 0 leads. Same as 10-06. Lead campaign not spending. No fatigue (freq 1.30). Setup issue unchanged (Reach not ARL, freq cap 2/7d, ABO, 16 cities × 25 mi + recent). **Staged, not applied:** rebuild as CBO + Ad Recall Lift, no cap, living-in geo (All Seasons 10-09 pattern). KPI Health = Mixed. Meta trend/benchmark tools returned no data.

## 2026-10-20 — Weekly 7-day Meta (AT task ef13cf06 completed, KPI 01ec60ce, Gui)

Only the awareness campaign spent (120253326490610155): $282.36, impressions 126,818, reach 91,323, frequency 1.39, CPM $2.23, CTR 0.17%, 0 leads. Video 10 / 05 / 06 = 86% of spend; Video 06 again cheapest CPM ($1.44) and best CTR (0.36%). Second account 1900919440286623 = $0. Setup issue unchanged (Reach not ARL, freq cap 2/7d, ABO, 16 cities × 25 mi + recent). **Staged, not applied:** CBO + Ad Recall Lift, no cap, living-in geo. KPI Health = Mixed.

## 2026-10-27 — 7-Day + 30-Day Meta (AT tasks, Gui via Claude), read-only

Tasks: 7-Day https://app.agencytitan.com/tasks/instance/cdd9505b-e9c7-4ef9-b508-36a8b3846a1b, 30-Day https://app.agencytitan.com/tasks/instance/2244051e-db19-499a-b622-7a182728eefe, both completed. KPI - Meta row e9428f92 (10-27, weekly + 30-day keys). 2nd account 1900919440286623 = $0 in 30d.
**Week 10-20..10-26:** $383.72, 88,987 impr, reach 58,554, freq 1.52, CPM $4.31 (prior $2.23), CTR 0.08%, 0 leads. The CBO/ARL rebuild 120255538868320155 delivered for the first time: $329.31, reach 41,126, freq 1.67, CPM $4.81, 1,110 estimated ad recallers ($0.30, 2.7% of reach). Old ABO Reach 120253326490610155 spent $54.41 then PAUSED. Video 09 = 59% of ARL spend ($0.30/recaller); Video 10 ($0.09) and Video 04 ($0.15) cheaper per recaller. No fatigue.
**30d 09-27..10-26:** $1,308.49, 497,198 impr, reach 267,691, freq 1.86, CPM $2.63, CTR 0.15%. Hook 10.63% (ABO 11.44%, ARL 5.59%), retention 9.26% (ABO 8.87%, ARL 14.21%). Best on the old set: Video 06 (CTR 0.38%, CPM $1.52), Video 10 (most ThruPlays 1,645).
Setup now OK on CBO, ARL, no cap, Advantage+, home only. Still off: 16 cities × 25 mi radius, 1.67/week vs 3x target at $40/d, ad set not DCT (9 separate ads). **Staged, not applied:** tighten geo to the service cities (smaller radius or ZIPs) after learning (~11-03); 2 brand-recall statics; consider one DCT ad set per angle; lead gen stays on hold until CRM outcomes. Health Unclear (awareness only). Toggles (UI, 30-Day): Awareness Reviewed = Yes, Hook-Rate & Retention Checked = Yes, Winning Post IDs Found = Yes, Core Results Declined = No, Last 60 Days Reviewed = No, New Test Deployed = No, New Awareness Ads Launched = No, Older Ads Paused = Yes (old ABO paused), Refreshed With New DC Test = No, Underperformers Found = No.

## 2026-10-28 — fu-075 first-week check of the CBO / ARL awareness campaign (read-only, NO changes)

Campaign 120255538868320155, first full 7 days 10-21 → 10-27 (Meta MCP).
| Spend | Impressions | Reach | Frequency (7d) | CPM | CTR | Est. ad recallers | Cost / recaller |
|---|---|---|---|---|---|---|---|
| $365.93 | 76,125 | 43,202 | **1.76** | **$4.81** | 0.09% | 1,300 | $0.28 |

- **Pacing OK:** launch-week front-loading ($50–69/d 10-21 → 10-24), then $37–43/d from 10-25 on the $40 budget. Old ABO campaign spent
  $15.11 on 10-21 (the day after the pause), $0 since. No duplicates.
- **Frequency 1.76/week, not the ≥3 target.** The cap is gone, but $40/d can't reach 3x on this audience (16 cities, 25-mile radius each =
  most of DFW). At $4.81 CPM, 3x/week on ~43k people ≈ 130k impressions ≈ $90/day. The other lever is a smaller audience: tighten the
  radius to the real service area so $40/d reaches ~25k people 3x.
- **CPM $4.81 vs old $2.13–2.34:** expected. ARL buys people likely to remember the ad (pricier than cheapest reach), and living-in
  targeting removes cheap travelers.
- **All 9 videos ACTIVE and delivering.** CBO put 56% on Video 09 ($207) and 18% on Video 06 ($67); the rest $5–36 each. Video 05 CTR 0%.
**Why CPM doubled (Edu asked, checked 10-28):** settings diff old ad set 120253326490730155 vs new 120255538874060155: optimization
REACH → AD_RECALL_LIFT, frequency cap 2/7d → none, location type home+recent → home only. Same 16 cities × 25 mi, ages 22–64, exclusions,
Advantage+ audience, all placements. Placement mix (old 10-06→10-19 vs new 10-21→10-27): old spent **72% on Facebook Marketplace**
($404 at $2.62) + 23% IG Stories ($131 at $1.42); new spends **62% on IG Reels** ($227 at $4.91) + 29% IG Stories ($105 at $5.01),
Marketplace $0.05. Same placement also costs more under ARL (IG Stories $1.42 → $5.01, IG feed $1.91 → $4.63, FB feed $2.49 → $3.84).
So the goal change drives it twice: it left cheap, low-attention Marketplace inventory for Reels/Stories, and it bids for people more likely
to remember the ad. Removing the cap would normally LOWER CPM, so it isn't the cause.
**Proposed (Edu to decide):** tighten the geo (the open 10-20 question: 25-mile radius → ~10 miles, or the core cities only) to reach 3x/week
at $40/day. Or keep the geo and fund ~$90/day from the unspent Google budget (needs the AM/client, ties to fu-100).

---

## 2026-10-20 — Awareness switched to the 10-13 CBO/ARL rebuild; old ABO campaign PAUSED (Edu: "make them go live and make sure that we wont have duplicate campaigns")

No new build: a rebuild already existed, PAUSED since 10-13: `Spencer Air | Awareness | CBO | ARL | Videos | 13Oct2026`
(120255538868320155), CBO $40/d, ad set `Spencer Air | TX | Advantage+ Audience | 22-64 | ARL` (120255538874060155):
optimization **AD_RECALL_LIFT**, **no frequency cap**, location type **home only** (people living in), Audience Network off,
same 9 creative IDs as the old ads (post social proof carries over).
**Done (live, read-back):** new campaign + ad set + all 9 ads ACTIVE (ads IN_PROCESS = review; Video 08 needed 2 retries after a
Meta internal error). Old `Spencer Air | Awareness | ABO | Videos | 30Jun2026` (120253326490610155) **PAUSED** (its ads show
CAMPAIGN_PAUSED). So only one awareness campaign runs; total stays $40/d.
**Left as built:** geo is still the 16 service cities at 25-mile radius (covers most of DFW); the old exclusion list wasn't
carried over (far-away Texas cities, irrelevant at this radius). Tightening the radius = Edu's call.
**Account hygiene, not touched:** 5 very old campaigns still show ACTIVE with $0 spend (Valentine Giveaway 2022, Christmas
Giveaway-2021, Thanksgiving Giveaway 2021, Velentines Promo, Job Ad - AC/Heating Service Techs); they don't deliver.
⚑ First-week check 10-27 (fu-075): frequency heading to ≥3/wk, reach, CPM vs old $2.13–2.34.

## 2026-11-02 — Pixel correction for Alex's CAPI test

Alex (DM 10-29) asked for a Test events code on pixel 3027702340698908. Edu: that ID was his mistake, the right pixel is **1258997717469696** (same as live GTM-KT5RPTP v11 vars 11 + 39 and Alex's CAPI). Edu generated Test events code **TEST84597** on 1258 and a new CAPI token; both sent to Alex in DM 11-02 ~09:36 BRT (token not stored in the repo). Nothing changed in GTM.

## 2026-11-03 — 7-Day Meta (AT task, Gui via Claude), read-only

Task https://app.agencytitan.com/tasks/instance/a148fea0-e6de-40f0-8353-80497e1f83a3 completed, KPI - Meta row 70254e07 (11-03, cost_per_result = cost per recaller). Week 10-27..11-02: only ARL campaign 120255538868320155 spent, $289.15 (prior $383.72 incl. $54.41 old ABO), 60,414 impr, reach 34,529, freq 1.75 (prior 1.67), CPM $4.79, CTR 0.10%, 0 leads. 1,770 estimated ad recallers at $0.16 (prior 1,110 at $0.30), 5.1% of reach. Hook 6.68%, ThruPlay/3s 12.5%. Video 09 $130.28 ($0.15), Video 06 $94.68 ($0.14, 194 ThruPlays); Video 10 $0.05 and 04 $0.07 cheapest at low spend. No fatigue, no frequency cap, Advantage+, home only. Still 16 cities x 25 mi, 9 separate ads (not DCT), 1.75/wk vs 3x target. 2nd account 1900919440286623 $0. **Staged, not applied:** tighten geo (smaller radius / service ZIPs) to lift frequency at the same budget; 2 brand-recall statics; one DCT ad set per angle. Lead gen on hold. Health Unclear.

## 2026-11-10 — 7-Day Meta (AT task, Gui via Claude), read-only

Task https://app.agencytitan.com/tasks/instance/8ee50da5-5281-46d8-9932-108e2888812f completed, KPI - Meta 8b669b77 (cost_per_result = cost per recaller). Week 11-03..11-09: ARL CBO 120255538868320155 only, $274.43 (prior $289.15), 66,876 impr, reach 37,477, freq 1.78/wk (prior 1.75), CPM $4.10, CTR 0.12%, 0 leads. 2,020 recallers at $0.14 (prior 1,770 at $0.16), 5.4% of reach. Hook 7.5%, ThruPlay/3s 12.3%. Video 09 $121.98 ($0.12), Video 06 $76.96 ($0.11); cheapest at low spend Video 10 $0.04, 03 $0.07. Ad freq 1.1-1.5, no fatigue. Old acct 1900919440286623 $0. Frequency still under the ~3x/week target with reach growing: budget gap, not audience. Nothing staged beyond that (more awareness budget only with client approval).

## 2026-11-17 — 7-Day Meta (AT task, Gui via Claude), NOT done

Task https://app.agencytitan.com/tasks/instance/0c28fee8-0a0c-499e-8e4e-4ade828937b8 left OPEN, no KPI - Meta row. The Meta MCP `ads_get_ad_entities` returned "Tool definitions have changed since your session started" on every call (connector needs a refresh/restart), so no spend/reach/frequency numbers could be read. What did work: activity log since 11-03 shows no changes on 1845825982372184 (only "Account billed" $665.00 on 11-17), and the performance-trend tool rates the ARL ad set 120255538874060155 CPM trend GOOD ("12.40% change", CTR "59.45% change", direction not stated) with no window numbers. Redo after refreshing the Meta connector: week 11-10..11-16 vs 11-03..11-09, ARL CBO 120255538868320155 + check 1900919440286623.

## 2026-11-17 (later) — 7-Day Meta DONE after the Meta connector refresh (Gui via Claude), read-only

Task https://app.agencytitan.com/tasks/instance/0c28fee8-0a0c-499e-8e4e-4ade828937b8 completed, KPI - Meta 25efa238 (cost_per_result = cost per recaller). Week 11-10..11-16: ARL CBO 120255538868320155 ($40/d) only, $277.47 (prior $274.43), 60,981 impr (prior 66,876), reach 32,662 (prior 37,477), freq 1.87/wk (prior 1.78), CPM $4.55 (prior $4.10), CTR 0.13%, 0 leads. 1,660 recallers at $0.17 (prior 2,020 at $0.14), 5.1% of reach. ThruPlays 573. Video 09 $106.48 + Video 06 $93.12 = 72% of spend; others $6-21 at freq ~1.17. No fatigue. Old acct 1900919440286623 $0. Still under 3x/week = budget gap (about 1.6x the $40/d for this reach, only with client approval). Nothing staged beyond that.
