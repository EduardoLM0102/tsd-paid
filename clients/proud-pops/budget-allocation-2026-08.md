# Proud Pops — $50,000 Budget Allocation (through Aug 31, 2026)

**Account:** 1051843378 (PPC) · **Date:** 2026-07-30 · **Source:** Google Ads API, pulled 2026-07-30
**Companion to:** `budget-brackets-and-keyword-research.md` (Jul 23), `rank-loss-remediation-2026-07-23.md`
**Approved:** $50,000 total pool through Aug 31.

---

## 1. Headline: the constraint flipped

The July 23 analysis concluded the account was **rank-limited, not budget-limited** — 50–85% of
impression share lost to Ad Rank, only 3.5–29.5% to budget — and recommended holding budget until
the conversion signal came back.

**The signal came back on July 22–23, and the constraint flipped.** Comparing the trailing 30 days
against the clean post-fix window:

| Campaign | Lost to BUDGET (30d) | Lost to BUDGET (Jul 22–29) | Lost to RANK (30d) | Lost to RANK (Jul 22–29) |
|---|---:|---:|---:|---:|
| Search Nonbranded Electrical | 36.4% | **46.9%** | 51.3% | 42.9% |
| Search Nonbranded Plumbing | 17.4% | **44.4%** | 68.9% | 40.6% |
| PMax Electrical | 17.5% | **41.0%** | 67.2% | 44.4% |
| PMax HVAC | 20.6% | **25.5%** | 64.4% | 59.8% |

Rank-lost share fell 20–28 points across the board and budget-lost share roughly doubled. That is
exactly what should happen when Maximize Conversions stops bidding at the floor: the GTM conversion
fix (live v38, Jul 23) gave the bidder real data, Ad Rank recovered, and the campaigns now run out
of money instead of running out of rank.

**The gate the July 23 doc set — "spending toward BETTER/BEST only makes sense once the signal is
back" — is cleared.** Budget is now the binding constraint. This is the right moment to fund it.

### The conversion signal, confirmed

Every conversion recorded in the last 30 days landed in the last 8 days. Before Jul 22 the account
was recording effectively zero.

| Conversion action | Primary | Jul 15–29 volume |
|---|---|---:|
| `TSD - Website Call` | Yes | 32.0 |
| `Website lead` | Yes | 11.0 |
| `local_services_phone_lead` | Yes | 7.0 |
| `local_services_message_lead` | Yes | 5.0 |
| `instant_quote_hvac_click` | **No** (correctly non-biddable) | 182.0 |

Daily conversions: 0–2/day through Jul 21, then 2.3 → 3.7 → 9.0 → 4.5 → 3.5 → 12.0 → 7.0 → 9.0.

---

## 2. The clean baseline (Jul 22–29, 8 days)

This is the only window with working tracking. All CPA figures below come from it. 30-day CPAs in
the account UI are meaningless — they divide a month of spend by a week of conversions.

| Campaign | ID | $/day | Conv | **CPA** | IS | Lost budget | Lost rank |
|---|---|---:|---:|---:|---:|---:|---:|
| PMax Electrical | 23866982084 | $61.92 | 16.5 | **$30.02** | 14.6% | 41.0% | 44.4% |
| PMax HVAC | 23853595615 | $85.62 | 18.5 | **$37.03** | 14.7% | 25.5% | 59.8% |
| Search Nonbranded Electrical | 23866999121 | $50.99 | 5.0 | **$81.58** | 10.2% | 46.9% | 42.9% |
| Search Nonbranded Plumbing | 23853484024 | $84.32 | 3.0 | **$224.86** | 15.0% | 44.4% | 40.6% |
| **PPC total** | | **$282.85** | **43.0** | **$52.62** | | | |
| In-account LSA | 20067257249 | $117.13 | 8.0 | $117.13 | — | — | — |

**Caveat on CPA:** these are cost per *tracked lead*, not per booked job. The signal is 8 days old
and has not been validated against ServiceTitan outcomes. Treat $52.62 as a directional floor, not
a proven acquisition cost.

### LSA is demand-limited, not budget-limited

All three LSA surfaces carry a $714.29/day budget and none comes close to spending it:

