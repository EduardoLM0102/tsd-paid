---
name: tsd-neon-monkey
description: "TSD client Neon Monkey (tree service, West Fort Worth): ⚑ ACTIVE PLAN clients/neon-monkey/action-plan-2026-10-08.md; site tag dead ~08-30 → BACK 10-13 (GTM v11 adds biddable phone-tap action); PPC 7953905280 + LSA 1219885876 + GA4 328458299"
metadata:
  node_type: memory
  type: project
  originSessionId: d9dd2e35-2058-44f0-8194-61308014ad50
  modified: 2026-10-09T01:40:06.044Z
---

TSD Google Ads client **Neon Monkey Services** (tree service), West Fort Worth TX. Owner **Brock**, AM **Angela** (was Eve until Oct 2026). Site fixes route to TSD Web Dev (Justin), not the client. No weekly AT task. Log folder `topserv-workspace/clients/neon-monkey/`. **Re-read `action-plan-2026-10-08.md` first** (8 phases, dated; Command Center followups fu-026..029 + fu-017).

**Accounts** (MCC 4155514468): PPC `7953905280` (live: NB Trimming `23825900343` $150/d, Branded `23739724064` $100/d, PMax `21225221220` $110/d, all Max Conv), LSA `1219885876` separate ($214/d budget, spends ~$30/d). GA4 `328458299` (G-WF5DBMQ644). Site = **neonmonkeytree.com** (WordPress/Divi; old neonmonkeyservices.com redirects).

**Non-obvious facts (10-08):**
- Site LOST ITS GTM Sat Aug 29 ~5-6pm (GA4 hourly: last normal hour 17h, near-zero after; 2 pages edited Sun Aug 30 22:11; weekly Thursday city pages stopped after Aug 27): container **GTM-WM9CDGPT** (TSD GTM acct 6264215029, live v10 published 2026-08-03, 18 tags: GA4, Google Ads config + Lead + user data, conv linker, GHL form listener, CallRail, Meta pixel, Clarity, TikTok) is intact but no page loads it (GA4 sessions 1,458 Aug → 12 Sep). Fix = Web Dev re-adds the snippet; no rebuild. CallRail lived inside GTM, so the `Phone Call` UPLOAD_CLICKS import (stopped Sept) is likely CallRail's. Meta pixel is down too. Only signals left: `Calls from ads` + server-side GA4 `ghl_contact_us`; `ghl_request_estimate` not imported. Site shows toll-free 800/866 numbers (maybe CallRail), ads use (817) 409-8954.
- Search geo is ALREADY a 36-location West FW list (applied before 09-09); only PMax (Presence OR Interest, 5 circles; 70% of spend outside targets) and LSA (whole counties) are on old geo. The geo "blocked" status was stale.
- `CSMS_Negatives` shared list (477) is attached only to paused campaigns and blocks real tree terms (crape myrtle, pine, pecan, 76116) — clean before reuse.
- NB had a "Free Pump Inspections" callout from another client.
- Holiday Lighting `18787352551` / Leaf Cleanup `19146431184` paused, didn't run last season.
- Sept PPC $8,356 vs $6,930 cap in the 08-10 log.

**Timeline:** 07-20 geo review → 07-28 call drop = PMax paused → 08-10 PMax back → 08-31 `contact_us` non-biddable → 09-28 "lawn" negative (holding) → 10-08 check + action plan (nothing applied yet) → 10-10 GTM v11 published (not by us) → 10-13 site tag BACK.

**2026-10-13: tag restored.** Web dev re-added GTM-WM9CDGPT (head + body noscript, all pages checked). GA4 site sessions resumed 10-13 ~9am CT. GTM live is now **v11** (published 2026-10-10, 19 tags), which adds `Google Ads | Phone Call Click` (trigger `Link Click - Phone Number`, label a504CPz3mZgdEIy01Kso) feeding new action **`[TSD] Click to call` 7835384828** (CLICK_TO_CALL, PHONE_CALL_LEAD, primary). `PHONE_CALL_LEAD/WEBSITE` is biddable on NB + Branded, so **phone taps now count as conversions** (NB on Max Conv). That goes against the plan's taps-not-primary rule; open decision. Creator unknown (change_event doesn't log conversion actions). Site sits behind a "Checking your browser" bot wall: headless Playwright gets a 403 while curl gets the real page, so verify via curl + GA4, not headless.

**2026-10-20:** Angela asked → "tree place" + "treeplace" PHRASE negatives added on the 3 enabled campaigns (NB Trimming, PMax Evergreen, Branded Mix); was $80.56/90d. Log: `clients/neon-monkey/google-ads-log.md`.
