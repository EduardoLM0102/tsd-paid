# King's Window Services — Google Ads log

Customer ID `6769493219` — "King's Window Services - PPC & LSA" (PPC and LSA live in the same
customer ID here, unlike most TSD clients). Not in `contas.yaml` yet — found via `customer_client`
under MCC `4155514468`. Site: kingswindowservices.com. GA4 property `389493105`. GTM container
`GTM-MNF2N73B`.

---

## 2026-08-31 — PMax paused, budget shifted to Nonbranded Search; keyword cleanup

**Executed** by Edu (Head of Paid, verbal authority) after reviewing account status.

### Changes

| # | Object | ID | Before | After |
|---|---|---|---|---|
| 1 | `phone_call` conversion action (real CallRail calls, GA4 import) | 7314063586 | `primary_for_goal: False`, `include_in_conversions_metric: False` | **`True` / `True`** — now counted toward Conversions + biddable |
| 2 | Nonbranded Search `TSD_28.04_Search_Nonbranded_Evergreen` — network settings | 23796640968 | `target_search_network: True` (partners on) | **`False`** |
| 3 | 10 broad keywords, 0 conversions / 30d, spread across Glass Replacement, Frameless Shower Enclosures, and Window Replacement ad groups (list below) | — | ENABLED | **PAUSED** |
| 4 | PMax `TSD_Pmax_WindowServices_Calls` | 23036120066 | ENABLED, $20/day | **PAUSED** |
| 5 | Nonbranded Search budget (`campaignBudgets/15547840993`) | 23796640968 | $32/day | **$52/day** |

Account-level daily budget unchanged (~$82/day live spend capacity) — PMax's $20/day moved into
Nonbranded, not added on top. No client-facing total budget change.

**Keywords paused (10, all $0 return over trailing 30 days):**
glass replacement near me ($68.14), glass repair service ($38.97), residential glass replacement
($37.56, QS 1 — worst score in the account), bathroom shower glass ($36.96), bathroom shower
remodel doors ($24.41), glass shower door service ($21.38), shower enclosure installation
($19.62), replacement windows for home ($24.70), glass companies near me ($24.58), window fixer
near me ($23.86). ~$320/mo of campaign spend freed, zero conversions lost.

### Why

- PMax relaunch (see 2026-08-17 change in [[tsd-kings-window]] memory) delivered 1 conversion in
  12 days for $150.92 (~2.15x its $70 tCPA target), lumpy delivery (several $0 days, then bursts
  ~2x its daily budget), flagged `LIMITED / BUDGET_CONSTRAINED` by Google. Second underperformance
  strike after the mid-July overspend/auto-throttle crash on the same campaign.
- Nonbranded Search converts reliably ($47–83 CPL by keyword) but was both rank-capped (55.6%
  impressions lost to Ad Rank) and, as of this week, budget-capped too (28.6% lost to budget,
  up from ~7.5% two weeks prior) — real headroom to buy more volume at a proven CPL.
- Edu's call: prefers Search carrying the large majority of spend; PMax's delivery pattern has
  been unreliable twice now.

### Flag for correlation — READ THIS FIRST if the client asks about traffic/volume changes

**2026-08-31**: PMax campaign fully stopped (was running since 2026-08-17 post-relaunch, before
that since account start). If total account traffic/impressions drop noticeably in the days
following this date, PMax's removal is the most likely cause (it was still delivering real
impression volume — Cross-network/Display/YouTube reach — even though it converted poorly). Lead
*volume* should hold or improve (spend moved to a channel with a real, proven CPL); raw
impressions/reach will likely drop since PMax's placements (Discover, Gmail, YouTube, Display)
disappear entirely. Check this entry before assuming a tracking break if the client flags a
volume or reach change in the next few weeks.

### Open items
- Re-verify `phone_call` conversion volume accumulates cleanly over the next 1-2 weeks now that
  it's biddable — GA4 attribution is still ~80% "Unassigned" for this event (unresolved, parked
  per Edu 2026-08-31), so actual usable signal will be thinner than raw event counts suggest.
- Once phone_call data is clean, retune Nonbranded's implicit CPA expectation (no tCPA cap
  currently set — running plain Maximize Conversions).
- Decide whether PMax gets a third attempt later (better landing assets, logo files added, tighter
  budget) or stays off for good — not decided, just paused for now.

---

## 2026-09-15 — Weekly PPC snapshot pull + conversion trust check

**Read-only session** — no live changes, reporting only.

### What was pulled
Standard 7-day snapshot (see `[[tsd-weekly-ppc-snapshot]]` recipe), PPC only (Nonbranded +
Branded Search), LSA and paused PMax excluded:

