# Cool Hand Electric — internal notes (NOT client-facing)

Mansfield & Red Oak, TX (Ellis/Johnson/Tarrant/Dallas counties) · coolhandelectric.com · owners Kristen & Luke Strange · founded 2015, 11 employees. CRM ServiceTitan, site GoDaddy.
Status: **existing Google Ads account, new to Meta/TikTok.** Google Ads CID `9865206319`.

Client-facing deliverable: `media-plan-aug-dec-2026.md` → `Cool-Hand-Electric-Media-Plan_Aug-Dec-2026.pdf`.
Operational guidelines below were cut from the client PDF (Edu, 2026-08-05) and live here instead.

---

## Channel architecture (Edu's call, 2026-08-05)

Google Ads carries the majority of both budget and lead-gen — Search does the direct-response heavy lifting, YouTube rides along inside the same Google Ads spend as a smaller awareness-only carve-out. Meta runs lighter than Google overall: a low always-on baseline for retargeting/brand most months, concentrated into two seasonal-offer bursts (September "Beat the Heat," December holiday panel-safety) where it's worth asking Meta to generate leads directly rather than running flat spend all five months. Edu left the exact mechanism ("lower budget and/or occasional") to be decided — picked the seasonal-burst structure because it maps cleanly onto the arc already built into the plan (two moments — pre-winter AC push, holiday electrical push — where a specific offer beats generic always-on retargeting). TikTok is unaffected, still the same optional pure-awareness add-on.

Five-month average: **Google Ads (Search + YouTube) 81% · Meta 19%.** Within Google Ads, Search alone averages 69%, YouTube 12%.

## Scope decision: LSA is excluded

**Edu's call (2026-08-05, mid-build): TSD is not running Cool Hand Electric's Google LSA right now.** Plan covers Google Ads (Search/PPC), Meta, and TikTok (optional, awareness-only) only.

