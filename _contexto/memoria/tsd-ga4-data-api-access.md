---
name: tsd-ga4-data-api-access
description: GA4 Data/Admin API read access already wired in google-ads-ratos (ga4.py, GA4_REFRESH_TOKEN in .env.topserv); Proud Pops property 438523825
metadata:
  type: reference
---

GA4 reads work today. Scripts in `~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts/`: `./gtm.sh ga4.py properties|streams|events|report|conversions`, or import `data_service()` from `ga4_setup` in a scratchpad script and call `runReport` directly (needed for dimension filters). Token = `GA4_REFRESH_TOKEN` in `.env.topserv`, scope analytics.readonly. I wrongly told Edu on 2026-09-25 that I had no GA4 access; check this file first next time.

Proud Pops: property `438523825`, stream G-C7QTE9ZZXQ (stream is still named txproblemsolvers.com), tz America/Chicago. See [[tsd-proud-pops-tracking]] and [[tsd-gtm-tag-manager-setup]].

Gotchas: `pageReferrer` carries the full URL incl. query strings (gclid/fbclid), so one referrer explodes into many rows; pull rows and bucket by host/path in Python. `sessions` and `activeUsers` can read higher than `screenPageViews` on a page-filtered query; use views as the click proxy.

2026-09-25 result: homepage banner "View your offer" -> /first-repair. Sep 9-24: 86 views with homepage referrer (banner clicks), of 123 total /first-repair views (22 direct, 11 youtube, 4 other). Homepage had 2,266 views / 1,849 sessions in the same window. No dedicated GTM click event exists.