| Metric | Value |
|---|---|
| Spend | $433.58 |
| CPL | $21.70 |
| CPC | $6.57 |
| Total Conversions | 19.98 |
| Conv. Rate | 30.28% |
| Branded Conversions | 3.98 |
| Unbranded Conversions | 16.0 |
| Branded CPL | $4.36 |
| Unbranded CPL | $26.01 |
| Impression Share (Search, blended) | 20.0% |

LSA (same customer ID, excluded from the table): 4.0 conversions / $328.03.

### Conversion trust check
Broke the 19.98 PPC conversions down by `segments.conversion_action_name` — all real lead
signals, no page_view/tap-click junk:

| Action | Category | Count |
|---|---|---|
| GA4 `phone_call` (CallRail-verified calls) | Phone Call Lead | 13.98 |
| Submit lead form | Submit Lead Form | 3.0 |
| GA4 `ghl_request_estimate` | Submit Lead Form | 2.0 |
| Repeat Phone Call | Default | 0.98 |

LSA's 4.0: `local_services_phone_lead` (Phone Call Lead, 3.0) + `local_services_message_lead`
(Unknown category — a text/message inquiry, not a call, 1.0).

**Open question, not investigated this session:** "Repeat Phone Call" is a separate legacy
Google Ads action from the GA4 `phone_call` import — worth checking whether the two are double
counting the same physical calls before leaning on the combined phone-call total.

---

## 2026-09-15 — Tracking rebuild

**Reported by Edu via chat, not executed by Claude this session.**

Tracking rebuilt and fixed. Old tags deactivated to make sure they don't disrupt or interfere with
the new setup.

---

## 2026-10-05 — Weekly 7-day check (Agency Titan task): no changes needed

**Read-only.** Last 7 days (09-28 → 10-04), PPC only (LSA excluded):

| Campaign | Spend | Clicks | Conv | CPL |
|---|---|---|---|---|
| TSD_28.04_Search_Nonbranded_Evergreen | $276.90 | 48 | 14 | $19.78 |
| TSD_03.16_Search_Branded_Evergreen | $7.74 | 4 | 2 | $3.87 |
| **Total** | **$284.64** | **52** | **16** | **$17.79** |

Account search IS 20.2% (56.2% lost to rank, 23.6% to budget). Conversions mostly GA4 `phone_call` (CallRail-verified)
plus `[TSD] Click to call` taps and lead forms. LSA same week: $298.16, 5 leads.

**Search terms:** clean. Window-screen searches kept open on purpose: the site lists "Window Screens & Accessories" and
"Screen Repair & Replacement" (checked 10-05). Competitor names get impressions (Glass Doctor, Ajax, Keller Glass, Lone
Star Glass), but "binswanger glass fort worth" converted once, so none were blocked. Decision for Edu.

**Agency Titan:** task closed with a note; KPI - Google Search entry 10-05 (Account Health "Good").

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $385.63, 66 clicks, 23 conv, $16.77 CPL (prior $21.08/16). Nonbranded 23 conv = 9 [TSD] Click to call taps, 8 GA4 phone_call, 3 Calls from ads, 3 forms (≈14 non-tap leads at ~$27). call_view 9 calls, 3 ≥60s. Branded $14, 100% IS. Nonbranded 42% IS lost to budget (16% last week) at $16 CPL: budget is the lever, needs client written OK via AM. LSA $578.33, 6 leads. KPI Health = Good.

**Changed:** nothing, no changes needed. AT task 2627ca2d closed, KPI record edf2fc90.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-19 — Weekly 7-day pass (Google + LSA + Meta) + 14-day review (Agency Titan tasks, Gui): read-only, all staged

**PPC 10-12..10-18:** $371.79, 17 conv, $21.87 CPL (prev $435.97 / 24 / $18.17). NB $353.62 / 17 (8 taps, 6 GA4 phone_call, 2 forms, 1 calls from ads; ~9 non-tap at ~$39). IS 20%: budget-lost 37%→12%, rank-lost 68%. Branded $18.17, 100% IS. Staged neg: 'kings windows and doors'.
**LSA (inside 6769493219):** $622.07, 7 leads (5 calls, 2 msg), $88.87, 98.4% top.
**Meta 483679897962388:** $294.65, 6 leads, $49.11. Lead campaign is ABO ($30+$15 ad sets). **Awareness `TSD_02.26_TOF_AWARENESS_CBO_Creatives` = REACH + frequency CAP 3/7d** (off doctrine) → rebuild as ARL no cap, staged.
**14-day (10-05..10-18):** $807.76 / 41 conv. Rank is the limit (53% rank-lost); 'glass company near me' QS 3 carries 29/41 conv → improve ad/LP relevance; low-QS glass/shower keywords; remove Branded kw 'king's window repair houston'; outside-target clicks only 7% (Fort Worth, Grapevine). No audiences.
AT tasks 1a6a8163 / 5f8a5a77 / 567d82cd / cb7050b0 left open for Gui's review.
