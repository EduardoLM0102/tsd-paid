# Watt's Right Electric — Meta Ads Log (588638883283311)

Convention: newest entry on top. One entry per work session — researched → found → did → open items. See `clients/README.md`.
Google Ads, LSA and GTM history lives in `google-ads-log.md` in this folder.

---

## 2026-10-12 — Client retargeting report, Oct 2 to Oct 8 (MOF + BOF)

**Scope:** read-only live pull via Meta MCP + activity log. No account changes.

**Deliverable:** `Watts Right - Facebook Retargeting Report (Oct 2 - Oct 8).pdf` (source
`Watts-Right-Facebook-Retargeting-Report_2026-10-12.html`), 1 page, same structure as the 10-05 report. Rendered with
Playwright (no Chrome on this Mac). Pool sizes as of 10-12: TOF 3sec 69.2–81.4k, MOF 10sec 14.2–16.7k.

**Client PDF numbers (Oct 2 to Oct 8):** MOF $399.94 / 8,471 impr / reach 5,717 / 8 leads / $49.99 (freq 1.48). BOF $125.26 /
2,142 / 1,231 / 2 / $62.63 (freq 1.74). Total $525.20 / 10 / $52.52. By ad: Done Before Dinner ("The fastest way to upgrade")
$253.57 / 3 / $84.52; Mess-Free ("What does a mess-free panel") $146.37 / 5 / $29.27; Who Would You Trust $90.68 / 1 / $90.68;
Family's Safety $34.58 / 1 / $34.58. Prior week was $598.86 / 12 / $49.91 (no week-over-week in the PDF).

### Internal findings (kept out of the client PDF)
- **TSD campaign renames were reverted.** 10-06 11:18 "Clay Manus token" (app Manus Dash) renamed both back to
  `Leads-Panels-MOF-6/21/26` and `Leads-Panels-BOF-7/9/26`.
- **New retargeting outside MOF/BOF, launched 10-06 by Clay Manus token:** `05-RT-TOF3s | TOF video viewers` ($10/d) in the
  FourMode website-leads campaign, retargets TOF 3sec viewers to the landing page. Oct 2–8: $27.75 / 1 website lead. Also
  `RT-FourModeLPVisitors` ($5/d, site-visitor pool) in the TOF campaign, $0 delivered in the window. Plus 2 cold LAL1pct ad
  sets (paying-customers lookalike) in FourMode. **Not in the client PDF** (kept to the 3-step instant-form scope of 10-05).
- **Meta flipped Advantage+ audience ON 10-10 00:05** (actor Meta, no app) on every ad set in the account incl. MOF Broad-5/-9.
  MOF now also carries a hidden "Lookalike (US, 1%) - TOF 3sec Audience" expansion (creation_ui "Rules Engine"). Window
  Oct 2–8 is unaffected, but from 10-10 step 2 is no longer strictly 3s viewers. Next report's setup text has to account for it.
- **Live budgets now:** MOF Broad-5 $40, Broad-9 $27 (was $20 on 10-05, change predates log coverage); BOF -8 $15 (was $10,
  updated 10-05 10:02 CT, actor unknown), -9 $5.

