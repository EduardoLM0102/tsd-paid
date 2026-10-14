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
