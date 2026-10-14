# Integrate Comfort Systems — Google Ads log (2895702982)

**Not in `contas.yaml` yet.** CID given directly by Edu (not found via MCC listing), confirmed
accessible under the Topservdigital MCC (4155514468) via the `tsd.sh` profile. Account name in
Ads: "Integrate Comfort Systems - LSA Belleville". USD, `America/New_York`.

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
