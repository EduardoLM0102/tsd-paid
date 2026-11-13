# All Seasons AC — Client Strategy Review "Oct/Nov Review" (AT 7be61e95), Paid row DRAFT 2026-11-13

Cycle 2026-10-10 → 2026-11-08. Call was 2026-11-10 10:00 ET (already happened). Stage Performance Reporting `8a93a40f`, assigned to Gui's AT user 7f88768a, status not_started. NOT written to AT yet, NOT submitted.
Counting rule: 2026-11-12 (existing customers who reach the office through an ad COUNT, labelled existing). Every lead judged from the transcript / message text, not the Google status.

| Field | Value | Source |
|---|---|---|
| period | 2026-10-10 → 2026-11-08 | task |
| ad_spend | **3051.80** = Google PPC 4467722415 $1,938.59 + LSA 8655979348 $994.53 + Meta $118.68 (awareness 10-10..10-15, paused since) | Google Ads API (pulled 11-13), Meta from task notes / meta-ads-log |
| agency_fees | blank (not on record) | |
| total_spend | blank | |
| qualified_leads | **20** = 11 new + 9 existing customers (Google 11 = 3 new + 8 existing; LSA 9 = 8 new + 1 existing; forms 0; Meta 0) | call-wins-log.md 11-13 reconciliation + LSA transcripts below |
| cpl | **152.59** overall. Google $176.24 (since 10-16: $997.78 / 11 = $90.71; Oct 10-15 $940.81 / 0). LSA $110.50. New customers only: $277.44 | |
| recommend_budget | **3200** (LSA to $60/day ≈ $1,800/mo, Google $46/day ≈ $1,400, Meta $0) | |

## How counted

**Google 11** (cycle slice of the 11-13 reconciliation in `call-wins-log.md`; call_view ∪ CallRail gclid/cpc). Oct 10-15: 0 real (all wrong company / wrong number / car AC).
- New (3): Woodbury restaurant RTU replacement, site visit same day (10-22); Floral Park install re-quote, past prospect (10-28); Valerie mini split inquiry, callback owed (11-05).
- Existing (8): no heat 10-19; Patrick follow-up 10-20; filter ETA 10-26; appointment ETA 10-27; Mineola extension HVAC job 10-29; visit confirmation 10-30; maintenance reschedule 11-02; Shelly appointment 11-03.
- Not counted: wrong company / wrong number / product shopper / no contact.

**LSA 9 of 16** (all 12 recorded calls transcribed locally, faster-whisper small.en; 4 message leads read from the API; audio in `_pessoal/call-wins/all-seasons-ac-lsa/`):