### Open
- [ ] Edu: include the 05-RT-TOF3s website-leads ad set in future retargeting reports or keep 3-step scope only?
- [ ] Edu: Advantage+ audience ON for MOF (Meta's 10-10 switch). Turn back off to keep step 2 pure retargeting?
- [ ] Who is "Clay Manus token" / Manus Dash? Reverting TSD names + launching ad sets in this account.

*Reversibility: no account changes made.*

---

## 2026-10-05 — Client retargeting report built (MOF + BOF)

**Scope:** read-only live pull via Meta MCP. No account changes.

**Deliverable:** `Watts Right - Facebook Retargeting Report (Sep 25 - Oct 1).pdf` (source
`Watts-Right-Facebook-Retargeting-Report_2026-10-05.html`), 1 page (Edu cut the lead-dates section), plain format (Mission Accomplished
09-29 precedent). **Window per Edu: Sep 25 to Oct 1, 2026.** Client-facing, results only: setup, week
results by step, by ad. Edu: "keep the adjustment comments for us", so NO What's Next, no
since-launch/monthly history, no lookalike note in the PDF. First draft (30d + since launch + What's Next)
was replaced.

**Client PDF numbers (Sep 25 to Oct 1):** MOF $478.51 / 11,191 impr / reach 7,536 / 8 leads / $59.81. BOF
$120.35 / 2,184 / 1,380 / 4 / $30.09. Total $598.86 / 12 / $49.91. By ad: Done Before Dinner $299.70 / 5 /
$59.94; Mess-Free $178.81 / 3 / $59.60; Who Would You Trust $76.86 / 2 / $38.43; Family's Safety $43.49 / 2 /
$21.75. Leads by day: 9/25 2, 9/26 2, 9/27 1, 9/28 3, 9/29 1, 9/30 3, 10/1 0.

**Background analysis (not in the PDF), Sep 5 to Oct 4:** MOF $1,494.60 / 27 leads / $55.36, reach 17,624, freq 1.95. BOF $299.71 / 7 /
$42.82, reach 2,928, freq 2.02. Retargeting total $1,794.31 / 34 / $52.77. TOF $3,141.64 / 67 / $46.89.
**Since Jun 22:** MOF $4,648.77 / 85 / $54.69; BOF $1,273.55 / 21 / $60.65; retargeting $5,922.32 / 106 /
$55.87; TOF same period $8,557.64 / 164 / $52.18. July BOF = $796.38 / 7 / $113.77 (10 ad sets launched at once).

### Internal findings (kept out of the client PDF)
- **Retargeting is not cheaper than cold.** MOF (3s viewers) is the most expensive stage. BOF (10s viewers)
  is the cheapest instant-form stage over 30d. The 3s pool (64.6k–76k, 120-day retention) is loose.
- **BOF isn't pure retargeting.** Both active BOF ad sets have `targeting_relaxation_types: {custom_audience: 1}`
  with `expanded_implicit_custom_audiences` = "Lookalike (US, 1%) - MOF 10sec Audience" (creation_ui "Manus
  Dash"). Geo still Tulsa 50mi. Mentioned neutrally in the PDF note.
- **Correction to 10-01 entry: ad sets are NOT $5/day** (names say $5). Live: MOF Broad-5 $40, Broad-9 $20
  (set 07-28); BOF MOF10sViewers-8 $10 (raised from $5 on 09-22), -9 $5. $75/d budgeted, ~$60/d actually
  spent (~80% delivery).
- **Correction to 10-01 entry: FourMode is not an instant form campaign.** Result type = Website leads
  (`offsite_conversion.fb_pixel_lead`), ads are link/image (`SHARE`, GET_QUOTE). So its reach never enters the
  video-viewer pools, and no campaign retargets site visitors (pixel audiences ~20 people).
- **MOF since-launch total includes $555 / 6 leads from 6 paused ad sets with no audience at all** (cold broad).
  Left in the client totals so they match Ads Manager.
- **Actors:** budget/status changes Jul–Sep came from "Austin Ensz" (Power Editor) and "Clay Manus token" (app
  "Manus Dash", e.g. 09-22 reactivated MOF Broad-9 + BOF -9, raised BOF -8). Identity unconfirmed, not
  assumed external.
- Audience source video IDs (10 per audience) don't resolve in the ad-account video library. Likely the page-post
  copies of the 10 TOF / 10 MOF ads. Not verified 1:1, but the 3s pool is still growing (62.8–73.8k on 10-01 →
  64.6–76k on 10-05), so it's being fed.

### Open
- [ ] Internal adjustment ideas (kept out of the client PDF, Edu to decide): (1) ask client for 90d lead→job outcomes
  by step, (2) test MOF pool at 50%-watched instead of 3s, (3) website-visitor pool off the FourMode landing page (pixel check first).
- [ ] Decide whether to turn off lookalike expansion on BOF.
- [ ] Where instant-form leads land (GHL or not) is unconfirmed for this account.

*Reversibility: no account changes made.*

---

## 2026-10-01 — Retargeting audit; MOF + BOF campaigns renamed to TSD convention

**Authority:** Edu, in-session. Renames only, no budget, targeting or status changes.

**Why:** Edu asked whether retargeting had ever come up for Watt's Right. It hadn't. Searched this folder
(Google log, Sep budget report PDF, ad spend review) and all past Claude Code sessions: no retargeting
discussion anywhere. Then checked the Meta setup directly.

**Correction:** the 09-28 Growth Engine pull (`paid/relatorios/growth-engine-pull-2026-09/`) listed this
account as "Meta awareness only." That's wrong. It runs a live lead-gen funnel for panel replacement.

### Live funnel (all Instant Forms, Tulsa 50 mi around 5865 S Garnett Rd, age 25–65, Advantage+ audience OFF)

| Campaign | ID | Audience | Retargeting? | Last 30d |
|---|---|---|---|---|
| Leads-Panels-TOF-5/7/26 | 120243811096150470 | Cold. Excludes MOF 10sec viewers + form submitters 90d | No | $3,179 / 63 leads / $50.47 |
| **TSD_06.21_MOF_LEADS_ABO_Panels - Retargeting 3s Video Viewers** | 120246886128520470 | Active ad sets INCLUDE "TOF 3sec Audience" (~63–74k). Exclude MOF 10sec + form submitters | **Yes** | $1,434 / 26 leads / $55.16 |
| **TSD_07.09_BOF_LEADS_ABO_Panels - Retargeting 10s Video Viewers** | 120247833941160470 | Active ad sets INCLUDE "MOF 10sec Audience" (~11.5–13.5k). Exclude form submitters | **Yes** | $274 / 6 leads / $45.65 |
| LS \| Panels-FourMode-LP-ABO-9/22/26 | 120249335098310470 | Cold. Excludes TOF 3sec + form submitters | No | $279 / 6 leads / $46.52 |

MOF and BOF have no campaign budget (ABO, $5/day ad sets). In MOF, 6 older PAUSED ad sets ($555 lifetime)
had no audience at all. Only the current ad sets carry the 3s-viewer include.

### Audiences in the account

| Audience | Type | Size | Used by |
|---|---|---|---|
| TOF 3sec Audience (120247833507190470) | Video engagement | 62.8k–73.8k | MOF (include); FourMode + TOF-Static (exclude) |
| MOF 10sec Audience (120247833864160470) | Video engagement | 11.5k–13.5k | BOF (include); TOF + MOF (exclude) |
| WR - Form Submitters - 90d (120247858798180470) | Lead form submitters (Page) | n/a | Excluded across all funnel campaigns |
| Page Views (120222329102330470) | Pixel 567402072026960, PageView 30d | ~20 | Nothing |
| Page View_Without Leads (120228677791790470) | Pixel | ~20 | Nothing |
| Lookalikes ×4 (MOF 10sec 1%; Pagelike / Page Messaged / Page Engaged 3%) | Lookalike | INACTIVE | Nothing |

**Website retargeting isn't viable as-is.** The pixel audiences hold ~20 people and nothing uses them. All
retargeting here is built on video viewers.

### Older campaigns with misleading names
- **BOFU_Remarketing_Zips_Free Inspection** (120227868593760470, PAUSED, $5,330 lifetime): no custom
  audience. Targeted 17 Tulsa-area ZIPs with Advantage+ audience ON, optimizing for landing page views.
  Not retargeting.
- **Remarketing_ Sales Campaign_Free Inspection [Dec 17]** (120237020863290470, ARCHIVED): US-wide, no
  audience, $0 spend. Never ran.

### Did
- Renamed `Leads-Panels-MOF-6/21/26` → **`TSD_06.21_MOF_LEADS_ABO_Panels - Retargeting 3s Video Viewers`**
- Renamed `Leads-Panels-BOF-7/9/26` → **`TSD_07.09_BOF_LEADS_ABO_Panels - Retargeting 10s Video Viewers`**
- Pattern taken from existing TSD Meta names (`TSD_<date>_<FUNNEL>_<OBJECTIVE>_<CBO|ABO>_<descriptor>`).
  Kept the original launch dates. API confirmed both, `status_forced_to_paused: false`, both still ACTIVE.

### Open
- [ ] MOF ad sets are named `$5-Instant Forms-Tulsa 50mi-A25+-Broad-N` but target 3s video viewers, not
  broad. Rename to match (offered, not done). BOF ad sets (`...-MOF10sViewers-N`) are accurate.
- [ ] TOF and FourMode campaigns still use non-TSD names. Left alone, since only the retargeting ones were in scope.
- [ ] Who built this funnel is unconfirmed (no TSD_ prefix; "LS |" prefix on the 09-15/09-22 campaigns).
- [ ] Growth Engine pull: Watt's Right row should not read "awareness only".
