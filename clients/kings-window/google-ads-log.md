# King's Window Services — Google Ads log

Customer ID `6769493219` — "King's Window Services - PPC & LSA" (PPC and LSA live in the same
customer ID here, unlike most TSD clients). Not in `contas.yaml` yet — found via `customer_client`
under MCC `4155514468`. Site: kingswindowservices.com. GA4 property `389493105`. GTM container
`GTM-MNF2N73B`.

---

## 2026-08-31 — PMax paused, budget shifted to Nonbranded Search; keyword cleanup

**Executed** by Edu (Head of Paid, verbal authority) after reviewing account status.

### Changes

| # | Object | ID | Before | After |
|---|---|---|---|---|
| 1 | `phone_call` conversion action (real CallRail calls, GA4 import) | 7314063586 | `primary_for_goal: False`, `include_in_conversions_metric: False` | **`True` / `True`** — now counted toward Conversions + biddable |
| 2 | Nonbranded Search `TSD_28.04_Search_Nonbranded_Evergreen` — network settings | 23796640968 | `target_search_network: True` (partners on) | **`False`** |
| 3 | 10 broad keywords, 0 conversions / 30d, spread across Glass Replacement, Frameless Shower Enclosures, and Window Replacement ad groups (list below) | — | ENABLED | **PAUSED** |
| 4 | PMax `TSD_Pmax_WindowServices_Calls` | 23036120066 | ENABLED, $20/day | **PAUSED** |
| 5 | Nonbranded Search budget (`campaignBudgets/15547840993`) | 23796640968 | $32/day | **$52/day** |

Account-level daily budget unchanged (~$82/day live spend capacity) — PMax's $20/day moved into
Nonbranded, not added on top. No client-facing total budget change.

**Keywords paused (10, all $0 return over trailing 30 days):**
glass replacement near me ($68.14), glass repair service ($38.97), residential glass replacement
($37.56, QS 1 — worst score in the account), bathroom shower glass ($36.96), bathroom shower
remodel doors ($24.41), glass shower door service ($21.38), shower enclosure installation
($19.62), replacement windows for home ($24.70), glass companies near me ($24.58), window fixer
near me ($23.86). ~$320/mo of campaign spend freed, zero conversions lost.

### Why

- PMax relaunch (see 2026-08-17 change in [[tsd-kings-window]] memory) delivered 1 conversion in
  12 days for $150.92 (~2.15x its $70 tCPA target), lumpy delivery (several $0 days, then bursts
  ~2x its daily budget), flagged `LIMITED / BUDGET_CONSTRAINED` by Google. Second underperformance
  strike after the mid-July overspend/auto-throttle crash on the same campaign.
- Nonbranded Search converts reliably ($47–83 CPL by keyword) but was both rank-capped (55.6%
  impressions lost to Ad Rank) and, as of this week, budget-capped too (28.6% lost to budget,
  up from ~7.5% two weeks prior) — real headroom to buy more volume at a proven CPL.
- Edu's call: prefers Search carrying the large majority of spend; PMax's delivery pattern has
  been unreliable twice now.

### Flag for correlation — READ THIS FIRST if the client asks about traffic/volume changes

**2026-08-31**: PMax campaign fully stopped (was running since 2026-08-17 post-relaunch, before
that since account start). If total account traffic/impressions drop noticeably in the days
following this date, PMax's removal is the most likely cause (it was still delivering real
impression volume — Cross-network/Display/YouTube reach — even though it converted poorly). Lead
*volume* should hold or improve (spend moved to a channel with a real, proven CPL); raw
impressions/reach will likely drop since PMax's placements (Discover, Gmail, YouTube, Display)
disappear entirely. Check this entry before assuming a tracking break if the client flags a
volume or reach change in the next few weeks.

### Open items
- Re-verify `phone_call` conversion volume accumulates cleanly over the next 1-2 weeks now that
  it's biddable — GA4 attribution is still ~80% "Unassigned" for this event (unresolved, parked
  per Edu 2026-08-31), so actual usable signal will be thinner than raw event counts suggest.
- Once phone_call data is clean, retune Nonbranded's implicit CPA expectation (no tCPA cap
  currently set — running plain Maximize Conversions).
- Decide whether PMax gets a third attempt later (better landing assets, logo files added, tighter
  budget) or stays off for good — not decided, just paused for now.

