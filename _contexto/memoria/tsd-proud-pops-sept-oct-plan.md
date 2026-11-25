---
name: tsd-proud-pops-sept-oct-plan
description: Proud Pops Sept/Oct-2026 plan — Gate 0 is fixing the phone-click conversion action before any budget decision; constraint flipped back to rank-limited on 5 of 6 campaigns; doc at clients/proud-pops/september-october-plan-2026-09-03.md
metadata: 
  node_type: memory
  type: project
  originSessionId: fa515fa3-e81c-4a05-b839-c593a7d24f4f
  modified: 2026-09-03T15:07:15.545Z
---

⚑ 11-16 fu-137 read + APPLIED (Edu): Electrical $455→$375 (the 11-09 +$80/d bought looser matches, 0 extra leads, ~$317/lead; 3 of 4 callers wanted same-day and didn't get it), Plumbing $145→$75 ($1,661 / 2 leads since 11-04, General kept = the group that produces), 8 negatives (mechanic/circuit board/gate opener/independent/cheap on Elec; pops/corporation on HVAC; pops on Plumb). Lesson: pausing a bare keyword on a no-target Max Conv campaign just moves the leak (Services→Repair on 11-09); the lever is budget/tCPA. Search caps $730/d. Next read fu-172 11-23.


Built 2026-09-03 — no Sept/Oct plan existed before this (the Aug doc, [[tsd-proud-pops-aug-budget]],
only covered through Aug 31). Full doc: `topserv-workspace/clients/proud-pops/september-october-plan-2026-09-03.md`.

**Gate 0, before any budget call:** demote `TSD - Website Call` from primary/biddable — see
[[tsd-proud-pops-tracking]] for the full diagnosis. It's still live and still dominating reported
conversions as of today.

**Constraint flipped back to rank-limited** on 5 of 6 live campaigns (same wall as July) — only PMax
HVAC is genuinely budget-capped (90% lost to budget), and even that read isn't trustworthy until Gate 0
lands (94% of PMax HVAC's reported conversions are the phone-click). Search Plumbing got *worse* while
capped-and-waiting for 5 weeks (73.7% rank-lost now vs 40.6% in July) — the "hold budget pending a fix"
pattern doesn't work if the fix never happens.

**Zero-cost items still open since July, unchanged today:** geo widening (HVAC/Plumbing still
San Antonio-only vs Electrical's 5 cities vs LSA's 47), water-treatment rebuild (still 0 keywords),
AC install/replace split (never built), ServiceTitan lead validation (6 weeks open).

**Process gap:** live daily budget caps sum to ~$58.8k/mo; actual spend lands ~$48–50k/mo on
autopilot — nobody decided a September number, the Aug-ramp budgets just never rolled back, and there's
no written approval on record past Aug 31.

**Sequencing:** Week 1 = Gate 0 + geo widening + water-treatment go/no-go + get an AM ticket on record.
Week 2 = re-baseline CPA on `Website lead` + `Calls from ads` + LSA only (real number, not the reported
one), then decide Plumbing and the actual Sept budget off that. October is explicitly conditional on
what that re-baseline shows — scale (fund PMax HVAC, build AC install/replace) if the honest CPA holds
up, optimize-only (QS/rank work, no more budget) if it doesn't.

**How to apply:** don't quote this account's reported CPA/conversion numbers without checking whether
Gate 0 has landed yet — re-verify `TSD - Website Call`'s `primary_for_goal` status before trusting any
blended CPA figure from this account.

**2026-10-13 — why it ran ~$2,000/d, and the cut back to $50k (Edu OK, APPLIED).** The $50k approval was the AUGUST pool.
Only $6,005 was spent by Aug 10, so the Aug 10 / Aug 17 raises (+ YouTube $200/d from Aug 8) were sized to spend ~$44k in
21 days (~$2,100/d). That catch-up rate was never rolled back on Sep 1: caps $1,960/d × 30.4 = $59.6k/mo, which matches Sept
($59,635) and the October pace (~$60k). Cut on 10-13 (`clients/proud-pops/budget_cut_50k_2026-10-13.py`, read-back OK): PMax HVAC
$295→$50, PMax Elec $230→$75, Search HVAC $375→$300, Search Elec $600→$500. Caps went to $1,385/d, and to $1,285/d once Edu pauses
YouTube San Antonio in the UI (fu-046), so October lands at about $50k. Recheck fu-047 on 10-20. **Nov 1 steady state for $50k/mo
≈ $1,600/d caps.** **How to apply:** an approval for a monthly total needs a matching steady-state daily rate. Any catch-up rate
must come with a written date to roll it back. Check sum(caps) × 30.4 against the approved month at every monthly rollover.

**2026-10-23 weekly pass (Gui, read-only):** Branded-only week $818.60 / 18 conv, all phone taps, 0 recorded calls (call asset still disapproved, fu-052); brand CPC $8.95 → $10.91 under Max Conv, Target IS + ~$8 cap staged; LSA 3 surfaces $305.53 / 4 leads; no Meta account shared with TSD.

**2026-10-14 22:48 CT — CLIENT CUT TO $25k/MONTH (supersedes the $50k above).** October was already $28,105 (3 accts) by Oct 14,
so Oct can't hit $25k; Edu chose **Branded only for Oct 15-31 → Oct ≈ $30k**. Paused Search Elec/HVAC/Plumbing + both PMax
(`branded_only_25k_2026-10-14.py`); both YouTube need the UI (fu-046). **Nov 1 restore staged:** `nov_restore_25k_2026-11-01.py`
= Search Elec $340, HVAC $210, Plumbing $130, Branded $120 = $800/d (×30.4 = $24.3k + LSA ~$0.6k), PMax + YouTube stay off.
Command Center fu-053 (Nov 1 restore) + fu-054 (Nov 4 pacing). **How to apply:** before quoting a month-end landing for a budget
cut, pull month-to-date first; a cut announced mid-month can already be underwater. Nov 1 = Sunday: needs a UI automated rule or
a Monday run.

**2026-11-06 — fu-127 check (read-only).** Real-lead bidding works: taps only in all_conversions, CallRail First Time Phone Call uploads landing (4 on 11-05), call asset 225-5767 approved + serving. Electrical 6 real leads ~$131 each in 2 days. **Branded went dark after the 11-04 Target IS switch** (abs-top 95%, $10 cap): 2 impr after 08:08 on 11-04, 0 on 11-05. Not cannibalization (Nonbranded has brand negatives). Pre-switch brand CPC was $11.78-17.55, so a $10 cap can't win. Proposed cap $18. Detail in clients/proud-pops/google-ads-log.md 2026-11-06. (The "cap under the recent CPC turns it off" reading from this day was corrected on 11-09, see below.)

**2026-11-09 — fu-132 recheck (read-only): Branded serving again, and the 11-06 diagnosis was wrong on price.** After the ceiling went $10 → $18 (11-06 06:27 CT) impressions came back within hours: Search IS <10% (11-05) → 30.8% → 50.0% → 88.9% on 11-08, abs-top 38.9% vs the 95% target, status still LEARNING. Clicks cost $0.27–$3.94 (avg $2.79 on 11-08), nowhere near $18 and well under the old $10 cap. So the $11.77–17.55 brand CPC before the switch was Max Conversions overbidding while it still chased taps, not the market price. The data can't tell whether the dark days were the strategy ramping after the 11-04 switch or the $10 cap; the cap edit and the recovery happened the same morning. 1 real lead since (First Time Phone Call 11-08). Branded spends $1–20/d of its $130 (brand volume is ~16–50 eligible impressions/day), so ~$100/d is free. Electrical (8 real leads, $214 each, 11-04..11-08) loses 38% IS to budget. **APPLIED 11-09 (Edu's go): Branded $130 → $50, Electrical $375 → $455** (total $880 unchanged, `branded_to_electrical_2026-11-09.py`, read-back OK). Overview 11-04..11-08, 3 accounts: $3,686 / 15 real leads (~$246): Search $3,268 / 10 (~$327), LSA $418 / 5 (~$84). Plumbing $806 / 40 clicks / 0 actions of any kind (pages render fine, so traffic not a broken page; Max Clicks buys 'best/cheap plumbers' + competitor names); HVAC $751 / 1 lead, AC Repair clicks $53.52; My Favorite Service Smart campaign still running unmanaged (~$13/d, fu-019). November tracks ≈ $21.2k across the 3 accounts, ≈ $22.5k with the move, vs $25k; pacing fu-054 11-11. proudpops.com is a JS shell that returns 200 for any path: check landing pages with a headless render, not curl.

**2026-11-09 (later) — fixes APPLIED on Edu's go (`fixes_2026-11-09.py`).** Electrical: bare `electrical services` [PHRASE] paused ($461 / 14 clicks / 0 leads) + negatives electric company / aep / hourly rate. Plumbing: the 3 generic plumber keywords paused inside Leak Detection (they took $454 of $806; General keeps them) + negatives cheap / saws. HVAC: negative cheapest + portfolio Max Conversions 'TSD_ProudPops_HVAC_MaxConv_CPC30' (12308461252), $30 CPC ceiling, tCPA $265 kept (⚠ HVAC had a $265 tCPA all along, not "no cap"). 16 competitor names → account-level list 12263521315. My Favorite Service Smart campaign 23065942452 PAUSED (30d: $574, 5 tracked calls, none in the last 14 days; 5 other campaigns there are ENABLED but not serving, fu-019). **HELD: 'commercial' negative**, because the site sells "Residential & Commercial". One-week read fu-137 11-16. **How to apply:** before proposing a service-scope negative (commercial, emergency, a trade), render the client's site and check they don't sell it; and read `campaign.maximize_conversions.target_cpa_micros` before calling a Max Conversions campaign uncapped. **How to apply:** a Max Conversions CPC on a brand campaign is not the price of a brand click; don't size a Target IS ceiling or a brand budget from it. After switching a campaign to Target IS, give it 2–3 days before calling it dark, and judge by impression share, not spend.

**2026-11-09 (Gui AT run):** Nov restore ran 11-04 (not 11-01) at $880/d (Elec $375, HVAC $230, Plumbing $145, Branded $130), Branded → Target IS 95% abs-top, $10 cap starved it 11-05..11-07, raised to $18 11-06. 11-09 Edu: Branded $130 → $50, Elec $375 → $455 (total same), HVAC on shared tCPA $265 / $30 cap. Week 11-02..11-08 Search $3,514.65 / 13 conv: Elec $1,714 / 8, HVAC $751 / 1, Plumbing $768 / 0. Nov lands ≤ ~$24.8k at full caps.

**2026-11-16 (Edu 08:05 CT, found in change history by Gui's AT pass):** Electrical $455 → $375, Plumbing $145 → $75 (Search caps $880 → $730/d) + 8 phrase negs (Elec mechanic/circuit board/gate opener/independent/cheap, HVAC pops/corporation, Plumbing pops). Week 11-09..11-15: $4,673 / 17 real leads / $275 (Branded 5 @ $61, Elec 9 @ $336, Plumbing 3 (1 job seeker), HVAC $368 / 0). Nov 1–15 $9,550 (3 accts) → lands ~$19.5–20k vs $25k cap (Angela was told ~$21k, d2b5e325). HVAC = 1 lead / $1,120 in Nov: Edu to decide heating ad group vs pause.

**2026-11-20 (Gui AT run):** week 11-13..11-19 Search $4,403 / 21 / $210 (Elec $178/lead since the $375 cut, Plumbing $724 / 0 with 43% at night, HVAC $586 / 2); /pricing sitelink $2,288 / 3 conv in 14d; Nov to 11-19 $13,192 → lands ~$23.5k vs $25k. YouTube back ON 11-18 (Edu): New Braunfels 99% on TV apps (Samsung TV Plus, Tubi, Pluto). All staged for Edu.

**2026-11-20 (later, Edu's go):** /pricing sitelink 360873861063 REMOVED from Electrical + Plumbing (kept on Branded + HVAC), replaced by new sitelinks `Electrical Repair` 441525652903 / `Drain Cleaning` 441598912395 (account's service sitelinks are AUTOMATICALLY_CREATED = can't be linked, create new ones); Elec AG2 RSA 827482059113 PAUSED. Plumbing = hold (Edu). Edu fixed YouTube 11-20 himself (video partners off). Planned Nov = $25k, ~$23.5k is in range. [electrician] exact neg NOT applied (not confirmed). Script clients/proud-pops/pp_apply_1120.py (do not re-run).
