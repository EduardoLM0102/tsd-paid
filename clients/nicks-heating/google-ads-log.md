# Nick's Heating and Air Conditioning — Google Ads log

Google Ads `1854100356` ("Nicks Heating and Cooling"), under Topservdigital MCC `4155514468`. LSA runs
inside the same account. Hammond, LA (Tangipahoa / Northshore). Agency Titan client "Nick's Heating and
Air Conditioning" (`0400fd40-cff2-46eb-ab46-c9befc4f7c7a`). Newest entry on top.

Folder created 2026-10-08. Before this there was no workspace record for Nick's, no Agency Titan 7-day
Google/LSA task, and zero account changes by anyone in the last 30 days (change_event, 09-08 → 10-08).
Campaigns are TSD-named (built Feb–May 2026, before Edu joined).

---

## 2026-11-11 (later) — APPLIED 1 + 2 + 3 (Edu: "Execute 1 to 3"), ~10:21 BRT / 07:21 CT

All validate-only first, then `--apply`, read-back confirmed:
1. **NB 23821497590: new ad group "Heating Repair" 205669629001** (`nicks_heating_adgroup_1111.py`) → https://nicksac.com/heating-repair-hammond-la/. 18 keywords (exact: heating repair, heating repair near me, heating repair hammond la, furnace repair, furnace repair near me, furnace repair hammond la, heater repair, heater repair near me, heat pump repair, heat pump repair near me, heating service hammond la; phrase: heating repair hammond, gas furnace repair, heating system repair, emergency heating repair, heater not working, furnace not working, no heat). 14 ad-group PHRASE negatives (for sale, in store, deals, evaporator core, why isn't, why won't, how to, diy, parts, manual, space heater, water heater, cost of, price of). 1 RSA, 15 headlines / 4 descriptions, paths heating-repair/hammond-la, **in review**. Ad group cpc bid $12 (campaign Max Clicks $15 cap applies).
2. **Branded 23675600637: 39 non-brand keywords PAUSED** (`nicks_branded_cleanup_1111.py`), 16 brand keywords stay (nicks ac / nicks heating and air / … in exact, phrase, broad).
3. **Budgets** (`nicks_budgets_1111.py`): NB $25 → **$40/day**, Branded $100 → **$85/day**. PMax stays $50. Total caps unchanged ($175 + PPL $71).
**Rollback:** ad group → PAUSED; re-enable the 39 keywords (list printed in the script's validate run); NB $25 / Branded $100.
⚑ Recheck 11-18 (fu-152): RSA approved? heating ad group clicks/CPC/leads (transcribe ad calls), search terms (furnace parts / DIY leaks?), NB spend vs $40; Branded IS back toward ~90% on brand terms, spend; PMax rule (≤$120); PPL PMax impressions + leads per day, leads marked?
Still owed: AM note (fu-005 + the 10-22 declined replacement lead + 10-27 geothermal callback + unmarked PPL leads); the 10-27 geothermal LSA dispute (Edu, LSA UI).

---

## 2026-11-11 — fu-124 read: week 2 after the PMax brand exclusion + heating LP status (read-only, 2 changes STAGED for Edu)

`nicks_read_1111.py` (this folder) + `/tmp/nicks_branded.py` (Branded detail) + LSA recordings 10-22..10-27 (call-wins, `lsa-call-wins-log.md`). POST 11-04..11-10 (7d) vs PRE 10-29..11-03 (6d), conversions by conversion date. No account changes since 11-04.

| | POST spend (budget) | Leads | Per lead | PRE | Note |
|---|---|---:|---:|---|---|
| TSD PMax 23586346547 | $312 ($50) | 3 (2 ad calls 377s/65s + 1 lead form) | **$104** | $303 / 3 = $101 | passes ≤$120 again. YouTube 25% → 12% ($38, 0 conv). Budget-lost 48%. Search categories clean (keefe's 5 impr / 0 clk, benfatti 4 / 0). |
| Branded 23675600637 | $32 ($100) | 2 ad calls (634s, 125s) | $16 | $15 / 2 | IS 92% → **40%**, rank-lost 60%: see below, it is not the brand terms |
| NB AC 23821497590 | $115 ($25) | 0 (1 ad call 37s, 225 area) | – | $49 / 0 | AC spend doubled in November ($16/d), 9 clicks at $12.77: hvac near me, ac repair mandeville, ac unit. 17 "Local actions - Other engagements" = junk |
| PPL PMax 24425921001 (LSA) | $126 ($71) | 3 leads (1 charged 11-06) | $126/charged | old LSA $219 / 2 | 124 impr / 18 clicks in 7d; 11-07/08 no impressions; all 3 leads ACTIVE (unmarked) |

**Branded's IS drop is non-brand keywords, not brand.** The "Branded Evergreen Mix" campaign holds 55 enabled keywords: 16 brand (nicks…, QS 10, IS 83–100%) and **39 non-brand, almost all BROAD** (heating repair hammond, residential hvac companies, heating company near me, ac repair hammond la broad, furnace repair louisiana…). In heating season those are getting impressions (ac repair hammond la broad 42, heating repair hammond 32, residential hvac companies 22) at 50–82% rank-lost, which drags the campaign IS to 40%. Search terms: southern hvac, 1 hour hvac, american heating and cooling, amana dealers near me (competitors/dealers) on a Max Conversions campaign with a $100 cap. Same leak as the 10-21 "hvac contractors near me" pause, 39 more of them. They would also compete with a heating ad group.

**Heating LP: a page already exists.** nicksac.com/heating-repair-hammond-la/ = H1 "Heating Repair in Hammond, LA", 1,745 words, GHL form db9n5NmobCC51Ujra9lM, phone (985) 999-4785 (the GHL number pool in GTM v9 swaps it by source; Nick's has no CallRail), NATE / 40+ years / Carrier Factory Authorized / licensed & insured on the site. Not noindex (SEO page), phone not the biggest element. Close enough to launch heating NOW; the go.-style LP (fu-125) becomes a later upgrade, not a blocker. Also /heating-service/ and /furnace-repair-in-covington-la/ exist.

**LSA recordings (10-22..10-27, 5 calls transcribed):** 10-22 07:38 BOOKED = real AC repair (compressor, wife 26 weeks pregnant, Brenda works a slot) ✅; 10-22 10:33 DECLINED not charged = fuel delivery driver ❌ (correctly not charged); **10-22 11:16 DECLINED charged = a real lead Nick's turned away**: homeowner needs a diagnosis + replacement estimate for a flooded 4-ton system (insurance will pay), Nick's: "we don't work directly with the insurance company… we can't touch that price" → not disputable, it's a service they offer; AM item; 10-26 11:19 BOOKED = heating tune-up pricing ($89 / $189 / $215 plan) ✅; **10-27 13:14 DECLINED charged = geothermal thermostat in Ponchatoula**, Nick's doesn't service geothermal (only Mr. Nick), and the caller says he was promised a callback the week before that never came → dispute as "service not offered" (weak: the thermostat itself is serviceable), plus a dropped callback.

**STAGED (validate-only passed, NOT applied), Edu's go:**
1. `nicks_heating_adgroup_1111.py`: NB ad group **Heating Repair** → /heating-repair-hammond-la/, 18 keywords (exact + phrase: heating/furnace/heater/heat pump repair, + hammond la, near me, heater not working, no heat, emergency), 14 ad-group negatives (fu-125 list + how to, diy, parts, manual, space heater, water heater, cost of, price of), 1 RSA 15 H / 4 D (claims verified on the site). Campaign-negative conflict check passed.
2. `nicks_branded_cleanup_1111.py`: PAUSE the 39 non-brand keywords in Branded, keep the 16 brand ones. Budget untouched.
3. Budget (not scripted, Edu's call): NB $25 → $40 for the heating group. Source: Branded $100 → $85 (it spends $5/d, total cap unchanged) rather than PMax $50 → $35 (PMax passes its rule and already loses 48% to budget).
4. AM note (fu-005 still owed): add the declined replacement lead (10-22), the geothermal callback never made (10-27), 3 PPL leads ACTIVE/unmarked since 11-03, plus the old items (COI, hours, GA access, missed ad calls).
⚑ Next read fu-124 → new followup after the apply (heating week 1, Branded IS back to ~90%, PMax rule, PPL delivery).

---

## 2026-11-06 — LSA moved to Pay-per-lead PMax by Google (read-only, nothing changed)

Old LSA `23344968885` paused; new `24425921001` created 11-04 12:19. SERVING / LEARNING, asset group ELIGIBLE → nicksac.com, budget $71.43/d,
ad schedule carried over. Billing approved, license/insurance/background passed. **Not dark**: impressions 38 / 33 (11-02/03 old) →
25 on 11-05 (3 clicks, $0 = no charged lead). Leads by day: 11-02: 2, 11-03: 1, 11-04: 1, then 0. Watch at fu-124 (11-11): split the
pay-per-lead campaign from TSD PMax when reading PMax CPL.

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

## 2026-11-04 — fu-108 recheck of the 10-28 PMax brand exclusion + competitor negatives (read-only, nothing changed)

Script `nicks_recheck_1104.py` (this folder). POST 10-29 → 11-03 vs PRE 10-22 → 10-27 (6 days each), conversions by conversion date.
No account changes since Edu's 10-28 apply. **No tap action in this account** (no CLICK_TO_CALL; PMax on account-default goals), so the
custom-goal tap leak found on Watt's Right/ICS doesn't apply here.

| | POST spend | Leads | Per lead | PRE |
|---|---:|---:|---:|---|
| PMax ($50) | $303 | 3 ad calls (184s, 93s, 106s) | **$101** | $297 / 1 = $297 |
| Branded | $15 | 2 ad calls (362s, 77s; a 52s call not counted) | $7.45 | $0 / 0, IS 74% → 92% |
| NB AC ($25) | $49 | 0 | n/a | $29 / 0 |
| LSA | $219 | 2 | $109 | $465 / 5 = $93 |

- **PMax passes the rule** (≤ ~$120 per lead) → keep $50. Search $227 carries all 3 leads; YouTube grew $22 → $76 (25%, 308 clicks, 0 conv), watch it.
- **Brand exclusion worked:** Branded picked up the brand clicks (3 clicks, 2 real calls). PMax still shows 1 brand click ("nick's heating and air",
  1 conv) and 1 "theriot's heating and air" click (1 conv) in its search categories, despite the exclusion/negative. Minor, watch.
- **NB AC** is still nearly dark ($8/d of $25, AC in November). Heating ad group still waits on Edu's heating landing page.
- **LSA:** spend halved ($77/d → $36/d), 2 leads at $109. **Nick's IS marking leads now:** since 10-22, 3 BOOKED, 3 DECLINED, 1 message still NEW,
  2 recent ACTIVE. The "0 of 6 marked" AM item is outdated. 2 DECLINED leads were charged (10-22 11:16, 10-27 13:14): dispute candidates if they
  weren't real HVAC jobs (listen first).
- All ad calls from 985 (Hammond area) or 504 (New Orleans).
- AT Internal Request **5189e272-4def-4cb4-9c17-26c7417cce83** "Nick's: Google Ads update after the 10-28 changes" created as a DRAFT (Intake, Edu submits): FYI for Angela (Execution), Edu Intake + Review & Close.

---

## 2026-10-28 (later) — APPLIED: PMax brand exclusion + competitor negatives (fu-108 items 2 + 3, Edu's go)

Script `nicks_apply_1028.py` (this folder), validate-only first, then live. Read-back OK, PMax ELIGIBLE, still $50/d.
- **PMax brand exclusion:** new brand list "TSD | Nick's own brand (PMax exclusion)" (shared set 12290621628) with entity
  /g/11shhfxyk8 = "Nick's Heating & Air Conditioning LLC", nicksac.com. Attached to PMax as a negative brand list.
  In 60d, brand searches in PMax had 43 clicks / 4 conv. They should now go to Branded (~$4 CPC, IS 74%).
- **10 PHRASE negatives on PMax** (campaign level; PMax had none): theriot / theriots / theriot's, nash heating,
  burkhardt, hagerman, wilkins heating, southern air, accutemp, enviro mechanical. All 0 conv in PMax search categories over 60d.
- **NOT blocked:** "keefe's ac" had 4 clicks and 2 conv in PMax over 60d (same rule as "tropical air kare" on 10-21).
- Branded: broad "hvac contractors near me" confirmed still PAUSED (item 3, no change).
- Item 1 (NB → heating): ON HOLD. Edu is requesting a heating landing page first.
**Expect:** Branded picks up brand clicks and leads PMax used to get. PMax spends more on non-brand searches, so its CPL may look worse at first.
⚑ Recheck 2026-11-04 (fu-108): PMax per lead (rule: > ~$120 → back to $35, $15 to NB heating once its LP exists), Branded volume.

---

## 2026-10-28 — Recheck of the 10-21 changes (fu-078, read-only, NO changes)

Script `nicks_recheck_1028.py` (this folder). Windows: PRE 10-15→10-20 vs POST 10-22→10-27 (6 days each,
10-21 = change day). change_event: nobody else touched the account since 10-21 (only Edu's 07:40 apply).
Read-back still matches: NB $25 Max Clicks $15 cap (LIMITED, BIDDING_STRATEGY_LIMITED), PMax $50 PRESENCE.

| | PRE 6d | POST 6d |
|---|---|---|
| Nonbranded AC | $186 / 5 clk / 0 conv, CPC $37 | $29 / 2 clk / 0 conv, CPC $14.72, ~$5/d of $25 |
| PMax | $207 / 14 clk / 3 conv ($69) | $297 / 115 clk / 0 conv (by click date) |
| Branded | $9 / 2 clk / 0 | $0 / 0 clk (24 impr, IS 74%) |
| LSA | $490 / 4 ($123) | $465 / 5 ($93) |
| PPC ex-LSA | $402 / 3 | $326 / 0 |

- **NB is effectively dark.** The $15 cap is under half the old $37 market CPC, so it only wins 1 click
  every few days. Both clicks were off-target: "mini splits for sale near me" (retail) and "heating
  services near me" (heating demand landing in an AC-only campaign). Leak stopped, but no leads either.
- **PMax got worse.** By conversion date, 10-22→10-28 = 2 leads (10-23 call 101s + 10-28 lead form) on
  ~$307, about $154/lead vs the ~$61 target. PMax ad calls: 15 in the 13 days 10-08→10-20, 1 since 10-21.
  Clicks went from 14 to 115, but 93 of them are cheap YouTube/Display clicks ($36), and Search is still
  $247 of the $297. Daily spend spiked ($100 on 10-23, $85 on 10-25), then fell to $10–15/d from 10-26.
  Search categories include competitors (keefe's ac, theriot's, burkhardt, southern air of northshore,
  nash) and Nick's own brand. There's still no brand exclusion on PMax. Can't separate the effects of the geo
  change, the extra budget and the end of AC season with 1 week of data.
- **Branded:** the broad keyword's removal cost nothing visible this week (Branded had 0 conv in PRE too).
  Brand searches are tiny (24 impr), and PMax takes some of them.
- **LSA carries the account:** 6 leads 10-22→10-27, $93 CPL. All 6 are still unmarked (5 ACTIVE + the
  10-23 message lead NEW). Same lead-handling gap as 10-08, and the AM ticket is still owed.
- Tracking OK: the 10-23 PMax call counted (conversions_by_conversion_date). Ad calls ≥60s = primary.

**Proposed (not applied, Edu to decide), all at the same $75/d total:**
1. NB → heating for Nov–Feb: add a Heating ad group (furnace/heating/heat pump repair, phrase/exact) and
   keep AC to a few exact terms. Add negs "for sale", "in store", "deals", "evaporator core", "why isn't",
   "why won't". Keep the $15 cap for week 1. Ads go to the homepage (no heating page on nicksac.com).
2. PMax: brand exclusion (Nick's) + campaign-level competitor negatives (keefe's, theriot's, burkhardt,
   southern air, nash, accutemp, enviro mechanical). Keep $50 one more week. If CPL is still > ~$120 on
   11-04, go back to $35 and move the $15 to NB heating.
3. Branded: leave the broad keyword paused. With the PMax brand exclusion, brand searches move back here.

---

## 2026-10-21 — APPLIED: the 10-08 checklist (Edu's go)

Fresh read 10-08 → 10-20: Nonbranded AC $470 / 13 clicks / 0 conv ($36 CPC, 'air conditioner repair Louisiana' $208 / 7 clicks / 0). PMax $424 / 7 conv ($61 CPL, 32% budget-lost). Branded $38 / 3 conv. LSA $1,057 / 9 ($117). Only account change since 10-08 = the 10-16 AI Max cleanup.

Script `nicks_apply_1021.py` (this folder) passed every guard and validate-only:
1. Nonbranded: pause PHRASE 'air conditioner repair Louisiana'; 34 PHRASE negatives (14 competitors that never converted, supply/dealer/distributor, car AC, 8 out-of-area cities, price/DIY research). 60d replay: none blocks a converting term or a live keyword. Bidding Max Conversions → **Max Clicks, $15 max CPC**.
2. Branded: pause BROAD 'hvac contractors near me'. Trade-off: in 60d it bought competitor-name searches for ~$23 and 2 of them converted ('air dat', "berthelot's"), so the account loses ~1 cheap lead/month in exchange for a clean brand bucket.
3. PMax: geo PRESENCE_OR_INTEREST → PRESENCE.
4. Constant $75/d: Nonbranded $40 → $25, PMax $35 → $50.
Not blocked on purpose: 'tropical air kare' (competitor, converted once).

**Applied same day** (the first `--apply` was blocked by Claude Code's permission check; ran after Edu asked for it explicitly). Read-back: PMax $50/d PRESENCE; Nonbranded $25/d TARGET_SPEND (Max Clicks) $15 cap; both keywords PAUSED; 34/34 negatives on Nonbranded. Total still $75/d.
**Expect:** Nonbranded clicks under $15 and fewer of them; PMax should spend the extra $15/d near its $61 CPL. ⚑ Recheck 2026-10-28 (Command Center fu-078): NB CPC + search terms + any conversions, PMax CPL at $50, Branded volume without the broad keyword.
**Still open (Edu):** AM ticket (COI, evening/weekend hours, GA access, missed calls, LSA leads to mark + disputes), AT weekly tasks for Nick's, heating coverage for Nov–Feb.

---

## 2026-10-08 (later) — Lead quality check: are the 30d leads real? (read-only, NO changes)

Window 09-08 → 10-08. Sources: `call_view`, `local_services_lead` + `local_services_lead_conversation`,
`lead_form_submission_data`. PII not copied here.

**Verdict: yes, almost all real.** No spam pattern in any source.

- **Calls from ads (18 counted = calls ≥60s):** 28 calls total (PMax 19, Branded 8, Nonbranded 1). All 18
  counted calls ran 66s–7min from local/regional area codes (985 ×12, 504 ×5, 225 ×3, 601, plus one 469).
  The other 10 were 3 missed and 7 short or hidden-caller-ID calls, none counted. The 3 missed calls were
  PMax calls during business hours (09-10 09:48, 09-11 09:54 and 11:00). Branded calls probably include
  existing customers phoning the office. The API can't separate new from existing.
- **LSA (35 leads, 25 charged):** 18 BOOKED (14 charged), most calls 2+ min. 7 still ACTIVE, i.e. Nick's
  hasn't marked them. 6 of those are 10-05 or later; one is a MESSAGE lead from 09-14 that has sat
  unmarked for 3+ weeks. 10 DECLINED: 6 not charged; of the 4 charged, 1 was credited and 3 were not (calls
  of 25s, 91s and 91s, 09-16). Of the 18 charged leads with an outcome, 14 booked (78%).
- **Google-hosted lead form (2 counted):** 09-20 and 10-04 (plus 09-04, just outside the window). All
  have real names, local phones and Northshore ZIPs (70445, 70435, 70455).
- **Website form ("Submit lead form - web"):** the tag works, just at low volume. Monthly fills:
  Apr 7, May 5, Jun 3, Jul 5, Aug 3, Sep 1 (last 09-13, Branded). The Branded campaign doesn't have the
  form goal as biddable, so that fill wasn't counted. NB had form fills in May (3), Jul (2), Aug (2).
- **Nonbranded's 1 conversion** = a 3-minute call from a 985 number on 09-16. Real, but it's still
  1 lead for $1,257.

**Correction to the entry below:** finding 3 said the web form "fired once in 30d". That's true, but the
tag isn't broken; it fires at low volume. The real tracking gap is no website call tracking.

**Follow-ups for the AM (lead handling, not ads):** 3 missed ad calls during business hours, the 09-14
LSA message still unmarked, 7 LSA leads to mark, and dispute review for the 3 charged DECLINED leads.

---

## 2026-10-08 — First check: full read-only 7-day pass (NO changes made)

**Trigger:** book-wide review found Nick's is an active client (confirmed in the "Client Accounts - Audit
(Master doc)" sheet) with ~$4.8k/30d Google spend and no one checking it.

**Account state**
| Campaign | ID | Type | Bid | Budget/d | Notes |
|---|---|---|---|---|---|
| LocalServicesCampaign | 23344968885 | LSA | Max Conv | $71.43 | Ad schedule Mon–Fri 7:00–16:00 only |
| TSD_02.20_PMAX_Q1 | 23586346547 | PMax | Max Conv | $35 | Final URL /contact-us/, geo PRESENCE_OR_INTEREST |
| TSD_03.22_Search_Branded_Evergreen | 23675600637 | Search | Max Conv tCPA $25 | $100 | Contains a non-brand BROAD kw |
| TSD_05.05_Leads_Search_Nonbranded_AC | 23821497590 | Search | Max Conv (no target) | $40 | primary_status LIMITED |
| TSD_02.20_SEARCH_Q1, TSD_03.22_Search_Branded_Evergreenn | — | Search | — | — | PAUSED |

All Search campaigns: Google Search only (partners/display off). Geo: Amite City, Covington, Hammond,
Mandeville, Madisonville, Ponchatoula (95% of 30d spend from Louisiana). No auto-apply subscriptions.
**Zero negative keywords anywhere** (no campaign negatives, no shared lists). All RSAs approved, all
pointing at the homepage nicksac.com.

**Numbers**
| | 7d (10-01→10-07) | 30d (09-08→10-07) |
|---|---|---|
| LSA | $649 / 7 leads / $93 | $2,313 / 25 / $93 |
| PMax | $257 / 3 / $86 | $1,072 / 12 / $89 |
| Branded Search | $73 / 4 / $18 | $206 / 7 / $29 |
| Nonbranded AC | $372 / 0 / – | $1,257 / 1 / $1,257 |
| **PPC only (excl. LSA)** | **$702 / 7 / $100 CPL, CPC $16.71, CVR 16.7%** | **$2,535 / 20 / $127, CPC $12.01, CVR 9.5%** |

Branded vs unbranded (PPC, 7d): branded 4 leads / $18 CPL; unbranded (PMax + NB) 3 leads / $210 CPL.
Brand keyword IS: "nicks heating and air" 98%, "nicks ac" 100%. Nonbranded IS ~42% (rank-lost 32%,
budget-lost 26%).

Monthly Search + PMax: Jul $2,889 / 39 leads ($74) → Aug $2,573 / 29 ($89) → Sep $2,460 / 20 ($123).
LSA flat at ~22 leads/month, ~$2.15k.

**Findings**
1. **Nonbranded AC is the leak.** $1,257 for 1 conversion in 30d. CPC $24.65 (30d), $46.49 (7d). One
   PHRASE keyword, "air conditioner repair Louisiana", took $856 (68%) for 1 conversion. Max Conversions
   with no target and ~1 conversion/month has no signal to bid on. Visible search terms include
   competitors (professional heating and air, surgis/southern air), supply houses (ferguson hvac,
   trane dealers), car AC ("auto ac repair"), out of area ("hvac metairie") and price research. Only
   $519 of $1,463 Search spend shows as search terms. AC only, nothing for heating going into Nov–Feb.
2. **Branded campaign has a non-brand BROAD keyword**, "hvac contractors near me" (IS 10%). It matched
   ~100 competitor names and supply searches. 4 of the 7 "branded" conversions came from it (one on
   "berthelot's ac and heating"). That inflates the branded numbers and drags the campaign IS to 12%.
3. **Website conversions are nearly invisible.** No website call tracking. "Submit lead form - web"
   fired once in 30d (0 counted). Counted conversions are only Calls from ads, the Google-hosted lead form
   and LSA leads. NB ads land on the homepage, so site calls from NB aren't measured. No GA access
   (per the audit sheet), so we can't cross-check.
4. **LSA is the best channel but only runs Mon–Fri 7am–4pm.** 35 leads in 30d, 18 booked. 3 DECLINED
   leads were charged with no credit (1 other was credited). Check if they're disputable (30-day window).
5. **LSA insurance:** the API shows insurance PASSED (uploaded 2025-12-10, $2M), license PASSED
   (2026-04-09), background PASSED, campaign ELIGIBLE. The audit sheet says the COI expired 2026-08-05.
   Google hasn't acted yet. Get the renewed COI uploaded before it does.
6. PMax: 91% of spend on Search, $89 CPL, budget-lost IS 31%. It also picks up brand searches (26 clicks
   on "nick's heating and air") and competitor names. Geo setting is PRESENCE_OR_INTEREST.

**Recommendations (not applied, Edu to decide; all can be done at constant total budget)**
- NB: pause "air conditioner repair Louisiana", add negatives (competitors, supply houses, car AC,
  out of area, price research), and cap bids (Max Clicks with a CPC cap, as on Zen Air) until conversions
  come back. Consider moving part of NB's $40/d to PMax (budget-limited at $89 CPL).
- Branded: pause the BROAD "hvac contractors near me" in the branded campaign.
- PMax: geo to PRESENCE.
- LSA: ask the AM if Nick's takes calls evenings/weekends, review the 3 charged DECLINED leads for
  dispute, chase the renewed COI.
- Tracking: request GA access, check the GTM form tag, add website call tracking.
- Ask for Agency Titan 7-day Google Search + LSA tasks for Nick's.

**Open items**
- [ ] Edu: approve/decline the changes above.
- [ ] AM: renewed COI, weekend/evening hours, GA access.
- [ ] Heating coverage for NB (Nov–Feb).
