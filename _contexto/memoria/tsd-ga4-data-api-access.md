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

**2026-10-18 limits (Johnny's key-event ask):** the TSD token is `analytics.readonly`, so it CANNOT create key events (Admin API keyEvents.create needs `analytics.edit` + Editor role on the property). It also sees only 10 properties (Kings Window, All Season, C&S Air, Neon Monkey, Zen Air 350001559, Napps, Proud Pops, Topservdigital, GC, Cool Hand): Carey & Walsh 312972795, Nick's 385318676, Ryan Heating 313209811 all 403. To write key events by API: get the login added as Editor on the property, add `analytics.edit` to SCOPES in ga4_setup.py, re-run `./gtm.sh ga4_setup.py oauth`. Otherwise it's a UI job (Admin > Events > star the event).
**Update 2026-10-18 (later):** token login CONFIRMED = eduardo@topservdigital.com (tokeninfo shows no email; confirmed because the 3 properties appeared right after that user was added). Cowork (in access@topservdigital.com's browser) added eduardo@ as Editor on Carey & Walsh, Nick's, Ryan Heating and marked the key events: phone_click on all 3 + generate_lead on Nick's; purchase kept. Re-read via Admin API `properties().keyEvents().list` (works on readonly scope). Writes still need `analytics.edit` + re-oauth.
