---
name: tsd-integrate-comfort
description: "Integrate Comfort Systems (ICS, icshvac.com, NJ) PPC account facts: main Google 4571881760, PMax weekday schedule, double-counted form actions, NonBranded weak spot"
metadata:
  node_type: memory
  type: project
  originSessionId: c6148278-e414-4336-a569-2bbdde706789
  modified: 2026-10-07T14:14:15.703Z
---

"ICS" = Integrate Comfort Systems (icshvac.com, northern NJ, New York DMA). Current TSD client (see [[tsd-client-roster-status]]).

- **PPC = main Google account `4571881760`** (not in contas.yaml, pass `--customer-id`). LSA lives in separate accounts (2895702982 Belleville, 2175964343, 8323145223). Meta "ICS" 2070047533283360 is connector-disabled.
- Live campaigns as of 2026-10-07: `TSD_03_22_Pmax_Evergreen` ($40/d), `TSD_03.22_Search_Branded_Evergreen` ($12/d, Target IS), `ICS_Search_NonBranded_Core_2026-07` ($25/d, Max Conv).
- PMax has an ad schedule of **Mon–Fri 7am–5pm**, so it spends $55–80 on weekdays and $0 on weekends. That is monthly pacing, not overspend.
- PMax "clicks" include cheap YouTube clicks (e.g. 55 for ~$10 on 10-05/06), so account CPC and click totals look better than the search traffic really is.
- **Double counting CONFIRMED 10-07:** GTM `GTM-N4QW8BF` (acct 6002097837 / container 32532837) fires the Ads tag "Submit lead form - web" on custom event `form_submitted` from the GHL listener. Separately, GA4 property 310245312 receives `ghl_*` events (contact_us, service_area, survey, ac_ppc) that GTM does NOT send. Ads imports those as primary, so 5 of 11 form fills in 90d counted twice (same click hour/device/ad group). Fix = make the `ghl_*` imports secondary in the UI; no GTM change needed. Not applied yet. Our GA4 token can't see 310245312. phone_link_click and mailto_link_click count as leads too (same risk as [[tsd-proud-pops-tracking]]).
- "Calls from ads" uses a 60s threshold and checks out against call_view. **Website calls are nearly untracked** (1 Landing Page Call in 90d); CallRail runs on the site, so check CallRail before judging NonBranded.
- **APPLIED 2026-10-08 (verified):** PMax "air conditioning" + both "rebate" negatives removed, "tech support" added, budget $40→$50. NonBranded: AC Repair ad group paused (heating focus), 16 negatives added, $25→$15. Branded CPC ceiling $5→$7. Total still $77/day. Script: clients/integrate-comfort-systems/ics_changes_2026-10-07.py.
- ⚑ **CHECKPOINT ~2026-10-28:** PMax ≤ ~$150/call else roll back $10; NonBranded heating ≤ ~$200/real lead else pause + move $15 to PMax. ON HOLD: CallRail check, ICS questions (Saturdays/boilers/AW-1064128677), ghl_* imports → secondary (UI).
- 10-07 DEDUPED baseline: 7d $488 / 3 real leads ($163 CPL); 30d $2,172 / 16 real ($136 CPL; 18 reported). PMax ~$120 per call; Branded $52; NonBranded $383 with IS under 10%. Search-only CPC ~$9-10.

**Why:** these explain why ICS numbers look odd at first glance (weekend zeros, click spikes, branded leads in pairs).

**How to apply:** for the weekly snapshot ([[tsd-weekly-ppc-snapshot]]), de-dupe same-day form pairs in branded and quote search-only CPC. Full history is in `clients/integrate-comfort-systems/google-ads-log.md`.

**2026-10-28 checkpoint (fu-012, read-only):** both rules FAIL. PMax $936 / 1 real call ≥60s (was $733 / 6); ad calls up 16→24 but <20s calls 2→14, CallRail Google Ads ≥60s 8→5 → callers drop in ICS's IVR or mis-tap (call-wins 10-01..10-15 already showed IVR-only). '[TSD] Click to call' (= AD call-button taps, CLICK_TO_CALL, not site taps) are primary and = 7/8 PMax + 5/7 Branded conv. NB $287 / 1 real; heating ad group barely serves ($43), AC Install took $244 on DIY/cost terms. Branded healthy (~$50/lead, 15% budget-lost at $12). Decisions in Command Center fu-109.

