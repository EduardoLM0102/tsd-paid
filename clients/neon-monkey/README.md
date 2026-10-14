# Neon Monkey Services

Tree service (trimming/pruning, removal, stump grinding, plant health, holiday lighting, leaf cleanup).
**West Fort Worth, TX** and surrounding Tarrant/Parker/Johnson County area. TSD client.
Owner contact: **Brock**. AM: **Angela** (took over from Eve, Oct 2026). Folder created 2026-07-20.

## Accounts

| Platform | ID | Notes |
|---|---|---|
| Google Ads (PPC) | `7953905280` | Under Topservdigital MCC `4155514468`. 3 live campaigns: PMax Evergreen, Search Branded, Search Nonbranded Trimming. |
| Google LSA | `1219885876` | Separate account. 1 live system-generated Local Services campaign `19644340204`, ~$214/day. |

Access via `google-ads-ratos` skill → `scripts/tsd.sh` (TopServ profile `.env.topserv`, MCC `4155514468`).

## Current focus
Geo re-targeting to concentrate on **West Fort Worth** (Brock's 2026-07-16 meeting). See
`geo-targeting-review-2026-07-20.md`. Blocked on Brock's target-location list.

**2026-08-10:** PMax (`21225221220`) re-enabled at $110/day after the early-July pause (client-approved).
See `pmax-reactivation-2026-08-10.md` — includes the budget-headroom check against the $6,930/mo cap and
a finding that the `contact_us` conversion action is a page-view duplicate, not a real lead.
**2026-08-31:** cleaned up — `contact_us`'s CONTACT/WEBSITE conversion goal turned non-biddable on both
live Search campaigns, so it no longer inflates the Conversions/CPL column (still visible under All
Conversions). Details in `pmax-reactivation-2026-08-10.md`.

**2026-09-28:** client reported calls for lawn care. Root cause: `23825900343` (Search Nonbranded
Trimming) had zero negative keywords — despite EXACT/PHRASE-only keywords, Google's close-variant
matching pulled in "lawn care"/"lawn service" queries ($524.80/30d, 3 false conversions). PMax already
had "lawn" negatived; Search campaigns didn't. Added "lawn" (PHRASE) negative to both live Search
campaigns. Details in `lawn-care-negative-fix-2026-09-28.md`.


**2026-10-08:** account check + full action plan. `action-plan-2026-10-08.md` is the ACTIVE plan (read it
first). Key finds: site Google tag gone since ~08-30 (GA4 sessions 1,458 Aug → 12 Sep), NB CPC $19-22 → $30+
on uncapped Max Conv, PMax 70% of spend outside targets, Search geo already on a West FW list, Sept spend over
the documented cap, LSA volume down >50% at the same budget.

**2026-10-13:** site tracking BACK since ~9am CT. GTM-WM9CDGPT re-installed on neonmonkeytree.com, GA4 sessions
resumed. Live GTM is v11 (published 10-10, not by us): adds a phone-tap tag feeding new action
`[TSD] Click to call`, which is biddable on both Search campaigns. Recategorize to CONTACT pending Edu's OK.
Details in `tracking-restored-2026-10-13.md`.

## Gotchas
- LSA geo is set as campaign_criterion **location targets** (cities/ZIPs/**whole counties**) and IS
  readable via the API on this account — unusual for LSA. Tarrant County + Johnson County are
  targeted at county level (root cause of east-side / Grand Prairie leads).
- PMax uses **Presence OR Interest** positive geo (interest spillover) + radius circles, one of
  which (20 mi SE) reaches into Dallas County.
