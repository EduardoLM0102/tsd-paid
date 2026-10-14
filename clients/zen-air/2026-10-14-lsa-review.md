# Zen Air LSA review, 2026-10-14 (read-only, nothing changed in the account)

Edu asked, in order: (1) wins from LSA for the CS client call, (2) a way to identify the booked leads, (3) why LSA
isn't reaching more people or spending more, (4) whether the $12 target cost per lead (tCPL) found via the API is
actually in use, and when it was set.

- LSA account `3740502923` ("Zen Air Heating and Cooling - LSA"), separate from PPC `4360840956`. MCC `4155514468`.
- Campaign `20752144554` (`LocalServicesCampaign:SystemGenerated:000609a78b55614f`), status ENABLED, primary status ELIGIBLE.
- Account time zone `America/New_York`. All times below are ET.
- LSA was paused by Eddie on 2026-07-03 and re-enabled 2026-09-10 by access@topservdigital.com (see the 09-30 deep dive).
- Caller phone numbers and addresses are deliberately NOT in this file (repo syncs to GitHub). Pull them on demand, recipe in section 1.

---

## 1. How the pull was done

Everything through the Ratos skill on the TSD profile, from `.claude/skills/google-ads-ratos/scripts/`:

- `./tsd.sh lsa_report.py --client "Zen" --since 2026-09-01 --until 2026-10-14`: totals (leads, charged, by type, by status).
- `./tsd.sh read.py local-services-leads --customer-id 3740502923 --days 45`: lead list.
- Raw GAQL with `run_query()` (scratch scripts, not kept) on these resources:

| What | Resource / field |
|---|---|
| Lead status, charged, service, client feedback | `local_services_lead` (`lead_status`, `lead_charged`, `service_id`, `lead_feedback_submitted`) |
| Caller phone | `local_services_lead.contact_details` (select the whole message; `contact_details.consumer_name` is UNRECOGNIZED_FIELD) |
| Notes Zen's team typed in LSA | `local_services_lead.note.description`, `.note.edit_date_time` |
| Each call, duration, recording link | `local_services_lead_conversation` (`.lead`, `.event_date_time`, `.phone_call_details.call_duration_millis`, `.phone_call_details.call_recording_url`) |
| Spend / impressions | `campaign` + `metrics.cost_micros`, `metrics.impressions`, `segments.date/week/month/day_of_week/hour` |
| Bid settings | `campaign.bidding_strategy_type`, `campaign.local_services_campaign_settings.category_bids`, `campaign.bidding_strategy_system_status`, `campaign.maximize_conversions.target_cpa_micros` |
| Budget | `campaign_budget.amount_micros`, `.period`, `.type` |
| Service area, schedule, services | `campaign_criterion` (types LOCATION, AD_SCHEDULE, LOCAL_SERVICE_ID), names via `geo_target_constant` |
| License / insurance | `customer.local_services_settings.granular_license_statuses` / `granular_insurance_statuses`, `local_services_verification_artifact` |
| Who has access | `customer_manager_link`, `customer_user_access` |
| Change log | `change_event` (30-day retention, needs BOTH date bounds via BETWEEN plus a LIMIT, otherwise CHANGE_DATE_RANGE_INFINITE) |

- New reusable script: `./tsd.sh zenair_lsa_bids.py` prints the bidding strategy, target per lead and manual max per lead.
- `metrics.conversions` on the LSA campaign = charged leads (matches the charged count every month).
- The API has NO URL for a lead's page in the LSA dashboard. Only per-call recording links. Real dashboard URL format
  (from Slack): `ads.google.com/localservices/inbox?cid=<customer id>&bid=<business id>&pid=9999999999`. The `bid` is not
  in the API. Per-lead URL format still unknown.

---

## 2. Results since the restart (09-10 to 10-14)

**13 phone leads, 6 booked, 4 declined, 3 not yet marked by Zen. $169.01 spend. Google charged only 2 of the 13.**

