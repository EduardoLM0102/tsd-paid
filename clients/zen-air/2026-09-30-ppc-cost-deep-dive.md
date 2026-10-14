# Zen Air PPC: why conversions cost so much (deep dive, 2026-09-30)

Account `4360840956`. Read-only analysis, no changes made. Window is **2026-08-31 to 09-29** (30 days,
all traffic clean after the 08-26 geo fix) unless noted. Scripts: `google-ads-ratos/scripts/zenair_deepdive_0930_*.py`,
`zenair_st_classify_0930.py`, `zenair_ga4_lp_0930.py`, `zenair_lsa_0930.py`, `zenair_ctc_0930.py`.

## The real number

| | Branded | Non-branded | Account |
|---|---|---|---|
| Spend | $815 | $4,223 | **$5,038** |
| Clicks | 119 | 150 | 269 |
| Avg CPC | $6.85 | **$28.15** | $18.73 |
| Reported conversions | 2 | 18 | 20 → $252 CPL |
| Connected 60s+ calls (`call_view`) | 2 | 10 | 12 |
| Real form fills | 0 | 1–2 (the 09-15 one may be a test) | 1–2 |
| **Real leads** | 2 | ~11–12 | **~13–14 → ~$360–390 per lead** |

The 6–7 conversions that are not real leads are: 4× `[TSD] Click to call` (taps, see finding 5),
1× `ghl_contact_us` (still suspect), 1× Peach AI booking on 09-22 (same day as a 291s call, probably the same person).

Non-branded is 84% of spend. At ~7.7% click-to-real-lead, **every $10 of CPC is ~$130 of CPL**. The CPC
is the problem.

## Finding 1: Non-branded is mostly buying competitor names

Search terms, 08-27 to 09-29 (visible terms = $3,181 of non-branded spend; ~27% of account spend is hidden by Google):

| Bucket | Spend | Clicks | Conv | CPC |
|---|---|---|---|---|
| Other companies' names, manufacturer help lines, supply houses | **$2,777 (87%)** | 100 | 11 | $27.77 |
| Real service searches ("hvac free estimate", "ac repair near me"...) | $381 (12%) | 8 | 2 | $47.63 |
| Zen Air's own name | $23 | 1 | 0 | |

Top examples: shumate heating and air $254, goodman ac unit $154 (1 click), zone heating and air $119,
e dennis plumbing $116, anytime heating and cooling $101 (1 click), bardi hvac $100, goodman hvac $99 (1 click),
reliable heating and air $89, zerorez duct cleaning $79, coolray (3 variants) $188, lennox help line $57,
daikin tech support phone number $23, ed's supply doraville $46.

11 of the 13 non-branded conversions visible in the search-term report came from these names. The 3 from
"e dennis plumbing" are one person counted 3 times (form + tap + ghl_contact_us on 09-15). **Correction
(same day):** I first guessed these were misdials. Matched to `call_view`, the competitor-search calls ran
65s to 367s, so they look like real conversations: 7 of the ~10 real non-branded calls. See update below.

**Cause:** 30 keywords in 1 ad group (20 BROAD), but only 5 got impressions; zero negative keywords;
uncapped Maximize Conversions. `hvac contractors near me` BROAD alone is **60% of all account spend**
($3,037), **Quality Score 3** (expected CTR Below Average, landing page Below Average). Broad match plus
a bidder hunting for calls found that competitor-name searchers call, so it chases them at $25–150 a click.

## Finding 2: Maximize Conversions has no leash

`$150/day` budget, no target CPA, spending the full budget every week. The pool it can win with QS 3 is
small, so it pays whatever it takes to spend the budget. Conversion signal is ~12 real events a month,
and part of it is competitor misdials, so Smart Bidding is learning the wrong thing.

Note: on a budget-capped campaign like this, negatives alone move spend, they don't cut it. They have to
come with a bid cap (or budget cut), or the bidder just pays more for what is left.

