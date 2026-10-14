# Live Wire Electric — Google Ads log (1056617442)

Registered in `contas.yaml` 2026-09-03 — found by listing all `customer_client` accounts under the
Topservdigital MCC (4155514468), since the client name wasn't registered anywhere in this workspace
yet. Business is an electrician in Lynnwood/Seattle, WA (site: livewireelectricwa.com). LOCAL_SERVICES
(LSA) lives inside this same account, not a separate one. 8 legacy campaigns sit PAUSED (old Smart
Campaign, 3x PMax, Display, 2x old Search) — not touched, no live impact.

Live campaigns at time of audit: `TSD_03.16_Search_Branded_Evergreen` (23665625884),
`TSD_04.28_Search_Nonbranded_Evergreen` (23806096501), and the system-generated LSA campaign
(20154807116).

---

## 2026-09-03 — Full audit: conversion-goal gap found and fixed

**Authority:** Edu, in-session. Conversion-tracking config change, not a budget change — no approval
gate applies.

### What we found

**Last 30 days, LSA excluded:**

| Campaign | Cost | Clicks | "Conversions" | Real leads (all_conversions) |
|---|---:|---:|---:|---:|
| Branded | $1,167.03 | 125 | 12.0 | 21.97 |
| Nonbranded | $1,233.06 | 128 | 0.0 | 8.0 |

Nonbranded looked like a total dud (0 conversions on $1,200+/mo). It wasn't — segmenting by
conversion action showed real phone-call leads happening but not counting:

| Campaign | Conversion action | Counted in "conversions"? | Count (30d) |
|---|---|---|---:|
| Branded | First Time Phone Call | Yes | 12.0 |
| Branded | Calls from ads (call-extension click) | No | 6.0 |
| Branded | Repeat Phone Call | No | 3.97 |
| Nonbranded | First Time Phone Call | **No** | 6.0 |
| Nonbranded | Repeat Phone Call | No | 3.0 |

Zero form fills on either Search campaign in 30 days — every real lead from Search right now is a
phone call.

Root cause, confirmed via `campaign_conversion_goal`: Branded has `category=DEFAULT,
origin=WEBSITE` set `biddable=True`; Nonbranded had that same row unset (`None`). That's the exact
switch that decides whether First Time Phone Call counts for a given campaign. This wasn't a blanket
account-level flag — it was campaign-specific, and only Nonbranded had the gap. Checked history: this
has undercounted every month since Nonbranded launched (e.g. Aug: 0 reported vs 6 real; Branded Aug:
14 reported vs 25 real).

Also found, same audit: Branded is losing **89.4% of impression share to Ad Rank on its own brand
name** (`live wire electric`, QS 9-10, budget_lost only 0.9% — budget is not the constraint). Leading
hypothesis: Maximize Conversions with a $62 target CPA was bidding conservatively off this same
starved conversion signal. Same pattern was found and fixed at Watt's Right 2026-08-12 (branded CPA
dropped $287 → ~$21 after closing an equivalent gap). Left this alone for now — see budget-realloc
entry below for the plan to re-check it.

**Deliberately not touched:** `Calls from ads` (call-extension click, `PHONE_CALL_LEAD` /
`CALL_FROM_ADS`). Already `biddable=True` at the campaign-goal level on both campaigns, but excluded
because the conversion action itself has `primary_for_goal=False` account-wide. That's an unverified
button click, not a confirmed call — flipping it to primary would inflate "conversions" with the same
kind of fake signal flagged on Proud Pops (button-click miscounted as lead, ~600 fake/qtr). Same
reasoning for `Repeat Phone Call` — not a fresh lead, correctly excluded.

### What was written

`update.py conversion-goal --customer-id 1056617442 --campaign-id 23806096501 --category DEFAULT
--origin WEBSITE --biddable TRUE`

`customers/1056617442/campaignConversionGoals/23806096501~DEFAULT~WEBSITE`: `biddable` unset/None →
`True`. Verified via re-query. Reversible (`--biddable FALSE`).

---

## 2026-09-03 — Nonbranded competitor-name negatives

**Authority:** Edu, in-session. Negative keywords, not a budget change — no approval gate applies.

### What we found

