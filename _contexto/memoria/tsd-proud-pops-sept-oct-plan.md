---
name: tsd-proud-pops-sept-oct-plan
description: Proud Pops Sept/Oct-2026 plan — Gate 0 is fixing the phone-click conversion action before any budget decision; constraint flipped back to rank-limited on 5 of 6 campaigns; doc at clients/proud-pops/september-october-plan-2026-09-03.md
metadata: 
  node_type: memory
  type: project
  originSessionId: fa515fa3-e81c-4a05-b839-c593a7d24f4f
  modified: 2026-09-03T15:07:15.545Z
---

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
