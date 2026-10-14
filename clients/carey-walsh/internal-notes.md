# Carey & Walsh — internal notes (NOT for the client)

Companion to `media-plan-nov-2026-jan-2027.md`. Pre-launch gates, open questions, the research behind the numbers, and confidence levels live here, not in the client PDF.

**Task (AM, 2026-10-05):** "We will be starting paid ads for Carey & Walsh - they would like to see a proposed media/paid plan to review. Target area will be all of Westchester County." Client was supposedly signed a while ago but never surfaced to Paid. Edu's call: Meta = awareness only; Google Search + LSA lead lead-gen.

## Client facts (verified on careyandwalsh.com, 2026-10-05, raw HTML not summaries)

- Carey & Walsh Inc., 529 North State Road, Briarcliff Manor, NY 10510. Est. 1944, "80+ years", "four generations", "not a franchise or a roll-up".
- Main 914-762-9600 ("call at any hour"). Separate 24/7 emergency line **(347) 508-9713**.
- Serves Westchester, Putnam, Rockland. Residential + commercial (offices, retail, multi-family, light industrial; rooftop units, commercial boilers, PM contracts).
- Mitsubishi Electric Diamond Contractor (site: extended warranty coverage non-Diamond dealers can't offer; "fewer than 1%" claim, left out of the plan). NATE-certified, background-checked, "NY Licensed & Insured".
- Steam + hot-water boiler specialty, oil and gas; burners (Beckett, Riello, Carlin); oil-to-gas conversions; dual-fuel heat pump + existing boiler ("staged approach where a full conversion is premature").
- In-house sheet metal fab shop ("Built In-House. Built to Last."). Manual J on every install.
- Free estimates on new installs, written proposals, financing on qualifying equipment, "NY State incentives / NYSERDA / manufacturer rebates".
- Maintenance agreement plans + "Energy Savings Agreements" (ESA) with priority scheduling.
- Same-day claims: "most repairs are completed same-day" (site's own words).
- Review used in the plan's December Meta line: "Boiler went out on the coldest night of the year. Carey & Walsh dispatched a technician within two hours and had us back up and running before midnight." (on site, Google review).

## Account status checked 2026-10-05

- **Google Ads:** no Carey & Walsh account under TSD MCC 4155514468 (127 customer_client rows checked by name). Net-new build.
- **Meta:** no Carey & Walsh ad account in the full paginated `ads_get_ad_accounts` list. Net-new build. Facebook Page exists (site links to it), access not checked.
- **LSA:** none under the MCC. Unknown whether C&W already has an LSA / Google Guaranteed profile outside TSD. **Ask before creating one.**
- **GTM:** TSD's GTM has account `6000900042` "Carey and Walsh inc," → container `31040482` **GTM-M5DW5ZN**, which is the one on the live site. **Workspace 6 holds a full unpublished build**: Google Ads config + Lead + User-Provided Data, Meta pixel events (Lead / Phone Click / Email Click / Page View), GA4 events, Conversion Linker, CallRail config, GHL form listener. **Live published version 5** only carries GA4 `G-6J3K34P4W5` + the GHL listener: no AW- conversion ID, no Meta pixel. So someone at TSD started the tracking build (fits "we were supposed to be running ads for a while") and stopped because the ad accounts never got created. Forms are GHL (LeadConnector); CallRail is hardcoded on the site, not via GTM in the live version.

## Pre-launch gates

1. **Budget.** Unknown. Plan models $4k / $6k / $9k. Ask the AM whether the contract already names a number. A client-approved plan = written budget approval up to its total.
2. **Google Ads account** under MCC 4155514468 (billing owner?). Link GA4 `G-6J3K34P4W5`. Conversions: calls from ads, CallRail-tracked website calls, GHL form submit. Phone-click taps must NOT be primary (Proud Pops / Cool Hand lesson). Fill the Conversion ID constant in GTM, review workspace 6, publish separately from edits.
3. **Search settings at creation:** Search Partners + Display OFF (`create.py` defaults `target_search_network=True`); geo = Westchester County `9058785`, **PRESENCE only** (Cool Hand Dallas leak lesson); ad schedule 24/7 is fine since the emergency line is 24/7.
4. **LSA verification:** owner + field tech background checks, license, insurance. NY has no statewide HVAC license, so confirm what Google will accept (likely Westchester County home improvement license or a municipal license; site only says "NY Licensed & Insured"). Usually 2–5 weeks. Plan assumes LSA ramps in November.
5. **Which number goes on ads/LSA:** main 914-762-9600 vs emergency (347) 508-9713, plus a CallRail tracking number for the Google call asset.
6. **Meta:** ad account (client's BM or TSD's?), pixel ID into GTM, Page access. Creative = awareness-only per doctrine (Ad Recall Lift, ~3x/week, never recycled conversion creative): shop, fleet, technicians, reviews, 1944 story. Designer dependency, **set a creative deadline** (Cool Hand Meta slipped a full week past target).
7. **Service area:** site serves Putnam + Rockland too; task says Westchester only. Plan = Westchester only. Ask if the other two get added later.
8. **Commercial scope:** plan includes a Building Manager persona; confirm C&W wants commercial leads from paid.
9. **Federal tax credit language:** the site still says heat pumps "may qualify for federal tax credits". My understanding is the 25C credit ended for equipment placed in service after 2025-12-31 under the July 2025 tax law, so the plan copy only says "New York incentives and rebates". Verify before anyone writes "tax credit" into ads; flag to the AM that the site copy may be stale.
10. **Cooling:** AC campaigns excluded Nov–Jan. Spring plan should bring them back from April (cooling demand curve below).

## Research behind the numbers

**Keyword Planner** (Westchester County `9058785`, English, Google Search only, Sep 2025–Aug 2026, via `keyword_planner.py`, customer 8513856629). Raw JSON was in the session scratchpad, not saved here.

Heating seed set (boiler/furnace/heating repair, replacement, boiler service, steam boiler, oil burner, emergency heating) monthly searches: Jan 1,450 · Feb 1,160 · Mar 590 · Apr 430 · May 300 · Jun 270 · Jul 530 · Aug 380 · Sep 1,200 · **Oct 2,000** · Nov 1,430 · Dec 1,150.
Cooling (ac repair + ac installation): peaks **Jul 1,860**, Dec–Jan ~190.

| Keyword | Avg/mo | Top-of-page bid (low – high) |
|---|---|---|
| ac repair | 590 | $22.59 – $90.53 |
| hvac near me | 480 | $21.28 – $78.62 |
| furnace repair | 390 | no bid data |
| boiler repair | 260 | no bid data |
| hvac contractors near me | 320 | $17.57 – $96.17 |
| hvac companies near me | 260 | $17.71 – $78.99 |
| hvac repair near me | 170 | $24.65 – $100.00 |
| hvac service | 140 | $25.00 – $78.69 |
| heat pump installation | 140 | no bid data |
| heat pump repair | 140 | no bid data |
| ductless mini split | 110 | $2.24 – $9.16 |
| boiler replacement | 20 | $2.62 – $21.39 |

"No bid data" on boiler/furnace/heating repair is the basis for the plan's "few advertisers compete" line. That's an inference, not a measured auction fact. Real CPCs come after 30 days live.

**LSA benchmark:** web benchmarks put HVAC LSA at ~$51/lead national (Feb 2026), $45–$80 in large metros, NY 20–50% above national ([99calls](https://99calls.com/LSA-Cost-Estimator/hvac-contractor), [bookedfriday](https://bookedfriday.com/local-services-ads-cost), [adgenius](https://adgenius.com/blog/google-local-services-ads-cost-per-lead/)). Internal cross-check: the unnamed LSA account **8655979348** under our MCC is a **Long Island** HVAC business (155 geo criteria: Albertson, Great Neck, Cold Spring Harbor...), NOT Carey & Walsh. Feb–Sep 2026: $2,884.24 / 61 charged leads = **$47.28 per charged lead**, mostly hvac_maintenance. Small budget (~$300/mo), so it understates what a heavier winter push costs. Not cited in the client doc.

**Meta:** home services CPM ~$13.40 national ([digitalapplied](https://www.digitalapplied.com/blog/facebook-ads-benchmarks-2026-cpc-cpm-ctr-industry), [get-ryze](https://www.get-ryze.ai/blog/meta-ads-cost-benchmarks-by-industry-2026)); no NY home-services number found. **Reach math:** at $600–$900/mo and a $12–$20 CPM that's ~30k–75k impressions/month, roughly 2.5k–6k people a week at 3x/week. A small slice of a county of ~1M. Ad Recall optimization picks who. If the client expects "everyone in Westchester sees us", Meta needs more than 13%.

**Competitors on Meta** (Ad Library 2026-10-05, "Westchester HVAC", active): One Hour Heating & Air Conditioning of Westchester, Innovative Air Solutions ("$25 OFF your AC tune-up"), HVAC Specialist Inc. ("No Heat? We're On It.", "Premier Comfort Club"), Comfort Experts ("$500 Off Any New Installation"), Royal Comfort, Liberty HVAC (NYC). Mostly offers, which is the basis for the plan's "pushing discounts" line.

## Lead math (at $6,000/mo, plan-average shares)

- Search 49% = $2,940 ÷ $125–$275 CPL → ~11–24 leads (assumes ~10–12% CVR on $18–$40 CPC).
- LSA 38% = $2,280 ÷ $50–$90 → ~25–46 leads. LSA volume may cap below that in one county; overflow goes to Search per the plan.
- Total ~36–69 → stated as 35–65.

## Benchmark confidence

- LSA $50–$90: **medium** (web benchmarks + one NY-metro account).
- Search CPC $18–$40: **medium** (Keyword Planner, county-level).
- Search CPL $125–$275: **low–medium** (CVR assumed, no account history).
- Meta CPM $12–$20: **low** (national number + "NY runs higher" assumption).
