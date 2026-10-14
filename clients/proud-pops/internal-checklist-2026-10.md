# Proud Pops — Internal Execution Checklist (Plan 1)

Source plan: `internal-action-plan-2026-10-07.md` · AM/client side: `am-client-action-plan-2026-10-07.md`
Log every executed step in `google-ads-log.md` and Agency Titan.

**Claude: re-read this file at the start of any Proud Pops session, and tick boxes + fill "Result" the moment a
step is done and verified. Never tick on a mutation's own success message. Tick on a read-back.**

Last updated: 2026-10-13 · **10-13: budgets cut to land October at the approved $50k (D-10); YouTube San Antonio pause = Edu in UI.** Status: see ▶ RESUME HERE. Older status: GTM v43 live. **10-08 evening: H4a/b/c, H5a, G1a/b/c, G2a, G2c applied; G2b switchover waiting on ad approvals.** E1 passed. **B1, B2, B2b, B3, B5, B7 APPLIED 10-08. B4 applied then REVERTED, waiting on Edu's number check.** Under review: B7 ads + B4 call asset → rechecks B7a/B7b + B4 next-day check, then `b4-cleanup`. B6 + D1 done. Next [C]: E2 on Oct 9.

---

## ▶ RESUME HERE (state as of 2026-10-08, end of day)

### Where things stand

**Everything on our side for 10-08 is done.** What's open is waiting on Google review, on data, or on Edu / the client.

**LIVE in the account / site:**
- **GTM v43** (rollback = v42):
  - /careers job applications → GA4 `job_application` only (v42, 10-07)
  - careers guard on "Appointment Scheduled" + Meta Lead tag sends "Lead" (v43, 10-08 12:26 CT)
- **Search Electrical:**
  - AI Max fully OFF
  - 36 + 2 + 1 negatives (H2, H2b; "electricians for hire" negative removed, D-9)
  - ads → /services/electrical (B7)
- **Search Plumbing:**
  - Maximize Clicks, $45 CPC cap
  - "leak detection near me" paused
  - competitor list attached
  - new AG4_Plumbing_General built (H7)
- **Search HVAC:** 9 competitor negatives (H9).
- **Branded:**
  - $100/d, funded by PMax HVAC $325 → $295 (budget-neutral)
  - + "pops electric(al)" keywords
  - 47-city location targeting (incl. New Braunfels)
- **Location targeting:** HVAC + Plumbing on the 20-city core metro; PRESENCE on HVAC, Plumbing, Branded, PMax Electrical.
- **Negatives:** account-level job-seeker list (22 → 26 terms). "job / jobs" BROAD removed from CSMS_Negatives.
- **PMax:**
  - /careers URL exclusion on both
  - Proud Pops brand exclusion + brand negatives on both (H10)
- **Sitelinks:**
  - "Contact Us" → proudpops.com/contact
  - old-domain sitelinks removed
  - "Book a Free Pop-In" → /schedule on all 4 Search campaigns
- **YouTube / account:** account-level exclusions = "content suitable for families" + 34 kids channels.
- **Calls from ads** minimum 60s. **Legacy roofing LSA paused.**

**Under Google review (switchovers run when approved):**
- the 6 B7-edited ads
- AG4_Plumbing_General RSA 827480907116 (→ H7a cutover)
- 14 new site-verified RSAs (→ G2b cutover)
- the "Book a Free Pop-In" sitelink

**Not done / waiting:**
- B4 call extension (reverted; Edu confirming the right number)
- Block F (needs E2 + E3 + client heads-up)
- C1 / C2 GA4 key events and D2 LSA profiles (Edu)
- everything client-side (P-1 to P-14)
- **Agency Titan:** nothing logged there yet, and no AM ticket. All logging so far is local (this file + google-ads-log.md).

### Do next, in this order

1. **[C] Oct 9 morning, run these four checks:**
   - `./tsd.sh proud_pops_b7_delivery_check.py` (B7a / B7b approvals + Electrical / Plumbing delivery)
   - `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/h7_plumbing_general_adgroup_2026-10-08.py cutover --apply` (H7a; refuses until approved)
   - `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/g2b_cutover_2026-10-08.py --apply` (G2b, all 14; pauses only old ads whose replacement is approved)
   - `./tsd.sh proud_pops_verify_careers_fix.py` (E2) + Meta MCP `ads_get_dataset_stats` pixel 597145242772352, event Lead (G5a)
2. **[E] Client heads-up (P-1)** + AM ticket in Agency Titan (P-1 to P-14). Claude can draft it on request.
3. **[E]** B4 phone number · C1 / C2 GA4 key events · D2 LSA profiles · D-2 August report.
4. **[C] Oct 10:** E3. **Oct 12–13:** Block F if unblocked. **~Oct 13–15:** H1a, H3d, G1d, H9a (search-term re-sweep on
   HVAC / Plumbing / Branded after the location expansion). **Oct 26:** G3 re-baseline + G4.

### History: afternoon update (2026-10-07)

- **Real-world proof the fix works:** 3 real job applications since publish (GA4: 11:00, 12:00, 13:00 CT) were
  all recorded as `job_application`, with 0 `generate_lead` on /careers. The formal E1 still runs on Oct 8.
- **10-08 update:** B3, B5, B7 applied and read back. B4 deliberately left open (Edu will work it).
- **Ready to apply, waiting on Edu's OK:** ~~B3~~, B4, ~~B5~~, ~~B7~~. All four passed Google's validate-only check (nothing written).
  One command each: `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py <b3|b4|b5|b7> --apply`
- **Done:** B6 (pages pass), D1 (LSA snapshot), B3 review.
- **New findings:**
  - Legacy Problem Solvers LSA **3477779749 (PS Roofing SA) spent $83.52 in September**. contas.yaml says the legacy
    accounts have had no spend since ~Apr 2025 → added as D-8.
  - My Favorite Service Company (separate set) spent $2,072.42 in September (Search $1,431, Smart $636).
- **September spend, Proud Pops:** **$60,422.56**
  - PPC account $59,635.16 = Search $36,547 + PMax $16,872 + YouTube $6,082 + in-account LSA $135
  - LSA [1] $387.54
  - LSA [2] $399.86

### Open decisions for Edu