---

## 2026-09-15 — Weekly PPC snapshot pull + conversion trust check

**Read-only session** — no live changes, reporting only.

### What was pulled
Standard 7-day snapshot (see `[[tsd-weekly-ppc-snapshot]]` recipe), PPC only (Nonbranded +
Branded Search), LSA and paused PMax excluded:

| Metric | Value |
|---|---|
| Spend | $433.58 |
| CPL | $21.70 |
| CPC | $6.57 |
| Total Conversions | 19.98 |
| Conv. Rate | 30.28% |
| Branded Conversions | 3.98 |
| Unbranded Conversions | 16.0 |
| Branded CPL | $4.36 |
| Unbranded CPL | $26.01 |
| Impression Share (Search, blended) | 20.0% |

LSA (same customer ID, excluded from the table): 4.0 conversions / $328.03.

### Conversion trust check
Broke the 19.98 PPC conversions down by `segments.conversion_action_name` — all real lead
signals, no page_view/tap-click junk:

| Action | Category | Count |
|---|---|---|
| GA4 `phone_call` (CallRail-verified calls) | Phone Call Lead | 13.98 |
| Submit lead form | Submit Lead Form | 3.0 |
| GA4 `ghl_request_estimate` | Submit Lead Form | 2.0 |
| Repeat Phone Call | Default | 0.98 |

LSA's 4.0: `local_services_phone_lead` (Phone Call Lead, 3.0) + `local_services_message_lead`
(Unknown category — a text/message inquiry, not a call, 1.0).

**Open question, not investigated this session:** "Repeat Phone Call" is a separate legacy
Google Ads action from the GA4 `phone_call` import — worth checking whether the two are double
counting the same physical calls before leaning on the combined phone-call total.

---

## 2026-09-15 — Tracking rebuild

**Reported by Edu via chat, not executed by Claude this session.**

Tracking rebuilt and fixed. Old tags deactivated to make sure they don't disrupt or interfere with
the new setup.

---

## 2026-10-05 — Weekly 7-day check (Agency Titan task): no changes needed

**Read-only.** Last 7 days (09-28 → 10-04), PPC only (LSA excluded):

| Campaign | Spend | Clicks | Conv | CPL |
|---|---|---|---|---|
| TSD_28.04_Search_Nonbranded_Evergreen | $276.90 | 48 | 14 | $19.78 |
| TSD_03.16_Search_Branded_Evergreen | $7.74 | 4 | 2 | $3.87 |
| **Total** | **$284.64** | **52** | **16** | **$17.79** |

Account search IS 20.2% (56.2% lost to rank, 23.6% to budget). Conversions mostly GA4 `phone_call` (CallRail-verified)
plus `[TSD] Click to call` taps and lead forms. LSA same week: $298.16, 5 leads.

**Search terms:** clean. Window-screen searches kept open on purpose: the site lists "Window Screens & Accessories" and
"Screen Repair & Replacement" (checked 10-05). Competitor names get impressions (Glass Doctor, Ajax, Keller Glass, Lone
Star Glass), but "binswanger glass fort worth" converted once, so none were blocked. Decision for Edu.

**Agency Titan:** task closed with a note; KPI - Google Search entry 10-05 (Account Health "Good").

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $385.63, 66 clicks, 23 conv, $16.77 CPL (prior $21.08/16). Nonbranded 23 conv = 9 [TSD] Click to call taps, 8 GA4 phone_call, 3 Calls from ads, 3 forms (≈14 non-tap leads at ~$27). call_view 9 calls, 3 ≥60s. Branded $14, 100% IS. Nonbranded 42% IS lost to budget (16% last week) at $16 CPL: budget is the lever, needs client written OK via AM. LSA $578.33, 6 leads. KPI Health = Good.

**Changed:** nothing, no changes needed. AT task 2627ca2d closed, KPI record edf2fc90.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-19 — Weekly 7-day pass (Google + LSA + Meta) + 14-day review (Agency Titan tasks, Gui): read-only, all staged