Search terms report (30d, Nonbranded) showed spend on searches for other companies, not Live Wire —
zero conversions on all of them. Checked existing negatives first rather than assuming a blank slate:
the campaign already carries **131 negative keywords** across both Search campaigns, including a
well-built competitor list (`boyer electric`, `wired seattle`, `edmonds electric`, `chargepoint`,
`tesla lynnwood`, `tesla in bellevue`, `tesla of renton`, `tesla dealership`, `tesla charging
station`, and ~35 more "X electric" competitor names) — those terms still showing spend in the 30-day
window is most likely a timing artifact (negatives added partway through the window), not a broken
list.

Genuinely missing, same pattern as the existing list: `bob's electric`, `provident electric`, `unity
electric`, `all wire electric`, `harts electric`, `admiral electric`, `j & j electric`, `hello
electric`.

### What was written

8x `CampaignCriterionOperation` (create, negative, PHRASE match) on
`customers/1056617442/campaigns/23806096501`, matching the account's existing convention:

- bob's electric — `campaignCriteria/23806096501~589694592175`
- provident electric — `campaignCriteria/23806096501~681716412708`
- unity electric — `campaignCriteria/23806096501~308946166773`
- all wire electric — `campaignCriteria/23806096501~369711917501`
- harts electric — `campaignCriteria/23806096501~981591847178`
- admiral electric — `campaignCriteria/23806096501~670976633748`
- j & j electric — `campaignCriteria/23806096501~469046041866`
- hello electric — `campaignCriteria/23806096501~457779755236`

---

## 2026-09-03 — Budget reallocation: Branded → Nonbranded, net $0

**Authority:** Edu, explicit ("go for it"), in-session. Reallocation between existing campaigns at
constant account total — falls outside the "no budget change without written client approval via AM
ticket" gate, which applies to net increases/decreases. Same reading Edu confirmed at Watt's Right
2026-08-03.

### What we found

| Campaign | Budget/day (before) | Actual avg spend/day (30d) | Budget-lost IS |
|---|---:|---:|---:|
| Branded | $80 | ~$38.90 | 0.9% |
| Nonbranded | $40 | ~$41.10 | 27.5% |

Branded was sitting on ~$40/day of unused headroom — its bottleneck is Ad Rank (89.4% lost there, see
first entry above), not budget, so the cap was oversized relative to what it can currently spend.
Nonbranded was the opposite: spending at/above its nominal cap and losing over a quarter of its
available impressions purely to budget.

LSA's $500/day cap deliberately left untouched — best-performing channel by far ($35.90 CPA, 23
leads/30d), nowhere near its cap (~$25/day actual), no reason to touch it.

### What was written

`update.py campaign --customer-id 1056617442 --campaign-id 23665625884 --budget 5000` (Branded,
campaignBudgets/15432023732): $80/day → $50/day.

`update.py campaign --customer-id 1056617442 --campaign-id 23806096501 --budget 7000` (Nonbranded,
campaignBudgets/15537680624): $40/day → $70/day.

Combined stays $120/day, same as before. Both verified via re-query.

### Follow-up owed

Re-check in ~1-2 weeks:
- Nonbranded's budget-lost IS % (should trend toward 0)
- Branded's impression-share/rank-loss (should improve now that the conversion-goal gap is closed and
  it's not competing with Nonbranded for headroom it wasn't using anyway)
- Nonbranded's reported "conversions" (should now reflect real phone-call volume, not 0)

---

## 2026-09-08 — Geo-targeting narrowed to client's requested service area

**Authority:** Edu, in-session, acting on a service-area map the client provided
(`~/Documents/livewire_targeting.png`) — a hand-drawn polygon covering South Snohomish County plus a
thin strip of North King County (Shoreline/Kenmore/Lake City corner). Geo-targeting scope, not a
budget change — no approval gate applies.

### What we found

Both live Search campaigns (Branded 23665625884, Nonbranded 23806096501) were targeting **all of King
County + all of Snohomish County** — including downtown Seattle, Bellevue/Kirkland/Redmond,
Renton/Kent/Auburn/Federal Way, and rural north Snohomish (Marysville, Stanwood, Darrington) — none of
which the client's map asked for. (LSA's own ~50-city service-area list is separately configured and
just as broad — left untouched this round; LSA service-area profile isn't edited the same way as
Search campaign criteria and wasn't in scope here.)

