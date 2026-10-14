---
name: tsd-live-wire-electric
description: "Live Wire Electric (Lynnwood/Seattle WA) TSD client — Google Ads account structure, 2026-09-03 conversion-goal fix, and 2026-09-08 geo-targeting narrowed to client's own service-area map"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9693fddd-05ba-4720-ab0c-9d1ef093e76b
  modified: 2026-09-08T12:38:28.870Z
---

Live Wire Electric — electrician, Lynnwood/Seattle WA (livewireelectricwa.com). TopServ client,
Google Ads customer_id 1056617442 (MCC Topservdigital 4155514468), registered in `contas.yaml`
2026-09-03 (found by listing `customer_client` under the MCC — wasn't tracked anywhere before that).
Full history in `topserv-workspace/clients/live-wire-electric/google-ads-log.md` — read that before
acting on this account.

**Account structure:** LSA (`LocalServicesCampaign:SystemGenerated:...`) lives inside this same
account, like [[tsd-watts-right]] — best-performing channel (~$35.90 CPA, ~23 leads/30d), $500/d cap,
nowhere near it. Two live Search campaigns: `TSD_03.16_Search_Branded_Evergreen` (23665625884) and
`TSD_04.28_Search_Nonbranded_Evergreen` (23806096501). 8 legacy campaigns sit paused, no live impact.

**2026-09-03 conversion-goal gap (fixed):** same failure pattern as
[[tsd-google-conversion-goals-mechanics]] — Nonbranded Search had `campaign_conversion_goal`
(DEFAULT/WEBSITE, i.e. First Time Phone Call) unset while Branded had it biddable, so real phone-call
leads on Nonbranded weren't counting as conversions (looked like a 0-conversion dud on $1,200+/mo,
real leads were ~8/mo). Fixed via `update.py conversion-goal`. Also found Branded losing 89.4% of
impression share to Ad Rank on its own brand name (budget not the constraint) — same pattern as
Watt's Right 2026-08-12, left alone pending re-check. Added 8 missing competitor-name negatives.
Reallocated budget same day, net $0/day: Branded $80→$50, Nonbranded $40→$70 (reallocation at
constant total, no AM-approval gate — see [[tsd-budget-approval-scope]]).

**2026-09-08 geo-targeting narrowed to client's map:** client provided a hand-drawn polygon
(`~/Documents/livewire_targeting.png`) covering South Snohomish County + a thin strip of North King
County (Shoreline/Kenmore/Lake City corner) — nothing like the county-wide targeting that was live.
Both Search campaigns had been targeting **all of King County + all of Snohomish County** (including
Seattle, the Eastside, south King County, rural north Snohomish) — replaced with a 20-city list
matching the polygon: Mukilteo, Everett, Snohomish, Lake Stevens, Monroe, Lynnwood, Edmonds,
Mountlake Terrace, Brier, Mill Creek, Shoreline, Kenmore, Bothell, Lake Forest Park, Machias, Silver
Firs, Martha Lake, Maltby, Canyon Park, North Creek. Woodinville deliberately excluded (genuinely
split by the boundary line); Bothell was initially excluded on the same boundary-call logic, then
added back after an independent re-check found its core reads as inside, not edge-adjacent — worth
remembering that "is this city mostly inside the drawn line" deserves a second look before excluding
a fairly large, central city on a boundary judgment call. LSA's own separate ~50-city service-area
list (still includes Seattle, the Eastside, south King County) was left untouched — not in scope,
would need its own pass if the client's map is meant to apply there too.

**New tooling:** `delete.py location` subcommand added to the shared `google-ads-ratos` scripts (only
had keyword/negative/ad-group/ad before) — removes a campaign-level geo-target via
`CampaignCriterionOperation.remove`, using the geo target constant ID as the criterion ID. Reusable
for any other TSD client that needs geo-targeting narrowed from county/broad-city-list down to a
tighter set.

**How to apply:** this is a real narrowing of Search reach — watch impression/click volume over the
1-2 weeks after 2026-09-08 for a real drop-off before assuming the narrower targeting is a net
improvement. When re-checking a client-provided targeting map against live settings, don't just trust
the first boundary call on ambiguous edge cities — a second look caught a real gap (Bothell) that the
first pass got wrong.

**2026-10-08 change-history pull (unresolved, ask Edu):** someone outside TSD is running this account now. `brandon@tradevulcan.com` (Trade Vulcan) built copies of both Search campaigns on 09-16 (`... | LWE V2 REVIEW 2026-09-16`, ENABLED), then paused TSD's originals on 10-05/10-06 and added keywords/ads/negatives. ~690 changes by him since 09-16; the client's own email changed the LSA budget 10-06. TSD's last logged work is 09-15, and the Agency Titan 7-day Google/LSA tasks stopped recurring after 09-21. Before doing anything here, confirm with Edu whether Live Wire is still a TSD client.
