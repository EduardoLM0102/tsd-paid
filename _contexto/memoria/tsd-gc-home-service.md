---
name: tsd-gc-home-service
description: "TSD client GC Home Service (Greater Comfort) HVAC Cincinnati — Google Ads acct + 2026-07-27 audit findings (PMax budget bleed, call-click-only tracking, wrong vehicle)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e0f3fe08-b2a0-43ff-b8d0-23a749f97e55
  modified: 2026-08-28T12:52:44.102Z
---

GC Home Service ("Greater Comfort") — TSD client, HVAC/home services, Greater Cincinnati tri-state (Northern KY + SW OH + SE IN). Folder created 2026-07-17 (not in contas.yaml). Full context: topserv-workspace/clients/gc-home-service/ (README + weekly-log + google-ads-audit-2026-07-27.md).

**Accounts:** Google Ads `2375064049` (under Topservdigital MCC `4155514468`, access via local `google-ads-ratos` skill + scripts/tsd.sh). Meta acct `1434273655098937` (business "Greater Comfort" `362393681555340`, Ads MCP enabled but Meta *targeting* not readable via connector — read it from activity log). **LSA is a SEPARATE, unnamed customer_id `2974002658`** under the same MCC — not in `contas.yaml`, not in `lsa_report.py`'s hardcoded list, no LOCAL_SERVICES campaign inside `2375064049`. Only findable by geo match (Boone/Campbell/Kenton KY + Butler/Clermont/Hamilton OH = GC's tri-state area) — surfaced once before in a Proud Pops audit doc that excluded it for that client and never linked it to GC.

**2026-08-28 LSA diagnosis (low impressions):** compliance/eligibility all clean (license renewed 07-28 valid to 2027-06, insurance renewed 08-13 valid to 2027-08, background check passed, campaign ELIGIBLE/SERVING). Root cause: ad schedule was **Mon–Fri 8am–4pm only** (40 hrs/wk, no evenings/weekends) vs comparable healthy LSA accounts running 63-70 hrs/wk incl. weekends — GC markets 24/7 emergency service but the ad was ineligible to show exactly when HVAC emergency demand peaks. Result: $0 spent, 32-98 impressions/month, 2 leads in 90 days. Weekly budget reads $2,700/wk. Edu submitted an AM ticket same day asking for: (1) 24/7 hours, (2) bump the $2,700/wk budget, (3) add profile bio features (locally-owned, discounts, military discount, eco-friendly, workmanship guarantee, professional service). None of these three are Ads-API-executable (live in the Local Services app) — status: awaiting client/AM action, not yet verified live. Full detail in `clients/gc-home-service/google-ads-log.md` (2026-08-28 entry).

**Google account gotchas:** timezone `Africa/Kampala` (Cincinnati client — days shifted ~7h, budget resets ~5pm local, fixing needs Google support + wipes history); data lags ~1 day; `audit_history.py` is hardcoded to Mission Accomplished, don't reuse; `campaign.start_date/end_date` invalid in v24 GAQL. Service-area lists for Meta vs Google DON'T match + "Amelia KY"/"Williamsburg KY" unresolved (see README).

**Google Ads audit 2026-07-27** (30d: $3,752 / 15 conv / $250 CPL / 13% IS; last 7d = $1,330 spend → 1 conv). Only 2 of 12 campaigns live: `TSD_PMAX_Calls` + `TSD_Leads_Search_Branded_08.06`. Three findings, priority order:
1. **PMax budget 3x is bleeding — reverse it.** Raised $50→$155/day Jul 16 at ~$293 CPL; since then ~$963 for 1 conv, now 59% of all spend. Cut to ~$55/day (needs written client-budget-change ticket per doctrine).
2. **Optimizing to phone-call CLICKS, not booked jobs.** All 15 conv = `Calls from ads` + `[TSD] Website Call Link` (tap events). Zero form leads / CRM / offline import — same tracking gap as [[tsd-golden-plumbing]] and [[tsd-proud-pops-tracking]]. $250 CPL is vanity; fix before scaling.
3. **PMax losing 89% of impressions (56% Ad Rank / 33% budget), wrong vehicle for $150/day local HVAC.** Branded Search runs 87% IS / $84 CPL. Shift weight to tight-match Search + brand, shrink PMax to controlled test, fix landing-page/asset quality.
Secondary: competitor conquesting was pure waste (arlinghaus $132/0-conv etc, ~1 conv on ~$1,200) — already paused, keep off; brand defense worth keeping but $8+/click (check QS); archive 10 dead campaigns.

**Landing page (requested 2026-07-31, awaiting client approval):** scoped **for Google Ads search
traffic specifically**, not as a general/Meta page. Rationale is destination quality → lower CPC →
better Ad Rank → lower CPL (PMax was losing 68.5% of impressions to Ad Rank vs 11.2% to budget).
Meta is a *later* test once it proves on search, so pitch it as one page for search with Meta as
upside, never as a two-platform project. Second, internal-only reason: GC has no working form path
(`Form Submision [Landing Page]` 0/90d, `[TSD] Lead Form [LP]` 0 and not counted), so a page we
control is the only way to get a measurable form. Never tell the client a tag is broken.

**Conversion-action truth (verified 2026-07-31, corrects the 07-27 audit):** `Calls from ads [1]` is
a real connected call at a **15s** threshold, NOT a call-button click (the audit said click, it was
wrong). `First Time` / `Repeat Phone Call` are WEBSITE-origin at **60s**. So the Jul 28 goal rebuild
moved bidding from a 15s bar to a 60s bar plus the form, which is a lead-*quality* upgrade. Only
`[TSD] Website Call Link` (4 of 31 firings/90d) is a tel: tap. Don't repeat "call button."

