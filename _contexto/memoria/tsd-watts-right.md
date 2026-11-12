---
name: tsd-watts-right
description: "Watt's Right Electric (Tulsa OK) TSD client — Google Ads 3651667805, LSA-in-same-account, 2026-09-29 overhaul; 10-09 recheck done, 3 fixes proposed, fu-034 on 10-20"
metadata:
  node_type: memory
  type: project
  originSessionId: 12a4b551-6109-49d4-8e9d-77b05aa786be
  modified: 2026-10-01T14:23:13.198Z
---

⚑ 11-10 fu-117/119 read (11-04..11-09): blended PPC+LSA $73 = on Push plan; Branded $22 CPL but budget-lost 57%; NB $117 Google → ~$140 after transcribing (3 of 9 callers not leads, 2 job seekers; 2 of 3 new booked = whole-home generator); PMax 4 ad calls transcribed = 0 new customers → 11-10 09:13-09:14 APPLIED (Edu): PMax 23833205176 PAUSED, Branded $50→$145 (got PMax's full $95, Target IS $8 ceiling), NB kept tCPA $110/$320 + 6 competitor negs, PPC total $465/d unchanged, AM note owed, next read fu-145 11-17; ⚠ Google 'Calls from ads' overstates, always transcribe (CallRail 'Call Extension PPC' recordings match call_view by timestamp, WR CallRail = own acct 537241053);
> **11-04 LSA → PAY-PER-LEAD PMAX MIGRATION (Google, not us):** 12:45 CT Google created `Pay-per-lead-PMax-Watt's Right Electric`
> (24425981973, PERFORMANCE_MAX, Max Conv, LEARNING, budget $1,714.29/d = same as old LSA, 1 asset group `xcat:service_area_business_electrician`
> → homepage); 12:46 old `LocalServicesCampaign:SystemGenerated` 17732780541 set PAUSED (no user in change_event). Old LSA still billed $546 + 9 leads
> on 11-04 before the switch. Gotchas: our LSA tooling keys on channel LOCAL_SERVICES / local_services_lead (lsa_report.py, google_channels.py),
> and PMax rechecks must now split 24425981973 from TSD PMax 23833205176. LSA history doesn't migrate to the new campaign: keep old-campaign pulls.

> **11-04 APPLIED Option 3 "Push" (+$7k/mo Search, client pick via Angela Slack 11-04, Edu's go):** Branded $35→$50, NB $105→$320 (Search $370/d ≈ $11.25k/mo),
> NB tCPA $95→$110, 3 new NB ad groups (Electrician (General) → /locations/tulsa-ok/, Whole-Home Generator, Whole-Home Surge Protector) + 17 job-seeker negs.
> LSA + PMax unchanged. RSAs in review at apply. Check approval/pacing 11-06, read 11-10 w/ fu-117. Detail: google-ads-log 2026-11-04.

> **11-04 Budget proposal GOOGLE-ONLY (Angela, client meeting 11-04):** TSD does NOT manage Watt's Right Meta (Edu 11-04), so Meta is out of every
> TSD proposal/report scope from now on. PDF `Watts-Right-Budget-Proposal_Q4-2026-Q1-2027_Google-only.pdf`, math in the internal-notes file (11-04 section).
> All Meta $ into Search isn't feasible: NB rank-limited (rank-lost 55-60%), Branded tops out ~+$500/mo, generic "electrician" pot ≈4,700 searches/mo in
> Tulsa DMA (untargeted, $25-30+ CPC, under LSA). Search ceiling ~$11k/mo. Options +$2.6k/+$5.5k/+$7k, rec Opt 2 ($25.4k/mo, ~360 leads, ~$70).

> **10-28 Angela follow-up ("how $15.5k excl. LSA on a $7k budget?"):** 30d 09-28..10-27 = PPC $7,181 (on the $235/d total, unchanged since 09-22;
> 10-20 was a reallocation only) + Meta $8,374. Meta live ad set budgets ~$273/d that actually deliver (TOF $145, MOF $67, FourMode $66, BOF $20;
> 3 TOF test/RT ad sets $45/d ACTIVE but $0 spend) + TSD Awareness CBO ~$10/d + boosted posts ~$9/d. Last Meta budget changes = 10-05/10-06,
> all raises, by "Clay Manus token" (Manus Dash app). Identity of Clay not confirmed in repo.
> Full answer (meta-ads-log 10-28): TSD manages MOF + BOF + awareness (Edu, corrected 10-28), NOT TOF/FourMode/boosts. Lead-campaign daily
> budget $70 (07-28 am) → $223 (Clay 07-28) → $150 (Manuel/TSD pauses 08-01/12) → $227 (Clay 09-22) → $318 (Clay 10-05/06; $273 spends).
> No TSD raise since July. Stevie Fernandez boosts posts since 09-21. Final Slack reply for Angela drafted 10-28.
>
> **10-27 Angela budget question:** AT Client Request 7b72529c-add0-447f-8d89-4f54b660d723 (Execution done by Gui 10-24, now at Angela's
> Communicate stage). The ATTACHED PDF is Gui's FINAL, not the local .md draft: total $27,409 / 464 leads, Search $4,251, PMax flat at
> $2,890 in all options (local copy saved as *_AT-attached.pdf). Angela's "$7k budget excl. LSA" = Google PPC only, ON RECORD (found 10-28): AT ticket #793 'Demographics & Ad Spend Increase',
> client Luke: "As for the PPC Budget, lets double it from $3,496 to $7,000" ($3,496 = our 09-09 PPC-only PDF, LSA+Meta excluded) + AT task
> 0f5120ba-7d7b-4864-b424-72c3d12b1cee (09-21, 'Budget increase to $7,000/month', executed 09-22 as $235/d). NO approved Meta figure anywhere.
> Don't confuse: 09-30 '$3,500 never approved' DM thread = On The Way; 09-23 '$7,200 Meta+PPC' = Napps. Non-LSA $14,672 = Google PPC $6,836 + Meta $7,836. Meta is a separate pot (TOF/FourMode non-TSD names, Manus Dash).

> **10-27 fu-072 RECHECK of 10-20 changes (read-only)** → log 10-27. Real PPC CPL ~$100 → $66 (21 leads/7d). Branded worked
> (IS 37→80%). NB real CPL ~$129 → $48 but spends $75 of $105 (tCPA $80, rank-lost 71%), Emergency halved. PMax drifted to
> YouTube on 10-21 by itself (YouTube $409 vs Search $102/7d), 56/60 counted conv = Click-to-call taps, 4 real leads ($160).
> 10-27 later: NB tCPA $95 + 7 negs APPLIED (Edu's go), recheck fu-097 11-03. CallRail: PMax YouTube/Display ($538/wk) →
> 4 site-visit calls, 2 real (~$269/real call) vs PMax Search ~$51/real call. PMax gad_campaignid 23833223188 = Search side, 23833219135 =
> YouTube/Display side (wbraid, no gclid, so not uploaded). 10-27 APPLIED: PMax → custom goal 'TSD | Calls + Forms (no taps)'
> 6459658990 (Calls from ads + Phone Call + 2 forms). NOTE: here `[TSD] Click to call` = CLICK_TO_CALL (ad call-button taps,
> same bucket as Calls from ads), NOT a site tel: tag like Zen Air's; 55 YouTube/Display taps → 0 ad calls. Recheck fu-098 11-03.
>
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

**2026-10-23 PMax CallRail check (Gui):** PMax's "36 real leads / $72" (proposal baseline) does NOT hold up. 45 PMax calls in 30d (CallRail campaign stamp + Google call_view time match), transcribed locally: only 2 new booked (1 cancelled) + 3 open; 15 wrong number/utility (PSO, OG&E, Claremore, Generator Supercenter), 6 retail/job/out-of-area, 11 no conversation, 3 existing customers. Wrong-number calls run 60-300s so they count as conversions and Max Conv learns from them; top PMax term = 'generator supercenter tulsa'. ~$520 per real call lead. Don't add budget to PMax until fixed; NB + Branded calls not yet transcribed. Full table in clients/watts-right/budget-proposal-q4-2026-q1-2027-internal-notes.md.

**2026-10-24 proposal v2 (ready to send, Gui):** rebuilt on CallRail-verified Google leads (verified service calls + forms from 09-30). Baseline 421 leads / $27,409 / $65 (Search $4,251 incl. paused EV / 37 / $115, PMax 13 / $199). NB ≈ PMax per verified lead (~$200) but NB wins on booked new jobs; Branded ~$26. PMax flat in all options, its increment → Search (Branded $45 first, then NB, which needs tCPA up: rank-lost 68% at $80). Options ~450 / ~480 (rec) / ~510 leads. ~7 Search call leads were estimated from campaign lead rates while the last 17 transcripts ran.

**2026-10-24 v2.1 FINAL (Gui validated):** client table back on RAW leads (464 / $27,409 / $59; Search 57 / $75 incl. paused EV, PMax 36 / $72), verified finding used only to explain PMax staying flat (good volume, many calls not service requests, lots of room to improve). Options on raw basis: ~460 / ~500 / ~530 (rec, +70) / ~570, CPL $60-64. Verified table stays internal. Client-facing rule from Gui: show raw platform leads in client baselines, keep disqualification analysis as the reason for allocation, not as the headline number.

**2026-10-26 (Gui AT run, fu-072 recheck):** Branded IS 34%→71%; NB real CPL $130.66→$51.49 but NB underspends under the $80 tCPA (~$62/d of $105), staged tCPA ~$95-100. ⚠ PMax drifted to YouTube/Display tap-buying (10-21..10-25 Search $47.75 of $437.50, 50 of 53 conv = taps, 5 real leads): Edu to decide taps → secondary. KPI row 10-26 excludes taps (22 real / $65.24). Meta 7d 39 leads $51.86; FourMode (Clay Manus) $459 / 2 leads.

**2026-11-03 (fu-097, Claude):** Nonbranded on tCPA $95 (10-28..11-02): $96/day of $105 (was $75), rank-lost 71 → 66%, Emergency back (2 real leads),
real CPL $71.93 / 8 vs $44 / 12 on $80 → hold $95 (step back to ~$85-90 if > $80). 10 PHRASE negatives (competitors + EV research, ~16% of spend)
staged for Edu, next read fu-117 on 11-10. ⚠ PMax: custom goal 6459658990 is attached and excludes the tap action, yet PMax still counts
`[TSD] Click to call` as conversions (18 → 40/day, 0 real Google leads, Display $129 → $429, Search ~$0) → fu-098. Detail: clients/watts-right/google-ads-log.md 2026-11-03.

**2026-11-03 (later):** 5 competitor PHRASE negatives APPLIED on Nonbranded (evans/ap/half moon/ecs/blue sky electric, Edu's go). 5 EV research negatives still pending (fu-117).

**2026-11-03 fu-098:** the 10-27 custom goal did NOT remove taps from PMax bidding (custom goal including `Calls from ads` pulls in `[TSD] Click to call`, same PHONE_CALL_LEAD/CALL_FROM_ADS bucket). PMax 10-28..11-02: $617, Search $0.76, Display $429, 176 taps counted, 0 real Google conv, 0 ad calls, 0 CallRail 60s+ calls (11 short ones, several out-of-area). Proposed: pause PMax, Branded $35 → $45. Detail in clients/watts-right/google-ads-log.md 2026-11-03.

**2026-11-03 (later), Edu's call:** `[TSD] Click to call` set to SECONDARY account-wide (read-back primary False + include_in_conversions_metric False); PMax NOT paused, gets 1-2 weeks: verify taps gone from Conversions 11-05 (fu-118), first read 11-10, kill-or-keep 11-17 (fu-119; keep ≲ $100 real CPL + Search back, kill if 0-1 real leads at 11-10 or > ~$150 at 11-17). Branded $45 not applied.

**2026-11-12:** fu-068 (10-18 weekend ad calls hit a full voicemail on 918-508-0195) REMOVED by Edu as stale.