- About $28 per booked job ($169.01 / 6).
- Blended $13.00 per lead ($169.01 / 13, counting uncharged leads).
- $84.50 per charged lead ($169.01 / 2).
- Lead 344561908 flipped ACTIVE to BOOKED during the session (first pull showed 5 booked, about an hour later 6).

| Week (Mon) | Leads | Booked | Impressions | Spend |
|---|---|---|---|---|
| 09-07 (from 09-10) | 3 | 1 | 28 | $106.61 |
| 09-14 | 3 | 1 | 95 | $0 |
| 09-21 | 2 | 0 | 102 | $0 |
| 09-28 | 1 | 1 | 76 | $0 |
| 10-05 | 4 | 3 | 68 | $62.40 |
| 10-12 (to 10-14) | 0 | 0 | 29 | $0 |

### Booked leads

| # | Lead ID | Created (ET) | Calls | Zen's note in LSA (paraphrased) | Charged |
|---|---|---|---|---|---|
| 1 | 339341316 | Fri 09-11 2:25 PM | 15m14s, then 21m29s at 2:59 PM | none | no |
| 2 | 340956501 | Sat 09-19 9:44 AM | 2m20s | AC not cooling, Norcross, $79 diagnostic, appointment Mon 8-9 AM | no |
| 3 | 343547992 | Fri 10-02 10:07 AM | 4m26s | EXISTING customer, schedule maintenance (not a new customer win) | no |
| 4 | 344021214 | Mon 10-05 1:02 PM | 3m33s, callback 10-13 8:17 AM 3m38s | repair, part ordered | no |
| 5 | 344561908 | Wed 10-07 10:47 AM | 2m57s | none (marked booked 10-14) | no |
| 6 | 344640606 | Wed 10-07 4:42 PM | 4s, 2m04s at 4:48 PM, callback 10-10 10:24 AM 4m30s | AC repair, "let me get back to you" (may not be confirmed) | $62.40 |

### Declined

| Lead ID | Created (ET) | Call | Charged |
|---|---|---|---|
| 339188014 | 09-10 2:38 PM | 1m45s | no |
| 339121110 | 09-10 5:08 PM | 25s (service repair_hvac) | **$106.61** (charged and declined, check in the dashboard if it can still be disputed) |
| 339878415 | 09-14 3:47 PM | 16s | no |
| 340556462 | 09-18 4:10 PM | 4s | no |

### Not yet marked by Zen

342007215 (09-24 1:02 PM, 3m55s), 341709461 (09-24 1:59 PM, 1m48s), 344766323 (10-09 10:10 AM, 2m01s, feedback submitted).

### Wins as given to Edu for the CS call

13 calls, 6 booked (5 new customers, 1 existing), $169 total, about $28 per booked job, last full week best (4 calls,
3 booked), booked calls ran 2 to 21 minutes and 3 of the callers called back. One average service ticket ($225 per AT)
covers all LSA spend so far. Which lead became the "won" job is not visible in LSA (only BOOKED); best guess #4, confirm
with Eddie/GHL. Do NOT mention the July pause to the client, and don't promise $28/booked going forward (only 2 of 13
charged, unusually low).

### Monthly history (all leads incl. uncharged)

