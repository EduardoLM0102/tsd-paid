---
name: tsd-watts-right
description: "Watt's Right Electric (Tulsa OK) TSD client — Google Ads 3651667805, LSA-in-same-account, 2026-09-29 overhaul; 10-09 recheck done, 3 fixes proposed, fu-034 on 10-20"
metadata:
  node_type: memory
  type: project
  originSessionId: 12a4b551-6109-49d4-8e9d-77b05aa786be
  modified: 2026-10-01T14:23:13.198Z
---

> **10-09 RECHECK DONE (read-only)** → log entry 10-09 in `clients/watts-right/google-ads-log.md`. Findings:
> Nonbranded fully spends $120 but Max Conv doubled CPC ($9.46→$19.38), budget-lost IS still 27%; Branded now
> budget-capped by the $8 ceiling (IS 86%→55%) AND has a Mon–Fri 06–22 ad schedule, so nights/weekends brand
> searches get no ad (brand negated in NB+PMax since 09-29); PMax real CPL $82. Proposed (await Edu): Branded
> $20→$35 + all-week schedule, NB $120→$105 + tCPA ~$80, 11 competitor negatives incl. 'quality electric'.
> Next: fu-034 (10-20) RSA A/B + CPL recheck.

Watt's Right Electric — Tulsa OK electrician, TopServ client. Google Ads customer_id 3651667805
(MCC Topservdigital 4155514468), in `contas.yaml`. Full history in
`topserv-workspace/clients/watts-right/google-ads-log.md`. Read that before acting on this account.
GTM: GTM-K52ZTWS8 = account 6275120193 / container 209660640 (live v9 as of 09-29).

**Account quirk:** LSA (`LocalServicesCampaign:SystemGenerated:...`) lives inside this same account,
~77% of Google spend ($11.5k/30d, ~$55/lead). PPC is the minority.

**Live PPC after 2026-09-29 (3 campaigns, $235/d):** Branded $20 (Target IS 95% top, max CPC $8),
Nonbranded $120 (Max Conv; ad groups → service pages), PMax $95 (Max Conv, homepage). EV Charger
(24094882200) PAUSED 09-29; EV searches are now covered by Nonbranded's EV ad group
(`ev electrician` re-enabled). All geo = PRESENCE, with India/Pakistan/Philippines excluded.

**What 09-29 found (why things changed):**
- EV Charger's "$24 CPA" and the 72.8% budget-lost IS behind the 09-22 raise were India traffic
  (pre-09-17 geo fix: 908/979 clicks, 35/39 conv). Post-fix it was competitor names at $62–84/click.
  Always segment `geographic_view` by country before trusting a new campaign's CPA.
- PMax "best CPA" was job seekers (12.3/38.9 conv, e.g. "electrical apprentice jobs tulsa") + brand (7).
  The careers page GHL form fired Google Ads Lead via GTM listener [55] → trigger [35] → tag [58].
  Fixed in GTM v9 (blocking trigger [73] on tags 58+71), extended to Meta Lead [42] + GA4 [53] in v10.
- Brand + competitor searches were leaking into Nonbranded broad match. Now blocked by negatives
  (Edu chose block over conquest).

**09-30:** GTM v10 extends the careers block to Meta Lead + GA4. 09-22 increase was client-requested
(ticket to-do closed). 3 new Nonbranded RSAs (ads 826560998576/579/582) ENABLED 10-01, running A/B
against the original ads. Compare at the recheck and pause the weaker per ad group.

