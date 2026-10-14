# Growth Engine ad-account pull

For Alex, from Eduardo. September 29, 2026, revised October 7, 2026.

## What changed on October 7

- **Roster.** ICS (Meta 2070047533283360) is Integrate Comfort Systems, a current client. On The Way is no longer counted as current (status `offboarding`), so its Google numbers and the Houston market leave the headline. Rhino (849885463684603) stays unconfirmed: its ads run in Oklahoma, so it isn't Lily Pad (Kansas). Your New Door had no delivery.
- **Cool Hand campaign split (your open item 3): closed.** One campaign, Ad Recall Lift, $505.67, which equals the account total to the cent. Its weekly rows are now in 05b.
- **Meta market breakdown (your open item 4): closed, not usable.** `comscore_market` returns "Unknown" for 93% of Napps' 12-month spend and 45% of Zen Air's. State-level `region`, which your baseline has, is the usable Meta geography. See item 2.
- **On The Way's Meta (your open item 2): dropped.** On The Way is offboarding, and its awareness campaign only ran Sep 4 to 11.
- **New item 7: where awareness impressions land, and which template bought them.** Pulled campaign-level placements plus each ad set's optimization goal. Reach campaigns put 55% of their impressions on Facebook Marketplace. Ad Recall Lift campaigns put 0.4%.
- **Correction.** The September template table counted Mission Accomplished's older awareness campaign as Reach. Its ad sets are Ad Recall Lift, so the Phoenix row compared Ad Recall Lift with Ad Recall Lift. The table now uses each campaign's actual optimization goal (item 2).
- **Numbers that moved:** Meta awareness CPM $2.87 to $2.88 (Q3 $3.47 to $3.51). Awareness frequency 1.77x unchanged, weeks at 3x 2.7% to 2.6%. YouTube in-stream $8.91 to $8.76. PMax YouTube $4.82 to $5.06. CTV $12,692 to $11,745. Markets with a brand CPM: 9 of 14 to 8 of 13. Everything else is unchanged.
- **Access note.** Gillespie's Meta account (2014320269203822) stopped being readable after the September 28 pull. Its 12-month numbers are from that pull. Only its ad-set goal and placement split are missing.

Window for everything: 52 full Monday to Sunday weeks, **2025-09-29 to 2026-09-27**, each account in its own time zone. All accounts are USD. Meta came from the Meta Ads connector, Google from the Google Ads API under the TopServ MCC. Every metric in the CSVs is straight from the platform. The only things added on top are labels (client, market, roster status) and simple arithmetic, like CPM and impressions ÷ 3.

