# Spencer Air — Q1 2027 Preliminary Marketing Recommendations (Internal)
## First Slice of 2027 Planning — Budget, Allocation, Lessons, Branding/Retargeting, QL/ROI

**INTERNAL ONLY.** Client ask (via AM): Spencer will begin planning for 2027 within the next
couple of months and wants TopServ's recommendations on budget and strategy. Scoped down to **Q1
2027 (Jan–Mar)** rather than the full year — a preliminary first slice, not the annual plan. Covers
overall budget, recommended Google/LSA/Meta allocation, lessons from 2026 performance,
branding/retargeting strategy, and opportunities to improve qualified lead volume and ROI, all
sized to what's realistic to commit to for Q1. Built 2026-08-26 directly off live Google Ads
(customer 2524618054) and Meta Ads (account 1845825982372184) data — no prior media plan or
approved budget figure exists on file for this account. Every dollar figure below is
illustrative/ratio-based, not a commitment — nothing here is final until the client signs off in
writing per MasterOps hard rule #1. A fuller year-two view (Q2–Q4) can follow once Q1 lands and the
gates below (Meta geo-targeting fix, CAPI restoration) have real data behind them — deliberately not
committing to Q3/Q4 numbers this far out on an account with only ~8 weeks of live Meta data.

Format follows the GC Home Service forward calendar (`clients/gc-home-service/marketing-calendar-2026-h2.md`),
adapted for this account's own season, channel mix, and gaps.

---

## The Season This Is Built Around

Spencer Air's live geo-targeting (Google LSA + Search, Meta lead ad sets) centers on the DFW/North
Texas metro (Bedford, Fort Worth, Dallas, Arlington, Euless, Keller, Burleson, Crowley, Wylie, Anna,
Grand Prairie, Sanger, Springtown). That market is **cooling-dominant**: a long, hot cooling season
runs roughly April through September/October, and winter is short and mild with only occasional
hard-freeze risk (the Feb 2021 Texas grid freeze is the standing reminder that "mild" doesn't mean
"zero emergency demand"). **Q1 sits in the lowest-demand part of this account's year** — no cooling
season pressure yet, and heating demand is thin and freeze-driven rather than sustained. That's
useful: Q1 is naturally the right quarter to do foundational/gate-clearing work (CAPI restore,
audience rebuild, geo-targeting fix) before budget needs to follow the cooling ramp starting in Q2.

---

## Lessons From 2026 Performance

### Google (customer 2524618054)

- **LSA is the account's real engine, and it hasn't shown saturation yet.** Monthly LSA spend
  scaled roughly 4.5x from January to August ($1,094.89 → $4,959.65) while cost-per-lead held in a
  tight $73–110 band the entire time (Jan $109.49, Feb $103.15, Mar $73.02, Apr $90.84, May $100.92,
  Jun $90.59, Jul $95.93, Aug $88.32 through the 25th) — CPA did **not** degrade as spend went up.
  That's the strongest signal in the account for where Q1 budget should go first.
- **Branded Search is budget-capped today.** Last 30 days: 79.6% impression share, 74.5% top IS,
  59.8% absolute top IS — but 11.3% is lost to **budget**, not rank, on a $50/day cap that's
  essentially fully spent ($1,530.12 actual vs. ~$1,500 cap). This is the cheapest lead in the
  account ($35.85 CPA last 30 days) and doesn't need to wait for Q1 — it's a same-week fix.
- **The July branded-search conversion count needs verification before it's trusted.** Conversions
  went from 22.13 in June to 71.99 in July on essentially flat spend ($1,411.52 → $1,539.41) — CPA
  fell from $63.79 to $21.38 in one month. Too sharp a jump to take at face value without checking
  whether a conversion-goal/counting change (not real demand) drove it — this should be reconciled
  in Q1 before it anchors any budget math.
- **Nonbranded Search had one real trial and it failed.** `TSD_07.05_Leads_Search_Nonbranded_Cooling`
  spent $712.88 in May for 59 clicks and zero real conversions. It's been PAUSED since. Not a Q1
  candidate — no working formula exists for it on this account yet.
- **No PMax exists anywhere in this account's history.** Not a Q1 default either — a deliberate
  yes/no decision for later in the year, not now.
- **LSA lead-level quality detail (disputed/booked/charged) is not accessible via the API** — the
  `local_services_lead` query returned a permission error specific to that resource. Worth
  requesting Local Services detailed-lead-reporting access from Google as a Q1 task, since LSA is
  the account's largest spend line and currently unverifiable on quality.