**Meta (acct 588638883283311), checked 2026-10-01** (log: `clients/watts-right/meta-ads-log.md`). NOT awareness-only (the 09-28 Growth Engine
pull undercounted it). A live panel-replacement Instant Form funnel, Tulsa 50mi, age 25+, Advantage
audience off: TOF-5/7/26 (cold, excludes MOF 10s viewers + form submitters), MOF-6/21/26 (retargets
"TOF 3sec Audience" video viewers), BOF-7/9/26 (retargets "MOF 10sec Audience"), plus "LS | Panels-
FourMode" (cold, 09-22, website leads via landing page). Last 30d: TOF $3,179/63 leads, MOF $1,434/26, BOF $274/6, FourMode $279/6.
10-01 renamed MOF -> "TSD_06.21_MOF_LEADS_ABO_Panels - Retargeting 3s Video Viewers" and BOF ->
"TSD_07.09_BOF_LEADS_ABO_Panels - Retargeting 10s Video Viewers" (both ABO; ad sets are NAMED $5 but live budgets are MOF $40+$20, BOF $10+$5, spending ~80% of that; still ACTIVE).
**10-05:** client retargeting report built for Sep 25-Oct 1 (2-page plain PDF, results only; Edu wants adjustment ideas kept internal, never in the client doc). Findings: MOF (3s pool) costs MORE per lead than cold TOF; BOF has 1% lookalike expansion ON; FourMode is a WEBSITE-leads link-ad campaign, not instant form. Adjustment ideas (MOF 50%-watched pool, site-visitor pool, lead->job match) live only in meta-ads-log.md. Details in meta-ads-log.md.
**10-12:** weekly retargeting report #2 built for Oct 2–8 (same 1-page plain format; $525.20 / 10 leads / $52.52). Found:
TSD MOF/BOF renames REVERTED 10-06 by "Clay Manus token" (Manus Dash), who also launched a 05-RT-TOF3s website-leads
retargeting ad set in FourMode (kept out of the client PDF, Edu to decide scope); Meta flipped Advantage+ audience ON
10-10 on all ad sets incl. MOF (step 2 no longer pure retargeting going forward). Details in meta-ads-log.md 10-12.
**10-22:** client report #3 = Oct 9–21, FB retargeting (17 leads / $69.33) + NEW Google page (29 verified leads / $102, LSA out) + the 10-20 changes. Google page also has a CallRail table (49 Google Ads calls = Call Extension PPC tracker + Website pool w/ gclid; Google counts 60s+, one per click, so only 19). Meta CPL +32% vs Oct 2–8. Next report starts Oct 22. Details meta-ads-log + google-ads-log 10-22.
TOF + FourMode keep their original non-TSD names. Whoever runs them, nobody had discussed it with Edu before 10-01.
Pixel audiences ("Page Views", "Page View_Without Leads", pixel 567402072026960) are ~20 people and
unused, so website retargeting isn't viable as-is. Old "BOFU_Remarketing_Zips" ($5.3k, paused) was
named remarketing but was zip-code targeting with no audience.

**Older history:** Branded conversion-goal gap fixed 2026-08-12 (only calls-from-ads was biddable;
see [[tsd-google-conversion-goals-mechanics]]). Nonbranded "overrun" on 08-12 was normal 2x daily
smoothing.

**How to apply:** check the log for the latest state before re-diagnosing. Several "problems" here
were stale to-dos or tracking config, not performance. Budget moves at a constant total need no ticket
([[tsd-budget-approval-scope]]).

**10-05 weekly 7-day pass (AT task closed):** 14 Nonbranded negatives (6 competitors PHRASE, EV product/utility: tesla/tesla wall connector/level 2 ev charger EXACT, electrify america/pso/for sale/free electrician PHRASE). Left 'quality electric' open (converted once), decide at 10-09 recheck. Week CPL $72 vs $40 prior (EV Charger's last $401 + careers block). Log entry 10-05.

**2026-10-19 (Gui weekly + 14-day, staged only):** PPC $1,530 / 28 / $54.65; LSA $2,527 / 44 / $57; Meta $1,952 / 31 / $62.97 (retargeting MOF/BOF 2.6–3.3x TOF CPL). New non-TSD boosted post (engagement) live in Meta. Proposed tCPA ~$90 / CPC cap on NB (uncapped Max Conv bidding up).

**2026-10-23 Q4/Q1 budget proposal DRAFT (Gui, AT Client Request 7b72529c from Allen via Angela, awaiting Gui's validation, not sent):** `clients/watts-right/budget-proposal-q4-2026-q1-2027.md` → PDF (2 pages) + internal notes. Baseline 30d $26,860 / 462 leads / $58 (LSA $12.7k/219, cap $12k/wk only 25% used = not budget-limited). 3 options on ~$27.7k/mo: +$2.6k / +$5.5k (recommended, ~525 leads) / +$9k; extra to NB (+ raise Edu's $80 tCPA), PMax, Meta TOF + ARL; new generator/surge ad group. Last winter LSA flat Oct–Jan, Feb −15-20%.
