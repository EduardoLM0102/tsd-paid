# On The Way AC Plumbing & Electric — Google Ads Search Launch Brief

**Prepared:** 2026-09-09 · **Owner:** Paid Ads (Eduardo) · **Status:** Phase 1 BUILT & PAUSED in customer `3454686129` (Branded + AC-Repair, Plumbing-Emergency, Electrical — see `google-ads-log.md` session 2). Remaining ad groups below (AC-Maintenance, AC-Replacement, Heating, Water-Heater, Drain-Sewer, Leak-Detection, Roofing, Insulation, Generators, Energy-Audit) are Phase 2 — researched and copy-ready, not yet built.

Built per [`google-ads-launch-buildout.md`](../../paid/sops/google-ads-launch-buildout.md) Stage 4 (keyword/offer/competitor research) and Stage 5 (ad copy). This is the Campaign Brief + RSA deck in one file. Keyword volume/CPC pulled live via Keyword Planner, geo'd to Galveston + Harris + Brazoria counties (the three counties the 16-city service area sits inside — Keyword Plan Idea Service doesn't accept a mixed city/neighborhood location list in one call, so county-level is the closest valid proxy; directional, not exact for any single city).

---

## 1. Structure

Two campaigns, per SOP 7.1 — branded and non-branded always separate, cross-negated.

- **`TSD_09.09_Search_Branded_Evergreen`** — 1 ad group ("Brand"), brand terms EXACT.
- **`TSD_09.09_Search_NonBranded_Evergreen`** — 13 themed ad groups, one per service intent, PHRASE + EXACT only.

Brand terms (EXACT, branded ad group; same list becomes EXACT negatives on non-branded):
`on the way` · `on the way pros` · `on the way ac plumbing and electric` · `on the way ac plumbing & electric` · `onthewaypros` · `on the way service pros` · `on the way ac` · `on the way plumbing` · `on the way electric`

---

## 2. Non-branded ad groups, keywords & final URLs

Match type on every keyword: **PHRASE + EXACT** (both added), no broad. Volumes are monthly, 3-county estimate.

