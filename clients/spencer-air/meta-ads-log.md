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
