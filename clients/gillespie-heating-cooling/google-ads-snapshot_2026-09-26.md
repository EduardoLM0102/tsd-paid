# Gillespie's Heating and Cooling: Google Ads snapshot (2026-09-26)

Internal reference, taken before the Maximize Conversions rebuild. Ad copy, keywords and negatives below are pulled from the live account by script (`read.py` + GAQL), not retyped. Nothing on the account was changed to produce this.

- **Customer ID:** `7410489772` (TSD MCC `4155514468`), USD, America/New_York
- **Site:** gillespieheatingcooling.com · **Phone:** (859) 445-6500
- **Performance window used below:** 2026-08-18 (launch) through 2026-09-26

---

## 1. Account state at snapshot

| Campaign | ID | Status | Budget | Bidding | Networks | Geo setting |
|---|---|---|---|---|---|---|
| `TSD_08.18_Search_NonBranded_Evergreen` | `24155674204` | **PAUSED** | $65.00/day | Manual CPC (eCPC off) | Google Search only | PRESENCE |
| `TSD_08.18_Search_Branded_Evergreen` | `24155673340` | **PAUSED** | $1.00/day | Manual CPC (eCPC off) | Google Search only | PRESENCE |
| `LocalServicesCampaign:SystemGenerated:0006540e96ed9ca4` | `23940351598` | ENABLED | n/a | LSA (out of TSD PPC scope) | n/a | 14 KY locations |

- **Both Search campaigns were paused by eduardo@topservdigital.com on 2026-09-26 at 06:53 UTC** (Google Ads web client). The last log entry (09-23) had them enabled, and they were spending through 09-25 (~$70/day).
- The 2026-09-22 edits in the change history are also Edu's, via API: 5 phrase negatives added to Non-Branded (`cheap`, `quote`, `price`, `cost`, `how much`) and 2 keywords removed (one from AC-Repair-Install, one from Furnace-Heating-Repair). None of that is in the log. The lists below are the state after those edits.
- 2026-09-23: AC-Repair-Install and Heat-Pump-Services ad groups paused by Edu (already logged).

## 2. Performance since launch (08-18 to 09-26), Non-Branded by ad group

| Ad group | ID | Status | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|---|
| HVAC-General-Company | `199263226493` | ENABLED | 95 | 1,515 | 5 | $1,493.66 |
| Furnace-Heating-Repair | `199028708869` | ENABLED | 26 | 533 | 1 | $372.42 |
| AC-Repair-Install | `202443542394` | PAUSED | 23 | 357 | 1 | $245.70 |
| Heat-Pump-Services | `197137071057` | PAUSED | 8 | 114 | 0 | $95.46 |
| **Non-Branded total** | | | **152** | **2,519** | **7** | **$2,207.24** |
| Brand-Terms (Branded) | `197137075177` | ENABLED | 0 | 2 | 0 | $0.00 |

Top keywords: `hvac company` (PHRASE) 65 clicks, 3 conv, $1,086.65 at $16.72 avg CPC. `hvac service` 19 clicks, 2 conv, $312.91.

## 3. Conversion setup (this is what Maximize Conversions will optimize to)

**Enabled conversion actions:**

| Action | ID | Type | Category | Counting | Primary |
|---|---|---|---|---|---|
| TSD - Lead Form | `7725242585` | WEBPAGE | SUBMIT_LEAD_FORM | ONE_PER_CLICK | yes |
| Click to call | `7725368783` | CLICK_TO_CALL | PHONE_CALL_LEAD | ONE_PER_CLICK | yes |
| Calls from ads | `7728360430` | AD_CALL | PHONE_CALL_LEAD | MANY_PER_CLICK | yes |
| local_services_phone_lead | `628` | LSA-native | PHONE_CALL_LEAD | MANY_PER_CLICK | yes (LSA only) |
| local_services_message_lead | `629` | LSA-native | UNKNOWN | MANY_PER_CLICK | yes (LSA only) |

**Campaign-level goals (both Search campaigns, both biddable):** `SUBMIT_LEAD_FORM / WEBSITE` and `PHONE_CALL_LEAD / CALL_FROM_ADS`.

**Lifetime conversions by action (08-18 to 09-26), all 7:** Click to call 5, Calls from ads 1, TSD - Lead Form 1.

**Timeline:** conversions on 09-01, 09-06, 09-07, 09-08, none since. From 09-09 through 09-26 (18 days) the account spent **$1,169.69 on 73 clicks with 0 conversions**. Since the 09-17 relaunch on the new landing pages (09-17 to 09-26): **$602.77 on 38 clicks, 0 conversions**.

## 4. Responsive Search Ads (verbatim, all 5)