## Finding 3: The "branded" campaign's waste is the `zen air` BROAD keyword (and the 09-07 read was wrong)

- The ad group has 8 brand BROAD keywords; `zen air` BROAD is the one that spent. Since 08-17: **$1,625, 0 conversions.** Since 09-07: $665 of $747 branded spend (89%).
- It matches "hvac", "what is hvac", "ac unit for house price", "goodman ac units reviews", competitor names.
- Real brand keywords (exact/phrase) cost **~$123 in 30 days** for 2 conversions. True brand need is ~$4/day
  against a $50/day budget.
- The 09-07 entry said branded was rank-limited on its own name and raised the Target IS ceiling $4→$8.
  **That diagnosis was wrong.** The lost impression share came from the broad keyword entering generic
  auctions it could not win at $4. Raising the ceiling let it win them: its impressions went 256 → 1,183
  the week of the change, CPC $3.27 → $7.46, conversions 0 since.

## Finding 4: The new landing page is not converting forms

`/book-hvac-service/` since 09-15 (GA4, google/cpc): 41 sessions, 17 engaged, 59% bounce, **0 form
submits**, 1 phone tap. Tracking works: a Tag Assistant test on 09-15 fired `generate_lead`. The old
contact page (still reached via sitelinks) produced 1 form + 3 phone taps from 19 sessions. Small
samples, but in the whole clean window (since 08-27) GA4 shows only ~1–2 real form fills from paid
traffic. Almost everything is phone.

Landing page experience is Below Average on the main keyword. It was also Below Average in July on the
old URL, so this is long-standing, not caused by the 09-15 switch.

`LP | Qualified Lead`, `LP | Call Now Click`, `LP | Booking Click`, `LP | Disqualified Lead` are all
secondary and have never recorded a conversion.

## Finding 5: Conversion counting inflates the reported CPL's denominator

- `[TSD] Click to call` (created in the 09-15 rebuild) is type **CLICK_TO_CALL**: it counts a tap on
  the number, not a connected call. It is primary and biddable, in the same PHONE_CALL_LEAD /
  CALL_FROM_ADS bucket as `Calls from ads` (60s+). On 09-22 a tap and a 291s call both counted.
  Its 4 firings (09-15, 09-22, 09-26, 09-29) line up day for day with GA4 `phone_click` from google/cpc.
- `ghl_contact_us` still primary (open since 08-24).
- Non-branded bids on PURCHASE/WEBSITE (GA4 ghl_* events) and DOWNLOAD/APP goals too.

## Smaller items

- **After-hours spend:** non-branded spent $546 after 6pm (2 conv) and $94 before 8am (0). The two calls
  after 9pm lasted 11s and 4s. Worth an ad schedule once Zen Air's answering hours are confirmed.
- **Short calls:** 9 of 25 ad calls since 08-31 lasted under 15 seconds (hang-ups, misdials or no answer).
- **Device:** 88% of non-branded clicks are mobile. Nothing to change.
- **Geo:** traffic is inside the 5 × 7-mile circles (Cumming, Lawrenceville, Johns Creek, Berkeley Lake,
  Tucker...). Fine now.
- **Ads:** both campaigns send every click to `/book-hvac-service/`. Branded ad headlines are generic
  ("AC Repair Duluth GA", "HVAC Contractors Georgia") instead of leading with Zen Air.
- **LSA** (`3740502923`): re-enabled 09-10 by access@topservdigital.com. Serving ~15 impressions/day,
  1 charged lead in September. Most lead records since June are DECLINED on the business side.
- **Budget history:** 09-09 Edu moved $50/day from branded to non-branded (total unchanged at $200).
- **Season:** late September is shoulder season in Atlanta, so volume is soft. That explains volume,
  not a $28 CPC.

## Recommended moves, in order

1. **Branded: pause the BROAD brand keywords.** (Ceiling: see update, kept at $8.) Branded isn't budget-limited, so this is a
   real spend cut (~$600–700/mo) with no budget change and no lead loss.
