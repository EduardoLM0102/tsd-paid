# Zen Air — Meta Ads log

Account `381256660973192` ("Zen Air - Third Ad account ( Active Account)").

## 2026-10-23 — Weekly 7-day Meta pass (AT task ff291b11, Gui): read-only, KPI logged, changes staged

**10-16..10-22:** $1,500.82, 137 leads, $10.95 CPL, $6.45 CPM, 0.50% CTR, reach 108,339, freq 2.15 (10-16 entry: $1,535.43 / 98 / $15.67).
- Lead ad set `09/22/26 - Service Area ZIPs (New Creatives)`: $1,047.16, 83 leads, $12.62 CPL, $11.79 CPM. Around Edu's 10-20 change (home only +
  30320 excluded): 10-16..19 $584 / 50 ($11.68) → 10-20..22 $463 / 33 ($14.03), CPM ~$10.7 → $13.2 (narrower audience). Lead location recheck ~10-27.
- Awareness `Open Audience` ($65/d): $453.66, reach 66,468, freq 2.16/wk, $3.16 CPM; also reports 54 "leads" (likely pixel Lead events, not forms).
Lead Quality = **Mixed**. **Staged, not applied:** (1) ARL rebuild of awareness, no cap (still REACH + cap 4/7d); (2) at ~10-27 decide Fulton → North Fulton.
KPI - Meta `db74ef1f`.

## 2026-10-16 — Weekly 7-day Meta pass (AT task fc797a2f, Gui): read-only, KPI logged, changes staged

**10-09..10-15:** $1,535.43, 98 leads, $15.67 CPL, $6.85 CPM, 0.51% CTR, reach 116,470, freq 1.93 (10-13 entry: $1,582.55 / 56 / $20.05).
- Lead CBO `09/17/26 - CBO | Leads` ($150/d): $1,081.77, 70 leads, $15.45 CPL, 1.26% CTR, one ad (09/22/26 | Ad 02).
- Awareness `TOFU - Brand Awareness_Reach_OA_FQ4_7` / ad set `Open Audience` 120227295614750711 ($65/d): $453.66, reach 77,376, **freq 1.85/wk**, $3.18 CPM. **Off doctrine:** optimization_goal = REACH and `frequency_control_specs` = CAP 4 impressions / 7 days.

Lead Quality = **Mixed** (10-14 geo audit: 13/27 post-fix leads still outside the core area).

**Staged, not applied:** (1) rebuild awareness as a new ARL campaign with no frequency cap, same 131 ZIPs, then pause the old one (same as All Seasons 10-09); (2) at the ~10-19 recheck, if out-of-area leads continue, cut Fulton to North Fulton ZIPs.

## 2026-10-12 — Service-area targeting fixed on both live ad sets (AT task: "FB ads getting worse as far as location")

**Trigger.** Client said Facebook leads are getting worse in terms of where they come from; AT task asked to make
sure the area is set up correctly.

### Finding
- Lead CBO `09/17/26 - CBO | Leads` (120247267872090711, built by Jonathan Bannister 09-17, ~$1,050/wk) and the
  awareness ad set `Open Audience` (120227295614750711, TOFU campaign) both targeted **Duluth, Marietta, Monroe**
  (city limits, no radius, home + recent). The awareness ad set already had these 3 cities before 08-18 (oldest
  activity log pulled), so the 09-17 lead build most likely copied it (inference).
- **Marietta (Cobb, ~23 mi) and Monroe (Walton, ~29 mi) are outside the service area**: not on
  callzenair.com/service-area (14 cities) and not in AT "ICP - Target Cities". 13 of the 14 real cities were not
  targeted at all.
- Earlier lead campaigns (Apr to Jul, $49 offer / ANIV SALE) used Duluth +15 mi. No lead campaign ran 08-03..09-16.
- Delivery was 100% Georgia, Optimize locations OFF, so Meta wasn't expanding geo; the leak was the setup.
- Lead campaign since 09-17: $3,739 / 168 leads (19, 60, 41, 48 per week).

### Changes (all on Edu's instruction, published from draft and read back live)
| Time (ET) | Change | Both ad sets |
|---|---|---|
| ~09:43 | Removed Marietta + Monroe (left Duluth only) | yes |
| ~09:46 | Excluded Marietta (2433307) + Monroe (2433510) via `excluded_geo_locations` | yes |
| ~09:49 | Added AT Target Cities as **131 ZIPs**; Duluth city key dropped | yes |
| ~09:5x | Renamed lead ad set → `09/22/26 - Service Area ZIPs (New Creatives)` | lead only |

**Final live state (both ad sets, ACTIVE):** 131 ZIPs = all GeoNames ZIPs in Gwinnett (30), Fulton (85, whole
county as AT lists it, incl. Atlanta / South Fulton), Hall (12), Forsyth (3) + Hoschton 30548 (Jackson). Covers all
14 AT cities (Johns Creek / Sugar Hill sit in 30097/30022/30005 and 30518). "Forsyth, GA" read as Forsyth County
(Forsyth city is near Macon). Marietta + Monroe excluded. Unchanged: age 18-65, Advantage+ audience with geo
expansion off, location type home + recent, placements, budget, ads. ZIP list:
`meta_zips_service_area_2026-10-12.txt`.