| Month | Impr | Spend | Leads | Charged | Blended $/lead | $/charged | Booked |
|---|---|---|---|---|---|---|---|
| 2024-10 | 248 | $35.88 | 3 | 1 | $11.96 | $35.88 | 0 |
| 2024-11 | 208 | $131.04 | 4 | 2 | $32.76 | $65.52 | 0 |
| 2024-12 | 101 | $50.40 | 2 | 1 | $25.20 | $50.40 | 0 |
| 2025-01 | 204 | $100.80 | 5 | 2 | $20.16 | $50.40 | 0 |
| 2025-02 | 195 | $143.87 | 4 | 2 | $35.97 | $71.94 | 0 |
| 2025-03 | 284 | $157.90 | 2 | 2 | $78.95 | $78.95 | 0 |
| 2025-04 | 228 | $0.00 | 1 | 0 | $0 | n/a | 0 |
| 2025-05 | 378 | $293.15 | 7 | 4 | $41.88 | $73.29 | 0 |
| 2025-06 | 1,306 | $1,549.52 | 20 | 17 | $77.48 | $91.15 | 0 |
| 2025-07 | 2,654 | $2,609.66 | 40 | 33 | $65.24 | $79.08 | 0 |
| 2025-08 | 888 | $1,066.88 | 25 | 14 | $42.68 | $76.21 | 0 |
| 2025-09 | 512 | $288.00 | 10 | 6 | $28.80 | $48.00 | 0 |
| 2025-10 | 639 | $169.34 | 8 | 2 | $21.17 | $84.67 | 0 |
| 2025-11 | 507 | $151.20 | 9 | 3 | $16.80 | $50.40 | 1 |
| 2025-12 | 556 | $386.99 | 9 | 5 | $43.00 | $77.40 | 0 |
| 2026-01 | 805 | $184.08 | 8 | 3 | $23.01 | $61.36 | 0 |
| 2026-02 | 537 | $124.80 | 7 | 2 | $17.83 | $62.40 | 1 |
| 2026-03 | 368 | $244.80 | 11 | 4 | $22.25 | $61.20 | 5 |
| 2026-04 | 344 | $228.63 | 8 | 4 | $28.58 | $57.16 | 1 |
| 2026-05 | 234 | $62.40 | 5 | 1 | $12.48 | $62.40 | 1 |
| 2026-06 | 414 | $249.60 | 11 | 4 | $22.69 | $62.40 | 4 |
| 2026-07 (1-3 only) | 294 | $766.40 | 13 | 10 | $58.95 | $76.64 | 3 |
| 2026-09 (from 09-10) | 261 | $106.61 | 8 | 1 | $13.33 | $106.61 | 2 |
| 2026-10 (to 10-14) | 136 | $62.40 | 5 | 1 | $12.48 | $62.40 | 4 |

Zen only started marking leads BOOKED in 2026 (0 booked in all of 2025), so booking rates before 2026 aren't comparable.
Before the July pause (05-01 to 07-03): 29 leads, 8 booked (28%), 13 charged, $1,078, about $135 per booked job.
07-02 alone had 8 leads, mostly declined and charged (likely why Eddie paused on 07-03).

---

## 3. Why LSA isn't reaching more people (diagnosis)

**Budget is not the limit.** `campaign_budget` = $642.86, period DAILY, type LOCAL_SERVICES. Actual spend about $5/day,
under 1% of the cap.

**Bid: see section 4.** Short version: Google's own forecast is 3 leads/week at both $24 and $80, and Zen already gets
about 2.6/week, so the bid probably isn't what limits volume (forecast is weak evidence, see 4).

**Service area: 15 cities, city limits only.** Alpharetta, Auburn, Buford, Cumming, Dacula, Duluth, Grayson, Johns
Creek, Lawrenceville, Lilburn, Loganville, Norcross, Snellville, Sugar Hill, Suwanee. Missing vs Zen's site list:
Flowery Branch, Hoschton, Peachtree Corners. No county or ZIP coverage, so unincorporated Gwinnett/Forsyth/Hall gets
nothing. Meta uses 131 ZIPs (Gwinnett + Fulton + Hall + Forsyth + Hoschton) since 10-12, list in
`meta_zips_service_area_2026-10-12.txt`.

**Schedule.** Mon to Fri 8 AM to 8 PM, Sat 8 AM to 5 PM, Sunday OFF. 0 of 216 leads since 2025-01 came on a Sunday, 2
of 216 outside 8 AM to 8 PM. Impressions by weekday since 09-10: Mon 59, Tue 88, Wed 72, Thu 62, Fri 82, Sat 33.

**Services enabled (13):** ac_maintenance, ductless_heating_and_ac_services, heating_maintenance, hvac_maintenance,
install_ac, install_ducts_vents, install_heating_system, install_thermostat, repair_ac, repair_ducts_vents,
repair_heating_system, repair_hvac, repair_thermostat. All leads are category `xcat:service_area_business_hvac`.