| Created | Type | Google status | Charged | What happened | Counted |
|---|---|---|---|---|---|
| 10-12 | message | NEW | yes | price of oil boiler maintenance (they don't service oil), never answered | no (service not offered) |
| 10-13 | call 7m | BOOKED | yes | NEW: Smithtown, oil to gas conversion + central AC estimate, file created for sales | yes (new) |
| 10-14 | message | NEW | yes | NEW: gas furnace 15+ yrs, wants to drop HomeServe, asked for a quote, **never answered** | yes (new) |
| 10-15 | call 4m | ACTIVE | yes | NEW: Farmingville, central air + ductwork for an extension, owner Dennis Costello Jr. going out | yes (new) |
| 10-19 | call 85s | BOOKED | yes | EXISTING commercial (Sunrise Hall shop), 2 unit heaters cycling | yes (existing) |
| 10-19 | call 3m | DECLINED | yes | job seeker (rated, no credit, closed) | no |
| 11-02 | call 3m | BOOKED | yes | NEW: East Northport, central air for whole house (window units now), comfort advisor to schedule | yes (new) |
| 11-02 | call 36s | ACTIVE | yes | wants heating oil delivery | no |
| 11-03 | call 83s | DECLINED | no | job seeker | no |
| 11-03 | call 24s | DECLINED | no | wrong company | no |
| 11-03 | message | BOOKED | yes | NEW: Farmingdale office, RTU heat not working, quote; office replied + called | yes (new) |
| 11-03 | call 4m | ACTIVE | yes | NEW: Daikin split not working, installer won't help, price talk ($195), no visit booked | yes (new, open) |
| 11-05 | call 79s | ACTIVE | yes | oil boiler checkup, told they don't do oil | no |
| 11-06 | call 23s | ACTIVE | no | wrong company (Dix Hills AC) | no |
| 11-06 | message | ACTIVE | yes | NEW: HVAC stalls on start (capacitor/relay?), messaged other businesses too; office left voicemail | yes (new, open) |
| 11-06 | call 2m | ACTIVE | yes | NEW: Fujitsu split error code, stunned by $195 + $240/hr, "talk to my husband" | yes (new, open) |

13 charged / 3 not charged → $76.50 per charged lead. Charged non-leads for US to rate bad (fu-161, kept out of AM notes per tsd-lsa-rating-is-ours; credit is Google's call): 10-12 08:59 oil boiler message, 11-02 14:48 oil delivery, 11-05 16:15 oil boiler. October half matches the earlier notes (4 real of 6).

## To write in AT — budget_rationale (table)

> Recommend about $3,200/mo, up from the $2,500 cap. 20 qualified leads this cycle on $3,051.80 of ad spend, $153 each: 11 new customers and 9 existing customers who reached the office through the ads. LSA is the strongest channel at $111 per real lead (8 of its 9 were new customers), but at $35.71/day it runs out mid month (dark Oct 20 to 31, likely again around Nov 18). Raising LSA to $60/day (about $1,800/mo) keeps it on all month. Google is $46/day: its first six days of the cycle ($941) brought nothing before the cleanup, and since Oct 16 it costs about $91 per real request. Meta stays off unless the client approves a Meta budget in writing. Any change needs the client's written OK; the growth options sent Oct 19 are still open.

## To write in AT — additional_paid_ads_notes (replaces the current text)

Changes vs. what is there now: lead count 9 → 20 under the existing-customer rule, the "still to review" items are done (all LSA transcribed; Google calls reconciled 11-13), LSA charged count fixed (13 charged, the job seeker was rated with no credit, not credited), "disputed" wording removed, the "please mark / rate LSA leads" ask removed (that's ours). Google / Meta / budget bullets kept, client asks updated.

- **How leads were counted:** 20 qualified leads on $3,051.80, about $153 each: 11 new customers and 9 existing customers who reached the office through the ads. Every call and LSA message was reviewed. Google: 11 (3 new: a Woodbury restaurant needing a rooftop unit replaced, a Floral Park install re-quote and a mini split inquiry on Nov 5; plus 8 existing customers). LSA: 9 of 16 (8 new, 1 existing); the other 7 were 2 job seekers, 2 wrong company and 3 oil-only requests. Google's own conversion count (36) is not used: many were taps on the number or calls for other companies. No website form leads were recorded all cycle.
- **Google Search:** $1,938.59, 337 clicks, 11 real requests ($176 each). Almost half ($940.81) went out Oct 10 to 15, before the budget cut, and none of those calls was a real lead. Since Oct 16: $997.78 for 11 real requests, about $91 each. Google runs at $46/day on two campaigns (general HVAC and Mitsubishi mini splits). What we changed: calls only count at 60 seconds or longer (Oct 16), about 690 other-company and junk searches blocked (Oct 16, Oct 22, Nov 10), 898 dead keywords paused (Oct 22), ads shown only to people in the service area, and the costly Nonbranded campaign paused Oct 23. Other companies' names went from 62% of search spend in early October to about 32% in the week of Nov 2. On Nov 11 the brand campaign was turned back on at $5/day inside the same $46/day, because people searching "All Seasons" were costing up to $24.92 a click in the general campaigns.
- **LSA (Google Local Services):** $994.53, 16 leads (12 calls, 4 messages), 13 charged, about $77 per charged lead. 9 were real (8 new, 1 existing), about $111 per real lead, the best of the three channels. The problem is the $35.71/day budget: each call costs about $100, so the month's budget runs out early. October ran out Oct 19 and LSA was off Oct 20 to 31. November had used about half its budget by Nov 8 and will likely stop around Nov 17.
- **Meta:** $118.68 on brand awareness Oct 10 to 15, then paused Oct 15 under the $2,500 cap and the client's earlier request to keep Meta off. $0 since Oct 16. It stays off unless the client approves a Meta budget in writing.
- **Budget:** the current cap is $2,500/mo for all platforms (Google about $1,400, LSA about $1,086, Meta $0). We recommend raising LSA to $60/day (about $1,800/mo, roughly $740 more) so it stays on all month, since it brings real leads at the lowest cost. That puts the total at about $3,200/mo. The growth options sent Oct 19 ($4,630 / $7,400 / $10,150) are still open. Any change needs the client's written OK.
- **For the client:** the Oct 14 LSA message (gas furnace owner wanting to leave HomeServe) was never answered, so messages need a same-day reply. Four new leads still need a follow-up: the Nov 3 Daikin split owner, the Nov 6 Fujitsu error code caller, the Nov 6 LSA message (unit stalls on start, voicemail left) and the Nov 5 mini split caller from Google. Did any website form leads come in since Oct 8? We record none, so we want to confirm the form works. And the written OK on the LSA budget, plus whether the client picked one of the Oct 19 options.
