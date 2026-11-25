# Proud Pops — Google Ads log (1051843378)

---

## 2026-11-20 (later) — APPLIED: pricing sitelink swap + Elec AG2 RSA pause (Edu's go on the AT read)

Edu's answers 11-20: "segura plumbing por agr / pode trocar o sitelink / pode pausar mas coloca isso no log / hj ajustei isso ai e tirei o youtube partners, tudo certo / o budget planejado e 25k, entao ta no range". Script `clients/proud-pops/pp_apply_1120.py` (validated, then applied 2026-11-20 23:27 UTC, Gui via Claude). **Do not re-run --apply** (would create the sitelinks again).
- **'See Our Pricing' sitelink 360873861063 (/pricing) REMOVED from Electrical 23866999121 + Plumbing 23853484024** (14d: Elec $4,045 / 155 clk / 13 conv, Plumbing $1,466 / 97 / 0). Kept on Branded (9 conv / $511) and HVAC.
- Replaced by 2 NEW sitelinks (the account's service sitelinks are all automatically created and can't be linked): Electrical → `Electrical Repair` asset **441525652903** (/services/electrical/repair, "Breakers, wiring and outlets" / "Written price before any work"); Plumbing → `Drain Cleaning` asset **441598912395** (/services/plumbing/drain-cleaning, "Clogs, slow drains and backups" / "Written price before any work"). Both URLs in sitemap-services.xml; descriptions reuse claims from the approved RSAs. Read-back: Elec 6 sitelinks, Plumbing 4.
- **Elec AG2_Electrical_Services RSA 827482059113 PAUSED** (14d $549 / 0 conv); 809490621054 ($785 / 5) stays ENABLED. Read-back OK.
- **Not done:** EXACT [electrician] negative (not confirmed by Edu), Plumbing schedule/pause (Edu: hold for now). YouTube: Edu adjusted it himself 11-20 and removed video partners. Nov ~$23.5k is inside the planned $25k.
- At the new-site DNS switch: 200-check the 2 new sitelink URLs too (fu-178).
- Rollback: remove the 2 campaign_asset links, re-link 360873861063 on both campaigns, set 827482059113 ENABLED.

---

## 2026-11-20 — AT tasks (Gui, via Claude)

Read-only, nothing applied. Week 11-13..11-19 vs 11-06..11-12. Extra pulls: scratchpad `r1120/pp_x1120.py` + `pp_x1120b.py` (Nov MTD 4 accts, budgets, daily IS, conv by date, landing pages by campaign, sitelinks, AI Max, hours, calls, recs, YouTube networks), `pp_g14_digest.py`. Site check 11-20: proudpops.com still the Lovable build (GTM-WBFDB6L8 live v43), new-site draft ws 45 untouched. Changes since 11-16: only Edu's 11-16 08:05 budgets/negatives and 11-18 YouTube enable.