**Untouched:** paused ad set `09/17/26 - Marietta & Duluth & Monroe` (120247267872100711) keeps its old targeting
and name. Paused legacy campaigns not touched.

### Mechanics / gotchas
- Meta rejects the legacy `page_types` targeting field on write (error 1885366). Placements were resent as
  `publisher_platforms` + `*_positions` copied from the live `effective_*` values.
- IG `explore` placement is deprecated (error 2490589), dropped from awareness. Meta also didn't keep
  `profile_reels` in the effective IG positions.
- A city plus ZIPs inside it = "locations conflict" (error 1487756). Use one or the other.
- 60 of 131 ZIPs return `primary_city_id: 0` (mostly PO box / unique ZIPs, downtown Atlanta 303xx/311xx). Accepted.
- Lead ad set re-entered learning (targeting change).

### AT check: when was "never target Marietta/Monroe" added?
- The rule lives in AT field **Notes - Paid Advertising** (`notes_paid_advertising`): "Please do not target
  Marietta/Monroe ever for campaigns". "Do Not Target Areas" is empty.
- Edu suspects it was added after the 09-17 build. **Not provable via the AT MCP:** field history
  (`data_field_history_list`) only supports built-in fields (status worked; `icp_target_cities`,
  `notes_paid_advertising`, `do_not_target_areas` rejected), and the client audit feed (`data_activity_list`,
  GET /v1/activity) returned internal errors on every call, even unfiltered. No task title/stage or client comment
  mentions Marietta/Monroe; ticket bodies couldn't be searched.
- Only data point: client record `updated_at` 2026-09-22 02:03 UTC = **09-21 10:03 PM ET** (any field). That is
  after the 09-17 lead build and before the 09-22 7:53 AM ad set, but it doesn't prove the note was written then.
- Marietta/Monroe were already an "outlier cities" topic in Andrea's Jun 1-15 summary (see
  `2026-07-09-geo-and-account-findings.md`), so the concern predates September.

### Open
- Recheck in a week (~10-19): lead CPL/volume after the expansion and learning reset, and ask the AM whether lead
  addresses now fall inside the area.
- Whole Fulton is live (reaches ~44 mi south). If leads show up from south Atlanta / South Fulton, cut to North Fulton
  (Alpharetta, Johns Creek, Milton, Roswell).
- AT: check the web UI for profile edit history, or ask AT support to pull it and report the /v1/activity internal
  error.
- Reply to the task (draft given in chat) still to be posted.

## 2026-10-14 — Lead geo + quality audit of ad `09/22/26 | Ad 02 - Images 07, 11, 13` (read-only)

Source: Edu's lead export (173 leads, 09-22 09:21 .. 10-14 09:34, times in the file are UTC-5). Ad spend same window
$3,434.66 / 173 leads = $19.85 CPL (Meta, ad 120247339585920711). The form only collects name/phone/email/**city**
(Facebook prefills the profile city), so geography is self-reported, no ZIP.

| Bucket (by city field) | All 173 | Before fix (146) | After fix 10-12 ~09:49 ET (27) |
|---|---|---|---|
| Core area (site 14 cities + LSA extras Grayson/Loganville) | 28 (16%) | 24 | 4 |
| AT counties, not a site city (Atlanta 29, N. Atlanta, Gainesville, Fairburn, Union City, College Park) | 36 (21%) | 27 | 9 |
| Marietta / Monroe | 47 (27%) | 47 | 0 |
| Other Georgia, outside area | 43 (25%) | 34 | 9 |
| Out of state / country | 13 (8%) | 9 | 4 |
| Junk / unclear | 6 | 5 | 1 |

- Cost per core-area lead ≈ $123 ($3,435 / 28); including the Atlanta/Fulton/Hall maybes ≈ $54.
- Fix worked on Marietta/Monroe (0 since). But after it, 13 of 27 are still clearly outside: New Orleans, Tallahassee,
  N. Charleston, Chicago, Augusta, Athens, Guyton, Bremen, Riverdale, Locust Grove, Covington, Lithonia, Acworth, plus
  South Fulton (Fairburn, Union City, College Park). Likely cause (inference): whole Fulton incl. airport ZIP 30320 /
  downtown + location type home+recent = travelers and commuters. This is the fu-042 trigger to cut Fulton to North Fulton.
- Contact data mostly clean: no duplicate phones/emails, 172/173 US numbers. Obvious junk ~5%: 770-777-7777, 773-556-5555,
  a Brazil number, gibberish city, phone typed into name. 4 trade/business emails (a plumbing co., "Acsspecialist" in
  Duluth, a cleaning co., a media co.).
- Real quality (booked vs not) needs GHL outcomes from the AM/Eddie; not visible here.
- **Edu's framing (same day): "workable" = core cities + Gainesville/Fairburn/Union City/College Park (Atlanta kept
  separate).** Workable 34/173 (20%). Before fix 25/146 (17%, ~1.3/day, ~$120 each); after fix 9/27 (33%, ~4.4/day,
  roughly $40-45 each, spend split by day so approximate). Last full week before the fix was the worst: 6/50 (12%).
  But leads from outside the area excluding Marietta/Monroe rose from 29% to 48% of leads, and 3 of the 9 post-fix
  workable leads are South Fulton. 27 leads / 2 days in learning, so directional only.