### Meta (account 1845825982372184)

- **Meta was completely dark for five months this year** ($0 spend Jan–May), only back online June
  30. Everything below is based on roughly 8 weeks of live data — a reason to keep Q1 Meta spend
  disciplined rather than scaling on a thin track record.
- **Both active lead campaigns leak out-of-area leads.** `07/01/26 - CBO | Leads` and `08/11/26 -
  CBO | Leads`, both named "Texas Locations," are delivering 22% and 30% of leads respectively to
  people in Louisiana, Mississippi, Oklahoma, and Oregon. The newer campaign's lower headline
  cost-per-lead ($50.44 vs. $79.88 in August) is partly an artifact of that leak. **This needs
  fixing in Q1 before any Meta budget increase** — check the location-targeting type (living-in vs.
  broader) and whether Advantage+ Audience expansion is on.
- **No retargeting layer exists.** Only three LOOKALIKE audiences, all created 2017-10-04, all
  INACTIVE, seeded from stale 2017 page-likers. Meanwhile the Awareness campaign has delivered
  333,005 impressions this year at a strong $2.40 CPM — reach with nothing capturing it. Q1's
  low-demand season is the right window to build this before it's needed for the Q2 cooling ramp.
- **Conversions API has been dead since June 2023.** Browser pixel is healthy (last fired
  2026-08-23) but server-side hasn't fired in over three years. Fixing this is a Q1 technical
  prerequisite for everything else on the Meta side.

---

## Recommended Q1 2027 Budget & Allocation

**No total budget figure exists on file for this account today** — the table below is the account's
live, currently-committed daily budget, presented as the baseline Q1 reacts to, not something
Spencer has already agreed to.

| Channel | Current daily budget / pace | Current ~monthly | Last-30-day actual result |
|---|---|---|---|
| Google — LSA | ~$164.29/day cap (spending at cap) | ~$4,930 | 56.16 conv, $88.32 CPA |
| Google — Branded Search | $50/day (spending at cap) | ~$1,500 | 42.68 conv, $35.85 CPA |
| Google — Nonbranded Search | $0 (paused) | $0 | — |
| Meta — Lead CBO (07/01/26) | $51/day | ~$1,530 | 16 leads/Aug, $79.88 CPL |
| Meta — Lead CBO (08/11/26) | $50/day | ~$1,500 | 14 leads/Aug, $50.44 CPL (geo-leak discount applies) |
| Meta — Awareness (ABO) | uncapped ABO, ~$10–16/day pace | ~$300–480 | 122,912 impr/25d, no lead action |
| **Combined current run-rate** | | **~$9,200–9,900/mo** | **~$110–119K annualized** |

**Q1 2027 allocation logic:**

1. **Google gets the growth budget first, but modestly.** LSA has shown 8 straight months of rising
   spend with flat-to-improving CPA — recommend a single step-up to the LSA weekly cap for Q1
   (roughly +15–20% over the current run-rate) rather than a large jump, and let the response set
   the pace for Q2.
2. **Recover Branded Search's lost budget share immediately** — doesn't need to wait for Q1 to
   start, but should be locked in as part of the Q1 baseline regardless. Lifting the $50/day cap to
   close the 11.3% budget-lost impression share is close to risk-free ROI.
3. **Don't fund Nonbranded Search in the Q1 baseline.** Gate it on a real negative-keyword build and
   confirmed landing page, revisit later in the year.
4. **Hold Meta lead-gen spend flat through Q1** while the geo-targeting leak and CAPI are fixed.
   This is a low-demand quarter anyway — the right time to fix the funnel before it needs to carry
   real volume in Q2.
5. **Fund the retargeting build as a Q1 project, not a Q1 media-spend line.** The audience rebuild
   and CAPI restoration are engineering/setup work this quarter; the actual retargeting ad spend can
   wait until there's a matched audience worth spending against — targeted for a Q1-end/Q2-start
   soft-launch.

**Illustrative Q1 2027 target (ratios, not commitments):**

| Month | Combined monthly target | Rationale |
|---|---|---|
| Jan 2027 | ~$9,500–10,000/mo | Hold near current run-rate; CAPI restoration work begins, no new media spend yet |
| Feb 2027 | ~$10,000–10,500/mo | Small LSA step-up lands; Branded budget lift in effect; audience rebuild in progress |
| Mar 2027 | ~$10,500–11,000/mo | LSA/Branded at new Q1 baseline; Meta still flat pending gates; retargeting soft-launch targeted for month-end if CAPI/audiences are ready |