| LSA surface | Account | Budget/day | Actual/day (30d) | Conv | CPA |
|---|---|---:|---:|---:|---:|
| In-account LSA | 1051843378 | $714.29 | $105.71 | 31 | $102.30 |
| LSA Electrician | 7261668241 | $714.29 | $38.02 | 19 | $60.03 |
| LSA HVAC | 6621969129 | $714.29 | $55.78 | 21 | $79.68 |
| **Total** | | | **$199.51** | **71** | **$84.29** |

LSA has 7x headroom on paper and does not use it. **Extra dollars into LSA do nothing** — it is
constrained by lead demand, review profile and ranking, not by budget. Any LSA gain comes from
bids, reviews and geo, not from this $50k. Budget the LSA line at its run rate (~$6,200/mo) and
spend the increment on PPC.

---

## 3. The honest ceiling: the current structure cannot absorb $50,000

$50,000 over Aug 1–31 is **$1,613/day**. Current PPC run rate is **$283/day** — a 5.7x increase.

Buying back 100% of the impression share currently lost to budget, on the four live campaigns:

| Campaign | Now $/day | IS now | IS at full budget | Multiplier | Ceiling $/day |
|---|---:|---:|---:|---:|---:|
| Search Nonbranded Electrical | $51.0 | 10.2% | 57.1% | 5.58x | $284.7 |
| Search Nonbranded Plumbing | $84.3 | 15.0% | 59.4% | 3.96x | $333.9 |
| PMax Electrical | $61.9 | 14.6% | 55.6% | 3.82x | $236.6 |
| PMax HVAC | $85.6 | 14.7% | 40.2% | 2.73x | $233.8 |
| **Total** | **$282.8** | | | | **$1,089** |

**$1,089/day = $33,760/month.** That is the theoretical maximum the four existing campaigns can
absorb, and it is optimistic — incremental impression share costs more per point than the share you
already hold, because you win the cheap auctions first.

$50,000 − $33,760 = **~$16,240 has nowhere to go** inside the current structure. It has to come from
new inventory, or it will be spent by bidding up CPCs on the same auctions, which raises CPA without
raising lead volume.

---

## 4. Before any money moves: the July 23 fix list was never executed

This is the most important finding in this doc. Items 2–5 of the remediation plan are still open,
and the account is still leaking at the same rate.

### 4.1 The live campaigns have zero negative keywords

There is a **758-member shared negative list, `CSMS_Negatives`, already built in the account.** It is
attached to nine PAUSED legacy campaigns and to **none of the live ones.** Neither live Search
campaign has a single campaign-level negative.

Search terms, Jul 22–29 — of **$585 in visible term spend, roughly $414 (71%) cannot become a lead:**

| Bucket | Cost | Examples |
|---|---:|---|
| Competitor brands | ~$250 | `the bearded plumber san antonio` $86.04 (1 click), `george's plumbing` $40.26, `zeus plumbing` $37.97, `shafer services` $34.11, `quan air` $20.70, `elmer zubiate plumbing` $14.65, `royal flush plumbing` $12.80 |
| Own brand in nonbranded | ~$84 | `proud pops san antonio` $37.81, `proud pops plumbing` $28.27 + $6.87, `problem solvers san antonio` $7.71 |
| Cross-service in Electrical | ~$80 | `cheapest ac repair san antonio` $37.54, `hvac specials near me` $18.66, `hvac contractors in my area` $18.01 |

Only ~54% of search spend is visible (the rest is privacy-thresholded), so true waste is higher.

**At $283/day this waste costs ~$5,300/mo. At $1,613/day it costs ~$30,000 of the $50,000.**
Scaling before the negatives are in is the single most expensive mistake available here.

### 4.2 AI Max is still on

`cheapest ac repair`, `hvac specials near me`, `mini split ac san antonio` and `free ac installation`
are all still being served by the **Electrical** campaign. AI Max, final URL expansion and
auto-created assets — enabled by brandon@proudpops.com on 2026-06-26 — are still running.

### 4.3 Search Nonbranded Plumbing is serving on Display

`target_content_network = True` on campaign 23853484024. A Search campaign running Display
inventory, on the account's worst performer ($225 CPA, 3 conversions). Search partners are also on
for both live Search campaigns.

### 4.4 The Branded campaign is still paused

23853361615 sits PAUSED with 31 keywords across 5 ad groups and 5 enabled ads (2 EXCELLENT, 3 POOR)
— while brand searches pay $28–38 per click inside the nonbranded campaigns.