**2026-10-28 APPLIED (Edu's go, fu-109 1-3), total $77/d:** PMax $50→$40 + custom goal 'TSD | Calls + Forms (no taps)' 6459689709 (Calls from ads + Landing Page Call + Submit lead form - web + Lead form - Submit; no taps, no ghl_*); NB AC Installation PAUSED → heating-only, Max Clicks $15 cap, $15→$22; Branded $12→$15. Recheck 11-04 fu-109. Script clients/integrate-comfort-systems/ics_apply_1028.py.

**2026-10-28 call-wins (10-16..10-28, 14 ad calls):** IVR question RESOLVED: recording continues through the transfer, so IVR-only = real hang-ups in the 8-option menu (~45-60s). 10-01..10-28: 31 ad calls, 3 new booked, 24 never reached a person. Staffing fine (answer ~10s after picking service). AM ask = route ad/LSA tracking numbers past the menu (fu-110). Several ad callers from NYC, outside the NJ geo.

**2026-10-28 fu-031:** CallRail → Ads uploads for ICS still ZERO since 10-09 despite ~12 gclid Google Ads calls (incl. 10-21 483s booked). Integration shows active; check CallRail UI via browser.
**2026-11-02 AT Internal Request 5e5dcc2a (DRAFT, Intake open for Edu to submit):** 'ICS: most ad callers hang up in the phone menu' → Angela (Execution), Edu (Review & Close), dept Customer Success. Asks: route ad tracking numbers straight to service/sales (change in CallRail) or 'Press 1 for service or a new system' first; NYC boroughs (AT service area lists Manhattan only). fu-110.

**2026-11-04 fu-109 recheck (10-29..11-03 vs 10-09..10-26):** PMax $28/d of $40, 2 real 60s+ ad calls (152s Orange, 65s Jersey City, not transcribed) = ~$83/real call vs $936; Search partners $160 → $9, YouTube 31%. NB heating-only $123 / 18 clicks / 0 leads (too early). Branded IS 82%, budget-lost 0. The 10-28 no-taps custom goal LEAKED taps (2 counted), same as Watt's Right → APPLIED `[TSD] Click to call` 7835539864 → Secondary + NB PHRASE negs 'steve sirc', 'advanced heating' (read-back OK). Next read fu-123 11-11. IVR drops continue (3 of 6 ad calls < 40s).

**2026-11-11 whole-account read (fu-123):** paid = 0 real leads 11-05..11-10 ($441); ICS's real calls come from GBP + organic (~10-12/wk). **LSA Belleville 2895702982 sits at $1/day** (eligible, insurance/license PASSED) after doing 30 leads/$1,435 in May 2026 and 40-106/mo in 2023-24; cut in June by unknown hand. LSA Englewood Cliffs 8323145223 = $1,429/day budget, 0 impressions ever (never served, UI check). Carlstadt 2175964343 $51/d, 1-4 leads/mo. Mitsubishi YouTube 23599485735 in the Belleville acct burns $610/mo since April, owner unknown. NB ad URL redirects twice to /services/heating/repair/ (no form, QS 3, LP below avg). PMax = 11 towns, homepage, partners+display on, Mon-Fri 7-17, buys competitor names + YouTube. Plan + table in google-ads-log.md 2026-11-11 (later): pause NB+PMax, restore LSA Belleville ~$50/d, cap Englewood, IVR fix, heating LP + NB relaunch.
**2026-11-11 APPLIED (Edu's go):** NB 24047025253 + PMax 22890783804 PAUSED; LSA Belleville 15786867110 budget $1.43 → $50/day; LSA Englewood 21467507022 $1,429 → $50/day. Live paid = Branded $15 + 3 LSA. AT draft be762554 to Angela (did ICS want Belleville cut? Mitsubishi YouTube owner?). AT client record = "ICS" 1e439ca7 (not "Integrate Comfort"), AM Angela. Gotcha: the API shows LSA budgets as daily (weekly ÷ 7), so "$10/week" reads $1.43.

**2026-11-12 APPLIED (Edu's go): NB 24047025253 RELAUNCHED on the new heating LP** icshvac.com/furnace-heating-repair-northern-nj/ (Sha, live 11-12, brief-checked): goal = no-taps custom 6459689709, $25/d, Max Clicks $20 cap, 12 exact + 4 phrase heating kws (old 8 phrase paused), +20 negs, new RSA 831383124121 (old paused). GTM listener needs email in the GHL payload. Google rejects the keyword "no heat in house" as Dating policy. Test lead + first read fu-159 11-19. Script ics_nb_relaunch_1112.py.