No pinned assets, no display paths (`path1`/`path2` empty). Ad strength is not returned by the read tool. Every asset shows `PENDING` performance label, all policy APPROVED. Each ad is ENABLED at ad level (parent state governs delivery).


### HVAC-General-Company  (NonBranded)
- Ad `821380502381` · Ad group `199263226493` · Ad group status ENABLED
- **Final URL:** https://gillespieheatingcooling.com/emergency-ac-repair/
- Lifetime: 95 clicks, 1515 impr, 5 conv, $1493.66
- **Headlines** (15):
  1. Gillespie's Heating & Cooling
  2. Local HVAC Company
  3. Family Owned Since Day One
  4. Free HVAC Estimates
  5. Licensed & Insured KY/OH
  6. NATE Certified Techs
  7. Upfront Honest Pricing
  8. No Hidden Fees, Ever
  9. Response Within 1 Hour
  10. Financing Available
  11. 5.0 Star Google Rating
  12. Serving Northern KY & OH
  13. Get A Free Estimate
  14. HVAC Company Near You
  15. All Major HVAC Brands
- **Descriptions** (4):
  1. Family owned HVAC company serving Northern KY and the Cincinnati area.
  2. Free estimates, upfront pricing, no hidden fees. NATE certified technicians.
  3. Licensed and insured in KY and OH. All major brands: Trane, Carrier, Lennox.
  4. Response within 1 business hour. Contact us today to get started.

### Furnace-Heating-Repair  (NonBranded)
- Ad `821380505447` · Ad group `199028708869` · Ad group status ENABLED
- **Final URL:** https://gillespieheatingcooling.com/emergency-furnace-repair/
- Lifetime: 26 clicks, 533 impr, 1 conv, $372.42
- **Headlines** (15):
  1. Furnace Repair & Install
  2. Gillespie's Heating & Cooling
  3. Free Furnace Estimates
  4. Family Owned HVAC Company
  5. Licensed & Insured KY/OH
  6. NATE Certified Techs
  7. Upfront Honest Pricing
  8. No Hidden Fees, Ever
  9. Response Within 1 Hour
  10. Financing Available
  11. 5.0 Star Google Rating
  12. Serving Northern KY & OH
  13. Get A Free Estimate
  14. Furnace Repair Near You
  15. 2-Yr No Hassle Warranty
- **Descriptions** (4):
  1. Family owned furnace repair, install and replacement in Northern KY and OH.
  2. Free estimates, upfront pricing, no hidden fees. NATE certified technicians.
  3. Licensed and insured in KY and OH. All major brands: Trane, Carrier, Lennox.
  4. Response within 1 business hour. Contact us today to book your repair.

### AC-Repair-Install  (NonBranded)
- Ad `821307379177` · Ad group `202443542394` · Ad group status PAUSED
- **Final URL:** https://gillespieheatingcooling.com/emergency-ac-repair/
- Lifetime: 23 clicks, 357 impr, 1 conv, $245.70
- **Headlines** (15):
  1. AC Repair & Installation
  2. Gillespie's Heating & Cooling
  3. Free AC Repair Estimates
  4. Family Owned HVAC Company
  5. Licensed & Insured KY/OH
  6. NATE Certified Techs
  7. Upfront Honest Pricing
  8. No Hidden Fees, Ever
  9. Response Within 1 Hour
  10. Financing Available
  11. 5.0 Star Google Rating
  12. Serving Northern KY & OH
  13. Get A Free Estimate
  14. AC Repair Near You
  15. 2-Yr No Hassle Warranty
- **Descriptions** (4):
  1. Family owned AC repair, install and tune ups across Northern KY and Cincinnati.
  2. Free estimates, upfront pricing, no hidden fees. NATE certified technicians.
  3. Licensed and insured in KY and OH. All major brands: Trane, Carrier, Lennox.
  4. Response within 1 business hour. Contact us today to book your repair.

### Heat-Pump-Services  (NonBranded)
- Ad `821380488128` · Ad group `197137071057` · Ad group status PAUSED
- **Final URL:** https://gillespieheatingcooling.com/emergency-furnace-repair/
- Lifetime: 8 clicks, 114 impr, 0 conv, $95.46
- **Headlines** (15):
  1. Heat Pump Repair & Install
  2. Gillespie's Heating & Cooling
  3. Free Heat Pump Estimates
  4. Family Owned HVAC Company
  5. Licensed & Insured KY/OH
  6. NATE Certified Techs
  7. Upfront Honest Pricing
  8. No Hidden Fees, Ever
  9. Response Within 1 Hour
  10. Financing Available
  11. 5.0 Star Google Rating
  12. Serving Northern KY & OH
  13. Get A Free Estimate
  14. Ductless Mini Splits Too
  15. 2-Yr No Hassle Warranty