Implied Q1 total: roughly **$30,000–31,500** across the quarter, a modest ~10–15% step-up over the
current run-rate — intentionally conservative given Q1 is DFW's lowest-demand window and the
priority this quarter is fixing structural gaps, not scaling spend.

---

## Branding & Retargeting Strategy for Q1

The account currently runs a two-stage funnel: cold Awareness video (reach only, no follow-up) and
an immediate Lead-gen ask. Q1's job is to build the missing warm middle stage while demand is
naturally low, so it's ready before the Q2 cooling ramp needs it:

1. **Cold — Awareness (existing, keep running as-is).** No change to the buy; $2.40 CPM is efficient.
2. **Warm — Retargeting (new, this is the Q1 build).**
   - Rebuild the pixel-based website-visitor custom audience (none exists today).
   - Stand up a video-viewer custom audience off the Awareness campaign's own delivery — 333K
     impressions already sitting there unused.
   - Retire the three stale 2017 lookalike audiences.
   - Restore CAPI first — without it, a value-based lookalike can't be built this quarter, only
     basic visitor/viewer audiences. The qualified-lead lookalike becomes a Q2 item once CAPI has
     been live long enough to accumulate real signal.
3. **Conversion — Lead-gen (existing, fix before scaling).** Geo-targeting fix applies in Q1; actual
   budget scaling waits for Q2 per the allocation section above.

**Target for end of Q1:** CAPI restored, two clean audiences built (site visitors, video viewers),
and — if both land on schedule — a small retargeting campaign soft-launched in March. If either
technical fix slips, hold the retargeting launch rather than force the date; this mirrors the same
discipline used elsewhere in TSD's book (don't hand a new lever dirty signal).

---

## Opportunities to Improve Qualified Lead Volume & ROI (Q1 Priorities)

1. **Fix the Meta location-targeting leak** on both active lead campaigns (22–30% of leads landing
   outside Texas) — the single highest-priority Q1 item on the Meta side.
2. **Add an Instant Form screening question** ("Do you live in [specific DFW counties]?") — a
   same-week fix, doesn't wait on the full targeting audit.
3. **Restore Conversions API** — Q1 technical prerequisite for the retargeting build and for any
   future qualified-lead signal back to Meta.
4. **Lift Branded Search's daily budget** to close the 11.3% budget-lost impression share — cheapest,
   most certain win available, should be locked in during Q1 regardless of the rest of the plan.
5. **Verify the July branded-search conversion spike** before it anchors Q1/Q2 CPA assumptions.
6. **Don't relaunch Nonbranded Search blind in Q1.** Needs a real negative-keyword list and confirmed
   landing page first — gate it to later in the year.
7. **Pursue LSA detailed-lead-reporting API access from Google** as a Q1 task — LSA is the account's
   biggest line item and currently unverifiable on quality (disputed/booked rate unknown).
8. **Lay the groundwork for a CRM/booking feedback loop** in Q1 (even if the live sync isn't built
   until Q2) — once CAPI is restored, disqualified/out-of-area/no-show leads need a path back to
   Meta so the algorithm stops optimizing toward the cheap-but-unqualified profile.

---

## Evergreen Baseline — What Runs Every Month Regardless of Season

- **Google LSA** — the primary lead engine, running year-round; Q1 sees one modest step-up.
- **Google Branded Search** — always on; budget lifted to close the impression-share gap.
- **Meta Lead-gen CBO(s)** — always on, held flat in Q1 pending the geo-targeting/CAPI fixes.
- **Meta Awareness (ABO video)** — always on, feeding the new retargeting layer once it's built.

---

## Open Items / Next Step

- [ ] AM ticket: get this Q1 preliminary plan in front of Spencer with the budget figures explicitly
      marked as illustrative — nothing here is a commitment until they sign off.
- [ ] Fix Meta location-targeting leak on both active lead campaigns (blocks any Meta budget increase).
- [ ] Restore Conversions API (blocks the retargeting build and any qualified-lead feedback loop).
- [ ] Verify the July branded-search conversion spike before it anchors Q1 CPA assumptions.
- [ ] Request LSA detailed-lead-reporting API access from Google (or arrange a manual cross-reference
      against Spencer's booking records).
- [ ] Lift Branded Search's daily budget to close the 11.3% budget-lost impression share — can
      happen now, doesn't need to wait for Q1 to start.
- [ ] Once Q1 lands and the gates above clear, extend this into a Q2–Q4 view — deliberately not
      committing to cooling-season budget numbers this far out on ~8 weeks of live Meta data.
