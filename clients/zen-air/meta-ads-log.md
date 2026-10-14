# Zen Air — Meta Ads log

Account `381256660973192` ("Zen Air - Third Ad account ( Active Account)").

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
