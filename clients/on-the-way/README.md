# On The Way AC Plumbing & Electric

**Status:** live client. Google Ads customer ID `3454686129`, in `contas.yaml`, linked under the TSD MCC.
**Work to date:** 14 video scripts across all 7 services (V1 + V2), a Jul–Sep 2026 quarterly media plan, and a Phase 1 Search build (2026-09-09): Branded + 3 non-branded ad groups (AC-Repair, Plumbing-Emergency, Electrical), all PAUSED. See `google-ads-log.md` and `google-ads-search-launch-brief.md`.
**Last updated:** 2026-09-09

---

## Client snapshot

| | |
|---|---|
| **Site** | onthewaypros.com |
| **Phone** | (409) 310-1464 |
| **Based** | 2513 FM 646 Rd, Santa Fe, TX 77510 (Galveston County) |
| **Hours** | Mon–Sun 8am–6pm, 24/7 emergency |
| **Owner name** | **Unknown.** No about page on their site. |

**Service area (16 cities):** Santa Fe, League City, Friendswood, Dickinson, Texas City, Galveston, Alvin, Webster, Manvel, La Marque, Kemah, Seabrook, Bacliff, Hitchcock, Clear Lake, South Houston.

**Services:** AC/HVAC · Plumbing · Electrical · Roofing · Insulation · Generators · Energy audits.

**Positioning:** three active state licenses, one call covers every system. Call-driven, same-day, 24/7. GoodLeap financing across the board.

**Licenses:** TACLA914 (AC) · RMP43535 (plumbing) · TECL34051 (electrical).
Texas does **not** license roofers, so no roofing license exists to claim. Their site says "fully licensed and insured roofing contractor" but the numbers above are the three trades. Scripts deliberately avoid implying a roofing license.

### The biggest asset: "Licensed, local since 1976"

Found on their roofing page. **Fifty years in Santa Fe as of 2026.** On the Gulf Coast, where every hurricane brings a wave of out-of-state storm chasers, this is the most valuable thing the company owns and nothing else on the site is close. It currently appears on the roofing page only — worth using across every service.

### Per-service detail (all from their own site)

**AC/HVAC** — repair, maintenance, replacement, heating (furnace, heat pump, full installs). Residential + commercial.

**Plumbing** — tank & tankless water heaters, "same day" diagnose and repair · drain cleaning · sewer line repair with **camera inspection included** · repiping (galvanized/polybutylene/corroded → copper or PEX) · **electronic slab leak detection "without unnecessary demolition"** · emergency 24/7 (burst pipes, sewer backups, gas leaks) · "upfront pricing, no surprises" · free estimate.

**Electrical** — 200A panel upgrades **"with full permits and inspections"** · recessed/landscape/security lighting · outlets (two-prong → grounded, USB) · repairs (tripping breakers, dead outlets, flickering) · whole-home rewiring · EV charger (Level 2, 240V) · generators. Residential + commercial.

**Roofing** — repair, storm & hail · **emergency tarping** · full replacement with **Owens Corning Duration (SureNail) & GAF Timberline HDZ, both rated to 130 MPH** · **free roof inspections** · full storm damage documentation for insurance · flat/low-slope (TPO, EPDM, mod bit) · metal. Residential + commercial. Site references **Hurricane Harvey** by name.

**Insulation** — blown-in fiberglass only, **Owens Corning AttiCat Pink** · **"Owens Corning AttiCat Certified Installer"** · installed R-38 to R-49, stated target **R-38 to R-60 for the Texas Gulf Coast climate zone** · free attic assessments · most homes same day · site knocks batt for gapping and compressing · claims "up to 20%" bill reduction (deliberately unused in scripts). **Residential only.**

**Generators** — **Generac Authorized Dealer** (only brand) · whole-home standby · automatic transfer switch included with every install · **"starts automatically within 10 seconds"** · natural gas or propane, runs on existing gas line, no refueling · **weekly automatic self-test** · all permits, inspections & gas line hookup handled · most installs one day · 10–13kW covers essentials, 20–22kW whole-house · free in-home consultation. **Residential only.**

