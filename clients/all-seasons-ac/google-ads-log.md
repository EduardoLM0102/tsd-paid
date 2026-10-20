# All Seasons AC — Google Ads Log

**Client:** All Seasons AC (HVAC — residential cooling/heating, incl. Mitsubishi/Daikin ductless mini-splits)
**Account:** All Seasons AC — Customer ID `4467722415` (under MCC Topservdigital `4155514468`)
**Platform:** Google Ads (PPC). Not yet added to the skill's `contas.yaml` registry (found via `customer_client` query under the MCC — wasn't in the known-accounts list).
**GA4:** Property `312966741` ("All Season - GA4"), under GA4 account "All Season" (`accounts/137389351`). Accessible via `ga4.py`.

> Running log of paid-search work on this account. Newest entry on top. One entry per work session: what we looked at, what we found, what we changed, and what's still open.

---

## 2026-10-19 — Weekly 7-day pass, Google + LSA (Agency Titan tasks 5d7481ca / 74e89c01, Gui): read-only, staged

**PPC 10-12..10-18:** $827.25, 16 conv, $51.70 CPL (prev $1,353.80 / 31 / $43.67). Spend fell with the temporary $2,500 budget (Client Request bff1955c): ~$210/d to 10-14, then $118 / $58 / $15 / $7 (10-18). **Edu 10-15:** Branded Evergreen, PMax Mitsubishi-Ductless, Search Mitsubishi-Brand PAUSED; live = LeadGen $14 + Nonbranded $8 + MiniSplit $24 ($46/d). **10-16:** ~146 negatives (LeadGen 44 / NB 53 / MiniSplit 49), 12 kw pauses, geo target type changed on Search campaigns, AI Max/asset settings. Conv: 8 call ext LEAD + 8 taps; call_view 8 (4 60s+). IS <10% (63–81% budget-lost). KPI Health Mixed.
With Branded paused, brand searches land in LeadGen/MiniSplit broad at $10–17/click; 'petro home services' still buys in MiniSplit ($75, only exact 'petro' excluded). Staged: 'petro' phrase neg on 3 campaigns; decide Branded inside the $2,500; fu-049 UI auto-apply still open.
**LSA 8655979348:** $289.31, 4 leads (2 calls, 2 msg), $72.33; all spend 10-12..10-15, Oct cap hit 10-15 → dark to 11-01 (Overspending). Both message leads still NEW (no reply) → AM flag.

---

## 2026-10-14 — LSA account found + weekly LSA task done (AT 363a93f3, closed)

**LSA account:** `8655979348` (865-597-9348), under MCC Topservdigital `4155514468`, separate from PPC. Edu: it was missing verification documents before, now live. One campaign `LocalServicesCampaign:SystemGenerated` (23394236866), ENABLED / SERVING, $35.71/d (= the $250/wk agreed 09-14), schedule 7 days 8am-5pm. Insurance PASSED (exp 2027-06-26), background check PASSED. No change_event in the last 30 days. Read-only, nothing changed.

