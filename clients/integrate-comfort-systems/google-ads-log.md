# Integrate Comfort Systems — Google Ads log (2895702982)

**Not in `contas.yaml` yet.** CID given directly by Edu (not found via MCC listing), confirmed
accessible under the Topservdigital MCC (4155514468) via the `tsd.sh` profile. Account name in
Ads: "Integrate Comfort Systems - LSA Belleville". USD, `America/New_York`.

## 2026-11-12 (later 2) — Tracking test on the new heating page: PASS

Edu submitted one test lead ~09:40 BRT (name "TSD TEST - please ignore", eduardo@topservdigital.com, 555-010-1112, 1 TSD Test Street, Belleville); Cowork read Tag Assistant (GTM-N4QW8BF live, GPC + ad blocker off).
- Page load: Google Ads config, GA4 config + page_view, CallRail, GHL listener, Conversion Linker, Google forwarding number (AW-461860660), Meta + TikTok page views all fired. Phone stays (866) 658-2987 (no CallRail swap, by design).
- gclid: with ?gclid=TSDTEST1112 typed directly, location.search, `_gcl_aw` cookie and the form iframe src all carry it (the first "missing gclid" was Tag Assistant's connect box stripping the query).
- Phone tap: Google Ads | Phone Call Click + GA4 Phone Click (+ Meta/TikTok contact) fired.
- Form: email required. **form_submitted (#19) → Google Ads | Event | Lead, Google Ads | User-provided Data, GA4 | Event | Lead (generate_lead), Meta | Event | Lead all FIRED (Succeeded).** Form then redirects to a "Thank you - Integrate Comfort Systems" page (tags on it not checked).
- Not confirmed: the Ads hit payload (Tag Assistant "Hits Sent" empty), mobile view (Edu checks on phone).
- ⚠ Second Google Ads tag on the site: **AW-1064128677** (besides 461860660). Old open question; check where it loads and whether it double-counts.
- To do: delete the test contact from ICS's GHL (Edu/Mo).

---

## 2026-11-12 (later) — APPLIED: NB relaunch on the heating page (Edu: "Go")

`ics_nb_relaunch_1112.py --apply`, all 7 steps APPLIED. Read-back: campaign 24047025253 **ENABLED**, cap $20, budget $25/d; goal = CAMPAIGN custom 6459689709; 16 enabled keywords (12 exact + 4 phrase); new RSA **831383124121** ENABLED → icshvac.com/furnace-heating-repair-northern-nj/ (REVIEW_IN_PROGRESS); old RSA 817245367827 PAUSED; 20 negs added.
**Rollback:** campaign → PAUSED.
**Open:** Edu test lead on the page (GTM Preview, GPC + ad blocker off) → Ads 'Lead' (tag 93) fires → GHL; new RSA approval; first read 11-19 (fu-159). Holiday offer copy if approved (fu-131).

---

## 2026-11-12 — NB relaunch on the new heating page STAGED + validated (fu-151), waiting on Edu's go

**Page live** (Sha built it, AT 82ecaff6 still in Execution): icshvac.com/furnace-heating-repair-northern-nj/ (www 301s to non-www). curl vs brief PASSES: H1 exact, noindex, (866) 658-2987 x23, main line 866-749-6331 only in the site-wide schema (invisible), GHL form 9yoyys68IRpTtwyjDdjr + gclid/utm iframe script, GTM-N4QW8BF, "15,000+", brand line as briefed. Not checked: visual/mobile.
**GTM (live container, read-only):** tag 78 GHL listener + tag 93 Ads "Lead" (form_submitted) + tag 97 phone-click tag fire on All Pages, so the new page is covered. ⚠ Listener only pushes form_submitted when the GHL payload has an **email** (same trap as Napps); this form fired in Oct so email is likely required, the test lead confirms. Also live: CallRail swap.js 974585705 on All Pages + tag 52 Google forwarding number (AW-461860660) on All Pages.
**Campaign state read (paused 11-11):** heating AG 197798871985 = 8 PHRASE kws; 30d paid terms mostly competitors (steve sirc, lenny's, smiths, advanced) + price research; old RSA 817245367827 → /furnace-repairs (2 redirects), says "12,000+" and "NJ & NYC" (NYC is a negative); campaign on account-level goals (incl. a PAGE_VIEW goal); geo PRESENCE, no partners/display; 18 campaign negs + 4 shared lists.

**Staged `ics_nb_relaunch_1112.py` (validate-only PASS, all 7 steps):**
1. Goal → custom 6459689709 'TSD | Calls + Forms (no taps)' (Calls from ads, Landing Page Call, Submit lead form - web, Lead form - Submit), same as PMax.
2. Budget $22 → $25/d; Max Clicks cap $15 → $20.
3. +20 campaign PHRASE negs: cost, price(s), how much, reviews, reddit, diy, parts, westchester, new york, lenny's/lennys, smiths heating, a j perri/aj perri, reiner, gadaleta, petro, jobs, salary.
4. Pause the 8 old PHRASE kws; add 12 EXACT (furnace repair, heating repair, heater repair, furnace/heating repair near me, boiler repair (+near me), emergency heating repair, no heat repair, heat pump repair, oil burner repair, furnace not working) + 4 PHRASE (furnace/heating/boiler repair nj, emergency furnace repair). "no heat in house" rejected by Google as Dating policy (!), dropped.
5. New RSA → the new page, path Heating-Repair/Northern-NJ, 15 headlines/4 descriptions (15,000+, NATE, 24/7, gas/oil/boiler/heat pump, licensed NJ, 5 counties; no NYC, no offer yet), old RSA paused.
6. Campaign ENABLED.
Spend: +$25/d vs today (Branded $15 + LSA). Still below the pre-11-11 PPC total ($77/d), so inside what was running.
After apply: Edu test lead on the page (GTM Preview, GPC + ad blocker off) → Ads 'Lead' fires → GHL; first read ~11-19. Holiday offer copy only if approved by 11-13 (fu-131).

---

## 2026-11-11 (later 3) — Heating landing page brief for Sha DRAFTED in Agency Titan (fu-151)

Internal Request **82ecaff6-4816-49c7-8ee6-ba46371f078d** "Build 1 landing page: Furnace & Heating Repair (Northern NJ)", client ICS, priority high, due Thu 11-13 EOD. Intake = Edu, Execution = Sha (60c4ead4), Review & Close = Edu. Left in Intake for Edu to submit (and pick WebDev as the Execution department in the form). https://app.agencytitan.com/tasks/instance/82ecaff6-4816-49c7-8ee6-ba46371f078d
Brief = Cool Hand bd47275a format, one page, model = go.coolhandelectric.com/hvac-repair/:
- URL icshvac.com/furnace-heating-repair-northern-nj/ (main site, WordPress + Elementor, noindex; no go. subdomain exists for ICS). H1 "Furnace & Heating Repair in Northern NJ"; subhead mirrors the live heating RSA (since 1990, gas/oil/boiler/heat pump, NATE, 24/7). No promo bar (fu-131 offer, if any, later).
- Phone = Google Ads CallRail number **(866) 658-2987 / +18666582987** (the call-extension tracker; same pattern as Cool Hand's 469-351-1738 on every page). Never the main line 866-749-6331 (the site's default, header + footer).
- Form = the GHL form already on /contact-us/ (9yoyys68IRpTtwyjDdjr) + the gclid/utm iframe script. GTM-N4QW8BF stays; GTM internals + all testing = Edu.
- Proof verified on icshvac.com 11-11: since 1990, 15,000+ installations (the RSA says 12,000+, stale), 3 NJ offices, 24/7 emergency, NATE-certified, Mitsubishi Electric Diamond Contractor, NJ #19HC00444000 + HIC #13VH00607800, financing on replacements. Reviews/rating from the Belleville GBP only.
- Brand line proposed "Family-owned. Northern NJ since 1990." (Edu/JB to confirm); owner story from /about-us/ (Chris Wisniewski); video = ZhZmpBYn2fs.
Edu's open choices before submitting: main site vs a go.icshvac.com subdomain, the brand line, the H1 wording, the deadline.
Next, when Sha posts the URL: relaunch NB with one heating ad group (phrase/exact), Max Clicks ~$20 cap, $22-30/day, ad URLs → the new page; GTM lp_form_submit / GHL trigger check; test lead.

---

## 2026-11-11 (later 2) — APPLIED A + B + C (Edu: "Execute A and B ... Execute C"), ~09:50 BRT / 07:50 ET

All validate-only first, then `--apply`, read-back confirmed on each:
1. **NonBranded 24047025253 → PAUSED** (`ics_nb_pause_1111.py`). Budget $22 / $15 cap left as they are.
2. **PMax 22890783804 → PAUSED** (`ics_pmax_pause_1111.py`). Budget $40 left. The 11-18 checkpoint is moot.
3. **LSA Belleville 2895702982 / 15786867110: $1.43/day ($10/week) → $50.00/day** (`ics_lsa_budgets_1111.py` block B). Insurance PASSED in the API. Manual CPA bid $24 untouched.
4. **LSA Englewood Cliffs 8323145223 / 21467507022: $1,428.57/day → $50.00/day** (block C). Never served; cap only.
Net: PPC −$62/day, LSA +$48.57/day on a profile that should spend, −$1,378.57/day on a profile that never did. Live paid now = Branded $15 + LSA Belleville $50 + Carlstadt $51 + Englewood $50 (not serving) + Mitsubishi YouTube ~$20.
**Rollback:** NB/PMax status → ENABLED; Belleville budget → $1.43; Englewood → $1,428.57.

**AM note DRAFTED** in Agency Titan: Internal Request **be762554-82f7-4c17-967b-6068ba223791** "Google Ads update: Search paused, Local Services budget restored, one question" (client ICS 1e439ca7, Angela = AM on the record). Asks whether ICS wanted Belleville cut in June and wants it back; FYI on the pauses + Englewood cap; Mitsubishi YouTube owner; phone menu reminder. Left in Intake for Edu. https://app.agencytitan.com/tasks/instance/be762554-82f7-4c17-967b-6068ba223791
⚑ Watch: Belleville LSA impressions/leads per day from 11-12 (fu-150); if Angela says the client wanted it off, revert.

---

## 2026-11-11 (later) — Whole-account picture + turnaround plan (read-only; Edu asked "what else can we do, ASAP")

`ics_full_picture_1111.py` + LSA probes (/tmp scripts, output summarized here) + CallRail 11-04..11-10 + site checks.

**Where ICS's leads actually come from (CallRail, 11-04..11-10, 24 calls):** GBP Belleville + Englewood Cliffs 14 calls (9 at 60s+, 5 first-time), homepage organic/direct 9 (7 at 60s+, 3 first-time), **Google Ads 1 (21s)**. Demand exists; paid captures almost none of it.

**1. LSA is the account's lost engine.** Three LSA accounts, **1 lead in 30 days**:
| Account | Budget | 30d spend | Leads | Notes |
|---|---|---|---|---|
| Belleville 2895702982 | **$1/day** | $0 | 0 | ELIGIBLE/SERVING, latest insurance + license PASSED, manual CPA bid $24. History: Apr-26 12 leads/$672, **May-26 30 leads/$1,435 (~$48/lead)**, then June→ 1-3/mo since the budget went to $1. Good months in 2023-24: 40-106 leads. Budget last changed before 08-15 (API can't see who). Geo: Bergen/Essex/Hudson/Morris/Passaic counties + Basking Ridge/Bedminster/Bernardsville/Far Hills/Summit/Andover, excl. Newark/Paterson/Elizabeth/Irvington. |
| Carlstadt 2175964343 | $51/day, tCPA $60 | $106 | 1 | 27 Bergen/Essex/Hudson towns, 280-390 impr/mo, reach-limited |
| Englewood Cliffs 8323145223 | **$1,429/day** | $0 | 0 ever | targets only Englewood Cliffs city, 0 impressions ever; older license FAILED/insurance EXPIRED, latest PASSED. Never served: needs a UI look (reviews/profile). Budget is a loaded gun if it ever starts. |
- Also in the Belleville account: **"Mitsubishi YouTube" 23599485735, $610/mo flat since April ($7.3k/yr)**, 56-210k impr/mo, no TSD log, 0 attributable leads. Last touched 11-07 (someone). Owner unknown (client / Mitsubishi co-op / inherited).

**2. Nonbranded lands on a weak page through two redirects.** Ad URL `www.icshvac.com/furnace-repairs` → 301 → 301 → `/services/heating/repair/`. Page: H1 "Furnace & Heating Repair", one generic 866 number, **0 forms**, 2 YouTube embeds. Landing page experience BELOW AVERAGE on every keyword, QS 3, rank-lost 57%, $15 cap. The Hawkins/Cool Hand go. template (1 service/page, H1 = keyword + town, CallRail number big, form at top) is the fix.

**3. PMax is not a lead campaign.** Homepage URL, geo = 11 towns only (not the 8 counties NB/Branded use), Search Partners + Display ON, Mon-Fri 7-17 schedule (no nights/weekends in heating season), legacy negative list of 21 Latin American countries. Search categories last 13d = competitor names (reiner group, total comfort, gadaleta, njr, aj perri, petro...). Since taps left the goal: 69% YouTube. 1 booked lead in October (10-21 Jersey City). 

**4. The IVR eats 3 of 4 ad callers** (Oct: 24 of 31; this week 1 of 1). AT 5e5dcc2a with Angela since 11-02, no answer yet. Nothing in Google fixes this.

**5. Tracking debt:** CallRail→Ads uploads 0 since 10-09 (fu-031); ghl_* GA4 imports still primary (double-count forms); GA4 page_view as a conversion action (secondary); 866 number on the LP = "Homepage Calls" pool, so paid website calls would show a gclid, and none did.

**6. Geo mismatch:** NB/Branded = 8 NJ counties; PMax = 11 towns; LSA Belleville = 5 counties; Carlstadt = 27 towns; Englewood = 1 town. Site has a /new-york-city/ service page; NYC is not targeted anywhere, yet NYC callers book (10-27 Queens). Ask ICS if NYC is in scope.

**Plan (fastest first):**
| # | Action | Owner | Approval | Effect |
|---|---|---|---|---|
| A | Pause NB (staged) + pause PMax now (not 11-18): $62/d of 0-lead spend stops | Edu | none (spend down) | funds B |
| B | LSA Belleville $1 → ~$50/day (May level). First ask Angela who cut it in June and why. | Edu + Angela | net total paid goes DOWN vs today ($62 out, $50 in); still confirm with the client since someone cut it | at May's rate ~30 leads/mo at ~$48 |
| C | Cap LSA Englewood Cliffs $1,429 → $50/day; UI check why it never served | Edu | none (budget down) | safety + maybe a 3rd LSA area |
| D | Chase the IVR fix (AT 5e5dcc2a): ad + LSA tracking numbers straight to service | Angela → ICS | client | roughly triples usable ad calls at the same spend |
| E | Heating landing page (go. template) → relaunch NB on it, 1 heating ad group, $20 cap, $22-30/d, + ICS's holiday offer if approved by 11-13 | Edu → Sha; Edu rebuild | none | QS 3 → 6+, same $ buys ~2x clicks that convert |
| F | Mitsubishi YouTube: who owns it? If nobody, pause and move $20/d to LSA | Angela | client | +$610/mo |
| G | Tracking: CallRail uploads (fu-031), ghl_* → secondary, during the LP build | Edu | none | clean bidding data for E |
| H | Branded: leave ($7 cap, IS 62-89%) | | | |

Followups: fu-150 (LSA Belleville restore + Englewood cap), fu-151 (heating LP request). fu-123 note updated.

---

## 2026-11-11 — fu-123 read: 0 real leads from paid in 6 days (read-only, nothing changed yet)

`ics_read_1111.py` (this folder) + CallRail 11-04..11-10 (24 calls). POST 11-05..11-10 (6d, first full days after the 11-04 tap fix) vs PRE 10-29..11-03 (6d).
Only change since 11-04: the 2 NB negatives (11-04 07:42). Tap action 7835539864 confirmed Secondary (taps only in All conversions now).

| | POST spend (budget) | Real leads POST | PRE spend | Real leads PRE |
|---|---|---:|---|---:|
| PMax | $244 ($41/d of $40) | **0** | $166 | 2 (152s, 65s ad calls, not transcribed) |
| NonBranded heating | $158 ($26/d of $22) | **0** | $123 | 0 |
| Branded | $39 ($6/d of $15) | **0** | $59 | 0 (1 tap) |

- **PMax went to YouTube once the taps left the goal:** YouTube $167.52 of $244 (69%, 672 clicks at $0.25) vs 31% before. Search $73 (6 clicks). Conversions column 0.0; all_conversions = 331 GA4 page_views + 8 taps. Search IS 11%, rank-lost 82%. Same drift as Neon Monkey PMax after its geo fix.
- **Ad calls:** call_view = 1 call in 7 days (11-04 08:45 ET, 21s, Caldwell). Transcribed: it ends during the greeting ("Thank you for calling ICS…"). CallRail: that call is the only Google Ads one; **0 website calls with a gclid** (the rest are GMB, organic, direct).
- **NonBranded heating:** 25 clicks, 0 leads. Competitor 'lenny's plumbing & heating clark reviews' $12.74 / 2 clicks; research terms (home heater not working, how much does furnace repair cost); 'best hvac companies in westchester ny' (NY, outside geo?). Since heating-only (10-29..11-10): **$281, 0 real leads** → fails the ≤ $200 per real lead rule a second time (10-28: $287 / 1).
- **Branded:** IS 68%, budget-lost 21% while spending $6/d of $15 (Target IS day-to-day swings). 0 calls.
- Account-wide paid (11-05..11-10): **$441, 0 real leads.** 13 days since 10-29: ~$790 for 2 untranscribed PMax calls.

**Proposed (Edu's go):**
1. **Pause NonBranded** now. `ics_nb_pause_1111.py` staged + validated. Spend goes down $22/d, no approval needed.
2. **PMax:** one more week to 11-18, hard stop. Keep only if ≥ 2 transcribed real calls at ≤ ~$150 each. YouTube share is the tell: if it stays ~70%, pause it.
3. **Branded** stays as is ($15, Target IS).
4. The IVR (AT 5e5dcc2a, with Angela since 11-02) is still the first fix: the one ad call this week hung up in the greeting.

---

## 2026-11-04 (later) — APPLIED: tap action → Secondary + 2 NB competitor negatives (Edu: "Apply 1 and 2")

`ics_apply_1104.py` (this folder), validate-only first, then `--apply`, read-back confirmed:
1. `[TSD] Click to call` 7835539864 → **Secondary** account-wide (primary_for_goal False, include_in_conversions_metric False). Taps still report
   under All conversions. Only PMax bids on conversions here, so only its bidding changes. Custom goal 6459689709 left as is.
2. NonBranded 24047025253: PHRASE negatives **steve sirc**, **advanced heating** (30d replay: 4 terms, $22.38, 0 conv, no keyword conflicts).
Budgets unchanged ($40 / $22 / $15). ⚑ Next read 2026-11-11 (fu-123): PMax Conversions = real only (no taps), PMax cost per real call (transcribe),
NB heating leads vs the ≤ $200 rule, Branded leads.
- AT Internal Request **2895ef4a-c0b0-4d2c-b8a9-b8048a69ed5c** "ICS: Google Ads update after the 10-28 changes" created as a DRAFT (Intake, Edu submits): FYI for Angela (Execution), Edu Intake + Review & Close.

---

## 2026-11-04 — fu-109 recheck of the 10-28 changes (read-only, nothing changed)

Script `ics_recheck_1104.py` (this folder) + CallRail (COM742d…, 22 calls 10-29 → 11-03). POST 10-29 → 11-03 (6d) vs PRE 10-09 → 10-26 (18d).
No account changes since the 10-28 apply. Real = Calls from ads (60s) + Landing Page Call + Submit lead form - web + Lead form - Submit; taps and GA4 page_view out.

| | Spend/day (budget) | Real leads | Per real lead | Notes |
|---|---|---:|---:|---|
| PMax | $28 ($40), PRE $52 | 2 (PRE 1 in 18d) | **$83** (PRE $936) | Search partners $160 → $9; YouTube now 31% ($52) |
| NonBranded heating | $20 ($22), PRE $16 | 0 (PRE 1) | n/a | 18 clicks, CPC $6.83, IS 12%, budget-lost 31%, rank-lost 56% |
| Branded | $10 ($15) | 0 (PRE 2 in 18d) | n/a | IS 82%, budget-lost 15% → 0% |

- **PMax real calls:** 10-30 152s (Orange) and 11-02 65s (Jersey City), both first-time in CallRail (Call Extension), not transcribed yet.
  The other 4 ad calls: 37s, 17s, 17s, 1 missed. The IVR drop pattern continues (ticket 5e5dcc2a with Angela).
- **⚠ The custom goal leaks taps here too** (same as Watt's Right 11-03): PMax Conversions column = 2 Calls from ads + 2 `[TSD] Click to call` taps.
  Small volume, but PMax still bids on them. Fix = tap action 7835539864 → Secondary. Branded is Target IS and NB is Max Clicks, so only PMax's bidding changes.
- **NB:** heating-only works (all spend on Heating & Furnace Repair, 749 impr). 0 leads on $123 is too early under the ≤ $200/real lead rule.
  Clicks on competitors: steve sirc clark nj $13.10 (2), advanced heating and cooling asbury nj $9.28; research: gas valve for furnace replacement cost,
  when heater is not working. Boiler terms showing (oil boiler technician near me clicked): boiler service still unconfirmed with ICS (10-08 question).
- PMax underspends ($28 of $40) while it relearns on the new goal.

---

## 2026-10-28 (later) — APPLIED fu-109 items 1-3 (Edu's go), total still $77/d

Script `ics_apply_1028.py` (this folder), validate-only first, then live. Read-back confirmed every change.
1. **PMax** 22890783804: $50 → **$40/d**. Bidding goal: campaign-level PHONE_CALL_LEAD (Calls from ads + [TSD] Click to call
   ad-button taps + Landing Page Call + GA4 phone_link_click) → custom goal **"TSD | Calls + Forms (no taps)"**
   (customConversionGoals/6459689709) = Calls from ads (60s) + Landing Page Call (30s) + Submit lead form - web (GTM) +
   Lead form - Submit. ghl_* GA4 imports left out (they double-count the GTM form). Same fix as Watt's Right 10-27.
2. **NonBranded** 24047025253: AC Installation & Replacement **PAUSED** (Heating & Furnace Repair is now the only live ad group;
   AC Repair was already paused). Max Conversions → **Max Clicks, $15 cap** (no Google bid estimates, the heating keywords barely
   serve; Keyword Planner furnace repair top-of-page $5–48, actual heating CPC ~$7). **$15 → $22/d.**
3. **Branded** 23675636592: **$12 → $15/d** (Target IS unchanged, $7 cap).
**Expect:** PMax converts less on paper (taps no longer counted) and should drift toward real calls and forms. NB spend shifts fully
to heating, with more clicks at ≤$15. ⚑ Recheck 2026-11-04 (fu-109): PMax real calls/forms per $, NB heating clicks + search terms + leads, Branded IS.

---

## 2026-10-28 — Checkpoint on the 10-08 changes (fu-012, read-only, NO changes)

Main account 4571881760. Script `ics_checkpoint_1028.py` (this folder). PRE 09-20→10-07 vs POST 10-09→10-26 (18 days each).
change_event since 10-08: only the 10-08 apply, a 10-10 auto-apply keyword REMOVE in Branded (before the 10-16 auto-apply cleanup)
and the 10-16 AI Max cleanup on 2 paused rebate campaigns.

| | PRE | POST |
|---|---|---|
| PMax | $733, 6 counted (all Calls from ads) = $122/call | $936, 8 counted = 1 Calls from ads + 7 [TSD] Click to call taps |
| Branded | $129, 3 real (5 reported, 2 ghl dups) | $180, 7 counted = 5 taps + 1 Landing Page Call + 1 form |
| NonBranded | $448, 3 | $287, 1 (Landing Page Call) |

- **PMax fails the rule (≤ ~$150 per call).** Real ad calls ≥60s: 6 → 1, so ~$936 per real call. Ad calls placed went UP
  (16 → 24), but the length mix collapsed: under 20s 2 → 14, 60s+ 7 → 4 (all campaigns). CallRail "Google Ads" calls: 16 → 20,
  ≥60s 8 → 5. The 10-01→10-15 call-wins log already showed most ad calls ending inside ICS's extension menu with no live person.
  So people are calling and dropping before they reach anyone, or are accidental taps (Search Partners up $107 → $160). Can't
  separate the two without listening to the 10-16→10-27 calls.
- "[TSD] Click to call" (CLICK_TO_CALL = taps on the AD's call button, origin CALL_FROM_ADS; corrected later 10-28, first written as site taps) is primary and now makes 7 of PMax's 8 and 5 of Branded's 7 conversions.
  PMax bids toward taps that rarely turn into a 60s call. Same problem fixed on Watt's Right 10-27 with a no-taps custom goal.
- PMax Search IS 15% → 16%, budget-lost 14% → 21%; YouTube spend fell $49 → $15 (the "air conditioning" neg removal moved spend to Search).
- **NonBranded fails the rule (≤ ~$200 per real lead):** $287 / 1. The heating focus didn't take: Heating & Furnace got $43 / 6 clicks
  (IS < 10%, 62% rank-lost), and AC Installation & Replacement took $244 / 32 clicks on research and DIY terms (cost, how to install,
  mobile home units, mini split sizes, brand installers, competitor smiths heating newton).
- Branded: fine. ~$45–60 per real lead, IS 81%, now 15% lost to budget at $12/d (avg CPC $4.86 under the $7 cap).
- Rules conflict: pausing NB "and moving $15 to PMax" would fund the campaign that also failed. Decision for Edu (fu-109).

---

## 2026-10-08 — APPLIED steps 4, 5 (rebate), 6, 7, 8 (verified by read-back)

Ran `ics_changes_2026-10-07.py --live` (24 ops, one atomic request) with auto mode off, on Edu's "go". All 24 applied, and a read-back confirms each one:
- **PMax** `22890783804`: removed negatives "air conditioning" (PHRASE) and "rebate" (BROAD + PHRASE); added "tech support" (PHRASE). 430 → 427 negatives. Budget **$40 → $50/day**.
- **NonBranded** `24047025253`: **AC Repair ad group (197798871825) PAUSED**; Heating & Furnace Repair + AC Installation & Replacement still enabled. Added 16 campaign negatives (PHRASE): greensboro, cleveland, brooklyn, nyc, san antonio, mattituck, lowe's, lowes, home depot, window ac, window air conditioner, window unit, for sale, without outdoor unit, frigidaire, windmill. Budget **$25 → $15/day**.
- **Branded** `23675636592`: Target IS CPC ceiling **$5 → $7** (top of page 95% unchanged). Budget $12 unchanged.
- Total daily budget unchanged at $77.

**On hold (Edu):** step 1 CallRail check (if NonBranded shows real calls, raise it to $20), step 2 questions for ICS (Saturdays, boilers, AW-1064128677), step 3 setting the ghl_* + dead GA4 imports to secondary (UI only).
**Checkpoint ~2026-10-28:** PMax cost per call ≤ ~$150, else roll back the $10. NonBranded heating ≤ ~$200 per real lead, else pause it and move its $15 to PMax. Compare with `all_conversions` if step 3 lands in between.

## 2026-10-07 (later) — Next-steps plan (recommendations only, nothing applied)

**Extra findings (90d, 07-09 → 10-06):**
- PMax: $3,662.68, 28 conv (Search $2,726.56 / 22; Search Partners $732.97 / 6, same ~$122 per conv, so partners are fine). Display/YouTube/Discover $203 / 0. Brand terms in PMax search insights are small ("ics hvac" 1 conv / 30d). PMax IS ~15%, mostly lost to rank (72%), only ~13% to budget, so more budget won't buy calls at the same $120.
- **PMax negative list (430 terms) includes "air conditioning" PHRASE**, which blocks every query containing it. It also includes rebate (broad+phrase), Equipment, Financial, Loan, options, types, How/what/why, Discount/Coupon/Promo (all broad). Insights also show manufacturer "tech support" queries (rheem/carrier/goodman/mitsubishi).
- NonBranded: $2,048.46 / 8 reported, **6 real** (2 were ghl_ac_ppc dups) = ~$341 per real lead. IS under 10% every month since July. 25 phrase keywords, **zero negatives**. Search terms: competitor names (2 of the conversions came from these), out-of-area (Greensboro NC, Cleveland, Brooklyn, NYC, San Antonio, Mattituck), DIY/retail (Lowe's, Home Depot, window AC, "for sale"). Heating & Furnace ad group got only 13 clicks in 90d (summer).
- **Website calls are almost invisible to Ads:** Landing Page Call = 1 in 90d, First Time/Repeat Phone Call = 5 (secondary). CallRail + the Google forwarding-number tag both run on the site. NonBranded calls from the site may not be counted.
- Branded Target IS: top of page 95%, **CPC ceiling $5**; lost 14–17% to rank.
- Geo: northern NJ counties (Bergen, Essex, Hudson, Morris, Passaic, Sussex, Union, Warren) + a few towns; PMax excludes Jackson Twp.

- **Heating rationale, checked with Keyword Planner (NJ statewide, Google Search, Sep 2025 → Aug 2026):** "furnace repair" 1,600 (Sep) → 5,400 (Oct) → 8,100 (Nov) → 9,900 (Dec) → 12,100 (Jan/Feb). "ac repair" 6,600 (Sep) → 4,400 (Oct) → 3,600 (Nov–Feb). "boiler repair" 880 (Sep) → 2,400–2,900 (Oct–Feb). Top-of-page bid range: furnace repair $5–48 vs ac repair $23–114.

**Plan given to Edu:** Step 0 check CallRail for Google Ads calls to NonBranded landing pages. Budget at the same $77/d total: PMax $40→$50, NonBranded $25→$15 (heating-focused, AC Repair paused for winter), Branded $12 unchanged. Changes: ghl_* + dead GA4 imports to secondary; remove "air conditioning" PMax negative and review the others; add "tech support" negative; NonBranded negatives; Branded CPC ceiling $5→$7. Checkpoint ~10-28.

**Steps 4, 6, 7, 8 STAGED (applied 2026-10-08, see entry above):** `clients/integrate-comfort-systems/ics_changes_2026-10-07.py`, one atomic request, now 24 operations after Edu approved removing both "rebate" PMax negatives (broad + phrase, step 5). Validate-only run passed 2026-10-07. The live run (`--live`) was blocked by Claude Code auto mode, so Edu needs to run it with auto mode off. Steps 1, 2, 3, 5 on hold per Edu.

## 2026-10-07 (later) — GTM check on the branded double count (read-only, no changes)

**Question (Edu):** is the branded form double count real, given the Ads lead tag fires on the GHL custom event?

**Found:**
- GTM `GTM-N4QW8BF` (account 6002097837, container 32532837), live v19: `Google Ads | Event | Lead` (awct, label `ZdW2CKaGvoccELTendwB` = "Submit lead form - web") fires on `cEvent - Lead` = custom event `form_submitted`, pushed by `cHTML - GHL Form Listener` from the GHL iframe's `set-sticky-contacts` message. GA4 `generate_lead` and Meta Lead fire on the same trigger. **Edu is right about this part.**
- **But no GTM tag sends `ghl_contact_us`, `ghl_service_area`, `ghl_survey` or `ghl_ac_ppc`.** They reach GA4 property `310245312` some other way (most likely the GHL form's own tracking, or a GA4 create-event rule; our GA4 token can't see this property). Ads imports them as primary SUBMIT_LEAD_FORM actions, so they count on top of the GTM tag.
- **Pairs from the same click, last 90 days** (same click date, hour, device and ad group): 07-19 (Submit lead form - web + ghl_survey), 07-29 and 08-10 (Form Submission + ghl_ac_ppc), 09-12 (+ ghl_service_area), 10-02 (+ ghl_contact_us). 5 of 11 form fills were counted twice. The other 6 were the Ads tag alone.
- "Form Submission" (label `FNPZCOqKlIoDELTendwB`) is not in GTM v17–v19, so it also fires from outside GTM. Last seen 08-10.
- The site also hard-codes `AW-1064128677`, which is not this account's tag (this account = AW-461860660). Not investigated.

**Fix (not applied):** nothing in GTM. In Google Ads, make the GA4 `ghl_*` imports secondary and keep the GTM tag as the single primary form action. Do it in the UI, because the API `primary_for_goal` toggle is a no-op and the actions share the SUBMIT_LEAD_FORM/WEBSITE goal.

**Deduplicated numbers (same session):** GA4 `ghl_*` events dropped when an Ads-tag form conversion shares the same click key (date, hour, device, ad group).
- 7d (09-30 → 10-06): $488.26, 3 real leads (4 reported), CPL $162.75. Branded $57.25 / 1 lead. Unbranded $431.01 / 2 PMax calls = $215.51. NonBranded Search $183.86 / 0.
- 30d (09-07 → 10-06): $2,171.73, 16 real leads (18 reported), CPL $135.73. Branded $208.15 / 4 = $52.04. Unbranded $1,963.58 / 12 = $163.63 (PMax $1,197.37 / 10 calls = $119.74; NonBranded $766.21 / 2 = $383.10).
- Search-only CPC (excl. PMax YouTube/Display/Discover): 7d $10.08 on 47 clicks; 30d $8.88 on 237 clicks.

## 2026-10-07 — 7-day PPC check, main account 4571881760 (read-only, no changes)

**Window:** 2026-09-30 → 2026-10-06 (LAST_7_DAYS). PPC only, LSA accounts not included.

| | Spend | Leads (reported) | CPL | CPC | Search IS |
|---|---|---|---|---|---|
| Account | $488.26 | 4 | $122.07 | $4.36 | under 10% (Google floor value 0.0999) |
| Branded Search (`TSD_03.22_Search_Branded_Evergreen`) | $57.25 | 2 | $28.63 | $3.58 | 83% (17% lost to rank) |
| Unbranded = NonBranded Search + PMax | $431.01 | 2 | $215.51 | | |
| ↳ `ICS_Search_NonBranded_Core_2026-07` | $183.86 | 0 | | $15.32 | under 10% (61% rank-lost, 33% budget-lost) |
| ↳ `TSD_03_22_Pmax_Evergreen` | $247.15 | 2 calls | $123.58 | | n/a |

30-day (09-07 → 10-06): $2,171.73, 18 reported conv, $120.65 CPL. PMax $1,197 / 10 calls; Branded $208 / 6; NonBranded $766 / 2 forms ($383 CPL).

**Found:**
- PMax calls are real: "Calls from ads" uses a 60s threshold, and call_view shows the 2 counted calls at 376s (10-01) and 119s (10-06). The other 4 calls that week were under 60s.
- **Likely double count on branded form fills:** 10-02 logged both "Submit lead form - web" and "icshvac.com - GA4 (web) ghl_contact_us" in the branded campaign; 09-12 logged "Submit lead form - web" + "ghl_service_area". About 14 overlapping primary lead actions are enabled (GA4 form_submit_*, ghl_*, plus phone_link_click and mailto_link_click as leads). So the real count this week is probably 3, not 4.
- **Oct 5–6 click spike = PMax YouTube**, not search demand: 55 YouTube clicks for ~$10.50. Inflates account clicks and makes CPC look low.
- PMax runs **Mon–Fri 7am–5pm** only (ad schedule). Google paces the monthly budget into weekdays, so it spends $55–80/day on a $40/day budget. 30d spend ≈ $40 × 30, so no overspend.
- NonBranded search terms that showed (4 of 12 clicks): competitor names (harmony hvac rockaway nj, ck control temp green brook nj), "hvac companies new jersey", and junk ("blue star ac 2 ton price 5 star").
- `change_event`: no edits in the account from 09-23 to 10-07.

**Did:** nothing on the account.

## 2026-09-29 — Confirmed current client; data from the Growth Engine pull (read-only, no changes)

**Confirmed by Edu (2026-09-29):** Integrate Comfort Systems is a current TSD client. This resolves the
first open item below.

**Found** (Growth Engine pull, 2025-09-29 → 2026-09-27, `paid/relatorios/growth-engine-pull-2026-09/`):
- Four Integrate accounts under the MCC, all New York DMA:

| Account | Customer ID | Spend, 12 months |
|---|---|---|
| Main | `4571881760` | $31,732 |
| LSA Belleville (this log) | `2895702982` | $8,949 |
| LSA Carlstadt | `2175964343` | $594 |
| LSA Englewood Cliff | `8323145223` | $0 |

- **TSD has run the main account since at least 2026-03-22.** `4571881760` has TSD-named campaigns
  from that date: `TSD_03_22_Pmax_Evergreen` ($16,468, ENABLED), `TSD_03.22_Search_Branded_Evergreen`
  (ENABLED), and paused TSD_04.25 / TSD_05.04 Search. It also has `ICS_Search_NonBranded_Core_2026-07`.
- **"ICS" = Integrate Comfort Systems.** So the active Meta ad account named "ICS" (`2070047533283360`,
  Meta connector disabled for it) is very likely theirs.
- **"Mitsubishi YouTube"** (`23599485735`, in this account):
  - $5,015 over 12 months, $6.49 in-stream CPM.
  - 31 weeks at a median 1.44x weekly frequency, never reaching 3x.
  - $1,890 of it served on connected TVs.
  - The only visible human edit in this account is `chriswisics@gmail.com` (2026-08-18), so it's
    unclear whether TSD runs this campaign.

**Did:** nothing on the accounts. In the Growth Engine `client_roster.csv`, Integrate counts as a
current client, with its YouTube treated as TSD delivery until confirmed otherwise.

## 2026-09-11 — initial history/change check + weekly budget question

**Researched:** account structure, change history (`change_event`/`change_status`), LSA lead
volume, and — on a follow-up ask — when/who set the LOCAL_SERVICES campaign's budget to $10/week.

**Found:**
- 30 campaigns total, only 2 ENABLED: the system-generated `LOCAL_SERVICES` campaign
  (`LocalServicesCampaign:SystemGenerated:0005d4e194c1ee73`, id `15786867110`) and "Mitsubishi
  YouTube" (VIDEO, id `23599485735`, $20/day budget). The other ~28 (Search/PMax/Display/Smart/old
  Video, e.g. the "RTM ..." series and "INTEGRATE COMFORT SYSTEMS | Google Optimized") are PAUSED
  — leftover from a prior agency build, not touched by us.
- **Change history:** `change_event` (API max lookback 30 days) shows exactly one human/API edit
  in that window — `chriswisics@gmail.com` added a YouTube video asset on 2026-08-18, unrelated to
  the LSA campaign. `change_status` (API max lookback 90 days) shows 59 entries, all Google-side
  automation (asset/ad-group-criterion churn on paused campaigns, plus same-day automated touches
  on Mitsubishi YouTube and the paused "RTM Heating PMAX") — none are `CAMPAIGN_BUDGET`.
- **LSA lead volume (365d pull, `local-services-leads`):** 48 leads total (30 charged, 18 not; 33
  phone calls, 15 messages). By month: Apr 12, May 30, Jun 1, Jul 3, Aug 2 (last lead 2026-08-10),
  **zero since** — matches the campaign's near-dead serving (4 clicks / 25 impressions over the
  trailing 30 days).
- **Weekly budget ($10/week = $1.43/day on `campaignBudgets/10147464134`):** checked
  `change_event` for `CAMPAIGN_BUDGET` changes (30d max) and `change_status` for the same resource
  type (90d max, the API's hard ceiling — cannot query further back) — **zero hits in either
  window.** Two explanations, can't distinguish from Ads data alone: (a) the budget predates
  2026-06-13 and is simply outside what the API's change history can show, or (b) it was set
  through the separate Local Services Ads provider dashboard, which doesn't log into Google Ads'
  `change_event`/`change_status` even though the resulting number surfaces on the campaign_budget
  object. Flagged as a loose, unconfirmed correlation: the timing sits right at the edge of the
  90-day window and near the May→June lead cliff — not proof of cause.

**Did:** read-only investigation, no changes made to the account.

## Open items
- ~~Confirm with Edu whether this is a live engagement or diligence-only~~ → **resolved 2026-09-29:
  current client.** Still to do: register all four accounts in `contas.yaml` and move Integrate to the
  Clients list in `clients/README.md`.
- Confirm whether TSD runs "Mitsubishi YouTube". If not, set a `tsd_managed_since` date for this
  account in the Growth Engine `client_roster.csv` and rebuild.
- Origin of the $10/week LSA budget still unresolved — needs checking directly in the Local
  Services Ads dashboard (not visible via Ads API), or asking `chriswisics@gmail.com`, the only
  user account with visible activity here.
- "Mitsubishi YouTube" (VIDEO) spent ~$595 over the trailing 30 days with 0 conversions — flagged,
  not investigated.

---

## 2026-10-09 — ⚠ CallRail → Google Ads integration went DISABLED (side effect of the C&S reconnect session)

Found via CallRail API (read-only) after Edu reconnected C&S Air integrations with access@topservdigital.com in the CallRail
UI. This client's CallRail Google Ads integration (MCC 4155514468 → this account, first-time vs repeat) was **active
earlier on 10-09 and is now DISABLED**. Same happened to All Heart (offboarded) and ICS/Spencer: exactly the 3
integrations routed through MCC 4155514468. Cause not confirmed (re-auth side effect or the browser agent).
access@topservdigital.com is ADMIN on MCC 4155514468, so it can re-enable them.

Impact: CallRail call conversions (`First Time Phone Call` / `Repeat Phone Call`) stop reaching this Google Ads account
until it is re-enabled. **Fix: reconnect in CallRail with access@topservdigital.com via MCC 4155514468, same settings.**

ICS was receiving a few: 30d First Time 2 + Repeat 2, last 09-29. Matters for the 10-28 checkpoint (PMax cost per call).

## 2026-11-13 — Heating LP (AT 82ecaff6) reviewed for Edu's Review & Close

Sha completed Execution; task sits in Review & Close on Edu (AT API down today, close it in the UI). Re-checked live 11-13 ~15:00 BRT:
- Page vs brief: H1 exact, brand line "Family-owned. Northern NJ since 1990.", (866) 658-2987 x23 (tel +18666582987), main line 866-749-6331 only in the site-wide schema, GHL form 9yoyys68IRpTtwyjDdjr in the hero card + 2 lower CTAs, noindex, viewport meta OK, GTM-N4QW8BF. Desktop render (1366px) clean: hero, 4.9/363 reviews strip, trust bar, reviews, "Signs you need heating repair". www 301s to non-www.
- Hardcoded gtag `AW-1064128677` on the page = base config only (no send_to / conversion event), so no double count from it; the Ads "Lead" conversion fires from GTM tag 93 (tested 11-12). Question closed.
- Mobile: headless phone render blocked by the site's "Confirm you are human" check (not bypassed). Edu checks on his phone.
- Campaign 24047025253: ENABLED, LIMITED (BIDDING_STRATEGY_LEARNING, normal after the 11-12 rebuild). New RSA 831383124121 APPROVED → the new page. 11-12: $29.02 / 106 impr / 6 clicks / 1 conv (= Edu's 09:40 BRT test lead; exclude at the 11-19 read, delete the GHL test contact). 11-13 so far: 22 impr / $0. Search terms clean (no-heat/furnace-not-working intent) + competitor names at 0 clicks (iceman, ixim, o neill, smith heating, your ultimate comfort): add as negs at the 11-19 read if they take clicks.

## 2026-11-16 — quick read-only peek (11-12..11-15), no changes

- NB 24047025253: $105.76 / 631 impr / 20 clicks / 1 conv (11-12 'Landing Page Call', logged as Edu's test lead; confirm at fu-159). Search terms with clicks: 2 of 3 are competitor names (total comfort westwood 2 clicks $12.74, 1 800 heaters edison $6.49) + furnace repair. Add competitor negs at the 11-19 read.
- Branded: $10.98 / 2 clicks / 0 conv (quiet).
- LSA Belleville: impressions ramping after the $50/d raise (11-11: 5 → 11-13: 74), $0 cost, 0 leads yet. Carlstadt 4-12 impr/d. Englewood still 0 impressions.
- Mitsubishi YouTube (Belleville acct) still ~$21/d, owner still unknown.

## 2026-11-16 — DEEP DIVE (read-only, nothing changed). Scripts: ics_deep_1116_ppc.py / _ppc_b.py / _ppc_c.py / ics_deep_1116_lsa.py (this folder) + CallRail API + AT + Slack

**Correction to the 11-13 note:** the 11-12 NB conversion is NOT Edu's test. call_view: 2026-11-12 13:05 ET, **170s, type LANDING_PAGE, area 956, campaign NB** = a real call through the Google forwarding number on the new heating page. It bypassed CallRail (no matching call there; Google's forwarding number goes to the main line, not the 866-658-2987 tracker), so CallRail will never show paid website calls. The test form (fake gclid) did not register as a conversion.

**1. Spend is ~1/4 of last heating season.** Nov-25 $3,093, Dec-25 $5,010, Jan-26 $4,783, Feb $2,065, Mar $1,658 ($2000 Rebates Search $2.4-2.8k/mo + PMax $2-2.2k/mo). Real calls last season (Calls from ads 60s+): Rebates 40 + PMax 46 + 6 LP calls on ~$16.6k = ~$180/call. Nov-26 to date $845; current run rate $40/d (~$1.2k/mo). Apr-Jun 2026 both PPC and LSA Belleville collapsed in June (PPC $569, LSA $24): looks like one cut, PPC came back in July (ICS_Search_NonBranded_Core_2026-07), LSA never did. AT client record `ads_budget_marketing` = null: no approved budget on file.

**2. LSA serves only Mon-Fri 7am-3:59pm, both profiles, always.** Belleville May-26 (the 30-lead month): 0 impressions Sat/Sun, 0 after 15:59; same in Nov-26 (0 on 11-07/08, 11-14/15). Carlstadt Oct-26 identical. The May leads came Mon-Fri 7-17h because that's the only window it runs. NB data says heating demand is 42% Sat+Sun and 31% 8pm-midnight. Fix = LSA profile hours / "show ads during business hours" in the LSA dashboard (not in the API). Belleville after the $50/d restore: impr 5 (11-11) → 27 → 74 → 0 → 0 → 27 (11-16), 17 clicks, 0 leads, $0. All 3 profiles on Maximize leads (API MAXIMIZE_CONVERSIONS; Carlstadt/Englewood tCPA $60). Englewood (1 town) overlaps Carlstadt's 27-town geo and has never served; verification now all PASSED. Not a lever.

**3. NB since relaunch (11-12..11-16): $111, 641 impr, 21 clicks, 1 real call (above).** IS 18-24%, **lost-rank 43-77% on weekdays**, lost-budget 32-63% Sat/Sun; top IS 12-15%, abs-top 10%; CPC $5.4 under the $20 cap (Max Clicks buys bottom-of-page). Mobile 80%. 'heating repair nj' PHRASE = 77% of impressions and matches 'hvac repair paramus nj' (78 impr, 0 clk), 'hvac repair mahwah nj' and ~35 competitor names; competitor clicks $24.64 (22%): total comfort westwood $12.74, 1 800 heaters $6.49, bogush $5.41. Geo: Newark $8.40 + Elizabeth $10.75 (17%) + Paterson 13 impr = cities the client EXCLUDES in its own LSA geo. 'furnace not working' EXACT 58 impr / 0 clk (why/how-to variants). Branded 11-01..11-16: $84 / 15 clk / 0 conv, IS ~100%, fine.

**4. Calls (CallRail 10-17..11-16, 99):** GBP 48 (31 at 60s+), Direct 19, Google Ads 15 (8 at 60s+, 10 gclid), Organic 10, Bing 3; ~25/wk. Last week 26 calls, 0 paid. Ad calls since 11-01: 11-02 66s, 11-04 22s, then none (PMax paused 11-11). IVR task 5e5dcc2a still in Execution with Angela, no answer; be762554 (Belleville cut / YouTube owner) same. CallRail→Ads integration is ACTIVE again (was disabled 10-09) but 0 uploads in 30d (no gclid website calls to upload).

**5. Mitsubishi YouTube is the client's own:** chriswisics@gmail.com (Chris, the owner) added YouTube video assets 11-02 (x3) and 11-15. TARGET_CPV $20/d, Bergen/Essex/Hudson, custom-intent audiences, 30d $605 / 55k impr / 83 clicks, 28% connected TV. Leave it; exclude from TSD numbers.

**6. Conversion actions:** 26 enabled, 25 primary (GA4 form_submit_* x4, ghl_* x4, mailto, phone_link_click, book_now, 'Phone Call', 'Form Capture', 'Form Submission'...). NB bids on custom goal 6459689709 so bidding is clean; the Conversions column is not. UI cleanup still pending.

**Plan proposed to Edu (nothing applied):** A LSA hours → 24/7 (dashboard; Chris or whoever has LSA access, Marlo was chasing it 10-01). B IVR: route 866-658-2987 + the 2 LSA trackers to a direct service line (CallRail destination). C NB: Target IS top-of-page ~65% cap $15-18 (or keep Max Clicks) + budget $25 → $50-60/d; ~35 competitor PHRASE negs + why/how to/can a; exclude Newark/Paterson/Elizabeth/Irvington; add 'hvac repair' kws. D Budget ask via Angela (last Nov-Jan $3-5k/mo). E PMax stays paused until the IVR is fixed; relaunch on the heating LP (7-day schedule, NB geo, no-taps goal) if budget comes. Next read fu-159 11-19.

## 2026-11-16 (later) — APPLIED plan C on NonBranded (Edu: "approved"), total budget unchanged $25/d

`ics_apply_1116.py` (this folder), validate-only PASS then `--apply`, read-back confirmed:
1. Bidding Max Clicks ($20 cap) → **Target Impression Share, TOP_OF_PAGE, 65%, CPC ceiling $18** (learning restarts).
2. **+51 campaign PHRASE negatives** (now 89): ~42 competitor names from search terms (total comfort, 1 800 heaters, bogush, smith heating, ixim, iceman, oneill/o neill/o'neill, scotty and son, good tidings, comfort pro, princeton air, revere plumbing, schaible, splash plumbing, pete manley, platinum hvac, nj hvac and plumbing, air group, atlantic heating, colella, merring, climate care, dave's/daves heating, ductmate, gold medal, ideal air, jack dong, keil, perfection contracting, russo brothers, edison heating, sunrise heating, tanous, trinity air, warren heating, your ultimate comfort, harmony hvac, ck control temp), plumbing/plumber/plumbers, why / how to / can a / what's wrong / whats wrong / if the.
3. **Negative locations** Newark 1022300, Paterson 1022331, Elizabeth 1022108, Irvington 1022190 (the 4 cities the client excludes in LSA Belleville).
4. Heating ad group 197798871985: +hvac repair [EXACT], hvac repair near me [EXACT], hvac repair nj [PHRASE] (19 enabled keywords).
**Rollback:** campaign bidding back to target_spend cap $20; remove criteria ids printed in the apply output (saved in the script run, 11-16).
**Expect at the 11-19 read (fu-159):** top IS 13% → 50%+, CPC up toward $9-15, fewer clicks per $ but top-of-page on mobile "no heat" searches; competitor + Newark/Elizabeth spend gone. Judge on real calls (call_view LANDING_PAGE + Calls from ads) not clicks.

**E:** PMax stays PAUSED until the phone menu is fixed; relaunch (heating LP, 7-day schedule, NB geo, no-taps goal, $40/d) to be staged when B + budget land.

**AT Internal Request DRAFT 8861cf80-f0c1-4f89-84ec-99fa1eb9fc09** "Three questions for Chris: Local Services hours, phone menu, winter budget" (A + B reminder of 5e5dcc2a + D, suggests ~$3k/mo Google for Nov-Feb; closes the Mitsubishi owner question). Intake = Edu to submit, Execution = Angela, Review & Close = Edu. https://app.agencytitan.com/tasks/instance/8861cf80-f0c1-4f89-84ec-99fa1eb9fc09


## 2026-11-19 — fu-159 first read of relaunched NonBranded (read-only, nothing changed). Scripts ics_read_1119.py / ics_read_1119b.py

**NB 24047025253, 11-12..11-18 (7 full days): $193.58 / 35 clicks / CPC ~$5.5 / 1 real lead** (11-12 13:05 ET, 170s call through Google's forwarding number, area code 956; call_view type now reads MANUALLY_DIALED). $194 per real lead vs the ≤ ~$200 rule from 10-28: borderline, one data point. Branded $40.66 / 7 clicks / 1 conv.
- **Plan C (11-16) has not moved the auction yet:** 11-17 / 11-18 CPC $5.9, top IS 10-13%, abs-top 10% (same as before), spend pinned at ~$29.5/day. Budget is the binding limit: budget-lost 64% on 11-17, and the day's share is high only until the money runs out (11-19 morning IS 61 / top 36 at $0 spent). Status LIMITED / BIDDING_STRATEGY_LEARNING. Target IS 65% top cannot be reached on $25/day; the winter budget ask (AT 8861cf80, submitted 11-16, In Progress with Angela, no answer) decides this.
- **QS:** 1-3 on every rated keyword, landing page experience BELOW AVERAGE everywhere except 'boiler repair near me' (4, average). Expected CTR below average on all. The new heating page has not lifted QS yet.
- **RSA 831383124121 APPROVED** (heating page). The 2 old AC RSAs (→ /ac-repairs/, /ac-installations/) are still enabled in the campaign.
- **Clicked terms** (Google shows only 5 for the week): furnace repair, who fixes gas furnaces, and 3 competitors 11-14..11-16 (1 800 heaters, total comfort westwood, bogush; all negated 11-16). **Impression-only terms 11-17..11-19 still include ~15 competitor names** (arctic ac / arctic air conditioning old bridge, delta heating and cooling, dennis terhune, efficient air service, kays affordable, l&f hvac, ludlow heating, poust / rpoust, sam's air control, verona heating and cooling, bi state, dj wagner, dwyer, energy solutions, hart and iliff) + AC terms (ac repair nj, a c repair near me, ac repair bergen county) on the heating page. 0 clicks on them so far.
- **Forms:** 0 real form leads since the relaunch (no 'Lead' conversion; Edu's 11-12 test lead PASSED in Tag Assistant but carried a fake gclid, so it never registered in Ads). Only GA4 page_view all-conversions show (secondary).
- ⚠ **Client Request a569ef96 "Inquiry Forms" (Chris, 11-18, due 11-23):** replace the general forms (/contact-us/) and service/booking forms (/book-online/) with **Ascora** enquiry/booking widgets, + "Book a Service" in the menu. If that reaches the heating landing page, the GHL form + GTM 'Lead' listener stops counting. Also b5880d5c (Daniel, due 11-20) asks Chris whether the Ascora button sits next to or replaces the forms. Paid needs a say before the swap: either keep the GHL form on the ad landing page or get an Ascora conversion signal (thank-you page / postMessage) into GTM.

**Staged for Edu (not applied):** (1) ~15 competitor PHRASE negatives above + 'ac repair' / 'a c repair' PHRASE on NB (heating-only campaign) ; (2) pause the 2 AC RSAs if the campaign is heating-only now; (3) hold bidding/budget until Angela answers 8861cf80; (4) note on a569ef96 about the ad landing page form. Next read fu-159 → 11-24.

## 2026-11-19 (later) — APPLIED staged items 1 + 2 (Edu: "apply 1 and 2, yes"). Script ics_apply_1119.py (validate-only PASS, then --apply)

1. **+21 campaign PHRASE negatives on NB 24047025253** (89 → 110): arctic ac, arctic air, delta heating, dennis terhune, terhune, efficient air, kays affordable, l&f hvac, ludlow heating, poust, rpoust, sam's air control, sams air control, verona heating and cooling, bi state heating, dj wagner, dwyer heating, energy solutions, hart and iliff, ac repair, a c repair. Criterion resource names printed in the apply output (ids 295628663900 ... 1020222550).
2. **Old AC RSAs PAUSED:** 817245367824 (AC Repair ad group, → /ac-repairs/) and 817245367830 (AC Installation, → /ac-installations/). Their ad groups were already PAUSED, so they weren't serving; this is cleanup. Live = heating RSA 831383124121 only.
- ⚠ The guard first ABORTED: 'ac repair' matches enabled keywords in the PAUSED AC Repair ad group (ac repair nj / near me / emergency ac repair). Guard narrowed to enabled ad groups. **If AC Repair 197798871825 is re-enabled in spring, remove the 'ac repair' + 'a c repair' negatives first.**
Rollback: remove the 21 criteria; set the 2 ads to ENABLED. Read at fu-192 (11-24).

## 2026-11-19 — fu-150: LSA delivery one week after the 11-11 restore (read-only, nothing changed). Script ics_lsa_read_1119.py

**Belleville 15786867110 ($50/day since 11-11):** impressions ramped 5 (11-11) → 27 → 74 → 99 (11-16) → 54 → 73; clicks 1-13/day. **First charged leads: 11-16 13:08 ($106.38) and 11-18 08:54 ($98.80)**, ~$100 each (May 2026 was ~$48). Both real new customers (transcribed locally): 11-16 condo owner in Queens, old 2002 HVAC with a suspected heat exchanger issue, PSE&G involved, wants quotes, Jason quoted the $149 service call; 11-18 Kearny-area building, 2-3 year old boiler won't start, installer gone, Jason taking it. Phones answered by Jason directly (no IVR drop on these two). $205 spent of a possible ~$400.
**Englewood 21467507022 ($50/day since 11-11):** still 0 impressions ever. UI check still owed (profile/reviews/hours).
**Carlstadt 21042970942 ($51.43/day):** 1-20 impr/day, 0 charged leads since 11-01.
**AT be762554 (did the client cut Belleville in June, Mitsubishi YouTube owner):** Execution with Angela since 11-11, no reply. The newer 8861cf80 (11-16: LSA hours, phone menu, winter budget) also unanswered. Mitsubishi YouTube 23599485735 still ENABLED $20/day (client's own, chriswisics@, per the 11-16 deep dive).
Next: keep $50/day; read again with fu-192 (11-24): leads/day, cost per lead vs the $48 May level, Englewood UI check.