**Weekly update format (first one shipped 2026-07-31, `GC-Home-Service-Weekly-Update_2026-07-31.*`
+ internal `weekly-log-2026-07-31.md`):** four numbered sections Edu specified — **1. What Changed**
(split Google Ads / Meta Ads), **2. Why It Changed** (tables + supporting data), **3. Expected
Impact** (what each fix should do + what we'll monitor), **4. Next Steps** (next week / monitoring /
waiting on you). PLAIN Word styling per [[tsd-client-report-plain-design]]. Goes to **Eve (AM)** for
review before it reaches the client.

**Baseline for next week's comparison (Jul 25–31):** Google $766.13 / 61 clicks / $12.56 CPC / 2
calls (vs Jul 18–24 $1,658.86 / 68 / $24.39 / 2). Post-change Jul 28–31 only: CPC $6.73, clicks 41.
Meta $1,249.18 total = lead gen $1,048.83 / 6 leads / $174.81 (paused Jul 30), hiring $146.03 / 9
applications / $16.23, awareness $54.32 / $0.68 recall. Meta creative read: **offer beats format** —
"$1,500 back on your quote" $47.16 CPL @ 2.67% CTR vs "$99 tune up" $432.52 @ 0.75%; campaign
lifetime $3,660.11 / 33 leads / $110.91. (Quote-back is 5 leads on $235, signal not benchmark.)

Committed to client: written update every Friday. The defining doc (*July Campaign Management, Budget Allocation & Lead Quality Review*) has never been provided to Claude — get it before client-facing output. Client version sanitized per [[topserv-client-report-format]] / [[tsd-client-facing-voice]].

**EXECUTED 2026-07-28** (log: `clients/gc-home-service/google-ads-log.md`): (1) **PMax budget $155 → $50/day** (`TSD_PMAX_Calls` 23511318927, budget 15337617979) — reverses the bleed; AM client-budget-change ticket still owed. (2) **Conversion goals rebuilt on both live campaigns** (PMax 23511318927 + Search Branded 23921909024): were bidding on ONLY `PHONE_CALL_LEAD/CALL_FROM_ADS` (call-button clicks); now `DEFAULT/WEBSITE` biddable (First Time Phone Call 13/90d + Repeat Phone Call 8/90d) + `QUALIFIED_LEAD/WEBSITE` biddable (Form), call-clicks OFF. Lever is `campaign_conversion_goal.biddable` (NOT `primary_for_goal`); False writes need explicit `FieldMask(paths=["biddable"])`. Verified by read-back. Repeat rides along (shares First Time's DEFAULT/WEBSITE bucket — can't split via goals without recategorizing First Time). **GC has ZERO ServiceTitan/upload-origin conversion actions** — unlike [[tsd-servicetitan-marketing-pro]] (MA), the ST→Google offline import was never built; that's the real fix. **Form Submision [Landing Page] fires 0/90d** (dead tag — verify it; it's the best signal and currently contributes nothing, so both campaigns are now in learning on ~13/90d). Open items in `tarefas.md` under "GC Home Service".

**2026-08-14:** PMax asset group final URL fixed (was pointed at an untracked GHL funnel page mislabeled "ServiceTitan booking," actually zero tracking of any kind) → redirected to the tracked `/gc-heating-and-cooling/` page. Also found + fixed: `SUBMIT_LEAD_FORM/WEBSITE` goal was never set biddable across the Jul 28 rebuild, so real lead-form conversions (confirmed Aug 13) were logging into `all_conversions` but showing 0 everywhere that mattered — fixed same day, all 3 live campaigns.

**Weekly update Aug 21 2026** (`GC-Home-Service-Weekly-Update_2026-08-21.*` + internal `weekly-log-2026-08-21.md`): headline is the **Yeti Giveaway Meta launch** — `CBO | YETI GIVEAWAY | 20 AUG`, $100/day CBO, broad 18–65+ M+F, Advantage+ on, 7 static ads, optimization "Leads," launched 2026-08-20 by **Jonathan Bannister — confirmed TSD-side, not external** (first read of the activity log wrongly took him for an outside/client actor; Edu corrected it — don't repeat that mistake). Same session paused `CBO | NEW CREATIVES | 8 JUL` (retired, replaced by Yeti) and one of two Awareness ad sets (`TOFU - Awareness - Ad Recall Lift`) — **the Awareness campaign itself stayed ACTIVE throughout**, delivering via its other ad set `08/06/2026 - ZIP Codes | Broad`; don't repeat "awareness paused," only one ad set of two was retired. Google: PMax's first full week on the tracked landing page took clicks 1,085→2,314 and blended CPC $0.90→$0.61 (Aug 8–14 vs Aug 15–20), but the standard `conversions` column is still 0 and PMax `search_impression_share` is still only ~12% — open question whether the cheaper clicks are genuine local intent or cheaper Display/Discover/YouTube inventory inside PMax; not verified, needs a network/placement breakdown. Real signal found via `all_conversions` (`st_conv_check.py customer_id`, a reusable generic script despite its Mission-Accomplished-sounding name): 55 `[TSD] Website Call Link` (tel-tap, non-biddable category) firings since the Aug 14 redirect vs 4 in the whole prior 90 days — but zero `First Time`/`Repeat Phone Call` or `[TSD] Lead Form [LP]` fills this week, i.e. the goal categories actually being bid on are still silent. Per Edu's instruction this week: client-facing copy never states a conversions figure (positive or zero), and week-over-week comparison tables get dropped when asked, not just reworded. **Chrome isn't installed on this machine** for the usual `--headless --print-to-pdf` recipe — use Playwright's bundled Chromium instead (same approach as `build_calendar_pdf.py`), and `open <path>` (macOS) reliably surfaces a built PDF to Edu when `SendUserFile` alone didn't.
