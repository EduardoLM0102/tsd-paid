# Zen Air — Client Strategy Review "Oct/Nov Review" (AT c29ad0c8), Paid row 2026-11-12

Cycle 2026-10-10 → 2026-11-08. Angela's call was 2026-11-10 15:00 ET (already happened). Stage Performance Reporting assigned to Gui's AT user 7f88768a. Pulled 2026-11-12 (`strategy_review_pull_1112.py`, Meta MCP, HighLevel via AT, LSA recordings transcribed locally with faster-whisper small.en; audio + transcripts in `_pessoal/call-wins/zen-air/`).

| Field | Value | Source |
|---|---|---|
| period | 2026-10-10 → 2026-11-08 | task |
| ad_spend | **$7,481.80** = Meta $6,501.59 (lead CBO 120247267872090711 $4,517.71 + awareness 120227295614760711 $1,957.64 + Now Hiring 120247939383320711 $26.24 since 11-03) + Google Search $855.41 (Branded 23675783172 $181.96 + Non-Branded 24100030790 $673.45, 10-23..10-29) + LSA 3740502923 $124.80 (2 charged leads) | Meta MCP, Google Ads API |
| qualified_leads | **207** = Meta 195 + LSA 6 + Branded 6 (see "How counted") | HighLevel, LSA transcripts, conversion actions |
| cpl | **$36.14** overall. Meta $33.34 (lead campaign alone $23.17; per core-area lead ~$51); Google Search $142.57 (Branded alone $30.33; NB $673 / 0); LSA $20.80 | |
| agency_fees | blank (AM) | |
| total_spend | blank | |
| recommend_budget | **7000** (hold at this cycle's pace; +$50/day Meta if bookings confirm) | |

## How counted

**Meta 195.** Platform: 334 form leads on "49$ Furnace Tune-Up" (ad 09/22/26 Ad 02, ad set 120247339585910711), $13.53 each. CRM: 328 unique contacts in HighLevel (source Facebook, tags `fb lead` / `49$ furnace tune-up`), daily counts match Meta within 1/day (6 fewer = duplicates merged). City is self-reported (profile prefill), no ZIP. Buckets (Edu's 10-14 framing + "other targeted ZIP cities" for Roswell/Sandy Springs/Dunwoody/East Point/Oakwood/Murrayville/Palmetto etc.):

| Bucket | All (328) | Oct 10-20 (125) | Oct 21-Nov 8 (203) |
|---|---:|---:|---:|
| Core service cities | 55 | 15 | 40 |
| Workable extras (Gainesville 14, Union City 4, College Park 4, Fairburn 3) | 26 | 8 | 18 |
| Other targeted ZIP cities | 7 | 1 | 6 |
| Atlanta | 107 (33%) | 29 (23%) | 78 (38%) |
| **Inside targeted area (counted)** | **195 (59%)** | **53 (42%)** | **142 (70%)** |
| Marietta/Monroe (excluded cities) | 15 | 11 | 4 |
| Outside (far Georgia + out of state) | 115 (35%) | 60 (48%) | 55 (27%) |
| Blank ("Georgia") | 3 | 1 | 2 |

Counted = inside the area the ad set targets (131 ZIPs = Gwinnett + whole Fulton + Hall + Forsyth + Hoschton; Atlanta is in because Edu chose whole Fulton on 10-12 and Fulton County is on the AT target list). Not counted: outside, Marietta/Monroe, blank.
Previous cycle 09-10..10-09 (campaign live from 09-17): $3,416.89 / 145 platform leads / $23.56 → CPL down 43%, ~11 leads/day now.
Awareness `Open Audience`: $1,957.64, reach 165,379, freq 3.66, CPM $3.24. Its 165 pixel "lead" events are NOT form leads, not counted. Now Hiring (Eddie, AT 6f21b9fb): $26.24, applicants, not counted.
HighLevel pipeline IbUE8pXG5PYTiXB5vJjc: 332 of 340 cycle contacts have 1 opportunity, all `open`, first stage c1d700a4 → nobody moves the GHL pipeline; outcomes live in ServiceTitan (AT crm_system). Non-FB GHL contacts in cycle: City Pages Form x2, Contact Us x1, Club Zen x1, 8 with no source. Not attributable to paid (form → Google Ads tracking dead since 09-15), not counted.

**LSA 6 of 10** (all phone, all transcribed; times ET):

| Created | Call | Google status | Charged | Transcript | Counted |
|---|---|---|---|---|---|
| 10-15 09:10 | 79s | DECLINED ("hiring??") | no | job seeker asking about openings | no |
| 10-15 16:16 | 168s | BOOKED (returning customer) | no | existing customer, HVAC leaking in Milton, booked next day | yes (existing) |
| 10-16 08:17 | 52s | DECLINED (tech application) | no | job applicant checking on his application | no |
| 10-19 09:23 | 130s | DECLINED | no | NEW: furnace stopped overnight, booked next day 12-2:30 | yes (new) |
| 10-20 11:22 | 106s | DECLINED (fleet services) | no | vendor pitch (auto shop) | no |
| 10-21 13:00 | 28 min | BOOKED (2 addresses, both paid) | no | existing member, 2 properties: maintenance visit + a no-heat unit next day, paid on the call | yes (existing) |
| 10-22 13:32 | 284s | DECLINED | no | NEW: upstairs heat stopped, tech next morning ~9 | yes (new) |
| 10-28 14:04 | 87s | ACTIVE | **yes $62.40** | wrong number (Astoria NY caller looking for "David") | no |
| 11-04 10:28 | 85s | DECLINED | no | existing customer paying for a visit done the day before | yes (existing, per 11-12 rule) |
| 11-05 15:57 | 223s | DECLINED | no | existing customer asking for the sales rep's name to refer a friend | yes (existing, per 11-12 rule) |

LSA campaign 20752144554 cost in cycle $124.80 (charges 10-10 and 10-28), 238 impr, 36 clicks. The 10-19 and 10-22 leads are marked DECLINED in LSA even though both booked (office marks). Existing-customer calls count per [[tsd-existing-customers-count-as-leads]]; the 11-04 (payment) and 11-05 (referral) ones are the weakest of the 4, say so if Edu wants them out (then 205 / $36.50).

**Branded 6.** 2 `Calls from ads` 60s+ on 10-16 (68s area 206, 118s area 850, call asset) + 4 `Peach AI — Booked Call` (10-14, 10-23, 11-03, 11-04; Peach DNI on the site for gclid visitors). 5 `[TSD] Click to call` taps not counted (10-14, 10-20, 11-03, 11-04 x2: same events as the Peach bookings). Branded: $181.96, 30 clicks, 181 impr, IS 93% (7% rank), CPC $6.07; terms all brand.
**Non-Branded 0.** Relaunched 10-23 on the 2 new LPs (heating + AC, phrase/exact), $673.45 / 55 clicks / 1 tap / 0 calls / IS 20% (56% rank-lost); PAUSED 10-29 ~15:00 ET by Edu on Eddie's request (AT 'Stop PPC - Google' 6ae9c79c). Not in the recommendation.

## Written to AT (budget_rationale, table)

> Keep about $7,000/mo, the pace of this cycle ($7,482 across Meta, Branded Search and LSA). Meta is the lead engine: the $49 furnace tune-up form brought 328 contacts into the CRM for $4,518, and after the targeting refinements on Oct 12 and Oct 20 the share of leads inside the service area went from 42% to 70%. Counting only the 195 leads inside the targeted area (Atlanta included), plus 6 LSA calls and 6 Branded Search calls, that's 207 qualified leads at $36 each. Branded Search costs about $6 a day at 93% impression share and LSA only charges for valid leads ($125 this cycle), so neither needs more money. Non-branded search is paused per Eddie's Oct 29 request and isn't in this number. Two things decide the next step: how many tune-up leads booked in ServiceTitan, and whether the Atlanta leads book (Atlanta is now a third of the Meta leads). If both look good, the move is +$50/day on the Meta lead campaign for the rest of heating season. The written approval on file (Jul 31, $8k = $6k Google + $2k Meta) no longer matches the Meta-first split, worth refreshing.

## Written to AT (additional_paid_ads_notes, task long text)

- How leads were counted: Meta reported 334 form submissions on the $49 furnace tune-up form, 328 unique contacts landed in HighLevel. We checked the city on every one: 195 are inside the area the campaign targets (55 in the core service cities, 26 in Gainesville, Fairburn, Union City and College Park, 7 in other targeted ZIP cities, 107 in Atlanta), 115 are elsewhere in Georgia or out of state, 15 Marietta/Monroe, 3 blank. Only the 195 count. LSA: we listened to all 10 calls, 6 count (2 new heating repairs booked for the next day on Oct 19 and Oct 22, plus 4 existing customers: a Milton member with a leaking unit booked next day on Oct 15, a two-property member who booked maintenance plus a no-heat visit on Oct 21, one paying for a visit on Nov 4, one asking for a sales rep's name to refer a friend on Nov 5). The other 4 were 2 job seekers, a vendor and a wrong number. Branded Search: 2 calls from the ads on Oct 16 (68s and 118s) and 4 calls Peach AI logged as booked (Oct 14, Oct 23, Nov 3, Nov 4). Phone-number taps on the site are not counted. Total 207 at $36.14.
- Meta: $4,518 on the lead campaign for 334 leads, $13.53 each on the platform (down from $23.56 the previous cycle), about 11 leads a day. Awareness ran alongside at $1,958 (165k people reached 3.7 times). Targeting refinements this cycle: Marietta and Monroe removed on Oct 12 and the full service-area ZIP list added; Oct 20 switched to people living in the area and excluded the airport ZIP. Result: leads from outside the area fell from 48% to 27% and in-area went from 42% to 70%, with Atlanta now 38%. Hector's Winter Ready and Rated & Guaranteed creatives went live Nov 9 and 10 on the same form. The Now Hiring ad Eddie asked for runs at $5 a day since Nov 3 ($26 so far, applicants only, not in the lead count).
- LSA: $125 charged for the cycle (2 leads), 10 calls, 6 counted. Google only charges when it sees a valid lead, which is why the cost stays low. Both new leads were heating breakdowns booked for the next morning.
- Google Search: Branded at about $6 a day, 93% impression share, 6 calls counted ($30 each). Non-branded ran a one-week test on the two new heating and AC pages (Oct 23 to 29, $673, no calls) and was paused on Oct 29 at Eddie's request. It stays paused; a heating-season search test later is a separate decision.
- For Angela to raise: (1) how many of the $49 tune-up leads booked in ServiceTitan (the HighLevel pipeline doesn't show outcomes, every opportunity is still in the first stage, so the count has to come from ServiceTitan), (2) whether the Atlanta leads book, since Atlanta is a third of the Meta leads and all of Fulton is on the target list, (3) refresh the written budget approval to the current Meta-first split (the Jul 31 approval says $6k Google + $2k Meta; the account now runs about $6.5k Meta and under $1k Google), (4) budget stays about $7,000/mo until (1) and (2) are answered, then +$50/day on Meta for heating season.

## Slack overview for Angela (Edu sends)

Zen Air, Oct 10 to Nov 8
Ad spend: $7,482 (Meta $6,502, Branded Search $855 incl. the one-week non-branded test, LSA $125)
Qualified leads: 207 (Meta 195 inside the targeted area out of 328 CRM contacts, LSA 6, Branded 6)
Cost per lead: $36 (Meta alone $33, lead campaign $23)
Caveat: Meta leads counted by self-reported city and Atlanta is a third of them. Bookings aren't visible to us (GHL pipeline sits in stage 1), we need the ServiceTitan count before pushing Meta.
Recommended budget: hold about $7k/mo, +$50/day on Meta if the tune-up leads are booking. The Jul 31 approval ($6k Google / $2k Meta) needs a refresh to the Meta-first split.

## Our side (NOT in the AM notes)

- LSA 10-28 wrong-number call (New York caller) was charged $62.40: rate it bad in the LSA inbox ourselves (credit is Google's call), fu-161 style. 10-19 and 10-22 booked leads sit as DECLINED (office marks), nothing to do.
- Internal only: Nick's lead form removed from Branded 10-26; site form → Google Ads tracking dead since 09-15 (Gui); GHL pipeline unworked.
- Transcript of the 10-21 call contains spoken card details: never copy them anywhere.

## Checklist

- [x] KPI row WRITTEN 2026-11-12: record **53ecca81-aee0-4316-b6de-36f2d2196219**, linked to the client field c72c4f7e (relationship a5ee1ef9) + `additional_paid_ads_notes` applied on task c29ad0c8
- [x] Stage Performance Reporting NOT completed (Edu decides)
- [ ] Command Center follow-ups: LSA rating 10-28; refresh after Angela answers bookings/Atlanta
- [ ] Edu reviews; if he wants the 11-04/11-05 existing-customer calls out: 205 leads / $36.50