**Scope.** Headline numbers cover current TSD clients only, using the same rule on both platforms. `client_roster.csv` lists every account in the pull, its status (current, offboarding, offboarded, not current, unconfirmed, internal) and where that status came from. Frequency numbers also drop weeks from before TSD took an account over: On Time Service Pros' Meta before March 2026 and Lily Pad's Google before 2026-08-20 (Search only, so it changes nothing). Those weeks stay in CPM, since price is price no matter who bought it. Tables 01 and 03 also carry "all accounts" columns (everything we can see except TopServ's own ad accounts), and the row-level files carry each account's roster status, so you can compare either way.

## Answer first

1. **Frequency (item 5): no, we are not delivering 3x a week.**
   - Per client on Meta (all campaigns, people deduplicated within each week), the median weekly frequency is **1.88x**. Only **13 of 331 client-weeks (3.9%)** reached 3x, and 4 of those came from a hiring ad, not brand.
   - Brand campaigns alone: median **1.77x**, with **2.6%** of weeks at 3x. YouTube: median **1.83x**, with 15.3% of weeks at 3x, all from two small campaigns.
   - These are per-platform numbers. Nothing deduplicates people across Meta and YouTube, so the platform figures can't settle it on their own. Raw volume can: weekly impressions ÷ 3 is the most adults a client's delivery could possibly reach 3 times. **Our biggest client (Zen Air) tops out around 65,000 adults a week. The median client is around 14,500.** One ZIP (30096) has 54,888 adults. Any zone larger than those numbers cannot be at 3x, however the impressions are spread.
2. **The CPM constants sit well above delivered brand CPMs.**
   - Meta awareness/reach delivered at **$2.88** over 12 months (**$3.51** in Q3).
   - YouTube in-stream delivered at **$8.76**, and YouTube inside Performance Max at **$5.06**. In-feed came in at $2.22, but that's one campaign now, so don't price from it.
   - $12.64 / $14.21 / $20.08 look like our conversion CPMs instead: Meta lead campaigns ran **$20.13**.
3. **Market tiers: the buying setup moves CPM more than market size does.** In the four markets that ran both, the Meta "Ad Recall Lift" template cost 1.5 to 1.8x the Reach template. With the template held constant, big DMAs (New York, Dallas, Atlanta) came in cheaper than small ones, not pricier.
4. **Only 8 of the 13 markets our current clients run in have a delivered brand CPM at all.** Louisville, Minneapolis, New Orleans, Seattle and Wichita have either no brand campaign or too little to price. There's nothing there yet to replace a constant with.
5. **OTT/CTV (item 4): no OTT or CTV buy in any TSD Meta or Google Ads account.** YouTube already reaches TV screens, though: **$11,745 and 1.16M impressions** served to connected TVs at a **$10.10 CPM**. That includes **66% of all our standalone YouTube spend**. I did not check vendors outside Meta and Google Ads.
6. **Most of our YouTube is hidden inside Performance Max.** PMax put **$72,243** on YouTube, 4.1x what our Video campaigns spent. Google reports neither a format split nor frequency for it.
7. **More than half of our Reach impressions run on Facebook Marketplace (new, item 7).** Reach campaigns put **55%** of their impressions there (25% to 98% by campaign), and the two Reach campaigns launched since June (Spencer Air, All Seasons) put 92 to 98%. Ad Recall Lift puts **0.4%** there. Marketplace isn't why Reach is cheap: Reach costs $2.80 outside Marketplace, against $4.28 for Ad Recall Lift. But if a Marketplace impression shouldn't count toward the 3x floor, Reach costs **$6.02 per thousand counted impressions**, and Ad Recall Lift ($4.29) becomes the cheaper way to buy the floor.

## Item 1. Delivered CPM by platform and objective

File: `01_cpm_by_platform_and_objective.csv` (campaign detail in `01b_campaign_detail_both_platforms.csv`). Recruiting campaigns (hiring ads) are split out so they don't distort customer CPMs.

| Platform | Objective / channel | Accounts | Spend 12 mo | Impressions | CPM |
|---|---|---|---|---|---|
| Meta | Awareness / Reach | 12 | $39,165 | 13.59M | **$2.88** |
| Meta | Traffic | 4 | $17,354 | 1.88M | $9.24 |
| Meta | Engagement | 2 | $823 | 74k | $11.07 |
| Meta | Leads / Conversions / Sales | 11 | $123,772 | 6.15M | **$20.13** |
| Google | Video (YouTube) | 3 | $17,730 | 2.07M | $8.58 |
| Google | Demand Gen | 1 | $842 | 367k | $2.29 |
| Google | Display | 2 | $1,901 | 1.11M | $1.71 |
| Google | Performance Max, all networks | 17 | $354,892 | 20.37M | $17.42 |
| Google | PMax, YouTube network only | 17 | $72,243 | 14.29M | $5.06 |
| Google | PMax, Display network only | 17 | $60,160 | 4.79M | $12.56 |

Current clients only. Search ($434.14), Smart ($23.39) and Local Services ($826.11) CPMs are in the file for completeness. Those channels are priced per click or per lead, so their CPMs mean nothing for brand sizing. The Google rows moved on October 7 because On The Way left the headline: its PMax bought a lot of cheap Display inventory, which is why PMax Display went from $7.49 to $12.56.

Seasonality (`07_cpm_by_quarter.csv`): Meta awareness CPM went $2.77 (Q4-25), $2.15 (Q1-26), $3.18 (Q2-26), $3.51 (Q3-26). Summer costs about 60% more than winter.

## Item 2. Delivered CPM by market

- **Google by DMA:** `02a_google_cpm_by_dma.csv`. Google's "metro" is the Nielsen DMA, based on where the user physically was. It covers 99.0% of Google spend.
- **Meta by market:** `02b_meta_cpm_by_client_market.csv`. Each client serves one DMA, so account CPM is the market CPM. The DMA is assigned from the client's service area (taken from its Google metro delivery), not from a Meta geo breakdown.
- **Meta's own market breakdown doesn't work for this.** Meta retired `dma` and points to `comscore_market`. Over the 12 months it returned "Unknown" for $14,816 of Napps' $15,935 (93%) and for $18,989 of Zen Air's $41,969 (45%). Raw: `raw/meta_comscore_market_check.csv`. State-level `region` (in your September 28 baseline) is the usable Meta geography. It shows one place where "one DMA per client" breaks: about a third of Napps' last-90-day delivery landed in Louisiana and Arkansas.
- **Side by side:** `02c_market_summary_brand_cpms.csv`, one row per DMA with $500 or more of brand-relevant spend.
- **Coverage:** `02d_market_coverage.csv`, every market a current client spends in, and whether it has a delivered brand CPM.

Coverage by market:

| DMA | Delivered brand CPM? | Meta awareness | Standalone YouTube |
|---|---|---|---|
| Atlanta, GA | yes | $2.77 | none |
| Cincinnati, OH | yes | $3.27 | $7.46 |
| Dallas-Ft. Worth, TX | yes | $3.18 | $2.29 |
| New York, NY | yes (Integrate's Meta account isn't in this pull, see gaps) | $2.16 | $6.49 |
| Phoenix, AZ (Mohave County) | yes | $3.79 | none |
| San Antonio, TX | yes, YouTube only | none | $10.51 |
| Tulsa, OK | yes | $3.48 | none |
| Tyler-Longview, TX | yes | $3.52 | none |
| New Orleans, LA | too thin to price ($492 of Meta awareness) | | |
| Louisville, KY | no brand campaign | | |
| Minneapolis-St. Paul, MN | no brand campaign | | |
| Seattle-Tacoma, WA | no brand campaign | | |
| Wichita-Hutchinson, KS | no brand campaign | | |

Meta awareness CPM by DMA, same quarter (Q3-26):

| DMA | Clients | Awareness CPM |
|---|---|---|
| New York, NY | All Seasons AC | $2.56 |
| Dallas-Ft. Worth, TX | Cool Hand, King's Window, Spencer Air | $3.02 |
| Atlanta, GA | Zen Air | $3.32 |
| Phoenix, AZ (Mohave County) | Mission Accomplished | $4.23 |
| Cincinnati, OH | GC Home Service, Gillespie's | $4.43 |
| New Orleans, LA | Nick's Heating & Air | $4.76 |
| Tyler-Longview, TX | Napps | $4.88 |
| Tulsa, OK | Watt's Right | $5.14 |

The split that explains most of this is the buying template, not the market (12-month numbers, current clients, template taken from each ad set's optimization goal, file `08b_meta_awareness_goal_summary.csv`):

| DMA | Ad Recall Lift CPM | Reach CPM | Ratio |
|---|---|---|---|
| Cincinnati, OH | $4.43 | $2.45 | 1.8x |
| Dallas-Ft. Worth, TX | $4.76 | $3.07 | 1.6x |
| Tulsa, OK | $5.14 | $3.25 | 1.6x |
| Tyler-Longview, TX | $4.88 | $3.35 | 1.5x |
| All markets | $4.32 | $2.73 | 1.6x |

Corrected October 7: the September version had a Phoenix row ($5.14 vs $3.47). Both of Mission Accomplished's campaigns turned out to be Ad Recall Lift, so Phoenix has no Reach CPM to compare. The $3.47 vs $5.14 gap there is the same template in two different periods (late April to August, then September), not two templates.

The Ad Recall Lift template happens to be running in the smaller markets. If we rule primary, secondary and tertiary tiers straight from market averages, we'll be pricing the template and calling it the market.

## Item 3. YouTube CPM, in-stream vs in-feed

Files: `03_youtube_cpm_by_format.csv`, detail in `03b_youtube_format_detail.csv`.

| YouTube format (Video + Demand Gen campaigns) | Spend | Impressions | CPM |
|---|---|---|---|
| In-stream (skippable) | $15,544 | 1.77M | **$8.76** |
| In-feed | $792 | 356k | $2.22 |
| Shorts | $2,235 | 303k | $7.37 |
| YouTube inside Performance Max (format not reported) | $72,243 | 14.29M | $5.06 |

Things to know:
- In-feed is now a single Demand Gen campaign (Cool Hand). The other in-feed account was On The Way, which has left the headline. Don't price in-feed from $2.22. The September figure across both accounts was $3.84.
- Every standalone YouTube ad group we run is "video responsive" (multi-format). The in-stream vs in-feed split comes from Google's ad format segment, not from how the campaigns were set up.
- GC Home Service's YouTube campaign served entirely as Shorts.
- The buying goal matters here too. Proud Pops ran two YouTube campaigns in the same DMA: the views-goal campaign came in at $7.53 in-stream CPM and the awareness-goal campaign at $17.67.

## Item 4. OTT / CTV

File: `04_ctv_ott_delivery.csv`.

- **No OTT or CTV buy exists in any TSD Meta or Google Ads account.** This is the finding you described. Nobody is deliberately buying the intrusive TV layer through our ad accounts. I did not check vendors outside Meta and Google Ads.
- **Meta:** Meta reports a device for every impression. Across current clients it returned phones, tablets, desktop, iPod and "other" (0.25% of 22.4M impressions), with no TV category.
- **Google:** YouTube is already on TV screens. **$11,745 and 1.16M impressions** served to connected TVs at a **$10.10 CPM**, and 66% of current clients' standalone YouTube spend ran on TVs. Proud Pops alone is $8,832. So the channel exists in the book, just unmanaged as a layer.

## Item 5. Delivered frequency

Files:
- `05a_meta_weekly_frequency_by_client.csv`: one row per client per week (Meta dedupes people across all of that client's campaigns within the week).
- `05b_meta_weekly_frequency_awareness_campaigns.csv`: one row per brand campaign per week.
- `05c_google_weekly_frequency_video_display.csv`: YouTube / Display / Demand Gen, Google's unique users and frequency per user, weekly.
- `05d_frequency_summary.csv`: per client and per campaign: median, max, weeks at 3x or more, median weekly reach, last 4 weeks, and how many pre-TSD weeks were dropped.
- `05e_frequency_book_rollup.csv`: the book-level numbers below, plus the same numbers for every account and every week, for reference.
- `05f_cross_platform_weekly_impressions_by_client.csv` and `05g_cross_platform_summary_by_client.csv`: Meta and Google impressions per client per week, side by side (details below).

Every row in 05a to 05c has a `counts_as_tsd_delivery` column. The headline numbers use only current clients and only weeks TSD ran the account.

| Series | Weeks | Median weekly frequency | Weeks at 3x+ |
|---|---|---|---|
| Meta, per client, all campaigns | 331 | 1.88 | 13 (3.9%) |
| Meta, per client, last 4 weeks only | 49 | 1.87 | 1 (2.0%) |
| Meta, awareness campaigns (weeks with $20+ spend) | 227 | 1.77 | 6 (2.6%) |
| Google, YouTube campaigns | 59 | 1.83 | 9 (15.3%) |

The brand campaigns that did clear 3x all did it on a small slice of the zone:
- GC Home Service's Meta Ad Recall Lift campaign: 6 of 11 weeks at 3x+, on a median of about 9,700 people a week at about $140 a week.
- GC's ZIP-code YouTube campaign: 5 of 7 weeks at 3x+, on about 16,800 people a week.
- Proud Pops' New Braunfels YouTube campaign: 4 of 8 weeks at 3x+, on about 14,400 people a week.
- Mission Accomplished's Google Display "News" placements show 11x a week on about 5,300 people. That's placement noise, not brand reach, and it's not in the YouTube number.

### Frequency is per platform

Read the table above with three limits in mind:
- **Nothing deduplicates people across Meta and Google.** Someone reached twice on Meta and twice on YouTube shows up as 2x on each, not 4x.
- **Performance Max reports no frequency at all,** and it's where most of our YouTube runs.
- **Platform frequency counts only the people reached,** not all the adults in the zone.

Google isn't a rounding error in this. For six clients that also run Meta, YouTube and Display (mostly bought by PMax) are more than half of their brand-type impressions: Neon Monkey 97%, Cool Hand 78%, Mission Accomplished 74%, Hawkins 65%, Watt's Right 56%, Napps 54%. Their real combined frequency is higher than the Meta number alone.

So 05f and 05g give volume instead of frequency. For each current client and week they show Meta impressions and Google YouTube and Display impressions (search excluded), plus the total divided by 3: the most adults that week's delivery could possibly reach 3 times, if every impression landed in the zone and was spread perfectly evenly. Compare that number to the zone's adults 18+. If the zone is bigger, the floor is impossible that week, whatever the overlap. Over TSD-run weeks, the median of that number is about 65,000 for Zen Air, about 38,000 for Proud Pops, and under 20,000 for 15 of the 21 current clients in 05g.

A last caution: **we have no data on what CPM would be at 3x across a full zone.** Delivered CPMs above were bought at about 1.7 to 2x. Pushing frequency up on a fixed audience usually raises CPM, so the delivered CPM should be read as a floor, not the price of the floor.

## Item 6. Meta audience-size estimates

Not in this drop. Meta's audience-size estimate is only available in Ads Manager's audience setup, not through the API tools we have, so it's a manual lookup. Template: `06_meta_audience_size_estimates.csv`, with ZIP 30096 and the Census figure pre-filled. For the two client ZIPs, Zen Air covers Duluth, so ZIPs next to 30096 (30097 Duluth/Johns Creek, 30043 Lawrenceville) would sit in the same market as your test ZIP.

## Item 7. Where awareness impressions land (added October 7)

Files: `08_meta_awareness_placement.csv` (one row per awareness campaign) and `08b_meta_awareness_goal_summary.csv` (rollups by template, and by template and market). Raw: `raw/meta_awareness_placement_12mo.csv` and `raw/meta_awareness_adset_goal_12mo.csv`. Same 12-month window. Every campaign's placement rows add back to its 12-month total to the cent.

The template comes from each ad set's `optimization_goal`, not from the campaign name. Names miss it in both directions: Mission Accomplished's `TSD_04.27_BOF_Awareness_CBO_Evergreen` is Ad Recall Lift without saying so. Four Reach campaigns (Watt's Right, GC Home, Napps, King's Window) also hold an Ad Recall Lift ad set that never spent in the window.

| Current clients, 12 months | Ad Recall Lift | Reach |
|---|---|---|
| Campaigns / accounts | 8 / 7 | 14 / 8 |
| Spend | $5,531 | $33,634 |
| CPM | $4.32 | $2.73 |
| Share of impressions on Facebook Marketplace | 0.4% | 54.6% |
| CPM outside Marketplace | $4.28 | $2.80 |
| CPM if Marketplace impressions don't count | $4.29 | $6.02 |

Campaigns with $400 or more:

| Client | Template | Spend | CPM | On Marketplace | CPM if Marketplace doesn't count |
|---|---|---|---|---|---|
| GC Home Service | Ad Recall Lift | $1,498 | $4.32 | 0.4% | $4.33 |
| Mission Accomplished (Apr to Aug) | Ad Recall Lift | $1,249 | $3.47 | 0.3% | $3.48 |
| Cool Hand Electric | Ad Recall Lift | $506 | $4.76 | 0.4% | $4.78 |
| Nick's Heating & Air | Ad Recall Lift | $492 | $4.76 | 0.6% | $4.79 |
| Mission Accomplished (Sep) | Ad Recall Lift | $447 | $5.14 | 1.0% | $5.19 |
| Napps | Ad Recall Lift | $405 | $4.88 | 0.9% | $4.92 |
| Zen Air (open audience) | Reach | $10,979 | $3.03 | 43.2% | $5.34 |
| Zen Air (lookalike) | Reach | $8,390 | $2.50 | 59.8% | $6.21 |
| All Seasons AC (older) | Reach | $3,989 | $2.11 | 48.4% | $4.09 |
| King's Window | Reach | $3,071 | $3.46 | 43.8% | $6.15 |
| Napps | Reach | $2,228 | $3.35 | 25.4% | $4.50 |
| GC Home Service | Reach | $1,695 | $2.45 | 92.9% | $34.71 |
| Spencer Air | Reach | $1,431 | $2.52 | 97.5% | $100.00 |
| Watt's Right | Reach | $1,207 | $3.31 | 70.9% | $11.35 |
| All Seasons AC (Sep) | Reach | $497 | $2.56 | 91.5% | $30.19 |

Gillespie's Ad Recall Lift campaign ($669) is in 08 with its 12-month spend, but its placement split couldn't be pulled (account access lost, see top).

What it means for the engine:
- **The template sets the price, not the placement.** Reach is about $2.80 outside Marketplace too. Ad Recall Lift is about $4.30 everywhere.
- **The placement mix is a separate quality question.** Reach goes wherever reach is cheapest, and lately that's Marketplace almost entirely. Whether a Marketplace impression counts toward the 3x preference floor is a doctrine call for you and Ryan, not something the data settles.
- **If it doesn't count, the floor gets priced off Ad Recall Lift (about $4.30), not the $2.88 awareness average.** That's about 50% more per counted impression, and it flips which template is cheaper for the floor.
- ICS (Integrate) looks like the same Reach pattern. Your September 28 baseline puts 87% of its impressions on Marketplace at $2.48. Its ad-set goal is unknown because only your token can read the account.

## For your reconciliation against the agency-token pull

How the Meta numbers were built, so the two paths line up:
- **Scope first.** Your pull most likely covers every account the agency token can see. Compare it against the "all accounts" columns or the files in `raw/`, not the current-clients headline. `client_roster.csv` says which accounts are in the headline and why.
- Weekly rows use `time_increment=7` anchored on Monday 2025-09-29, in the ad account's time zone. Weeks with no delivery are omitted.
- **Reach is not additive.** Account-level weekly reach dedupes across campaigns; campaign-level reach dedupes only within the campaign. The 12-month reach in 01b is deduplicated over 12 months, so it won't equal the sum of weeks.
- **Archived and deleted campaigns are included.** The default campaign listing leaves them out. If your pull did the same, you'll be short $441.24 on Napps, $66.07 on On Time Service Pros and $0.26 on GC Home Service.
- Every account's campaign spend was checked against its account-level weekly spend and matches to the cent, Cool Hand included since October 7. The device breakdown in item 4 also adds back to each account's total.
- Spend is Meta's `amount_spent` in USD. CPM is Meta's reported CPM.
- **Never included anywhere:** TopServ's own ad accounts (Meta 1997521500535964 and 2999650013725143, Google 8513856629).

Notes on your September 28 baseline (`meta-baseline` JSON), from checking it against this pull:
- **Brand vs capture labels.** The JSON's `cls` follows campaign names in places. Watt's Right's `Leads-Panels-TOF-5/7/26` is a leads-objective campaign ($7,478) but sits in `brand`, so Watt's Right's brand CPM reads $32.66 instead of $5.14. On Time's link-click campaign is also `brand`, and the Watt's Right engagement boosts are `capture`. This pull groups by objective, splits out hiring ads, and uses ad-set optimization goals for the template.
- **Week buckets.** Your weekly rows start on a Tuesday (06-30), or a Wednesday for Spencer, Napps, All Heart and TopServ. Your last bucket covers 6 days (ICS shows $41.98 against its usual $49). They can't be merged with the Monday to Sunday weeks here as-is.
- **Scope.** The JSON includes TopServ Digital Ads (our own account), All Heart (offboarded) and 532145676808452 (unconfirmed, Oklahoma). Take those out before any book-level number.

Google notes:
- Cost is converted from micros.
- Weekly totals match the 12-month totals for every account. The weekly split by network (used in 05f) comes out $22 short across the book, from rows with spend but no impressions.
- Two accounts are set to African time zones, so their weeks run offset: GC Home Service 2375064049 (Kampala) and 2974002658 (Nairobi).

## Gaps in this drop

- **Integrate Comfort's Meta account (ICS, 2070047533283360).** Current client, but only the agency token can read it. Your 90 days show awareness at $2.48 and 1.64 to 1.95x a week. Adding it wouldn't move either headline: awareness CPM stays $2.88 and the awareness median stays 1.77x. For the record, it needs the same pull as everything else here: 2025-09-29 to 2026-09-27, `time_increment=7` from that Monday, account level and campaign level including archived, plus ad-set `optimization_goal` and the placement breakdown.
- **Rhino (849885463684603):** unconfirmed client, Oklahoma, a calls campaign. Out of the headline until someone confirms who it belongs to. Your New Door had no delivery.
- **Gillespie's Meta:** readable on September 28, not on October 7. Its ad-set goal and placement split are missing. Everything else for it is in.
- **Several current clients have no Meta delivery in this pull,** so their numbers are Google only. Proud Pops, Strickland, C&S Air, Golden Plumbing and Live Wire have no Meta account visible to us. Lily Pad has one, but it didn't deliver in the window.
- **OTT/CTV vendors outside Meta and Google Ads** were not checked.
- **Item 6** is manual, as above.

## Files

| File | What it is |
|---|---|
| `client_roster.csv` | Every account in the pull, its client, status, TSD start date where it matters, and the source for each. Edit a status and rerun the build to change scope. |
| `00_account_registry.csv` | Same accounts with DMA, spend and last-4-weeks activity |
| `01_...`, `01b_...` | Item 1: CPM by objective, plus campaign detail |
| `02a_...` to `02d_...` | Item 2: CPM by market, plus market coverage |
| `03_...`, `03b_...` | Item 3: YouTube by format |
| `04_...` | Item 4: CTV / OTT |
| `05a_...` to `05g_...` | Item 5: frequency, plus the cross-platform impression files |
| `06_...` | Item 6: template for the manual lookup |
| `07_cpm_by_quarter.csv` | Seasonality |
| `08_...`, `08b_...` | Item 7: awareness placements and optimization goal, per campaign and rolled up |
| `raw/` | Platform responses the files are built from. The Meta files added October 7 (`meta_awareness_placement_12mo.csv`, `meta_awareness_adset_goal_12mo.csv`, `meta_comscore_market_check.csv`) are the connector's rows written out as CSV. The comscore file condenses the long tail of markets under a dollar into one line. |
| `build_outputs.py` | Rebuilds every file from `raw/` and `client_roster.csv` |
