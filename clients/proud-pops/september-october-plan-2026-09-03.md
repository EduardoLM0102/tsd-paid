# Proud Pops — September / October plan

**Prepared by:** Eduardo Marinho, Paid Ads · **Date:** September 3, 2026
**Account:** 1051843378 (PPC), + LSA `7261668241` (Electrician), `6621969129` (HVAC)
**Source:** Google Ads API, pulled live 2026-09-03. Covers the gap left after `budget-allocation-2026-08.md`,
which only planned through Aug 31 — there is no September/October plan on record before this doc.
**Companion docs:** `budget-brackets-and-keyword-research.md` (Jul 23), `budget-allocation-2026-08.md` (Jul 30),
`google-ads-log.md` (through Aug 19).

---

## Headline: the account has been bidding on phone-number clicks, not leads, for over a month

This has been diagnosed **three separate times** — Jul 23, Aug 10, Aug 19 — and never actually fixed.
`TSD - Website Call` is a **click-to-call tap**, not a verified call (confirmed at the GTM layer:
it's an `awct` click conversion by design, with CallRail owning real call verification separately).
It is still `primary_for_goal = True` and `include_in_conversions_metric = True` today, and it now
dominates the account's reported conversion count:

| Campaign | "TSD - Website Call" (clicks) | Real `Website lead` (form fills) | Share that's just a click |
|---|---:|---:|---:|
| PMax HVAC | 607.4 | 39 | 94% |
| PMax Electrical | 310.5 | 62 | 83% |
| Search Nonbranded Electrical | 98.0 | 19 | 84% |
| Search Nonbranded HVAC | 31.1 | 10 | 76% |
| Search Nonbranded Plumbing | 28.5 | 4 | 88% |
| Search Branded | 19.0 | 9 (all_conversions) | 68% |

(Aug 4 – Sep 2 window, `metrics.conversions` / `metrics.all_conversions` by `segments.conversion_action_name`.)

**What this actually costs:** PPC spend over the same 29 days was ~$41,500. Using only `Website lead`
(the one reliable lead signal) as the denominator: **143 real form-fill leads → ~$290/lead.** That is
roughly **double** the $137.70 fully-loaded cost-per-form-fill flagged as a concern back on Jul 30 — and
that number was already called out as too high. The account's own reporting says blended CPA is
$13–40 across PMax; the real number, once you strip the phone-click inflation, is closer to $290.

Every August budget decision — the ramp to $525/day, then to $1,760/day in live caps today — was made
partly on this inflated signal, because it is what Maximize Conversions and Target CPA are optimizing to.
**This is Gate 0 for September. Nothing else in this doc matters until it's fixed**, because right now
we cannot tell the difference between "the ramp is working" and "the bidder found a cheap way to win
auctions with people who tap a phone number and hang up."

### The fix (this one is finally executable, not a UI/tag problem)

Unlike the earlier GTM-layer fixes (those needed Edu on-site), this is a **Google Ads account-level
conversion-action setting** — `ConversionActionService.mutate_conversion_actions` on `TSD - Website Call`,
setting `primary_for_goal = False` (or removing it from `include_in_conversions_metric`). That's inside
what the skill tooling can already do. Two sequencing notes:

1. **Do not do this in the same week as a budget change.** PMax HVAC and PMax Electrical will look like
   their CPA got dramatically worse overnight — it didn't, the number just became honest. Demote first,
   let a clean week of data accumulate, *then* make budget calls off the new baseline.
2. Existing Target CPA bids (PMax HVAC $27, PMax Electrical similar) were set against the inflated
   number and will be too low once the fix lands — plan to loosen or remove them for a week rather than
   let Maximize Conversions starve the campaigns chasing an unreachable CPA.

---

## What's live right now (Sept 3 snapshot)

| Campaign | Budget/day | 7d Impr. Share | Lost to budget | Lost to rank |
|---|---:|---:|---:|---:|
| Search Nonbranded HVAC | $375 | 21.8% | 25.0% | 53.2% |
| Search Branded | $70 | 81.2% | 9.0% | 9.8% |
| Search Nonbranded Plumbing | $160 | 16.0% | 10.2% | **73.7%** |
| PMax HVAC | $325 | 10.0% | **90.0%** | 0.9% |
| PMax Electrical | $230 | 13.2% | 8.5% | 78.3% |
| Search Nonbranded Electrical | $600 | 25.6% | 11.6% | 62.7% |

**The constraint flipped back.** In July the account was budget-limited; the Aug ramp fixed that for most
campaigns — now **every campaign except PMax HVAC is rank-limited again**, the same wall this account
kept hitting all summer. Pouring more raw budget in for September would mostly not buy impressions
except on PMax HVAC — and PMax HVAC is the campaign most contaminated by the phone-click signal (94%),
so its "budget-starved" read isn't trustworthy yet either.

**Search Plumbing got worse, not better.** 73.7% rank-lost today vs. 40.6% in the Jul 22–29 clean
window. It was deliberately capped at $120–160/day for five weeks *pending* a landing-page/QS fix that
was never executed. "Wait and see" has now produced a worse campaign, not a fixed one.

**Total live daily budget caps: ~$1,760/day PPC + $200/day video ≈ $58.8k/mo if fully spent.** Actual
utilization runs 66–88% of cap, which is why the account landed close to $48–50k over the last 29 days —
essentially the Aug pool. **Nobody has decided a September number.** The budgets simply never rolled
back after Aug 31, so the account is spending at Aug-ramp levels on autopilot, with no new approval on
record. That's a process risk independent of the strategy question below.

## Still open since July, zero build cost, never executed

- **Geo widening** — PMax HVAC, Search HVAC, and Search Plumbing still target **San Antonio city only**;
  Electrical targets 5 cities; LSA runs in **47**. Confirmed unchanged today. Free incremental inventory,
  flagged Jul 30, still not done.
- **Water treatment rebuild** — campaign `23875125989` is still the PAUSED SMART campaign with
  **zero keywords**. Still a rebuild-not-relaunch. The softener-cluster research (~1,600 service-intent
  searches/mo at $3–11 CPC vs. $20–30 on core plumbing) from Jul 23 has never been acted on.
- **AC install/replace split** — recommended Jul 23 (different buyer, different bid, high ticket),
  never built.
- **ServiceTitan validation** — every CPA figure in every doc since Jul 23, including this one, is cost
  per *tracked lead*, never checked against a *booked job*. Six weeks open. This is the one dependency
  that would tell us whether $290/lead (or whatever the honest number turns out to be) is even a problem.
- **AM ticket / written approval** — the Jul 7 budget cut and the Aug ramp still have no record per
  Edu's Aug 10 note that the $50k was approved as a top-level pool (which satisfies MasterOps at the
  pool level) — but there is no pool approval at all for what's currently running in September.