**Energy audits** — lives at `/energy-efficiency/` (**`/energy-audit/` 404s**). Inspects attic R-value, air leaks, HVAC, ductwork (**"ducts can waste 20-30% of conditioned air"**), and **window & door SEALS — weatherstripping, not replacement**. Deliverable: written report with prioritized recommendations ranked by impact and cost. **THE ONLY PAID ITEM** — "costs depend on home size and scope," no number given. Differentiator: unlike standalone audit companies they do the follow-up work themselves. **They do NOT sell windows** (verified: absent from nav and services). **Residential only.**

---

## Account status

**Not in the TSD book.** Checked 2026-07-16:
- No prior folder, and no mention of the name anywhere under `~/Documents`.
- **Google Ads:** no match across all 124 child accounts under the Topservdigital MCC (`4155514468`), searched by name and by city.
- **Meta:** no match across the first 100 ad accounts visible via the connector. Not exhaustive — the third page errored.
- **Not in `contas.yaml`** (correctly — no customer ID exists yet).

One loose end worth ruling out: a Meta account named just **"Gulf Coast"** (`918721531652701`) sits under the Topservdigital business, currently UNSETTLED and not queryable. Galveston County is Gulf Coast Texas, so it's a plausible alias. Pure geography-based guess.

**When they become real:** add to `contas.yaml`, add to `clients/README.md` account list, and start `google-ads-log.md` / `meta-ads-log.md` per the folder convention.

---

## Files in this folder

| File | What it is |
|---|---|
| `OTW - Script & Instructions.pdf` | **The shoot doc. Current V2.** 16pp. Every beat with its shot, the line, on-screen text, end card, production notes, verification flags. This is what a videographer works from. |
| `OTW - Script Only.pdf` | **Current V2.** 7pp. Spoken copy only, for reading and review. |
| `video-scripts-v2.md` | **Content source of truth.** All 14 scripts, shot direction, production notes, open items, plus a full changelog of what V2 changed from V1 and why. |
| `video-scripts.md` | **V1, preserved.** Do not overwrite. Kept for comparison. |
| `On-The-Way-Video-Scripts_2026-07-16.pdf` | V1 scripts-only. Superseded, kept for comparison. |
| `*.html` | Sources for each PDF, same basename. Edit the HTML, re-render, don't hand-edit PDFs. |
| `media-plan-jul-sep-2026.md` | Quarterly media plan, Jul–Sep 2026. $9k/mo recommended, brandformance split (~85% conversion / ~15% awareness growing to ~18% by Sep) across Google LSA + Google Ads + Meta. Written 2026-09-08. |

