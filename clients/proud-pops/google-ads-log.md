# Proud Pops — Google Ads log (1051843378)

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