Three cities sat right on the polygon's boundary line — Monroe, Bothell, Woodinville — where Google's
city-level targeting (whole city, not a clipped shape) doesn't perfectly hug a hand-drawn line either
way. Edu's call: include Monroe (core reads as inside the vertex), exclude Bothell and Woodinville
(more area outside the line than in).

### What was written

Added `location` remove support to `delete.py` (previously only had keyword/negative/ad-group/ad) —
`CampaignCriterionOperation.remove` via `campaign_criterion_path(customer_id, campaign_id,
geo_target_id)`, mirroring the existing `negative` removal pattern. Location criterion IDs equal the
geo target constant ID, so no extra lookup needed to build the resource name.

Per campaign (Branded 23665625884, Nonbranded 23806096501):
- Removed: King County (9059806), Snohomish County (9059820)
- Added (19 cities): Mukilteo (1027672), Everett (1027583), Snohomish (1027753), Lake Stevens
  (1027634), Monroe (1027664), Lynnwood (1027647), Edmonds (1027576), Mountlake Terrace (1027670),
  Brier (9194342), Mill Creek (9052439), Shoreline (9052842), Kenmore (1027621), Lake Forest Park
  (9191638), Machias (9218144), Silver Firs (9191794, Neighborhood-level), Martha Lake (9052397),
  Maltby (9052372), Canyon Park (9190260, Neighborhood-level), North Creek (9052537)

Verified via re-query: both campaigns show exactly these 19 city-level targets, county-level targets
gone.

Not found as distinct Google Ads geo-targets: Clearview, Richmond Beach (no dedicated city entry —
Richmond Beach is a Shoreline neighborhood, already covered by the Shoreline target added above).

### Follow-up owed

This is a real narrowing of Search reach (cutting out all of Seattle proper, the Eastside, south King
County, and rural Snohomish). Watch Branded + Nonbranded impression/click volume over the next 1-2
weeks for a real drop-off — if lead volume falls off a cliff, the polygon may need to be revisited with
the client before assuming the narrower targeting is working as intended. Can layer onto the existing
2026-09-03 impression-share re-check.

---

## 2026-09-08 — Coverage re-check: added Bothell back

**Authority:** Edu, in-session, independent re-check of the same map against the just-applied
targeting ("doesn't need to be super precise, but must cover most of the area").

### What we found

Re-reading the polygon fresh (not just trusting the earlier boundary call): Bothell's core reads as
mostly *inside* the line, not edge-adjacent like Woodinville — it sits centrally between Kenmore
(targeted) and Woodinville (excluded), flanked by Canyon Park and North Creek (both targeted, both
effectively Bothell-adjacent neighborhoods). Leaving it out was creating a real hole in the middle of
the covered area, not just a shaved edge. Woodinville still reads as genuinely split by the line —
left excluded.

Rest of the 19-city list checked out fine against the polygon on this re-check. Remaining minor gaps
(Lake City corner of Seattle at the polygon's SW tip, small unincorporated spots — Clearview, Three
Lakes, Chain Lake, Hartford) are too small to threaten "most of the area," and most have no dedicated
Google geo-target anyway.

### What was written

Added Bothell (1027517) to both Branded (23665625884) and Nonbranded (23806096501) via
`create.py location`. Both campaigns now carry 20 city-level targets.

---

## 2026-09-11 — CS-reported booking/call dip: diagnosis

**Authority:** Edu, in-session. Diagnostic audit only, no account mutations this session.

### What we found

CS reported the client is seeing web bookings down ~20% and calls to the business down over the last
30 days, and asked for a check on PPC and web traffic. Pulled 90 days of Google Ads (daily campaign
metrics, LSA leads, real conversions by action, impression share, network settings) and GA4 (channel
sessions, all events, key events) to see what's actually going on before responding.

**GA4 — site traffic is not down:**
- Total sessions actually increased over the period, roughly 900/week in early July to 1,600+/week by
  late August
- Property has zero configured key events and no call/booking event tracking at all — only generic
  page_view/session_start/click/form_start fire. `form_start` (22 total in 90 days) dropped to 0 for 5
  straight weeks in August
- Can't verify or refute the client's specific "bookings" or "calls" numbers from GA4 — not
  instrumented here, presumably tracked in a system we don't have visibility into (GBP, phone system,
  booking tool)

**Google Ads — real decline, but not caused by tracking, network settings, or this month's account changes:**

