# Spencer Air — Google Ads log (2524618054)

Not in `contas.yaml` — pass `--customer-id 2524618054` explicitly on every `tsd.sh` call. LSA lives
inside this same account (campaign 15789372405), not a separate one. See [[tsd-spencer-air]] /
[[topserv-google-ads-location]] for full account background (Meta account, prior lead-quality ticket
findings, etc.).

---

## 2026-11-06 — LSA moved to Pay-per-lead PMax by Google (read-only, nothing changed)

Old LSA `15789372405` paused; new `24436741588` created 11-04 11:29. SERVING / LEARNING, asset group ELIGIBLE → spencerairconditioning.com,
budget $164.29/d, 78 locations. Billing approved, license + insurance passed. **Not dark**: impressions 85 / 79 (11-02/03 old) → 88 on 11-05
(12 clicks, $0 = no charged lead). Old LSA had the same pattern (11-02: 85 impr, 12 clicks, $0). Leads ~1 every other day (11-01, 11-03).

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

## 2026-11-04 — fu-111 Branded after the $10 cap + fu-031 CallRail uploads (read-only, nothing changed)

Script `spencer_recheck_1104.py` (this folder) + CallRail (COM4563…, 151 calls 10-21 → 11-03). POST 10-29 → 11-03 (6d) vs PRE 10-21 → 10-27 (7d on $8).
No account changes since Edu's 10-28 cap raise.

| Branded (Target IS 95% abs-top) | POST ($10 cap) | PRE ($8 cap) |
|---|---|---|
| Spend/day | $18.40 | $3.80 |
| Clicks / impr | 14 / 71 | 5 / 44 |
| Avg CPC | $7.90 (not pinned at the cap) | $5.28 |
| IS / abs-top / rank-lost | **98 / 67 / 2** | 72 / 50 / 28 |
| Real leads | 2 ad calls (217s, 81s) + 1 CallRail upload + 1 web form | 0 |

- **The $10 cap works:** brand coverage is back (IS 98%, every day 92-100%), and CPC averages $7.90, below the cap. Keep it.
- **All 4 Google Ads calls since 10-21 are repeat callers in CallRail** (existing customers: 10-30 218s, 11-02 385s homepage, 11-03 82s, all Dallas/Irving).
  0 first-time brand calls. Normal for brand search; Branded mostly serves existing customers.
- Branded's Conversions column also counts 2 `[TSD] Click to call` taps (no bidding effect on Target IS, but it inflates KPI rows) and misses the
  web form (Submit lead form - Web counts under All only).
- **fu-031 Spencer: uploads WORK.** Repeat Phone Call uploads landed 10-28 and 11-02 (the 11-02 one = the 385s homepage call with gclid). The
  First/Repeat split is restored. Call-extension calls (10-30, 11-03) did NOT upload: Google already counts them as Calls from ads, so CallRail
  skipping them looks expected (inference, same pattern on ICS).
- **fu-031 ICS:** a Repeat Phone Call upload landed 10-31 (first since 10-09). Its 3 gclid calls 10-29 → 11-03 were all call-extension calls (same as
  above), which explains the "0 uploads" seen before. Integration looks fine; no UI check needed unless a website gclid call fails to upload.