---

## 5. Where the new inventory comes from

### 5.1 Search Nonbranded HVAC is built, ready, and paused — in August

Campaign **23848895678**, budget already set at $100/day, PAUSED since build:

| Ad group | Keywords | Ad strength |
|---|---:|---|
| AG1_HVAC_ACRepair | 8 (`ac repair near me` exact, `ac repair san antonio` exact, `emergency ac repair san antonio` …) | GOOD |
| AG2_HVAC_Installation | 8 (`ac installation san antonio`, `ac replacement san antonio` …) | GOOD |
| AG3_HVAC_Maintenance | 8 (`ac tune up san antonio`, `hvac service near me` …) | GOOD |

**There is currently no non-branded HVAC Search campaign live at all** — HVAC search demand is served
only by PMax, which the account cannot control at the query level. The July 23 keyword research put
AC repair at **4,500+ searches/month in San Antonio at LOW–MEDIUM competition**, and this is peak
cooling season. This is the largest single opportunity in the account and it needs zero build work.

Note: expect PMax HVAC's search share to shift into this campaign once it is live — exact/phrase
Search generally outranks PMax on the same query. That is the intended outcome (controllable
inventory), but judge the two together, not separately.

### 5.2 Geo: HVAC and Plumbing are targeting San Antonio city only

| Campaign | Geo targets |
|---|---|
| PMax HVAC, Search Plumbing | San Antonio **only** |
| PMax Electrical, Search Electrical | San Antonio, Boerne, Helotes, New Braunfels, Fair Oaks Ranch |
| LSA | **47 cities** across the metro |

The business demonstrably services the wider metro — LSA runs in 47 cities. Bringing HVAC and
Plumbing up to at least the 5-city Electrical footprint is free incremental inventory with no new
build, and it raises the $33,760 ceiling in §3.

### 5.3 AC install/replace deserves its own campaign

Per the July 23 research: repair is ~4,500 searches/mo, install/replace is under 1,000 but at a far
higher ticket. In one campaign, repair volume eats the budget and starves install, and a bid tuned
for a $200 repair call is wrong for a $6,000 system quote. Split AG2 out into its own campaign.

### 5.4 Water treatment — rebuild, not relaunch

Campaign 23875125989 is a **SMART campaign with zero keywords**. It cannot be un-paused into
anything useful. Rebuild as a standard Search campaign on the softener cluster (~1,600 service-intent
searches/mo, $3–11 top-of-page bids vs $20–30 CPCs on core plumbing terms), with retail negatives
(`brita`, `berkey`, `pitcher`, `countertop`, `refrigerator`, `replacement cartridge`).

### 5.5 One leak to close

`TSD_05.14_Leads_Search_Nonbranded` — a Search campaign sitting **inside LSA account 6621969129**,
spending $481.69/30d at **$20/day with zero conversions**. Orphaned where nobody looks at it.
Pause it or fold it into the main account.

---

## 6. Recommended allocation — August (31 days)

| # | Campaign | Now $/day | **Aug $/day** | **Aug total** | Rationale |
|---|---|---:|---:|---:|---|
| 1 | Search Nonbranded HVAC *(relaunch 23848895678)* | $0 | **$250** | **$7,750** | Built and ready, peak AC season, 4,500 searches/mo, no HVAC Search live today |
| 2 | PMax HVAC | $85.6 | **$240** | **$7,440** | CPA $37, absorbs full budget-lost share |
| 3 | PMax Electrical | $61.9 | **$210** | **$6,510** | CPA $30 — best in the account |
| 4 | Search Nonbranded Electrical | $51.0 | **$180** | **$5,580** | 46.9% budget-lost; only after AI Max off + negatives |
| 5 | Search Nonbranded Plumbing | $84.3 | **$120** | **$3,720** | **Deliberately capped** — $225 CPA, 3 conversions |
| 6 | AC Install/Replace *(new split)* | $0 | **$90** | **$2,790** | Different buyer, different bid, high ticket |
| 7 | Water treatment *(rebuild)* | $0 | **$60** | **$1,860** | $3–11 clicks vs $20–30 core plumbing |
| 8 | Search Branded *(relaunch 23853361615)* | $0 | **$45** | **$1,395** | Stops the $28–38/click brand leak |
| | **PPC subtotal** | **$282.8** | **$1,195** | **$37,045** | |
| | LSA (3 accounts, at run rate) | $199.5 | $200 | $6,200 | Demand-limited — more budget does nothing |
| | **Allocated** | | | **$43,245** | |
| | **Performance reserve** | | | **$6,755** | Deploy mid-month into whatever holds CPA |