- **Descriptions** (4):
  1. Family owned heat pump repair, install and service across Northern KY and OH.
  2. Free estimates, upfront pricing, no hidden fees. NATE certified technicians.
  3. Ductless mini split installs too. Licensed and insured in KY and OH.
  4. Response within 1 business hour. Contact us today to book service.

### Brand-Terms  (Branded)
- Ad `821380510997` · Ad group `197137075177` · Ad group status ENABLED
- **Final URL:** https://gillespieheatingcooling.com/
- Lifetime: 0 clicks, 2 impr, 0 conv, $0.00
- **Headlines** (12):
  1. Gillespie's Heating & Cooling
  2. Official Gillespie's Site
  3. Free HVAC Estimates
  4. Family Owned Since Day One
  5. Licensed & Insured KY/OH
  6. NATE Certified Techs
  7. 5.0 Star Google Rating
  8. Serving Northern KY & OH
  9. Get A Free Estimate
  10. Upfront Honest Pricing
  11. No Hidden Fees, Ever
  12. Financing Available
- **Descriptions** (4):
  1. Gillespie's Heating and Cooling, Brooksville KY. Family owned and operated.
  2. Free estimates, upfront pricing, no hidden fees. NATE certified technicians.
  3. Licensed and insured in KY and OH. All major brands: Trane, Carrier, Lennox.
  4. Response within 1 business hour. Contact us today to get started.

## 5. Keywords (41 live)

**HVAC-General-Company** (8)

| Match | Keyword | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|
| PHRASE | hvac company | 65 | 1095 | 3 | $1086.65 |
| PHRASE | hvac service | 19 | 273 | 2 | $312.91 |
| PHRASE | hvac contractor | 7 | 98 | 0 | $53.44 |
| PHRASE | hvac repair near me | 2 | 20 | 0 | $34.84 |
| PHRASE | local hvac company | 2 | 9 | 0 | $5.82 |
| EXACT | hvac repair near me | 0 | 1 | 0 | $0.00 |
| PHRASE | hvac technician near me | 0 | 0 | 0 | $0.00 |
| PHRASE | hvac company near me | 0 | 2 | 0 | $0.00 |

**Furnace-Heating-Repair** (8)

| Match | Keyword | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|
| PHRASE | heating repair | 11 | 101 | 0 | $157.02 |
| PHRASE | furnace replacement | 3 | 75 | 0 | $47.11 |
| EXACT | furnace repair | 0 | 0 | 0 | $0.00 |
| PHRASE | furnace repair | 0 | 0 | 0 | $0.00 |
| PHRASE | furnace installation | 0 | 2 | 0 | $0.00 |
| PHRASE | heater repair | 0 | 6 | 0 | $0.00 |
| PHRASE | gas furnace repair | 0 | 0 | 0 | $0.00 |
| PHRASE | furnace not working | 0 | 29 | 0 | $0.00 |

**AC-Repair-Install** (9)

| Match | Keyword | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|
| PHRASE | ac installation | 9 | 104 | 0 | $130.00 |
| PHRASE | air conditioning repair | 6 | 97 | 1 | $61.32 |
| PHRASE | ac replacement | 8 | 107 | 0 | $54.38 |
| EXACT | ac repair | 0 | 2 | 0 | $0.00 |
| PHRASE | air conditioner installation | 0 | 7 | 0 | $0.00 |
| PHRASE | air conditioner repair | 0 | 4 | 0 | $0.00 |
| PHRASE | ac repair | 0 | 27 | 0 | $0.00 |
| PHRASE | central air repair | 0 | 0 | 0 | $0.00 |
| PHRASE | ac tune up | 0 | 1 | 0 | $0.00 |

**Heat-Pump-Services** (8)

| Match | Keyword | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|
| PHRASE | heat pump replacement | 7 | 67 | 0 | $83.71 |
| PHRASE | heat pump installation | 1 | 1 | 0 | $11.75 |
| PHRASE | heat pump repair | 0 | 0 | 0 | $0.00 |
| EXACT | heat pump installation | 0 | 0 | 0 | $0.00 |
| PHRASE | heat pump service | 0 | 3 | 0 | $0.00 |
| PHRASE | mini split installation | 0 | 19 | 0 | $0.00 |
| PHRASE | ductless mini split installation | 0 | 1 | 0 | $0.00 |
| PHRASE | heat pump not working | 0 | 0 | 0 | $0.00 |

**Brand-Terms** (8)