**Styling:** the two current V2 PDFs are deliberately **plain** — Times New Roman 12pt, 1in margins, black on white, like a Word document. An earlier navy/gold designed version existed and is recoverable (it's only CSS; the copy lives in the markdown) if a client-facing handoff ever wants it.

**Rebuilding a PDF:**
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=out.pdf in.html
```
Letter via `@page { size: Letter; margin: 0 }` + `print-color-adjust: exact`. Navy `#12305a` / gold `#c9a24b` (placeholder — no official TSD brand assets in the workspace).

---

## The 14 scripts

Two per service. While the owner-on-camera question is open, each pair is one owner-on-camera and one VO-over-b-roll so both shapes can be compared.

| # | Service | Title | Angle | Shape | Runtime |
|---|---|---|---|---|---|
| 01 | AC/HVAC | Thursday | The wait, not the breakdown | Owner | ~42s |
| 02 | AC/HVAC | Pointing fingers | Three licenses, no referral runaround | VO | ~37s |
| 03 | Plumbing | Standing in the shower | Water heater, same day. Volume play | Owner | ~39s |
| 04 | Plumbing | The warm spot | Slab leak, fear of demolition | VO | ~42s |
| 05 | Electrical | The one that doesn't work | The problems people live with | Owner | ~34s |
| 06 | Electrical | The boring way | Permits | VO | ~36s |
| 07 | Roofing | Since 1976 | Storm chaser contrast | Owner | ~40s |
| 08 | Roofing | Either way you stop wondering | Free inspection vs insurance dread | VO | ~35s |
| 09 | Insulation | Maybe | The anti-upsell | Owner | ~40s |
| 10 | Insulation | If you can see the wood | A test the viewer will fail | VO | ~35s |
| 11 | Generators | Nobody looks up | The portable you already own | VO | ~41s |
| 12 | Generators | There's no list | Sells the calendar, not the machine | Owner | ~40s |
| 13 | Energy audits | Nothing sounds wrong | Ductwork. Delivery, not the barrier | VO | ~41s |
| 14 | Energy audits | We don't sell windows | Names his own conflict of interest | Owner | ~34s |

**Standing parameters:** videographer on location (never self-recorded unless Edu says so) · **45s hard cap** · CTA on every script is "Tap Learn More and talk to us right now" · Meta, so no phone number on end cards · natural and organic voice, never textbook English.

---

## Open items — blocking first

**These two gate everything and get more expensive the longer they sit:**

- [ ] **Does the owner go on camera, and what's his name?** No about page, so no name available. **7 of 14 scripts are built around him being a real face** and collapse to VO rebuilds if he'd rather not. Settling this also ends the two-shapes-per-service hedge.
- [ ] **Where does Learn More go?** "Talk to us right now" is a promise with a clock on it. Click-to-call or click-to-Messenger keeps it honest; a landing page only works if someone genuinely answers during ad hours. Script 2 spends 37 seconds mocking companies that don't keep this promise, so a slow destination breaks it from the inside.

**Client questions:**

- [ ] **The audit is the only paid item in all 14 scripts.** Everything else attaches to something free (roof inspection, attic assessment, generator consult). So Scripts 13 & 14 are the only ones where the CTA leads to a price conversation instead of a truck. Real friction on Meta. Ask: fixed number for the ad, or make it free and let it feed the insulation/AC replacement work it's designed to feed? Their own page says it "pays for itself many times over," which argues for free.
- [ ] **Script 7 — can he name storms?** Site only supports "local since 1976." If the business worked through Alicia ('83), Ike ('08), Harvey ('17), swap Beat 3 for the named-storm variant, which is far stronger for this audience. **Smaller ask than it looks: their generator page already references Harvey by name.** Do not shoot unverified.
- [ ] **Script 7 — does anything from 1976 physically exist?** Original sign, founder photo, old truck, framed first license. Highest-value asset on the entire shoot and it can't be recovered later. **Ask before the shoot day, not on it.**
- [ ] **Script 4 — verify the leak detection method.** Written as listening through the slab with a ground mic. Site only says "electronic leak detection." If their techs use something that looks different on camera, a load-bearing beat falls apart on the day.
- [ ] **Script 6 — two client checks.** The adjuster line gestures at insurance trouble from unpermitted work (hedged as a question, not a denial claim). And "It costs more than a Saturday" openly admits they're not the cheap option, which is what buys credibility for the rest. Some owners hate seeing that in their own ad.

**Production:**

- [ ] **This is NOT a one-day shoot.** Beats that can't be staged or recovered if the day is sequenced wrong: **S10 Beat 2** (must shoot the attic *before* the crew touches it — the match cut to Beat 5 is the whole ad) · **S4** (needs a real slab leak to exist) · **S13 Beat 2** (needs a real disconnected duct) · **S9 Beat 3** (thermometer reads whatever it actually reads). Several need capturing on real jobs as they come up. Raise with the videographer before a date locks.
- [ ] **Script 12 is the only season-bound one** (hurricane season, June–November). If anything shoots first, that.

**Media planning:**

- [ ] **Don't run all 14 at once.** Per [[tsd-meta-ads-methodology]], 14 scripts = 14 angles = 14 DCT ad sets. The second-person callout hooks are correct individually, but a feed seeing three at once will read the sameness. Pick a starting slate.

---

## Notes on approach

Three patterns produced the good scripts, worth repeating on the next client:

1. **The best angles all came from their own site saying something specific.** Batt gaps and compresses → "if you can see the wood, you don't have enough." Starts in 10 seconds → the kitchen where nobody looks up. Ducts waste 20-30% → a hand in front of a loose duct.
2. **Every percentage claim they offered was skipped** ("up to 20%" off bills, "15-30% more than you need to"). Concrete beats a number nobody believes. A thermometer reading 140 proves more than a statistic.
3. **The strongest lines are all sub-promises.** "Maybe. We sell those too." · "If there's nothing, we tell you there's nothing and we leave." · "We do it the boring way." · "It costs more than a Saturday."

**Deliberately not used:** their own "Galveston County's only full-service home contractor" line. Superlatives invite disproof and the provable version (three licenses, one truck, since 1976) is stronger anyway.
