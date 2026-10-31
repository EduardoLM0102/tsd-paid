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