**Week 10-07 to 10-13** (continues the other AT user's 10-07 entry, which matched 09-30..10-06 to the cent): $372.25, 4 charged leads (3 calls, 1 message), $93.06 CPL. Prior week $430.91, 4 calls, $107.73. 648 impressions, 93.3% top / 14.1% abs top. 2 more calls Google didn't charge (10-08, 10-09).

**Budget:** calls cost ~$100 each, so one charged call ≈ 3 days of budget. Oct 1-13 = $803 of the ~$1,086 monthly limit (35.71 x 30.4), ~$283 left (≈3 calls), so LSA likely goes quiet in the second half of October. Sep: $749.91 from 09-11 to 09-24, then no impressions 09-25 to 09-30. Raising budget = client call, not changed. Monthly: Jun $358, Jul $300, Aug $292, Sep $750, Oct MTD $803.

**AT:** KPI - LSA `7e1e2f9c` (date_pulled 2026-10-14, Overspending, lead quality Good); task fields checklist (all 7) + lead_quality + notes; blocker_details overwritten with a "Resolved 10-14" line; stage complete. No comments. Added 8655979348 to `lsa_report.py`, `lsa_health_check.py` and the `contas.yaml` notes.

---

## 2026-10-14 — APPLIED: auto-apply cleanup (Edu: "Execute that of All Seasons - GO")

Ran `asac_autoapply_cleanup_1013.py --live`, read back:
- **156 auto-added BROAD keywords (10-11) → PAUSED** (all 156 confirmed PAUSED). Before the pause they spent **$29.41 total**: 1 click on 'tf o brien' (competitor, 1 conv); 'hvac installers' and 'heating and cooling installation' had impressions, $0.
- **14 auto-apply subscriptions → PAUSED**: TARGET_CPA_OPT_IN, MAXIMIZE_CONVERSIONS_OPT_IN, KEYWORD, OPTIMIZE_AD_ROTATION, RESPONSIVE_SEARCH_AD, MAXIMIZE_CLICKS_OPT_IN, TARGET_ROAS_OPT_IN, RAISE_TARGET_CPA, RESPONSIVE_SEARCH_AD_IMPROVE_AD_STRENGTH, SET_TARGET_ROAS, USE_BROAD_MATCH_KEYWORD, LOWER_TARGET_ROAS, MAXIMIZE_CONVERSION_VALUE_OPT_IN, SET_TARGET_CPA. With DISPLAY_EXPANSION_OPT_IN (10-05) that's 15 off.
- **7 still ENABLED** with a type this SDK reports as UNKNOWN (resource name `.../recommendationSubscriptions/UNKNOWN`), not mutable via API → turn off in the UI (Recommendations > Auto-apply). Command Center fu-049.
- Not touched (not part of the go): 'portable ac' pause, 'petro' negative (competitor call is Edu's).

---

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $1,285.17, 29 conv, $44.32 CPL (prior $35.89/33). 17 Click to call taps (8 PMax, all Display/YouTube), 11 call extension LEAD (≥1s), 1 form. call_view 12 calls, 5 ≥60s → ~$257 per real connected call. Nonbranded 82% budget-lost. KPI Health = Mixed.

**⚠ Auto-apply added 156 BROAD keywords on 10-11** (change_event client_type GOOGLE_ADS_RECOMMENDATIONS_SUBSCRIPTION): 153 in TSD_Search_LeadGen, 2 MiniSplit, 1 Nonbranded. Junk-heavy (furnace chimney cleaning, kerosene heaters, hvac careers, free hvac training, water-heater brands, competitor plumbers, FL/NYC businesses, Spanish terms). All ENABLED, $0 through 10-12. 21 auto-apply subscriptions still ENABLED (only DISPLAY_EXPANSION_OPT_IN paused 10-05), incl. KEYWORD, USE_BROAD_MATCH_KEYWORD and bid-strategy types.

**Staged, not applied:** `asac_autoapply_cleanup_1013.py` (this folder), validated OK: pauses the 156 keywords + 14 auto-apply subscriptions; 7 subscriptions have types this SDK reports as UNKNOWN and must be turned off in the UI (Recommendations > Auto-apply). Also: pause 'portable ac' (QS 1, $32, 0 conv); 'petro' PHRASE negative on Branded Evergreen ($52 + $12 on 'petro home services').
Still open from 10-08: heating ads disapproved, competitor block/keep.

**LSA task (363a93f3) left OPEN:** client-owned LSA, not under the MCC; blocker written in the task.
AT Google task de48b610 closed, KPI record e18ef4a9.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

---

## 2026-10-12 — Simple budget breakdown v2 (client-facing), checked against the 09-10 change

**Read-only.** Edu asked for a simple report: "detail where your budget is being spent across each platform and campaign", aligned with the 09-10 budget change.

**Deliverable:** `All-Seasons-AC-Ad-Budget-Breakdown_2026-10-12.pdf` (+ .html), 1 page, plain Times. Replaces the 10-08 version (2 tables merged into 1, adds a before/after table for the 09-10 change). Window Sep 12 → Oct 11, so all of it is after the change.

**Alignment check:** Google budgets live = $185/d exactly (70/55/24/14/13/9), unchanged since 09-10. Google spent $5,092.54 vs $5,550 allowed (92%). LSA $250/wk per the 09-14 confirmation (client-owned, spend not visible to us). Google + LSA weekly: $1,546 before vs $1,545 after.

**Meta is outside that agreement:** `TSD_10.09_Awareness_Brand_TOFU_ARL` still ACTIVE $20/d ($45.23 since 10-09) + old `TSD_09.02` $557.61 = $602.84 in the window. Not part of the 09-10 change, client asked Meta off 04-15, ticket #935 "Facebook Charges" still with Angela (fu-033). Report shows Meta as it is; if it gets paused before sending, update the Meta row.

**AT:** the request is Client Request `7a4c9a19` "Paid Ads Reporting" (Donna, 10-09). Execution on Edu, then Communicate on Angela. Not uploaded / completed yet.

**Edits after Edu reviewed it:**
1. Removed the closing line ("If you'd like to move money between platforms or campaigns, just let us know..."). Edu: never put stuff like this. Saved as a standing rule in memory (no closing offers in client reports).
2. Removed the note paragraph under the table (Google under budget vs $5,550, co-op subtotal $1,405.75, Meta 10-09 version swap, LSA in own account, ×30.4 monthly math).
Final PDF = header, intro line, section 1 (09-10 change + before/after table), section 2 (one table: platform / campaign / daily / monthly / spent 30d), ends on the "Total, all platforms" row. Still 1 page.

**AM summary for Angela (internal, sent by Edu):** "Here's where the All Seasons money goes right now. Google Ads is at $185/day (about $5,625/mo), the level we set on 9/10 to free up room for LSA. Last 30 days it spent $5,092.54: Heating & Cooling Service $70/day ($1,617.58), AC Install & Repair $55/day ($1,699.47), the 3 Mitsubishi co-op campaigns $47/day combined ($1,405.75), and Branded $13/day ($369.74). Meta is one awareness campaign at $20/day (about $608/mo), which spent $602.84. LSA is $250/week (about $1,083/mo), but that runs in the client's own account, so we can't see the actual spend. All in, that's about $7,316/mo budgeted."

**Same session, AT check on Meta approval:** Edu remembered Angela approving Meta budget as "within budget". She didn't. That approval is on the Google Branded $15/d task `99d49b0e` (08-31). The Meta task `2758649a` never reached her. Detail in meta-ads-log.md 10-12.

Scripts: `all_seasons_budget_1012.py` + `all_seasons_budget_1012_micros.py` in the Ratos scripts folder (read-only pulls).

---

## 2026-10-08 (3) — Whole-operation rating for Edu: 4/10 (PPC 4, LSA 6, Meta 3)

**LSA found:** Agency Titan client record, `kpis_lsa` (weekly entries, window not stated, assumed 7d):

| Pulled | Spend | Leads | Calls / Msgs | CPL | Quality | Top impr. |
|---|---|---|---|---|---|---|
| 09-18 | $519.56 | 8 | 3 / 5 | $64.94 | Mixed | 28.5% |
| 09-22 | $179.00 | 4 | 0 / 4 | $44.77 | Good | 94.6% |
| 09-30 | $29.55 | 1 | 1 / 0 | $29.55 | Unclear | 90% (underspending) |
| 10-07 | $430.91 | 4 | 4 / 0 | $107.73 | Good | 90.6% |
| **Total** | **$1,159.02** | **17** | **8 / 9** | **$68** | | |

Disputes, credits and booking rate never filled. AgencyAnalytics MCP (via AT) returned Unauthorized, so no daily LSA data.

**Meta 30d (Sep 8–Oct 7):** $594.97, reach 104,027, frequency 2.24 over the month, CPM $2.55, CTR 0.06%. 10-06 setup fixes (meta-ads-log) still not done.

**Rating basis:** LSA cheapest per lead (~$68 vs $116–253 per real PPC lead), but only 8 phone leads and no outcome data. PPC on budget with real Search calls, but reported leads inflated, heating dark, PMax Display taps. Meta under the TSD method's own bar. No booked-job data on any channel.

---

## 2026-10-08 (2) — Client budget breakdown report (Angela request, Google + LSA + Meta)

**Trigger:** Angela asked for a breakdown of where the ad budget is allocated and spent, per platform and campaign, incl. Meta and LSA. Client-facing.

**Deliverable:** `All-Seasons-AC-Ad-Budget-Breakdown_2026-10-08.pdf` (+ .html source) in this folder. Plain Times format (Watt's Right FB report CSS), rendered with Playwright. Budgets as of 10-08, spend Sep 8 → Oct 7.

| Platform | Daily | Monthly (×30.4) | Spent 30d |
|---|---|---|---|
| Google Ads (6 campaigns) | $185 | $5,625 | $5,560.70 |
| LSA | $250/wk | $1,083 | not visible to us |
| Meta (TSD_09.02_Awareness_Brand_TOFU) | $20 | $608 | $594.97 |

Mitsubishi co-op subtotal (MiniSplit + PMax + Mitsubishi-Brand): $47/d, $1,430/mo, $1,487.63 spent. Meta hiring campaign `TSD_03.12_Leads_Forms_Hiring` still shows ACTIVE but spent $0 in the window (lifetime budgets used up), left out of the report.

**LSA:** no LSA campaign in `4467722415` and no All Seasons LSA account under the TSD MCC. LSA is client-owned. Report shows the $250/week planned on 09-10/09-14 and points the client to their LSA dashboard for actual charges. If the AM can get the real LSA spend, swap it into table 1.

Report leaves out lead quality, Display, heating disapprovals (internal only, see entry below).

---

## 2026-10-08 — Mid-week check: Display fix held, PMax now Display taps, heating ad groups dark, real calls falling

**No account changes.** Read-only check, Edu asked "check All Seasons PPC".

**Last 7 days (10-01 → 10-07), PPC only:** $1,366.97 spend, 290 clicks, $4.71 CPC, 33 conv, $41.42 CPL, 10.7% conv rate, Search IS <10%. Branded (Branded Evergreen only, per the 09-15 rule) 2 conv / $48.41; unbranded 31 / $40.97.

| Campaign | Spend | Clicks | Conv | CPL | Search IS | Lost budget | Lost rank |
|---|---|---|---|---|---|---|---|
| TSD_Search_LeadGen | $501.09 | 42 | 8 | $63 | 24% | 19% | 57% |
| TSD_04.29_Search_Nonbranded_Evergreen | $429.76 | 31 | 8 | $54 | <10% | 84% | 12% |
| TSD_07.01_Lead_Search_MiniSplit-General | $180.77 | 9 | 5 | $36 | <10% | 63% | 27% |
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | $98.82 | 149 | 10 | $10 | n/a | | |
| TSD_08.31_Search_Branded_Evergreen | $96.82 | 43 | 2 | $48 | <10% | 19% | 77% |
| TSD_07.01_Lead_Search_Mitsubishi-Brand | $59.71 | 16 | 0 | n/a | 19% | 19% | 62% |

**Found:**
1. **Display fix held.** Last Display spend on Branded Evergreen / Mitsubishi-Brand was 10-05 (fix day, $5.43 / $2.03). $0 since 10-06. Closes the 10-05 open item.
2. **Conversion mix:** 22 `Click to call` (taps), 11 `call extension LEAD` (calls), 0 forms. Form last fired 09-29 and runs ~1/week, so not alarming yet. On Search, taps run ~1:1 with calls (LeadGen 4/4, Nonbranded 4/4, MiniSplit 2/3), consistent with one caller counting twice (tap + call).
3. **Real calls from ads are falling** (`call extension LEAD`, Mon–Sun weeks):

| Week | Spend | Search clicks | Calls | $ / call |
|---|---|---|---|---|
| 08-31 | $1,464 | 108 | 20 | $73 |
| 09-07 | $1,479 | 115 | 16 | $92 |
| 09-14 | $1,311 | 96 | 18 | $73 |
| 09-21 | $1,111 | 83 | 11 | $101 |
| 09-28 | $1,099 | 82 | 9 | $122 |

4. **PMax switched from YouTube to Display on 10-01.** Before: ~$15/day YouTube, $0 Display. Since 10-01: Display $7–19/day, YouTube ~$1. All 10 PMax conv this week are `Click to call` on Display, so ~30% of the account's reported conversions are Display taps. PMax is one of the 3 Mitsubishi co-op campaigns (plan through Dec), so pausing is not a simple call.
5. **Heating ad groups are dark going into heating season.** LeadGen `furnace repair` + `heating repair`: 0 impressions in 30 days. Their 6 ads (STALE_DISAPPROVAL) all use final URL `seasonsair.com/heating-repairs/`, which now redirects to `seasonsair.com/services/residential-heating/heater-repair/` (~5s load). 6 more disapproved ads with the same URL sit in paused ad groups (ignore). Heating demand only reaches us through `residential hvac` broad terms ("home heating service" 80 impr / 6 clicks / $101 in 14d).
6. **Branded Evergreen leak source found** (10-05 open item): its brand keywords are BROAD. `all seasons hvac` BROAD and `all seasons air conditioning` BROAD matched "petro home services" / "petro long island": $73.89 / 10 clicks / 1 conv in 30d.
7. Spend ran $229–287/day 10-05 → 10-07 vs $185/day budget (Google daily overdelivery once Display money moved into Search). 7-day total $1,367 vs $1,295 budget; inside the monthly cap.
8. Only non-TSD change activity since 10-05: ClickCease rotating IP exclusions on the 5 Search campaigns several times a day (normal).

**Search terms:** competitor names still carry most spend and still convert (gallettair, haviland hvac, slomin's, tf o brien, burke energy). Small junk: "407c freon" $10.01, "fujitsu website" $3.46.

**Recommended (not applied, Edu's call):**
- [ ] Repoint the 6 heating ads to the live heater-repair URL (forces re-review), or appeal in the UI.
- [ ] Branded Evergreen: move brand keywords to phrase/exact, or add "petro" as a negative there.
- [ ] `Click to call` → secondary (at least for PMax) so bidding chases calls/forms; report calls + forms as leads.
- [ ] Negatives: "407c freon", "fujitsu website".

### Lead types, last 30 days (09-08 → 10-07), Edu follow-up "what types of leads are we getting"

$5,560.70 spend, 137 reported conversions ($40.59 each): 71 `Click to call` taps, 61 `call extension LEAD`, 5 forms.

- **`call extension LEAD` counts any call of 1 second or more** (`phone_call_duration_seconds = 1`; Google default is 60). That's why "calls" looked healthy.
- **call_view: 70 tracked calls, 3 missed, median 33s.** <15s: 11 · 15–29s: 16 · 30–59s: 26 · 1–2 min: 7 · 2+ min: 10. **17 calls over a minute** (LeadGen 8, MiniSplit 6, Nonbranded 3) = ~$327 per 60s+ call. All tracked calls come from those 3 Search campaigns.
- **Taps:** 35 from PMax, 0 tracked calls from PMax in call_view (same call asset (631) 212-8021 as Search; no ad_group fields in the query, so not the Napps PMax-drop gotcha). Caveat: Google can't always forward Display/YouTube calls, so this doesn't prove zero, but nothing confirms any. 14 taps from Branded Evergreen, which has **no call asset attached** (only campaign without one), so its taps can't be tracked as calls at all.
- **Callers:** 516 = 25, 631 = 11 (36 of 70 Long Island), NYC cell codes 14, hidden 11, other 9 (FL/VA/AL/CT/NJ/Westchester/Hudson Valley). Weekdays (Mon+Tue = 36), 7am–5pm, peak 9–10am, none after 5pm.
- **Forms:** 7 in 60d, almost all from brand searches (Branded Evergreen 3, Mitsubishi-Brand 2, LeadGen 1, Nonbranded 1).
- **Converting search terms are almost never generic service searches.** They are competitor names (petro home services = 10 call conv, mostly via MiniSplit broad; gallettair 4; tf o brien, haviland, a1, accutemp, five star, cornetta, burke, slomin's, pseg), the All Seasons name, supply houses (ferguson, johnstone, hydronic supply) and manufacturer/support lookups (york tech support, honeywell thermostat, carrier plainview). Only ~half of conversions are visible at search-term level.
- **Correction to 10-05:** "competitor and supply-house searches convert" rested on the 1-second call threshold. A caller looking for Petro or Ferguson counts as a lead after 1 second. Not proven either way until call length per term or GHL outcomes are checked.

**Recommended (not applied):**
- [ ] Raise `call extension LEAD` threshold 1s → 60s (changes what Max Conversions bids toward, so expect a volume drop on paper).
- [ ] Attach the (631) 212-8021 call asset to Branded Evergreen.
- [ ] GHL/call-recording check on a sample of competitor-term and PMax leads (PMax one open since 08-04).

---

## 2026-10-05 — Weekly 7-day optimization (Agency Titan task): Display off again, help-line negatives, Display auto-apply paused

**Authority:** Edu, in chat ("Do the changes on All Seasons"). No budget, bid strategy or conversion-setting changes.

**Last 7 days (09-28 → 10-04), PPC only:**

| Campaign | Spend | Clicks | Conv | CPL | Search IS | Lost to budget |
|---|---|---|---|---|---|---|
| TSD_Search_LeadGen | $421.04 | 29 | 10 | $42 | 22% | 22% |
| TSD_04.29_Search_Nonbranded_Evergreen | $278.18 | 26 | 4 | $70 | <10% | 83% |
| TSD_07.01_Lead_Search_MiniSplit-General | $152.34 | 7 | 4 | $38 | 12% | 58% |
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | $95.39 | 280 | 6 | $16 | n/a | n/a |
| TSD_08.31_Search_Branded_Evergreen | $91.58 | 71 | 4 | $23 | <10% | 1% (90% rank) |
| TSD_07.01_Lead_Search_Mitsubishi-Brand | $68.47 | 26 | 1 | $68 | 15% | 36% |
| **Total** | **$1,107.00** | | **29** | **$38** | | |

Prior week: $1,110.71, 21 conv, $53 CPL. All conversions are `call extension LEAD`, `Click to call` and `[TSD] Lead Form` (2 forms). PMax: 71% of its spend went to YouTube.

**Found:**
1. **Display was ON again** on 3 Search campaigns (fixed 08-31): MiniSplit-General, Branded Evergreen, Mitsubishi-Brand. Display this week: Branded $49.11 / 57 clicks / 1 conv (54% of its spend), Mitsubishi-Brand $30.27 / 18 clicks / 0 conv (44%), MiniSplit $0. `change_event` (30d) shows no network edit, so it flipped before 09-06 or via Google automation. Auto-apply `DISPLAY_EXPANSION_OPT_IN` was ENABLED, one of 22 enabled auto-apply types (auto-apply also edited MiniSplit's target ROAS on 09-14 and added ad-group negatives to LeadGen on 10-03).
2. **Heating ads can't serve.** All 6 ads in LeadGen's `furnace repair` and `heating repair` ad groups are DISAPPROVED with topic `STALE_DISAPPROVAL` (old disapproval, never re-reviewed). Both heating ad groups have 0 approved ads going into heating season.
3. **Search terms:** competitor names convert in this account (gallettair inc, a1 air conditioning, petro home services, pseg home service, slomin's, burke energy), so none were blocked. Supply-house searches also converted (hydronic supply copiague, johnstone supply farmingdale), so "supply" was NOT negated. Visible junk was manufacturer help lines ("lennox air conditioner phone number", "mitsubishi air conditioner customer service").
4. Branded Evergreen picks up non-brand searches ("petro home services" $11.33, "hvac in new york" $8.15), which explains its <10% IS with 90% lost to rank.

**Changed** (script `asac_apply_1005.py` in this folder; every change read back from the account):

| Change | Before | After |
|---|---|---|
| Display network: MiniSplit-General `24050402045`, Branded Evergreen `24202454875`, Mitsubishi-Brand `24050401592` | ON | **OFF** (Search Partners already off) |
| PHRASE negatives "customer service", "phone number" on Nonbranded Evergreen `23813282398`, MiniSplit `24050402045`, Mitsubishi-Brand `24050401592` (criteria `~13863971`, `~12958870`) | none | **added** |
| Auto-apply `DISPLAY_EXPANSION_OPT_IN` | ENABLED | **PAUSED** (10-05 15:31) |

Negatives not added to LeadGen (still holds a brand ad group) or Branded. Replayed against 30d search terms, they would have blocked 5 clicks / $76.58 / 0 conversions, and no active keyword. The other 21 auto-apply types are untouched.

**Open:**
- [ ] Appeal the 6 stale-disapproved heating ads in LeadGen (UI: Ads, filter Disapproved, Appeal) or recreate them.
- [ ] Decide on the remaining auto-apply types (incl. USE_BROAD_MATCH_KEYWORD, RAISE_TARGET_CPA, SET_TARGET_ROAS, KEYWORD).
- [ ] Nonbranded Evergreen loses 83% IS to budget at $70 CPL while LeadGen runs $42 CPL: reallocation call (constant total, no ticket needed).
- [ ] Branded Evergreen: find which keywords let non-brand searches in.
- [ ] Competitor terms convert here: block or keep is still Edu's call.
- [ ] Next week: confirm Display spend is $0 on all Search campaigns.

---

## 2026-09-09 — Conversion type breakdown, last 7 days

**Trigger:** Edu asked to check the last 7 days and report what types of conversions came in and how many of each.

### Breakdown

| Action | Category | Count |
|---|---|---|
| Click to call | CLICK_TO_CALL | 22.0 |
| call extension LEAD | PHONE_CALL_LEAD (AD_CALL) | 19.0 |
| [TSD] Lead Form | SUBMIT_LEAD_FORM | 3.0 |
| **Total** | | **43.99** (matches account-level `conversions`, cross-checked) |

Cost over the period: $1,620.13, blended CPL ~$36.83. Mix is still almost all phone (41 of 44, ~93%), form-fills thin at 3 — consistent with the 50/50 call-type split and 1-3% form-fill share noted in the 2026-09-08 entry above.

## 2026-09-08 — Full performance review (7/14/30d + since last change), lead-type breakdown, GA4 cross-check, budget ask drafted — REQUESTED, PENDING APPROVAL

**Trigger:** Edu asked for a results breakdown across 7d/14d/30d plus results since whatever the last significant change was, then a series of follow-ups: what conversion types make up "leads," CPL per type, whether GA4 could cross-check that, an overall performance read, and finally whether to ask for more budget. Pure analysis/reporting session — no account mutations made.

### Performance snapshot

| | Last 7d | Last 14d | Last 30d |
|---|---|---|---|
| Spend | $1,545.84 | $2,797.60 | $5,878.23 |
| Clicks | 321 | 971 | 1,643 |
| Leads | 41.0 | 78.0 | 173.0 |
| CPL | $37.71 | $35.87 | $33.98 |
| CPC | $4.82 | $2.88 | $3.58 |
| CTR | 2.52% | 2.93% | 2.94% |
| Search IS | 12.19% | 12.62% | 13.13% |
| Conv. rate | 12.77% | 7.81% | 10.35% |

**Last significant change identified as 2026-08-31** (the bundled day: Display-network leak fix on all 4 Search campaigns, LeadGen geo-targeting fix, budget-neutral reallocation, 59 legacy ETAs paused, new Branded campaign launched). Before/after, 8 days each side:

| | Before (Aug 23–30) | After (Aug 31–Sep 7) | Δ |
|---|---|---|---|
| Spend | $1,422.15 | $1,693.53 | +19% |
| Clicks | 695 | 351 | −49% |
| Leads | 43.0 | 45.0 | +2 |
| CPL | $33.07 | $37.64 | +14% |
| CPC | $2.05 | $4.82 | +135% |
| Conv. rate | 5.96% | 12.78% | +6.8pt |
| Search IS | 14.03% | 11.62% | −2.4pt |

Read: fewer, pricier, far more relevant clicks post-fix (conv. rate more than doubled, lead volume held flat on half the clicks) — consistent with cutting a Display leak that was buying cheap junk clicks. Nominal CPL rose rather than fell short-term; too early (8 days, several bundled changes) to call that a clean win or a problem — re-check in another 1-2 weeks.

### Lead-type breakdown

Only 3 conversion actions are currently live and counting:

| Action | Type | What it is |
|---|---|---|
| call extension LEAD | `AD_CALL` | Real connected phone call via the ad's call-forwarding number, past Google's duration threshold — the strong signal |
| Click to call | `CLICK_TO_CALL` | Tap on the call button/number in the ad — counted instantly, no connect/duration requirement — soft signal |
| [TSD] Lead Form | `WEBPAGE` | Real website form submission — genuine form-fill lead |

Mix: roughly 50/50 Click-to-call vs. call extension LEAD, form-fills only 1-3% of volume (7d: 20/20/1 of 41; 14d: 40/36/2 of 78; since Aug 31: 23/21/1 of 45). 30-day figure also includes now-dead legacy GA4-imported actions (`phone_link_click` 26, `book_now_link_click` 4) that don't appear at all in the shorter windows — confirms the 2026-08-13 GA4-disconnect ([[gtm-log.md]]) held and future counts are on clean native tracking only. `page_view` still sits misconfigured as a GA4 key event (0 in "conversions," 287.75 in `all_conversions` over 30d) — dormant, not distorting CPL, still not cleaned up (open since 2026-08-04).

### Per-type CPL — genuine API wall, not a script gap

Tested directly: GAQL rejects combining `metrics.cost_micros` or `metrics.cost_per_conversion` with `segments.conversion_action_name` (`PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE`) — cost lives on the click, not the conversion event, so Google doesn't expose a real split. Tried allocating each campaign's cost proportionally across its action mix as a workaround — proved circular: within any campaign it just reproduces that campaign's blended CPL for every action type (mathematically forced, no new signal). Only place a real number exists: PMax Mitsubishi-Ductless runs 100% Click-to-call, so its campaign CPL (**$21.95**, since Aug 31) is a genuine, isolated Click-to-call CPL for that campaign. Everywhere else remains blended.

### GA4 cross-check

Checked whether GA4 could supply the cost split Ads can't. `advertiserAdCost` by campaign came back $0 everywhere and no real Ads campaign names surfaced in `sessionCampaignName`. Queried the GA4 Admin API directly (`properties/312966741/googleAdsLinks`) — **came back completely empty: there is no Google Ads link on this GA4 property at all.** No cost data exists in GA4 to cross-check against. Likely (not confirmed) a side effect of the 08-13 GA4-disconnect action removing the same link object that also carried cost import — worth deciding later whether to relink for cost-only without resurrecting the conversion-import junk.

GA4 does still auto-classify gclid-tagged sessions as `google / cpc` independent of that link, so pulled real on-site behavior for that segment as a volume cross-check (not cost):

| Window | Ads-reported phone-related conv. | GA4 `phone_link_click` (google/cpc) | Ads Lead Form | GA4 `submit_lead_form` (google/cpc) |
|---|---|---|---|---|
| Since Aug 31 (8d) | 44 | 26 | 1 | 0 |
| Last 14d | 76 | 41 | 2 | 1 (+1 `lead`) |
| Last 30d | 141 | 124 | 2 | 5 |

Gap is expected, not a red flag — Ads' call-extension clicks often dial straight from the ad/SERP without ever loading the site, so GA4 structurally can't see all of them. Volumes are the same order of magnitude — no evidence Ads is fabricating call volume. Minor note: at 30d GA4 shows *more* real form submits (5) than Ads counted as Lead Form conversions (2) — if anything hints Ads may be slightly undercounting forms, not overcounting; sample still thin, not conclusive, worth another look with more volume.

Computed as an alternative, non-circular blended figure: cost per GA4-confirmed on-site phone click = $47.40 (30d), $68.23 (14d), $65.13 (since Aug 31) — legitimate since it's spend against one independent behavioral metric, not an attempt to split cost across competing types. Cost per GA4-confirmed form submit ≈ $1,175.65 (30d, n=5 — too small to lean on).

### Overall performance read (given to Edu)

Mid-turnaround, trending the right way, not yet healthy: core constraint is visibility (12-13% Search IS across every window, ~87% of eligible auctions missed); the 08-31 Display-leak fix traded volume for quality but nominal CPL hasn't shown the expected improvement yet (too early to call); ~50% of "leads" are soft click-to-call taps not verified calls, PMax's leads are still 100% click-based with the GHL/CRM verification gap open since 08-04 (now >1 month); tracking hygiene is real and improved (GA4 junk cut, Display leak plugged, geo bug fixed, 59 dead ETAs paused); new Branded campaign is a clean early win. Priority next: PMax lead-quality verification, Mitsubishi-Brand QS/rank fix, LeadGen ad-group consolidation — bigger levers than more spend for 3 of 6 campaigns.

### Fresh budget-lost vs. rank-lost IS pull → grounded the budget ask

Pulled current (not pre-08-31-fix) per-campaign IS-loss split to check whether more budget would actually help:

| Campaign | Budget | Budget-lost IS | Rank-lost IS | Read |
|---|---|---|---|---|
| Nonbranded Evergreen | $63/d | 51-58% | 30-37% | Still genuinely starved even after the 08-31 bump |
| Branded Evergreen (new) | $15/d | ~60% | 36% | Budget-capped, converting very well |
| LeadGen | $80/d | 25-29% | 53-56% | Now mostly rank-capped, not budget |
| MiniSplit-General | $27/d | 21-26% | 68-73% | Flipped to rank-capped after its own bump |
| PMax Mitsubishi-Ductless | $16/d | 0% | 90% | Entirely rank-capped |
| Mitsubishi-Brand | $10/d | 42-44% | 35-38% | 0 conversions this week, known QS 1-3 issue — not a scaling candidate |

Checked Google's `campaign_simulation` resource for a data-driven sizing — returned empty, no simulation data available for this account currently, so sizing below is a reasoned test figure, not an optimizer output.

### Budget ask — REQUESTED, PENDING APPROVAL

Recommended and Edu has requested **~$900/month net-new (~$30/day)**, on top of the current $211/day (~$6,330/month) total — bringing the account to ~$7,200-7,250/month all-in. Targeted specifically at the two currently budget-capped campaigns: Nonbranded Evergreen ($63→~$80/d) and Branded Evergreen ($15→~$25/d). Framed as a test-and-reassess move, not a permanent commitment. **Not yet executed — per house budget doctrine (client/AM-ticket approval required before Paid moves on it), this is currently sitting with the client/AM awaiting written approval.**

### Open / next steps
- [ ] Follow up on approval status for the ~$900/mo budget ask; once approved, apply via `update.py` and verify live before communicating as active
- [ ] Re-check budget-lost/rank-lost IS 1-2 weeks after the increase actually goes live
- [ ] Re-check nominal CPL trend post-08-31 fixes now that more time has passed (too early to call as of this session)
- [ ] Resolve PMax lead-quality question via GHL/CRM cross-check — open since 2026-08-04, still blocking any scale decision on that campaign
- [ ] Discuss + execute LeadGen ad-group consolidation and Mitsubishi-Brand RSA rewrite (both free, rank-capped fixes, still open from 2026-08-31 (4))
- [ ] Decide whether to relink Google Ads↔GA4 for cost-data import without resurrecting the conversion-import junk the 08-13 disconnect was fixing

---

## 2026-08-31 (5) — New dedicated Branded campaign built (staged, PAUSED — not live)

**Trigger:** Edu asked what to do about branded traffic — found it was living inside LeadGen's "All Seasons AC (BRAND)" ad group rather than its own campaign.

**Investigation:** The account already had a dormant paused legacy campaign "All Seasons AC Branded" (`9609583334`, $8/d) — decided not to revive it: most of its keywords are PAUSED/REMOVED, it still has deprecated broad-match-modifier syntax (`+all +seasons +air`), and one ad group has an unrelated keyword ("all weather ac") that isn't even brand intent. Cleaner to build fresh.

Current brand performance (inside LeadGen, 30d): "all seasons air conditioning" (Broad, QS 10, 230 impr/30 clicks/7.7 conv/$247.05) and "all seasons hvac" (Broad, QS 10, 29 impr/5 clicks/3.0 conv/$99.43) are essentially 100% of the real activity — both perfect QS, no rank problem at all. Several close variants were sitting PAUSED with zero impressions (never actually tested), and "best ac" (a generic, non-branded term) had leaked into the brand ad group by mistake.

**Built same day** (all creates via `create.py`, everything starts PAUSED by design):
- Campaign `TSD_08.31_Search_Branded_Evergreen` (ID `24202454875`) — SEARCH, Google-Search-only (no partners/display), Maximize Conversions, $15/day (sized to comfortably cover current ~$11.50/day actual brand spend).
- Geo: same 3 locations as the rest of the account (Suffolk County, West Babylon, Nassau County).
- Ad group "Brand Core" (ID `196705043461`) with 12 keywords: the 2 proven winners + phrase variants, plus 4 untested-but-plausible variants (all seasons air / heating / maintenance / ny) that never got a real chance before. Dropped "best ac."
- 1 RSA: homepage URL (`seasonsair.com/`, Edu's call over the generic `/ac-installations/` page it was using before) with trust/recognition-angled copy for people who already know the name (reviews/licensed-insured/local framing) instead of the generic "call now" urgency copy reused from LeadGen.

**Blocked mid-build**: `create.py campaign` was denied by the Claude Code auto-mode permission classifier (a different, more consequential category than the update/pause/reallocate mutations run earlier — a Bash settings.local.json allow-rule did NOT fix it, confirmed by testing). Edu switched the session from Auto to Default permission mode, approved the prompt, and the rest of the build (geo, ad group, keywords, RSA) went through cleanly afterward.

**Activated same day.** Edu made the call to go live now and handle the client/AM written-approval ticket himself in parallel, rather than gate the technical activation on it — his call as the account owner. Flipped campaign, ad group ("Brand Core"), and the RSA to ENABLED via `update.py` (keywords were already ENABLED at the criterion level, just dormant under the paused parent). Verified live via read-back: campaign ENABLED, ad group ENABLED, all 12 keywords ENABLED, RSA ENABLED (ad_strength still PENDING — normal, not yet calculated).

**Cleanup done immediately after activation** to stop the new campaign from competing with itself against the old brand traffic still live in LeadGen:
- Paused LeadGen's old "All Seasons AC (BRAND)" ad group (`130559857567`).
- Added `all seasons` (PHRASE) as a campaign-level negative on LeadGen (`11803942938`) — blocks any LeadGen keyword (including the now-paused brand ones) from matching a brand query going forward.

Old dormant campaign `9609583334` left untouched (not worth cleaning up a campaign we're not using).

### Open / next steps
- [x] AM ticket sent 2026-08-31, informing $15/d net-new spend (campaign was already live at time of sending).
- [ ] Watch the new campaign's first week: conversions, CPL, and whether ad_strength settles above AVERAGE once Google finishes calculating it.
- [ ] Confirm no brand-query volume is leaking to LeadGen post-negative (spot check ad_network/search-terms next check-in).

---

## 2026-08-31 (4) — Rank-capped bucket started: paused 59 legacy Expanded Text Ads in LeadGen

**Trigger:** Edu split the rank-capped work into ad cleanup (this), ad-group consolidation, and Mitsubishi-Brand ad copy — asked to do the ad cleanup first, then discuss the other two.

**Diagnosis:** Pulled keyword-level QS sub-components (`creative_quality_score`, `post_click_quality_score`, `search_predicted_ctr`) for LeadGen and Mitsubishi-Brand. Two findings:
- LeadGen has ~24 overlapping ad groups (hvac contractor / hvac contractor #2 / commercial hvac / industrial hvac / hvac company are largely the same intent), and most keywords show no QS at all — too little volume per node for Google to score. Ad-group consolidation is next (not yet done, needs a decision session with Edu).
- LeadGen had 59 legacy `EXPANDED_TEXT_AD` (format Google stopped allowing new creation/edits of in mid-2022) still ENABLED alongside 42 `RESPONSIVE_SEARCH_AD` in the same ad groups — dead weight diluting average ad quality in the rotation. Every affected ad group already had an EXCELLENT/GOOD-rated RSA live, so no ad group loses coverage.

**Fixed same day:** paused all 59 ETAs via `AdGroupAdOperation`, verified live via read-back. Left the 1 `EXPANDED_DYNAMIC_SEARCH_AD` untouched (different format, real traffic — 1022 impr/30 clicks/$243.57 over 30d — not part of this finding). Script: `clients/all-seasons-ac/pause_legacy_etas_leadgen.py`.

Verified: LeadGen ad type × status — EXPANDED_DYNAMIC_SEARCH_AD ENABLED ×1, EXPANDED_TEXT_AD PAUSED ×68 (59 just paused + 9 already paused), RESPONSIVE_SEARCH_AD ENABLED ×42 / PAUSED ×13.

Also found: landing pages are topically well-matched to their ad groups already (heating-repair keywords → `/heating-repairs/`, etc.), but `post_click_quality_score` (landing page experience) scores BELOW_AVERAGE almost everywhere except branded queries hitting the same pages ("all seasons air conditioning"/"all seasons hvac" both hit QS 10). Points at page-level UX/speed rather than topic mismatch — a PageSpeed/Core Web Vitals check on seasonsair.com is still open, not done this session.

Mitsubishi-Brand diagnosis (not yet fixed, discussion pending): all 3 ad groups (Core/+Installation/+Location) reuse one identical RSA verbatim, AVERAGE ad strength. "mitsubishi electric hvac" and "mitsubishi electric mini split" score BELOW_AVERAGE ad relevance specifically — neither headline contains "electric."

### Open / next steps
- [ ] Discuss + execute LeadGen ad-group consolidation (merge overlapping intent groups to concentrate QS signal).
- [ ] Discuss + write distinct RSA copy per Mitsubishi-Brand ad group, working in "electric" phrasing.
- [ ] PageSpeed/Core Web Vitals check on seasonsair.com to explain the landing-page-experience gap.

---

## 2026-08-31 (3) — Budget-neutral reallocation: Mitsubishi-Brand → Nonbranded Evergreen + MiniSplit-General

**Trigger:** Edu asked to split the impression-share-loss findings from the prior entry into "budget-capped" vs. "rank-capped" buckets and work budget-capped first, keeping total account budget unchanged — just reallocate.

**Analysis:** Cross-checked each campaign's budget-lost IS against actual avg daily spend vs. nominal budget (LAST_7_DAYS):

| Campaign | Budget | Avg daily spend | Budget-lost IS | Read |
|---|---|---|---|---|
| Nonbranded Evergreen | $60/d | $57.01/d (95%) | 57.9% | Genuinely starved |
| MiniSplit-General | $24/d | $22.50/d (94%) | 46.7% | Genuinely starved |
| PMax Mitsubishi-Ductless | $16/d | $18.38/d (115%) | 39.7% | Starved too, but held — leads still unverified Click-to-call |
| Mitsubishi-Brand | $16/d | $14.92/d (93%) | 2.4% | Not budget-capped — its problem is QS/rank (separate bucket) |
| LeadGen | $80/d | $85.93/d (107%) | 15.8% | Mostly rank-capped, but footprint just changed from the geo fix — held for fresh data |

Only Mitsubishi-Brand was genuinely over-provisioned relative to what it can spend (its ceiling is Ad Rank, not budget), making it the one clean donor. LeadGen and PMax were deliberately left untouched — LeadGen because this week's numbers predate enough data since the geo fix, PMax because its conversions aren't verified real leads yet.

**Applied same day** via `update.py campaign --budget` (all mutations, verified live via `read.py campaigns` read-back):

| Campaign | Before | After |
|---|---|---|
| Mitsubishi-Brand | $16/d | **$10/d** |
| Nonbranded Evergreen | $60/d | **$63/d** |
| MiniSplit-General | $24/d | **$27/d** |
| PMax Mitsubishi-Ductless | $16/d | $16/d (unchanged) |
| LeadGen | $80/d | $80/d (unchanged) |

Total account budget unchanged at $196/day. Edu clarified TSD's budget-approval doctrine only gates a *change in the total figure* — reallocation among campaigns at a constant total doesn't need separate client/AM-ticket approval, so this was executed directly.

### Open / next steps
- [ ] Watch Nonbranded Evergreen and MiniSplit-General's budget-lost IS next week — should drop meaningfully now that they have more room.
- [ ] Re-pull LeadGen's budget-lost/rank-lost IS after a few days on the corrected geo targeting before deciding whether it has spare budget to donate too.
- [ ] Resolve PMax lead-quality question (GHL/CRM cross-check) before considering giving it more budget.
- [ ] Rank-capped bucket (Mitsubishi-Brand QS 1-3, LeadGen's remaining 62%+ rank loss) still open — separate work session per Edu's split.

---

## 2026-08-31 (2) — LeadGen geo-targeting bug found and fixed: 22 wrong countries + Queens

**Trigger:** Edu asked for improvement opportunities after the weekly check below; found this while diagnosing why `TSD_Search_LeadGen` had the account's worst rank-lost IS (62.4%, vs. 2.4–50% on the other 4 campaigns).

**Found:** LeadGen's location targeting had the account's correct service area (Suffolk County, West Babylon, Nassau County — Long Island NY, same set used by PMax, Mitsubishi-Brand, and MiniSplit-General) PLUS 22 unrelated countries (Andorra, Argentina, Bolivia, Belize, Chile, Colombia, Costa Rica, Dominican Republic, Ecuador, El Salvador, Equatorial Guinea, Gibraltar, Guatemala, Honduras, Mexico, Nicaragua, Panama, Paraguay, Peru, Puerto Rico, Uruguay, Venezuela) PLUS Queens — none of which any other campaign in the account targets. Likely a leftover from a location-list copy/paste error. Plausible explanation for LeadGen's outlier rank-lost IS and for why its Click-to-call CPL ($200.50) ran 3.5x its call-extension-LEAD CPL ($56.37) — soft engagement from irrelevant markets, not real Long Island intent.

**Fixed same day:** removed the 22 country criteria + Queens via `CampaignCriterionOperation.remove` (23 ops), left the 3 correct location criteria untouched, verified live via read-back. Script: `clients/all-seasons-ac/fix_leadgen_geo_targeting.py`.

Verified: only `geoTargetConstants/1023413` (Suffolk County), `1023474` (West Babylon), `9058760` (Nassau County) remain on LeadGen.

### Other improvement opportunities surfaced same session (not yet actioned — Edu said come back to these)
- Nonbranded Evergreen is genuinely budget-capped (57.9% budget-lost IS) — candidate to raise its $60/d budget, more so now the Display leak is fixed.
- Mitsubishi-Brand keywords sit at Quality Score 1–3 (manufacturer-brand terms, high competition) — its 71.3% rank-lost IS is a QS/landing-page problem, not budget.
- PMax Mitsubishi-Ductless has the cheapest nominal CPL ($10.72) but its conversions are still 100% "Click to call" (soft engagement) — same caution as the 2026-08-04 finding, don't scale budget until verified against GHL/CRM.
- Conversion action values are inconsistent and likely skewing the 2 campaigns on Maximize Conversion Value bidding (LeadGen, MiniSplit-General): `call extension LEAD`/`Phone Call` = $100, `Submit lead form` = $80, `[TSD] Lead Form` = $0, `Click to call` = $1.
- 3 GA4-import conversion actions (`phone_link_click`, `book_now_link_click`, `mailto_link_click`) are still ENABLED and `primary_for_goal: true` even though GA4 was disconnected as a data source 2026-08-13 — dormant landmine if GA4 ever gets reconnected. Candidate for deletion now that GHL server-side is the real tracking source.
- 2 duplicate $0-value call-tracking actions ("Calls from Smart Campaign Ads," "Calls from Ads New") not firing — safe cleanup.
- 18 paused legacy campaigns still sitting in the account — no cost, just clutter.

Also found in `contas.yaml` this session (not fixed, flagged to Edu): the "Cool Hand Electric" entry has two `customer_id`/`notas` keys in one YAML mapping — looks like the "All Heart Heating and Cooling" `- nome:` line got dropped, merging the two clients. Duplicate YAML keys silently resolve to the last value, so "Cool Hand Electric" currently resolves to All Heart's customer_id.

---

## 2026-08-31 — Weekly check + Display network leak fixed on all 4 Search campaigns

**Trigger:** Edu asked for a routine check on the account.

### 7-day snapshot (LAST_7_DAYS)
Spend $1,391.17, 669 clicks, 42 leads, 6.03% conv rate, $2.08 CPC, $33.12 blended CPL, 14.1% total Search IS. Branded (Mitsubishi-Brand): $104.45 / 1 lead / $104.45 CPL. Nonbranded Search (LeadGen + Nonbranded Evergreen + MiniSplit-General): $1,158.03 / 29 leads / $39.93 CPL. PMax (Mitsubishi-Ductless): $128.69 / 12 leads / $10.72 CPL.

**Tracking trust check — clean.** Conversion-action breakdown shows only `call extension LEAD`, `Click to call`, and `[TSD] Lead Form` — no `page_view` or `book_now_link_click` junk. Confirms the 08-11/08-13 GA4-disconnect + native tag fix ([[gtm-log.md]]) held.

**Display network leak found and fixed.** Per the systemic `create.py` bug already found across the TSD book on 2026-08-24 ([[tsd-weekly-ppc-snapshot]]), All Seasons AC was flagged then but never corrected. Confirmed via 7-day network breakdown:
- `TSD_04.29_Search_Nonbranded_Evergreen`: $131.93 of $399 spend (33%) on Display vs $267.11 on real Search — Display conversions were muddying the campaign's true CPL.
- `TSD_07.01_Lead_Search_Mitsubishi-Brand`: $68.68 of $104.45 spend (66%) on Display with **zero** conversions, vs $35.77 on real Search that produced the campaign's only lead — true branded CPL is ~$35.77, not $104.45.
- `TSD_Search_LeadGen` and `TSD_07.01_Lead_Search_MiniSplit-General` also had Display on but with negligible/no leak.

Search Partners (`target_search_network`) was already `False` on all 4. Fixed same day: mutated `network_settings.target_content_network` to `False` on all 4 enabled Search campaigns, verified live via read-back (not just the mutation's success response). Script: `clients/all-seasons-ac/fix_search_network.py`.

Verified: TSD_Search_LeadGen | target_search_network = False | target_content_network = False
Verified: TSD_04.29_Search_Nonbranded_Evergreen | target_search_network = False | target_content_network = False
Verified: TSD_07.01_Lead_Search_Mitsubishi-Brand | target_search_network = False | target_content_network = False
Verified: TSD_07.01_Lead_Search_MiniSplit-General | target_search_network = False | target_content_network = False

### Open / next steps
- [ ] Watch next week's snapshot to confirm Nonbranded Evergreen's and Mitsubishi-Brand's CPL improve now that Display is off.
- [ ] Confirm whether the new `awct` Lead/Phone Click GTM tags (drafted 2026-08-13, not published as of that log entry) ever got published — current conversion actions look clean regardless, but worth closing the loop.

---

## ⚡ Quick access (read this first — don't re-discover the account)

- **Customer ID (no hyphens):** `4467722415`
- **MCC / login-customer-id:** `4155514468` (Topservdigital)
- **GA4 property ID:** `312966741`
- **Skill:** `google-ads-ratos` — scripts at `~/.claude/skills/google-ads-ratos/scripts/`, run via `./scripts/tsd.sh <script>` to use the TopServ profile

**Ready-to-run commands** (from `~/.claude/skills/google-ads-ratos/scripts/`):
```bash
./tsd.sh read.py campaigns --customer-id 4467722415
./tsd.sh insights.py account --customer-id 4467722415 --date-range LAST_30_DAYS
./tsd.sh insights.py campaign --customer-id 4467722415 --date-range LAST_30_DAYS
./tsd.sh ga4.py conversions --property 312966741
./tsd.sh ga4.py report --property 312966741 --start 30daysAgo --end yesterday \
  --dimensions sessionCampaignName,eventName --metrics eventCount,keyEvents --limit 200
```

**Active campaigns (5 ENABLED, 18 PAUSED legacy — as of 2026-08-04):**
| Campaign | ID | Channel | Daily budget |
|---|---|---|---|
| TSD_Search_LeadGen | 11803942938 | SEARCH | $80 |
| TSD_04.29_Search_Nonbranded_Evergreen | 23813282398 | SEARCH | $60 |
| TSD_07.01_Lead_Search_MiniSplit-General | 24050402045 | SEARCH | $24 |
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | 24045403368 | PERFORMANCE_MAX | $16 |
| TSD_07.01_Lead_Search_Mitsubishi-Brand | 24050401592 | SEARCH | $16 |

Paused: Direct Call Ads, AC LP Campaign, Heating LP, All Seasons AC Branded, All Seasons Search \| HVAC/Repair, All Seasons Search \| Installations, HVAC (Call Only) PHR, HVAC (Lead Gen) EXA, HVAC (Call Only) EXA, Sales-Performance Max-09/18/2023, TSD_04.07_Search_MitsubishiHeatPump, TSD_04.08_PMAX_Daikin_Calls, TSD_03.23_Search_NonBranded_Evergreen, TSD_04.15_Search_DaikinHeatPump.

---

## 2026-08-13 — GA4 disconnected as an Ads data source (tracking cleanup)

Edu disconnected GA4 as a data source in the account's conversion/data-source settings, so GA4 events no longer auto-populate as Ads conversions — cuts off the junk-event path (e.g. the inflated `book_now_link_click` events flagged 2026-08-11) from becoming conversions. Paired with new GTM work building dedicated `awct` Lead and Phone Click conversion tags to replace the GA4 import; full detail in `gtm-log.md` (2026-08-13 entry) since that side lives in GTM, not here. Those new tags are still in a draft workspace, not published yet.

---

## 2026-08-04 (2) — Mitsubishi co-op media plan launch-date discrepancy: actual date, receipt, and plan impact

**Trigger:** A CSR flagged (via Edu, "@Eduardo Marinho") that the Mitsubishi co-op media plan "isn't accurate anymore because we're a month delayed" — asked for the real launch date, a receipt proving it, and how the delay affects the rest of the plan.

**Docs reviewed:** `~/Documents/All Seasons /` — `AllSeasons_Mitsubishi_MediaPlan (3).docx` (the co-op plan, submitted to Mitsubishi 2026-05-22), `SEASONS AIR - 2026 Mitsubishi Coop Package with Guidelines (...).pdf` (Mitsubishi's program rules), and `1264344367254795_20260731.pdf` (Google Ads July billing statement).

### Plan says July 1. Actual launch, verified via Ads API: July 20.

`campaign.start_date_time` pulled directly for all 3 co-op campaigns — launched simultaneously:

| Campaign | Type | Actual start |
|---|---|---|
| TSD_07.01_Lead_Search_Mitsubishi-Brand | Search | 2026-07-20 13:11:00 |
| TSD_07.01_Lead_Search_MiniSplit-General | Search | 2026-07-20 13:11:20 |
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | PMax | 2026-07-20 13:15:03 |

Real gap = **19 days**, not the "month" the CSR quoted — worth correcting when it goes back to her (that framing wasn't Edu's, came from the CSR).

There's also a legacy `TSD_04.07_Search_MitsubishiHeatPump` (PAUSED, started 2025-12-10) — not part of the current co-op plan, noted only so it isn't confused with the live campaigns.

### Plan impact

- **No co-op compliance risk.** METUS preapproval (Nov 15, 2026) and final claim submission (Jan 4, 2027) are fixed calendar dates, unaffected by the launch delay.
- **~$1,031 of peak-season budget unspent.** Plan called for $3,400 combined across July + August ($1,700 each, "Peak Summer"). At the current $56/day combined run rate (PMax $16 + Brand $16 + MiniSplit $24), Jul 20–Aug 31 spend lands ~$1,031 short of that.
- **Section 7 milestones all shift ~19 days**: learning phase (planned Jul 1–14 → actually Jul 20–Aug 3), first optimization review (Jul 15 → ~Aug 4), CPA bidding switch (~Sep 1 → ~Sep 20), Q4 heating push (Oct 1 → ~Oct 20).
- **Dec 15 stop date is TSD's own execution choice, not a co-op requirement** — Section 2 of the plan states the approved co-op window runs through Dec 31. Room exists to extend serving to recover lost days if needed, but that's a separate decision from the August catch-up below.

### Fix proposed — PENDING, not yet executed

Raise combined daily budget from $56/day → $94/day for Aug 5–31 to close the $1,031 gap by end of month, split proportionally to preserve the plan's ~61/29 Search/PMax mix:

| Campaign | Current | Proposed (Aug 5–31) |
|---|---|---|
| Search — Mitsubishi Brand | $16/day | $27/day |
| Search — MiniSplit General | $24/day | $40/day |
| PMax — Mitsubishi Ductless | $16/day | $27/day |

Reverts to plan levels ($950 search / $400 PMax) in September. Flagged risk: a ~68% jump this early (day 16 of serving, near the edge of the learning window) can reset/extend Google's learning phase — expect CPL to move around short-term, not necessarily a problem.

**Not yet pushed live** — per house doctrine (budget changes require written client/AM approval via ticket, Paid never executes first and notifies after), this stays as a proposed number until that approval comes through.

### Receipt found for the co-op claim file

`1264344367254795_20260731.pdf` (Google Ads July statement) confirms real spend on the 3 co-op campaigns in July:

| Campaign | Units | Amount |
|---|---|---|
| Search — MiniSplit-General | 83 clicks | $288.00 |
| PMax — Mitsubishi-Ductless | 252 clicks + 373 impr. | $192.00 |
| Search — Mitsubishi-Brand | 33 clicks | $186.54 |
| **Total** | | **$666.54** |

This belongs in the co-op invoice-compilation package (Section 7 of the plan calls for exactly this). Caveat: it's a monthly rollup with no daily breakdown, so on its own it doesn't visually prove the Jul 20 start date — pair it with the campaign start-date data above if the date itself needs to be shown, not just the spend.

### Side note (not actioned)

The docx itself is internally inconsistent: Section 2.1's monthly budget schedule tapers from $1,700 (Jul) down to $1,153 (Dec), but Section 3.1's per-campaign table lists flat ~$305/$325/$282 monthly figures that don't match any single month in 2.1. Didn't chase this down since it wasn't what was asked — flagging in case it causes confusion later.

### Open / next steps

- [ ] Get written approval (client/AM ticket) before pushing the $56→$94/day budget change live.
- [ ] Decide separately whether to extend serving past Dec 15 (plan allows through Dec 31) to recover lost days, vs. just closing the July/August gap and reverting to plan pace in September.
- [ ] Reconcile the docx's Section 2.1 vs. 3.1 budget inconsistency at some point — not urgent.

---

## 2026-08-04 — Initial account check + PMax "conversions" turn out to be soft link clicks, not verified leads

**Trigger:** Edu asked to check the account cold (no prior log existed — first time touching this client).

### Account snapshot, last 30 days

| Metric | Value |
|---|---|
| Total spend | $5,016.00 |
| Clicks | 1,212 |
| Conversions (Ads-reported) | 153 |
| Search impression share (blended) | 13.2% |
| Blended CPL | $32.78 |

### Per-campaign CPL (Ads-reported "conversions")

| Campaign | Cost | Conversions | CPL | Search IS | Budget-lost IS | Rank-lost IS |
|---|---|---|---|---|---|---|
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | $230.68 | 89.0 | $2.59 | 10.0% | 32% | 61% |
| TSD_Search_LeadGen | $2,437.52 | 34.5 | $70.65 | 17.6% | 50% | 32% |
| TSD_07.01_Lead_Search_MiniSplit-General | $353.17 | 5.0 | $70.63 | 10.9% | 46% | 43% |
| TSD_07.01_Lead_Search_Mitsubishi-Brand | $224.80 | 3.0 | $74.93 | 17.8% | 46% | 36% |
| TSD_04.29_Search_Nonbranded_Evergreen | $1,769.84 | 21.5 | $82.32 | 11.1% | 78% | 11% |

At face value the PMax campaign looks like the account's best performer (89 conversions at $2.59 CPL, ~27x cheaper than the Search campaigns). Edu flagged this as suspicious and asked to check GA4 for a more realistic read.

### GA4 investigation — PMax "conversions" are 100% link clicks, zero verified leads

GA4 conversion-action breakdown for campaign `24045403368` (Ads side, `segments.conversion_action_name`, LAST_30_DAYS):

| Conversion action | All conversions | Conversions (primary) |
|---|---|---|
| book_now_link_click | 52.0 | 52.0 |
| phone_link_click | 36.0 | 36.0 |
| call extension LEAD | 1.0 | 1.0 |
| page_view | 541.0 | 0.0 (not counted toward primary "conversions") |

So the 89 primary conversions = 52 book-now clicks + 36 phone clicks + 1 call-extension lead. `page_view` is misconfigured as a GA4 key event (4,029 page_views account-wide are marked as "conversions" in GA4) but is **not** flowing into the Ads "conversions" column — it only inflates `all_conversions`. Good news: it wasn't the source of the $2.59 CPL.

The real issue: cross-checked against GA4's own event table for this campaign's sessions (`sessionCampaignName = TSD_07.01_Lead_PMax_Mitsubishi-Ductless`, 30-day window):

| GA4 event | Count | GA4 key event? |
|---|---|---|
| page_view | 511 | Yes (misconfigured) |
| book_now_link_click | 47 | Yes |
| phone_link_click | 27 | Yes |
| contact_us | 42 | No |
| submit_lead_form | **0** | — |
| ghl_contact_us / ghl_book_now / ghl_schedule_service | **0** | — |

**Zero** actual form submissions or GHL-captured contacts came from this campaign's traffic in 30 days — even though other campaigns in the account (e.g. TSD_04.29_Search_Nonbranded_Evergreen) show a couple of real `submit_lead_form` events. All 89 "conversions" credited to the PMax campaign are link-click engagement (clicking "Book Now" or a phone number), not confirmed leads.

### Realistic CPL, recut by definition

| Definition | Count | Cost | CPL |
|---|---|---|---|
| Google Ads "conversions" (as-reported) | 89 | $230.68 | $2.59 |
| GA4 engaged clicks (book_now + phone, excl. junk page_view) | 74 | $230.68 | $3.12 |
| Phone-click only, Ads-side count | 36 | $230.68 | $6.41 |
| Phone-click only, GA4-side count | 27 | $230.68 | $8.54 |
| **GA4 verified leads (form submit / GHL contact)** | **0** | $230.68 | **N/A — no confirmed leads in the period** |

### Aberto / next steps (parked — Edu said we'll get back to it)

- [ ] Decide which conversion action(s) should actually count as "primary" for this campaign in Google Ads — `book_now_link_click` and `phone_link_click` are soft signals, not verified leads.
- [ ] Investigate why `page_view` is marked as a GA4 key event account-wide — likely a legacy misconfiguration, worth fixing regardless of this campaign (it's polluting `all_conversions` everywhere, not just PMax).
- [ ] Same "real CPL" gut-check hasn't been run yet for the other 4 active campaigns — worth doing before drawing conclusions about which campaign is actually cheapest.
- [ ] Add this account to the skill's `contas.yaml` registry (not there yet — had to be found manually via `customer_client` query).
- [ ] No GHL/CRM cross-check done yet on whether phone/book-now clicks convert to real jobs downstream — GA4 alone can't answer that.

## 2026-09-10 — PPC budget cut to fund LSA increase

Client wants LSA raised from $69/week to $250/week ($1,000/month) and asked us to fund it by deducting from PPC.

**Math:** LSA increase = $250 - $69 = $181/week. Current PPC total was $211/day ($1,477/week). New PPC target = $1,477 - $181 = $1,296/week → $185.14/day.

**Where the cut came from:** Pulled fresh 7-day search_budget_lost_impression_share / search_rank_lost_impression_share for all 6 enabled campaigns — every single one was budget-capped (36.7%-61.9% budget-lost IS), unlike the 2026-08-31 audit where Mitsubishi-Brand had headroom. With no campaign safely absorbing the full cut, applied a proportional ~12.3% reduction across all 6 rather than concentrating the hit on one:

| Campaign | Before | After |
|---|---|---|
| TSD_Search_LeadGen | $80/d | $70/d |
| TSD_04.29_Search_Nonbranded_Evergreen | $63/d | $55/d |
| TSD_07.01_Lead_Search_MiniSplit-General | $27/d | $24/d |
| TSD_08.31_Search_Branded_Evergreen | $15/d | $13/d |
| TSD_07.01_Lead_PMax_Mitsubishi-Ductless | $16/d | $14/d |
| TSD_07.01_Lead_Search_Mitsubishi-Brand | $10/d | $9/d |
| **Total** | **$211/d** | **$185/d** |

Verified live via `read.py campaigns` after the `update.py` calls (not just the success JSON, per the known silent-failure gotcha). New total = $185/day = $1,295/week (~$1 off target from whole-dollar rounding). Told client PPC is now at $185/day so they can set LSA to $250/week accordingly.

**Aberto:** none of the 6 campaigns had budget headroom this week (all budget-capped, a change from the 08-31 audit) — worth re-checking impression share in a week or two to see if the smaller budgets are costing real lead volume, and whether the proportional split should be rebalanced toward the stronger performers (LeadGen $36/CPL, Branded Evergreen $15/CPL) away from the weaker ones (MiniSplit-General $71/CPL, Mitsubishi-Brand 0 conversions this week).

## 2026-09-14 — LSA bump confirmed, client reply sent

Follow-up on the 2026-09-10 PPC cut. Client (via ticket) asked to confirm how much to bump LSA up to. Confirmed: $250/week (~$1,000/month), the same target the 09-10 PPC cut was sized against — no new math needed, just reconfirming the number before the client pulls the trigger on their end.

Sent client-facing ticket reply: PPC cut from $211/day to $185/day (~$26/day, ~$181/week) frees up the room for the LSA increase from $69/week to $250/week.

No account changes made this session — LSA budget itself is set client-side, not through us.

## 2026-09-15 — Weekly account-level snapshot + conversion trust check

No account changes. Pulled the standard weekly metric set, account-level, last 7 days:

| Metric | Value |
|---|---|
| Spend | $1,574.20 |
| CPL | $38.40 |
| CPC | $3.55 |
| Total Conversions | 40.99 |
| Conv Rate | 8.82% |
| Impression Share | 12.07% |
| Branded Conversions | 3.0 |
| Unbranded Conversions | 37.99 |
| Branded CPL | $32.39 |
| Unbranded CPL | $38.88 |

Branded/unbranded split rule for this account: only campaigns with "Branded" literally in the name count as branded (`TSD_08.31_Search_Branded_Evergreen`) — everything else, including `TSD_Search_LeadGen` (which still has an unmigrated brand ad group per the 08-31 audit), counts as unbranded.

Ran the conversion-action trust check (`segments.conversion_action_name` from `customer`, `LAST_7_DAYS`) — all 40.99 conversions are legit lead signals, no junk:

| Conversion Action | Category | Count | % |
|---|---|---|---|
| call extension LEAD | Phone call lead | 23.00 | 56.1% |
| Click to call | Phone call lead | 15.00 | 36.6% |
| [TSD] Lead Form | Form submission | 3.00 | 7.3% |

No `page_view` or other soft-signal junk in this window (contrast with the PMax `book_now_link_click` gut-check from earlier in the log — that pollution isn't showing up in the account-level number right now, but wasn't re-checked at the GA4 level this session).