**PPC 10-12..10-18:** $371.79, 17 conv, $21.87 CPL (prev $435.97 / 24 / $18.17). NB $353.62 / 17 (8 taps, 6 GA4 phone_call, 2 forms, 1 calls from ads; ~9 non-tap at ~$39). IS 20%: budget-lost 37%→12%, rank-lost 68%. Branded $18.17, 100% IS. Staged neg: 'kings windows and doors'.
**LSA (inside 6769493219):** $622.07, 7 leads (5 calls, 2 msg), $88.87, 98.4% top.
**Meta 483679897962388:** $294.65, 6 leads, $49.11. Lead campaign is ABO ($30+$15 ad sets). **Awareness `TSD_02.26_TOF_AWARENESS_CBO_Creatives` = REACH + frequency CAP 3/7d** (off doctrine) → rebuild as ARL no cap, staged.
**14-day (10-05..10-18):** $807.76 / 41 conv. Rank is the limit (53% rank-lost); 'glass company near me' QS 3 carries 29/41 conv → improve ad/LP relevance; low-QS glass/shower keywords; remove Branded kw 'king's window repair houston'; outside-target clicks only 7% (Fort Worth, Grapevine). No audiences.
AT tasks 1a6a8163 / 5f8a5a77 / 567d82cd / cb7050b0 left open for Gui's review.

---

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Google Ads / LSA. All staged.

**7-day PPC 10-19..10-25:** $354.57, 46 clicks, 12 conv, $29.55 CPL (prior $371.79 / 17 / $21.87). 12 conv = 6 [TSD] Click to call taps, 5 GA4 phone_call, 1 form; call asset 2 calls (44s, 29s), 0 counted. ~6 real leads at ~$56 on NB. NB IS 19.7%, budget-lost 54% (was 12%), rank-lost 26%. Branded $19.44, 91.7% IS. Competitor terms $51.81 / 4 conv (kept open). No account changes since 10-16. KPI Health = Mixed.
**30-day:** $1,574.66 / 72 conv / $21.87 (prior 30 $1,657.58 / 71). RSA performance labels not returned (all NOT_APPLICABLE); by asset stats best headlines 'Same Day Glass Service', 'Affordable Glass Repair'. Shower LP 1 conv / 20 clicks, shower RSA AVERAGE. 'glass company near me' QS 3 = $1,031.68 / 51 conv. 100% PPC spend in targeted locations.
**90-day:** $4,837.06 / 161 conv / $30.04. Stalled primaries: ghl_request_estimate last 09-23, phone_link_click last 08-13, 0 for 90d on Phone Call, ghl_contact_us, ghl_schedule_service, Clicks to call, Local actions, Store visits. Branded double counts GA4 phone_call + First Time/Repeat. 12am-6am $456.45 / 7 conv ($65 CPL), Sunday $74.87 CPL. No audiences attached.
**LSA:** 7d $332.14, 5 charged leads (4 calls, 1 msg), $66.43, top 99.5%, budget $428.57/d → Underspending (demand/schedule-limited, Mon-Fri 8-5). 30d $1,608.91, 23 leads (20 charged), $80.45 per charged lead, 0 credits/disputes, 4 BOOKED / 4 DECLINED / 15 ACTIVE (17.4% floor).

**Staged, not applied:** NB budget raise needs client written OK via AM; taps → secondary (Edu decision); '$99' phrase neg on NB, hold 'kings windows and doors' until client confirms; own ad group for 'glass company near me'; NB ad schedule off 12am-6am; structured snippet + image on Branded, swap weak headlines, rewrite shower descriptions + improve shower LP; tracking task (Gui) for stalled primaries + Branded double count; observation audiences; LSA: dispute 10-07 16:26 + 10-08 14:30 out-of-area charged calls, office to mark lead status, Saturday hours if staffed.