| | Prior 30d (7/13-8/11) | Last 30d (8/12-9/10) | Change |
|---|---:|---:|---:|
| Search real phone-call leads (`all_conversions`) | 37.3 | 23.0 | |
| LSA charged leads | 31 | 17 | |
| Total PPC+LSA leads | 68.3 | 40.0 | -41% |
| Search impressions | 8,676 | 7,173 | -17% |
| Search clicks | 382 | 352 | -8% |

- Decline is gradual through August — no cliff or spike right after either the 9/3 conversion-goal
  fix/negatives/budget-realloc or the 9/8 geo narrowing. Ruled both out as the cause.
- Network settings confirmed clean on both live Search campaigns (Branded 23665625884, Nonbranded
  23806096501): `target_search_network`, `target_content_network`, `target_partner_search_network` all
  `False` — no Search Partners/Display leak.
- Branded's chronic ~85-90% impression-share-lost-to-Ad-Rank (see 2026-09-03 entry) is flat across the
  period, not worsening — not a new cause.
- No confirmed root cause identified. Told CS it's likely just tighter auction dynamics mixed with some
  seasonality — flagged internally as unconfirmed, not stated as fact.

**Landing pages found live but not yet wired to matching ads:**
- 4 new pages went live today: `/free-ev-charger-estimate`, `/free-generator-estimate`,
  `/old-wiring-inspection`, `/panel-upgrade-electrification` — checked each, well built out (forms,
  phone CTA, testimonials, FAQ, credibility markers).
- Checked every live ad's `final_urls`: none point to these 4 pages yet. Ad groups with an obvious
  matching page (EV Charger Installation / Ev charger, Generators, Panel Installation / Panel &
  Service Upgrades / Panell Installation, Rewiring & Wiring) all still point to the homepage,
  `/contact`, or `/service-area/snohomish`.

### What was written

Nothing — diagnosis only.

### Follow-up owed

- Connect each matching ad group's final URL to its landing page: EV Charger Installation / Ev charger
  ad groups -> `/free-ev-charger-estimate`; Generators -> `/free-generator-estimate`; Panel
  Installation / Panel & Service Upgrades / Panell Installation -> `/panel-upgrade-electrification`;
  Rewiring & Wiring -> `/old-wiring-inspection`.
- Re-check campaign performance 7 and 14 days after the landing pages are live in the ads.
- Still watching the 9/8 geo-narrowing for a real drop-off per that entry's own follow-up — this
  reported dip adds urgency to that check.

---

## 2026-09-15 — Weekly PPC snapshot

**Authority:** Edu, in-session. Read-only pull, no account mutations.

### What we found

Last 7 days, PPC only (LSA excluded — its clicks/impressions show in the account pull but its cost
and conversions come back $0/0 through this endpoint, so summing the two live Search campaigns
equals the true PPC total):

| Metric | Value |
|---|---:|
| Spend | $616.65 |
| CPC | $10.11 |
| Total Conversions | 2 |
| Conv Rate | 3.28% |
| Branded Conversions | 2 |
| Unbranded Conversions | 0 |
| Branded CPL | $81.26 |
| Unbranded CPL | N/A (0 leads on $454.12 spend) |
| CPL (blended) | $308.32 |
| Search Impression Share (account) | 9.99% |

Unbranded (`TSD_04.28_Search_Nonbranded_Evergreen`) went the full week with 0 tracked conversions on
$454 spend — worth watching given the conversion-goal gap on this same campaign was only just closed
2026-09-03. Not diagnosed further this session (no `all_conversions`/conversion-action segmentation
pulled — just the standard weekly bundle).

### What was written

Nothing — read-only.

### Follow-up owed

- If Unbranded's 0-conversion week repeats next check-in, re-run the conversion-action segmentation
  (same method as the 9/3 audit) to confirm the goal fix is still holding and this isn't a tracking
  regression, not just a soft week.

---

## 2026-09-15 — Tracking rebuild + website/GTM flag

**Reported by Edu via chat, not executed by Claude this session.**

Tracking rebuilt and fixed. Old tags deactivated to make sure they don't disrupt or interfere with
the new setup.

**Flagged:** the client's website has changed and no longer carries GTM. Sha (WebDev) says the
change wasn't his; Alex also says it wasn't his. Checking with the client to find out who made the
change and why GTM is missing.
