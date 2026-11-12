---
name: tsd-meta-reach-estimate-limits
description: Meta reach/audience-size estimates + per-placement CPM forecasts are NOT available via the Meta MCP; recipe for observed CPMs + Census radius proxy (TIGERweb, no key)
metadata:
  type: reference
---

Learned 2026-10-26 on Ryan's Amazing Morrow ask (prospect, office 17013 Seven Pines Dr, Spring TX 77379; brand fence radius sizing, $15k/mo, 3x/wk).

- **Meta forecasts are Ads Manager only.** Estimated audience size, estimated reach and estimated CPM by placement do not come back from any Meta MCP tool. `.env.meta` token is a placeholder (Graph API unusable). So: build a draft ad set in Ads Manager by hand, or give observed data.
- **Observed CPM by placement:** `ads_get_ad_entities` level campaign, filter `campaign.objective IN [OUTCOME_AWARENESS]` + all statuses, `breakdowns: [publisher_platform, platform_position]`. FB Stories gets ~0 delivery in our auto-placement awareness campaigns. Under Reach goal with Marketplace limited, Meta piles into IG Stories (Spencer 30d: 81% of non-Marketplace imps at $1.48), so a "six placement blend" under Reach is carried by one cheap placement too.
- **Houston Meta awareness data:** only On The Way (1428068256022895, Santa Fe TX pin, 35 mi, ARL, 2026-09-04 to 09-11, $363, six-placement blend $3.72).
- **Census radius proxy:** api.census.gov now needs a key (redirects to missing_key). TIGERweb works keyless: `tigerWMS_Census2020/MapServer/8/query` (block groups) with point + distance, outFields INTPTLAT/INTPTLON/POP100, filter by centroid distance. Gives 2020 total pop only (no 18+); geocode with geocoding.geo.census.gov onelineaddress.

**How to apply:** any Ryan/JB ask for Meta reach or CPM forecasts. Say up front the forecast needs Ads Manager, send observed first. See [[tsd-growth-engine-brandformance]], [[tsd-meta-ads-methodology]].