Tasks (all completed): [7-Day Google](https://app.agencytitan.com/tasks/instance/b70c9a91-9ddc-4af8-afbe-a160b0d3e6e9) (KPI d7cbc6aa), [30-Day Google](https://app.agencytitan.com/tasks/instance/b9146e5f-b176-4eb4-ac4d-110d1eaa0648), [90-Day Google](https://app.agencytitan.com/tasks/instance/2d635aa8-0565-43ac-a3be-f44ab51dead2), [7-Day LSA](https://app.agencytitan.com/tasks/instance/72a99537-bbaa-4bac-bae0-0217b747a803) + [30-Day LSA](https://app.agencytitan.com/tasks/instance/c71b6d60-cabd-4bb9-b7a3-6e38991040fa) (KPI LSA 49dbdedf). Meta: see meta-ads-log.md.

## 2026-11-06 — LSA moved to Pay-per-lead PMax by Google (read-only, nothing changed)

Old LSA `23025462677` paused; new `24431038949` created 11-04 11:55. SERVING / LEARNING, asset group ELIGIBLE → homepage, budget
$428.57/d, ad schedule carried over (5 criteria), 10 locations. Billing approved, insurance + background check passed.
Impressions held: old 59 / 59 (11-02/03) → new 65 on 11-05 (9 clicks, $78.90, 1 lead). Leads by day 11-02..11-05: 4, 2, 2, 1. Not dark.

**Context:**
Google (not TSD) is moving LSA into a new campaign type, "Pay-per-lead PMax". It creates a PERFORMANCE_MAX campaign
(`Pay-per-lead-PMax-<business>`, Max Conversions, same daily budget as the old LSA, one asset group `xcat:service_area_business_<trade>`)
and pauses the old `LocalServicesCampaign:SystemGenerated`. Still billed per valid lead, still Search + Maps only, badge carries over.
What changes: no manual bidding, one campaign-level target instead of one per trade, weekly budget becomes a daily average, old LSA
dashboard reports don't migrate (lead history does). Sweep of all 57 enabled MCC accounts on 11-06: 7 switched on 11-03/11-04
(Watt's Right, Amazing Morrow, Golden, Gray Duct, King's Window, Nick's, Spencer). Full write-up: `_contexto/memoria/tsd-lsa-ppl-pmax-migration.md`.

Data notes: `local_services_lead` still returns leads after the switch (lsa_report.py lead data OK). Spend/metrics now sit on the
PMax campaign, so anything filtering on channel LOCAL_SERVICES (google_channels.py) misses them. **$0 spend ≠ dark**: only charged
leads cost money, clicks are free. Judge delivery by impressions + leads per day.

---

## 2026-11-10 — META: lead campaign dark since 10-17, old ad set RE-ENABLED (Edu's go)

**Found (Meta 483679897962388):** `TSD_04.29_BOF_Leads_Evergreen` spent $40–50/day through 10-16, $3.89 on 10-17, $0 since.
10-17 ~02:00 Gui built `Richlandtx_Broad_18.65_M.F_Dynamic` ($30/d, 120254214478390721) with one ad
`GlassReplace_Ads1,2,3_Dynamic_callform_FO` (120254214546330721), then paused both working ad sets
(`Richlandtx_Broad_18.65_M.F` $30/d and `... 2` $15/d). The new ad went "Update Required" (issue code 2465018,
"Unknown Error When Creating Ad ... try creating your ad again") the same night; retried 10-26, same error. Never spent.
Account ran on the $10/d awareness campaign only: Oct $1,023 (vs $1,650–1,700 Aug/Sep), Nov 1–9 $91.
Gui's 7-Day Meta AT task f4c80451 (closed 11-09) already noted the campaign dark since 10-17, fixes staged not applied.
Also: dynamic ad set geo includes a pin at Willis TX (lat 30.42 / lng -95.44, ~250 mi from NRH), likely a mis-geocoded
"Fort Worth Dr" address. Remove before that ad set ever runs.

**Changed 11-10:** ad set `Richlandtx_Broad_18.65_M.F` (120246749328610721) PAUSED → ACTIVE. Ad `GlassReplace_Image_callform_FO`
(120247045640540721) delivery = active (read back). Other 3 ads in that ad set stay paused. Broken dynamic ad set untouched (not delivering).
**Open:** rebuild the dynamic ad from scratch (not a duplicate), drop Willis pin, then decide which ad set carries the $30.


## 2026-11-13 — Two AT Client Requests from Lee (Angela 11-12), both in Execution on Edu

- **"spend" (AT 25df0be2):** Q3 actuals + Q4/Q1 projections. Pulled from Google 6769493219 (LSA incl. pay-per-lead PMax, Search, PMax) + Meta 483679897962388. Q3 = $17,708 (LSA $7,265 / NB Search $4,604 / Branded $278 / PMax $849 / Meta $4,711). Oct $4,672; Nov 1-12 $2,011 (~$5,000 pace). Projection written at **$5,100/mo** (= the Oct/Nov strategy review rec, row d233f769): Q4 ≈ $14,800, Q1 ≈ $15,300; split LSA ~$2,400 / NB ~$2,000 / Brand ~$80 / Meta ~$620. Seasonality from last winter's LSA leads (Nov 18, Dec 12, Jan 33, Feb 25, Mar 50; Google-only spend Oct-25..Mar-26 was $859–$5,297/mo, pre-TSD Search). Completion Notes written via API addressed to Angela, Execution left open for Edu. Growth Engine excluded. AT client budget field not readable today (connector errors).
- **"Negatvie Keywords" (AT cf56717b):** Lee asks for "shutter repairs" as a negative. Safety check 2026-05-01..11-12: 6 shutter search terms, 1 click, $0.09, 0 conv; no shutter keywords bid; none of 120 converting terms contain "shutter". Rec: PHRASE negatives "shutter" + "shutters" on Nonbranded 28.04 (and Branded). NOT applied, waiting on Edu's go; no shutter calls in the transcribed logs since 10-01, so the calls Lee mentioned are probably LSA (a Search negative won't touch those).
- **11-13 later:** 1-page client PDF built for the spend task: `clients/kings-window/Kings-Window-Ad-Spend-Breakdown_2026-11-13.pdf` (plain Times, Q3 table, Q4 so far, projections at $5,100/mo, seasonal LSA note; Growth Engine excluded). AT API was down (3 errors), so the Completion Notes text was handed to Edu to paste; draft text in `at-spend-breakdown-draft-2026-11-13.md`.
- **11-13 APPLIED (Edu's go), `kings_shutter_negs_1113.py`:** PHRASE negatives `shutter` + `shutters` on Nonbranded 23796640968 and Branded 23666406217, read-back OK (45 → 47 campaign negatives each). Blocks 6 research terms since mid-May ($0.09 total, 0 conv); no live keyword or converting term contains "shutter". AT cf56717b answer written for Angela (API) or handed to Edu to paste if AT is still down. Lee's shutter calls likely came via LSA/GBP, not Search; LSA has no negatives, only the service list on the profile.
- **11-13 SENT:** Edu pasted both answers into AT (25df0be2 spend breakdown + PDF attached; cf56717b shutter negatives) and completed the Execution stages → with Angela. fu-165 closed.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Google Ads / LSA. All staged.

**7-day PPC 10-27..11-02:** $356.70, 50 clk, 15 conv, $23.78 CPL (prior $352.24 / 18 / $19.57). 15 conv = 7 GA4 phone_call, 5 [TSD] Click to call taps, 2 forms, 1 Calls from ads → ~10 real leads at ~$34 on NB (10-26: ~6 at ~$56). NB IS 18.1%, budget-lost 38.9%, rank-lost 42.9%; 11-02 NB spent $98.33 on $52/d (week within cap). Branded $18.56 / 0 conv, IS 87.5%. Competitor terms $45.52 (king glass $17.02 / 0, glass doctor near me $12.19 / 2, runnels $9.77 / 0, pilkington $6.54 / 0). No account changes since 10-16. KPI Health = Good.
**14-day 10-20..11-02:** $708.94 / 33 conv / $21.48 (prior 14 $774.92 / 41). 'glass company near me' QS 3 (CTR + ad relevance below) = $555.38 / 28 conv; 100% PPC spend in targeted locations (Presence); 1 RSA per ad group (shower AVERAGE); /glass-replacement/ 29 conv / 73 clk; no audiences; 75 auto recs open; 12am-6am $40.30 / 0 conv.
**LSA:** 7d $625.08, 7 charged leads (6 calls, 1 msg) + 3 uncharged, $89.30 (prior $447.02 / 6 / $74.50), top 100%, abs top 85%. API budget $428.57/d → Underspending (schedule Mon-Fri 8-5 limits volume). 1 BOOKED, 9 ACTIVE.

**Staged, not applied:** NB phrase negs king glass / runnels / pilkington (keep glass doctor + binswanger, they convert); confirm with client if cabinet / table-top glass is a service; own ad group + matched RSA for 'glass company near me'; 'custom shower glass company' ($27.34 / 0) pause or phrase; NB schedule off 12am-6am; observation audiences; reject search partners / display expansion / broad match / PMax / tCPA recs; NB budget raise needs client written OK via AM; carry-over tracking task + LSA disputes 10-07 / 10-08.

Tasks (all completed): [7-Day Google](https://app.agencytitan.com/tasks/instance/2c98bc41-18ad-4bc2-bf7b-bfe9625b9147) (KPI 74e559d6), [14-Day Google](https://app.agencytitan.com/tasks/instance/51fe37ca-8ec1-461c-b7d6-a097e97e986c), [7-Day LSA](https://app.agencytitan.com/tasks/instance/f06b6a6e-a65e-413d-97d6-0f1db4962750) (KPI LSA 5cb0a715). Meta: see meta-ads-log.md.

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Google Ads / LSA. All staged.

**7-day PPC 11-02..11-08 (Branded + NB only):** $381.97, 59 clk, 20.25 conv, $18.86 CPL (prior $327.02 / 15 / $21.80). NB $367.20 / 18.25 conv = 6.1 GA4 phone_call, 5.1 [TSD] Click to call taps, 4 Calls from ads, 3 forms → ~13 real leads at ~$28; call_view 8 NB calls, 4 of 60s+. Branded $14.77 / 2 real calls, IS 85.7%. NB IS 20.9%, budget-lost 41.0%, rank-lost 38.1%; NB spent its full $52/d. 'glass company near me' (QS 3) $272.49 / 17.3 conv. Competitor terms $41.07 / 6 conv ('king glass company' converted 1 → drop 'king glass' from the 11-03 neg list). Mirror / glass-cutting terms $15.95 / 0.3. 100% PPC spend in targeted locations. No user changes since 10-20. KPI Health = Good.
**⚠ NEW: 'Pay-per-lead-PMax-King's Window Services LLC' (24431038949)** appeared 11-04 11:55, no change_event (not created by a TSD user). Same $428.57/d budget as LSA, asset group named after the LSA category, homepage URL, Mon-Fri, Search + Maps only. $225.70 / 3 'Phone calls (Pay-per-lead goals)' on 11-05..11-06 (~$75/lead); its 3 leads are in the LSA lead list and the LSA campaign spent $0 from 11-05. = LSA leads billed through a PMax shell → counted under LSA, excluded from the PPC KPI (with it: $607.67 / 23.25 / $26.14). Confirm with Edu (Google migration or opt-in) before touching it.
**LSA (LSA + pay-per-lead PMax added):** $896.01 (LSA $670.31 11-02..11-04 + PMax $225.70), 12 leads, 10 charged (9 calls, 1 msg), $89.60 per charged lead (prior $588.19 / 7 / $84.03). LSA impr 145 (prior 325) + PMax 127; LSA top 98.96%, abs top 79.2%. Underspending vs API $428.57/d (30%), schedule-limited. All 12 ACTIVE. LSA campaign shows PAUSED in the API but SERVING (status quirk). 11-06 three glass_installation calls in 23 min, 2 charged (12:19 + 12:42): dispute 12:42 if same caller.

**Staged, not applied:** NB budget raise needs client written OK via AM; mirror / glass cutting phrase negs if client confirms not a service; drop 'king glass' neg, keep glass doctor; carry-over from 11-03 (own ad group for 'glass company near me', shower kw pause/phrase, NB 12am-6am off, audiences, tracking task, LSA disputes 10-07/10-08).

Tasks (all completed): [7-Day Google](https://app.agencytitan.com/tasks/instance/d37877f0-d6bb-4ad0-8787-d058f4044e07) (KPI 27e35d7d), [7-Day LSA](https://app.agencytitan.com/tasks/instance/f8d877c7-f104-4d64-8eaa-7c88a45d4551) (KPI LSA 31df0bfc). Meta: see meta-ads-log.md.

## 2026-11-12 — Post Strategy Review: Paid Ads Alignment check (Gui, via Claude)

Read-only, nothing changed in Google Ads / LSA / Meta. The Strategy Review (call 11-10) has only our pre-call report, no call notes: no Top Marketing Services or budget decision recorded, so alignment can only be checked against the pre-call recommendations.

**Google 11-05..11-11:** Branded + NB $386.71 / 60 clk / 16.25 conv (NB $373.13 / 14.25; Branded $13.58 / 2 ad calls). NB budget still $52/d (11-09 spent $103.89, within Google's 2x day), Branded $30/d Target IS. Ad groups live: Glass Replacement ($315.83 / 11.25 conv), Window Replacement ($15.21 / 2), Frameless Shower ($42.09 / 1); 1 approved RSA each, each on its own service page; Branded RSA on the homepage. LSA now = 'Pay-per-lead-PMax' 24431038949 ($428.57/d API, Mon-Fri 8-5): $294.28 / 4 pay-per-lead calls (11-05, 11-06, 11-09). Old LSA, old PMax and 4 legacy Search campaigns $0. No change_event since 11-10 → **the +$500/mo NB raise from the pre-call report is NOT applied** (needs client written OK).
**Run rate:** PPC ~$1,680/mo + LSA ~$1,260 + Meta ~$1,220 ($30/d lead + $10/d awareness) ≈ $4,150/mo vs the ~$5,100 recommended.
**Geo:** NB = 16 NE Tarrant / Mid-Cities cities incl. Fort Worth (Presence); Branded = 20 mi around NRH; pay-per-lead PMax = 10 cities (Presence or interest, Google-set). No geo change was proposed.
**Auto-glass negatives:** already on Branded + NB as phrase (auto glass, windshield, car window, automotive, safelite) + PMax's 704-term list. 30-day search terms: no auto-glass clicks (only 'the glass truck reviews' $14.03 and 'mobile home window glass replacement' $4.51). If auto-glass calls are coming from LSA, keyword negatives can't fix it → LSA disputes / service category check. Side note: shared list 'Competitos May' (22 terms) is attached to no campaign.
**Tracking (7d):** Calls from ads 6, GA4 phone_call 5.1, [TSD] Click to call taps 4.1 (still primary, inflates), Submit lead form 1, CallRail First Time 3 + Repeat 1 in all-conv only; pay-per-lead calls 4. Leads are being captured for glass, window and shower.
**Meta 11-05..11-11:** old ad set Richlandtx_Broad_18.65_M.F back ON 11-10 ($30/d, GlassReplace_Image_callform_FO): $93.04 / 4 leads / $23.26 in 2 days. Awareness $68.35. The DCT ad set Richlandtx_Broad_18.65_M.F_Dynamic is still ACTIVE ($30/d, $0) with its broken ad 120254214546330721 still WITH_ISSUES: pause or clean up so it doesn't double the lead budget if Meta clears it.

**Checklist ticked in AT:** geo (405d242c), conversion tracking (03192707), escalate to AM (00a2f11b). Left open: TMS review, campaign/TMS alignment, budget match, ad copy/offers, pause deprioritized services (no TMS/budget/offer recorded from the call). Stage NOT completed.
**For the AM:** what TMS and monthly budget were agreed on 11-10; written OK for the +$500 NB raise; current offers/promos to feature in copy; whether auto-glass leads came via LSA; after-hours answering / same-day callback (pre-call rec).

Task: [Post Client Strategy Review](https://app.agencytitan.com/tasks/instance/9f657ee7-e1aa-4095-b0a2-fbc5ef39939b).

## 2026-11-16 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Google Ads / LSA. All staged.

**7-day PPC 11-09..11-15 (Branded + NB only; Pay-per-lead PMax 24431038949 = LSA, excluded):** $397.57, 63 clk, 22.0 conv, $18.07 CPL, CVR 34.9% (prior $381.97 / 20.25 / $18.86). NB $380.32 / 21 conv = 10 GA4 phone_call, 6 [TSD] Click to call taps, 4 Calls from ads, 1 form → ~15 real at ~$25; call_view 7 NB calls, 4 of 60s+. Branded $17.25 / 1 ad call (174s), IS 100%. NB IS 23.3%, budget-lost 32.3%, rank-lost 44.4%; spent $380 vs $364 weekly. 'glass company near me' (QS 3) $256.84 / 15 conv. Last 2 Sundays NB $80.25 / 14 clk / 0 conv (11-15 alone $57.60). Shower RSA now AVERAGE; 'custom shower glass company' 14d $50.54 / 0. Only change: Edu's 11-13 shutter / shutters phrase negs (no shutter terms since). KPI Health = Good.
**14-day 11-02..11-15:** $779.54 / 122 clk / 42.25 conv / $18.45 (prior 14 $681.59 / 29 / $23.50). 100% spend in targeted locations; no audiences; 12am-6am now only $8.74 (old rec dropped); 77 auto recs (63 KEYWORD, partners x2, display expansion, broad, tCPA x2, budget, lead form x3, sitelink), none applied.
**LSA (pay-per-lead PMax only, old LSA $0):** $359.80, 6 leads (5 calls, 1 msg), 4 charged (3 calls, 1 msg), $89.95 per charged lead (prior $896.01 / 10 / $89.60). Impr 247 (prior 271). Top impression rate not reported for this campaign type. Underspending vs API $428.57/d (12%), schedule-limited. All ACTIVE, no credits. Leads halved vs prior week: watch. Rating = TSD Paid's job (fu-161), not done here.

**Staged, not applied:** NB +$500/mo needs client written OK via AM (row d233f769); NB Sunday off (Edu decision); shower kw pause/phrase + new Shower RSA headlines; 'sliding glass shower doors' QS 2 pause; ask client re table top glass / glass cutting / door repair before any negs; reject partners / display expansion / broad / tCPA / lead form recs; carry-over own ad group for 'glass company near me', taps → Secondary, stalled-primaries tracking task, observation audiences; rate the 4 charged LSA leads (11-09 15:01, 11-12 09:34, 11-13 11:32 call, 11-13 12:06 msg) + the 11-06 12:42 one.

Tasks (all completed): [7-Day Google](https://app.agencytitan.com/tasks/instance/b581ae80-2d09-408f-a1f8-5044d86a9186) (KPI 66aa3267), [14-Day Google](https://app.agencytitan.com/tasks/instance/42d3e7b2-d8b0-45fb-ac82-813c2003633d), [7-Day LSA](https://app.agencytitan.com/tasks/instance/9623d886-80c5-4677-b136-8ce5ca86f736) (KPI LSA 433a8062). Meta: see meta-ads-log.md.
- **11-16 call-asset audit (for Alex's portal, read-only):** CallRail WEBSITE POOL number 817-510-8654 (asset 340546433919) is the call asset on 'Branded - Search - King's Window Services #2' (23666426623, ENABLED, $0 in 2026). Pool numbers rotate between visitors, so calls to it get mis-attributed. All other campaigns use the CallRail 'Google Ads Extension' tracker 817-512-7341 (asset 290663581861). Not changed yet: fu-167 (due 11-20). Source: paid/handoffs/alex-naming-audit-2026-11-16/call_assets.csv

## 2026-11-19 — Growth Engine pre-launch BASELINE (read-only; AT 1496977c, Ryan's 11-18 build sheet, fu-196)

Pulled before any brand impression serves (the sheet says it can't be reconstructed later). Window 2026-08-21 → 2026-11-18.
**Branded search volume (TSD_03.16_Search_Branded_Evergreen 23666406217, IS 87-97% so impressions ≈ eligible searches):** Aug 21-31 34 impr · Sep 92 · Oct 49 · Nov 1-18 22 → **~50-95 brand searches a month**. Brand terms 90d: "kings windows" 75 impr, "kings window" 48, "kings windows and doors" 30, "king glass (company)" ~20, "king's window" 2. Almost nobody searches the name today; this is the number the Growth Engine is meant to move.
**GA4 389493105, sessions by month (Sep / Oct / Nov 1-18):** Direct 168 / 182 / 174 · Organic Search 287 / 275 / 165 · Paid Search 290 / 248 / 146 · Organic Social 111 / 142 / 71. Direct ≈ 170-180 sessions a month = the second baseline. (Nov is a partial month.)
**Meta today (483679897962388):** awareness `TSD_02.26_TOF_AWARENESS_CBO_Creatives` ad set `TX_Broad_Homeowners_18.65_M.F` 120242967352230721 = REACH, cap 3/7d, $10/day, ZIPs 76034 Colleyville + 76092 Southlake + 76248 Keller, home+recent, 18-65, Advantage+ audience ON, old videos AD I-IV. Last 30d $298 / reach 28,551 / freq 3.25 / **CPM $3.22** (planning CPM in the sheet is $16.20). Lead campaign ABO $30/d, 13-city 20 km radii + a stray Willis TX pin.
**Videos:** Meta library has only AD I-IV (1:1 + 4:5). The 9 Oct 13 cuts sit in Drive folder "KINGS ADS" (1NCxMwJQp742o2om-vl_gReSf2QXCgu_K, copied by Sara 10-27; SB 01, SB 03, SB02 V2, SB 06, SB 09 SUIT...), 16:9 .mov/.mp4, never uploaded, no client approval on record (fu-187).
**Google:** no YouTube/Video campaign exists on 6769493219. Branded Search $30/d.