| Match | Keyword | Clicks | Impr | Conv | Cost |
|---|---|---|---|---|---|
| EXACT | gillespie air conditioning | 0 | 0 | 0 | $0.00 |
| EXACT | gillespie heating and cooling | 0 | 2 | 0 | $0.00 |
| EXACT | gillespie hvac | 0 | 0 | 0 | $0.00 |
| EXACT | gillespies heating and cooling | 0 | 0 | 0 | $0.00 |
| EXACT | gillespie heating & cooling | 0 | 0 | 0 | $0.00 |
| EXACT | gillespie heating and cooling brooksville | 0 | 0 | 0 | $0.00 |
| EXACT | gillespie hvac brooksville ky | 0 | 0 | 0 | $0.00 |
| EXACT | gillespie's heating and cooling | 0 | 0 | 0 | $0.00 |

## 6. Negative keywords (39, all campaign-level on Non-Branded; Branded has none)

- **BROAD (12):** career, careers, electrical, electrician, employment, hiring, job, jobs, plumber, plumbing, roofer, roofing
- **PHRASE (19):** capacitor, cheap, cost, craigslist, diy, home depot, how much, how to, hvac certification, hvac school, lowes, manual, price, quote, recall lawsuit, salary, used hvac, warranty claim, wiring diagram
- **EXACT (8):** gillespie air conditioning, gillespie heating & cooling, gillespie heating and cooling, gillespie heating and cooling brooksville, gillespie hvac, gillespie hvac brooksville ky, gillespie's heating and cooling, gillespies heating and cooling

The 8 EXACT terms are the brand cross-negatives (all 8 Brand-Terms keywords).

## 7. Targeting settings (identical on both Search campaigns)

- **Locations (11 cities, PRESENCE only):** Alexandria KY `1017681`, Brooksville KY `1017704`, Covington KY `1017733`, Cynthiana KY `1017738`, Erlanger KY `1017751`, Flemingsburg KY `1017759`, Florence KY `1017760`, Fort Mitchell KY `1017768`, Maysville KY `1017832`, Newport KY `1017851`, Cincinnati OH `1023626`
- **Language:** English (`languageConstants/1000`)
- **Devices:** all (no bid adjustments)
- **Ad schedule:** none (24/7)
- **Networks:** Google Search only (Search Partners and Display off since the 08-24 fix)

## 8. Assets

**Callouts, linked to both campaigns (8):** No Hidden Fees · Family Owned & Operated · Financing Available · Free Estimates · Upfront Pricing · Licensed & Insured · 5.0 Star Rating · NATE Certified Techs

**Sitelinks linked at campaign level to both campaigns (4):**

| Text | Description 1 | Description 2 | URL | Asset ID |
|---|---|---|---|---|
| Indoor Air Quality | Purifiers & filtration | Free estimates | /indoor-air-quality/ | `409474614430` |
| Commercial HVAC | Rooftop units & more | Licensed and insured | /commercial/ | `409474971790` |
| Contact Us | Response within 1 hour | Request a free quote | /contact/ | `409474971793` |
| About Us | Family owned HVAC company | NATE certified techs | /about/ | `409474992694` |

**Sitelinks linked at customer level (5, created 09-08, text only, no descriptions):** Furnace Installation `/heating/furnace-installation/`, Heat Pump Repair `/heating/heat-pump-repair/`, Furnace Repair `/heating/furnace-repair/`, AC Repair `/air-conditioning/ac-repair/`, AC Installation `/air-conditioning/ac-installation/`. Campaign-level sitelinks override these, so they have not been serving on the two Search campaigns.

**Ad-group-level sitelinks:** Brand-Terms has bare "Indoor Air Quality" (`416358096710`) and "Commercial HVAC" (`416463847936`) linked and enabled. Both were removed from HVAC-General-Company.

**Call asset (customer level):** (859) 445-6500 `371246986318`

## 9. Flags

1. **Ad claims to re-verify against the site before reuse:** "Response Within 1 Hour" (site says "within 1 business hour"), "2-Yr No Hassle Warranty", and "All major brands: Trane, Carrier, Lennox" (the 08-18 site recon logged "major brands" without naming them).
2. **`Click to call` is 5 of the 7 lifetime conversions.** It is a button tap (`ONE_PER_CLICK`, no call-duration threshold), and only 1 form fill has ever been recorded. Any Smart Bidding on this account currently learns mostly from taps. Biddability can be changed per campaign through `campaign_conversion_goal.biddable` if the rebuild should optimize to form fills only.
3. **Log gaps this snapshot fills:** the 09-22 negatives/keyword edits and the 09-26 pause were not in `google-ads-log.md`.