This matters because the account already has a live, auto-generated LSA campaign in the *same* Google Ads CID (`9865206319` — the intake's "Google LSA CID" and "Google Ads CID" are the same number because LSA lives inside the standard account). Pulled directly from the account for context, not part of this plan's spend or KPIs:

- **Last 30 days: 47 conversions (leads) / $3,506.22 spend / $74.60 avg. CPL.**
- **July alone: 42 leads / $3,054.06 / $72.72 CPL.** Ramped steadily since first activity in late May.
- Daily budget cap is $214.29/day (≈ $6,428/mo) but actual spend runs $40–$310/day — the account is **not maxing its own budget cap.** That points to a lead-volume/engagement ceiling (LSA rank, category approval, service-area limits), not a budget ceiling. Don't assume raising the cap buys more leads without checking what's actually capping it.
- 291 clicks / 4,190 impressions / 47 conversions over 30 days blends desktop (10 conv, $74.50 CPL) and mobile (37 conv, $74.63 CPL) roughly evenly on CPL, mobile carrying the bulk of volume.
- Which LSA categories are currently approved (HVAC? Electrician?) is **not verified** — the campaign name is Google's auto-generated system name, doesn't state category. Whoever manages LSA should confirm.

**Consequence for this plan:** whatever this plan drives (Google Search, Meta, TikTok) is additive to that existing ~42–47 leads/month LSA is already producing elsewhere. Don't let anyone read this plan's lead targets as the client's *total* lead flow — they're this plan's channels only. And since LSA and standard Search share the same Google Ads account (different budget objects, same billing profile), coordinate before touching account-level settings.

## Scope decision: Plumbing excluded

The intake has a full **Plumbing Services Offered** catalog (general plumbing, drains, water treatment, emergency, gas lines, sewer, water heaters, commercial) — but the **Top Marketing Services** field says only *"Residential HVAC & Electrical Services,"* the business name is "Cool Hand Electric, Heating, & AC Repair" (no plumbing in the name), and the 6 listed competitors split HVAC/electrical only — none are plumbing competitors. This plan markets **HVAC + Electrical only,** treating the plumbing catalog as stale/template carryover.

**Confirm with the AM/client before the next revision:** does Cool Hand actually offer plumbing, and if so should it be in paid scope? If yes, this changes messaging, keyword targeting, and competitor set.

## Hours conflict

Services list **"24/7 Emergency Service"** under both Heating and Air Conditioning. Business Hours on file: **Mon–Fri 8:00 AM–5:00 PM, Sat–Sun Closed.** Same conflict pattern seen on other TSD accounts (e.g. Lilypad Septic, Zen Air) — don't advertise availability nobody is there to answer. Need an on-call/answering-service protocol confirmed before any campaign runs emergency-intent keywords or dayparts outside those hours. Response speed also affects LSA rank if/when LSA is ever brought into TSD's scope.

## Tracking is a blank slate for the new channels

No GA4 property, no Facebook Pixel ID, no GTM container, no call tracking provider on file — all dashes in the intake. The existing Google Ads account has *some* conversion tracking (the LSA campaign shows conversions), but nothing is confirmed for a standalone Search campaign, and nothing exists for Meta or TikTok. **TSD hard rule: end-to-end lead flow test before anything goes live**, same gate as every blank-slate account. This is a full build for Meta (Business Manager, pixel, CAPI) and TikTok (Pixel/Events API) before spend starts, and a GA4/conversion-action build for the new Search campaign so its performance isn't blended with the LSA campaign already in the account.

## Other open items

- **Target CPA/conv-rate fields are all blank** in the intake. No client-approved CPA target exists — the CPL ranges in the plan are Keyword-Planner-derived (Texas geo, pulled 2026-08-05) and industry benchmark estimates, not client-set targets.
- **Google Search KPI ranges are Texas-state-level Keyword Planner data** (geo target constant 21176), not hyper-local to the Ellis/Johnson/Tarrant/Dallas zip list. Directionally solid for a metro this size; replace with the account's own auction data after 30 days live, same as every other TSD plan.
- **Service area looks tight and plausible** — 6 target cities + 9 zips across 4 counties around two offices (Red Oak and Mansfield, ~20 min apart) — lower risk than accounts with overstated service radii, but still confirm ad geo-targeting is built to this exact list rather than a broad-radius default.
- **Budget is genuinely unset.** Intake literally says "No ads budget." Plan ships as ratios with $3,500 / $5,000 / $7,500 monthly dollar scenarios per Edu's direction, same approach as Lilypad.
- **If they move forward:** add to `contas.yaml`, start `google-ads-log.md` and `meta-ads-log.md`, and confirm which LSA categories are live if/when LSA ever comes into TSD's scope.

## Benchmark provenance

- **Google Ads (Search) CPC** — pulled live via Keyword Planner, Texas geo (constant 21176), 2026-08-05: `ac repair` $12.31–$95.49 (LOW comp, 49.5k/mo TX), `electrician near me` $6.69–$65.34 (HIGH comp, 33.1k/mo), `furnace repair` $2.89–$52.68 (LOW comp, 12.1k/mo), `ac installation` $7.58–$56.50 (LOW comp, 6.6k/mo), `electrical panel upgrade` $3.30–$32.00 (LOW comp, 720/mo), `generator installation` $8.23–$41.47 (LOW comp, 1k/mo). These are top-of-page bid ranges, not observed CPCs — treat as planning inputs, replace with real auction data after 30 days.
- **Meta CPL $30–$50** — same LocaliQ Home & Home Improvement lead-gen benchmark ($41.26) used for Lilypad. No Cool Hand-specific Meta data exists yet.
- **TikTok** — awareness-only in this plan (Edu's call), so no CPL target modeled. Benchmarked on CPM/reach, not lead cost.
- **National seasonality** (from the same Keyword Planner pull, US-wide): `ac repair` peaks Jul–Sep, troughs Dec–Feb; `furnace repair` inverts, troughs Jun–Aug, peaks Nov–Jan. This is the spine of the Aug–Dec monthly messaging arc.