- **Clean-up proposed (Edu's go):** Spencer leftover 'Phone Call' 7849678789 → Secondary (no conversions since 10-19, First/Repeat now proven);
  Spencer `[TSD] Click to call` → Secondary (reporting only, Branded doesn't bid on conversions).
- Still open from fu-111: AM note on the Google underspend (LSA leads down for the season) + early Meta retargeting ask (Edu).
- **APPLIED later 11-04 (Edu: "Apply the clean up please")**, `spencer_cleanup_1104.py`, validate-only then `--apply`, read-back OK:
  'Phone Call' 7849678789 and `[TSD] Click to call` 7835387495 → **Secondary** (primary False, include_in_conversions_metric False). Both still report
  under All conversions. From 11-04 Branded's Conversions column = Calls from ads + First Time/Repeat Phone Call only (the web form is still All-only).
- AT Internal Request **65cc23b2-8716-4c47-b0d1-7e1f6405b315** "Google Ads update: branded campaign and call tracking" created as a DRAFT for Angela (Intake, Edu submits; task department = Customer Success).

---

## 2026-09-15 — weekly PPC snapshot pulled (read-only)

**Authority:** none needed — read-only metrics pull, no account changes.

Ran the standard [[tsd-weekly-ppc-snapshot]] recipe: `insights.py account`, `read.py campaigns`, and
`insights.py campaign` for LAST_7_DAYS, plus a `FROM campaign` conversion-action segment query to
trust-check the conversions.

**PPC only (LSA excluded)** — only active Search campaign is Branded
(`TSD_07.05_Leads_Search_Branded`, 23822436393); Nonbranded (`TSD_07.05_Leads_Search_Nonbranded_Cooling`,
23822363451) is built but paused, $0 spend.

| Metric | Value |
|---|---|
| Spend | $429.19 |
| CPC | $18.66 |
| Total Conversions | 3.00 |
| Conv Rate | 13.04% |
| CPL | $143.12 |
| Branded Conversions | 3.00 |
| Unbranded Conversions | 0 |
| Branded CPL | $143.12 |
| Unbranded CPL | N/A (Nonbranded paused) |
| Impression Share (Search, total) | 94.29% |

Trust check: the 3 Branded conversions were 1 Form Capture + ~2.0 Calls from ads — real lead signals,
no junk conversion actions in the breakdown this period.

**Context excluded from the table above but relevant:** LSA (campaign 15789372405) did $1,706.36 /
17.0 conversions the same week — it's still the dominant lead engine on this account, this snapshot
just isolates PPC per Edu's standard convention.

---

## 2026-09-21 — Nonbranded campaign pause inquiry + re-enable request to AM

**Authority:** none needed for the inquiry (read-only, no account changes). Re-enabling needs written
client approval via the AM ticket, so Edu asked the AM for permission to turn Nonbranded back on at
$50/day. Approval status: pending, no answer on record as of this entry. The campaign is still PAUSED.

**Question:** why and when was `TSD_07.05_Leads_Search_Nonbranded_Cooling` (23822363451) paused, given
Branded is the only Google Search campaign running.

**When:** it only ever served 2026-05-07 to 2026-05-19 (13 days, launched the same day as Branded; "07.05"
in the name is 7 May). Zero impressions since 05-19, so it was paused around 05-19/20, before Edu joined
(06-17). The exact date and actor could not be pulled: the API's `change_event` only holds ~30 days and
returned 0 rows. The Google Ads UI change history (Tools > Change history, filter the campaign,
05-19 to 05-21) should show it. Not yet checked there.

**Why: no record found.** No decision documented in Slack or ClickUp (the ClickUp workspace connected here
is not TSD's ticket system; Agency Titan not checked). What the data shows for the 13-day run:

| Metric | Value |
|---|---|
| Spend | $712.88 |
| Clicks | 59 (~$12 CPC) |
| Counted conversions | 0 |
| All conversions | 2 ("Submit lead form - Web", not counted as primary) |

Search terms were mostly competitor brands and DIY/junk (r 10 heat & air, elmers ac, chill brothers dallas,
tiger air dallas, mondragon mechanical reviews, freon-cost questions). Poor performance is the likely reason,
but that is an inference, not a documented decision. The "one real trial and it failed" line in
`marketing-calendar-2027.md` comes from this same data.

**Lead to the actual reason:** Manuel Cabrera (paid at the time) posted a 05-22 Slack update saying the
Spencer Air Meta card was failing, Meta budget was moved toward Google, and part of the LSA budget was
being shifted to Google. It does not mention Nonbranded. His Media Plan sheet (Drive id
`1yXcPF--RJge9zlH35o4Y-3iikIuvO4CKV-eELUEVaLc`) holds the per-client pacing notes but the Drive connector
could not open it.

**State of the campaign today:** PAUSED, budget $56.73/day (the ask is $50/day, so the budget needs to be
reset when it is enabled), Maximize Conversions, ad groups AC Repair and AC installation with keywords still
enabled (mostly exact/phrase).

**Google spend since Edu joined (2026-06-17 to 2026-09-21):**

| Campaign | Spend | Conversions |
|---|---|---|
| LSA (15789372405) | $15,793 | 168.2 |
| Branded Search (23822436393) | $4,808 | 144.7 |
| Legacy Search_Brand (22295433521) | $62 | 0 |

Branded has been the only Search campaign running since Edu joined. The legacy Search_Brand campaign is a
pre-TSD brand campaign that trickled 39 impressions between 06-17 and 07-01 and has been dark since.
Nonbranded: $0.

**Next:** wait on AM approval. Before enabling, the 05-07 to 05-19 search terms say the negative keyword list
and match types need a review, and the Q1 2027 strategy already gates a Nonbranded relaunch on a real
negative-keyword build and a confirmed landing page (see `marketing-calendar-2027.md`).

---

## 2026-10-05 — Weekly 7-day check (Agency Titan task): no changes needed

**Read-only.** Last 7 days (09-28 → 10-04), PPC only: Branded `23822436393` is the only Search campaign live.

| Spend | Clicks | Conv | CPL | Search IS |
|---|---|---|---|---|
| $176.69 | 14 | 7 | $25.24 | 77.4% (14.5% lost to budget, 8.1% to rank) |

Conversions: 3 Calls from ads, 3 Repeat Phone Call (existing customers, still counted), 1 First Time Phone Call. Search
terms 100% brand. It spent about half its $50/day (no clicks 10-03 and 10-04). LSA same week: $287.91, 3 leads.

**Status:** Nonbranded `23822363451` still PAUSED, waiting on the 09-21 AM approval request to relaunch at $50/day.

**Agency Titan:** task closed with a note; KPI - Google Search entry 10-05 (Account Health "Good").

---

## 2026-10-06 — Weekly 7-day task (next cycle, 1 day after the 10-05 pass): no changes

**Read-only.** Last 7 days (09-29 → 10-05), PPC only: Branded $219.19, 13 clicks, 8 conv, $27.40 CPL, Search IS 70.2%.
Spend is lumpy ($0 on 10-03 and 10-04, $99.96 on 10-05). Conversions: 2 Calls from ads, 2 First Time Phone Call,
**4 Repeat Phone Call** (existing customers), so ~$55 per new-customer call. Search terms 100% brand. LSA $398.31, 4 leads.

Nonbranded still PAUSED: the 09-21 AM approval request has had no answer for 2 weeks.

**Agency Titan:** task `d4839f0a` closed; KPI - Google Search entry 10-06 with the full note in Lead Quality Notes.


---

## 2026-10-09 — ⚠ CallRail → Google Ads integration went DISABLED (side effect of the C&S reconnect session)

Found via CallRail API (read-only) after Edu reconnected C&S Air integrations with access@topservdigital.com in the CallRail
UI. This client's CallRail Google Ads integration (MCC 4155514468 → this account, first-time vs repeat) was **active
earlier on 10-09 and is now DISABLED**. Same happened to All Heart (offboarded) and ICS/Spencer: exactly the 3
integrations routed through MCC 4155514468. Cause not confirmed (re-auth side effect or the browser agent).
access@topservdigital.com is ADMIN on MCC 4155514468, so it can re-enable them.

Impact: CallRail call conversions (`First Time Phone Call` / `Repeat Phone Call`) stop reaching this Google Ads account
until it is re-enabled. **Fix: reconnect in CallRail with access@topservdigital.com via MCC 4155514468, same settings.**

Spencer was receiving them: 30d First Time 6 + Repeat 19 + Form Capture 2, last upload 10-07.

---

## 2026-10-10 (evening): Branded paying $25–$100 per click (found while refreshing the funnel, nothing changed)

TSD_07.05_Leads_Search_Branded, Maximize Conversions, no CPC cap, $50/day budget. Spend vs clicks: 10-05 $99.96/4, 10-06 $100.00/3,
10-07 $107.69/4, 10-08 $7.19/1, 10-09 $18.28/1, 10-10 $99.74 on ONE click (11h). Google is spending up to 2x the daily budget on a handful
of branded clicks. Options for Edu: max CPC cap (portfolio Max Conv with bid limit / Target Impression Share) or Manual CPC on Branded.

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Google (PPC only):** Branded $359.79, 11 clicks, 6.2 conv (4.5 Repeat + 1.7 First Time Phone Call), $58.34 CPL, ~$212 per new-customer lead, 57% IS (40% lost to budget), $32.71 avg CPC (QS 9–10 exact brand). Days at ~2x budget: 10-06 $100/3 clk, 10-07 $107.69/4, 10-10 $99.74/1. CallRail uploads recorded for 10-10 (after the 10-09 disable), so imports look live again; confirm in CallRail before closing fu-031. KPI Health = Mixed.
**Staged, not applied:** Branded → Target IS (top of page 90%) with $8 max CPC (fu-040).
**LSA:** $751.77, 8 leads (6 calls, 2 messages), $93.97, budget $164.29/d spent $107.40/d (Underspending), top impression 91.6%. Google status: 4 booked, 2 active, 2 declined (messages, charged). Mix 5 maintenance / 3 repair.
**Meta:** see meta-ads-log.md 10-13.
AT tasks closed: Google 6111eb8b (KPI 2307dd48), LSA a27a3265 (KPI ee323d22), Meta 2938e9db (KPI 75e0da94).

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-20 — Weekly 7-day + 14-day pass (Agency Titan tasks, Gui): read-only, KPI entries logged, changes staged

**Google (PPC only, 10-13..10-19):** Branded $172.18 (prior $359.79), 11 clk, 8 conv, $15.65 CPC, 94% IS (prior 57%). The 8 conv are inflated: call_view = 3 calls (2 over 60s) counted under 5 actions (Phone Call 2, Calls from ads 2, Repeat 2, First Time 1, Click to call 1). Real new-customer leads ≈ 1. 10-19 = $99.93 on 5 clicks (2x budget). 'spencer hvac service llc' may be another company (1 clk). KPI Health = Mixed.
**14-day (10-06..10-19):** avg CPC $24.18; 'spencer air conditioning' [exact] $45.09/clk at QS 10 (bidding, not quality); 1 RSA only; 18 brand variants Rarely served; no audiences; geo fine.
**Staged, not applied:** Target IS 90% top + $8 max CPC (fu-040); one primary call action (keep CallRail First Time, others secondary); 2nd RSA; observation audiences; dismiss broad/PMax/Display/partners recs.
**LSA:** $354.10, 4 charged leads (3 calls, 1 message), $88.53 CPL; lead report 7 total (1 booked, 1 message still NEW / unanswered, 1 declined). $50.59/d of $164.29 = Underspending, top impr 90.5% (demand drop, not rank).
**Meta:** see meta-ads-log.md 10-20.
AT tasks completed 10-20: Google d7740224 (KPI bcdc6869), 14-day e5a65586 (toggles must be set in UI), LSA 0cfc0119 (KPI c95f35ea), Meta ef13cf06 (KPI 01ec60ce).

---

## 2026-10-20 — What happened to the CallRail → Google Ads calls (fu-031), read-only

**CallRail uploads landing in Google Ads (all conversions, by day):** First Time / Repeat Phone Call kept arriving after the
10-09 disable (10-10 Repeat 3, 10-13 Repeat 2, 10-14 First Time 1), then nothing 10-15 → 10-18. On **10-19 a NEW upload action
`Phone Call` (7849678789) got 2 calls.** It is ENABLED and PRIMARY, next to the old primary First Time Phone Call (7537112154),
Repeat Phone Call (7536813785) and Form Capture (7536813764).
**Reading:** someone reconnected the CallRail → Google Ads integration between 10-14 and 10-19 with CallRail's default settings
(one 'Phone Call' action for all calls) instead of the old first-time vs repeat split. Calls flow again, but existing-customer
calls now count as full primary leads, and if the old integration also comes back, calls will count twice.
Who did it is not visible: change_event returns 0 rows on this account (known), and the CallRail API returned 429 (rate limit)
on every try today, so the integration config is not checked yet.
**ICS (4571881760) for comparison:** last CallRail upload 09-29 (First/Repeat), nothing since. Still broken.

**Options for Edu:** (a) keep the new integration but set it back to first-time vs repeat in CallRail, then set `Phone Call`
7849678789 to secondary; or (b) keep 'Phone Call' as the only call action and set First/Repeat secondary. Either way only one
call action should be primary. ICS still needs the reconnect.

## 2026-10-20 (later) — CallRail integrations fixed by Edu via Claude in Chrome + Google Ads read-back

**Browser agent report (Edu, CallRail UI):** Spencer integration was set to "one conversion action for all calls" (that made
`Phone Call` 7849678789). Changed to first-time vs repeat separately; rest unchanged (enhanced conversions on, call values
after 15 min, all forms, texts off). Active, access@topservdigital.com, 252-461-8054. ICS: was Disabled with no settings saved;
reconnected (access@topservdigital.com) to 457-188-1760, first-time/repeat separate, enhanced conversions on, **forms OFF**
(only changeable by a bulk edit across all 6 companies in the group, not done), call values off. Spencer, ICS, C&S all
stayed Active after each save. Accidental "Export conversions" on Spencer (email report only).

**Google Ads read-back (API):** no duplicate actions created. Spencer still has one First Time Phone Call (7537112154), one
Repeat (7536813785), Form Capture (7536813764), plus the leftover `Phone Call` 7849678789 (2 conv on 10-19, should get no new
uploads). All four are DEFAULT/WEBSITE, so goal-level settings can't separate them; left as is (option: hide/remove it later).
ICS: First/Repeat (7532065560/7531895404) are NOT in the Conversions column (secondary), same as before the break; old
`Phone Call` 496748578 (CONTACT, primary) won't receive uploads now. So ICS bidding still won't see CallRail calls; that was
already true before 10-09.
**Not checked:** CallRail calls 10-15 → 10-18 (API still 429 at end of day).

## 2026-10-20 (night) — APPLIED: Branded → Target Impression Share, 95% absolute top, $8 CPC cap (Edu: "go for it")

Why: last 30d Branded = $1,130 / 58 clicks / 225 impressions, **$19.49 avg CPC** on QS 9–10 exact brand terms, 55% absolute
top, single clicks up to $100 (10-10). Maximize Conversions with no target was bidding up for brand clicks (many are existing
customers calling, counted via Repeat Phone Call).
Applied via `branded_target_is_2026-10-20.py` (validate first, then live). Read-back: TARGET_IMPRESSION_SHARE, ABSOLUTE_TOP_OF_PAGE
95%, ceiling $8.00, budget $50/d unchanged. Rollback = back to Maximize Conversions.
**Expect:** Branded spend ~$37/d → ~$5–15/d; counted conversions from Branded may drop a little.
**⚑ Recheck 2026-10-27 (fu-073):** absolute-top IS (was 55%) and IS (76%); if it falls under ~80% because of the cap, raise the
ceiling $2 at a time. Avg CPC, spend/day, brand calls. Unspent Branded money can move to Nonbranded or LSA later at the same total.

## 2026-10-22 — CallRail upload check after the 10-20 fix (fu-031), read-only

CallRail calls 10-13 → 10-21 matched against Google Ads conversions by conversion date. Both integrations show `active` in CallRail.
**Spencer:** gclid calls 10-13 (2, repeat) and 10-14 (1, first) uploaded as Repeat 2 / First Time 1, matching. **10-16 11:15 'Google Ads' call, 110s, repeat, gclid: never uploaded** (the 10-15 → 10-18 gap). 10-19: 3 gclid calls (12:22 first, 12:59 first, 15:27 repeat) → only 2 landed, under the leftover `Phone Call` 7849678789 (pre-fix config). **No gclid calls on 10-20 or 10-21**, so the restored First/Repeat split has not had a call to prove itself yet. All 4 upload actions are still primary_for_goal (Form Capture, First, Repeat, Phone Call).
**ICS (4571881760):** 7 'Call Extension (Google Ads)' calls with gclid 10-13 → 10-21, **0 First/Repeat uploads in Google Ads**, including 10-21 06:45, 483s, first-time, which came after the 10-20 reconnect. Integration says active, so the next step is CallRail's ICS Google Ads integration page (upload history, min duration, linked account 457-188-1760), not the API. ICS Google side meanwhile records `[TSD] Click to call`, `Landing Page Call` and `Calls from ads` (1 on 10-21).
**⚑ Recheck 2026-10-24 (fu-031).**

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

**90-Day Google (https://app.agencytitan.com/tasks/instance/7eec5b35-5a73-4fbf-aaf5-1362ce20e184), read-only, completed.** 07-28..10-25 Branded only: $3,875.37 / 256 clk / 101.7 conv / $38.12 / CPC $15.14 / IS 75.9%. Repeat Phone Call 46.8 (46%), Calls from ads 32.8, First Time 17 (~$228 per new-customer call); call_view 37 calls (33 of 60s+), so calls are double counted.
**Stalled:** First Time last upload 10-14, Repeat 10-13; Branded calls 10-16 (109s) + 10-19 (131s) got no First/Repeat upload, the 2 uploads on 10-19 went to the leftover 'Phone Call' action; Submit lead form - Web 0 in 90d; Form Capture last 09-20; GA4 ghl_* + Local actions primaries dead. Staged: tracking task (Gui to create).
**After the 10-20 Target IS $8 cap:** 10-20..10-25 $10.64 / 3 clk / 0 conv / 0 calls; IS 25% on 10-21/22, 50% 10-23, 100% 10-24/25 (prior 7d $172.18 / 11 / 8). fu-073 recheck 10-27: cap may be too low on weekdays.
Hours: 07-18h = 92.7 of 101.7 conv; Sat/Sun CPL $48.82 / $59.59. Demographics: 65+ mostly Repeat. No audiences (lists exist: GA4 all users 1,700, converters 24). Geo 100% in the 10 targeted cities. 20/30 kws RARELY_SERVED. Recs open: KEYWORD, RSA, partners, PMax, dynamic image.
**Staged, not applied:** one primary call action (First Time); CallRail integration re-test; 2nd RSA; observation audiences; dismiss partners/PMax/dynamic image recs; re-check URLs/tags when Alex's site launches. Toggles (UI): Stalled Conversions Found = Yes, Schedule Adjusted = No, Demographics Excluded = No, Audiences Excluded = No, Locations Excluded = No.

## 2026-10-27 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in the account. KPI rows dated 10-27: Google fb824fb4, LSA 7b30dc67 (weekly + 30-day keys on one row).

**7-Day Google (https://app.agencytitan.com/tasks/instance/70bce40a-d9d8-47cd-8931-b702478bee8c), completed.** 10-20..10-26 Branded only: $26.38 / 5 clk / 45 impr / 0 conv / CPC $5.28 / IS 74.3% (rank-lost 25.7%, budget 0%). Prior $172.18 / 11 / 47 / 8 conv / $15.65. fu-073 recheck: the $8 ceiling cut spend 85% with impressions flat, but weekday IS fell to 25% (10-21, 10-22) and 50% (10-23), then 86-100% 10-24..10-26. 0 Branded calls in call_view all week. Search terms 100% brand. Health Mixed.
**30-Day Google (https://app.agencytitan.com/tasks/instance/14f1f563-4e78-430b-9744-5e7fadc10d67), completed.** 09-27..10-26 $915.30 / 50 clk / 27 conv / $33.90 CPL / CPC $18.31 / IS 74.7% (prior 30 $1,442.11 / 29.9 conv / $48.15). 27 conv vs 6 calls in call_view (Repeat 14, First Time 5, Calls from ads 5, Phone Call 2, Click to call 1). RSA labels all NOT_APPLICABLE; top headlines 'Spencer Air Conditioning', 'Spencer HVAC - Irving, TX', 'Spencer Air 24/7 Service'; weak 'Since 1960', 'Carrier Certified', '5-Star AC Service'. QS 9-10. Geo 100% in targeted cities (Irving $525.96, Dallas $211.95, Coppell $113.31). Homepage 39 clk / 18.5 conv. Stalled: First Time last 10-14, Repeat 10-13, Submit lead form / Form Capture / GA4 ghl_* / Local actions 0 in 30d. CallRail API 429 today, integration not re-checked.
**Staged, not applied:** Branded CPC ceiling $8 → ~$12 (recheck 11-03); one primary call action (First Time); CallRail integration re-test; 2nd RSA (top 4 headlines + heating lines); Services snippet; swap Blog/Our Mission sitelinks for heating pages. Toggles (UI): Extensions & Assets Updated = No, Geo Exclusions Added = No, Landing Page Issues Found = No, Session Recordings Audited = No, Blockers to Escalate = Yes (7-Day: Tracking Firing = No, Blockers To Escalate = Yes).
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/6fbfc8dc-063a-4356-a8e4-02c7a2882e90) + 30-Day (https://app.agencytitan.com/tasks/instance/5d5cdf08-b6e2-4ccf-9877-ffe94d41b1a6), completed.** Week: $208.20, 3 charged (1 call + 2 msg), $69.40 CPL, 6 leads in report (3 calls not charged), 18% of the $1,150/wk budget (Underspending), top impr 93.0%. 30d: $1,712.38 vs $4,937.97 prior (-65%), charged 19 vs 50, CPL $90.13 vs $98.76; budget unchanged and only 35% used, top impr 91.6% vs 89.3%, impressions -13% but charged leads/impression 1.38% → 0.60%: the early-Sept AC repair peak (wk 08-31 $1,961 / 20 leads, 09-07 $1,873 / 18) rolled out of the window; mix now maintenance (10 of 26). Booking 9/26 = 34.6%; 1 dispute PENDING, 0 credited; 4 charged DECLINED not disputed; 2 NEW messages unanswered (10-19, 10-25). Staged: dispute eligible declined leads, answer the 2 messages, confirm heating job types on in the profile. No budget change.

## 2026-10-28 (later) — fu-031: CallRail → Google Ads uploads after the 10-20 fix (Spencer + ICS, read-only)

- **Spencer: can't verify yet, nothing to upload.** CallRail has 7 gclid calls 10-12 → 10-28 (187 calls total), the last on 10-19.
  Zero gclid calls since the 10-20 fix, because Branded now gets ~1 click a day. Uploads by conversion date: 10-13 Repeat x2,
  10-14 First Time x1, 10-19 leftover 'Phone Call' x2 (pre-fix), nothing since. The 10-16 repeat gclid call (110s) never uploaded (known gap).
  Leftover 'Phone Call' 7849678789 is still ENABLED + primary. Remove/hide it once a First Time/Repeat upload shows up after 10-20.
- **ICS: still broken.** Zero First Time / Repeat / Phone Call uploads since 10-09, although CallRail has ~12 gclid Google Ads calls since
  10-09, incl. the 10-21 483s first-time booked call. The integration says active, but nothing arrives. Needs a look in the CallRail UI
  (integration status, which actions, min duration) via the browser. ICS PMax doesn't bid on these anyway (custom goal 10-28).

---

## 2026-10-28 — fu-100: Branded cap + unspent Google budget (read-only, NO changes)

No changes in the account since 10-20. Enabled: Branded (Target IS abs-top 95%, $8 cap, $50/d) + LSA ($164.29/d).
- **Branded since the 10-27 read:** 10-21→10-23 learning (1–2 impr/day, IS 25–50%). From 10-24 IS is back to 83–100%, rank-lost 0–17%.
  The 7-day average (72%) is pulled down by the learning days, so the 80% rule no longer triggers on recent days. But CPC sits right
  under the cap ($7.31, $7.87, $7.92 on 10-25/26/28), and abs-top was 57% / 50% on 10-26/27, the two busiest brand days (21 and 8 impr).
  So the $8 cap is what costs the top spot. Brand keywords are QS 9–10. Raising to $10 costs ~+$2/click on ~5 clicks/week (~$10/week).
- **Why Google underspends:** Branded ~$4/d by design. LSA (pay per lead) was ~$4,950/mo Jul–Sep (≈ the $164/d budget) and is $1,712 for
  Oct 1–27. LSA impressions/day are flat (Sep ~122/d, Oct ~120/d), and leads fell (50 in Sep → 19 in Oct). Same visibility, fewer people
  calling = shoulder season in DFW, not reach or budget. No ad schedule on LSA (runs 24/7), 13 service types, 78 locations.
  Nothing inside Google can absorb the gap under the Q1 plan (LSA + Branded only).
- LSA lead handling: in 30d, 5 phone leads ACTIVE + 2 messages NEW, not marked by Spencer.
**APPLIED same day (Edu's go):** Branded Target IS cap **$8 → $10** (`spencer_branded_cap_1028.py`, read-back $10.00, abs-top 95% unchanged). Recheck 11-04 (fu-111): abs-top share, CPC, brand calls.
**Still for Edu/AM:** Unspent budget: tell the AM that Google will run ~$35–45/d through the
shoulder season, and ask the client whether to start the Q1 plan's Meta retargeting early with part of it (needs the AM/client).

---

## 2026-10-27 — fu-073 recheck: Branded on Target IS ($8 cap), read-only

Script `spencer_branded_recheck_1027.py`. POST = 10-21 → 10-26 (6 days after the 10-20 night switch) vs PRE = 10-07 → 10-20 (14 days).
No changes in the account since Edu's 10-20 switch.

| Branded 23822436393 | Spend/day | Clicks | CPC | Conv (counted) | IS / top / abs-top | Rank-lost |
|---|---:|---:|---:|---:|---|---:|
| PRE (Max Conv) | $31 | 19 | $22.74 | 12 | 87 / 81 / 74 | 3% |
| POST (Target IS, $8 cap) | **$4** | 5 | **$5.28** | **0** | **70 / 67 / 50** | **30%** |

- **Cost: worked.** CPC $22.74 → $5.28, spend ~$31/d → ~$4/d (saves ~$27/d).
- **Coverage: dipped, then recovered.** 10-21 → 10-23 IS 25–50% on 1–2 impressions a day (learning); 10-24 → 10-26 IS 86–100%,
  abs-top 57–100%. The 6-day average (IS 70%, all loss = rank, 0 budget) is under the ~80% line set on 10-20.
- **Brand calls:** CallRail 'Google Ads' calls on Branded: PRE 4 first-time 60s+ (10-07, 10-14, 10-19 x2) + repeats; POST only 1
  (10-23, 230s, repeat customer, no gclid). Google call_view: no ad-button calls since 10-19. Small numbers, but ~1–2 new brand callers
  may have been lost in the 3 learning days. Overall calls didn't drop: Organic & GMB 5.9/day PRE → 8.5/day POST, so brand demand is
  there and most of it reaches Spencer through GBP/organic anyway.
- Counted conv PRE 12 included 5 Repeat + 2 'Phone Call' + 2 Calls from ads + 2 First Time + 1 Click to call (double counting, see 10-20).

**LSA (where unspent Branded money could go): not budget-limited.** $35/d of $164 POST (charged per lead, lumpy $65–74 days), 3 leads in
6 days vs 11 in 14 days before; CallRail LSA calls ~1/day both periods. LSA can't absorb more money, and Nonbranded is paused, so Spencer's
Google spend is ~$39/d against ~$214/d budgeted.

**Proposed (needs Edu's go):** raise the Branded cap $8 → $10 (the 10-20 rule: +$2 if IS < 80% because of the cap). Spend would stay
~$5–8/d. Bigger question for Edu/AM: Spencer is spending well under plan on Google; the only real outlet is relaunching Nonbranded. *(Corrected in the next entry the same day: the Q1 2027 plan rules out Nonbranded.)*

## 2026-10-27 (later) — Live Google tracking test on the NEW site (read-only, nothing recorded)

spencerairconditioning.com now serves Alex's Next.js site (no GHL markers), GTM-KT5RPTP live. Headless Playwright test, fake gclid, every
Google/Meta hit ABORTED, no real form submitted. Script `google-ads-ratos/scripts/spencer_live_google_test_1027.py` (+ ad-hoc passthrough test).
- **Loads:** GTM-KT5RPTP + AW-761311353 + G-4DT6CPR0BP on every page; CallRail swap.js loads and swaps the number (new pool number each load).
- **Consent:** default all denied → Ads/GA4 send cookieless pings (gcs G100) that still carry the gclid; after Accept All, `_gcl_aw` is set (G111).
- **Phone tap → `[TSD] Click to call` (Jm0cCOeMmpgdEPnggusC) fires with the gclid**, both consent states.
- **Form:** the site's lead code pushes `event: window.__trackingLeadEvent || "lead_submitted"` with event_id + user data after a successful
  submit; live pages set `__trackingLeadEvent = "form_submitted"`, which is exactly the GTM trigger. A synthetic `form_submitted` fires Ads
  **Submit lead form - Web** (ZwC_CPnY8okcEPnggusC) with the gclid (hashed email/phone only after consent) + GA4 generate_lead.
- **gclid survives landing → /contact** (client-side navigation), even with consent denied. A hard reload on another page without consent
  would lose it (no url_passthrough decoration on links).
- Duplicate hits per event in the test are expected from aborting requests (gtag retries over other transports); actions are ONE_PER_CLICK.
- **Not testable without a real lead:** the server action itself. First real form lead (or one agreed test) closes it.
- ⚠ **Leak:** the homepage's main buttons "SCHEDULE NOW", "Schedule Service", "Schedule" go to carrier.com/residential/.../find-a-dealer/
  schedule-now (dealerId 6628, zip 75038), not Spencer's /schedule or /contact. Anyone booking that way leaves the site: no Google Ads, GA4,
  Meta or CallRail conversion. Only /contact is linked internally from the homepage; /schedule exists but isn't linked there.
- Reminder: Submit lead form - Web (SUBMIT_LEAD_FORM) is not biddable on Branded's goals (DEFAULT / PHONE_CALL_LEAD / CONTACT).

**Nonbranded?** The client-facing Q1 2027 strategy says Google lead gen = LSA + Branded only, Meta/YouTube = awareness + retargeting; the May
2026 Nonbranded trial (13 days, $713, 0 conv, competitor/DIY terms) failed. So no Nonbranded relaunch now. Unspent budget belongs to the
plan's own outlets: LSA (why only $35/d of $164?), YouTube + Meta retargeting (Q1 plan).

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in the account. KPI rows dated 11-03: Google 82f466fb, LSA 8d2a2108.

**7-Day Google (https://app.agencytitan.com/tasks/instance/52600b61-035c-43d3-b081-9955b8c5b794), completed.** Week 10-27..11-02 vs 10-20..10-26, Branded only: $104.43 / 13 clk / 5.9 conv / CPL $17.77 / CPC $8.03 / IS 95.6% (rank-lost 4.4%); prior $26.38 / 5 / 0 / IS 74.3%. Edu raised the Target IS ceiling $8 → $10 on 10-28 14:07 (API); since then daily IS 92-100% (abs-top 50-80% vs 95% target, status Limited). The 5.9 conv = 3 click-to-call taps + 2 Repeat Phone Call uploads + 0.9 Calls from ads; real calls 2 (10-30 217s in call_view + CallRail, 11-02 385s CallRail gclid), both CallRail repeat callers, the 10-30 call counted twice. 0 new-customer calls. CallRail Google Ads integration active, Repeat uploads landing again; First Time untested (last first-time gclid calls 10-19 x2 went to leftover 'Phone Call'; none since). Search terms 100% brand. Health Mixed.
**14-Day Google (https://app.agencytitan.com/tasks/instance/c97b9978-3265-4e53-bb6c-a2ed04582d5d), completed.** 10-20..11-02 $130.81 / 18 clk / 5.9 conv / CPL $22.26 / CPC $7.27 / IS 86.3%; prior 14 $531.97 / 22 / 14.2 / $37.55 / CPC $24.18. QS 9-10, 1 RSA GOOD (assets NOT_APPLICABLE), geo 100% in targeted locations, no audiences, recs open: partners, KEYWORD, RSA, dynamic image, PMax. No keyword changes.
**Staged, not applied:** keep $10 ceiling (the ~$12 from 10-27 not needed), recheck 11-10; one primary call action (First Time) + retire leftover 'Phone Call' upload (tracking task, Gui to create); 2nd RSA with heating lines; GA4 lists as observation audiences; dismiss partners/PMax/dynamic image recs. Toggles (UI): 7-Day Tracking Firing = No, Blockers To Escalate = Yes; 14-Day High-CPC Keywords Reviewed = Yes, Keyword Warnings Reviewed = Yes, Keywords Paused or Fixed = No, Geo Targeting Adjusted = No, Audience Added = No.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/462e9704-5a36-4f89-87b8-1627f866301d), completed.** $341.33, 3 charged calls, 0 messages, CPL $113.78 (prior $208.20 / 3 / $69.40); 30% of the $1,150/wk budget (Underspending), top impr 93.0%, impressions 634 vs 641: demand, not budget/rank. Leads: AC maintenance, HVAC maintenance, AC repair (no heating); 10-30 lead dispute PENDING (new). 2 messages still NEW/unanswered (10-19, 10-25). Staged: answer them, confirm heating job types on.

## 2026-11-10 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in the account. KPI rows dated 11-10: Google 785a5599, LSA 74e48cfb.

**LSA migrated:** Google moved Spencer's LSA into a PMax-type campaign 'Pay-per-lead-PMax-Spencer Air Conditioning & Heating' **24436741588** (first spend 11-07); the old LocalServicesCampaign 15789372405 is PAUSED (last spend 11-03). No LSA spend 11-04..11-06. `weekly_kpi.py` counts the new one as PPC: excluded by hand from KPI - Google Search, counted as LSA.
**7-Day Google (https://app.agencytitan.com/tasks/instance/390bcf70-6dbd-48fc-93ff-9a02f329dec3), completed.** Week 11-03..11-09 vs 10-27..11-02, Branded only: $86.91 / 10 clk / 5 conv / CPL $17.38 / CPC $8.69 / IS 88.2% (rank-lost 11.8%); prior $104.43 / 13 / 5.9 / IS 95.6%. 5 conv = 2 Calls from ads + 1 First Time + 1 Repeat Phone Call (CallRail uploads of the same 2 calls) + 1 Local actions - Directions; call_view 2 calls, both 60s+: about 2 real leads, real CPL ~$43. **First Time Phone Call upload landed** (first since the 10-20 fix), so that action works. Terms all brand. No changes since Edu's 10-28 $10 ceiling.
**Staged, not applied:** Directions → secondary; one primary signal per call (uploads primary, Calls from ads secondary; tracking task, Gui to create); keep $10 ceiling; 2nd RSA with heating lines. Toggles (UI): Tracking Firing = Yes, Blockers To Escalate = No.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/65e46389-5a43-4b9a-b106-8960e2317512), completed.** $184.67 ($74.70 old + $109.97 PMax-type), 3 leads (2 calls, 1 message; 2 charged), CPL $61.56 (prior $341.33 / 3 / $113.78). $164.29/d = $1,150/wk, 16% used (Underspending). Top impr 98.0% on 106 impr (old campaign; the new type doesn't report it). Jobs: repair_ac, hvac_maintenance x2. 10-30 dispute now CREDITED. Messages 10-19 + 10-25 still NEW.

## 2026-11-17 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in the account. KPI rows dated 11-17: Google b3bb1635, LSA 6dd00560. No account changes since Edu's 10-28 ceiling ($8 to $10).
**7-Day Google (https://app.agencytitan.com/tasks/instance/975dcaea-00c4-4908-b1e5-2df7a20a63c5), completed.** Week 11-10..11-16 vs 11-03..11-09, Branded only (PMax-type LSA 24436741588 subtracted from weekly_kpi.py output): $103.78 / 14 clk / 4 conv / CPL $25.95 / CPC $7.41 / IS 100% every day (abs-top 50-100%); prior $86.91 / 10 / 7 conv (3 Directions) / IS 88.2%. 4 conv = 3 Calls from ads + 1 First Time upload; call_view 11-10 91s, 11-12 130s, 11-13 38s, 11-16 61s, the 11-16 call likely counted twice, so ~3 real calls (~$34.59). 11-04 cleanup held; Directions 7080814948 still primary. Terms 100% brand. CallRail caller check not done (API 429). Health Good.
**14-Day Google (https://app.agencytitan.com/tasks/instance/da66bd38-7e00-4a8d-a361-5099518cc8c7), completed, all 8 checklist items ticked.** 11-03..11-16: $190.69 / 24 clk / 11 conv / CPC $7.95 / IS 93.8%; prior 14 $130.81 / 18 / 5.9. 6 ad calls, 5 at 60s+ (~$38 per real call). QS 9-10, 1 RSA GOOD, homepage only, geo 100% targeted, no audiences. Open recs: partners, KEYWORD, RSA, dynamic image; sitelink + tCPA on the pay-per-lead campaign.
**Staged, not applied:** Directions → secondary; one primary signal per call (tracking task, Gui to create); keep $10 ceiling; 2nd RSA with heating lines; GA4 lists on Branded as Observation; dismiss partners/dynamic image/KEYWORD recs. Toggles (UI): 7-Day Tracking Firing = Yes, Blockers To Escalate = No; 14-Day High-CPC Keywords Reviewed = Yes, Keyword Warnings Reviewed = Yes, Keywords Paused or Fixed = No, Geo Targeting Adjusted = No, Audience Added = No, Blockers To Escalate = No.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/a7f0496b-b838-479c-9afb-88e89dc5a8b7), completed.** All on PMax-type 24436741588 (old 15789372405 $0): $530.12, 7 leads (2 calls + 5 messages, 6 charged), CPL $75.73 ($88.35 per charged); prior $184.67 / 3 / $61.56. Charges 11-14 $72.20, 11-15 $296.23, 11-16 $161.69, $0 on 11-10..11-13. 46% of $1,150/wk (Underspending, not budget-limited). 865 impr, top impr 100% (this GAQL on the new campaign does return it). Jobs: heating_maintenance x3, repair_hvac x2, repair_heating_system, install_thermostat: heating demand started. 11-15 two repair_hvac messages 20s apart, both charged = duplicate candidate to rate (fu-161). All 5 messages NEW, plus 10-19 and 10-25.
