# Lilypad Septic Company

Salina & Hutchinson, KS · [lilypadseptic.com](https://lilypadseptic.com) · owner **Cole Leister** (wife Calle co-owns) · founded 2016, 13 employees
CRM **ServiceTitan** · site **WordPress** · registrar GoDaddy

**Status: prospect.** Not in `contas.yaml`. No Google Ads CID, no LSA account, no Meta ad account, no GA4, no pixel, no GTM, no call tracking provider on file. Tracking is a blank slate, so any launch is a full build rather than a takeover.

---

## What's in this folder

| File | What it is |
|---|---|
| `media-plan-aug-sep-2026.md` | **Source of truth** for the Aug–Sep interim plan. Edit this. |
| `Lilypad-Septic-Media-Plan_Aug-Sep-2026.pdf` | Client-facing deliverable, 2 pages. Generated, never hand-edit. |
| `build_plan_augsep.py` | `python3 build_plan_augsep.py` rebuilds the Aug–Sep HTML + PDF. |
| `media-plan-q4-2026.md` | **Source of truth** for the Q4 client deliverable. Edit this. |
| `Lilypad-Septic-Media-Plan_Q4-2026.pdf` | Client-facing deliverable, 3 pages. Generated, never hand-edit. |
| `Lilypad-Septic-Media-Plan_Q4-2026.html` | Intermediate artifact. Generated. |
| `build_plan.py` | `python3 build_plan.py` rebuilds HTML + PDF from the md. |
| `internal-notes.md` | **Read this before any Lilypad work.** Pre-launch gates, ops items, benchmark provenance, competitive read. |

---

## 2026-07-31 — Aug–Sep 2026 interim plan built

**Why.** AM asked for a plan to launch now rather than wait for October. The Q4 plan could not just be re-dated: Aug–Sep is the **restroom half** of the counter-cyclical year, so a septic-weighted plan would have put 45% of budget on LSA during the quietest septic months while the live revenue line got nothing.

**What changed vs Q4.** Google Ads leads at 45% both months (install terms for the fall dig + restroom/trailer rental terms). LSA drops 45% → 27% average, baseline role only, since it has no category for restroom rental. Meta rises 18% → 28% and repoints from the Flush Family Plan to rentals. Kansas State Fair added as the September anchor. Q4 runs unchanged from October.

**Kept from Q4.** The install push. Installs run 2–5 months to dig and the window closes ~October, so Aug–Sep install spend is what fills the fall dig calendar. Deferring it to Q4 pushes those digs to spring.

**Still open (same gates as Q4, none cleared).** LSA eligibility for 67401/67501 under "Sewage system", GBP review count, Keyword Planner scoped to Saline/Reno, budget sign-off, hours conflict. Plus: the Oct–Apr / May–Sep seasonality split is **still an assumption** and this plan's whole shape rests on it — the ask for 2–3 years of job tickets by month and service line is now load-bearing, not nice-to-have. Tracking is still a blank slate, so the realistic launch date is set by the build, not by the plan.

## 2026-07-20 — Q4 2026 media plan built

**What we did.** Built a Q4 (Oct–Dec 2026) quarterly media plan across Google LSA, Google Ads Search, and Meta. Format follows the Gillespie's Heating and Cooling media plan precedent: plain black-and-white document styling, not the navy/gold TSD report template. Structured on **channel ratios rather than fixed dollars** (Edu's call) because no budget has been set, with dollar scenarios modeled at $2k / $3k / $5k per month.

**What we found.**
- **Google runs "Sewage system" as a standalone LSA category**, separate from Plumbers and Drain expert. Lilypad qualifies on its actual trade rather than riding under a plumbing listing. LSA at $30–60 CPL beats a $129 plumbing search CPL and outranks the national lead-resale sites that dominate these SERPs, which cannot obtain the Google Guarantee badge.
- **Not a general plumber.** Their site sells no water heaters, repiping or fixtures, so plumbing was excluded from scope per Edu's condition. Septic, drain/sewer, grease traps, portable sanitation.
- **Two counter-cyclical business lines.** Septic carries Oct–Apr, portable restrooms carry May–Sept (1,000+ units/month, plus luxury trailers). Budget should rotate between lines rather than scale the account as a whole. Kansas State Fair in Hutchinson is a September anchor.
- **Two markets, not one.** Salina and Hutchinson are 66 driving miles apart (~75 min). Separate campaigns, geo, and tracking numbers. Never average their performance.
- **Meta deliberately de-weighted to 18%.** Septic demand runs on a 3–5 year alarm-triggered cycle and goes to Google. Meta funds restroom bookings, brand familiarity, and the Flush Family Plan against the existing list.
- **Zero Kansas-local septic or porta-potty advertisers in the Meta Ad Library.** Uncontested channel.

**Deliberate omissions from the client PDF** (Edu, this session): the Operational Guidelines section, the "(Confidential)" footer marker, and the closing "to be confirmed before launch" line. All the operational content was preserved in `internal-notes.md`. **Consequence: the PDF now presents the plan without the caveats behind its own numbers.** Do not treat it as the full picture.

**Open items.** SEO/brand consolidation is already handled by that division (hutchseptic.com redirects) and is out of paid's lane. Everything else is in `internal-notes.md`; the three that gate a launch:

- [ ] Run ZIP **67401** and **67501** through Google's LSA eligibility tool with **"Sewage system"** selected. Gates the primary channel recommendation, which carries 45% of quarterly budget.
- [ ] Pull the real **Google Business Profile rating and review count**. LSA rank is review-weighted and this is unverified.
- [ ] **Keyword Planner scoped to Saline and Reno counties.** In a 46k/40k market the binding constraint is search volume, not click price. This number should set the budget.
- [ ] Confirm budget with Cole / the AM, plus the hours conflict (24/7 advertised vs Mon–Fri 8–5 on file), real drive-time service limits, and which phone number belongs to which market.
- [ ] If they convert: add to `contas.yaml`, move up to the Clients list in `clients/README.md`, start `google-ads-log.md` and `meta-ads-log.md`.