**7-Day Google (https://app.agencytitan.com/tasks/instance/f12fba76-88f0-46d2-89de-7dd0afbd1e27), completed.** Search only (YouTube $413.73 excluded): $4,403.22 / 247 clk / 21 conv / $209.68 CPL / $17.83 CPC / 8.50% (prior $4,601.10 / 17 / $270.65). Electrical $2,703.02 / 13 = $207.92 (prior $355.87; since the 11-16 cut to $375: $1,598.83 / 9 = $178), IS 42.4%, budget-lost back to 27.6%. Plumbing $723.74 / 56 clk / 0 (43% of it 19:00-06:59; since restore 1 real lead on $2,058.58). HVAC $586.27 / 2 (both 11-16 site calls) = $293, rank-lost 74%, Nov $1,535.50 / 3 tracked. Branded $390.19 / 6 = $65.03, IS 97.9%; 1 more uncounted Branded form 11-19. Branded 6 / $65.03, unbranded 15 / $267.54, Search IS 32.73%. 9 call-button calls (Elec 6, HVAC 2 under 60s, Branded 1), not transcribed (key on Edu's machine, CALL POP recording OFF). **New finding: 'See Our Pricing' sitelink (/pricing, all 4 campaigns) = $2,287.98 / 99 clk / 3 conv ($763) in 14 days** (Elec $1,630 / 54 / 3, Plumbing $539 / 35 / 0) vs /services/electrical $266/conv. Nov 1-19 $13,192.47 (PPC acct $12,678.82 incl. LSA $1,408 + YT $413.73; SA[1] $281.75; SA[2] $231.90; MFS $116.36 not counted) → lands ~$23.5k vs $25k. Staged: EXACT [electrician] neg (14d $329 / 6 / 0, 11-09 trigger met), cobalt electrical / ross electric / lentz plumbing to list 12263521315, swap the pricing sitelink on Elec + Plumbing, Plumbing ad schedule 07-19 or pause (Edu), HVAC = Edu at fu-172, Branded form goal, transcript pass. KPI Google row `f3e895fa` (Mixed).

**14-Day Google (https://app.agencytitan.com/tasks/instance/076b5eb3-b018-4282-9128-0e6e7848d460), completed.** 11-06..11-19 Search $9,004.32 / 477 clk / 38 conv ($237): Elec $5,548.69 / 21, Plumbing $1,755.89 / 3, HVAC $1,086.12 / 2, Branded $613.62 / 12. New Elec AG2 RSA 827482059113 $549 / 0 vs old 809490621054 $785 / 5 (staged pause). Expected CTR below on ~all nonbranded kws, ad relevance below on Electrician_NearMe. All Search spend in targeted geo. 0 audiences (staged observation). 78 open recs (reject partners/display/broad/PMax). At the DNS switch: 200-check every final + sitelink URL on the new site. All 8 items ticked.

**LSA, 7-Day (https://app.agencytitan.com/tasks/instance/332a77e6-d30f-4a45-93f0-3bd2f1fc0823), completed.** 3 sources: main $660.62 (9 charged: 7 plumber msgs all NEW, 2 HVAC calls) + electrician $84.28 (1 call) + HVAC $0 (2 calls not charged) = $744.90 / 12 leads / 10 charged = $74.49 (prior $1,023.45 / 14 charged / $73.10). Top impr 96.03%, impr 798 vs 656. Underspending vs $714.29 x3 fields (not the limit). No PPL-PMax migration. Rating = fu-161, not done. KPI LSA row `7b21338e`.

**YouTube, 7-Day (https://app.agencytitan.com/tasks/instance/eeff1bd6-6d2a-4ffb-ba8f-a4d09ed35a74), completed (not N/A: restarted 11-18).** 2 days: SA $208.27 / 12,957 impr / 7,953 views (61% view rate, CPV $0.026, completion 60%), 100% YouTube; ads: Breaker Tripping + Surge best, Repair vs Replace weakest (27% completion). NB $205.46 / 6,798 impr / 6,290 views (CPV $0.033, completion 86%) but **99% of NB spend is reported on the Content network = TV apps** (Samsung TV Plus $75, Vizio WatchFree $25, Tubi, Pluto, Roku) although the API shows video partners off, and 95% on one ad (Breaker Tripping). SA placements include gaming streams (GTA 6 x3) and a Spanish reality live stream, small $. Both ~$100/day on budget, 0 conv (awareness). Staged: check NB's TV-app inventory in the UI and decide if CTV is wanted; SA gaming/live-stream exclusions if it grows. All 7 items ticked (task has no notes field).

**Meta, 7-Day:** N/A, see meta-ads-log.md (KPI Meta row `62a91857`).

---

## 2026-11-18 — YouTube RESTARTED (Edu's go: "we gotta restart YouTube Ads for them")

Context: client video audit for Ryan (Proud Pops = biggest spender with zero video live since the 10-16 cut).
- Pacing before the change: Nov MTD ≈ $11,990 (PPC acct $11,475.85 incl. in-acct LSA $1,343; LSA 7261668241 $281.75; 6621969129 $231.90). Search + LSA pace ≈ $680/d → ~$20.5k projected, so ~$4.5k room under the $25k cap (same gap flagged 11-11, option 3).
- **Both VIDEO campaigns ENABLED via the Google Ads UI** (API still returns MUTATE_NOT_ALLOWED on VIDEO status, validated first): `08/2026 - YT - VideoViews (San Antonio)` 24120440530 and `08/2026 - YT - Awareness - New Braunfels` 24120482524, budgets unchanged $100/d each, Target CPV. API read-back: ENABLED / ELIGIBLE. 8 video responsive ads (Repair vs Replace, Panel Replacement, Breaker Tripping, Surge Protection x2 geos) all APPROVED.
- Adds ≈ $2.5k for Nov 19–30 → month lands ≈ $23k, under $25k.
- Last active month (09-16..10-16): SA $3,014 / 349k impr / 231k views / 20 clicks; NB $3,033 / 200k impr / 151k views / 137 clicks. SA kids-content exclusions from 10-08 (H5a) stay on.
- **Open:** check day-1 delivery + placements 11-19/20 (SA kids inventory), and pacing vs $25k on ~11-24.

---

## 2026-11-17 — New site launch prep (Alex's platform replaces Lovable): GTM draft, keys, Slack replies

Alex's two asks in C0CJ3B859DM (p1794934763282159, p1794955039931059). Johnny answered the office side (forms → GHL + support@ email, GoDaddy = Daniel, switch today once the test passes) and confirmed (210) 864-6867 = CallRail "1st Repair is on Pops Letters" tracker on /first-repair, G-C7QTE9ZZXQ = Proud Pops stream, pixel 597145242772352.
- **GTM-WBFDB6L8 DRAFT, Default Workspace 45, NOT published** (live stays v43). Scripts in google-ads-ratos/scripts: `proud_pops_gtm_dump_1117.py`, `proud_pops_gtm_launch_draft_1117.py` + `_finish.py` (finish = 429 quota retry on tag 104). Compiles clean.
  - New trigger 133 `cEvent - lead_submitted (site forms)` (/careers excluded) → G.Ads - Lead (82), G.Ads - User-provided Data (94), Meta - Lead (111).
  - Meta - Lead eventId = `{{dlv - event_id}}`; advanced matching via new cJS Lead Email/Phone/First/Last (Concrete v4 pattern).
  - GA4 - Lead (90) NOT on lead_submitted: Alex's server sends generate_lead via Measurement Protocol. GHL widgets keep ghl_form_submit unchanged.
  - Meta tags 68/71/102/111/112/114 + CallRail 104 → require ad_storage.
  - **Publish only at the DNS switch** (Lovable defaults consent to denied, would cut Meta on the old site). fu-178.
- **Cowork (Edu's login):** GA4 MP secret created on G-C7QTE9ZZXQ ("Alex site launch 2026-11-17"); CAPI token generated (without Dataset Quality API, opt-in is irreversible and pre-selected 5 datasets); Meta Test Events code **TEST92292**; GA4 Internal Traffic filter was already Testing. Internal-traffic IP rule (45.225.171.108) saved UNPUBLISHED in the GA4 Google tag container GTM 6228503454 / 183775598 ws 3 (its only change), publish after Alex's IPs are added. Pixel is named "New Problem Solver Pixel", 1 open Diagnostics item.
- **Slack sent (Edu's go):** thread reply to Alex p1794958740203489 (test code, GTM summary, publish at switch, asks: his IPs, MP only for site forms?, email/phone dataLayer keys, test time) + follow-up p1794958987070289 (pixel name, no Quality API, diagnostics, GA4 tag rule, token rotation). MP secret + CAPI token sent by **Slack DM to Alex** (Edu chose DM; Johnny had asked for project settings) → rotate token after launch, fu-179.
- No Google Ads changes.

## 2026-11-16 (later) — APPLIED: Electrical $455 → $375, Plumbing $145 → $75, 8 PHRASE negatives (Edu's go after the re-read, fu-137)

`fixes_2026-11-16.py`, validate-only then `--apply` at 14:05 UTC, one atomic mutate, read-back OK:
- Electrical 23866999121 budget $455 → **$375/day** (undo the 11-09 raise). Campaign PHRASE negatives: mechanic, circuit board, gate opener, independent, cheap (63 → 68).
- Plumbing 23853484024 budget $145 → **$75/day**, all ad groups kept (General produced the real lead + the form). Negative: pops (16 → 17).
- HVAC 23848895678 unchanged at $230 / $30 ceiling. Negatives: pops, corporation (27 → 29).
- Replay 11-02..11-15: blocked terms had 0 conversions ('electrical mechanic near me' $138, 'pops ac' $32, 'independent electricians' $44, 'cheap electricians near me' $39, 'carrier corporation' $28, circuit board x2 $37).
- Search caps now $730/day (Branded $50 + Elec $375 + HVAC $230 + Plumb $75), was $880. November still lands under the $25k cap.
- Next read fu-172 11-23: Electrical CPL and IS at $375, Plumbing on $75, HVAC volume under the ceiling.
- **AM note = AT Internal Request DRAFT `4cde0fdd-2f03-43f9-a6c3-5ba0e93856a9`** "Google Ads update: Electrical and Plumbing budgets cut, keyword cleanup" (https://app.agencytitan.com/tasks/instance/4cde0fdd-2f03-43f9-a6c3-5ba0e93856a9), created via API 14:07 UTC, left in Intake for Edu to submit. Intake = Edu, Execution = Angela, Review & Close = Edu. Content: the 4 changes above + the two questions that decide the next step (same-day electrical capacity: 3 of 4 reviewed callers wanted same-day and didn't get it; night phones: Nonbranded 19–07 $575 / 1 lead this week), next read 11-23. The fu-157 asks (recording, weekends, text sequence, $299 fee) were never drafted in AT; they sit in the review task's notes, which Angela reads for today's 11:00 CT call.

---

## 2026-11-16 — fu-137: one-week read of the 11-09 fixes (11-10..11-15 vs 11-04..11-08), read-only, nothing changed

`pp_week.py` (scratchpad) + CallRail transcripts (`_pessoal/call-wins/proud-pops-1116/`). Search total after: $3,997.59 / 6 days.

| Campaign | Before 11-04..11-08 (5d) | After 11-10..11-15 (6d) |
|---|---|---|
| Electrical ($455) | $1,714 ($343/d), 8 conv, CPC $27.21, IS 34%, budget-lost 38% | $2,537 ($423/d), 8 conv, CPC $26.70, IS 57%, budget-lost 13% |
| Plumbing ($145) | $768, 0 conv | $893, 2 conv (1 real) |
| HVAC ($230, $30 ceiling) | $751 ($150/d), CPC $34.15, 1 conv, rank-lost 50% | $295 ($49/d), CPC $19.64, 0 conv, rank-lost 78% |
| Branded ($50) | $34, CPC $2.61, IS 55% | $273 ($45/d), CPC $7.80, IS 78%, 3 conv |

**Electrical:** 8 Google leads = generator inlet (booked 11-16), breaker swap (open, waiting on a cancellation), smoke detectors (lost, next slot Tuesday), 2 unrecorded call-button calls, 3 forms. Plus a repeat caller 11-15 (refrigerator outlet sparking, same day = $200 fee, lost). **Cost per lead ~$317 vs $214** before: the extra budget bought volume (IS 34→57%) at a worse rate. Electrical_Services ad group $631 / 26 clk / 2 = $315 (was $410, fix worked). **New leak: AG3_Electrical_Repair** $987 / 37 clk / 2; bare `electrical repair` [PHRASE] $765 / 28 clk / 1 conv; visible terms incl. 'electrical mechanic near me' $138 / 2 clk, 'independent electricians' $44, 'circuit board repair near me' $20, 'gate opener circuit board repair' $18, 'cheap electricians near me' $39 (Services). It also caught 'same day electrician' $79 → 1 lead. Geo twin `electrical repair san antonio` $217 / 8 / 1.
**Capacity:** 2 of 4 reviewed Electrical callers this week lost to availability. More Electrical spend partly buys calls the office can't serve this week.

**Plumbing:** fix worked as designed: Leak Detection $465 → $72; generic searches now serve from General (`plumber san antonio tx` $548 / 36 clk / 1 conv). 2 Google leads = 11-10 job seeker + 11-12 water heater leak (booked, $0 Pop-In 11-13). Since the 11-04 restore: **$1,661 / 1 real lead**. Water Heaters ad group $192 / 1 conv carries it.

**HVAC:** ceiling worked on price (CPC $34 → $19.64) but choked volume ($150/d → $49/d of $230, rank-lost 78%). 0 leads on $295 (before: 1 on $751). Junk seen: 'pops ac' $32 (brand intent on Nonbranded), 'carrier corporation san antonio tx' $28.

**Branded:** spend up to $45/d (CPC $7.80, Brand_HVAC 'proud pops hvac' exact $113 / 10 clk / 0 conv at ~$11). 3 Google leads = 11-12 Power Home (admin, not counted) + 2 unrecorded call-button calls.

**Night (Nonbranded 19:00–06:59):** $575 / 37 clk / 1 conv (15% of spend, 10% of leads). Still waiting on the AM's answer about night phone coverage (fu-157).

**Re-read (Edu asked, same day) — two of the first proposals were wrong:**
- Pausing bare `electrical repair` would move the leak, not fix it: that is exactly what happened on 11-09 (Services −$190, Repair +$660). Electrical is Max Conversions with NO target and budget-lost fell 38% → 13%, so Google spends the whole $455 on whatever matches; the marginal clicks are the loose ones. The keyword also caught 'same day electrician' → a real lead. Lever = budget (or a tCPA), not the keyword.
- Plumbing: General produced the only real lead (11-12 water heater, First Time Phone Call on AG4) AND the 11-09 form; the Water Heaters conv on 11-10 was the job seeker. So General stays. Plumbing is Max Clicks (TARGET_SPEND) on generic plumber terms = buys the cheapest clicks; with 2 leads in 12 days there is nothing for Max Conv to learn from, so the budget is the lever.
- Of the 4 Electrical callers read this week: 1 booked (generator, non-urgent estimate), 3 wanted same-day and didn't get it (Tuesday wait, waiting on a cancellation, $200 same-day fee). Volume is not the limit.
- Brand negatives: 'proud pops' PHRASE on all 3 Nonbranded, but 'pops ac' only on Electrical, so 'pops ac' $32 served on HVAC.

**Proposed, NOT applied (Edu's go), revised:**
1. Electrical $455 → $375/day (undo the 11-09 raise: it bought $80/day of looser matches and 0 extra leads while the office loses same-day callers). Alternative if Edu wants to keep the cap: tCPA ~$220 on the campaign. Plus campaign PHRASE negatives 'mechanic', 'circuit board', 'gate opener', 'independent', 'cheap'. Keep `electrical repair`.
2. Plumbing $145 → $75/day, all ad groups kept (General stays: it is the one that produces). LSA carries plumbing (8 of 14 LSA messages this cycle were plumber category).
3. HVAC: keep the $30 ceiling; add PHRASE negative 'pops' on HVAC + Plumbing and 'corporation' on HVAC. Structural issue for later: no heating ad group, so HVAC bids on AC terms in November.
4. AM (fu-157): same-day electrical capacity + night phones (Nonbranded 19–07 = $575 / 37 clk / 1 conv this week).

---

## 2026-11-16 — Oct Review FINAL: KPI row refreshed with the full cycle (10-16..11-14), fu-156

- Row 73060891: ad_spend **$11,572.19**, total $16,572.19, qualified_leads **55 verified** (72 tracked; 52 new + 3 existing customers), cpl **$210.40**, rec $25k, budget_rationale rewritten. Task fc4041bd `additional_paid_ads_notes` rewritten (FINAL). Read back OK. Call 11-16 11:00 CT.
- Delta 11-11..11-14: $3,533.93 (Electrical $2,018 / CPC $29.68, Plumbing $645, LSA in-account $380, HVAC $240, Branded $194, electrician LSA $58). Google real-lead conv: Electrical 6, Branded 2, Plumbing 1.
- Calls came straight from CallRail with `fields=transcription` (no whisper). Plumbing's first real call: 11-12 water heater, booked. Nov 9 radio caller booked (tech late, customer asked for a manager). Smoke-detector caller lost on a Tuesday wait.
- LSA delta 8: 1 booked (2 toilets 11-16), 5 open, 2 not leads (spam; electrician lead 351353602 Christmas lights, CHARGED → rate bad, added to fu-161).
- Detail: strategy-review-octnov-2026.md (2026-11-16 section), call-wins-log.md, lsa-call-wins-log.md.
## 2026-11-16 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied. Week 11-09..11-15 vs 11-02..11-08. Extra pull: scratchpad `r1116/pp/pp_x1116.py` (current budgets, change_event 11-09..11-16 with old/new, portfolio, Nov MTD 4 accounts, conv by date, daily IS, ad groups, hours).

**Edu's 11-16 08:05 CT changes (change_event, after the window, not yet logged here):** Electrical budget $455 → $375, Plumbing $145 → $75; PHRASE negatives Electrical mechanic / circuit board / gate opener / independent / cheap, HVAC pops / corporation, Plumbing pops. Search caps now $730/d. Nothing else changed 11-09 09:00 → 11-15.

**7-Day Google (https://app.agencytitan.com/tasks/instance/68af7f2e-b794-4c42-b48d-fe2400648fe8), completed.** $4,672.94 / 230 clk / 17 conv / $274.99 CPL / $20.32 CPC / 7.39% (taps + repeat calls in all_conv only; 17 = new-caller calls 60s+ and forms). Electrical $3,020.42 / 9 ($336, was $214; Repair ad group $527/conv), Plumbing $980.63 / 3 (first since restore, but the 11-10 call = job seeker per the 11-11 review), HVAC $368.32 / 0 (rank-lost 79%, ~$53/d of $230, AC Repair 2 clicks), Branded $303.57 / 5 ($60.75; Target IS reached, 100% IS from 11-11, abs-top 76-96%). Branded 5 / $60.75, unbranded 12 / $364.22, IS 34.8%. Nights 19-07 $259/conv vs day $278 (not worse). Competitor terms $66.50 (zimmermann, lentz, casanova, apc, classic electric, elevated electrical). Nov 1-15 $9,549.80 (3 accts; MFS $116.36 not counted) → ~$19.5-20k at the new caps vs $25k. Staged: EXACT [electrician] neg, competitor names to list 12263521315, HVAC heating ad group or pause (Edu), Plumbing hold $75, re-read Electrical_Repair terms, transcript pass on 6 ad calls 60s+, AM pacing number ~$19.5-20k. Transcripts not checked (Proud Pops CallRail key is on Edu's machine). KPI Google row `e1e1c532` (Mixed).

**LSA, 7-Day (https://app.agencytitan.com/tasks/instance/26822e92-516d-425f-be78-ecd421181950), completed.** 3 sources: main $650.70 + electrician $57.59 + HVAC $120.16 = $828.45 (prior $477.56) / 13 leads (2 calls, 11 msgs), 12 charged = $69.04 (prior $79.59). Main-profile messages 2 → 11 (9 plumber). 1 BOOKED, 3 ACTIVE, 9 NEW. Top impr 97.5% (prior 92.8%), impr 706 vs 722. Budget fields $714.29 x3 = Underspending, not the limit. No PMax migration on any of the 3. Rating = fu-161 (not done); spam 351579426 not charged. KPI LSA row `a0283cbd` (lead_quality had to go in as a list ["Good"]; plain string now rejected).

**YouTube, 7-Day (https://app.agencytitan.com/tasks/instance/9a2ac66c-9010-4e9c-963b-d746108b465e), completed as N/A.** Both YouTube campaigns (24120440530, 24120482524) still PAUSED, $0 / 0 impr both weeks; PMax paused too. All 7 items ticked.

**Meta, 7-Day:** N/A, see meta-ads-log.md (KPI Meta row `b28be850`).

---

## 2026-11-11 (later 2) — Oct Review call transcripts: 22 Search-ad calls + 17 LSA calls reviewed, KPI row re-based to verified leads

Edu asked for the review with transcripts. CallRail access: Edu created an API key in the Proud Pops CallRail account (533-681-324) → `.env.callrail.proudpops`. That account has Conversation Intelligence ON, so `fields=transcription` returns speaker-labeled text (no whisper needed; the `recording` field is a pointer JSON, fetch its `url` without auth). LSA calls pulled with `pull_lsa.py` per account and transcribed locally. Recording is OFF on the "210 - CALL POP" tracker (the ad call button), so the 5 call-button calls can't be reviewed.
- **Search-ad calls (22 recorded of 27):** 9 booked new jobs, 3 existing-customer service calls, 4 open, 6 not leads (2 job seekers, other company's HR call, internal forwarding test, document request, Saturday voicemail). Electrical 7 calls = 4 booked + 3 open, 0 junk. Plumbing's 11-10 "first lead" = job seeker. Branded 13 = 4 new + 3 existing + 1 open + 5 non-leads. Capacity lost 3 real callers (6-day wait, full day, Saturday 5 pm voicemail). Log: `call-wins-log.md`.
- **LSA (21 non-declined):** 3 booked (11-04 tub faucet, 11-06 P-trap + WH, 11-06 duct cleaning), 10 open real requests, 8 not customer requests. Google BOOKED wrong on 1 of 3; 2 charged leads are dispute candidates (10-29 outside area, 10-18 39s greeting only). Weekend fees ($120 Sat / $500 Sun) ended both weekend electrician leads. Electrician profile 0 booked on 4 charged. Log: `lsa-call-wins-log.md`.
- **Verified: 38 leads, $211.53** (was 55 / $146.15). Search $259.94 (25), LSA $114.30 (13). 12 jobs confirmed booked on the recorded calls. Stretch split flips: Branded-only 10-16..11-03 = 12 verified of 26 ($224); restored 11-04..11-10 = 26 of 29 ($206, 7 booked). KPI row 73060891 updated (qualified_leads 38, cpl 211.53), task notes rewritten, PDF rebuilt with a call-review section. AM asks in Command Center fu-157.
- Lesson: on Proud Pops, duration + first-time filters keep 60% real opportunities on Search calls (best in the book) but only ~60% on LSA; always run the transcript pass before quoting a CPL to the client.

---

## 2026-11-11 (later) — AT Client Strategy Review "Oct Review" (cycle 10-16..11-14): KPI row + task notes WRITTEN (Edu's go)

AT task `fc4041bd-72c3-4bad-84c0-84db5839bb06` (created by Angela 11-11; the 10-02..10-31 task 4ae4f4a8 is gone from AT). Pull: `strategy_review_pull_2026-11-11.py` (3 Google accounts) + GA4 438523825 + the CallRail export in ~/Downloads (10-14..11-03). Data through 11-10, 11-11 partial. Detail + method: `strategy-review-octnov-2026.md`.
- **Client Performance KPIs record `73060891-c33c-44c8-8f35-53178eeb58b1`** on the client field (relationship f619cda1): 2026-10-16..2026-11-14, ad_spend **$8,038.27** (Google Ads $6,552.43 + LSA $1,485.84), agency_fees $5,000 (carried from the 10-02 row, which the AM filled after 11-05), total_spend $13,038.27, qualified_leads **55** (7 forms, 27 calls, 21 LSA), cpl **$146.15**, recommend_budget $25,000.
- Task field `additional_paid_ads_notes` filled with the full breakdown, the changes this cycle, pacing (~$20.6k vs $25k) and the open items for the call (commercial jobs, night hours, CallRail pool, unmarked LSA leads).
- Split: 10-16..11-03 Branded only $2,685.01 / 26 leads ($103); 11-04..11-10 restored $5,353.26 / 29 ($185). Google Ads $193/lead, LSA $71/lead. My Favorite Service ($457) not included.
- Stage: by the time of the write the task was already in **Host Review Call** (Angela, call item 1 checked), so Performance Reporting was not completed by Paid. Slack overview drafted for Angela in the 11-05 format.
- **Client PDF report built 11-11:** `Proud Pops - Performance Report (Oct 16 - Nov 10).pdf` (4 pages, plain Times format like the Oct 7 report; source `Proud-Pops-Google-Ads-Performance-Report_2026-10-16_11-10.html`, rendered with Playwright Chromium because Chrome is not installed, Brave headless hangs). Sections: at a glance, two stretches, Search by campaign, phone calls, LSA by profile, what we worked on, budget and pacing, what's next. Client framing per topserv-client-report-format. NOT attached to the AT task yet: the Drive upload needed for `cloud_files_import` was blocked by the permission classifier, and the Client Strategy Review process has no file field anyway (list_fields 11-11), so it would go in as a task attachment.
⚑ Refresh the row after 11-14 with the full cycle (Command Center follow-up fu-156).

---

## 2026-11-11 — fu-054 pacing check + first days after the 11-09 fixes (read-only, nothing changed)

`pacing_check_2026-11-11.py`. 11-11 had no spend posted yet, so data runs through 11-10. 11-10 is the only full day after the 11-09 fixes, so treat everything below as an early read. The full one-week read is still fu-137 on 11-16.

**Pacing: November lands ≈ $20.6k vs $25k (about $4.4k short, ≈ $220/day).**
- MTD 11-01..11-10, 3 accounts: **$5,715.68** (PPC $5,343.90 incl. its LSA, SA [1] $139.88, SA [2] $231.90). My Favorite Service ($118.09, Smart campaign paused 11-09, $0.79 after) not counted.
- Run rate since the restore: weekdays ~$805/day (910, 733, 833, 810, 738), weekends ~$479/day, separate LSA accounts ~$37/day. 20 days left (14 weekdays, 6 weekend days). Thanksgiving 11-26/27 will probably come in lower, so it lands around $20–20.6k.
- Why the 11-09 projection of $22.5k didn't hold: Electrical did not take the extra $80 (11-10 $345 of $455, 0 budget-lost that day, 41% rank-lost), and the HVAC $30 ceiling cut HVAC from ~$150/day to ~$61/day.

**By campaign, 11-10 vs the 11-04..11-08 baseline:**

| Campaign | Budget | 11-10 spend | CPC | Real leads 11-09..10 | IS 11-10 | Lost to rank | Baseline 11-04..08 |
|---|---|---|---|---|---|---|---|
| Electrical (Max Conv) | $455 | $345.42 (11-09 $484) | $21.59 | 3 (2 first-time calls, 1 form) on $829 = $276 | 59% | 41% | $343/d, $214/lead |
| Plumbing (Max Clicks $45) | $145 | $156.49 | $14.23 | **2 (1 first-time call, 1 form) = first leads since restore**, $122 each | 35% | 65% | $154/d, 0 leads |
| Branded (Target IS, $18 ceiling) | $50 | **$49.75 = at the cap** | $6.22 | 3 ads calls (154–179s) | 60% (abs-top 60%) | 40% | $7/d |
| HVAC (portfolio, $30 ceiling, tCPA $265) | $230 | $48.90 | $24.45 | 0 | 21% | 79% | $150/d, $751/lead |

- **Nothing broke.** All 5 enabled campaigns are serving, and the portfolio 12308461252 reads ENABLED, $30 ceiling, tCPA $265. Taps sit in all_conversions only. HVAC primary status says BUDGET_CONSTRAINED, but it spends ~$60 of $230, so the status is lagging.
- **HVAC is effectively throttled by the ceiling:** 5 clicks in 2 days, all in AG3_HVAC_Maintenance. AG1_HVAC_ACRepair gets 23–25 impressions per day and 0 clicks. Terms: 'goodman hvac service near me' $52 / 2 clicks, 'hvac places near me', 'hvac companies', 'zimmermann ac' (probably a competitor). Working as intended (no $53 clicks), but it is no longer a place to put money.
- **Plumbing fix worked:** AG4_Plumbing_General now gets the generic plumber traffic (164 impr / 7 clicks 11-10..11), and Leak Detection dropped to 2 impressions. Water Heaters produced the lead.
- **Branded CPC is climbing as Target IS learns:** $0.27 → $0.48 → $2.79 → $5.11 → $6.22 (11-06..11-10), and abs-top went 15% → 60%. It still shows LEARNING_NEW. 11-10 hit the $50 budget exactly. The 3 ads calls since 11-09 came from area codes 818, 206 and 361, all outside San Antonio (they could be cell phones). Transcribe them before counting them as new customers.
- **LSA:** none of the 3 accounts has migrated to Pay-per-lead PMax yet. The PPC-account LSA spent ~$135/day on 11-09/10 (4 charged message leads, 3 plumber, all status NEW). SA [2] HVAC got 1 charged call on 11-09 (ACTIVE). SA [1] has no leads since 11-08.

**Where the gap could go (Edu's call; the client's $25k cap stays the ceiling, so all of these are within approval):**
1. **Branded $50 → $75**, taken from HVAC ($230 → $205; HVAC spends ~$60 under the ceiling, so this costs it nothing). Total caps stay at $880. Keeps the best source from capping out while Target IS climbs to abs-top.
2. Electrical is mostly rank-limited now, so a bigger budget adds little. Plumbing is rank-limited (0 budget-lost). HVAC is held back by the ceiling on purpose. **Search can't absorb about $220/day more at a sane cost per lead.**
3. To spend the rest: YouTube awareness (SA/New Braunfels Video campaigns, paused since fu-046) for ~$150/day for the remaining weeks (~$3k), which fits brand-first. Otherwise accept ≈ $20.5–21k and tell the AM why (Search is capped by rank, not budget, and we would rather not buy bad clicks).
- The AM update promised in AT d2b5e325 (Nov 9 Branded check + Nov 11 pacing) is owed now.

---

## 2026-11-09 (later 4) — APPLIED: keyword pauses, negatives, HVAC $30 CPC ceiling, My Favorite Service Smart campaign paused (Edu: "Apply all of the fixes, including the My Favorite Service")

`fixes_2026-11-09.py`, validate-only then `--apply` (~08:50 CT), read-back OK on every item.

1. **Electrical 23866999121:** `electrical services` [PHRASE] (criterion 95420911, AG2_Electrical_Services) **PAUSED**; the EXACT twin and the geo versions stay. Campaign negatives PHRASE **'electric company', 'aep', 'hourly rate'** (63 total now).
2. **Plumbing 23853484024:** generic plumber keywords **PAUSED in AG1_Plumbing_LeakDetection**: `plumber san antonio tx` [PHRASE] 354371636767, `plumber near me` [EXACT] 21810437552, `plumber san antonio` [EXACT] 1178376016 (third one not in the original proposal: same duplicate, $0 in the window). AG4_Plumbing_General keeps all three ENABLED. Leak Detection keeps 4 keywords (emergency plumber san antonio, leak detection san antonio, burst pipe repair san antonio, water leak repair san antonio). Campaign negatives PHRASE **'cheap', 'saws'** (16 total).
3. **HVAC 23848895678:** campaign negative PHRASE **'cheapest'** (27 total). Bidding moved from standard Max Conversions to portfolio **'TSD_ProudPops_HVAC_MaxConv_CPC30'** (12308461252): Max Conversions, **max CPC ceiling $30**, tCPA $265 carried over unchanged. ⚠ HVAC was NOT uncapped Max Conversions as the earlier entries say: it already had a **$265 tCPA**, which is why it bid $53 a click. Status after: LIMITED (BUDGET_CONSTRAINED).
4. **Account-level list 12263521315** (+16 PHRASE, 82 total): mesa electrical, enterprise electrical, 1 tom plumber, venture plumbing, amg plumbing, leaky's plumbing, leakys plumbing, benchmark plumbing, bearded plumber, cowboys heating, ems hvac, westerly air, my father's ac, my fathers ac, gillette ac, apollo air.
5. **My Favorite Service 9815330464:** Smart campaign 'HVAC Contractor Services' 23065942452 **PAUSED**.

**Replay against 09-01..11-09 search terms (what the new negatives would have blocked):** 'electric company' 25 clicks / $585.47 / 11 conversions, **all 11 = 'TSD - Website Call' taps before 11-04**, no verified lead (terms are mostly '<name> electric company' and utility lookups like 'bexar electric company'); 'cheapest' (HVAC) 3 clicks / **$294.23** / 1 tap; 'bearded plumber' 4 clicks / $74.91; 'cowboys heating' $93.85; 'mesa electrical' $71.01; '1 tom plumber' $49.24; rest under $35 each, 0 conversions.

**HELD (not applied): 'commercial' negative on Electrical + HVAC.** proudpops.com says "Residential & Commercial" on the homepage and on the HVAC ad landing page ("From cozy bungalows to busy storefronts"). It would block a service the client advertises. Evidence against it is 2 clicks ('commercial ac repair san antonio' $126.00, 'electrical companies commercial' $68.97), and the $30 ceiling now limits that kind of click on HVAC. Edu/AM to decide whether the client wants commercial leads.

**My Favorite Service, fuller picture:** last 30 days the Smart campaign spent $574.11 for 1,178 clicks and recorded **5 phone conversions** (4 'Business profile - Tracked call', 1 'Calls from Smart Campaign Ads'; last one 10-26), plus 36 untracked 'Business profile - Call'. Nothing in the 14 days before the pause ($225). Re-enable = status back to ENABLED. Still **ENABLED but not serving** in that account: Search_AC_Replacement, Search_Duct_Cleaning, Search_Air_Quality_Service, Search_AC_Repairs (primary NOT_ELIGIBLE, $50–150/day budgets), Pmax_AC Repair & Replacement (primary PENDING, $160/day), and one ended experiment campaign (can't be changed via API). Not touched.

**Not touched, noticed:** `emergency plumber san antonio` [PHRASE] also sits in Leak Detection (the Emergency ad group has the EXACT). Plumbing is Max Clicks with a **$45** CPC ceiling.

⚑ One-week read fu-137 on 11-16 (Electrical cost/lead vs $214, Plumbing first lead?, HVAC CPC under $30 and volume). Pacing fu-054 on 11-11.

---

## 2026-11-09 (later 3) — Keyword-level read, 11-04..11-09: three leaks + proposed fixes (read-only, NOT applied, Edu's go)

**1. Electrical: `electrical services` [PHRASE, no city], AG2_Electrical_Services = $460.64 / 14 clicks / 0 leads.** Biggest waster in the best campaign, and the reason that ad group runs $410/lead. Its terms lean utility/commercial: 'electric company san antonio' $96.08 / 3 clicks, 'electrical companies commercial' $68.97, 'aep pleasanton tx' $30.67, 'best electric company in san antonio' $23.05; plus 'mesa electrical contractors' $71.01 (Repair). Keywords that did produce leads: electrician san antonio, electrician near me, electrical services san antonio, home electrical services, electrical repair, affordable electrician near me, electrician san antonio tx (1 each).
   Proposed: pause the bare `electrical services` phrase (the geo twin stays); negatives PHRASE 'electric company', 'commercial', 'aep', 'mesa electrical', 'enterprise electrical', 'hourly rate'. Matters more now that Electrical has +$80/day.

**2. Plumbing: generic plumber keywords live in the Leak Detection ad group.** `plumber san antonio tx` [PHRASE] $390.01 / 18 clicks + `plumber near me` [EXACT] $64.16 / 3 clicks, both in AG1_Plumbing_LeakDetection = **$454 of the campaign's $806**, 0 leads. AG4_Plumbing_General has the same two keywords ($105.54). So a generic plumber search gets a leak detection ad. QS 3–5 across the campaign.
   Proposed: pause those two keywords in the Leak Detection ad group (General keeps them); negatives PHRASE 'cheap', '1 tom plumber', 'venture plumbing', 'amg plumbing', 'leaky's plumbing', 'benchmark plumbing', 'bearded plumber', 'saws' (water utility).

**3. HVAC: `ac repair san antonio tx` [PHRASE] = $428.13 / 8 clicks at $53.52 / 0 leads** (QS 5, 47% lost to rank). Visible terms: 'commercial ac repair san antonio' $126.00 for 1 click, 'cowboys heating and air san antonio' $93.85 / 2, 'cheapest ac repair san antonio' $46.51. Competitor names with impressions and no negative yet: ems hvac, westerly air, my father's ac & heating, gillette ac, apollo air. Only 5 of 22 HVAC clicks show a search term. No heating/furnace ad group exists (AC Repair, Installation, Maintenance only).
   Proposed: negatives PHRASE 'commercial', 'cheapest', 'cowboys heating', 'ems hvac', 'westerly air', 'my father's', 'gillette', 'apollo air' (competitor names → the account-level list from 10-16); CPC ceiling ~$30 on HVAC via a portfolio Max Conversions strategy (same route as Hawkins). 1 conversion in 5 days, so little learning to lose.

**Also seen:**
- No ad schedule on any Search campaign. Nonbranded 19:00–06:59 = $451 / 24 clicks / 0 leads; 07:00–18:59 = $2,784 / 99 clicks / 9 leads. 5 days only: ask the AM whether phones are answered at night before cutting.
- LSA last 30 days (10-10..11-09): PPC-account LSA 10 leads / 7 charged / $535 (statuses used: 3 BOOKED, 2 DECLINED, 1 CONSUMER_DECLINED); **SA [1] 5 leads and SA [2] 6 leads all still ACTIVE = never marked**. All three budgets $714/day, spend $9–18/day: reach-limited, not budget-limited.
- My Favorite Service Smart campaign: $100.58 in 11-02..11-08, 0 conversions.
- AT request d2b5e325 ("Google Ads upadte", typo in the title) was submitted 11-06 and is in Execution with the AM. It promises a Nov 9 Branded check and a Nov 11 pacing check: one combined AM update after 11-11.

---

## 2026-11-09 (later 2) — Overview of all accounts since the 11-04 restore (read-only)

`overview_since_restore_2026-11-09.py`. Window 11-04..11-08 (5 full days). "Real leads" = the Conversions column since 11-04 (First Time Phone Call via CallRail, Calls from ads 60s, Website lead) minus the 1 Branded tap that still counted on the morning of 11-04, plus charged LSA leads.

**Total, 3 accounts: $3,685.99, 15 real leads, ~$246 each.** Search $3,268.03 / 10 leads (~$327). LSA $417.96 / 5 charged leads (~$84).

| Campaign / surface | Spend | Clicks | CPC | Real leads | Cost/lead | Lost to budget | Lost to rank |
|---|---|---|---|---|---|---|---|
| Search Nonbranded Electrical | $1,714.36 | 63 | $27.21 | 8 (4 first-time calls, 2 ad calls 60s+, 2 forms) | $214 | 38% | 28% |
| Search Nonbranded Plumbing | $768.27 | 38 | $20.22 | 0 (0 in all_conversions too) | – | 28% | 46% |
| Search Nonbranded HVAC | $751.41 | 22 | $34.15 | 1 (first-time call) | $751 | 23% | 50% |
| Search Branded | $33.99 | 13 | $2.61 | 1 (first-time call) | $34 | 0 | 45% |
| LSA in the PPC account (20067257249) | $166.34 | – | – | 2 plumber (1 call, 1 message) | $83 | – | – |
| LSA SA [1] electrician (7261668241) | $139.88 | – | – | 2 calls | $70 | – | – |
| LSA SA [2] HVAC (6621969129) | $111.74 | – | – | 1 call | $112 | – | – |

- **Weekday vs weekend (PPC account):** Wed–Fri $825.55/day, 9 Search leads; Sat–Sun $478.85/day, 2 leads. Electrical lost 53% of impressions to budget on weekdays, none on the weekend.
- **Electrical ad groups (11-04..11-09):** Electrician_NearMe $603.79 / 4 leads ($151); Electrical_Repair $323.21 / 2 ($162); Electrical_Services $820.63 / 2 ($410). Junk clicks: 'mesa electrical contractors' $71.01, 'electrical companies commercial' $68.97, 'aep pleasanton tx' $30.67; bare 'electrician' $134 / 3 clicks / 0 leads.
- **HVAC:** AG1_HVAC_ACRepair $428.13 / 8 clicks at **$53.52** / 0 leads; AG3_HVAC_Maintenance $323.27 / 14 clicks / 1 lead. One click on 'commercial ac repair san antonio' cost $126.00; 'cowboys heating and air san antonio' (competitor) $93.85 / 2 clicks. Max Conversions with no cap.
- **Plumbing:** $806.19 / 40 clicks through 11-09, **no lead, no ad call, not even a call-button tap**. AG1_Plumbing_LeakDetection took $502.68 (24 clicks). Max Clicks buys 'best plumbers near me', 'cheap plumbers in san antonio', and competitor names ('1 tom plumber san antonio' x2, 'venture plumbing san antonio tx'). Call asset shows on Plumbing (77 impr). **Pages are not broken:** rendered headless 11-09, /services/plumbing, /leak-detection and /water-heaters all load with the right H1 and a tel: link (same template as Electrical, which converts). The plain HTTP check is useless on this site (JS shell, 200 for everything). The plumbing and electrical service pages show no form in the rendered DOM; only /proud-pops-hvac-services has the GHL survey.
- **Calls from ads (call asset 225-5767):** 3 calls, all Electrical: 11-04 48s, 11-04 372s, 11-07 141s.
- **LSA:** 5 leads, all charged, all still status ACTIVE (not marked).
- **My Favorite Service (9815330464):** Smart campaign 'HVAC Contractor Services' ($21/d) still running unmanaged: $64.69 since 11-04, 3,475 impr, 145 clicks, 0 conversions; $117.90 MTD. Its 2 LSA accounts: $0. fu-019 still open.
- **Pacing:** MTD through 11-08 = **$4,048.41** across the 3 accounts (PPC $3,796.79 + LSA $251.62; MFSC $117.90 not included). At the 5-day rates (16 weekdays, 6 weekend days left, separate LSA ~$50/day) November lands **≈ $21.2k**; with today's Electrical +$80 on weekdays **≈ $22.5k**, vs $25k. Thanksgiving week probably runs lower.
- Caveats: 5 days; HVAC (22 clicks) and Plumbing (38) are small samples; CallRail uploads for the last clicks can still land; the Conversions column is not comparable with October (taps were ~93% of it).

---

## 2026-11-09 (later) — APPLIED: Branded $130 → $50, Nonbranded Electrical $375 → $455 (Edu: "good to move that budget")

`branded_to_electrical_2026-11-09.py`, validate-only then `--apply`, read-back OK: Branded 23853361615 **$50/day**, Search Electrical 23866999121 **$455/day**, both ENABLED.
Search caps still **$880/day** (Branded $50, Electrical $455, HVAC $230, Plumbing $145), so no client approval needed. Rollback = Branded $130, Electrical $375.
Why: see the fu-132 entry below. ⚑ Read at fu-054 (11-11): Electrical spend vs $455 and its cost per real lead at the higher budget (was $214), Branded spend vs $50.

---

## 2026-11-09 — fu-132 recheck: Branded is serving again at the $18 ceiling (read-only, nothing changed)

`branded_recheck_2026-11-09.py` (read-only; `--extra` = QS/changes/ads, `--headroom` = other Search campaigns). Pulled ~07:30 CT, so 11-09 is partial.

**Branded 23853361615 is back.** Target IS abs-top 95%, ceiling $18, budget $130, status still LEARNING (BIDDING_STRATEGY_LEARNING).

| Date | Impr | Clicks | Cost | CPC | Search IS | Top | Abs-top | Lost to rank |
|---|---|---|---|---|---|---|---|---|
| 11-02 (Max Conv) | 26 | 12 | $141.30 | $11.77 | 51.2% | 48.7% | 38.5% | 0 (48.8% lost to budget) |
| 11-03 (Max Conv) | 12 | 6 | $105.32 | $17.55 | 45.8% | 45.8% | 25.0% | 0 (54.2% lost to budget) |
| 11-05 ($10 cap) | 0 | 0 | $0 | – | <10% | – | – | 90% |
| 11-06 (cap → $18 at 06:27 CT) | 5 | 2 | $0.54 | $0.27 | 30.8% | 30.8% | 15.4% | 69.2% |
| 11-07 | 9 | 2 | $0.97 | $0.48 | 50.0% | 50.0% | 16.7% | 50.0% |
| 11-08 | 22 | 7 | $19.52 | $2.79 | 88.9% | 83.3% | 38.9% | 11.1% |
| 11-09 (to 06h) | 4 | 0 | $0 | – | – | – | – | – |

- First impression after the cap change: 11-06 10h CT, about 3.5 hours later. 11-06..11-08 total: 36 impr, 11 clicks, $21.03, avg CPC $1.91.
- **Not pinned at the cap:** avg CPC $2.79 on the best day, single terms $0.28–$3.94, vs the $18 ceiling.
- **Abs-top 38.9% on 11-08 vs the 95% target**, 61.1% of abs-top lost to rank. Still learning; main keywords are QS 10 (proud pops, proud pops hvac, proud pops plumbing, proud pops san antonio), so there is room for the strategy to bid up. Bid estimates are not exposed under Target IS (API returns $0).
- Real leads on Branded since the change: **1 First Time Phone Call (CallRail upload, 11-08)**, 0 Calls from ads. 1 tap on 11-08 sits in all_conversions only, as intended.
- Search terms 11-06..11-09: brand only (proud pops, proud pops hvac, proud pops plumbing air & electric [san antonio], proud pops san antonio).
- Ads: 8 enabled RSAs all APPROVED / ELIGIBLE; the 2 POOR ones stay paused. Change history since 11-04: only eduardo@ via API, last = the 11-06 ceiling.

**Correction to the 11-06 diagnosis.** The $10 cap was probably not a price problem: brand clicks now cost $0.27–$3.94. The $11.77–17.55 CPC before the switch was Max Conversions overbidding (it was still chasing taps then), not the market price. What the data can't separate: the strategy needing ~2 days to ramp after the 11-04 switch vs the 11-06 cap edit restarting it. Either way Target IS now gets ~89% IS at about a fifth of the old CPC.

**Spend vs $130/d: Branded uses $1–20/day.** Brand volume here is small (~16–50 eligible impressions/day), so even at full IS it will not come near $130. About $100/day of the $880 plan has no use on Branded.

**Other Search, 11-04..11-08 (5 days):**

| Campaign | Budget/d | Spend/d | Clicks | CPC | Real leads | Cost/lead | IS | Lost to budget | Lost to rank |
|---|---|---|---|---|---|---|---|---|---|
| Nonbranded Electrical (Max Conv) | $375 | $342.87 | 63 | $27.21 | 8 | $214 | 33.6% | 38.1% | 28.3% |
| Nonbranded Plumbing (Max Clicks) | $145 | $153.65 | 38 | $20.22 | 0 | – | 26.3% | 28.0% | 45.7% |
| Nonbranded HVAC (Max Conv) | $230 | $150.28 | 22 | $34.15 | 1 | $751 | 26.8% | 23.0% | 50.2% |
| Branded (Target IS) | $130 | $6.80 | 13 | $2.61 | 1 real (+1 tap counted 11-04) | – | 54.7% | 0 | 45.3% |

In-account daily: 11-04 $910, 11-05 $733, 11-06 $833, 11-07 (Sat) $564, 11-08 (Sun) $394. **MTD 11-01..11-09 early = $3,867.98** (this account only; LSA accounts 7261668241 + 6621969129 not pulled). Rough projection at ~$825 weekdays / ~$480 weekends: **≈ $19.8k in this account vs $25k**.

**Proposed (Edu's go, total stays $880/d so no client approval needed):** Branded $130 → $50, Nonbranded Electrical $375 → $455. Electrical is the only nonbranded campaign producing real leads and loses 38% of its impressions to budget. $50 keeps 2.5x room over Branded's best day while the strategy pushes for abs-top. This alone adds at most ~$1.7k by month end, so the rest of the gap is for the 11-11 pacing check (fu-054).

⚑ Carry to fu-054 (11-11): Branded abs-top share vs 95% once learning ends, CPC drift toward the ceiling, and the pacing gap.

---

## 2026-11-06 — LSA → Pay-per-lead PMax migration: exposure check (read-only, NOT migrated yet)

None of the 3 Proud Pops LSA campaigns has switched yet (PPC-account LSA `20067257249`, SA [1] electrician 7261668241, SA [2] HVAC 6621969129).
The PPC-account LSA is multi-trade (leads 08-08..11-06: HVAC 12 / plumber 11 / bath 1) with ONE per-trade target set: HVAC $62
(plumber/bath none). On migration Google uses one campaign-level target; how the $62 carries over is unknown. Check that campaign's target
and lead mix right after it switches.

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

## 2026-11-06 (later) — APPLIED: Branded CPC ceiling $10 → $18, Target IS kept (Edu: "Let's move the max click and maintain tImp Share")

`branded_cap_18_2026-11-06.py`, validate-only then `--apply`, read-back OK: Branded 23853361615 Target IS absolute top 95%, **ceiling $18**, budget $130/d
unchanged, status LEARNING. Rollback = ceiling back to $10. ⚑ Recheck 11-09 (fu-132): impressions back, IS, avg CPC vs $18, spend vs $130.
- AT Internal Request **d2b5e325-d9b4-46c1-a98c-840b6af933a7** "Google Ads update: first real leads since the tracking fix" created as a DRAFT for Angela (Intake, Edu submits): first results + Branded cap $10 → $18 (corrects the $10 in 815ca8bc).

---

## 2026-11-06 — fu-127 check: first days on real-lead bidding + new call asset (read-only, nothing changed)

**Bidding change worked.** Taps ('TSD - Website Call') are out of the Conversions column: 11-05 = 0 conv / 5 all_conv. CallRail uploads land in this
account now: **First Time Phone Call 4** on 11-05 (Elec 3, HVAC 1), Repeat Phone Call 3 (all_conv only, as intended). Calls from ads 1 (Elec, 372s call 11-04).
Real leads by click date 11-04..06: **Electrical 6** (1 ad call + 3 first-time CallRail + 2 Website lead) on $784.92 ≈ **$131/lead**; HVAC 1 on $432.48;
Plumbing 0 on $302.69; Branded 0. Nonbranded total $1,520 / 7 ≈ $217 (2 days, too early to judge).
**Call asset (210) 225-5767 (428601259336): APPROVED, serving** account + campaign level: 95 impr 11-04, 173 impr 11-05; 2 calls 11-04 (48s, 372s), 0 on 11-05.
**Spend (in-account):** 11-04 Search $816.54 + LSA $93.70; 11-05 Search **$716.51** (Elec $374.54, HVAC $166.89, Plumbing $175.08, Branded $0). No day over 2x
(Elec 11-04 $410 = 1.09x, Plumbing 11-05 1.21x). MTD 11-01..11-06 ≈ $2,005. At the 11-05 rate November lands ≈ **$20.7k vs $25k**.
⚠ **BRANDED IS DARK since the Target IS switch (11-04 08:08).** 2 impressions after the switch on 11-04, **0 on 11-05 and 11-06 so far**. Status LEARNING,
rank-lost 40% on 11-04. Not cannibalization: all 3 Nonbranded have 'proud pops'/'problem solvers' negatives and 0 brand terms in their search terms.
The $10 cap sits under what brand clicks cost before the switch ($11.78 CPC 11-02, $17.55 11-03). Branded = ~$155 per new-customer call (CallRail 10-15..11-03),
the best lead source here, and its $130/d is most of the underspend.
**Proposed (Edu's go):** raise the Branded CPC ceiling $10 → $18 (keep Target IS abs-top 95%), recheck 11-09. Alternative: back to Max Conversions, which now
bids only on real calls + forms (the old CPC inflation was it chasing taps).

---

## 2026-11-04 (later 5) — APPLIED: Branded → Target IS + 2 POOR RSAs paused (Edu: "Apply 2 and 3, yes"; staged in Gui's 10-31 pass)

`branded_target_is_2026-11-04.py`, validate-only then `--apply`, read-back OK: Branded 23853361615 Maximize Conversions → **Target Impression Share,
absolute top 95%, $10 CPC ceiling**, budget $130/d unchanged (status LIMITED while it learns). **Paused POOR RSAs** Brand_OldName 808846497511 and
Brand_HVAC 808844736361 (each ad group keeps 1 enabled ad). Item 1 (Website lead biddable on Branded) dropped: Target IS doesn't bid on conversions.
⚠ Pacing: Branded spent ~$100-175/d on Max Conversions at $11-15 CPC; under a $10 cap it will likely spend less, so November may land under $25k.
Rebalance (e.g. unspent Branded → Search Electrical) at the fu-054 check 11-11.
- AT Internal Request **815ca8bc-e79d-4afd-a8e4-0b39df627b5c** "Google Ads update: Search back on and call tracking fixed" created as a DRAFT for Angela (Intake, Edu submits; task department = Customer Success).

---

## 2026-11-04 (later 4) — Phone numbers on the live ad landing pages (read-only)

Rendered all 11 proudpops.com final URLs of enabled ads + sitelinks (headless Chromium, ?gclid=TSDtest1104, after scroll): CallRail's script loads on
every page and **the only number shown is a CallRail website-pool number** (210-759-4194 in this session, swapped from the 225-5767 swap target),
3-9 tel: links per page. No main line (210-997-7190), no 864-6867, no old 794-7570 on these pages. Raw HTML has no numbers (client-rendered site).
- With Search back at $880/d, the **4-number pool** (CallRail recommends 14) will recycle numbers between visitors → some calls attributed to the wrong
  visit. AM item: grow the pool (client cost).
- ⚠ **2 sitelinks on Search Electrical 404:** 'Our Story' 120042497724 → txproblemsolvers.com/about/our-story/ and 'Contact Us' 185822702561 →
  txproblemsolvers.com/contact/contact-us/. Replacements that render: https://proudpops.com/about ("Pop's Promise") and https://proudpops.com/contact.
  **FIXED later 11-04 (Edu's go):** `sitelinks_404_fix_2026-11-04.py`, read-back OK: 'Our Story' → https://proudpops.com/about, 'Contact Us' → https://proudpops.com/contact.
  (/our-story and /contact-us render "We couldn't find that page" despite HTTP 200.) Fix needs Edu's go.

---

## 2026-11-04 (later 3) — APPLIED: bidding on real leads only + call asset swap (Edu: "Make the campaigns bid only on real calls" / "change the asset to the right number and get rid of the old disapproved one")

1. `conv_real_calls_2026-11-04.py` (validate-only, then `--apply`, read-back OK): **'TSD - Website Call' 7667749854 (ad call-button taps), 'Repeat Phone Call'
   7889536740, leftover 'Phone Call' 7238068273 → Secondary**; **'First Time Phone Call' 7889536968 stays primary, counting → ONE_PER_CLICK**.
   Counted for bidding now: First Time Phone Call (CallRail, 60s), Calls from ads (60s), Website lead (customer forms; careers excluded since v43).
   ⚠ The Conversions column drops sharply from 11-04 (taps were ~93% of it): that's the change, not a collapse. Compare on all_conversions across it.
2. `call_asset_swap_2026-11-04.py` (14 ops, one request, read-back OK): approved asset **428601259336 (210) 225-5767 linked at account level + 6 lead
   campaigns** (Search HVAC/Electrical/Plumbing, Branded, PMax HVAC/Electrical); **old disapproved (210) 794-7570 removed everywhere** (campaign asset
   360709032917 x6 + account asset 185848871539). Ad calls go through CallRail's '210 - CALL POP' tracker; Google counts them via its forwarding number (Calls from ads, 60s).
⚑ Check 11-06 (fu-127): asset serving (impressions on the call asset), first Calls from ads / First Time Phone Call conversions, Search spend vs $880/d.

---

## 2026-11-04 (later 2) — CallRail integration repointed to PPC (Edu via Cowork) + conversion-action read (read-only on Google Ads)

Cowork (CallRail UI): Google Ads integration moved from 849-758-3415 to **105-184-3378 (1051843378)**, Active, separate first-time/repeat ON,
minimum duration **15s → 60s**, all numbers; enhanced conversions came back checked on reconnect and was unchecked again (off after reload).
Integration was down only for the minutes between unlink and reconnect.
**API read of 1051843378, 11-04:** CallRail created **First Time Phone Call 7889536968** and **Repeat Phone Call 7889536740** (UPLOAD_CLICKS, DEFAULT/WEBSITE,
both PRIMARY, counting MANY_PER_CLICK). Also still enabled + primary: leftover **'Phone Call' 7238068273** (UPLOAD_CLICKS) and
**'TSD - Website Call' 7667749854 = CLICK_TO_CALL (taps on the ad's call button, despite the name), 483 of the account's ~517 conversions in 30d**.
DEFAULT/WEBSITE and PHONE_CALL_LEAD/CALL_FROM_ADS are biddable on Branded + all 3 Search campaigns (Max Conversions / Plumbing Max Clicks),
so the restarted Search campaigns would bid on taps + repeat customers. Careers fix (GTM v43, 10-08) is holding, so the old "careers before taps→Secondary" gate is met.
**Proposed (Edu's go):** Repeat Phone Call, 'Phone Call' 7238068273, 'TSD - Website Call' → Secondary; First Time Phone Call stays primary with
counting → ONE_PER_CLICK. Bidding then = customer forms (Website lead) + First Time CallRail calls (60s) + Calls from ads (60s, once fu-052 links the asset).

---

## 2026-11-04 (later) — APPLIED: November restore to $25k/month (Edu: "Let's bring them back to 25k/mo")

`nov_restore_25k_2026-11-04.py` (copy of the 11-01 script, caps scaled ~10% for the late start), validate-only, then `--apply`, read-back OK:
Branded $100 → **$130** (enabled), Search Electrical **ENABLED $375**, Search HVAC **ENABLED $230**, Search Plumbing **ENABLED $145** = **$880/day**.
PMax HVAC/Electrical + both YouTube stay PAUSED.
Math: Nov 1-3 spent $362 (Branded + LSA-in-PPC). $25,000 - $362 = $24,638 over Nov 4-30 (27 days) ≈ $912/d; LSA (3 surfaces) ≈ $31/d → Search caps ≈ $880/d.
Max Conversions can overspend single days (up to 2x); the script's "x30.4" line is a full-month figure, not this month's.
⚑ Pacing check fu-054 on 11-11: November should land $24-25k. If the average runs > ~$950/d, trim Search HVAC/Electrical first.
Still open: call asset 225-5767 (fu-052, Edu's go), CallRail → Google Ads integration repoint to 105-184-3378 (fu-126, Cowork), AM items (pool 4 → 14, GA4 old domain).

---

## 2026-11-04 — CallRail access via Cowork (Edu's other login): P-5 answered, fu-048 read (read-only, nothing changed)

Cowork pulled Proud Pops' CallRail (account #533-681-324, company "The Problem Solvers" 686172931; TSD is an admin user). Export saved locally:
~/Downloads/proud-pops-callrail-calls-2026-09-13_2026-11-03.csv (304 calls; **data only starts 10-14**). Settings untouched (Cowork added 7 Call-log columns to the view).

**P-5 answered:**
- **(210) 225-5767 = CallRail tracker "210 - CALL POP"**, and it is the website swap target. Main line = 210-997-7190 ("Proud Pops Main").
  210-794-7570 (the disapproved call extension) is not an active tracker. 210-864-6867 = tracker "1st Repair is on Pops Letters".
- 73 active numbers (69 source trackers + 4-number website pool). Unused PPC trackers exist: "PPC Electrical" 210-940-2589, "PPC HVAC" 210-920-8336,
  "PPC Plumbing" 210-361-7827 (source label Google Ads - Paid Search, 0 calls in the window).
- **Swap works:** the 4 pool numbers took 47 calls; CallRail warns the pool is too small (recommends 14). Swap target = 225-5767.
- ⚠ **CallRail's Google Ads integration points to the OLD account 849-758-3415** ("[Old Account] The Problem Solvers - LSA HVAC San Antonio 2"),
  not PPC 105-184-3378: First/Repeat call uploads go nowhere useful. Min 15s filter. GA4 integration still on txproblemsolvers.com (G-C7QTE9ZZXQ). GBP not connected.

**fu-048 (do PMax or Search drive real calls?) — can't be answered from CallRail:** the export starts 10-14 and nonbranded Search + PMax were paused
10-15 → today, so only 10-14 overlaps (2 Branded calls 195s/136s + 1 Search Electrical 614s, 0 PMax). Excluding one caller (…8301, 47 calls on 10-20/10-30,
looks like a test sweep), Google Ads calls 10-14 → 11-03 = 38:
| Campaign (landing URL) | Calls | 60s+ answered | 60s+ first-time |
|---|---:|---:|---:|
| Branded 23853361615 | 25 | 20 | **13** |
| GLSA Plumbing tracker (LSA) | 4 | 3 | 3 |
| old Search_Brand 21948583115 (paused; stale session URLs, repeat callers) | 4 | 2 | 0 |
| Search Electrical 23866999121 (10-14 only) | 2 | 2 | 2 |
| Website pool, no campaign | 2 | 2 | 0 |
| Murray GLSA | 1 | 1 | 1 |
- **Branded drives real calls Google can't see:** $2,010.72 10-15 → 11-03 → 13 first-time 60s+ calls ≈ **$155 per new-customer call** (plus forms).
  Google Ads counts ~0 of these (call extension disapproved since May, CallRail uploads go to the old account).
- Decision input for fu-053: no evidence for PMax either way; the staged restore keeps both PMax paused anyway → nothing to change in the split.
- `nov_restore_25k_2026-11-01.py` validate-only re-run 11-04: OK (7 ops, caps $800/d), awaiting Edu's go.

**Proposed (Edu's go):**
1. Run the Nov restore now (Search on at $800/d total; PMax stays off). Started 11-04, so November lands ~$22-23k unless caps rise ~10%.
2. fu-052: link the already-approved call asset 225-5767 (428601259336) at account level + 6 lead campaigns and remove the 794-7570 links (b4 path).
   Option later: per-campaign PPC trackers (PPC HVAC/Electrical/Plumbing) as call assets for CallRail attribution by campaign.
3. Repoint CallRail's Google Ads integration from 849-758-3415 to 105-184-3378 (CallRail UI; TSD is admin there). Then First/Repeat uploads reach PPC.
4. AM items: pool 4 → 14 numbers (client cost), GA4 integration on the old domain.

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied. Extra pulls: scratchpad `pp_x/pp_x1109.py` (change_event old/new, Branded daily IS, conv goals, call assets,
conv by action/campaign/date, Nov MTD), `pp_x2.py` (11-09 changes, portfolio strategies, paused kws), `rec.py` (recommendations).

**What changed since 10-31 (all eduardo@, change_event):** **11-04 Nov restore**: Search Elec / HVAC / Plumbing ENABLED, caps Elec $375,
HVAC $230, Plumbing $145, Branded $130 = $880/d (plan was $800/d). **Call asset fixed 11-04:** (210) 225-5767 (428601259336) linked on all 4
Search campaigns + account level, 794-7570 removed everywhere (fu-052 done). 2 POOR Branded RSAs paused (808846497511, 808844736361).
Branded → Target IS 95% abs-top, $10 cap (11-04) → $18 (11-06). Sitelink URLs → /contact, /about. **Block F effectively done ~11-04:**
`TSD - Website Call` now primary_for_goal false (last counted tap 11-04), CallRail import live (`First Time Phone Call` primary, `Repeat Phone
Call` secondary, UPLOAD_CLICKS). **11-09 (today, after the window):** Branded $130 → $50, Elec $375 → $455 (total still $880/d); HVAC on
portfolio `TSD_ProudPops_HVAC_MaxConv_CPC30` (12308461252, tCPA $265, CPC cap $30); paused Plumbing AG1 [plumber san antonio] / [plumber
near me] / "plumber san antonio tx" (AG4 dupes) + Elec "electrical services" phrase; negatives Elec electric company / aep / hourly rate,
Plumbing cheap / saws, HVAC cheapest.

**7-Day Google (https://app.agencytitan.com/tasks/instance/7154583f-04d7-472c-88d1-65d7940c0a4c), completed.** Week 11-02..11-08 (2 days
Branded only + 5 days full Search): $3,514.65 / 154 clk / 13 conv / $270.73 / $22.82 CPC / 8.43% CVR (prior Branded-only $666.37 / 45 / 8
taps). Elec $1,714.36 / 63 / 8 ($214.30; IS 33.6%, budget-lost 38%); HVAC $751.41 / 22 / 1 (CPC $34.15, rank-lost 50%); Plumbing $768.27 /
38 / 0 (Max Clicks $45); Branded $280.61 / 31 / 4 (IS 51.7% vs 74.0%). Counted 13 = Branded 3 taps (11-02..11-04) + 1 CallRail call; Elec
4 CallRail first-time calls + 2 Calls from ads + 2 forms; HVAC 1 CallRail call. +2 Branded forms not counted (no form goal on Branded) →
12 real leads, ~$293 each. call_view: 3 Elec calls (48s/372s/141s). **Branded Target IS $10 cap starved delivery** 11-05..11-07 (0/5/9
impr, rank-lost 50-90%); 11-08 back to IS 88.9%. Competitor terms $234.14 (cowboys heating and air $93.85, mesa electrical contractors
$71.01, 1 tom plumber $49.24, venture plumbing $20.04). Search IS 29.6%. Nov 1-8 PPC $3,570.85 + LSA $477.56; at full $880 caps Nov ≈ $24.8k
max (inside $25k); actual 11-04..11-08 $394-$817/d. Staged: 4 competitor negs, Branded form goal biddable, Plumbing decision 11-16 (Max Conv
or move budget to Elec at same total), HVAC ad groups to own pages, CallRail vs Calls-from-ads double-count check in CallRail UI, negate
exact [electrician] if still 0 conv. KPI Google row `dcaf4621` (Mixed).

**14-Day Google (https://app.agencytitan.com/tasks/instance/8d89a14e-12bb-48a9-a1ed-2c51e9a52109), completed.** 10-26..11-08 $4,181.02 /
199 clk / 20.98 conv (prior 14 $7,235.83 / 140, mostly taps). All PPC clicks in targeted geo (only LSA has out-of-target, $313.90). Old
Electrical RSAs out-convert the new G2 ones 7 vs 1 conv (809528123698 4, 809490671193 2, 809490621054 1) → don't run G2b as-is, fix their
plumbing descriptions instead. Expected CTR below avg on ~all nonbranded kws; Electrician AG1 ad relevance below avg; QS 1 "electrical work
near me". No audiences on any Search campaign. 96 open recs (82 keyword adds, partners x3, display x3, broad, Plumbing Max Conv, HVAC budget).
22:00-06:00 $409.13 / 0 conv. All 8 checklist items ticked.

**LSA, 7-Day (https://app.agencytitan.com/tasks/instance/c97d0a5a-b50a-4058-a704-f65609f391dc), completed.** 3 sources: in-account $225.94
+ electrician $139.88 + HVAC $111.74 = $477.56 (prior $244.78) / 7 leads (5 calls, 2 msgs), 6 charged / $79.59 per charged lead (prior
$81.59). Top impr 92.8% (prior 90.9%), impr 722 vs 637. 11-02 plumbing message CONSUMER_DECLINED + charged, undisputed; 6 still ACTIVE.
Budget fields $714.29/d x3 = Underspending, not the limit. KPI LSA row `665d1f48`.

**YouTube, 7-Day (https://app.agencytitan.com/tasks/instance/19eedeec-318f-4b4f-849c-a99d87bf7c2e), completed.** Both YouTube campaigns
(24120440530, 24120482524) still PAUSED: $0 / 0 impr both weeks, no ads/placements/conv rows. All 7 checklist items ticked.

**Meta, 7-Day:** N/A, see meta-ads-log.md (KPI Meta row `9c508a94`).

---

## 2026-10-31 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied. Extra pull: scratchpad `pp_x1031.py` (call assets, Branded daily, changes, geo, LSA leads, Oct MTD).

**7-Day Google (https://app.agencytitan.com/tasks/instance/d0e2f908-d839-4a82-9f65-39f82bde1132), completed.** Week 10-24..10-30, Branded
only (last week of the $25k cut): $687.25 / 52 clk / 7 conv / $98.21 CPL / $13.22 CPC / 13.46% CVR (prior $740.20 / 67 / 15 / $49.35 /
$11.05). All 7 = TSD - Website Call taps; 0 calls, 0 phone impressions; 1 Website lead form 10-24 not counted (not biddable on Branded).
Terms all brand ('problem solvers' variants $44.28 / 0 conv). IS 84.5% (bl 8.6%, rl 6.9%; prior 66.7%); daily $15.63-$173.78 on $100.
**Call asset UNCHANGED since 10-27:** only (210) 794-7570 (360709032917, DISAPPROVED) linked on Branded + 6 paused lead campaigns; account-
level 210-794-7570 (185848871539) DISAPPROVED; approved (210) 225-5767 (428601259336) REMOVED everywhere. Branded LIMITED /
CALL_EXTENSION_DISAPPROVED. No change_event since 10-16. Oct 1-30 all 3 accts $30,643.64 (lands ~$30.7k). Staged: link 225-5767 + unlink
794-7570 before 11-01 (fu-052), Website lead biddable on Branded, pause POOR RSAs 808846497511 / 808844736361, Branded Target IS abs-top
~$8-10 cap, Block F before the restored spend learns on taps. Nov 1 $800/d restore = Edu's (fu-053). KPI Google row `28c94e63`.

**LSA, 7-Day (https://app.agencytitan.com/tasks/instance/9f22518a-eb1a-4ab0-bf99-086dc3a6e103), completed.** 3 sources: in-account $173.30,
electrician 7261668241 $71.48, HVAC 6621969129 $0 (197 impr) = $244.78 / 4 calls, 0 msgs / 3 charged / $81.59 per charged lead (prior
$372.14 / 6 / 5 charged / $74.43). Top impr 89.3% (prior 90.7%), impr 608 vs 608. API budget fields $714.29/d x3 (~1.6% used) =
Underspending, budget not the limit. All 10 leads since 10-17 still ACTIVE/NEW. KPI LSA row `02d92a7c`.

**YouTube, 7-Day (https://app.agencytitan.com/tasks/instance/6401c616-e565-4bbc-a5d8-632926bc87cc), completed.** Both YouTube campaigns
(24120440530 SA, 24120482524 New Braunfels) still PAUSED since 10-16: $0 / 0 impr both weeks, no ads/placements/conv rows. Stays off in
the Nov 1 plan (fu-053). All 7 checklist items ticked (nothing to pause/escalate).

**Meta, 7-Day:** N/A, see meta-ads-log.md (KPI Meta row `78d95732`).

---

## 2026-10-27 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied. Extra pull: scratchpad `pp30_split_1027.py` (period split + call assets) and `pp_lsa_daily_1027.py`.

**30-Day Google (https://app.agencytitan.com/tasks/instance/1fd032c6-7075-4f7f-b381-77bf5eaf7e2e), completed.** 30d 09-27..10-26 PPC
$35,950.68 / 12,939 clk / 857 conv (prior $60,388.95). **Period 1 (09-27..10-14, full account):** $34,447.14 / 835 conv, 768 (92%) taps;
Elec Search $10,629 / 18 forms, HVAC Search $6,813 / 3, PMax HVAC $5,365 (99% Display) / 3, PMax Elec $3,816 (84% Display+YT) / 38,
Plumbing $2,775 / 5, Branded $1,474 / 4 (not biddable), YouTube $3,575 / 0. 59 of 71 forms fired before the 10-07 careers fix (/careers
145 clk / 50 conv); 10-08..10-14 = 12 forms. **Period 2 (10-15..10-26, Branded only):** $1,503.52 = Branded $1,252.53 / 118 clk / 22 conv
(all taps) + YouTube $250.99 on 10-15/16; Branded CPC $10.61, IS 74.0% (budget-lost 23.1%), $51-$155/d on $100 budget. 0 calls.
Findings: 794-7570 call asset still DISAPPROVED and the only one linked; 225-5767 (approved) unlinked (fu-052). RSA performance labels
all NOT_APPLICABLE (ranked by CTR instead). 3 old Electrical RSAs (809490671193, 809490621054, 809528123698) carry plumbing descriptions;
old + new RSAs both live (G2b not run). Nonbranded QS avg 4.6, expected CTR below average on 53/55. Out-of-target PPC $2,279.34 (HVAC
$2,092, PMax Elec $187), all period 1; Canyon Lake $1,981 / 7 conv in-target. HVAC Search sends every ad group to /proud-pops-hvac-services.
Speed score not available via API. Staged: link 225-5767, G2b cutover, pause 2 POOR Branded RSAs + Services snippet, rewrite low-CTR
headlines (problem + same-day + upfront price), HVAC ad groups to their own service pages, all before the Nov 1 restore (fu-053).
Checklist: 8 of 9 ticked (visitor recordings: no access). No KPI row (no 30-day Google keys). Toggles for Gui in the UI.

**LSA, 30-Day (https://app.agencytitan.com/tasks/instance/dc08ea58-52a8-4b24-897c-52c94df1ae60), completed.** 3 sources combined
(in-account $203.41, 7261668241 $210.45, 6621969129 $321.95) = $735.81 / 13 leads (7 calls, 6 msgs) / 11 charged / $66.89 per charged
lead, 0 credits, 0 disputes (prior 30 $1,280.80 / 29 / 18 charged). Period 1 $284.59 / 5; period 2 $451.22 / 8 (LSA not in the cut).
1 BOOKED, 2 DECLINED + 1 CONSUMER_DECLINED (all charged, undisputed), 9 ACTIVE -> booking 7.7% (floor). Impr 1,685 vs 3,327 (-49%),
top 91.2%, budget fields $714.29/d x3 (~1% used). All 5 HVAC-acct leads tagged clean_ducts_vents; 10-23 in-account charge maps to
Orlando FL. Staged: dispute review of 3 declined, client to answer msgs + update statuses (AM), job types check, D2 profile review.
KPI LSA row `16e5089d` (10-23) updated with 30-day keys (true CPL $66.89, credits 0, booking 7.69%, disputes 0/0).

**Meta, 30-Day (https://app.agencytitan.com/tasks/instance/a993237c-01c8-4575-807b-ca1be71c0c4b), completed as N/A.** No Proud Pops
ad account shared with TSD (all pages checked 10-27). KPI Meta row `d4ef0536` (10-23) updated: reach 0, frequency 0. See meta-ads-log.md.

---

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

**7-Day YouTube (https://app.agencytitan.com/tasks/instance/8ad3367a-3fa9-433d-aa77-fbaf957df09f), read-only, completed.** Both YouTube campaigns PAUSED (08/2026 - YT - VideoViews (San Antonio) 24120440530, 08/2026 - YT - Awareness - New Braunfels 24120482524; budgets $100/d each, paused 10-16 after the 10-14 $25k cut, fu-046). 10-19..10-25: $0, 0 impr. Prior week 10-12..10-16 (5 days): $423.80 + $432.13 = $855.93, views 29,780 + 22,189, view rate 68.4% / 81.5%, watched to 100% 67.4% / 80.9%, 10 clicks, 0 conversions. Placements/ads: no rows this week (nothing served). Tracking: 0 conversions in the prior week too (awareness / video views only, no conversion goal expected). Pacing: $0 vs $0 plan (Branded only to 10-31). Nothing to pause or escalate. YouTube stays off in the Nov 1 restore plan (fu-053). All 7 checklist items ticked (placements / pause / escalate reviewed, not applicable). No notes field on this task.

---

## 2026-10-23 — Weekly 7-day (Google, LSA, Meta) + 14-day review (Agency Titan tasks, Gui): read-only, everything staged

**Google 10-16..10-22 (PPC, LSA excluded):** $872.43 / 76 clk / 18 conv / $48.47 CPL (prior $12,106.21). Only Branded live since the
10-14 $25k cut (Nonbranded, both PMax, both YouTube paused by Edu 10-14/10-16; $53.84 YouTube on 10-16 before the pause). Branded
$818.60 / 75 / 18 / $45.48, CPC $10.91 (prior $8.95), IS 72% (25% budget-lost), Max Conv $100/d ran ~1.5x on 10-16/19/22. **All 18 conv
= TSD - Website Call taps; 0 call_view calls (call asset still disapproved, fu-052), 0 Website lead forms.** Terms all brand variants.
**LSA (3 surfaces):** in-account $69.16 / 1 msg; 6621969129 $176.78 / 1 call + 1 msg; 7261668241 $59.59 / 1 call = $305.53 / 4 / $76.38,
+2 uncharged phone leads; top impr 90.4%; budget fields $714.29/d each = Underspending. **Meta:** no ad account shared with TSD ($0, blocker).
**14-day 10-09..10-22:** $12,978.64 total (Branded $1,498.78 / 151 / 28). Staged: Branded → Target IS abs-top with ~$8 CPC cap; pause 2 POOR
RSAs (Brand_OldName 808846497511, Brand_HVAC 808844736361); observation audiences; dismiss partners/display expansion/broad/tCPA recs;
fix Nonbranded landing/offer (HVAC $3,182 / 1 form, Plumbing $791 / 0) and the call asset before the Nov 1 restore (fu-053).
AT: Google `5fcb9612` (KPI `247995a9`), LSA `6ee7bffa` (KPI `16e5089d`), Meta `43e88713` (KPI `d4ef0536`), 14-day `ec9d122a`, all completed.
14-day toggles must be set in the UI.

## 2026-10-20 — fu-047: Branded-only October is holding (read-only)

Oct 1–20 spend, all 3 accounts: **$29,234.11** (PPC 1051843378 $28,761.67, LSA 7261668241 $210.45, LSA 6621969129
$261.99). Only Branded + the 3 LSA campaigns are ENABLED. Both YouTube campaigns are PAUSED (last spend 10-16, $54).
Branded Oct 15–20: $56 / $149 / $57 / $112 / $154 / $64 = $99/day avg on the $100 budget (daily swings are Google's
2x overdelivery, monthly cap holds). LSA ~$45/day lately.
**Projection:** $29.2k + 11 days × ~$145 ≈ **$30.8k** for October, in line with the ~$30k expected on 10-14.
Nothing turned back on, no action needed. Next: Nov 1 restore (fu-053).

---

## 2026-10-16 — Campaign check (Oct 1–15) + account-level competitor negatives. APPLIED

**Check (read-only, same recipe as Hawkins / All Seasons 10-16):** Search traffic is mostly clean: ~80% of $10.1k visible search-term spend = real service searches, brand 9%, competitors 6% (Elmer AC, Above All Air, Gillette, Sigma Air, Service Experts, Wattsmith, "goodman phone number" $176), off-service 2%. The real problems:
- 617 of 666 counted conversions (93%) = `TSD - Website Call` phone taps, 0 tracked calls (call asset disapproved, fu-052) → PMax HVAC 99% Display, PMax Electrical ~86% Display + YouTube.
- Search CPCs: HVAC $45.68 avg ("ac repair near me" $393 for 2 clicks), Electrical $28.95, Plumbing $26.07; impression share 26–33%. Non-branded QS ~4.5, driven by below-average expected CTR on nearly every keyword; landing-page experience mostly average (4 HVAC keywords below average).
- Customer forms Oct 1–15: Search HVAC 3 on $5,985, PMax HVAC 2 on $4,152, Plumbing 3 on $2,242, Search Electrical 17 on $8,483, PMax Electrical 23 on $2,901, Branded 4 on $1,271.
- AI Max–matched terms ran on Search Electrical through 10-08 ($3,622 Sep 15–Oct 8, incl. plumbing and junk); none since. Old paused `Search_Electrical_Services` still has AI Max on (handled by the 10-16 MCC guardrail script).
- PMax final URL expansion is ON in all 3 PMax campaigns (all paused) → must be off before any relaunch.
- No Proud Pops company in any CallRail account TSD's key sees → no call transcripts. Client is getting CallRail (Edu, 10-16).

**Changed (script `proud_pops_account_negatives_1016.py`, validated, read-back confirmed):** 40 PHRASE negatives added to the existing ACCOUNT-LEVEL list `TSD - Account negatives (job seekers)` (12263521315, attached at customer level → covers Search + PMax), list now 66 terms: elmer, above all air, gillette air, sigma air, service experts, wattsmith, goodman phone, appliance repair, roof leak, roofing, nest error, error code, how to, diy + the 26 San Antonio plumbing competitors from `CSMS_Competitors` (previously attached only to one paused campaign). Deliberately NOT added: `phone number` (would block "proud pops phone number" on Branded), `plumer` (misspelling = real intent), appliance words stove/oven/washer/dryer/refrigerator (replay showed they block electrician jobs like "4 prong dryer outlet").

**Recommended before the Nov 1 restore (now in Command Center fu-053, Edu 10-16), not done:** keep PMax HVAC off; relaunch only after CallRail call imports (≥60s) + taps secondary + careers excluded + 2–3 weeks clean data, with goal = forms + CallRail calls only, final URL expansion OFF, HVAC LP, brand exclusions, ~$50/d start. New HVAC landing page + RSA rewrite together (QS is CTR-driven). Electrical Search must not buy plumbing terms again.

---

## 2026-10-14 (2) — Client cut to $25k/month: Branded only for the rest of October. APPLIED

**Ask (Edu, 10-14 ~22:45 CT):** Proud Pops is cutting to $25k/month; adjust so October hits $25k, and set a November check.

**October can't land at $25k.** Spend across the 3 accounts (PPC 1051843378 + LSA 7261668241 + 6621969129) was already
**$28,105 through Oct 14** (Oct 1–13 ran ~$2k/d before the 10-13 cut; Oct 14 = $1,643 PPC + $66 LSA by 22:44 CT). Options put
to Edu: pause everything (~$28.3k), Branded only (~$30k), core Search ~$400/d (~$35k), $25k pace now (~$42k).
**Edu chose Branded only.**

**Applied 22:48 CT** (`branded_only_25k_2026-10-14.py`, validate-only passed, applied, read-back PAUSED on all 5). Status only,
budgets left as they were so the Nov 1 restore starts from known values:

| Campaign | ID | Oct 1–14 spend | Now |
|---|---|---:|---|
| Search Electrical | 23866999121 | $8,483 | PAUSED ($500 budget kept) |
| Search HVAC | 23848895678 | $5,985 | PAUSED ($300) |
| PMax HVAC | 23853595615 | $4,162 | PAUSED ($50) |
| PMax Electrical | 23866982084 | $2,906 | PAUSED ($75) |
| Search Plumbing | 23853484024 | $2,242 | PAUSED ($160) |
| YouTube New Braunfels | 24120482524 | $1,417 | **still ENABLED, pause in UI (fu-046)** |
| YouTube San Antonio | 24120440530 | $1,410 | **still ENABLED, pause in UI (fu-046)** |
| Branded | 23853361615 | $1,215 | ENABLED $100/d |
| LSA (3 surfaces) | | $285 | on, demand-limited |

**YouTube:** the API rejected the VIDEO status change (`--youtube` validate failed, same block as 10-13). Both need the UI.
Each day they run adds ~$200 to October.

**October landing:** $28.1k + Branded ~$100/d + LSA ~$20/d for 17 days ≈ **$30k** (plus ~$200/d of YouTube until paused).

**Nov 1 restore staged, validated, NOT applied:** `nov_restore_25k_2026-11-01.py` → Search Electrical $340, Search HVAC $210,
Search Plumbing $130 (all re-enabled), Branded $100 → $120. **$800/d caps** × 30.4 = $24,320 max + LSA ~$600 ≈ $24.9k.
PMax HVAC / Electrical and both YouTube stay paused (worst cost per customer form; no confirmed calls). Split to be rechecked
against CallRail (fu-048) before it runs. Must run ON Nov 1 CT, not before.

**Command Center:** fu-053 (Nov 1, run the restore), fu-054 (Nov 4, November pacing vs $25k). Updated fu-046 (both YouTube
now), fu-047 (now: confirm Branded-only October holds), fu-048 (CallRail now feeds the Nov 1 split). Client card note updated.
**Superseded:** the 10-13 $50k pacing plan and its Oct 14–27 review window (`budget-cut-2026-10-13.md`, D-10 → D-11).

**Approval:** cut requested by the client via Edu; still needs to go on record (P-3, AM ticket) with the $25k figure and the
~$30k October landing.

---

## 2026-10-14 — Status check after the 10-08 fixes + 10-13 budget cut (read-only)

Scripts: `proud_pops_b7_delivery_check.py`, `proud_pops_verify_careers_fix.py`, `g2b_cutover_2026-10-08.py` (dry run),
`h7_plumbing_general_adgroup_2026-10-08.py cutover` (validate-only), plus scratchpad pulls. Nothing written to the account.

- **Approvals:** 6 B7 ads, 14 G2 RSAs, AG4 RSA 827480907116, "Book a Free Pop-In" sitelink 428522074259, and the unlinked
  (210) 225-5767 call asset 428601259336 are all APPROVED. Old 210-794-7570 call assets still DISAPPROVED (all campaigns show
  CALL_EXTENSION_DISAPPROVED). **G2b and H7a cutovers validated, not run.**
- **Changes since 10-09:** only Edu's 10-13 budget cut + 1 ASSET create by separated.tito@proudpops.com (10-13 14:47, P-8).
- **Forms (Ads `Website lead`, click date) Oct 8–14:** 11 = Electrical 7, Branded 2, Plumbing 1, PMax HVAC 1, Search HVAC 0,
  PMax Elec 0. Electrical ~$480/form ($3,355). GTM fix holding in Ads; one GA4-only /careers leak on 10-12 (E3 note).
- **Block F not started:** Oct 9–14 counted conversions = TSD - Website Call 257.8 vs Website lead 7.0 (97% taps).
- **Search HVAC:** $3,630 Oct 8–14, 0 forms; weekday spend 2× cap since the 10-08 geo widening; 54% of spend outside SA at
  ~2× SA's CPC; competitor terms leaking (elmer, gillette, sigma, holt, north east air, "one hour heating and air") + "pops ac".
- **Search Plumbing (Max Clicks $45 since 10-08):** CPC $38 → $12–25, clicks ~2×, but **0 forms and 0 taps Oct 9–14** ($724,
  47 clicks). Visible terms drift to competitors (patriot, bearded plumber, infinity, air and drain works) and "saws water leak".
- **Pacing:** PPC acct Oct 1–13 ≈ $26.2k. YouTube SA still ENABLED (fu-046). At current caps Oct ≈ $51.3k; with SA paused
  from 10-15 ≈ $49.6k, before any Max Conversions overdelivery.
- **Meta pixel:** Lead events arriving since GTM v43 (26), ~2× GA4 leads.
- **Conversion breakdown, Oct 8–14 vs Sep 30–Oct 6** (`scratchpad pp_conv_breakdown_1014.py`): spend $13,396 vs $13,021.
  Google-counted conversions 330 vs 339; phone-tap share 97% vs 86%. `Website lead` 11 vs 48, but GA4 put 36 of 38 pre-week
  google/cpc leads on /careers, so real customer forms ≈ 5 → 11 (Search Electrical ~3 → 7). Post-week per campaign: Search HVAC
  $3,631 / 0 forms; Search Electrical $3,486 / 7 (~$498); PMax HVAC $1,921 / 1; PMax Elec $1,271 / 0; Plumbing $922 / 1; Branded
  $751 / 2 (**Branded `Website lead` still not biddable: counted 0, all 2**). Search + PMax ≈ $1,090 per customer form. LSA: 1 lead
  (in-account HVAC message 10-08, consumer declined); 6621969129 $0. GA4 google/cpc: 8 customer `generate_lead` on /schedule, 6
  `job_application` (Search HVAC 3, Search Elec 2, PMax Elec 1).
- **Phone taps reported by Google (`TSD - Website Call`, all_conversions):** Oct 8–14 **321** (Search 31, Display 283, YouTube 7);
  Oct 1–14 **605**; Sep 15–Oct 14 **1,312** (Display + YouTube 1,086 = 83%). 30d by campaign: PMax Elec 776, PMax HVAC 365, Search
  Elec 91, Search HVAC 32, Branded 26, Plumbing 23. Call-extension `phone_calls` = 0 in all windows. GA4 `phone_click` from
  google/cpc: 92 / 197 / 433 (~⅓ of Google's count; widest gap on PMax).
- **Follow-up created:** Command Center **fu-052** (due 10-16), get the call extension approved; the 225-5767 asset is already
  approved, only the number check (P-5) blocks it.

---

## 2026-10-13 — Budget cut back to the approved $50k/month (Edu OK). APPLIED

**Full change record + before baseline + review plan: `budget-cut-2026-10-13.md`** (applied 17:17:25 CT by
eduardo@topservdigital.com per change_event; baselines in `budget-cut-2026-10-13/*.json`; re-run with
`budget_cut_review_2026-10-13.py --since 2026-10-14 --until 2026-10-27 --label post14`). Calls check = fu-048 (due 10-16, needs CallRail).

**Why the account was at ~$2,000/d:** the $50k approval was the August pool. By Aug 10 only $6,005 had been spent, so
the Aug 10 and Aug 17 raises (plus YouTube $200/d from Aug 8) were sized to spend ~$44k in the last 21 days (~$2,100/d).
That catch-up rate was never rolled back on Sep 1. Caps $1,960/d x 30.4 = $59.6k/mo: Sept landed $59,635 (PPC acct),
October was heading to ~$60k. No Sept/Oct approval on file (P-3).

**Oct MTD before the cut:** Oct 1–12 $24,185 (PPC acct $24,034 incl. in-account LSA $68, LSA Electrician $151, LSA HVAC $0).
Oct 13 already $1,950 by 17:15 CT. $50k leaves ~$23.8k for Oct 14–31 (18 days) → ~$1,285/d caps.

**Cuts (script `budget_cut_50k_2026-10-13.py`, validate-only passed, applied, read-back OK):**

| Campaign | Before | After | 30d $/customer form (Sep 8–Oct 7) | Post-fix Oct 8–12 |
|---|---:|---:|---:|---|
| PMax HVAC 23853595615 | $295 | **$50** | $4,904 (2 forms, 99% Display) | $1,571, 0 forms, 72 taps |
| PMax Electrical 23866982084 | $230 | **$75** | $2,296 (3 forms) | $1,132, 0 forms, 184 taps |
| Search HVAC 23848895678 | $375 | **$300** | $929 (12 forms) | $2,705, 0 forms, budget-lost 0% |
| Search Electrical 23866999121 | $600 | **$500** | $1,094 (17 forms) | $2,665, 5 forms ($533), budget-lost 19% |
| Search Plumbing | $160 | $160 | $835 | $760, 1 form, budget-lost 62% |
| Branded | $100 | $100 | $302 | $519, 1 form |
| YouTube San Antonio | $100 | **UI: Edu to pause** | 0 leads, kids inventory pre-10-08 | API blocks VIDEO mutations |
| YouTube New Braunfels | $100 | $100 | 0 leads (awareness) | |

Caps $1,960 → $1,385/d now, **$1,285/d once YouTube San Antonio is paused** (H5: "if something gets cut first, cut San Antonio").
Projection: with SA paused, October ≈ $50.2k; without it ≈ $52k. PMax HVAC kept at $50 instead of paused because the full
pause still waits on written client approval (P-2). PMax Electrical at $75 makes D-4 (5 customer forms by Oct 26) unreachable,
which matches the data (0 forms post-fix).

**Next:** recheck pacing ~Oct 20 (overdelivery on Max Conversions can run 2–40% over cap on single days). Nov 1: steady-state
$50k/mo ≈ **$1,600/d caps** (+~$315/d over October's landing rate); where it goes is decided at the Oct 26 review (G3/G4).
AM ticket / client note: spend coming back to the approved $50k (P-3).

---

## 2026-10-08 (night) — 30-day performance report built (Sep 8–Oct 7), customer leads only

Read-only. Client-facing plain PDF: `Proud Pops - 30-Day Performance Report (Sep 8 - Oct 7).pdf` (source
`Proud-Pops-Google-Ads-Performance-Summary_30d-2026-10-07.html`). Scripts in session scratchpad, not saved.

- **Spend $60,391.84:** Search $36,877.54 + PMax $16,696.60 + YouTube $6,028.94 + LSA $788.76 (in-account $134.67,
  Electrician $294.73, HVAC $275.84, legacy roofing $83.52).
- **Customer forms ~47** = Ads `Website lead` all_conv by click date (174) × each campaign's GA4 google/cpc non-/careers
  share (GA4: 95 /careers vs 31 customer). Elec 17, HVAC 12, Plumbing 6, Branded 7, PMax HVAC 2, PMax Elec 3 (99 × 2/78).
  ~127 job apps excluded. **$1,139.88 / customer form** (Search + PMax).
- **LSA:** 18 leads (16 calls, 2 messages), 12 calls ≥ 60s, 5 booked, 11 charged ($71.71 / charged lead), 9 still ACTIVE.
- **Customer leads 65** (47 forms + 18 LSA) → **$836.35 / lead** excl. YouTube.
- **Confirmed PPC calls = 0** (call_view 0 rows, phone_calls 0; call asset still disapproved, CallRail not linked).
- **Phone taps (`TSD - Website Call`) 1,227:** Search network 186 (Elec 101, HVAC 38, Plumbing 27.5, Branded 19.5) +
  PMax 1,041, of which 987 CONTENT/YOUTUBE. GA4 `phone_click` google/cpc = 390 (PMax Elec 223, PMax HVAC 109, Search 58);
  PMax taps include /privacy and /cookie-policy pages.
- Search IS 21.4% (budget-lost 30.6%, rank-lost 48.0%). GA4 sessions vs Ads clicks: PMax Elec 2,143 / 16,139, PMax HVAC
  802 / 8,558.
- **Report states the 174 → ~127 job-app split openly** (one sentence under the campaign table). D-2 (how to restate
  August) is still Edu + Jonathan's call; edit that sentence if they frame it differently.

---

## 2026-10-08 (night) — HVAC search-term sweep + PMax brand exclusion APPLIED

**Authority:** Edu ("execute on 1 and 2"). Both validated, applied, read back.
- **HVAC sweep:** 9 campaign negatives on Search HVAC (competitors airco, cowboys ac, beluga air, sa specialties, atlas ac, ems
  home services, one hour air, statewide ac; BROAD rv). $422.78 / 30d, 0 conversions.
  - Kept: commercial HVAC (site serves commercial), "cheapest" searches, equipment brands, "alamo air conditioning" (2 conv).
  - HVAC terms are clean overall (exact / phrase, no AI Max). The cost problem is CPC / QS, addressed by the G2 ads.
- **PMax brand exclusion:** BRANDS shared set 12263604514 (Google brand entities "Proud Pops" /g/11zy333b8y + "Proud Pops Plumbing,
  Air & Electric" /g/11zbnljsnq) excluded on PMax Electrical + PMax HVAC.
  - Mechanism: negative BRAND_LIST campaign criterion (a campaign_shared_set link is rejected for PMax).
  - Plus PHRASE negatives proud pops / problem solvers / pops electric / pops electrical on both.
  - Brand searches now route to Branded.
- Correction to a 09-09 memory note: brand lists ARE settable via the API now (BrandSuggestionService + BRANDS shared set).

---

## 2026-10-08 (evening) — H4a/b/c, H5a, G1a/b/c, G2a, G2c APPLIED; G2b switchover armed

**Authority:** Edu, one message ("H4a/b/c execute, H5a execute, H5b can't turn off, make sure right people, G1a/b/c execute,
G2a/b execute, H2c execute"). "H2c" was already done, so read as **G2c**. Every step was validated, applied, then read back.

- **Sitelinks (`h4_sitelinks_2026-10-08.py`):**
  - "Contact Us" → https://proudpops.com/contact (new account sitelink)
  - old txproblemsolvers.com Contact Us + 3 dead old-domain sitelinks removed from the account
  - new "Book a Free Pop-In" → /schedule (asset 428522074259) on all 4 Search campaigns, pending review
- **YouTube (`h5_youtube_kids_exclusions_2026-10-08.py`):** campaign-level edits on these video campaigns are blocked by the API
  (MUTATE_NOT_ALLOWED) and the families label is invalid there, so it went in at **account level**:
  - content exclusion BRAND_SUITABILITY_CONTENT_FOR_FAMILIES
  - 34 kids channels (≥ $5 spend; $797 since Aug 8, mostly the SA campaign)
  These also cover PMax's YouTube inventory. Right-people check: 84% connected TV, 18–24 already excluded, age-unknown kept
  (shared household TVs).
- **Location targeting (`g1_geo_2026-10-08.py`):**
  - Branded → 47 cities (the in-account LSA service area, incl. New Braunfels)
  - Search HVAC + Plumbing → 20-city core metro
  - PRESENCE on HVAC, Plumbing, Branded, PMax Electrical
  - Budgets unchanged
- **New ads, G2a + G2c:** 14 site-verified RSAs created next to the current ads. All under review.
  - G2a: Elec AG1 / AG2 / AG3, HVAC AG1 / AG3
  - G2c: Branded × 5, HVAC AG2, Plumbing AG1 / AG2 / AG3
- **G2b:** `g2b_cutover_2026-10-08.py --apply` pauses each old ad only when its replacement is APPROVED. Dry run: all 14 still
  in review, nothing paused.

---

## 2026-10-08 (late) — H4 / H5 / G1 / G2 analysis (read-only) → proposals

Full write-up: [proposals-h4-h5-g1-g2-2026-10-08.md](proposals-h4-h5-g1-g2-2026-10-08.md). Nothing applied.

- **H4:** "/pricing" = a "See Our Pricing" sitelink; sitelink clicks $10.8k / 30d. /pricing converts 3.2% vs homepage 4.3%,
  so keep it. Account sitelink "Contact Us" → old domain; the redirect drops the click ID and lands on the homepage. 3 dead
  old-domain sitelinks are still enabled. No sitelink to /schedule.
- **H5:** YouTube $12.3k since Aug 8.
  - San Antonio VideoViews runs largely on kids' channels (Disney Jr., Bluey, Ms Rachel…) at $0.011 per view.
  - New Braunfels: 76% smart-TV apps.
  - Brand lift unmeasurable: Branded paused late May → Aug 9; GA4 Direct polluted by bots before Aug and cut ~80% late Aug.
    Branded doesn't target New Braunfels.
- **G1:** Branded / HVAC / Plumbing / PMax HVAC target San Antonio city only. Electrical has 5 cities; LSA 47–50.
  Proposal: Branded → 47-city LSA area; HVAC + Plumbing → 20-city core metro; PRESENCE mode.
- **G2:** expected CTR below average on 65–100% of spend in the top 5 ad groups. Current ads contain unverified claims
  ("5-Star" vs actual 4.8; same-day for Electrical / Plumbing). 5 new RSAs drafted with site-verified claims; Google
  validate-only accepted all 5.

---

## 2026-10-08 (afternoon) — H2b, H2c, D-1, D-3, D-5, D-9 executed; D-7 decided

**Authority:** Edu, one message ("H2b both terms approved / turn off AI Max / D-1 execute / D-3 if budget-neutral go /
D-5 can you fix / D-9 go"). All read back.

**Google Ads** (`batch_h2b_h2c_d3_d9_2026-10-08.py`, validate then apply):
- **H2b:** EXACT "pops electric" + "pops electrical" added to Branded Brand_Electrical 193744394062. EXACT negatives for both on
  Search Electrical.
- **H2c:** AI Max OFF on Search Electrical 23866999121. The first attempt was rejected (AI_MAX_MUST_BE_ENABLED: text customization
  depends on AI Max), so the same op set TEXT_ASSET_AUTOMATION to OPTED_OUT. Read-back: enable_ai_max = False, both text
  automations OPTED_OUT.
- **D-3:** Branded 23853361615 $70 → **$100/d**; PMax HVAC 23853595615 $325 → **$295/d**. Total $395 unchanged (budget-neutral
  reallocation, no client approval needed). Both budgets reference_count = 1.
- **D-9:** removed EXACT "electricians for hire" from CSMS_Negatives.

**GTM v43 LIVE 2026-10-08 12:26 CT** (`gtm_d1_d5_2026-10-08.py`):
- **D-1:** trigger [73] cEvent - Appointment Scheduled += Page Path not contains /careers.
- **D-5:** tag [111] Meta Lead now sends standard event **Lead** (was PageView).
- **Process:** draft in ws 44, compile check, then create_version 43 UNPUBLISHED. A private "user" environment (127) pointed at
  v43 for a headless test, then publish, then env deleted. Default workspace is now 45. Rollback = republish v42.
- **Headless test, v42 vs v43** (all hits aborted):
  - /careers "Appointment Scheduled": v42 fired Ads lead + GA4 lead; **v43 fires nothing**.
  - /careers job form: GA4 job_application only (both versions).
  - /schedule customer form: Ads lead + GA4 lead (both versions).
  - Fresh /schedule "Appointment Scheduled": Ads + GA4 (both versions).
  - Note: all lead tags are "oncePerLoad", so a second lead event on the same page load won't re-fire.
- **Meta check:** the headless browser sent no Meta hits at all, but Meta MCP dataset stats show pixel 597145242772352 receives
  PageView ~100–350/hr, phone_click, instant_quote_hvac_click and Webchat Widget, with **0 "Lead" Oct 1–8**. Verify Lead events
  after publish (G5a, Oct 9).
- `ads_get_dataset_details` was blocked by the auto-mode classifier; stats worked.

**D-7 decided:** keep Branded on the homepage. Brand searchers mostly call, the header "Call" button is visible on mobile, and the
schedule CTA is just below the fold. Optional web-team ask → P-14.

---

## 2026-10-08 — H7 BUILT: AG4_Plumbing_General (cutover pending ad approval)

**Authority:** Edu ("Execute H7 now"). Script: `h7_plumbing_general_adgroup_2026-10-08.py` (validate, then apply). Supersedes
July's `change1_plumber_general_adgroup.sh`.

- **Ad group:** AG4_Plumbing_General **199626362094**, ENABLED, in Search Plumbing 23853484024.
- **Keywords:** EXACT plumber san antonio, EXACT plumber near me, PHRASE plumber san antonio tx.
- **RSA 827480907116:** → https://proudpops.com/services/plumbing (Plumber / San-Antonio). 15 headlines, 4 descriptions,
  REVIEW_IN_PROGRESS.
- **Copy claims verified on the live site 10-08:** home, /services/plumbing, water-heaters, leak-detection, /pricing, /about.
  Dropped from the July draft: "same-day" (only on the mailed-letter page), "5-star" (no rating shown), "upfront" (site says
  "written pricing"), "trusted".
- **Cutover (H7a):** pause the 3 generic keywords in AG1_Plumbing_LeakDetection only after the new RSA is approved, so
  Plumbing never goes without an eligible ad.
- **Side finding for B4:** /first-repair shows (210) 864-6867, a different number from the site's 210-CALL-POP (225-5767).

---

## 2026-10-08 — H3a/H3b/H3c APPLIED on Search Plumbing (Edu OK)

Script: `h3_plumbing_changes_2026-10-08.py all` (validate, then apply). All read back.
- **H3a:** paused keyword "leak detection near me" PHRASE (adGroupCriteria/196726297659~297313395770 = PAUSED). It cost $755 / 30d
  at $50.31 CPC, 0.7 all_conv, QS 4. EXACT "leak detection san antonio" stays.
- **H3b:** bidding **Maximize Conversions → Maximize Clicks (TARGET_SPEND), max CPC $45.00**. Read-back: TARGET_SPEND,
  ceiling $45.0. Budget unchanged $160/d. Edu chose to do it now rather than with Block F.
  - Why: 54% of spend went to the 18% of clicks priced over $40, driven by bidding on phone taps.
  - Plumbing will have ~6 real form leads / month after Block F, too thin for Max Conversions.
- **H3c:** PHRASE "aramendia" added to CSMS_Competitors.
- **Watch:** H3d, 7 days once the B7 ads clear review (Plumbing's ads are still under review, so the effect starts after approval).

---

## 2026-10-08 — H3 analysis: Plumbing cost per click (read-only)

`scripts/proud_pops_h3_plumbing_cpc.py`.
- **Setup:** Max Conversions, no target CPA, no CPC cap. Budget $160/d, actual $180–310 on many days.
- **30d:** $5,115, 135 clicks, avg CPC $37.89.

Exact single-click prices (183 search-term-days with 1 click, 60 days), median $12.77:

| CPC | Clicks | Share of clicks | Share of spend |
|---|---:|---:|---:|
| < $20 | 118 | 64.5% | 22.4% |
| $20–40 | 31 | 16.9% | 24.1% |
| $40–60 | 22 | 12.0% | 27.7% |
| $60–100 | 9 | 4.9% | 17.6% |
| $100+ | 3 | 1.6% | 8.2% |

- **Outliers:** almost all are "plumbers san antonio" / "san antonio plumbing" via EXACT "plumber san antonio" (QS 5, expected
  CTR below average). Today's $103.16 was 1 click at 06h CT on "plumbers san antonio".
- **Worst keyword:** "leak detection near me" PHRASE: $755 / 30d, $50.31 CPC, 0.7 all_conv, QS 4.
- **Root lever:** generic plumber terms sit in the Leak Detection ad group (expected CTR below average) → H7.

Follow-ups H3a (pause leak detection near me), H3b (CPC ceiling, ideally with Block F), H3c (aramendia competitor).

---

## 2026-10-08 — H2 APPLIED: 36 negatives on Search Electrical (search-term sweep)

**Authority:** Edu ("execute on H2 now"). Script: `h2_electrical_negatives_2026-10-08.py` (validate, then apply).
Analysis: `scripts/proud_pops_h2_electrical_terms.py`.

**Data:** 2,217 distinct terms, $10,567 visible spend (Sep 8–Oct 7). Match source:

| Source | Spend | Clicks | All conv | $ / all conv |
|---|---:|---:|---:|---:|
| Advertiser keywords | $5,981 | 197 | 46.0 | $130 |
| AI Max broad match | $1,858 | 98 | 14.5 | $128 |
| AI Max keywordless | $2,728 | 97 | 10.5 | $260 |

The worst terms came via AI Max keywordless: "goodman phone number" $176, "plumer" $172 (1 click), "american home shield customer
service" $109, "plumbers san antonio" $154, plus AC terms and a Spanish AC-maintenance query.

**Applied:** 25 competitor PHRASE + 11 off-service negatives (listed in checklist H2). Read-back 36/36.
- 0 collisions with own keywords; 0 core customer-intent terms blocked.
- Terms they'd have blocked: ~$2,374 / 30d.

**Held:** "pops electric" / "pops electrical". Branded has only "proud pops …" keywords, so negating these first would drop
those brand searches. They need Branded keywords first (H2b).

**Open decision:** AI Max search-term matching on Electrical (H2c).

---

## 2026-10-08 — H1 APPLIED: AI Max final URL expansion OFF on Search Electrical

**Authority:** Edu ("execute on H1"). Script: `h1_electrical_url_expansion_off_2026-10-08.py` (validate, then apply).

- Before: ai_max = True; TEXT_ASSET_AUTOMATION OPTED_IN; FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION OPTED_IN.
- After (read-back): ai_max = True; TEXT_ASSET_AUTOMATION OPTED_IN; **FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION OPTED_OUT**.
- **Why:** only 44% of Electrical's 30-day spend landed on the ad URL. Google was sending clicks to /pricing (26%), a generator
  blog post, and HVAC / plumbing / city pages, and could override the new /services/electrical URL (B7).
- **Left on deliberately:** AI Max search-term matching (judge after H2) and text customization.
- Client-enabled setting (Brandon, Jun 26) → FYI to client tracked as P-13.
- Verification: H1a, ~Oct 13.

---

## 2026-10-08 — Campaign review: AI Max URL expansion on Electrical; campaign backlog (checklist Block H)

Read-only.
- **Networks:** Search Partners + Display OFF on all 4 Search campaigns.
- **Search Electrical 23866999121:** AI Max ON + FINAL_URL_EXPANSION OPTED_IN (client-enabled Jun 26). Over 30 days only 44% of
  its spend landed on the ad URL (homepage). The rest: /pricing 26%, a generator blog post 5%, /services/electrical 10%,
  HVAC / plumbing / city pages ~10%.
- **/pricing:** takes 20–26% of Search clicks in every campaign (~$8.1k / 30d), probably a sitelink.
- **AG4_Plumbing_General** (July Change 1) was never built.

Backlog H1–H8 added to [internal-checklist-2026-10.md](internal-checklist-2026-10.md).

---

## 2026-10-08 — Legacy roofing LSA PAUSED; LSA lead-handling review (P-6 groundwork)

**Roofing LSA (Edu: "pause the ads in the roofing account"):**
- Account 3477779749 "[Old Account] The Problem Solvers - LSA Roofing San Antonio" was ENABLED / SERVING at
  $142.86/day.
- Spend history: $2.7k in Jan–Mar 2025, silent Apr 2025–Apr 2026, live again from May 2026 (182 impressions since Jun).
- Charged **$83.52 on Sep 11 for a roofing call that was then DECLINED**.
- Paused campaign 20805107400 (`pause_roofing_lsa_2026-10-08.py`, validate then apply). Read-back: status PAUSED,
  primary_status PAUSED.
- The other 6 legacy PS LSA accounts were already PAUSED with 0 impressions / $0 / 0 leads since Jun 1.

**LSA lead handling (`proud_pops_lsa_lead_handling.py`, no consumer PII pulled), all 3 live surfaces:**

| Month | Leads | Declined | Booked | Still active | Charged | Credited |
|---|---:|---:|---:|---:|---:|---:|
| Jun | 109 | 61 | 34 | 12 | 80 | 7 |
| Jul | 92 | 45 | 47 | 0 | 74 | 4 |
| Aug | 51 | 10 | 37 | 1 | 40 | 1 |
| Sep | 22 | 7 | 6 | 9 | 12 | 0 |
| Oct 1–7 | 3 | 0 | 0 | 3 | 3 | 0 |

- **Calls are answered:** September had no 0-second calls; 15 of 21 calls ran over 60 seconds.
- **Messages are not:** the last 2 (Sep 19 in-account duct cleaning, Oct 3 Electrician outlets/switches) got no reply.
- **Charged then declined:** 2 Sept Electrician leads (Sep 3, Sep 6 light-fixture repair). Credits dropped to 0, so nobody
  is disputing.
- **Read:** lead handling doesn't explain the impression collapse. Profile settings (D2) are the next suspect.
  Specific client asks written into P-6.

---

## 2026-10-08 — B4 REVERTED (Edu checking which number is correct)

`block_b_changes_2026-10-07.py b4-revert --apply`. Read-back: all 7 links to asset 428601259336 ((210) 225-5767) are REMOVED
(account + 6 lead campaigns). Call extensions are back to the pre-B4 state: only the old disapproved 210-794-7570 links.
The new asset never served (it was still under review). The unlinked asset stays in the library for reuse.
Next: Edu confirms the correct number (main line vs CallRail; see P-5), then redo B4 with it.

---

## 2026-10-08 — B4 ON HOLD: where 210-225-5767 came from; CallRail swaps nothing on the site

**Edu:** "hold on B4 - where did you get that number from exactly?" B4 had already been applied minutes earlier.
The new asset 428601259336 is still under review, so it isn't serving yet.

**Source of 210-225-5767:**
- Sep 3 live site fetch: header, CTA, meta description. It's the "210-CALL-POP" vanity number.
- The old GTM phone tag's phoneConversionNumber.
- 10-08 headless checks: the only tel: link for a direct visit, a simulated Google Ads click (gclid + utm google/cpc),
  and after Accept All.

**CallRail:** swap.js (company 686172931) has no swap targets (`session_exact_targets: []`), so CallRail replaces no number
on proudpops.com. The origin of the old 210-794-7570 is unknown. It may be a CallRail call-extension number Google
couldn't verify. Added to P-5.

**Revert ready, not run:** `block_b_changes_2026-10-07.py b4-revert --apply` (validate-only passed). b4-cleanup is on hold.

---

## 2026-10-08 (midday) — B1, B2, B2b, B4 APPLIED (Edu OK)

All read back from the API. Scripts: `block_b_b1_b2_2026-10-08.py` (b1/b2/b2b), `block_b_changes_2026-10-07.py` (b4).

- **B1:** negative WEBPAGE criterion "URL contains /careers" on PMax Electrical 23866982084 and PMax HVAC 23853595615
  (criterion 2501539306220 on both, ENABLED). Stops Final URL expansion sending traffic to the job page.
- **B2:** new account-level negative list **12263521315** "TSD - Account negatives (job seekers)", attached to the account
  (customerNegativeCriteria/2502916073266). It covers PMax too.
  - BROAD: careers, career, apprentice, apprenticeship, salary, employment, indeed, resume
  - PHRASE: now hiring, who's hiring, hiring now, near me hiring, job openings, jobs near me, electrician/electrical/
    plumbing/plumber/hvac jobs, hvac technician job(s), hvac tech jobs
  - The original single-word "job/jobs/hiring" plan was dropped: the collision check showed it would block
    "electrician near me for small jobs" and "hiring electrician near me".
- **B2b:**
  - Removed BROAD `job` + `jobs` from CSMS_Negatives (blocked customer "small jobs" searches on Search). 756 members left.
  - Added PHRASE electrician job / plumber job / hvac job / hvac tech job to the account list (26 total).
- **B4:** new call asset **428601259336** (210) 225-5767 → Calls from ads (60s), linked at account level + all 6 lead
  campaigns. REVIEW_IN_PROGRESS. Old disapproved 210-794-7570 links stay until it's approved (then `b4-cleanup`).
- **Watch:**
  - B7 ads still under review (edited 11:32:56 CT).
  - Plumbing Search delivery very light since midnight, which started BEFORE today's changes.
  - New D-9: EXACT negative "electricians for hire" in CSMS_Negatives is probably customer intent.

---

## 2026-10-08 — Checklist B3, B5, B7 APPLIED (B4 left open on purpose); E1 passed

**Authority:** Edu, in-session: "execute on B3, B5 and B7 - keep the other ones open". Script:
`block_b_changes_2026-10-07.py <step> --apply`. Every change read back from the API afterwards.

- **E1 PASS:** since the v42 publish, GA4 has 5 `job_application` on /careers and **0 `generate_lead` on /careers**.
  Customer leads still fire (2 `generate_lead` on /schedule).
- **B3:**
  - Added PHRASE `beyer` + `bryco` to CSMS_Competitors (11334178042).
  - Attached CSMS_Competitors to Search Plumbing 23853484024 (ENABLED).
- **B5:** `Calls from ads` (6569241485) minimum duration 15s → **60s**, read back = 60.
- **B7:** 6 ads switched to service pages, read back:

  | Ad | Ad group | New final URL |
  |---|---|---|
  | 809528123698 | AG1_Electrician_NearMe | /services/electrical |
  | 809490621054 | AG2_Electrical_Services | /services/electrical |
  | 809490671193 | AG3_Electrical_Repair | /services/electrical |
  | 808814916930 | AG1_Plumbing_LeakDetection | /services/plumbing |
  | 808929407402 | AG2_Plumbing_Emergency | /services/plumbing |
  | 808929711767 | AG3_Plumbing_WaterHeaters | /services/plumbing/water-heaters |

  **All 6 under review** (PENDING / REVIEW_IN_PROGRESS). They're the only enabled ads in Electrical and Plumbing Search,
  so those campaigns may not serve until approved. Rechecks: checklist B7a/B7b.
- **Left open on purpose:** B4 (call extension), plus Edu's UI items B1, B2, C1, C2, D2.

---

## 2026-10-07 (afternoon) — Checklist progress: B3/B4/B5/B7 validated (not applied), B6 + D1 done, fix confirmed by real traffic

**Edu:** "keep executing on the checklist". No live Google Ads writes this session; all four prepared changes wait on his OK.

- **Fix confirmed by real users:** GA4 shows 3 real `job_application` events on /careers (11:00/12:00/13:00 CT) and 0
  `generate_lead` on /careers after the v42 publish.
- **B3 review:** CSMS_Competitors' 23 members are all EXACT. 0 collisions with own keywords; blocks nothing in 90 days.
  Proposed PHRASE `beyer` + `bryco` would block 3 terms ($87.41).
- **B6:** /services/electrical, /services/plumbing, /services/plumbing/water-heaters all pass on desktop + mobile
  (CTA to /schedule above the fold, tel:210-225-5767, no errors). Mobile homepage has no visible schedule CTA above the fold.
- **B3/B4/B5/B7:** `block_b_changes_2026-10-07.py` written; validate-only accepted by Google (3 / 8 / 1 / 6 ops).
- **D1:** LSA weekly snapshot. HVAC LSA 6621969129 has had zero impressions since wk Sep 21; in-account LSA none
  since wk Sep 28; Electrician LSA declining (90 impressions wk Oct 5, partial).
- **September spend:**
  - Proud Pops total $60,422.56 (PPC acct $59,635.16 + LSA [1] $387.54 + LSA [2] $399.86)
  - Legacy PS Roofing SA LSA 3477779749 spent **$83.52** (supposed to be dormant)
  - MFSC (separate) $2,072.42
- New scripts: `proud_pops_spend_and_lsa_d1.py`, `proud_pops_b3_competitor_review.py`, `proud_pops_b6_page_check.py`
  (skill scripts dir); `block_b_changes_2026-10-07.py` (client folder).

---

## 2026-10-07 — End of morning session: state + resume point

**Resume from:** [internal-checklist-2026-10.md](internal-checklist-2026-10.md), section "▶ RESUME HERE". It holds:
the ordered next steps, open decisions D-1 to D-6, the AM/client tracker P-1 to P-12, pre-fix baselines, watch-outs,
and the script list.

- **Live:** GTM v42 (careers job applications out of lead tracking) since 10:32 CT. Nothing else changed in Ads/GA4.
- **Urgent:** client heads-up (P-1) not sent; lead counts started dropping at 10:32 CT.
- **Tomorrow:** E1 via `./tsd.sh proud_pops_verify_careers_fix.py` (baseline 5.00 `Website lead`/day → expect ≈ 1.2).
- **Saved** the session's analysis scripts to `.claude/skills/google-ads-ratos/scripts/proud_pops_*` (the scratchpad
  is session-only).

---

## 2026-10-07 — GTM Block A: job applications out of lead tracking. LIVE v42

**Checklist:** [internal-checklist-2026-10.md](internal-checklist-2026-10.md) Block A. Edu said "execute block A".

Workspace 43 (GTM-WBFDB6L8), draft only. Live is still **v41**, so nothing changed on the site.

- A1: live v41, ws 43 clean, 0 conflicts.
- A2: variable **124** `dlv - ghl_form_id` (DLV `ghl_form_id`, v2).
- A3: trigger **80** `cEvent - Lead` now also requires `{{Page Path}}` not containing `/careers` AND
  `{{dlv - ghl_form_id}}` not equal to `ThmcYYHImwSoYS9oBt3n`. This feeds [82] G.Ads Lead, [90] GA4 Lead,
  [94] G.Ads UPD and [111] Meta Lead.
- A4: trigger **125** `cEvent - Job Application` (ghl_form_submit + Page Path contains /careers).
- A5: tag **126** `06 | GA4 - Job Application` (GA4 event `job_application`, page_location), cloned from [90].
- A6: getStatus = exactly those 4 changes; quick_preview compiles with no errors; listeners [99]/[123] identical to live.

Not tested by this: whether the real careers form also emits `Appointment Scheduled` (trigger [73] still fires
[82]/[90]/[111] with no careers exclusion). It's caught by checklist E1/E3 after publish.

**PUBLISHED 2026-10-07 12:32 BRT (10:32 CT) as live v42** "TSD - Exclude careers job applications from lead
conversions (2026-10-07)", on Edu's "make it go live". Default Workspace is now 44. Rollback = republish v41.

Edu didn't run GTM Preview. The first publish attempt was blocked by the auto-mode classifier ("blind apply"), so
the draft was tested first, headless (`scripts/proud_pops_gtm_headless_test.py`). Method: load the real
proudpops.com in Playwright, serve the draft container (env-6, workspace preview auth), push fake `ghl_form_submit`
events, and intercept + abort every GA4/Ads/Meta request so nothing is recorded.

| Scenario | Live v41 (control) | Draft → live v42 |
|---|---|---|
| /careers, with job form id | Ads lead + GA4 generate_lead | GA4 job_application only |
| /careers, no form id | Ads lead + GA4 generate_lead | GA4 job_application only |
| HVAC page → /schedule (in-app) | Ads lead | Ads lead + GA4 generate_lead |
| Homepage → /schedule (click) | Ads lead + GA4 generate_lead | Ads lead + GA4 generate_lead |

The re-run against the published v42 (no override) was identical. Next: E1 on Oct 8 (first clean full day).

---

## 2026-10-07 — Weekly check (Sep 30–Oct 6): $248/form lead; PMax HVAC has been 100% Display since Aug 24

**Trigger:** Edu asked for Proud Pops results.

**Read-only session. No changes made to the account.**

**Basis:** lead-gen = Search + PMax. Excludes the 2 YouTube campaigns ($1,396/wk, zero conversions by design)
and the in-account LSA campaign ($0 this week). Real leads = `Website lead` all_conversions.

| Sep 30–Oct 6 | Spend | Form leads | $/form | Phone clicks |
|---|---:|---:|---:|---:|
| Nonbranded Electrical (Search) | $4,419 | 10 | $442 | 20.5 |
| PMax HVAC | $2,273 | 2 | $1,136 | 74 |
| Nonbranded HVAC (Search) | $1,897 | 2 | $948 | 3 |
| PMax Electrical | $1,456 | 28 | $52 | 177 |
| Nonbranded Plumbing (Search) | $1,148 | 3 | $383 | 7.5 |
| Branded (Search) | $482 | 2 | $241 | 2 |
| **Total** | **$11,674** | **47** | **$248** | **284** |

Prior 7 days (Sep 23–29): $11,154, 23 forms, $485/form. Weekly forms (Mon weeks from Aug 31): 35, 45, 52, 32, 43,
so this week is a return to normal, not a step up. $/form has sat at ~$250–370 for 5 weeks.
Google-reported: 329 conv / $35 CPL, of which 284 (86%) are `TSD - Website Call` phone clicks. Search-only CPC $27.31.
Account Search IS 22.9% (prev 17.3%), lost to budget 22.7%, lost to rank 54.4%. Branded IS 62.7%, 23.7% budget-lost.

**September full month:** lead-gen $53,419, 173 forms, $309/form. Total account incl. YouTube + LSA $59,635.
**October pace:** $11,566 in Oct 1–6 → ~$59.8k/month. Daily caps unchanged at ~$1,960/d. Still no written
Sept/Oct approval on record (last approved = $50k for August).

**Gate 0 still not done (5 weeks after the plan).** `TSD - Website Call` is PHONE_CALL_LEAD / CALL_FROM_ADS and that
bucket is biddable on every lead campaign. It shares the bucket with `Calls from ads`, which has recorded 0 since
2026-05-04, so turning the bucket off loses no real signal.

**PMax HVAC zero-forms cause found: it became a Display campaign.** Weekly network split of its spend:
Search 70% (wk Jul 27, 13 forms) → 31% (wk Aug 10, 26 forms) → 7% (wk Aug 17, 2 forms) → **0% from wk Aug 24 on,
~$2.2–2.4k/wk on CONTENT (Display), 0 forms** (2 forms wk Sep 28). Every form it ever produced came from its Search
slice. The shift lines up with the $27 target CPA set 2026-08-10: with phone clicks as the biddable signal, Display
taps hit $27 easily (it reports $29.9 this week, right on target). Same landing page as Search HVAC
(`/proud-pops-hvac-services`), but phone clicks per form are 37:1 from PMax HVAC vs 1.5:1 from Search HVAC, so the
Display "phone clicks" are very likely junk taps. Not verified against CallRail.

**PMax Electrical is starting the same drift.** Display share 0% (Aug) → 19% → 29% → 41% → 46% (wk Sep 28) → 61%
(Oct 5–6 partial). All its forms come from its Search slice (wk Sep 28: Search $305 → 27 forms; YouTube + Display
$1,253 → 0). It has no target CPA, so the pull is the phone-click goal alone.

**Change history since Sep 23:** only 4 ASSET creates by `tito@proudpops.com` (client side) on Oct 1 and Oct 4. No
TSD changes. Nothing from the Sep 24 open list has moved.

### Still open

- [ ] **Gate 0:** set PHONE_CALL_LEAD / CALL_FROM_ADS non-biddable on all lead campaigns (`campaign_conversion_goal`,
      explicit FieldMask on `biddable`). Warn whoever reads the UI: Conversions column drops; compare on all_conversions.
- [ ] **PMax HVAC:** pause (~$9.9k/mo of Display, ~0 forms). Doing it also brings October pace from ~$59.8k back to
      ~$50k. Spend change → AM ticket.
- [ ] **PMax Electrical:** recheck Display share one week after Gate 0.
- [ ] Sept/Oct budget approval on record via AM ticket.
- [ ] Ask who `tito@proudpops.com` is and what the Oct 1/4 assets are.

### Follow-up same day: confirmed phone calls from Google

**PPC: zero confirmed calls.** Call asset (210) 794-7570 is still `NOT_ELIGIBLE / ASSET_DISAPPROVED` on the account
level and all 6 live campaigns (unverified number, open since 2026-09-03). `metrics.phone_calls` = 0 for September and
for Sep 30–Oct 6. Last `call_view` record on a live-structure campaign: 2026-05-07 (June calls were the now-paused Water
Softening campaign). Real calls from PPC site visitors exist only in CallRail (site number swap); not accessed.

**LSA (Google-verified calls) has collapsed.** All 3 surfaces (in-account, 7261668241, 6621969129):

| Month | LSA spend | Leads | Phone calls | Charged calls |
|---|---:|---:|---:|---:|
| Jun | $6,793 | 109 | 88 | 59 |
| Jul | $6,273 | 92 | 71 | 53 |
| Aug | $3,084 | 51 | 33 | 22 |
| Sep | $923 | 22 | 21 | 11 |
| Oct 1–6 | $151 | 3 | 2 | 2 |

Sep 30–Oct 6: 2 confirmed calls + 1 message, all from 7261668241 (Electrician). Weekly LSA impressions: in-account
~800 (wk Jul 27) → 110 (wk Aug 17) → ~50–150 since, none in some weeks; 6621969129 ~600–700/wk through Aug → 351 (wk
Sep 14) → no impressions since; 7261668241 ~300/wk → 171 (wk Sep 28). All 3 LSA campaigns read ENABLED / SERVING /
ELIGIBLE at $714/d with no change events since 09-08, so the cause is not visible in Google Ads. It has to be checked in
the LSA dashboard (profile paused or budget, job types, business hours, verification or insurance lapse, ranking from
reviews and responsiveness). Sept lead status: 7 of 22 DECLINED, 10 of 21 calls not charged.

- [ ] Verify 210-225-5767 as the call asset (swap out the disapproved 794-7570). That makes `Calls from ads` a real,
      duration-qualified signal to bid on after Gate 0.
- [ ] CallRail → Google Ads integration for qualified website calls; confirm whether it's connected.
- [ ] LSA dashboard check on all 3 profiles: why impressions fell from ~1,900/wk combined to near zero.

### Follow-up 2, same day: ~3 in 4 "form leads" are JOB APPLICATIONS (30-day check, Sep 7–Oct 6)

**This corrects the per-campaign form CPLs above and in every check since 2026-07-23.**

`/careers` ("Join the Family - HVAC Plumbing Electrical Jobs San Antonio") embeds a GHL job application form
(`leadnurturemachine.com/widget/form/ThmcYYHImwSoYS9oBt3n`). Its submit fires the same `ghl_form_submit` →
`05 | G.Ads - Lead` → `Website lead` (and GA4 `generate_lead`) as the customer `/schedule` form. GA4 google/cpc
`generate_lead` by event pagePath, Sep 7–Oct 6: **/careers 99, /schedule 25, /proud-pops-hvac-services 7** (131 total vs
Ads 180; GA4 undercounts under Consent Mode). Site-wide all sources: /careers 131 of 193.

| Sep 7–Oct 6 | Spend | Ads forms | GA4 job apps | GA4 customer | Est. customer forms | $/customer form |
|---|---:|---:|---:|---:|---:|---:|
| Search Electrical | $18,569 | 35 | 9 | 10 | ~18 | ~$1,010 |
| Search HVAC | $11,001 | 15 | 2 | 8 | ~12 | ~$920 |
| PMax HVAC | $9,814 | 2 | 0 | 2 | 2 | ~$4,900 |
| PMax Electrical | $6,735 | 103 | 79 | 2 | ~3 | ~$2,650 |
| Search Plumbing | $5,130 | 9 | 3 | 5 | ~6 | ~$910 |
| Branded | $2,106 | 16 | 6 | 5 | ~7 | ~$290 |
| **Total** | **$53,355** | **180** | **99** | **32** | **~48** | **~$1,115** |

Est. = Ads forms × that campaign's GA4 customer share. Per-campaign GA4 samples are small (2–81), total is solid.
Ads-side count is otherwise clean: `Website lead` ONE_PER_CLICK, last click; click-date 180 vs conversion-date 188.

**Mechanism:** both PMax campaigns have `FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION` OPTED_IN. GA4: 176 PMax Electrical
sessions landed directly on /careers. `Website lead` is biddable (SUBMIT_LEAD_FORM/WEBSITE), so PMax is optimizing toward job
applicants. Job-seeker search terms on Search campaigns are negligible ($15 of $10.7k visible), so Search job apps come
from visitors browsing to /careers after a service click.

**Corrections to earlier today:**
- PMax Electrical is NOT the efficient campaign. 79 of its 81 GA4 forms were /careers.
- PMax HVAC's August forms were job applications too (GA4 Aug: 41 careers / 1 customer). Its "forms dropped to 0 after
  the Display shift" lost job applicants, not customers. Pause recommendation stands (~$9.8k/mo of Display phone taps).
- **Gate 0 must NOT go first.** With phone clicks off, `Website lead` becomes the only biddable signal and PMax Electrical
  would chase job seekers harder. The careers fix goes first.
- The Jul 23–Aug 16 "pre-ramp" $120–167/form baseline also included job apps (/careers leads start wk of Jul 27).

**August client report (sent Sep 3)** stated 129 form leads / $256.22 CPL and called PMax "the strongest cost per lead".
GA4 Aug google/cpc: 104 /careers vs 28 customer (79% job apps). It also labeled 1,069 phone-link clicks as "Calls to your
business line". Edu + AM to decide how to handle; the September report must not repeat either.

- [ ] **GTM first:** exclude /careers from the `05 | G.Ads - Lead` trigger (and GA4 generate_lead); send careers submits
      as their own `job_application` event, non-primary. Publish separately with Edu's OK.
- [ ] Both PMax: add /careers as a URL exclusion (or opt out of final URL expansion).
- [ ] Then Gate 0 + pause PMax HVAC.
- [ ] Recheck all campaign CPLs on customer-only forms 2 weeks after the GTM fix.

**Execution checklist (tick as we go):** [internal-checklist-2026-10.md](internal-checklist-2026-10.md).
**Plans:** [internal-action-plan-2026-10-07.md](internal-action-plan-2026-10-07.md) (account work) + [am-client-action-plan-2026-10-07.md](am-client-action-plan-2026-10-07.md) (AM/client). Background: [action-plan-2026-10-07.md](action-plan-2026-10-07.md) (GTM spec for trigger [80], Preview test, PMax
URL exclusion, phone taps → Secondary not goal-off, call asset + CallRail, LSA check, re-baseline Oct 26).

---

## 2026-09-24 — September MTD check (Sep 1–24): Gate 0 still not landed; real CPA $293/form lead; PMax HVAC dead on forms

**Trigger:** Edu asked for this month's PPC results.

**Read-only session — no changes made to the account.**

**Headline:** Google reports 1,048 conversions / $45.8 CPL. That figure is not usable. `TSD - Website Call`
(phone click) is still `primary_for_goal=True` and accounts for **916 of 1,048 (87%)**. Gate 0 from the
[Sept/Oct plan](september-october-plan-2026-09-03.md) (demote that action) is still open 3 weeks later.
`Calls from ads` = 0 this month (last fired 2026-05-04).

**Basis:** PPC only. Excludes the system-generated LSA campaign ($135 in Sept vs $1,459 in Aug 1–24) and
the two YouTube campaigns (`08/2026 - YT - Awareness - New Braunfels`, `08/2026 - YT - VideoViews (San
Antonio)`, $100/d each, $4,804 MTD, zero conversions by design). Real leads = `Website lead` form fills
(`all_conversions` 147; 130 counted in bidding, the 17 gap not chased). Search + PMax = "lead-gen spend".

| | Aug 1–24 | Sep 1–24 |
|---|---:|---:|
| Lead-gen spend | $28,104 | $43,076 |
| Form leads | 117 | 147 |
| $/form lead | $240 | $293 |

Spend +53%, forms +26%. Marginal: $14,972 extra for 30 extra forms = **~$500 per incremental form lead.**

| Campaign (Sep 1–24) | Spend | Forms | $/form |
|---|---:|---:|---:|
| Nonbranded Electrical (Search) | $14,699 | 29 | $507 |
| Nonbranded HVAC (Search) | $9,343 | 16 | $584 |
| PMax HVAC | $7,823 | **0** | n/a (280 phone clicks) |
| PMax Electrical | $5,485 | 78 | $70 |
| Nonbranded Plumbing (Search) | $3,972 | 7 | $567 |
| Branded (Search) | $1,754 | 17 | $103 |

Branded vs unbranded (PMax counted as unbranded per Edu's rule): branded $103/form,
unbranded $41,322 / 130 = $318/form. Weekly $/form (excl YT/LSA): wk Aug 10 $167, Aug 17 $401, Aug 24 $446,
Aug 31 $343, Sep 7 $298, Sep 14 $262 (improving 3 straight weeks, still above the pre-ramp $167).

**PMax HVAC form leads: 27 (wk Aug 10) → 2 → 0 for five straight weeks** at a constant ~$2.3k/wk. Phone
clicks keep reporting (43–212/wk). PMax Electrical forms rose over the same weeks (12 → 28/wk) and Search
HVAC forms are non-zero, so the site form tag fires. Cause NOT determined: tracking break specific to the
HVAC path vs genuinely bad traffic. `change_event` only reaches 30 days back, so the ~Aug 17 trigger
needs the Google Ads UI change history. Only change events in Sept: 4 ASSET creates on 09-03
(access@topservdigital.com).

**Impression share (Search, Sep 1–24):** account 21.8%. Nonbranded HVAC 26.2% (rank-lost 63.6%),
Electrical 27.6% (57.6%), Plumbing 13.7% (69.4%). Branded 72.4% IS, **20.5% lost to budget** at $70/d
while being the cheapest lead source.

**Budget:** live daily caps sum to ~$1,960/d (~$58.8k/mo), MTD pace ~$60k vs $50k approved for August.
No written September approval on record in my notes. Per workspace rule, budget changes need written
client approval via the AM ticket.

**Caveat:** $293 is cost per form lead only. Phone clicks are an intent signal with no call-quality
validation (no CallRail/ServiceTitan cross-check done), so this is an upper bound on cost per lead of
all types, not the true blended CPA.

**GAQL gotcha (new):** segmented `FROM campaign` queries return `cost_micros` as real micros in a
string (divide by 1e6). Unsegmented `insights.py` returns it pre-converted. Mixing the two heuristics in
one script blows up with `'>' not supported between 'str' and 'float'`.

### Still open

- [ ] **Gate 0:** demote `TSD - Website Call` to non-primary. Not executed (live bidding change on a
      client account; asked Edu, no answer yet). Expect a short Smart Bidding relearn dip.
- [ ] **PMax HVAC zero forms since ~Aug 17:** check UI change history around Aug 14–20, then test the
      HVAC form path in GTM Preview (workspace 38) to split tracking vs traffic.
- [ ] **Sept budget approval:** get it on record via the AM ticket; pace is ~20% over August's $50k.
- [ ] **Branded budget cap:** $70/d loses 20.5% IS to budget at $103/form. Cheap candidate for a raise,
      but that is a budget change, so it needs the approval above first.
- [ ] **LSA campaign inside this account:** $135 vs $1,459 in Aug 1–24, not investigated.

---

## 2026-09-14 — Keyword & search-term reports built, one per industry (HVAC/Electrical/Plumbing)

**Trigger:** Edu asked for a keyword + search-term report per industry, best keywords and actual
search queries together, branded traffic disregarded entirely (industry keyword research, not a
performance/brand audit).

**Read-only session — no changes made to the account.**

Pulled full lifetime data for the current campaign structure (2026-05-14 to 2026-09-13):
- Keywords via `ad_group_criterion` for the three live non-branded Search campaigns: HVAC
  (`23848895678`, 24 keywords), Electrical (`23866999121`, 45 keywords), Plumbing (`23853484024`,
  24 keywords).
- Search terms via `search_term_view`, queried **per campaign** (not the shared `read.py
  search-terms` command, which caps at one global `LIMIT` ordered by cost across all campaigns and
  was starving HVAC/Plumbing rows behind Electrical's much larger long tail). Full counts: HVAC
  1,163 distinct non-branded terms, Electrical 3,052, Plumbing 444.
- Stripped every Proud Pops / The Problem Solvers / My Favorite Service Company mention from both
  keyword and search-term tables (regex match, confirmed contamination existed pre-filter: 2 hits in
  HVAC, 20 in Electrical, 2 in Plumbing — all inside "nonbranded" campaigns via loose match types).

**PMax has no keyword or search-term data exposed via the API** (no manual keyword targeting, and
Performance Max's Search Terms Insights isn't queryable through this pipeline) — so HVAC and
Electrical's companion PMax campaigns (`23853595615`, `23866982084`) are out of scope by definition,
noted explicitly in each report. Plumbing has no active PMax at all (both prior attempts paused,
zero lifetime spend).

Each report has 3 sections: all current keywords ranked by conversions, top-40 converting search
terms with the keyword they actually matched (a gap between term and matched keyword flags a
same-exact-match candidate), and top zero-conversion terms by volume (negative-keyword or new-ad-group
candidates). Section 3 of the Plumbing report surfaced several competitor names riding on broad/phrase
match (Beyer Boys, The Bearded Plumber, George's Plumbing, Bryco) — not Proud Pops' own brand so left
in per Edu's ask, flagged for a possible negative-keyword pass.

**Delivered as PDF** (Georgia serif, plain b/w, print-margins) built by converting the markdown to
HTML and printing via headless Brave (`--headless --print-to-pdf`) — no pandoc/wkhtmltopdf/weasyprint
installed on this machine, Brave was the only browser binary available locally.

Saved in `clients/proud-pops/`, `.md` source + `.pdf` per industry:
- `Proud Pops - Keyword & Search Term Report (HVAC).md` / `.pdf` (6 pages)
- `Proud Pops - Keyword & Search Term Report (Electrical).md` / `.pdf` (8 pages)
- `Proud Pops - Keyword & Search Term Report (Plumbing).md` / `.pdf` (6 pages)

---

## 2026-09-03 — Branded campaign missing the form-lead conversion goal; verified the 8 uncounted leads are real via GA4

**Trigger:** Edu asked whether "0 conversions, 17 calls" on Branded is normal.

**Correction on the framing first:** Branded's official Conversions total is 17, not 0 — all 17 are
the phone-click type (`TSD - Website Call`), which IS a counted/biddable conversion for this
campaign. If "0" is showing up anywhere, it's a form-only view.

**The real finding:** pulled `campaign_conversion_goal` for Branded (`23853361615`) and found it's
the only live campaign in the account where `SUBMIT_LEAD_FORM/WEBSITE` is **not** in the biddable
goal set (`PHONE_CALL_LEAD/CALL_FROM_ADS` and `DEFAULT/WEBSITE` are; form-lead is not). Every other
live campaign (HVAC Search, Electrical Search, Plumbing Search, PMax HVAC, PMax Electrical) has it
and shows real counted form leads (10, 15, 3, 44, 57 respectively for August). Branded's
`all_conversions` shows **8 real `Website lead` fires** that never make it into the official
Conversions column because of this gap.

**Verified the 8 are real, distinct people, not double-counted against the 17 calls** — Edu pushed
back and asked directly whether I was sure, so checked via GA4 instead of assuming. Filtered GA4
property `438523825` to `sessionCampaignName = TSD_05.13_Leads_Search_Branded`, August: 8 distinct
users fired `phone_click`, 7 fired `generate_lead`, union (either event, no dimension breakout) =
15 = 8+7 exactly → **zero overlap**. `phone_click` in GA4 fires off the same underlying "tel:" link
click trigger as the Ads-side call conversion, so it's a fair proxy, not an unrelated metric.

**True picture for Branded in August: ~25 real conversions (17 calls + 8 forms), officially
reported as 17.**

**Not yet done:** add `SUBMIT_LEAD_FORM/WEBSITE` as a biddable conversion goal on Branded to match
the rest of the account. Offered to Edu, not executed this session.

- [ ] Add the missing conversion goal to Branded (`23853361615`).
- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-09-03 — HVAC landing page before/after: inconclusive; ruled out a tracking gap (with a wrong turn along the way)

**Trigger:** Edu asked for before/after data to back the argument that the 2026-08-05 HVAC landing
page swap improved performance.

**The raw comparison does not support that argument.** HVAC Search (`23848895678`), pre-swap
(Jul 30–Aug 4, homepage, 6 days) vs post-swap (Aug 5–31, dedicated LP, 27 days): conversion rate
31.8% → 12.25%, CPA $138.55 → $239.22. Using Electrical Search and Plumbing Search as a
same-account, same-window control (both stayed on the homepage the entire time): both *improved*
over the identical dates (Electrical 3.64%→6.56% conv. rate, CPA $126.03→$103.82; Plumbing
2.94%→6.13%, CPA $395.80→$115.99) — consistent with the general account tuning done 2026-08-10
(budgets/negatives/target CPA). HVAC moved the opposite direction from its own controls. Sample is
thin on both sides (HVAC pre-period = 7 total conversions), and HVAC was also a brand-new campaign
still maturing during the pre-window, so this isn't proof the landing page hurt anything — but it's
not a clean win either.

**Wrong turn, corrected after Edu pushed back:** first hypothesis was that the dip was a tracking
artifact — traced the `05 | G.Ads - Lead` GTM tag (id 82, fires "Website lead") and found its only
two firing triggers are `cEvent - Lead` (customEvent, `_event == "ghl_form_submit"`) and
`cEvent - Appointment Scheduled` (`_event == "Appointment Scheduled"`). Fetched the HVAC landing
page's live JS bundle (Vite/React SPA, Lovable-built) and its component tree (`HvacHub` →
`ServicePageTemplate`) — found zero references to either event name anywhere in that reachable
code, only `booking_cta_clicked`/`phone_call_clicked`, matching what the original 2026-08-05 entry
already flagged as unverified. Concluded (wrongly) that this page's own leads were invisible to
tracking.

**That conclusion was wrong — Edu correctly called it "not logical" given the report shows real
leads attributed.** Traced further: the page's "Schedule Your Free Pop-In Visit" CTA is a React
Router `<Link to="/schedule">`, not an inline form — `booking_cta_clicked` fires on that
click/navigation only. The shared `/schedule` route (`Schedule-BzD2dPW8.js`) embeds the real
GoHighLevel form via iframe (`link.leadnurturemachine.com/widget/survey/72XeoM18LZ5LbCHDrLVm`). So
the actual lead capture happens on `/schedule` after a page-to-page hop, Conversion Linker (tag 79)
keeps the gclid alive across that hop, and the conversion correctly attributes back to the origin
campaign. **No tracking gap exists for this flow** — the 10 form leads counted against HVAC Search
post-swap in August are real.

**Net:** the before/after read stands as inconclusive, not negative — no clean explanation for
HVAC's divergence from its own controls, and no grounds to claim the landing page helped either.

- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-09-03 — Call extension diagnosis: DISAPPROVED, has never served

**Trigger:** Edu asked to confirm all PPC runs to the homepage and all ads use the site's real
phone number, not a tracking number.

**Landing pages — not all homepage.** HVAC (both Search `23848895678` and PMax `23853595615`)
routes to the dedicated `proudpops.com/proud-pops-hvac-services` page (from the 2026-08-05 swap,
still live). Everything else live (Branded, Plumbing, Electrical Search, PMax Electrical, both
YouTube campaigns) routes to the homepage.

**Call extension — configured everywhere, but disapproved and has never served.** Account-level
default call asset + every live campaign's call asset (HVAC Search, Electrical Search, Plumbing
Search, Branded, PMax HVAC, PMax Electrical) all use phone number **(210) 794-7570**. The site's
actual displayed number is **210-225-5767** ("210-CALL-POP") — confirmed via a live fetch, appears
in the header, CTA, and meta description everywhere.

Checked `customer_asset`/`campaign_asset` `status`: all show `ENABLED` — Edu correctly pushed back
that the UI shows "Not eligible," and status ≠ eligibility. Pulled `primary_status`/`policy_summary`
next: **`ASSET_DISAPPROVED` → `UNVERIFIED_PHONE_NUMBER`** on every instance of the 794-7570 asset,
account-level and all 6 live campaigns. Google was never able to verify this number, so the
extension has never actually shown in a live ad, on any campaign, at any point.

One inconsistency found in passing: the PAUSED "Water Softening Equipment" campaign (`23875125989`)
carries a *different*, correctly APPROVED number, (830) 240-1661 — not serving only because the
campaign itself is paused, unrelated to the disapproval above.

**Practical upshot:** no customer has ever seen a mismatched number in a live ad — the disapproved
extension simply never rendered. The ~1,070/month "TSD - Website Call" conversions are NOT from
this call extension; they're a click-based conversion firing on whatever phone link is on the
*website* at the moment of click, so there's no ad-vs-site number mismatch possible for that volume
either.

**Fix, not yet done:** submit 210-225-5767 as a new call asset and get it through Google's phone
verification, then attach it in place of the disapproved one.

- [ ] Verify the real number through Google's call-asset verification flow and swap it in.
- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-09-03 — August performance report built (client-facing, plain format)

**Trigger:** Edu asked for an August breakdown (PPC + LSA, conversions by type and type-CPL), then
asked for a client-facing report built from it.

Built `clients/proud-pops/Proud-Pops-Google-Ads-Performance-Summary_2026-08.html` (+ PDF, since
renamed by Edu to `Proud Pops - August Report.pdf`) — first client-facing report for this account,
plain Times New Roman format (no navy/gold), golden-framing language throughout (no
"problem/issue/gap/leak/fix/wasted").

Structure: month-at-a-glance KPIs, Google Search & Performance Max by campaign, Local Services Ads
by surface, YouTube, "What We Worked On" (pulled from this file's August entries), "What's Next."

**Key methodology call, confirmed with Edu first:** `TSD - Website Call` (~1,071 phone-number-click
conversions in August, 88% of PPC's counted conversions) is reported as a separate "Calls" column,
never folded into the headline Leads count or cost-per-lead math — it's a click signal, not a
verified answered call (see the 2026-08-10 entry below and [[tsd-proud-pops-tracking]] in memory).

**Caught and fixed a double-count in my own draft before publishing:** the in-account Local
Services campaign (`20067257249`) lives inside PPC account `1051843378`, so its spend was already
included in the PPC total — an earlier chat answer had *also* added it again under "LSA total,"
inflating the reported grand total by $1,458.97 ($49,761.49 → corrected $48,302.53). Verified
against `read.py campaigns` cost sums before publishing.

Real August numbers (verified via `insights.py`/`read.py` for the calendar month,
`--since 2026-08-01 --until 2026-08-31`):
- Search & PMax (excl. LSA, excl. YouTube): $40,027.49, 129 form leads, 1,069 call clicks
- Local Services Ads (in-account + 2 dedicated surfaces): $3,273.87, 51 leads received / 40 billed
- YouTube (2 awareness campaigns): $5,001.17, 480,429 impressions, 112 clicks, ~0 leads (awareness
  only, not judged on cost/lead)
- Combined Google Ads investment: $48,302.53

- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-08-19 — Removed `instant_quote_hvac_click` conversion action

`ConversionActionService.mutate_conversion_actions` with a `remove` operation on
`customers/1051843378/conversionActions/7236987969` ("www.txproblemsolvers.com (web)
instant_quote_hvac_click", GA4-imported, category PURCHASE). Status confirmed `REMOVED` via a
fresh `read.py`-style query after the mutation, not the mutation's own response.

**Why:** This action was already `primary_for_goal = false` (correctly excluded from bidding since
the 2026-07-23 fix), but it was still MTD's single largest conversion count in the account —
664.9 of Aug 1–19, ahead of even `TSD - Website Call` — and kept showing up in `all_conversions`
reporting, making the account's real lead volume harder to read at a glance. It is a button click
on the instant-quote widget, not a lead.

**Not touched:** The underlying GA4 event/GTM tag on the site — this only stops Google Ads from
importing it as a conversion action. GA4 itself is unaffected; historical Google Ads data for this
action should still be queryable for past dates.

**Still open, unrelated:** `TSD - Website Call` remains primary and is still 86.5% of MTD's
"official" conversions (647 of 748) despite being a phone-number click, not a verified call — this
is the bigger distortion and has not been touched. See [[tsd-proud-pops-tracking]] in memory.

- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-08-17 — PMax HVAC asset-group cleanup: EXECUTED

`clients/proud-pops/fix_pmax_hvac_asset_contamination.py` targeted 10 off-topic Plumbing/Electrical
assets (7 headlines + 3 descriptions) contaminating the "HVAC" PMax asset group (`6712908741`,
campaign `23853595615`). The asset group's final URL was already fixed separately earlier
(`proudpops.com/` → `proudpops.com/proud-pops-hvac-services`, verified live).

Previously blocked by the Claude Code auto-mode classifier even with the `.claude/settings.local.json`
permission rule in place; cleared after Edu gave explicit in-session approval.

First run hit `OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE` on 6 of the 10 targeted resources — a
read-back showed they were already `REMOVED` (from an earlier partial attempt), and since the mutate
call has no `partial_failure` policy set, the whole batch rolled back with none applied. Re-ran with
only the 4 resources still `ENABLED`:

- Headline "Upfront Plumbing Pricing" (`360809118214`)
- Headline "Family-Owned Plumbing Co" (`360828257209`)
- Description "Licensed plumbers serving San Antonio & Hill Country..." (`360828257215`)
- Description "Family-owned electricians near you..." (`362781434102`)

All 4 removed, verified live via a fresh query after: 16 headlines / 7 descriptions remain. One
off-topic string still present by design — "Top-rated & reviewed San Antonio HVAC, plumbing &
electrical services" is one of the 4 combined-messaging assets the script deliberately left alone
(dropping those is a messaging call, not cleanup).

- [ ] Confirm ad strength improves from AVERAGE over the following days
- [ ] Consider the audience-signal gap (no customer-match/in-market segments on PMax HVAC — search
      themes only) as a follow-up, needs a strategic call on which segment, not autonomous
- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-08-17 — Budget bump: Branded + Search Electrical (budget-lost IS was the binding constraint)

Pulled `search_budget_lost_impression_share` vs `search_rank_lost_impression_share` (LAST_7_DAYS)
across all live campaigns to find where more budget actually converts to more impressions, as
opposed to HVAC/PMax/Plumbing where rank-lost dominates (44–80%) and budget is not the bottleneck.

Two campaigns came back budget-dominant:

| Campaign | Budget-lost | Rank-lost | IS | Old budget | New budget |
|---|---:|---:|---:|---:|---:|
| Branded (`23853361615`) | 20.5% | 10.8% | 68.7% | $45/d | **$70/d** |
| Search Electrical (`23866999121`) | 39.6% | 43.3% | 17.2% | $400/d | **$600/d** |

Branded: budget is clearly the dominant loss cause and rank position is already strong (68.7% IS) —
sized to roughly clear the missing budget-lost share (45 / (1-0.205) ≈ $57, rounded up with headroom
to $70).

Search Electrical: budget-lost (39.6%) is nearly as large as rank-lost (43.3%) — real headroom
exists, sized toward but not fully to the theoretical full-capture budget (~$662) pending a CPA check
before pushing further. Also contributes toward the account's $50k/Aug 31 pool gap.

Skipped: Search HVAC (rank-lost 44.3% > budget-lost 28.5%, but flagged as a secondary candidate if
gap-closing pressure increases), PMax HVAC/Electrical (budget-lost only 4.7–5.7%, essentially
rank-capped, more budget would mostly go unspent), Search Plumbing (rank-dominated at 62.9%, plus the
unresolved routing problem), in-account LSA (only ~20% of its $714/d cap used over the last 7 days —
demand-limited, not budget-limited).

Both budgets verified live via a fresh `read.py` query after the mutation.

- [ ] Re-check CPA on Search Electrical in ~1 week before deciding whether to push toward the full
      ~$662 budget-lost-capture level.
- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-08-17 — Gate-1 fix executed: Display network off on Search Plumbing

`fix_plumbing_display_network.py` (staged 2026-07-30, confirmed still unexecuted as of the 2026-08-13
script write and again in a 2026-08-17 status check) was run with Edu's explicit go-ahead.

Campaign `23853484024` (TSD_05.14_Leads_Search_Nonbranded_Plumbing) — `network_settings.target_content_network`
flipped `True → False`. Verified live via a fresh `read.py` query after the mutation, not the
mutation's own success JSON.

Plumbing's other known problem (homepage routing for service-specific queries) is still open — this
only closes the Display-serving leak.

- [ ] Log in Agency Titan per MasterOps doctrine.

---

## 2026-08-10 — HVAC budget push: budgets, bids, negatives, LSA cleanup

**Trigger:** Edu needs Proud Pops to hit $50k spend by Aug 31, with 70% of that pool directed at
HVAC specifically. Client approval is a **$50k top-level pool** — allocation across
campaigns/services is TSD's call, not a per-line-item client sign-off.

### Reality check run before touching anything

Pulled Aug 1–10 actuals: $6,004.72 spent account-wide (12% of $50k, a third of the month gone).
Broke lost impression share into budget-lost vs. rank-lost per campaign — Search HVAC and PMax HVAC
are 41–73% rank-lost (Ad Rank/QS), not budget-lost, so raising budget alone caps out around
$550–570/day combined for those two — nowhere near the ~$35k (70%) HVAC target. Also found the
account's `TSD - Website Call` conversion action is a phone-**click** signal, not a verified call —
it's 85% of MTD counted conversions, same click-vs-lead shape as the `instant_quote_hvac_click` trap
logged 2026-07-23 (see [[tsd-proud-pops-tracking]] in memory). Real trustworthy lead count for the
window: ~30 (24 web form + 6 LSA), not the reported 194.

### Changes made (all verified live via `read.py` after — never trusted the mutation's own JSON)

| Campaign | Account | Change |
|---|---|---|
| Search HVAC (`23848895678`) | 1051843378 | Budget $150→$300/day; target CPA added **$265** (was uncapped Maximize Conversions) |
| PMax HVAC (`23853595615`) | 1051843378 | Budget $130→$230/day; target CPA added **$27** |
| Search Electrical (`23866999121`) | 1051843378 | Budget $75→$150/day — clean case, 79% of lost IS was budget, not rank |
| Search Plumbing (`23853484024`) | 1051843378 | Budget $60→$90/day — kept modest, still has the known Display-network/homepage-routing problem; Change 1 fix still unexecuted |
| Search HVAC (`23848895678`) | 1051843378 | 2 campaign-level negatives added: `wrangler`, `radiator` — competitor-brand queries leaking in via search terms ("wrangler ac san antonio", "1 800 radiator and a c san antonio"); collision-checked against all 15 live keywords first |
| `TSD_05.14_Leads_Search_Nonbranded` (`23848792310`) | 6621969129 (HVAC LSA account) | **PAUSED** — zero conversions, ~$20/day, pure waste |

RSA/extension audit on Search HVAC: already Ad Strength GOOD, 15/4 assets filled, extensions solid
(sitelinks/callouts/structured snippets/call/logo) — no action needed there; every asset is still
`PENDING` performance-label because the campaign is too new for Google to have rated anything yet.

### Tooling gotcha found and fixed

`update.py campaign --budget` silently **"succeeds" with zero effect** if `--customer-id` isn't
passed explicitly — falls back to the profile default (All Heart, `9205826499`), the internal
budget-resource lookup returns 0 rows for a campaign that doesn't exist there, and the mutation is
skipped without any error. Burned two real attempts before catching it (verified via a direct
`read.py` re-check, not the JSON response). Also extended the skill with a one-off pattern for
setting `maximize_conversions.target_cpa_micros` — `update.py` has no bidding-strategy support
built in. **Lesson: always pass `--customer-id` explicitly on every write, and always re-verify with
a fresh read — never trust a mutation script's own success JSON alone.**

### Updated month-end projection

Naive budget-cap sum across all enabled PPC campaigns says ~$43.7k possible; realistic delivery
(accounting for rank-limited and demand-limited campaigns) projects to **~$27,800 by Aug 31** across
PPC + all 3 LSA surfaces — up from ~$19–20k pre-change, still well short of $50k. Also surfaced the
two external LSA accounts (San Antonio Electrician `7261668241`, San Antonio HVAC `6621969129`) were
both sitting at 2–6% of a $714/day cap — confirmed demand-limited, not something more budget fixes.

### Still open

- [ ] Change 1 (Plumbing QS fix, staged since before this session) — not executed
- [ ] Landing page split for Search HVAC's 3 ad groups (repair/install/maintenance all point to one
      generic page) — Edu says not now
- [ ] Verify `TSD - Website Call` against real CallRail call volume before trusting it as a KPI
- [ ] $35k HVAC target vs. ~$20–25k realistic HVAC ceiling — gap needs a decision (pull from
      Electrical/Plumbing headroom, or accept the miss)
- [ ] Log this in Agency Titan per MasterOps doctrine — client approval covers the pool, but ticket
      documentation is still pending

---

## 2026-08-08 — YouTube Video Views campaigns: San Antonio + New Braunfels launched, review in progress

**Trigger:** Edu wanted YouTube brand-awareness ads for the two markets he has video creative for
(San Antonio metro, New Braunfels/Boerne/Helotes/Fair Oaks Ranch). Videos cover 4 topics: HVAC
repair-vs-replace, panel replacement, breaker tripping, surge protection.

### Skill extended: google-ads-ratos had no Video campaign support at all

Before today, `create.py` only handled SEARCH/DISPLAY/PMAX — no VIDEO channel type, no video ad
groups, no video ad creation. Added:

- `create.py video-campaign` — VIDEO campaign, `--objective VIEWS` (Target CPV) or `REACH` (Target
  CPM/efficient reach)
- `create.py video-ad-group` — IN_STREAM or BUMPER format
- `create.py video-ad` — attaches a YouTube video ID to an ad group with CTA button + final URL
- `create.py location` — geo-target criterion, works on **any** campaign type (was missing
  entirely, not video-specific)
- `read.py locations` — lists geo-targets on existing campaigns
- `read.py geo-search` — looks up `geo_target_constant` IDs by place name (`SuggestGeoTargetConstants`)

**Important discovery: Google Ads API blocks all mutation of VIDEO campaigns.** Tried
`create.py video-campaign` live — failed with `MUTATE_NOT_ALLOWED, trigger: "VIDEO"`. Confirmed via
validate-only calls that this is not create-only: campaign status updates, network settings updates,
and ad group bid updates on an existing VIDEO campaign all hit the same block. This is a blanket
Google Ads API restriction (not a dev-token tier issue) — **Video campaigns must be created and
edited entirely in the Google Ads UI.** The new `create.py video-*` commands still work for other
channel types if that restriction is ever lifted, but for now they're unusable for actual video
campaigns. `read.py locations`/`geo-search` are unaffected (read-only) and useful for any campaign type.

One harmless side effect from the failed attempt: an orphaned `CampaignBudget` object
(`customers/1051843378/campaignBudgets/15777525966`) was created before the campaign mutation
failed. Unattached, $0 impact, safe to ignore or delete later.

### Campaigns (Edu built both in the UI after I gave exact settings)

| | San Antonio (`24120440530`) | New Braunfels (`24120482524`) |
|---|---|---|
| Name | `08/2026 - YT - VideoViews (San Antonio)` | `08/2026 - YT - Awareness - New Braunfels` |
| Status | ENABLED | ENABLED |
| Bidding | TARGET_CPV | TARGET_CPV |
| Budget | $100/day | $100/day |
| Geo | San Antonio city (`1026759`) | New Braunfels city (`1026651`) |
| Video partners | OFF (fixed 08-08) | **ON — not yet fixed** |
| Ad group | `VIDEO_RESPONSIVE`, 4 ads each, own distinct video files per city (not swapped) |
| CTA button | **missing on all 4 ads** | **missing on all 4 ads** |
| Delivery as of 08-08 | 0 impressions, $0 spent | 0 impressions, $0 spent |

Ad copy (headline + description, long_headlines/descriptions fields on `VIDEO_RESPONSIVE_AD`),
identical set used on both cities:

| Video | Long headline | Description |
|---|---|---|
| Repair vs. Replace HVAC | Old AC Acting Up? Find Out If It's Worth Fixing Or Time For A New One | We walk you through the real cost of fixing vs replacing your AC. |
| Panel Replacement | Old Electrical Panel? Here's When It's Time To Replace It | We'll check your panel and give you a straight answer, no pressure. |
| Breaker Tripping | Circuit Breaker Won't Stop Tripping? | We'll track down the real problem and fix it for good |
| Surge Protection | Why Does Your Home Need Surge Protection? | We'll show you how whole home surge protection actually works |

Final URL on all ads: `proudpops.com`. Business name "Proud Pops" + logo attached on every ad
(required for approval). Ad policy review status was still pending at last check on all 8 ads.

### Open — unresolved CPV bid discrepancy

Edu says the UI shows Target CPV at **$0.06** on both campaigns. Every API read of
`ad_group.cpv_bid_micros` — checked twice, both campaigns, fresh queries — comes back **$0.01**
(`10000` micros). Confirmed via source that `TargetCpv` (the campaign-level bidding strategy
message) has **no bid-amount field at all** in API v24 — it's meant to be fully automated — so
`ad_group.cpv_bid_micros` should be the only place a number lives. Zero impressions/zero spend on
both campaigns since launch is consistent with a bid that's too low to win auctions, which is a
plausible root cause if $0.01 is really what's saved. Not resolved — need Edu to confirm exactly
where in the UI he's reading $0.06 (Bidding section vs. ad group) before concluding whether this is
a real mismatch or a misread field.

### Still open — needs the UI, not available through the API tooling

- [ ] **New Braunfels: turn off Google video partners** (Settings → Networks) — same fix already
      done on San Antonio.
- [ ] **Add "Get Quote" CTA** to all 8 ads (4 per campaign) — never got attached, both campaigns
      currently have no call-to-action button at all.
- [ ] **Resolve the $0.01 vs $0.06 CPV bid discrepancy** above.
- [ ] Confirm ad policy approval clears (was pending on all 8 ads at last check) — campaigns will
      start spending automatically the moment it does, current settings (video partners on NB, no
      CTA, unresolved bid) and all.

**Trigger:** Edu asked to check how the Aug 5 landing-page swap (below) is performing so far.

**New page confirmed live:** `proudpops.com/proud-pops-hvac-services` returns HTTP 200.

### HVAC Search — before vs. after

| | Pre-swap (Jul 22–Aug 4, 14d) | Post-swap (Aug 5–7, 3d) |
|---|---|---|
| Clicks | 22 | 14 |
| Conversions | 6 | 1 |
| CPA | $161.64 | $368.55 |

Daily clicks/conversions, Jul 30–Aug 7 (`TSD_05.14_Leads_Search_Nonbranded_HVAC`, 23848895678):

| Date | Clicks | Conv | Cost |
|---|---|---|---|
| 07-30 | 3 | 1 | $50.08 |
| 07-31 | 5 | 4 | $249.88 |
| 08-01 | 3 | 0 | $156.08 |
| 08-02 | 3 | 0 | $173.66 |
| 08-03 | 3 | 0 | $174.91 |
| 08-04 | 5 | 1 | $165.21 |
| 08-05 (swap day) | 7 | 1 | $157.85 |
| 08-06 | 5 | 0 | $160.48 |
| 08-07 | 2 | 0 | $50.22 |

**Read: not a real signal yet.** CPA looks worse post-swap, but this campaign only runs 2–7 clicks/day and conversions were already noisy pre-swap (Jul 31 alone had 4 conversions off 5 clicks — almost certainly an attribution/lag artifact, not 4 real jobs booked in a day). Two days of a low-volume campaign isn't enough to separate signal from noise.

**Control comparison (same window, Aug 5–7, still on homepage):**

| Campaign | Clicks | Conversions | Cost |
|---|---|---|---|
| Electrical (23866999121) | 45 | 3 | $200.98 |
| Plumbing (23853484024) | 17 | 0 | $123.27 |

Also thin. No conclusion to draw from the control either at this sample size.

**Next check:** revisit in 5–7 more days once there's enough clicks to read a CPA trend instead of day-to-day noise, per the follow-up already flagged in the Aug 5 entry below.

---

## 2026-08-05 — HVAC landing page swap: EXECUTED

**Authority:** Edu, in-session. New page built by Edu himself on proudpops.com, tracking (GTM,
same container GTM-WBFDB6L8) confirmed live and running by Edu before the swap.

**What changed:** all 3 ads in `TSD_05.14_Leads_Search_Nonbranded_HVAC` (23848895678) — AC Repair,
Installation, Maintenance ad groups — final URL switched from the homepage (`https://proudpops.com/`)
to the new HVAC-specific landing page `https://proudpops.com/proud-pops-hvac-services`. Electrical
and Plumbing ad groups left on the homepage on purpose, as a control group for comparison.

| Ad group | Ad ID | New final URL |
|---|---|---|
| AG1_HVAC_ACRepair | 808927834052 | proudpops.com/proud-pops-hvac-services |
| AG3_HVAC_Maintenance | 808848684157 | proudpops.com/proud-pops-hvac-services |
| AG2_HVAC_Installation | 808848503953 | proudpops.com/proud-pops-hvac-services |

**Why:** page is built for paid traffic (single offer, testimonials, FAQ, reduced-friction CTA) vs.
the generic homepage. Diagnosed before the swap: page shares the already-fixed GTM container, but
its own on-page analytics only track clicks (`phone_call_clicked`, `booking_cta_clicked`) — same
shape as the previously-flagged `instant_quote_hvac_click` click-vs-lead trap — so the real form
submission on `/schedule` wasn't independently verifiable via static analysis. Proceeded on Edu's
direct confirmation that he set up and verified the tracking himself.

**Tooling change:** `update.py ad` (google-ads-ratos skill) extended to support `--final-urls`,
writing to the `Ad` resource via `AdService` (final URLs live on the shared Ad, not `AdGroupAd`) —
previously the subcommand only handled `--status`. `--ad-group-id` is now optional, required only
when `--status` is passed.

**Follow-up:** check `Website lead` conversions on this campaign in a few days vs. the Electrical/
Plumbing control to confirm the new page converts at least as well as the homepage did.

---

## 2026-07-30 — Step 1 of the $50k August ramp: EXECUTED

**Authority:** Edu, verbal, in-session. **$50,000 approved pool through Aug 31.**
**⚠️ MasterOps gap:** this increase — and the **Jul 7 reduction** ($409→$250/day by
andrea@topservdigital.com) — still have **no written client approval on an AM ticket.** Both belong
on the same ticket. Overdue.

Script: `step1_launch_2026-07-30.py` (dry-run by default, `--apply` to write). Rationale and full
allocation in `budget-allocation-2026-08.md`.

### Why now: the constraint flipped

The GTM conversion fix (live v38, Jul 23) worked. Every conversion in the trailing 30 days landed in
the last 8 days. Maximize Conversions stopped bidding at the floor, Ad Rank recovered, and
budget-lost impression share roughly doubled while rank-lost fell 20–28 points. The gate the Jul 23
remediation doc set is cleared — budget is now the binding constraint.

Clean baseline (Jul 22–29): PPC $282.85/day, 43 conversions, **$52.62 blended CPA**.
PMax Electrical $30 · PMax HVAC $37 · Search Electrical $82 · Search Plumbing $225.

### What was written

**1. Attached shared negative list `CSMS_Negatives`** (sharedSets/11330296375, 758 members) to the
three non-branded Search campaigns — 23853484024, 23866999121, 23848895678. It had been attached to
**nine paused legacy campaigns and zero live ones**, so the live campaigns were running with no
negatives at all.

**2. Added 47 campaign-level phrase negatives** covering the gaps the shared list does not:

| Campaign | Added |
|---|---:|
| Search Nonbranded Plumbing (23853484024) | 14 |
| Search Nonbranded Electrical (23866999121) | 18 |
| Search Nonbranded HVAC (23848895678) | 15 |

- Own brand — `proud pops`, `problem solvers`: **zero hits in CSMS_Negatives.** Brand was leaking
  into nonbranded at $28–38/click while the Branded campaign sat paused.
- Missing competitors/junk: `quan air`, `elmer zubiate`, `mr electric`, `mr sparky`,
  `allgood electric`, `handyman`.
- Cross-service, per campaign (the AI Max bleed): Electrical blocks HVAC+plumbing terms, Plumbing
  blocks HVAC+electrical, HVAC blocks plumbing+electrical.
- **Deliberately NOT added:** `pops heating and air`. Distinct company, but it collides with Proud
  Pops brand recall and a negative may block real brand searches. Needs a human call.

**3. Budgets:**

| Campaign | From | To |
|---|---:|---:|
| PMax HVAC (23853595615) | $80 | **$130** |
| PMax Electrical (23866982084) | $60 | **$110** |
| Search Nonbranded Electrical (23866999121) | $50 | **$75** |
| Search Nonbranded HVAC (23848895678) | $100 | **$150** |
| Search Nonbranded Plumbing (23853484024) | $60 | **$60 — held on purpose** |

Total live PPC budget $250 → **$525/day** (~$590/day expected, campaigns overdeliver ~13%). ~2.1x.

Plumbing held flat despite having the second-highest budget-lost share (44.4%): $225 CPA on 3
conversions, 40.6% still lost to rank, serving on Display, routing service queries to the homepage.
Lost impression share is the wrong signal to act on there. Fund it after the routing and QS work.

All five budgets verified `reference_count = 1` before writing — no shared budget resources, so no
cross-contamination. The script asserts this and aborts otherwise.

**4. Enabled `TSD_05.14_Leads_Search_Nonbranded_HVAC` (23848895678)** — PAUSED → ENABLED.

Opened at **$150/day, not the planned $250.** It is a brand-new Maximize Conversions campaign with
zero conversion history; $250 on day one buys expensive learning. Steps to $250 on Aug 8 once there
is an observed CPA. The account had **no non-branded HVAC Search live at all** — HVAC was served
only by PMax — in peak cooling season, with ac-repair at 4,500+ searches/mo at LOW–MEDIUM
competition. Built and ready: 24 keywords, 3 ad groups, 3 ads all GOOD strength.

Expect PMax HVAC's search share to shift into this campaign (exact/phrase Search generally outranks
PMax on the same query). That is intended — controllable inventory. **Judge the two together.**

### Collision check before applying

A phrase negative that matches your own keyword kills it silently, so every negative was checked
against all 93 keywords in the three campaigns using correct Google match semantics (EXACT = whole
query, PHRASE = word sequence, BROAD = all words present).

Result: **one** real collision — `ac install cost san antonio` is blocked by the pre-existing BROAD
negative `cost` in CSMS_Negatives. Accepted: price-research query, low booking intent.

Also noted in the inherited list and left alone: BROAD `free` (blocks "free ac unit for seniors"
type non-leads — net positive) and BROAD `austin` (correct geo negative).

### Still open — needs the UI, not available through the API tooling

- [ ] **Turn OFF AI Max, final URL expansion, auto-created assets on 23866999121.** Enabled by
      brandon@proudpops.com 2026-06-26; still the source of the cross-service bleed. The negatives
      added today contain it, but this is the actual cause.
- [ ] **Turn OFF Display network on 23853484024** (`target_content_network = True` — a Search
      campaign serving Display, on the worst performer) and search partners on both Search campaigns.
- [ ] **Un-pause Branded 23853361615** at $45/day. Ready: 31 keywords, 5 ad groups, 5 enabled ads
      (2 EXCELLENT, 3 POOR). **Not done today — Edu asked only for the HVAC campaign; needs his
      go-ahead.** Brand keeps leaking into nonbranded until it is live.
- [ ] Landing page routing → `/services/plumbing`, `/services/electrical`, `/services/hvac`.
- [ ] Widen geo: PMax HVAC + Search Plumbing target **San Antonio city only**; Electrical targets 5
      cities; LSA runs in 47.
- [ ] Kill or fold in `TSD_05.14_Leads_Search_Nonbranded` sitting inside LSA account 6621969129 —
      $481.69/30d, zero conversions.

### Post-fix conversion read (Jul 23–30, measured 2026-07-30)

Taken the same day, after the changes above went in. Jul 30 is a **partial day** and Search HVAC had
only been live a few hours, so both under-read.

**Non-phone conversions attributed to Google Ads: 16** — 15 `Website lead` (form fills) + 1
`local_services_message_lead`.

Excluded on purpose: `instant_quote_hvac_click` recorded **68** in the same window. It is a button
click, not a lead — non-primary, correctly not biddable. Counting it would show 84 and be wrong.

Form fills are accelerating, which is the real signal that the GTM fix took:

| | 7/23 | 7/24 | 7/25 | 7/26 | 7/27 | 7/28 | 7/29 | 7/30 |
|---|---|---|---|---|---|---|---|---|
| Form fills | 1 | 1 | 0 | 1 | 2 | 4 | 2 | 4 |

First four days 0.75/day → last three 3.3/day.

**Cost per form fill:**

| Campaign | Spend | Forms | $/form | Calls |
|---|---:|---:|---:|---:|
| PMax Electrical | $473.49 | 7 | **$67.64** | 13.2 |
| PMax HVAC | $591.82 | 7 | **$84.55** | 17.5 |
| Search Electrical | $400.21 | 1 | $400.21 | 4.0 |
| Search Plumbing | $600.04 | **0** | — | 4.0 |
| Search HVAC | $0.00 | 0 | — | 0 |
| **PPC total** | **$2,065.56** | **15** | **$137.70** | **38.7** |

$137.70/form is **fully loaded** — it charges all spend to forms and ignores the 38.7 calls the same
money produced. **The number to manage to is $38.49 per tracked lead** (53.7 forms + calls). This is
a phone-first business; forms are the minority path. Both PMax campaigns deliver forms at $68–85.

**Search Plumbing: $600 spent since the fix, zero form fills, 4 calls.** Largest PPC line in the
window, only campaign producing no forms at all. Third independent signal against it, after the $225
CPA baseline and 40.6% rank-lost. **Treat as a candidate for a cut at the Aug 8 step, not a hold.**

### GA4 cross-check (property 438523825)

GA4 shows **30 `generate_lead`** site-wide over the same window:

| Source / medium | Leads |
|---|---:|
| google / cpc | 12 |
| (direct) / (none) | 10 |
| google / organic | 3 |
| `tagassistant.google.com` / referral | **3** |

GA4's 12 vs Google Ads' 15 is **not** a discrepancy — GA4 counts by session source, Ads counts by
click date within its attribution window and includes cross-device. They agree directionally, which
confirms the fix fires correctly and is not double-counting.

**3 of the 30 are fake** — `tagassistant.google.com / referral` is GTM Preview mode, test fires from
validating the tag on Jul 23. Real site-wide leads ≈ 27.

- [ ] **GA4 config gap:** `generate_lead` is **not marked as a key event**; the only key event on the
      property is `instant_quote_hvac_click` (643 in 28 days). GA4 is flagging a button click as the
      conversion and ignoring the actual form fill. Does **not** affect bidding — the GTM fix sends
      to Ads directly via `awct`, bypassing GA4 import — but any GA4-based reporting is wrong until
      fixed. GA4 Admin → Events: mark `generate_lead`, unmark the button click.

### Next checkpoints

- **~Aug 2 (48h):** search-term report on all three — confirm competitor/cross-service terms are
  gone and the negatives did not over-block. First read on HVAC Search.
- **Aug 8:** step 2 → ~$900/day, HVAC Search to $250. Gate: CPA holding.
- **Aug 15:** step 3 → ~$1,195/day. Then release the $6,755 reserve into whatever holds CPA.
- **No tCPA before ~Aug 6–13** (2–3 weeks of clean data from Jul 23).
- CPAs here are cost per *tracked lead*, **not validated against ServiceTitan booked jobs.** Still
  the weakest link in the case for spending $50k.

## 2026-11-12 — fu-054 DECIDED: budget stays as is (Edu)
No Branded $50→$75 / HVAC swap, no YouTube fill. November lands ~$20.5-21k vs the $25k cap (11-11 check: MTD $5,715.68 through 11-10, ~$805/d weekdays, ~$479 weekends + ~$37/d LSA). Caps stay Branded $50 / Electrical $455 / HVAC $230 / Plumbing $145 = $880/d. Next read fu-137 11-16. AM update on AT d2b5e325: November lands ~ $21k, under the cap.

## 2026-11-13 — fu-157 AM asks rechecked (read-only) and trimmed for Angela

- **CallRail '210 - CALL POP' (210-225-5767) recording still OFF:** 161 calls on it 10-16..11-13 (20 on 11-11/12), none recorded. It is now the main ad call number, so most ad calls can't be reviewed. Client decision.
- **LSA message leads, main profile 1051843378:** 6 charged real requests 11-09..11-12 with NO business reply in the LSA inbox (ids 350858712 bathtub drain same-day, 351032898 PTAC, 351218835 PRV, 350855363 home estimate, 351634392 adding ducts, 351334991 garage water leak). 11-06 P-trap (350146313) was handled by phone and booked, so phone follow-up may exist outside the inbox. 351579426 = review-seller spam (not charged). Only 11-12 leads got inbox replies (20 min).
- **Weekend coverage facts:** LSA electrician 7261668241 schedule = 7 days 9-18 (incl. Sunday, where the $500 fee ends calls); main + HVAC 6621969129 = Mon-Fri 7-19, Sat 8-15, no Sunday. Search campaigns have no ad schedule. Search 10-16..11-12: Sat+Sun $1,409.05 / 5 counted conv vs Mon-Fri $7,806.94 / 64.
- **Test calls:** 47 calls from a caller ending 8301 (4 on 10-20, 43 on 10-30), CallRail source Google Ads, untagged. Ours to tag in the CallRail UI.
- **LSA ratings moved to fu-161 (ours):** rate bad 346547072 (electrician 10-18 greeting-only, charged) + 351579426 (spam); un-book 348716900 (10-29 price shopper); mark booked 350091694, 350146313, 350583822. 348872571 (10-29 outside area) already DECLINED + charged, no credit → closed. No disputes.
- None of the three LSA profiles has migrated to pay-per-lead PMax yet (11-13).
- AM note = AT Internal Request draft (Cowork), Edu submits; aim before the 11-16 review call.

## 2026-11-13 — The Original 97 Deal (AT bd8c7bb4): ads plan drafted

Edu: run both the $9,797 price and "as low as $135/mo" (+ $165 Comfort Plan first). Client-facing plan written into the Completion Notes field (request_completion_notes) on AT bd8c7bb4 via API, read back OK; Execution stage left open for Edu. Internal notes + Slack reply to Johnny in `original-97-deal-ads-plan.md`. Command Center fu-164.

## 2026-11-19 — New-site launch check (read-only, fu-178/179)
Switch NOT done: proudpops.com still serves the Lovable build (twitter:site @Lovable, gpt-engineer assets, /__l5e/ events, consent default denied, IP 185.158.133.1). GTM-WBFDB6L8 live = v43 (2026-10-08); launch draft = Default Workspace 45, 15 changes, unpublished, 0 conflicts. Johnny 11-18 15:41 BRT: staging lock comes off at the switch. fu-178 (publish at switch) moved to 11-20, fu-179 (CAPI token rotation) waits on it. fu-157 + fu-164 closed per Edu (asks went via the Oct Review / 11-16 notes; Original 97 now on AT a85b34ca + f7a74115).
