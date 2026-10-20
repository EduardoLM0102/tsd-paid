# Spencer Air — Google Ads log (2524618054)

Not in `contas.yaml` — pass `--customer-id 2524618054` explicitly on every `tsd.sh` call. LSA lives
inside this same account (campaign 15789372405), not a separate one. See [[tsd-spencer-air]] /
[[topserv-google-ads-location]] for full account background (Meta account, prior lead-quality ticket
findings, etc.).

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
