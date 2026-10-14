# Cool Hand Electric, Heating, & AC Repair

Mansfield & Red Oak, TX · [coolhandelectric.com](https://coolhandelectric.com) · owners **Kristen & Luke Strange** · founded 2015, 11 employees
CRM **ServiceTitan** · site **GoDaddy** · Google Ads CID `9865206319`

**Status:** existing Google Ads account (Local Services already live), 3 Search campaigns live since 2026-08-10 (Electrical/HVAC/Branded), GTM + GA4 tracking live. New to Meta and TikTok. In `contas.yaml`.

---

## What's in this folder

| File | What it is |
|---|---|
| `media-plan-aug-dec-2026.md` | **Source of truth** for the Aug–Dec 2026 client deliverable. Edit this. |
| `Cool-Hand-Electric-Media-Plan_Aug-Dec-2026.pdf` | Client-facing deliverable, 3 pages. Generated, never hand-edit. |
| `Cool-Hand-Electric-Media-Plan_Aug-Dec-2026.html` | Intermediate artifact. Generated. |
| `build_plan.py` | `python3 build_plan.py` rebuilds the HTML + PDF from the md. |
| `internal-notes.md` | **Read this before any Cool Hand work.** Scope decisions, ops items, benchmark provenance. |
| `google-ads-log.md` | Search campaign build log (Electrical/HVAC/Branded, live 2026-08-10). |
| `gtm-log.md` | GTM container review + GA4 tag build log (live 2026-08-10). |

---

## 2026-08-05 — Aug–Dec 2026 media plan built

**Why.** New media plan request. Built across Google Ads (Search) and Meta, with TikTok modeled as an optional awareness-only add-on per Edu's direction mid-build.

**Channel architecture revised mid-build (Edu, same session):** Google Ads carries the majority of budget and lead-gen (Search direct-response + a smaller YouTube awareness carve-out inside the same Google Ads spend). Meta scaled down to a low always-on baseline most months, concentrated into two seasonal-offer bursts (September "Beat the Heat," December holiday panel-safety) rather than flat spend across all five months. Five-month average: **Google Ads (Search + YouTube) 81% · Meta 19%.**

**What we found before writing anything.** Pulled the account's real Google Ads data first rather than starting from benchmarks — this is **not** a blank-slate account. Customer `9865206319` already runs a live, auto-generated Google Local Services (LSA) campaign: **47 leads / $3,506.22 / $74.60 CPL over the last 30 days**, ramped steadily since late May, running well under its own $214/day budget cap. **Edu's call: TSD is not managing this LSA campaign right now** — it's excluded from this plan's scope and budget, kept as context only in `internal-notes.md` so nobody double-counts its leads against this plan's targets.

**Format.** Follows the Gillespie's Heating and Cooling / Lilypad Septic precedent: plain black-and-white document styling, not the navy/gold TSD report template. Ratio-based rather than fixed dollars (intake literally says "No ads budget"), with dollar scenarios modeled at $3.5k / $5k / $7.5k per month.

**Structure.** Five-month arc matching the real seasonal shift in North Texas: peak AC repair (Aug) → AC tail/early replacement (Sep) → heating transition (Oct) → heating emergency (Nov) → holiday electrical/panel-upgrade (Dec). Google Search leads in the two AC months and November's cold-snap spike (active-search events); Meta's share climbs through October and peaks in December (electrical-safety and panel-upgrade demand has to be built, not just answered). Five-month average: **Google Search 60% · Meta 40%.**

**Scope cuts from the client PDF** (Edu, this session): the LSA context/numbers, the plumbing-scope ambiguity, the hours conflict (24/7 advertised vs. Mon–Fri 8–5 on file), and full benchmark provenance. All preserved in `internal-notes.md`.

**Real data used, not assumptions:**
- Google Ads Search CPC ranges pulled live via Keyword Planner, **Texas geo (constant 21176)**, 2026-08-05 — not national averages.
- Meta CPL is the same LocaliQ Home & Home Improvement benchmark used across other TSD plans ($30–50) — no Cool Hand-specific Meta data exists yet, net-new build.

**Open items (all in `internal-notes.md`):**
- [ ] Confirm with AM/client whether **plumbing** should be in paid scope — the intake has a full plumbing service catalog, but "Top Marketing Services," the business name, and the competitor set all point to HVAC + Electrical only. This plan excludes plumbing.
- [ ] Resolve the **24/7 emergency vs. Mon–Fri 8–5** hours conflict before any campaign runs emergency-intent terms or off-hours dayparts.
- [x] ~~No GA4, pixel, GTM, or call tracking provider on file~~ — GTM (`GTM-KWZDRBVQ`) + GA4 (`G-ZHH3FSDC4J`) live as of 2026-08-10. Meta pixel and TikTok Pixel/Events API still not built — needed before spend on those channels. See `gtm-log.md`.
- [ ] Confirm which Google LSA categories are currently approved, if/when LSA ever comes into TSD's scope.
- [x] ~~If they move forward: add to `contas.yaml`, start `google-ads-log.md`~~ — done 2026-08-10. `meta-ads-log.md` still not started (no Meta build yet).