**Why I am not allocating the full $50,000 up front.** The efficient ceiling for August is around
$43k. The remaining $6,755 should be held and released around Aug 15 into whichever campaigns are
holding CPA — most likely HVAC Search if AC repair performs the way the keyword data suggests.
Committing it on day one just bids up CPCs on auctions the account is already winning.

**Plumbing is capped on purpose.** It has the second-highest budget-lost share (44.4%) so the
mechanical read says "fund it." But it converts at $225 with 3 conversions, still loses 40.6% to
rank, is the campaign serving on Display, and sends service queries to the homepage. Fix the
routing and the negatives, prove the CPA, then fund it. This is the one place where lost impression
share is the wrong signal to act on.

---

## 7. Sequencing — the order matters more than the amounts

**Gate 1 — before a single dollar moves (Jul 30–31):**
1. Attach `CSMS_Negatives` (758 members, already exists) to both live Search campaigns
2. Add own-brand negatives — `proud pops`, `problem solvers`, phrase — to both nonbranded campaigns
3. Add the competitor list from `rank-loss-remediation-2026-07-23.md` §3.2, plus the new ones this
   pull surfaced: `the bearded plumber`, `george's plumbing`, `shafer services`, `quan air`,
   `elmer zubiate`, `royal flush plumbing`, `vamvoras plumbing`
4. Turn OFF AI Max, final URL expansion and auto-created assets on 23866999121
5. Turn OFF Display on 23853484024, and search partners on both Search campaigns
6. Point ad groups at `/services/plumbing`, `/services/electrical`, `/services/hvac` instead of the homepage

**Gate 2 — brand defense before scaling nonbranded (Aug 1):**
7. Un-pause Branded 23853361615 at $45/day. Refresh the three POOR ads afterwards.

**Gate 3 — staged ramp, not one jump (Aug 1 → Aug 15):**

Maximize Conversions with 8 days of conversion history will overspend badly if it is handed 5.7x
overnight. Ramp in three steps, each gated on CPA holding:

| Date | PPC $/day | vs today |
|---|---:|---|
| Aug 1 | ~$600 | 2.1x |
| Aug 8 | ~$900 | 3.2x |
| Aug 15 | ~$1,195 | 4.2x |

Relaunch HVAC Search and Branded on Aug 1 at full budget — they are new, so there is no learning to
disturb. Ramp the four existing campaigns.

**Gate 4 — bidding:**
Do not set a tCPA before **~Aug 6–13** (2–3 weeks of clean data from Jul 23). Once there is a real
observed CPA, move PMax Electrical and PMax HVAC to tCPA first — they have the volume and the
lowest CPA. Leave Plumbing on Maximize Conversions until its CPA is credible.

---

## 8. What to watch, and what would make me stop

- **CPA by campaign, weekly.** The $52.62 blended PPC CPA is 8 days old. If it doubles on the ramp,
  the ceiling is lower than §3 suggests and the reserve should not be deployed.
- **Search terms, twice in week 1.** The negatives are the whole basis for scaling safely. Verify
  competitor and cross-service terms are actually gone before the Aug 8 step.
- **Budget-lost vs rank-lost after the ramp.** If budget-lost share does not fall as budgets rise,
  the money is buying CPC inflation rather than impressions — stop and re-check.
- **ServiceTitan outcomes on the tracked leads.** Nothing here is validated against booked jobs yet.
  This is the same open dependency flagged on Jul 23 and it is still the weakest link in the case
  for spending $50k.

---

## 9. Process note

Per MasterOps, the budget change needs written client approval on record via an AM ticket — and the
**Jul 7 reduction** ($409 → $250/day, by andrea@topservdigital.com) still has no written record. Both
should go on the same ticket so the trail is clean: the July cut, and the August increase off that
reduced baseline. Whoever approves should see that every figure in §6 is an increase measured from a
level that was cut two weeks ago, not from the original plan.