2. **Non-branded: put a cap on the bidder.** Suggest Maximize Clicks with a ~$15–18 max CPC for 3–4
   weeks, then Max Conversions + target CPA once there are 20+ clean conversions a month.
   Alternative: Max Conversions with a target CPA now; with ~12 real conversions a month it will likely
   throttle hard.
3. **Non-branded: shared negative list** of competitor, manufacturer, supply-house and "tech support /
   help line" terms (~100 names from the search terms), on both campaigns. Only works together with #2.
4. **Non-branded: rebuild keywords.** Swap the 4 broad keywords for phrase/exact service themes in their
   own ad groups (heating/furnace repair first for the season, then AC repair, HVAC service, replacement,
   maintenance), each with matching RSA headlines. This is the QS 3 fix.
5. **Landing page:** CRO pass on `/book-hvac-service/` (form above the fold, click-to-call, service-
   specific versions). Goes to whoever owns web/GHL via ticket.
6. **Conversion hygiene:** move `[TSD] Click to call` and `ghl_contact_us` out of primary. Reported CPL
   will go up toward the real number. Compare weeks with `all_conversions` across the change.
7. **Ad schedule** after confirming answering hours (~$400–500/mo).

Arithmetic, not a promise: at today's ~7.7% real-lead rate, a $16 CPC gives ~$210 per real lead. Some of
today's "leads" are competitor misdials, so cutting those terms will also cut some reported conversions.

**Approval note:** #1–#4, #6 and #7 don't change the total account budget. A CPC cap will likely make
non-branded underspend on its own. Lowering the $150 or $50 daily budgets explicitly counts as a budget
change and needs written client approval through Andrea's AM ticket.

## Update 2026-09-30, executed (Edu approved in chat)

Script `google-ads-ratos/scripts/zenair_change_0930.py` (validate_only dry run first, then applied), verified
by read-back (`zenair_verify_0930.py`). Rollback snapshot: `snapshot-2026-09-30-pre-negatives-bidcap.json`.

- **Non-branded ad group 205687909824: 202 negatives** (178 phrase, 24 exact): ~170 local competitor names,
  supply houses + "tech support"/"help line", bare manufacturer names as EXACT only (so "lennox ac repair" still
  serves), and `zen air`/`zenair`/`callzenair` so brand searches go to the branded campaign.
- **Non-branded bidding: Maximize Conversions → Maximize Clicks, $18 max CPC.** Budget unchanged ($150/day).
- **Branded: all 8 BROAD brand keywords paused.** 10 exact + 10 phrase brand keywords stay live. In 90 days the
  exact/phrase keywords matched only queries containing "zen"; every non-brand query came through broad.
- **Branded campaign: 206 new negatives** (same competitor/supply/support/manufacturer set + jobs/careers/hiring/
  salary/employment), on top of the 4 existing. Safety net in case a broad keyword gets re-enabled.
- **Branded ceiling kept at $8, not lowered to $5.** Exact brand keywords run 81–100% IS at $4.23–5.26 avg CPC
  and still lose 12–16% to rank at $8. The ceiling only caused waste because of the broad keyword.

No total-budget change, so no written approval needed; still goes on Andrea's AM ticket with the rest.

**Competitor calls look real** (non-branded `call_view` matched to search-term conversions by day):
09-04 13:38 109s ed's supply doraville · 09-10 12:07 65s all good services · 09-16 15:06 128s cool air mechanical
atlanta · 09-17 13:21 249s zone heating and air · 09-22 17:11 291s shumate heating and air · 09-23 13:33 367s
goodman ac unit · 09-28 17:28 94s cool ray. Ask Eddie to check these in his call log: booked jobs, or people
asking for the other company? Expect non-branded conversions to drop sharply until the service rebuild lands.

**Watch in 3–4 days:** Max Clicks plus 20 broad keywords can chase cheap, irrelevant clicks. Check search terms.