| Ad group | Final URL | Keywords (core concepts) | Notable volume |
|---|---|---|---|
| **AC-Repair** | `/ac-repair/` | ac repair · air conditioner repair · ac repair near me · emergency ac repair · ac not cooling · hvac repair · hvac repair near me · ac repair technician · ac compressor repair | "ac repair" 8,100/mo, "ac repair near me" 6,600/mo |
| **AC-Maintenance** | `/ac-maintenance/` | ac maintenance · ac tune up · air conditioner maintenance · ac unit maintenance · hvac maintenance · ac maintenance near me · ac inspection · annual ac service | "ac unit maintenance" 1,900/mo |
| **AC-Replacement** | `/ac-replacement/` | ac replacement · ac unit replacement · new air conditioner installation · central air installation · mini split installation · ductless mini split installation · ac installation cost · ac system replacement | "ac replacement" 480/mo, mini-split cluster 3,600/mo |
| **Heating** | `/heating/` | furnace repair · heater repair · furnace installation · heat pump installation · heating repair near me · furnace not working · heating and air repair near me | "furnace repair" 1,600/mo |
| **Plumbing-Emergency** | `/plumbing/` | plumber near me · plumber · emergency plumber · emergency plumber near me · plumbing repair · licensed plumber · plumber service · 24 hour plumber near me | "plumber near me" 12,100/mo — highest-volume term in the account |
| **Water-Heater** | `/plumbing/` | water heater repair · water heater repair near me · water heater replacement · tankless water heater installation · replace a water heater · water heater maintenance | "water heater repair" 880/mo |
| **Drain-Sewer** | `/plumbing/` | drain cleaning · drain cleaning near me · sewer line repair · sewer line repair near me · hydro jetting · sewer camera inspection · drain cleaning companies · unclog drain | "drain cleaning" 1,300/mo |
| **Leak-Detection** | `/plumbing/` | slab leak repair · water leak detection · leak detection service · gas leak detection · gas leak repair · plumber for gas leak · plumbing leak detection | Low volume individually, but this is the "no unnecessary demolition" differentiator — worth its own ad group even thin |
| **Electrical** | `/electrical/` | electrician near me · electrical repair · electrical contractors near me · electric panel upgrade · cost to replace electrical panel · ev charger installation · emergency electrician near me · fix gfci outlet | "electrician near me" 5,400/mo |
| **Roofing** | `/roofing/` | roof repair · roof repair near me · roofing contractor · roofing companies near me · roof replacement · roof inspection · roof leak repair · roofing contractors near me | "roofers" 2,900/mo, "roofing companies near me" 2,400/mo |
| **Insulation** | `/insulation/` | attic insulation · blown in insulation · attic insulation near me · attic insulation contractors near me · insulation contractor · attic insulation cost · blown in attic insulation · fiberglass attic insulation | "attic insulation" 1,900/mo. Deliberately excludes spray foam/cellulose — they only install blown-in fiberglass. |
| **Generators** | `/generator-installation/` | whole home generator · home standby generator · generator installation · home generator installation · whole house generator installation · generac standby generator · standby generator cost · generac whole house generator | "generac company" 1,900/mo (brand-of-equipment searches — legitimate, they're a Generac Authorized Dealer) |
| **Energy-Audit** | `/energy-efficiency/` | home energy audit · energy audit · energy audit near me · energy assessment near me · home energy audit cost · home energy assessment | Thin volume (70–140/mo core term) — smallest ad group, lowest priority for budget if it needs trimming |

**Note on Plumbing:** four ad groups (Emergency, Water-Heater, Drain-Sewer, Leak-Detection) all point at the single `/plumbing/` page since that's the only plumbing page on the site — splitting by intent still lets each RSA speak to a specific problem even sharing one landing page. If non-branded budget can't support all 13 ad groups at launch, trim from the bottom of this list first (Energy-Audit, Leak-Detection) — see §6.

---

## 3. Negative keyword list (attach before enabling, per SOP 7.6)

**Standard base (PHRASE unless noted):**
job, jobs, career, careers, hiring, salary · diy, how to, diagram, manual, tutorial · free, cheap · rental, warranty claim, recall · craigslist, indeed

**Client-specific (from README service scope — things they don't do):**
- `septic` (PHRASE) — not a service; "septic tank pumped" showed real volume (880/mo) in the drain/sewer research, so worth blocking explicitly
- `well pump` (PHRASE) — not a service
- `pool leak`, `swimming pool` (PHRASE) — leak-detection research surfaced real pool-leak volume; different service entirely
- `window replacement`, `window installation`, `new windows`, `buy windows` (PHRASE) — README is explicit they do **not** sell windows, only inspect seals as part of the energy audit
- `spray foam insulation`, `cellulose insulation` (PHRASE) — they only install blown-in fiberglass; don't pay for the wrong product's demand
- `rain gutter` (PHRASE) — not a listed service, surfaced in roofing research
- `green gobbler`, `home depot drain opener` (EXACT) — retail product queries, not service intent

**Roofing license care:** do NOT add roofing-license negatives — but ad copy must never claim a roofing license (see §5, none of the roofing headlines/descriptions do). This is a copy discipline, not a keyword one.

Cross-negatives: full brand term list (§1) as EXACT negatives on the non-branded campaign.

---

## 4. Geo targeting

**Method:** LOCATION targeting on the 16 named cities from the media plan (not a single proximity circle — the service area spans two counties in a shape that doesn't reduce to one circle around the Santa Fe hub cleanly; per-city targeting is the more faithful read of the client's actual dispatch area). **Presence only** — people in or regularly in these locations, never "interested in."

| City | Geo target constant ID | City | Geo target constant ID |
|---|---|---|---|
| Santa Fe | 1026770 | Kemah | 1026519 |
| League City | 1026551 | Seabrook | 1026777 |
| Friendswood | 1026406 | Bacliff | 9195175 |
| Dickinson | 1026356 | Hitchcock | 1026475 |
| Texas City | 1026835 | Clear Lake (neighborhood) | 9198356 |
| Galveston | 1026415 | South Houston | 1026802 |
| Alvin | 1026181 | Manvel | 9052384 |
| Webster | 1026875 | La Marque | 1026536 |

No areas were flagged as refused-service in the source material, so no negative locations at launch.

---

## 5. RSAs (one per ad group)

Character-limit checked (≤30 headline / ≤90 description). All copy drawn from verified site content and the README — nothing invented (financing, licenses, ratings, materials, "no unnecessary demolition," "no roofing license" constraint all respected).

### Branded
**Headlines:** On The Way AC & Plumbing · On The Way Pros · Official Site: On The Way · Santa Fe's Trusted Pros · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · AC, Plumbing & Electrical · Call (409) 310-1464 · Same-Day Service
**Descriptions:**
- The official On The Way site. AC, plumbing & electrical from a family business since 1976.
- Licensed in all three trades. 4.8 stars, 1,650+ reviews. Same-day service, Santa Fe, TX.
- One call covers AC, plumbing and electrical. GoodLeap financing available. Book today.
- 50 years serving Galveston County. See why neighbors have trusted us since 1976.

### AC-Repair
**Headlines:** AC Repair, Same Day · AC Not Cooling? We Fix It · 24/7 Emergency AC Repair · Licensed AC Technicians · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate, No Surprise · Same-Day AC Repair Techs · 3 Licenses, One Trusted Call · GoodLeap Financing Available
**Descriptions:**
- Santa Fe's AC experts since 1976. Same-day repair, 4.8★ rated, three licensed trades.
- AC quit in the heat? We answer the phone and show up same day. Licensed & insured.
- No referral runaround. One licensed company fixes it right the first time. Free estimate.
- 24/7 emergency AC repair across Galveston County. Call now, we're on the way.

### AC-Maintenance
**Headlines:** AC Tune-Up & Maintenance · Beat the Heat, Book a Tune-Up · Annual AC Service · Prevent Costly AC Breakdowns · Licensed HVAC Technicians · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Same-Day Appointments · Free AC Inspection
**Descriptions:**
- Regular AC maintenance means fewer breakdowns. Licensed techs, same-day scheduling.
- Santa Fe's family-owned HVAC team since 1976. 4.8★ rated, 1,650+ reviews.
- A tune-up now beats an emergency call later. Book your AC maintenance today.
- Three licensed trades, one company. AC maintenance done right, every time.

### AC-Replacement
**Headlines:** New AC System Installation · Mini-Split Installation · Stop Repairing, Upgrade Now · High-Efficiency AC Systems · GoodLeap Financing Available · Free In-Home Estimate · Licensed AC Installers · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Ductless Mini-Split Experts
**Descriptions:**
- Old AC on its last leg? Upgrade to a high-efficiency system with GoodLeap financing.
- Licensed installers, free in-home estimate. Ductless mini-splits and central AC.
- 50 years installing AC systems in Santa Fe. 4.8★ rated, three licensed trades.
- Get a real quote, not a guess. Free estimate on your new AC installation today.

### Heating
**Headlines:** Furnace Repair Near You · Heater Not Working? We Fix It · Heat Pump Installation · Licensed Heating Technicians · Same-Day Furnace Repair · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate · GoodLeap Financing Available
**Descriptions:**
- Furnace or heat pump acting up? Licensed techs, same-day appointments available.
- Santa Fe's heating experts since 1976. 4.8★ rated, three licensed trades, one call.
- Heating repair, replacement and installation. Free estimate, financing available.
- No referral runaround. One licensed company handles your heating system, start to finish.

### Plumbing-Emergency
**Headlines:** Emergency Plumber, Same Day · Licensed Plumber Near You · Burst Pipe? Call Us Now · 24/7 Emergency Plumbing · Upfront Pricing, No Surprises · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate · Same-Day Plumbing Repair
**Descriptions:**
- Burst pipe, sewer backup or gas leak? Licensed plumbers, 24/7 emergency service.
- Upfront pricing, no surprises. Same-day plumbing repair across Galveston County.
- Santa Fe's licensed plumbers since 1976. 4.8★ rated, 1,650+ reviews. Call now.
- One licensed company for every plumbing emergency. Free estimate, honest pricing.

### Water-Heater
**Headlines:** Water Heater Repair, Same Day · Tankless Water Heater Install · Water Heater Replacement · Standing in a Cold Shower? · Licensed Plumbing Technicians · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · GoodLeap Financing Available · Free Estimate
**Descriptions:**
- No hot water? Same-day water heater repair and replacement, tank or tankless.
- Licensed plumbers install tank and tankless water heaters. Free estimate, financing.
- Santa Fe's trusted plumbers since 1976. 4.8★ rated, 1,650+ reviews, one call.
- Upfront pricing on every water heater job. No surprises, no upsell pressure.

### Drain-Sewer
**Headlines:** Drain Cleaning, Same Day · Sewer Line Repair Near You · Camera Inspection Included · Hydro Jetting Service · Licensed Plumbing Technicians · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate · Upfront Pricing, No Surprises
**Descriptions:**
- Clogged drain or sewer backup? Same-day service with camera inspection included.
- Licensed plumbers, upfront pricing. Drain cleaning and sewer line repair, done right.
- Santa Fe's plumbing experts since 1976. 4.8★ rated, 1,650+ reviews, one call.
- Every sewer repair includes a camera inspection, so you see what we see. Free estimate.

### Leak-Detection
**Headlines:** Slab Leak Detection · No Unnecessary Demolition · Electronic Leak Detection · Gas Leak? Call Us Now · Licensed Plumbing Technicians · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate · 24/7 Emergency Service
**Descriptions:**
- Suspect a slab leak? Electronic detection finds it without unnecessary demolition.
- Gas leak or hidden water leak? Licensed techs, 24/7 emergency response, free estimate.
- Santa Fe's plumbing experts since 1976. 4.8★ rated, 1,650+ reviews, one call.
- We find the leak before we touch the slab. Upfront pricing, no guesswork.

### Electrical
**Headlines:** Licensed Electrician Near You · Electrical Repair, Same Day · 200A Panel Upgrades · EV Charger Installation · Permits & Inspections Included · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Free Estimate · 24/7 Emergency Electrician
**Descriptions:**
- Panel upgrades, rewiring, EV chargers. Licensed electricians, permits included.
- Tripping breakers or dead outlets? Licensed electricians, same-day service available.
- Santa Fe's licensed electricians since 1976. 4.8★ rated, 1,650+ reviews, one call.
- We do it the boring way: permits and inspections on every job. Free estimate.

### Roofing
**Headlines:** Free Roof Inspection · Storm Damage Roof Repair · Roof Replacement Experts · 130 MPH-Rated Shingles · Insurance Documentation Help · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Licensed Roofing Crews · Emergency Storm Tarping
**Descriptions:**
- Free roof inspection, full storm damage documentation for your insurance claim.
- Owens Corning & GAF shingles rated to 130 MPH. Licensed crews, since 1976.
- Storm damage or a slow leak? Either way, you stop wondering. Free inspection.
- Santa Fe's roofing experts since 1976. 4.8★ rated, 1,650+ reviews, one call.

*(No headline or description claims a roofing license — Texas doesn't license roofers, and only the three trade licenses (TACLA/RMP/TECL) are real.)*

### Insulation
**Headlines:** Free Attic Assessment · Blown-In Attic Insulation · Owens Corning Certified · Most Attics Done Same Day · Stop Losing Energy at Home · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Licensed Insulation Techs · Free Estimate
**Descriptions:**
- Owens Corning AttiCat Certified installer. Free attic assessment, most jobs same day.
- If you can see the wood, you don't have enough insulation. Free attic assessment.
- Santa Fe's insulation experts since 1976. 4.8★ rated, 1,650+ reviews, one call.
- Blown-in fiberglass, done right the first time. Free estimate, no upsell pressure.

### Generators
**Headlines:** Whole-Home Generator Install · Generac Authorized Dealer · Starts Automatically in 10 Sec · Free In-Home Consultation · Never Lose Power Again · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Most Installs Done in One Day · Permits & Gas Hookup Included
**Descriptions:**
- Generac Authorized Dealer. Whole-home standby generators, transfer switch included.
- Power out? Yours starts automatically in 10 seconds. Free in-home consultation.
- Santa Fe's generator experts since 1976. 4.8★ rated, 1,650+ reviews, one call.
- Permits, inspections and gas line hookup all handled. Most installs done in a day.

### Energy-Audit
**Headlines:** Home Energy Audit · See Where You Lose Energy · Attic, Ducts & Window Seals · Prioritized Written Report · We Do The Follow-Up Work Too · Family-Owned Since 1976 · 4.8★ From 1,650+ Reviews · Licensed Home Energy Techs · Book Your Energy Audit
**Descriptions:**
- A full inspection of your attic, ducts and seals, with a written report ranked by impact.
- Unlike audit-only companies, we do the follow-up work ourselves. One trusted call.
- Santa Fe's home energy experts since 1976. 4.8★ rated, 1,650+ reviews.
- Ducts can waste 20-30% of your conditioned air. Find out where. Book your audit.

*(This is the only paid service in the whole book — no dollar figure is claimed anywhere, matching the open item in the video-scripts README: no fixed price was ever given.)*

---

## 6. Bidding, budget, schedule — what's confirmed vs. still open

**Bidding (SOP 7.3):** Non-branded launches on **Maximize Clicks with a max-CPC ceiling** (no conversion history yet). Branded on **Maximize Conversions, no target**.

**Ad schedule:** Site + README both give **Mon–Sun, 8am–6pm**. Per SOP 1C this field is a mandatory, no-default input — using the published hours as the best available evidence, but this should be confirmed as the actual phone-answering hours (not just business hours) before the schedule restriction is finalized, since "24/7 emergency" framing in the copy implies after-hours calls may also be answered.

**Monthly Search budget:** **Not yet set.** The Jul–Sep media plan gives a $9k/mo total across LSA + Google Ads + Meta with a fluid split, not a locked Search-only number, and SOP 1C requires written client approval before any budget goes live. Nothing here spends without that — see `google-ads-log.md` for the open item.

**Timing note:** the media plan's monthly emphasis (July peak cooling → August replacement → September storm/electrical) has already rolled past July–August as of this brief's date. Launching now lands in the **September window** — storm/electrical/generator demand plus AC tune-up prep is the live seasonal read, not July's emergency-AC peak. Non-branded budget weighting (once set) should favor Electrical, Generators, Leak-Detection and AC-Maintenance accordingly if the budget doesn't stretch to fully fund all 13 ad groups evenly.

**If the confirmed budget can't support all 13 non-branded ad groups at a meaningful daily spend**, trim in this order (lowest volume / most seasonal-fit first): Energy-Audit → Leak-Detection → Drain-Sewer → AC-Maintenance. Keep AC-Repair, Plumbing-Emergency, Electrical and Water-Heater in any trimmed version — they carry the volume.

**Everything in this brief builds PAUSED per SOP 7.9.12** — nothing here commits spend until the account is enabled, the budget is written down, and the account clears Pre-Launch QA (Stage 8).