**Lead types.** 203 PHONE_CALL + 13 MESSAGE since 2025-01, but no MESSAGE leads since the restart. Check whether
messaging is still on.

**Verification is fine.** License and insurance PASSED for HVAC in Georgia (geo 21143). Background check passed.

**Year over year.** Reach is down, lead count isn't:
- Impressions: Jun 2026 414 vs Jun 2025 1,306. October 2026 pace about 330 vs Oct 2025 639. Jan to Apr 2026 were ABOVE 2025, so the reach drop started around May 2026.
- Leads: Sep 2025 10, Oct 2025 8, vs about 11/month pace now. So in the fall, lead volume is on par with last year.

**Season.** October is shoulder season (Oct 2025 had a quarter of Jul 2025's impressions). Heating season should lift
Nov to Jan (Nov 2025 507 impr / 9 leads, Jan 2026 805 impr / 8 leads).

**Can't see via API:** review count and rating, call responsiveness (missed calls), competitors. These drive LSA ranking.

---

## 4. The $12 target cost per lead (tCPL): what we know and what we don't

### What the API shows (today)

`campaign.local_services_campaign_settings.category_bids` for `xcat:service_area_business_hvac`:
- `target_cpa_bid_micros` = 12,000,000 → **$12 target per lead**
- `manual_cpa_bid_micros` = 350,000,000 → $350 max per lead (manual bidding, not in use)
- `campaign.bidding_strategy_type` = MAXIMIZE_CONVERSIONS (= "Automated bidding (maximize leads)")
- `campaign.bidding_strategy_system_status` = ENABLED (no "limited" flag)
- `campaign.maximize_conversions.target_cpa_micros` = empty

The API only shows the value as stored NOW. It does not show when it was set, who set it, or whether Google applies it
while the dashboard box is unticked.

### What the dashboard shows (Edu, screenshot `~/Documents/Screenshot 2026-10-14 at 12.56.01.png`)

- Budget & bidding → "How do you want to bid?" → "Automated bidding (maximize leads)" selected.
- "Set a target cost per lead (optional)" box is UNTICKED.
- Ticking it shows: "$12 (current)", "$24", and a custom field that Google pre-fills with $80.
- Forecasts: $80 → "You may get 3 leads per week". $24 → "You may get 3 leads per week". $12 → no forecast, only the
  general warning ("Google recommends that you choose automated bidding without setting a target cost per lead. Target
  cost per lead is most effective if you have more than 15 leads per month").
- Nothing was saved (Cancel).
- The only place the UI shows the $12 is inside this dialog, after ticking the box.

### Change history: can we see when it was set? No.

- **API `change_event`:** keeps only 30 days. Zero events on this account from 09-15 to 10-15. So the $12 has NOT
  changed in the last month. Anything before that is gone from the API.
- **Google Ads UI Change history (Tools → Change history, all time):** shows ONLY account-level events (user invites,
  access grants, manager links, name change, location sync). Latest entry Dec 3, 2025. No campaign changes at all, not
  even Eddie's 2026-07-03 pause that the API logged at the time. So LSA bid/target/area changes don't show there.
- **Our own records:** the 09-30 pull (`zenair_lsa_0930.py`) read the bidding type and budget but NOT `category_bids`, so
  there is no older snapshot of the target. Nothing in our notes records what changed at the 09-10 restart.
- **Earliest possible date:** Google added the optional target field under Maximize leads in September 2024
  (support.google.com/localservices/answer/15406075), so the $12 was set Sep 2024 or later.

### Is it being applied? Unconfirmed. Evidence both ways

- **Not applied:** box is unticked (the saved setting). Since Sep 2024 the blended cost per lead never stayed near $12 for
  long: Jan to Jun 2026 averaged $22, 2025 ranged $17 to $79.
- **Applied:** UI labels $12 as "(current)". Blended cost since 09-10 is $13.00 per lead ($169.01 / 13), very close to $12.
- **Neither:** off-season months land near $12 anyway (Oct 2024 $11.96, May 2026 $12.48, Nov 2025 $16.80), so $13 fits
  both "target active" and "normal slow month". It could also have been set recently (for example at the 09-10 restart),
  which the history can't show.
- **Corrected reasoning (Edu caught it):** charged leads costing more than $12 ($62.40, $106.61) prove NOTHING. tCPL is an
  average, single leads can cost more (Google: "some conversions may cost more than your target and some may cost less").
  Don't use it as evidence.
- **Unknown:** whether Google's tCPL average counts uncharged leads ($13) or only charged ones ($84.50).
- **Forecast is weak evidence:** rounded to whole leads, thin data (~11 leads/month), accuracy unpublished. Small point in
  its favor: it says paying more gets nothing, the opposite of what a platform would want to say.

### Conclusion

We know the target is stored as $12 today and hasn't changed since 09-15. We can't see when it was set, by whom, or
whether it's applied. Only Google LSA support can confirm. Practical read: even if active, Google's forecast says
raising it adds about half a lead a week at most; the bigger limits are service area, hours, season.

### How to settle it

1. Ask Google LSA support to confirm whether a tCPL is active on HVAC and to clear the stored $12 (no target = Google's
   own recommended setup).
2. Then a before/after read of 3 to 4 weeks. Volume is tiny (2 to 4 leads/week) so it needs the full 4 weeks. Heating
   season starts in November, so compare against the same weeks of 2025 (Nov 2025: 507 impressions, 9 leads), not only
   against October.

---

## 5. Access audit (found while checking change history)

- **Manager links:** TSD MCC `4155514468` ACTIVE. **SearchLight Digital `6263403407` ACTIVE** (linked 2024-11-21 by
  elena@searchlightdigital.io via bulk upload, one day after TSD's link; an older link to the same MCC is INACTIVE).
  SearchLight is an LSA management platform (we cite their benchmarks in `clients/lilypad-septic/internal-notes.md`).
  Tools like that set bids by API, so they're a possible source of the $12, but there's no proof, and the API shows no
  changes by anyone since 09-15.
- **Users:** eddie@callzenair.com ADMIN, access@topservdigital.com ADMIN, khrystyna@topservdigital.com ADMIN,
  **localservicesteam@gmail.com ADMIN since 2024-01-29 (owner unknown, pre-TSD, Gmail so NOT Google)**,
  emily@callzenair.com STANDARD, rachel.shaffer22@gmail.com READ_ONLY.
- Old allowed-domains list included thecsms.com (previous agency, ads.csms@gmail.com was admin in Nov 2024).
- Nothing removed.

---

## 6. Updated elsewhere

- Command Center: `clients/zen-air.channels.lsa` set to live, lastChecked 10-14, spend7 $62.40, note with the numbers.
  Follow-up fu-051 created for the open items below.
- Team memory: `_contexto/memoria/tsd-zen-air.md` (10-14 entries) + README line; `topserv-google-ads-location.md` (LSA
  recipes, dashboard URL format, change_event bounds).

## 7. Open

- [ ] Google LSA support: is a tCPL active on HVAC? Clear the stored $12.
- [ ] After it's cleared: 4-week before/after read vs the same weeks of 2025.
- [ ] Service area → the 131 service-area ZIPs (heads-up to Andrea first, spend will likely rise; AM ticket if total spend changes).
- [ ] Via Andrea → Eddie: Sunday/evening hours (only if someone answers), who owns localservicesteam@gmail.com, mark the
      3 unmarked leads, which lead was the "won" job and its value.
- [ ] Ryan: is SearchLight Digital (6263403407) a TSD vendor or a leftover? Remove the link if unused.
- [ ] Check whether LSA messaging is still on (no MESSAGE leads since the restart).
- [ ] Lead 339121110 (charged $106.61, declined, 25s call): check in the dashboard whether it can still be disputed.
- [ ] Per-lead dashboard URL: when someone pastes one, record the format in `topserv-google-ads-location.md`.