| # | Decision | Recommendation | Status |
|---|---|---|---|
| D-1 | **DONE 10-08, GTM v43 live 12:26 CT.** Add the same `/careers` exclusion to trigger `[73] cEvent - Appointment Scheduled`. It fires `[82]` Ads Lead, `[90]` GA4 Lead and `[111]` Meta Lead with no careers guard. The job form probably never emits `Appointment Scheduled`, and E1 would show it if it does. | Do it if E1 shows any `/careers` lead; otherwise optional hygiene (1 edit + headless test + publish) | closed |
| D-2 | August client report restatement (it said 129 form leads / $256 CPL; ~79% were job applications; 1,069 phone taps called "calls") | Restate August next to September in the September report. Framing is Edu + Jonathan's call. | open |
| D-3 | Branded budget $70 → $100/day | **DONE 10-08, budget-neutral** (Edu: only if taken from elsewhere): Branded $70→$100, PMax HVAC $325→$295. Total $395/d unchanged, both budgets non-shared. No client approval needed (constant total). | closed |
| D-4 | PMax Electrical: pause on Oct 26 if fewer than 5 customer forms since the fix | Decide at G4 | later |
| D-5 | Fix `[111] Meta - Lead` (sent PageView, not Lead) | **DONE 10-08, GTM v43:** standardEventName → Lead. The Meta pixel 597145242772352 IS receiving events (PageView ~100–350/hr, phone_click, instant_quote_hvac_click, Webchat Widget) but had 0 "Lead" Oct 1–8. Verify "Lead" appears from 10-08 12:26 CT (G5a). | closed (verify G5a) |
| D-7 | Branded ads land on the homepage (mobile: no schedule button above the fold) | **DECIDED 10-08: keep the homepage for Branded.** Brand searchers already know Proud Pops and mostly call; the mobile header has a visible "Call" button and "Schedule Your Free Pop-In Visit" sits just below the fold. Branded is the cheapest PPC source. Optional web-team ask → P-14. | closed |
| D-8 | Legacy LSA 3477779749 (PS Roofing SA) spent $83.52 in Sept; supposed to be dormant. | **DONE 10-08:** it was ENABLED/serving at $142.86/d; charged $83.52 for a roofing call on Sep 11 that was then DECLINED. Campaign 20805107400 **PAUSED** by Claude on Edu's instruction (read-back PAUSED/PAUSED). Other 6 legacy accounts checked: all already paused, 0 activity since Jun. | closed |
| D-9 | CSMS_Negatives EXACT "electricians for hire" (customer intent) | **DONE 10-08:** removed (read-back: no longer present). | closed |
| D-10 | Spend back to the approved $50k/mo (Edu 10-13) | **Record + baseline: `budget-cut-2026-10-13.md`.** **APPLIED 10-13** (`budget_cut_50k_2026-10-13.py`, read-back OK): PMax HVAC $295→$50, PMax Elec $230→$75, Search HVAC $375→$300, Search Elec $600→$500. Caps $1,960→$1,385/d. **Edu: pause YouTube San Antonio in the UI** (API can't) → $1,285/d, Oct ≈ $50.2k. Recheck pacing ~Oct 20; Nov 1 steady state ≈ $1,600/d, split decided at Oct 26 review. | open (YouTube SA fu-046 + Oct 20 recheck fu-047 + call check fu-048: Edu wants to see if "no forms" meant more calls, once CallRail access is in) |
| D-6 | Real end-to-end test (actual form submit) | Optional; creates a GHL contact, so coordinate via AM. The headless test already covers the logic. | optional |

### Plan 2 (AM / client) tracker

Source: `am-client-action-plan-2026-10-07.md`. Update the Status column as things move.

| # | Item | Owner | Status | Notes |
|---|---|---|---|---|
| P-1 | Heads-up to client (lead counts dropping, by design) | Edu / Jonathan | **NOT SENT, urgent** | Drop started 10-07 10:32 CT |
| P-2 | Written approval: pause PMax HVAC 23853595615 | Jonathan → client | not requested | $9,814 / 30d, 99% Display, 2 customer forms |
| P-3 | Sept/Oct budget on record | Jonathan → client | not requested | Sept actual $59,635 vs last approval $50k (Aug). **10-13: budgets cut so October lands ~$50k (D-10); tell client spend is back at the approved $50k.** |
| P-4 | ~~Optional Branded raise $70 → $100/d~~ **Not needed:** done 10-08 as a budget-neutral reallocation (D-3) | — | closed | Total unchanged |
| P-5 | CallRail: who owns it, access or Google Ads integration. **+ 10-08:** is 210-225-5767 the main line or a CallRail number? Where does 210-794-7570 come from? Why does CallRail swap no number on proudpops.com (no swap targets)? | Jonathan → client | not requested | Today Google Ads sees zero real calls. B4 on hold pending this. |
| P-6 | LSA asks, now specific (from `proud_pops_lsa_lead_handling.py`, 10-08): (1) who monitors LSA **messages**? 2 recent ones got no reply (Sep 19 duct cleaning, Oct 3 outlets/switches); (2) please mark leads booked/declined in LSA, since 9 of 22 Sept leads are still "active"; (3) which jobs do they NOT do? 61 of 109 June leads and 7 of 22 Sept were declined, so switch those job types off instead (e.g. duct cleaning? light fixture repair? HVAC maintenance?); (4) dispute wrong charged leads promptly (Sep 3 + Sep 6 Electrician declined but charged; credits fell from 7 in Jun to 0 in Sep); (5) license/insurance/verification still current? | Jonathan → client | ready to send (+ D2 findings) | Calls are answered fine: 0 missed (0s) in Sept, 15 of 21 calls over 60s. The impression collapse isn't explained by call handling. |
| P-7 | Hiring: do they want a recruiting campaign? (~130 applications/30d, ~100 via Google Ads) | Jonathan → client | not asked | |
| P-8 | Who is tito@proudpops.com; what are the assets added Oct 1 + Oct 4; loop us in before changes | Jonathan → client | not asked | change_event shows 4 ASSET creates |
| P-9 | ServiceTitan booked jobs by lead source (Sept) | Jonathan → client | not asked | Open since July |
| P-10 | Phone verification for 210-225-5767 call asset, if Google asks | client | n/a yet | Triggered by B4 |
| P-11 | Does Proud Pops run Meta ads (in-house or another vendor)? | Jonathan | not asked | D-5 fixed 10-08; still useful to know whether Meta ads run anywhere |
| P-13 | FYI to client: **AI Max turned fully OFF** on Search Electrical (URL expansion 10-08 a.m., then AI Max + text customization 10-08 p.m.; Brandon enabled it Jun 26). 56% of Electrical's spend was landing on pages other than the ad's (/pricing, a blog post, HVAC/plumbing pages). AI Max itself is still on. | Jonathan → client | not sent | Done 10-08 |
| P-14 | Optional web-team ask: add a "Schedule Your Free Pop-In" button in the mobile homepage hero (above the fold today: First Repair banner + logo only). Helps all homepage traffic. | Jonathan → client | not sent | From D-7 |
| P-12 | September client report: customer forms only, no "calls" for phone taps | Edu / Jonathan | **30-day report DRAFTED 10-08** (Sep 8–Oct 7, `Proud Pops - 30-Day Performance Report (Sep 8 - Oct 7).pdf`) | D-2 framing still open; not sent |

### Baselines (pre-fix, for comparison)

| Metric | Value |
|---|---|
| 30 days (Sep 7–Oct 6) | Lead-gen spend $53,355 · Ads forms 180 (188 by conversion date) · GA4 google/cpc leads 131 = **99 /careers + 32 customer** · est. ~48 customer forms → **~$1,115 / customer form** |
| `Website lead` per day, Sep 23–Oct 6 | **5.00 total**: PMax Elec 3.21 · Search Elec 1.00 · Plumbing 0.29 · Branded 0.21 · Search HVAC 0.14 · PMax HVAC 0.14. **Expected after fix ≈ 1.2/day**, PMax Elec ≈ 0.1 |
| Reported conversions | 1,376 / 30d, 88% are phone taps → expect ~50 / 30d after Block F |
| Spend | Pre-10-13: October pace ~$59.8k/mo · daily caps $1,960/d. **10-13 cut to $1,385/d ($1,285 once YouTube SA paused) → Oct ≈ $50k** (D-10) |
| LSA calls | Jun 88 · Jul 71 · Aug 33 · Sep 21 · Oct 1–6: 2 |
| PMax HVAC | ~100% Display since wk Aug 24, ~$2.3k/wk |

### Watch-outs

- GA4 Data API lags hours; today's events show up later today or tomorrow.
- GA4 sees ~73% of what Ads counts (Consent Mode defaults to denied). Compare shares, not raw counts.
- The headless tests sent nothing (every hit aborted), so there's no test data to exclude.
- **Auto mode:**
  - GTM publish was blocked as "blind apply" until the draft was tested.
  - Google Ads mutations may be blocked; write + validate scripts first, and stop if blocked.
- `update.py`: always pass `--customer-id`; `--budget` is in centavos; tCPA is plain micros. Always read back.
- Phone taps → Secondary (F2) is a UI change. Verify via API the next day: `primary_for_goal` via API has been a no-op.
- Don't touch listeners `[99]` / `[123]` (enhanced conversions depend on `[99]`).

### Files and scripts

- **Plans:** `internal-action-plan-2026-10-07.md` · `am-client-action-plan-2026-10-07.md` ·
  `action-plan-2026-10-07.md` (combined, superseded)
- **Log:** `google-ads-log.md` (2026-10-07 entries: weekly check, confirmed calls, job-application finding, Block A live)
- **Scripts** in `.claude/skills/google-ads-ratos/scripts/` (run with `./tsd.sh`, or `./gtm.sh` for GTM-only):

  | Script | What it does |
  |---|---|
  | `proud_pops_verify_careers_fix.py` | **Block E check, run this first** |
  | `proud_pops_gtm_headless_test.py` | Pre/post-publish GTM test, all hits aborted |
  | `proud_pops_weekly_check_1007.py` | Weekly / Sep / Oct campaign pull + Gate 0 status |
  | `proud_pops_30d_cpl_1007.py` | 30-day CPL, forms by click vs conversion date, network split |
  | `proud_pops_ga4_careers_split_1007.py` | GA4 lead split by page / campaign |
  | `proud_pops_calls_lsa_1007.py`, `proud_pops_lsa_monthly_1007.py` | Call asset status, call_view, LSA leads |
  | `proud_pops_pmax_network_1007.py` | PMax weekly network split + bid targets |
  | `proud_pops_gtm_dump_live_1007.py` | Dump the live GTM container |

- **Added 10-08:**
  - **Change scripts** (client folder; validate-only by default, `--apply` writes, all read back):
    - `block_b_changes_2026-10-07.py` (b3 / b4 / b4-revert / b4-cleanup / b5 / b7)
    - `block_b_b1_b2_2026-10-08.py` (b1 / b2 / b2b)
    - `h1_electrical_url_expansion_off_2026-10-08.py`, `h2_electrical_negatives_2026-10-08.py`
    - `h3_plumbing_changes_2026-10-08.py`, `h7_plumbing_general_adgroup_2026-10-08.py` (build / cutover)
    - `batch_h2b_h2c_d3_d9_2026-10-08.py`, `gtm_d1_d5_2026-10-08.py`
    - `h4_sitelinks_2026-10-08.py`, `h5_youtube_kids_exclusions_2026-10-08.py`, `g1_geo_2026-10-08.py`
    - `g2_rsa_drafts_2026-10-08.py`, `g2c_rsa_drafts_2026-10-08.py`, `g2b_cutover_2026-10-08.py`
    - `pmax_brand_exclusion_2026-10-08.py`, `hvac_negatives_2026-10-08.py`, `pause_roofing_lsa_2026-10-08.py`
  - **Read-only analysis** (skill scripts dir):
    - `proud_pops_b7_delivery_check.py`, `proud_pops_lsa_lead_handling.py`, `proud_pops_legacy_lsa_status.py`
    - `proud_pops_h2_electrical_terms.py`, `proud_pops_h3_plumbing_cpc.py`, `proud_pops_h4_pricing.py`
    - `proud_pops_h5_youtube_brand.py`, `proud_pops_h5_audience.py`, `proud_pops_g1_geo.py`, `proud_pops_g2_qs.py`
    - `proud_pops_hvac_terms.py`, `proud_pops_campaign_settings_check.py`, `proud_pops_gtm_test_v43.py`
  - **Proposal doc:** `proposals-h4-h5-g1-g2-2026-10-08.md`

---

## Key IDs

| Thing | ID |
|---|---|
| Google Ads account | 1051843378 (MCC 4155514468, `./tsd.sh`) |
| GTM | account 6255217830 · container 198527160 (GTM-WBFDB6L8) · Default Workspace **44** (was 43) · live **v42** (rollback = v41) (`./gtm.sh`) |
| GA4 | property 438523825 · G-C7QTE9ZZXQ |
| Search HVAC | 23848895678 (tCPA $265) |
| Search Electrical | 23866999121 |
| Search Plumbing | 23853484024 |
| Branded | 23853361615 |
| PMax HVAC | 23853595615 (asset group 6712908741, tCPA $27) |
| PMax Electrical | 23866982084 (asset group 6714775802) |
| Conversion actions | Website lead 6562304397 · TSD - Website Call 7667749854 · Calls from ads 6569241485 |
| Old call assets (210-794-7570, disapproved) | campaign-level 360709032917 (on all 6) · account-level 185848871539 |
| Negative lists | CSMS_Negatives 11330296375 (on 3 nonbranded Search) · CSMS_Competitors 11334178042 (attached to nothing) |
| Job form ID | ThmcYYHImwSoYS9oBt3n (on /careers) |
| LSA | in-account campaign 20067257249 · 7261668241 · 6621969129 |

Who: **[C]** = Claude via API/script · **[E]** = Edu in the UI or approval · **[C→E]** = Claude prepares and
validates, Edu approves the live run.

---

## Block A — GTM: take job applications out of lead tracking (Oct 7–8)

- [x] **A1 [C]** Re-check live version is still v41 and workspace 43 is in sync before editing.
      *Done when:* `versions().live()` = v41 and workspace 43 shows no pending changes.
      **Result 10-07:** live v41 (23 tags / 14 triggers / 19 vars), ws 43 only workspace, 0 pending changes, 0 conflicts.
- [x] **A2 [C]** Create variable `dlv - ghl_form_id` (Data Layer Variable, name `ghl_form_id`, version 2).
      **Result 10-07:** variable id **124**.
- [x] **A3 [C]** Edit trigger `[80] cEvent - Lead`: keep `{{_event}} equals ghl_form_submit`, add filters:
      - `{{Page Path}}` contains `/careers` with **negate = true**
      - `{{dlv - ghl_form_id}}` equals `ThmcYYHImwSoYS9oBt3n` with **negate = true**
      *Done when:* workspace read-back shows both filters on trigger 80.
      **Result 10-07:** read-back shows both filters (contains /careers negate=true; equals ThmcYYHImwSoYS9oBt3n negate=true).
- [x] **A4 [C]** Create trigger `cEvent - Job Application`: customEvent `ghl_form_submit`, filter `{{Page Path}}`
      contains `/careers`. **Result 10-07:** trigger id **125**.
- [x] **A5 [C]** Create tag `06 | GA4 - Job Application`: type `gaawe`, eventName `job_application`,
      measurementIdOverride `{{GA4 Measurement ID}}`, eventSettingsTable `page_location = {{Page URL}}`,
      firing on A4's trigger. **Result 10-07:** tag id **126**, cloned from [90], eventName job_application, fires on [125].
- [x] **A6 [C]** Confirm nothing else changed: workspace diff shows only A2–A5. Listeners `[99]` and `[123]` untouched.
      **Result 10-07:** status = exactly 4 changes (var 124 added, trigger 80 updated, trigger 125 added, tag 126 added),
      0 conflicts. quick_preview compilerError = none. [82]/[90]/[94]/[111] still fire on cEvent - Lead; [99] and [123]
      identical to live. Draft = 24 tags / 15 triggers / 20 vars. Live still v41.
- [x] **A7 [E]** Preview test (GTM UI → Preview → proudpops.com):
  - [x] On `/careers`, console: `dataLayer.push({event:'ghl_form_submit', ghl_form_id:'ThmcYYHImwSoYS9oBt3n'})` *(covered by the automated headless test)*
        → only `06 | GA4 - Job Application` fires. `[82]`, `[90]`, `[94]`, `[111]` do NOT fire.
  - [x] On `/careers`, console: `dataLayer.push({event:'ghl_form_submit', email:'tsd-test@example.com'})` *(covered by the automated headless test)*
        (no form ID, like listener `[99]`) → still no `05 |` lead tags. Proves the Page Path rule works alone.
  - [x] Click from the HVAC page through to `/schedule` (in-app, not a reload), console: *(covered by the automated headless test)*
        `dataLayer.push({event:'ghl_form_submit', email:'tsd-test@example.com'})` → `[82]`, `[90]`, `[94]`, `[111]` fire once.
        Job Application does not.
  - [x] Same from the homepage → `/schedule`. *(covered by the automated headless test)*
  - [x] Screenshot the Tag Assistant summary for the log. *(covered by the automated headless test)*
      **Result 10-07:** Edu didn't run Preview; replaced by an automated headless test
      (`scripts/proud_pops_gtm_headless_test.py`): real site, container swapped for draft env-6, all tracking hits
      intercepted + aborted (nothing reached Google/Meta). Control on live v41: /careers → Ads lead + GA4 lead.
      Draft: /careers (with and without form id) → GA4 job_application ONLY; /schedule via in-app nav from HVAC page
      and homepage → Ads Website lead + GA4 generate_lead. Re-run on live v42 after publish: identical.
- [x] **A8 [E]** Approve the publish. **Result:** Edu, 10-07 ("make it go live").
- [x] **A9 [C]** Create the version and publish: `TSD - Exclude careers job applications from lead conversions (2026-10-0X)`.
      *Done when:* `versions().live()` returns the new version number and it contains A2–A5.
      **Result 10-07:** live **v42** (24 tags / 15 triggers / 20 vars), trigger 80 filters + 124/125/126 present,
      public gtm.js serves job_application. Default Workspace is now **44**. (First publish attempt was blocked by
      the auto-mode classifier as "blind apply"; it passed after the pre-publish test.)
- [x] **A10 [C]** Record the publish date/time here (it's the "after" start for every verification below):
      **2026-10-07 12:32 BRT = 10:32 America/Chicago (GA4 tz).** Oct 7 is a split day; Oct 8 is the first clean full day.

## Block B — Google Ads: no-approval changes (Oct 8–9)

- [x] **B1 [C→E]** (was [E]; doable via API) PMax URL exclusions: Campaign → Settings → Final URL expansion → Exclude URLs →
      `proudpops.com/careers` on **23866982084** and **23853595615**.
      *Done when:* [C] confirms over the next 3 days that GA4 shows no PMax sessions landing on /careers.
      **10-08:** API route = negative WEBPAGE campaign criterion "URL contains /careers" on both PMax.
      `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_b1_b2_2026-10-08.py b1 --apply`.
      **APPLIED 2026-10-08 (Edu OK). Read-back:** negative WEBPAGE criterion "Exclude careers (job applications)",
      URL CONTAINS /careers, ENABLED on 23866982084~2501539306220 and 23853595615~2501539306220.
      Still open: the 3-day GA4 check that no PMax sessions land on /careers (runs in `proud_pops_verify_careers_fix.py`).
- [x] **B2 [C→E]** (was [E]; doable via API) Account-level negative keywords (Admin → Account settings → Negative keywords). These cover PMax,
      which shared lists can't: `jobs`, `job`, `careers`, `career`, `hiring`, `apprentice`, `apprenticeship`,
      `salary`, `employment`, `indeed`, `resume`.
      Don't add `hire`: it's customer intent ("hire an electrician").
      **10-08 REFINED after a collision check (5,920 search terms, 124 live keywords):** bare `job`/`jobs`/`hiring` BROAD
      would block customer searches ("electrician near me for small jobs", "hiring electrician near me"). Final list:
      - BROAD: careers, career, apprentice, apprenticeship, salary, employment, indeed, resume
      - PHRASE: now hiring, who's hiring, hiring now, near me hiring, job openings, jobs near me, electrician jobs,
        electrical jobs, plumbing jobs, plumber jobs, hvac jobs, hvac technician job, hvac technician jobs, hvac tech jobs

      Blocks only 5 job-seeker terms in 90 days; 0 collisions. New ACCOUNT_LEVEL_NEGATIVE_KEYWORDS list
      "TSD - Account negatives (job seekers)" attached to the account.
      `... block_b_b1_b2_2026-10-08.py b2 --apply`. **APPLIED 2026-10-08 (Edu OK).** Read-back: shared set **12263521315**
      "TSD - Account negatives (job seekers)" (ACCOUNT_LEVEL_NEGATIVE_KEYWORDS) with all 22 terms, attached as
      customerNegativeCriteria/2502916073266. (member_count showed 0 right after create; the direct member query shows 22.)
  - [x] **B2b [C→E]** Follow-up found 10-08: **CSMS_Negatives** (on the 3 non-branded Search campaigns) has `job` and `jobs`
        as BROAD. That already blocks customer searches like "electrician near me for small jobs" on Search. Swap them
        for the job-seeker PHRASE terms above.
        **APPLIED 2026-10-08 (Edu OK)** (`... block_b_b1_b2_2026-10-08.py b2b --apply`):
        - Removed BROAD `job` (10005011) and `jobs` (10005021) from CSMS_Negatives (now 756 members).
        - Added PHRASE electrician job / plumber job / hvac job / hvac tech job to the account list (now 26).
        Validation: unblocks only 2 customer terms ("…near me for small jobs"), 0 collisions.
        Side note → D-9: CSMS_Negatives still has EXACT "electricians for hire", which is probably customer intent.
- [x] **B3 [C→E]** Competitors on Plumbing:
  - [x] [C] Pull CSMS_Competitors' 23 names and flag any that could be generic queries
        (e.g. "southside plumbing", "mission plumbing").
        **Result 10-07** (`proud_pops_b3_competitor_review.py`): all 23 are **EXACT** match, so they only block that exact
        query ("southside plumbing" etc. are safe). 0 collisions with our 24 Plumbing keywords. On 90-day search terms the
        existing list blocks nothing; the 2 additions block 3 terms ($87.41, 2.0 all_conv, likely phone taps).
  - [x] [E] Approve the list. **Approved by Edu 2026-10-08.**
  - [x] [C] Add `beyer` and `bryco` to CSMS_Competitors (george and the bearded plumber are already in
        CSMS_Negatives), then attach CSMS_Competitors to Plumbing 23853484024.
        *Done when:* `campaign_shared_set` read-back shows it attached.
        Script: `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b3 --apply`. **Validate-only passed 10-07 (3 ops).**
        **APPLIED 2026-10-08. Read-back:** `beyer` PHRASE + `bryco` PHRASE in CSMS_Competitors (sharedCriteria ~116352309,
        ~525859783); CSMS_Competitors attached to Plumbing 23853484024 (campaignSharedSets/23853484024~11334178042, ENABLED).
- [ ] **B4 [C→E]** New call extension: **↩ REVERTED 2026-10-08 (Edu). Waiting: Edu confirms which number is correct.**
      Where the number came from:
      1. 2026-09-03 live fetch of proudpops.com: 210-225-5767 ("210-CALL-POP" vanity) in the header, CTA and meta description.
      2. The old GTM `02 | G.Ads - Phone Call` tag had phoneConversionNumber 210-225-5767 (Jul 23 diagnosis).
      3. 10-08 checks: the only tel: on every page, for a direct visit, a simulated Google Ads click (gclid +
         utm google/cpc), and after "Accept All" cookies.
      **CallRail finding 10-08:** swap.js (company 686172931) loads but has `session_exact_targets: []` and
      `session_number_target_exists: false`. CallRail swaps NO number on proudpops.com, so it isn't tracking website calls
      by number swap. Origin of the old **210-794-7570** is unknown (not on the site, not in the swap config). It may be a
      CallRail tracking number made for the call extension, which Google couldn't verify → disapproved. If so, using
      225-5767 bypasses CallRail for ad calls (Google forwarding numbers + Calls from ads still count them in Google Ads).
      → Ask in P-5: who owns 794-7570 and 225-5767 in CallRail; is 225-5767 a CallRail number or the main line?
      *10-08 follow-up:* neither 225-5767 nor 794-7570 appears anywhere in CallRail's swap.js (44k chars).
      **Unknown whether 225-5767 is a CallRail number.** Only the CallRail account (Numbers) or the client can confirm.
      *10-08 clue:* the mailed-letter page /first-repair shows a DIFFERENT number, **(210) 864-6867**. That suggests channel-
      specific tracking numbers are in use, which would make 225-5767 the main line. Still unconfirmed.
      **Revert ready:** `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b4-revert --apply`
      (validate-only passed 10-08, 7 ops; removes the new links, leaves the old ones). `b4-cleanup` NOT to run while on hold.
      **REVERTED 2026-10-08. Read-back:** all 7 links to asset 428601259336 (account + 6 campaigns) = REMOVED. The account is back to
      its pre-B4 state: only the old disapproved 210-794-7570 links (NOT_ELIGIBLE). The unlinked asset 428601259336 still sits in
      the asset library (harmless; reusable if 225-5767 turns out to be right).
      **To redo with the right number:** change `NEW_NUMBER` in `block_b_changes_2026-10-07.py` → `b4` (validate) → `b4 --apply`,
      then update `NEW_ASSET` for b4-revert/b4-cleanup. If the correct number is 225-5767, re-link the existing asset 428601259336.
  - [x] [C] Script: create a call asset for `210-225-5767` (US), conversion action = Calls from ads
        6569241485, link at account level + on the 6 lead campaigns. Validate-only run first.
        **Done 10-07:** `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b4` → validate-only passed (8 ops: asset + account link + 6 campaign links).
  - [ ] [E] Approve the live run, **with the confirmed number**. History: 10-08 applied with 210-225-5767, then reverted
        the same day at Edu's request (`b4-revert --apply`).
        Was: Read-back: new asset **428601259336** (210) 225-5767
        REVIEW_IN_PROGRESS, linked at account level + on all 6 lead campaigns (PENDING). Old 210-794-7570 links still
        attached (NOT_ELIGIBLE), to be removed by `b4-cleanup` once the new one is approved.
  - [ ] [C] Next day: check its policy status is approved (not `UNVERIFIED_PHONE_NUMBER`).
        If Google asks for verification → move to the AM/client plan.
  - [ ] [C→E] Once approved: remove the old links (campaign assets `~360709032917~CALL` on the 6 campaigns and
        account asset `185848871539~CALL`). Script: `... b4-cleanup` (refuses unless the new asset is approved).
- [x] **B5 [C→E]** `Calls from ads` 6569241485: minimum call duration **15s → 60s**.
      *Done when:* `phone_call_duration_seconds` = 60 on read-back.
      Script: `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b5 --apply`.
      **APPLIED 2026-10-08 (Edu approved). Read-back:** Calls from ads `phone_call_duration_seconds` = **60**.
- [x] **B6 [C]** Landing pages, check first: open `/services/electrical`, `/services/plumbing`,
      `/services/plumbing/water-heaters` on mobile and desktop. Confirm each has a CTA that goes to `/schedule`,
      the phone number is visible, and nothing loads broken. Note anything off.
      **Result 10-07** (`proud_pops_b6_page_check.py`, tracking aborted): all 3 pages render on desktop + mobile, correct H1,
      no 404, no JS errors, "Schedule Your Free Pop-In Visit" → /schedule above the fold (2–3 links), tel:210-225-5767 visible.
      **Finding:** the HOMEPAGE on mobile has **no visible /schedule link** (above the fold = First Repair banner + big logo).
      That's where Electrical/Plumbing/Branded ads land today → supports B7; Branded raised as D-7.
- [x] **B7 [C→E]** Swap final URLs, then read back. Script: `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b7 --apply`.
      **APPLIED 2026-10-08 (Edu approved). Read-back:** all 6 ads show the new final URLs. All 6 are
      `PENDING / AD_GROUP_AD_UNDER_REVIEW` (review_status REVIEW_IN_PROGRESS). These are the ONLY enabled ads in Electrical
      and Plumbing Search, so both campaigns may not serve until approved.
  - [ ] **B7a [C]** Recheck approval a few hours after 2026-10-08 apply, and again next morning. Expect APPROVED.
        *10-08 first recheck (shortly after apply): all 6 still PENDING / under review. Next check: later today.*
        *10-08 11:38 CT recheck: still under review. The edits landed 11:32:56 CT (change_event, account tz America/Chicago).*
        *10-08 11:48 CT: still REVIEW_IN_PROGRESS on all 6. Plumbing primary_status = PENDING (MOST_ADS_UNDER_REVIEW +
        BUDGET_CONSTRAINED). Script: `./tsd.sh proud_pops_b7_delivery_check.py`. If still under review tomorrow morning → escalate.*
        If any is DISAPPROVED or still under review after ~1 business day → flag to Edu immediately (campaign not serving).
  - [ ] **B7b [C]** Check Electrical 23866999121 + Plumbing 23853484024 impressions for 10-08/10-09 vs their normal daily
        level, to confirm delivery resumed after review.
        *10-08 11:38 CT, hourly impressions:*
        - *Electrical: normal before the edit (07–11h CT: 16/36/24/23/12 vs 11/40/36/4 yesterday).*
        - *Plumbing: **very light since midnight, BEFORE any of today's changes** (8 impressions through 11h vs 68 by the same
          hour on 10-07; $103 spent). Not caused by B3/B7. Watch the afternoon; if it stays near zero, check the bid
          strategy status and budget pacing.*
        *Diagnosis 10-08 11:48 CT: Plumbing was throttled by budget pacing BEFORE the edit. It's over its $160/day budget this
        month ($1,253 in Oct 1–7) and today spent **$103 on 1 click** in the early hours (Max Conversions, no CPC cap), so
        Google held delivery (8 impressions). Lesson logged: editing the only ad in each ad group sent all 6 to review at
        once. Next time, create new ads and pause the old ones after approval.*

      | Ad group | Ad | New final URL |
      |---|---|---|
      | AG1_Electrician_NearMe 199431304209 | 809528123698 | proudpops.com/services/electrical |
      | AG2_Electrical_Services 196768586637 | 809490621054 | proudpops.com/services/electrical |
      | AG3_Electrical_Repair 195955611119 | 809490671193 | proudpops.com/services/electrical |
      | AG1_Plumbing_LeakDetection 196726297659 | 808814916930 | proudpops.com/services/plumbing (holds the generic "plumber san antonio" terms, so not the leak page) |
      | AG2_Plumbing_Emergency 196726811459 | 808929407402 | proudpops.com/services/plumbing |
      | AG3_Plumbing_WaterHeaters 196184241789 | 808929711767 | proudpops.com/services/plumbing/water-heaters |

      Branded stays on the homepage.
      *Done when:* `read.py` shows the new URLs and the ads are approved.

## Block C — GA4 (Oct 8, after A9 is live)

- [ ] **C1 [E]** Admin → Events → mark `generate_lead` as a key event. (Our API token is read-only.)
      *Could become [C]:* re-run the GA4 OAuth with the `analytics.edit` scope (Edu clicks through consent once), then
      Claude can set key events via the Admin API.
- [ ] **C2 [E]** Unmark these 11 key events: `ads_conversion_Form_1`, `purchase`, `book_now_link_click`,
      `phone_link_click`, `mailto_link_click`, `Shop`, `ghl_contact_us`, `Schedule Online`,
      `instant_roof_quote_click`, `instant_quote_hvac_click`, `button_schedule_online`.
      Their Google Ads imports are already secondary, so this doesn't change bidding.
- [ ] **C3 [C]** Read back: key events list = `generate_lead` only. `job_application` is a normal event.

## Block D — LSA check (Oct 8–9)

- [x] **D1 [C]** Pull fresh weekly impressions/leads for all 3 surfaces as the "before" snapshot.
      **Result 10-07** (`proud_pops_spend_and_lsa_d1.py`), weekly impressions / leads:
      - in-account: 503/10 (wk Aug 10) → 110/0 → none wk Aug 24 → 53, 95, 147/4, 134/0 → **none since wk Sep 28**.
      - 7261668241 Electrician: 239–370/wk through Sep 7 → 235, 232, 171, 90 (wk Oct 5, partial) → slow decline, still serving.
      - 6621969129 HVAC: 629–689/wk through Aug 31 → 416, 351 → **zero impressions since wk Sep 21** (fully dark ~3 weeks).
- [ ] **D2 [E]** In the Google Ads UI, for each of 20067257249 (in-account), 7261668241, 6621969129, record:
  - [ ] Profile status (active / paused / limited)
  - [ ] Weekly budget and bidding mode
  - [ ] Job types switched on
  - [ ] Service area
  - [ ] Business hours / ad schedule
  - [ ] Verification: license, insurance, background check, and any expiry warnings
  - [ ] Reviews (count, rating) and responsiveness / missed-call warnings
  - [ ] Any policy or suspension notices
- [ ] **D3 [C]** Turn findings into (a) fixes we can make now and (b) specific asks for the AM plan.
      **10-08 partial (lead handling, before D2):** `./tsd.sh proud_pops_lsa_lead_handling.py`.
      Monthly, all 3 surfaces:
      - Jun: 109 leads (61 declined, 7 credited)
      - Jul: 92 (45 declined, 4 credited)
      - Aug: 51 (10 declined, 1 credited)
      - Sep: 22 (7 declined, 9 still "active", 0 credited)
      - Oct 1–7: 3
      Sept calls: 0 at 0s, 2 under 30s, 4 at 30–60s, 15 over 60s → answering is fine. Messages: 2 of 2 recent got no business reply.
      Specific asks moved into P-6. Still needs D2 (profile settings) to explain the impression collapse.

## Block E — Verify the GTM fix (Oct 9–12, daily)

- [x] **E1 [C]** Day 1 after A10: GA4 `generate_lead` by pagePath since publish → `/careers` = 0;
      `job_application` > 0 (if anyone applied).
      **Result 10-08** (`proud_pops_verify_careers_fix.py`): **PASS.** After publish, GA4 has 5 `job_application` on
      /careers (Oct 7 11:00/12:00/13:00/19:00 CT, Oct 8 02:00) and **0 `generate_lead` on /careers**. Customer leads still
      fire: 2 `generate_lead` on /schedule (Oct 7 20:00, Oct 8 06:00 CT). 1 PMax Electrical google/cpc session still
      landed on /careers Oct 7 (expected until B1). Google Ads `Website lead` per click day still filling in (Oct 8:
      1.0 so far, Plumbing).
- [ ] **E2 [C]** Day 2: same, plus Google Ads `Website lead` daily all_conversions per campaign vs the prior 14-day
      average. Baseline (Sep 23–Oct 6) = **5.00/day** (PMax Elec 3.21). Expect ≈ **1.2/day**, PMax Electrical ≈ 0.1.
      Script: `./tsd.sh proud_pops_verify_careers_fix.py` covers E1–E3 in one run.
- [ ] **E3 [C]** Day 3: same. If `/careers` leads still appear → find which page/route they fire from and extend
      the exclusion before anything in Block F.
- [ ] **E4 [C]** Confirm the AM heads-up to the client has been sent (AM plan, item 1). **Block F waits on this.**

## Block F — Bidding signal (Oct 12–13, only when E1–E4 are all ticked)

- [ ] **F1 [C]** "Before" snapshot: per-campaign conversions vs all_conversions by action, last 14 days.
- [ ] **F2 [E]** Goals → phone call lead goal → set `TSD - Website Call` (7667749854) to **Secondary**.
      Do NOT switch off the whole PHONE_CALL_LEAD / CALL_FROM_ADS goal: Calls from ads shares it.
- [ ] **F3 [C→E]** Same day: remove the $265 target CPA on Search HVAC 23848895678
      (`maximize_conversions.target_cpa_micros = 0`, plain micros, explicit field mask). Read back.
- [ ] **F4 [C]** Next day: verify `TSD - Website Call` shows all_conversions > 0 and conversions = 0.
      If conversions still count → fallback: set PHONE_CALL_LEAD/CALL_FROM_ADS `biddable = false` per campaign
      (explicit FieldMask on `biddable`), then re-verify.
- [ ] **F5 [C]** Days 2–7: watch daily spend and impressions per campaign for a delivery collapse.
      Any campaign below 50% of its prior daily spend for 3 days → flag to Edu.

## Block G — Ongoing (Oct 13–30)

- [x] **G1 [C→E]** Geo: pull current location targets for HVAC 23848895678 and Plumbing 23853484024 and the LSA
      service-area cities → propose the added cities → Edu approves → apply → read back. Budgets unchanged.
      **ANALYSIS DONE 2026-10-08** (`proposals-h4-h5-g1-g2-2026-10-08.md`): Branded / HVAC / Plumbing / PMax HVAC target San Antonio city only; Electrical has 5
      cities; LSA (client-declared) 47–50 cities. HVAC Search + PMax Electrical use "presence or interest".
  - [x] **G1a [C→E]** Branded → the full 47-city in-account LSA service area.
  - [x] **G1b [C→E]** HVAC + Plumbing Search → 20-city core metro (list in the proposal; all from the client's LSA list).
  - [x] **G1c [C→E]** Search HVAC + PMax Electrical location option → PRESENCE.
        **G1a/b/c DONE 2026-10-08** (`g1_geo_2026-10-08.py`; geo constants copied from the LSA campaigns' own criteria). Read-back:
        Branded 47 location targets, Search HVAC 20, Search Plumbing 20. PRESENCE on HVAC, Plumbing, Branded, PMax Electrical.
        Budgets unchanged.
  - [ ] **G1d [C]** ~Oct 15: clicks / cost by city for Branded, HVAC and Plumbing since 10-08; make sure the new cities aren't
        eating budget at bad CPCs.
- [x] **G2 [C→E]** Ad Rank: pull Quality Score components per keyword on the 3 non-branded Search campaigns →
      draft RSA rewrites for the ad groups with Below Average expected CTR → Edu approves → apply.
      **DRAFTS DONE 2026-10-08** (`proposals-h4-h5-g1-g2-2026-10-08.md`; `g2_rsa_drafts_2026-10-08.py`): 5 RSAs for the top-spend below-average ad groups (Elec
      AG1 / AG2 / AG3, HVAC AG1 / AG3). Every claim verified on the site. **Google validate-only: all 5 accepted.** Current ads carry
      unverified claims ("5-Star" but it's 4.8; "Same-Day" on Electrical / Plumbing; "Upfront"; "Trusted"; "Affordable"; "We
      Answer Every Call").
  - [x] **G2a [C→E]** Create the 5 new RSAs (after Edu OKs the copy): `... g2_rsa_drafts_2026-10-08.py build --apply`. **DONE 2026-10-08:** new ads Elec AG1 827482059110, AG2 827482059113, AG3 827482059116, HVAC AG3 827482059119, HVAC AG1 827482059242 (all REVIEW_IN_PROGRESS, next to the old ads).
  - [ ] **G2b [C]** Once each is approved, pause the old ad in that ad group. **Set up 2026-10-08:** `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/g2b_cutover_2026-10-08.py --apply` covers all 14 new ads (G2a + G2c) and only pauses old ads whose replacement is APPROVED. Safe to re-run. **Run at each check until all 14 are done.**
  - [x] **G2c [C→E]** Second batch: Plumbing AG1 / AG2 / AG3, HVAC AG2, Branded (same unverified claims).
        **DONE 2026-10-08** (Edu wrote "H2c execute"; H2c was already done, so read as G2c). `g2c_rsa_drafts_2026-10-08.py`:
        9 site-verified RSAs, validated, then created:
        - Branded (homepage, per D-7): Brand_Electrical 827358146385, Brand_OldName 827358146388, Brand_Plumbing 827358146391,
          Brand_HVAC 827358146394, Brand ProudPops 827358146397
        - HVAC AG2 Installation 827358146520
        - Plumbing AG1 827358146523 (→ /services/plumbing/leak-detection, since the generic plumber terms are moving to AG4)
        - Plumbing AG2 Emergency 827358146526
        - Plumbing AG3 Water Heaters 827358146529
        All REVIEW_IN_PROGRESS. IDs saved in `.g2c_new_ads.txt` for the G2b switchover.
- [ ] **G3 [C]** Oct 26 re-baseline (window = A10 → Oct 25), per campaign:
  - spend
  - customer forms (`Website lead`, cross-checked against GA4 with /careers excluded)
  - Calls from ads (60s+)
  - LSA calls
  - CallRail calls, if connected
  Write it up in the log.
- [ ] **G4 [C]** PMax Electrical review on Oct 26: fewer than 5 customer forms since A10 → recommend pausing it
      (that goes through the AM, not here).
- [x] **G5 [C→E]** Later, separate GTM version: fix `[111] 05 | Meta - Lead` from PageView to Lead. Preview, publish.
      **DONE 10-08 in GTM v43** (with D-1).
  - [ ] **G5a [C]** Oct 9: Meta pixel 597145242772352 stats (Meta MCP `ads_get_dataset_stats`, event_name Lead) → expect "Lead"
        events after 10-08 12:26 CT that roughly match GA4 `generate_lead` (customer forms only).
- [ ] **G6 [C→E]** Later: merge the two GHL listeners (keep `[123]`, remap `dlv` variables to `ghl_data.*`,
      remove `[99]`). Retest enhanced conversions in Preview.

## Block H — Campaign backlog (from the 2026-10-08 campaign review)

Found 10-08 with `proud_pops_campaign_settings_check.py` + expanded landing page view (Sep 8 – Oct 7).
Search Partners + Display are OFF on all 4 Search campaigns (correct).

- [x] **H1 [C→E]** **Search Electrical 23866999121: AI Max is ON, with final URL expansion OPTED_IN** (enabled by the client,
      Brandon, Jun 26). Only **44%** of its spend ($7,841 / 30d) lands on the ad's URL. Elsewhere:
      - /pricing $4,685 (26%)
      - generator blog post $879 (5%)
      - /services/electrical $1,718
      - HVAC, plumbing and city pages ~$1.9k, incl. /san-antonio-tx/emergency-plumber
      It can also override the B7 /services/electrical URL. Recommendation: turn off final URL expansion (or AI Max
      entirely) via API. It was the client's setting, so tell the AM. Open since July.
      **APPLIED 2026-10-08 (Edu OK)** (`h1_electrical_url_expansion_off_2026-10-08.py`, validate then apply). Read-back:
      FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION = **OPTED_OUT**. Unchanged on purpose: AI Max (still ON, so broader search-term
      matching remains) and TEXT_ASSET_AUTOMATION (OPTED_IN). Client told via P-13.
  - [ ] **H1a [C]** ~Oct 13: re-run the expanded-landing-page split for Electrical (Oct 9 onward). Expect clicks only on
        /services/electrical (+ sitelink URLs like /pricing). Anything else → check for other URL sources.
- [x] **H2 [C]** Search term sweep on Search Electrical (largest spender, ~$18.5k / 30d, ~$1,010 per customer form): last 30
      days → negatives proposal (off-service, competitor, junk). AI Max likely broadens matching.
      **APPLIED 2026-10-08 (Edu: "execute on H2")** (`h2_electrical_negatives_2026-10-08.py`; 2,217 terms, Sep 8–Oct 7).
      **36 campaign-level negatives** on 23866999121, read-back 36/36:
      - 25 competitor PHRASE: q electric, mission city electric, wattsmith, snyder electric, elevate electrical, genesis
        electric/electrician, d & g electrical, hays electrical, advanced electrical contractors, finlee, turney electric,
        m & r electrical, chain electric, cfa electric, bates electric, sa classic electric, goettl, wrangler, service experts,
        jaydylan, willfixit, american home shield, goodman, trane
      - 11 off-service: BROAD plumbers / plumer / climas; PHRASE a c repair, ac service, ac technician, boerne ac,
        leak detection, appliance installer, customer service, pops ac
      Checks: 0 collisions with own keywords; 0 core customer-intent terms blocked. Terms they'd have blocked:
      **~$2,374 / 30d** (unique).
      Match source (visible terms, 30d):
      - keywords $5,981 → $130 per all_conv
      - AI Max broad $1,858 → $128
      - **AI Max keywordless $2,728 → $260 per all_conv**
  - [x] **H2b [C→E]** Own-brand leak: "pops electric" ($145) and "pops electrical" ($17) hit Electrical non-branded, but Branded
        only has "proud pops …" keywords. Add EXACT "pops electric" / "pops electrical" to Branded (Brand_Electrical
        ad group), THEN negate them on Electrical. Note Branded is already 25% budget-limited.
        **APPLIED 2026-10-08 (Edu OK):** EXACT "pops electric" + "pops electrical" ENABLED in Brand_Electrical; EXACT negatives
        for both on Electrical. Read back. (`batch_h2b_h2c_d3_d9_2026-10-08.py`)
  - [x] **H2c [C→E]** Decision: turn off AI Max search-term matching on Electrical? Keywordless matching = $2,728 / 30d at about
        2× the cost per (polluted) conversion of keyword traffic, and brought most of the junk above. Option: switch AI Max off
        entirely (URL expansion is already off; text customization would go with it), or wait until after Block F, when
        bidding optimizes to real forms.
        **APPLIED 2026-10-08 (Edu: "turn off AI Max").** Google rejects AI Max off while text customization is on
        (AI_MAX_MUST_BE_ENABLED), so the same op set TEXT_ASSET_AUTOMATION → OPTED_OUT. Read-back: enable_ai_max = False;
        TEXT + FINAL_URL_EXPANSION both OPTED_OUT. Electrical now serves only on its own keywords.
- [x] **H3 [C]** Plumbing cost control (item 3): spent $103 on 1 click on 10-08 (Max Conversions, no CPC cap; budget-throttled).
      Pull the CPC distribution + the terms behind $60+ clicks → recommend (e.g. Max Clicks with a CPC cap). Bidding change →
      Edu decides; coordinate with Block F.
      **DONE 2026-10-08** (`./tsd.sh proud_pops_h3_plumbing_cpc.py`):
      - Max Conversions, no target, no CPC cap; budget $160/d, regularly spends $180–310/d.
      - 30d: $5,115 / 135 clicks / avg CPC $37.89.
      - **Exact single-click prices** (183 one-click term-days, 60d): median $12.77. 65% of clicks are under $20 (22% of spend);
        **clicks over $40 = 18.5% of clicks but 53.5% of spend; over $60 = 6.5% of clicks, 26% of spend.**
      - Priciest: $120.52 / $103.16 (today 06:00 CT) / $101.64 / $93.61, almost all "plumbers san antonio" /
        "san antonio plumbing" matched by EXACT "plumber san antonio" (QS 5, expected CTR below average).
      - Today's $103.16 = 1 click at 06h CT on "plumbers san antonio" (recorded 1.0 all_conv, likely a phone tap).
      - Keywords (30d):
        - "plumber san antonio tx" PHRASE: $2,255, 44% of spend, QS 6 (up from 3 in July)
        - "leak detection near me" PHRASE: **$755, $50.31 CPC, 0.7 all_conv, QS 4** (worst in the account)
        - "emergency plumbing san antonio": $117.92 CPC (2 clicks)
  - [x] **H3a [C→E]** Pause keyword "leak detection near me" PHRASE (AG1_Plumbing_LeakDetection). Keep EXACT "leak detection
        san antonio" (QS 5, 9.0 all_conv). Budget-neutral.
        **APPLIED 2026-10-08 (Edu OK).** Read-back: adGroupCriteria/196726297659~297313395770 = PAUSED.
  - [x] **H3b [C→E]** CPC ceiling decision. Max Conversions can't cap CPC. Options:
        (a) Maximize Clicks with a ~$45 ceiling, same day as Block F (Plumbing will have only ~6 customer forms/30d, too thin
            for Max Conversions once phone taps stop counting);
        (b) portfolio Maximize Conversions with a CPC ceiling;
        (c) leave it.
        A $45 cap covers ~85% of today's clicks and removes the $60–120 outliers.
        **APPLIED 2026-10-08 (Edu chose now, not with Block F).** Option (a): bidding MAXIMIZE_CONVERSIONS → **TARGET_SPEND
        (Maximize Clicks), cpc_bid_ceiling $45.00**. Read-back: TARGET_SPEND, ceiling $45.0, ENABLED. Budget unchanged ($160/d).
        Block F's phone-tap change no longer affects Plumbing bidding (it doesn't bid on conversions now).
  - [x] **H3c [C]** Add competitor "aramendia" (PHRASE) to CSMS_Competitors ($81.90 single click Sep 20).
        **APPLIED 2026-10-08.** Read-back: PHRASE "aramendia" in CSMS_Competitors.
  - [ ] **H3d [C]** Watch Plumbing for 7 days after its ads clear review (B7a). Track daily spend, clicks, avg CPC (expect
        < $45, roughly $20–30), impressions/IS, and new search terms. Maximize Clicks can drift to cheap low-intent clicks →
        sweep terms ~Oct 15. Script: `./tsd.sh proud_pops_h3_plumbing_cpc.py`.
- [x] **H4 [C]** `/pricing` gets 20–26% of Search clicks in every campaign (~$8.1k / 30d), probably via a "Pricing"
      sitelink. Check the sitelink, whether /pricing has a schedule CTA, and how it converts (customer forms, via GA4). Then
      keep, repoint or drop.
      **DONE 2026-10-08** (`proposals-h4-h5-g1-g2-2026-10-08.md`): it's a "See Our Pricing" sitelink; sitelink clicks = $10,772 / 30d. /pricing converts 3.2% to
      customer leads vs 4.3% homepage, so keep it. Found: account sitelink "Contact Us" → old domain, and the redirect DROPS the
      click ID and lands on the homepage (105 clicks / 30d unattributable); 3 dead old-domain sitelinks still ENABLED; no sitelink
      to /schedule.
  - [x] **H4a [C→E]** Repoint "Contact Us" → proudpops.com/contact, or replace it with "Book a Free Pop-In" → /schedule. **DONE 2026-10-08 (Edu: execute)**: new account sitelink "Contact Us" → https://proudpops.com/contact (descriptions "Check we serve your area" / "A real person picks up"); old txproblemsolvers.com link removed. /contact verified as a real page. (`h4_sitelinks_2026-10-08.py`)
  - [x] **H4b [C→E]** Remove the 3 dead old-domain sitelinks (Air Conditioning Services, Bathroom Plumbing, Heat Pumps). **DONE 2026-10-08 (Edu: execute)**: account links removed; read-back shows no old-domain sitelinks left.
  - [x] **H4c [C→E]** Add a "Book a Free Pop-In" → /schedule sitelink on all 4 Search campaigns. **DONE 2026-10-08 (Edu: execute)**: asset 428522074259 ("Free visit, no obligation" / "Written price before any work") linked to Electrical, HVAC, Plumbing, Branded; status PENDING review.
- [x] **H5 [C]** YouTube ($6k/mo, ~10% of spend, awareness): branded search impressions/clicks trend since the Aug 8 launch,
      as a brand-lift read before the November budget decision.
      **DONE 2026-10-08** (`proposals-h4-h5-g1-g2-2026-10-08.md`): $12,298 since Aug 8. **SA "VideoViews" runs largely on kids' content** (Disney Jr., Bluey,
      Ms Rachel, Super Simple Songs, El Payaso Plim Plim; $0.011 per view). NB "Awareness" is 76% smart-TV apps. Brand lift is
      unmeasurable: Branded was paused late May → Aug 9; GA4 Direct had bot traffic before Aug then dropped ~80% late Aug (cookie
      banner); and **Branded doesn't target New Braunfels**.
  - [x] **H5a [C→E]** SA YouTube: exclude kids / made-for-kids content + those channels.
        **DONE 2026-10-08, at ACCOUNT level:** campaign-level criteria on these YouTube campaigns are read-only via the API
        (MUTATE_NOT_ALLOWED), and the families label is invalid at campaign level. Added account-level exclusions
        (`h5_youtube_kids_exclusions_2026-10-08.py`):
        - content label BRAND_SUITABILITY_CONTENT_FOR_FAMILIES (id 89504691659)
        - 34 kids YouTube channels with ≥ $5 spend ($797 since Aug 8): Disney Jr., Plim Plim, Bluey, Ms Rachel, Super Simple
          Songs, Sesame Street, Cocomelon, Peppa, Nick Jr. …
        Read-back: label present, 34/34 channels. These also apply to PMax's YouTube inventory.
        "Right people" check (Edu: "make sure we're showing to the right people"):
        - 84% of both campaigns' spend is on connected TV
        - ages 18–24 were already excluded
        - age-unknown (SA 44%, NB 25%) deliberately NOT excluded: on shared household TVs that's the homeowner household, and
          excluding it would cut most of the inventory
  - [x] **H5b [C→E]** ~~After G1a: 4-week geo test (pause NB YouTube, compare branded searches by city) or a Google Brand Lift study.~~ **Closed 2026-10-08 (Edu): turning YouTube off isn't an option. Done instead: H5a exclusions + the right-people check; Branded now covers New Braunfels (G1a).**
- [x] **H6 [C→E]** Branded (D-7): **closed 10-08, keep homepage (see D-7).** the homepage on mobile has no schedule CTA above the fold. Option: NEW branded ads (not edits,
      see the lesson) pointing at a page with a CTA, or ask the client's web team for a homepage hero CTA (→ AM).
- [x] **H7 [C→E]** Plumbing generic terms: July's "Change 1" (AG4_Plumbing_General, `change1_plumber_general_adgroup.sh`) was
      **never built** (no such ad group). Fold it into G2.
      **BUILT 2026-10-08 (Edu: "Execute H7 now")** (`h7_plumbing_general_adgroup_2026-10-08.py build --apply`, validated first).
      Read-back:
      - ad group **AG4_Plumbing_General 199626362094** ENABLED
      - keywords EXACT "plumber san antonio", EXACT "plumber near me", PHRASE "plumber san antonio tx" (ENABLED)
      - RSA **827480907116** → /services/plumbing, paths Plumber/San-Antonio, REVIEW_IN_PROGRESS
      Copy: 15 headlines / 4 descriptions, **every claim verified on the live site 10-08** (Free Pop-In, written price before
      work, no surprises / pressure, photos, licensed & insured, 24/7 emergency response, "Still Family. Still Local.", fix
      first, financing, leaks / drains / water heaters, SA + New Braunfels). July's "same-day", "5-star", "upfront" and
      "trusted" were dropped (not on the site / empty adjective).
      No downtime: the AG1 originals stay ENABLED until the new RSA is approved.
  - [ ] **H7a [C]** **Cutover** once RSA 827480907116 is APPROVED:
        `./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/h7_plumbing_general_adgroup_2026-10-08.py cutover --apply`
        Pauses the 3 generic keywords in AG1_Plumbing_LeakDetection; refuses if the RSA isn't approved. Check with B7a tomorrow.
  - [ ] **H7b [C]** ~2 weeks after cutover: QS + expected CTR on the 3 keywords in AG4 (they were QS 4–6, expected CTR below
        average in AG1) and their avg CPC vs the $45 cap.
- [x] **H9 [C→E]** HVAC search-term sweep (Edu: "execute on 1", 2026-10-08). `scripts/proud_pops_hvac_terms.py` →
      `hvac_negatives_2026-10-08.py`.
      - HVAC uses exact / phrase only (no AI Max): 78 terms, $5.3k visible, almost all relevant.
      - **Applied 9 campaign negatives** (read-back 9/9): PHRASE airco, cowboys ac, beluga air, sa specialties, atlas ac,
        ems home services, one hour air, statewide ac; BROAD rv. Would have blocked $422.78 / 30d, 0 conversions.
      - NOT blocked on purpose:
        - commercial HVAC ($372; the site says "Residential & Commercial")
        - "cheapest ac repair"
        - equipment brands (Ruud, Pioneer)
        - "alamo air conditioning" (2 conversions)
        - "sa specialist" (ambiguous)
      - The real HVAC problem is CPC / QS, not junk terms → G2 ads.
- [x] **H10 [C]** PMax brand exclusion (Edu: "execute on 2", 2026-10-08). `pmax_brand_exclusion_2026-10-08.py`.
      - BRANDS list "TSD - Proud Pops brand (PMax exclusion)" (shared set 12263604514) with Google brand entities /g/11zy333b8y
        "Proud Pops" + /g/11zbnljsnq "Proud Pops Plumbing, Air & Electric".
      - Excluded on both PMax campaigns via a negative BRAND_LIST campaign criterion. A campaign_shared_set link is rejected
        for PMax (OPERATION_NOT_PERMITTED_FOR_CONTEXT).
      - Plus PHRASE negatives proud pops, problem solvers, pops electric, pops electrical on both PMax campaigns.
      - Read-back all present. Google's "The Problem Solvers" entity is an unrelated UK company, so it's not used. Branded untouched.
  - [ ] **H9a [C]** ~Oct 15 (with G1d / H3d): re-sweep search terms on HVAC, Plumbing and Branded. The 10-08 location
        expansion will bring new terms from the added cities.
- [ ] **H8 [C]** Search HVAC ($733–948 per customer form): after Block F + re-baseline, consider testing /services/hvac vs
      /proud-pops-hvac-services (the latter is a two-hop to /schedule).

## Logging (after every block)

- [x] Block A logged · [ ] B · [ ] C · [ ] D · [ ] E · [ ] F · [ ] G · [ ] H
- Each entry: what changed, IDs, read-back proof, who approved. Same entry in Agency Titan.

## Do not

- Do not start Block F before E1–E4 are ticked.
- Do not enable, un-hide or recategorize any other conversion action to make up lost volume.
- Do not change any budget, or pause PMax HVAC, from this checklist. Those need written client approval
  through the AM.
- Do not trust a mutation's success JSON. Always read back. (`update.py` without `--customer-id` silently hits
  the wrong account. `--budget` is in centavos.)