**What did get done:** Branded is live (was paused all of July). Display network and search partners are
confirmed OFF on every live Search campaign today. `instant_quote_hvac_click` was pulled as a conversion
action Aug 19 (it wasn't biddable, but it was cluttering the conversion count).

---

## September — sequencing

**Week 1 (now):**
1. Demote `TSD - Website Call` from primary/biddable. Loosen or pull the Target CPA caps on PMax
   HVAC/Electrical for the week so the bidder doesn't starve chasing a now-unreachable number.
2. Hold budgets where they are — don't cut, don't raise — while the signal re-stabilizes.
3. Widen HVAC + Plumbing geo to the 5-city Electrical footprint. Zero cost, no learning-period risk.
4. Decide water treatment: rebuild it this month (it's a scoped, ready research doc) or formally kill
   the idea. Five weeks of "maybe" is its own cost.
5. Get a real AM ticket on record for current spend — it's running at ~$48–50k/mo pace today with
   nothing approved past Aug 31.

**Week 2 (once a clean week of honest data exists):**
6. Re-pull CPA using only `Website lead` + `Calls from ads` + LSA `local_services_*` — this replaces
   every CPA number in this account's history to date. **This is the number September's budget decision
   should actually be made on**, not the $13–40 figures currently in the reports.
7. Decide Search Plumbing for real: fund the landing-page/QS fix, or explicitly hold it flat through
   October instead of leaving it capped-and-hoping again.
8. Push the ServiceTitan cross-check — assign it an owner and a date instead of re-flagging it a fourth
   time next month.

**Do not** decide a bigger September/October budget number until step 6 lands. Scaling spend on top of
an unverified signal is exactly how the account got to a reported $38 blended CPA that's actually ~$290.

---

## October — conditional on what Week 2 shows

**If the honest CPA (Website lead + Calls from ads + LSA) comes back workable against job value:**
- Fund PMax HVAC specifically — it's the one campaign that's genuinely budget-capped (90% lost to
  budget, 0.9% to rank), so it's the one place more money can still buy volume, once the money is
  chasing a real signal.
- Build the AC install/replace split out of Search HVAC — high-ticket, different buyer, still just a
  July recommendation sitting unbuilt.
- Layer in water treatment (if rebuilt in September) as the cheap-CPC wedge it was scoped to be.

**If the honest CPA comes back bad:**
- October becomes an optimization month, not a scale month — QS/Ad Rank work on Plumbing and PMax
  Electrical (both still 73–78% rank-lost), landing-page routing to service-specific pages instead of
  the homepage, and no further budget increase until rank recovers.
- Revisit whether the ~$50k/mo run-rate is still the right target at all, now that the real cost per
  lead is on the table instead of the inflated one.

Either way, October's number should be set from Week 2's real data, not from extrapolating August.
