# Napps — Client Strategy Review "Oct/Nov Review" (AT 0de4a6cc), Paid row DRAFT 2026-11-19

Cycle 2026-10-19 → 2026-11-17. Call 2026-11-19 13:42 UTC. Stage Performance Reporting `fa40420e`, assigned to Gui (7f88768a), not_started. Twin task 6db957ea (cycle 10-20..11-18, call 11-20 17:48 UTC, Performance Reporting assigned to Edu b86625af): same label, created 10-09; 0de4a6cc was created 10-27. Which one is real is for Angela to confirm (fu-169 pattern).
Counting rule: existing customers who reach the office through an ad COUNT, labelled existing (2026-11-12). Every lead judged from the transcript / message / GHL record, never Google's status.

## Spend (pulled 2026-11-19)

| Channel | Spend | Notes |
|---|---|---|
| Google PPC 9509605037 | $2,205.39 | Branded $133.44 / NB Heating $1,371.21 / NB Plumbing $700.74. NB paused 10-22 → relaunched 10-27 on the 2 new pages |
| LSA 9239407401 | $1,639.74 | 174 clicks, 25 Google conv |
| Meta 438790276573563 | $148.97 | ARL awareness only ($5/d, ZIP 75605), 31,158 impr, reach 7,473, freq 4.17 over 30 days |
| **Total** | **$3,994.10** | |

## Google (CallRail "Google Ads" number 903-289-7073 + GHL web contacts with gclid)

- 10-20 chat widget (GHL), paid click "hvac maintenance" on the old Heating campaign → /schedule-now/. Name + phone + email, content not visible. Counted (new, web).
- 10-23 214s, existing customer (Buckeye St.) checking whether a motor came in for his unit. Counted (existing).
- 10-29 / 10-30 / 11-02 / 11-03, one existing customer (Winona): gas leak plumber visit booked then cancelled (fixed by someone else), then furnace won't light → booked, tech on site 11-03. Counted once (existing, booked).
- 11-04 chat widget (GHL), paid click "heating repair" on NB Heating → furnace page. Counted (new, web).
- 11-16 225s, existing commercial customer (Huntington Hills) asking about CO detector + TDLR registration on the boiler/water heater Napps just installed. Counted (existing).
- 11-16 418s, NEW caller, heat trips the breaker in a trailer house, booked 11-17. Via 'heating repair' on NB Heating. Counted (new, booked).
- Not counted: 11-15 Plumbing LP form "test" (Pakistan IP, Asia/Karachi timezone, Napps' own tracking number as the phone, ZIP "test") = junk submit. This is the "Tyler form" Google showed.

Google = 6 (3 new incl. 2 chats, 3 existing).
(Correction after the LSA pass: the 11-16 Huntington Hills caller is the same customer as the LSA 11-03 caller, phone ...2206. Counted once, under LSA. Google = 5: 3 new + 2 existing.)

## LSA (37 leads 10-19..11-17, 25 charged; all 42 recordings transcribed locally, base.en/small.en; messages read from lsa.json)

New (18): 10-19 two restaurants (drain clog, after-hours approved) · 10-20 Harvest Creek apartments Marshall AC, BOOKED · 10-20 Jefferson leak, asked price ($139 eval), "will check back" (Google DECLINED) · 10-20 msg water heater replacement quote (status NEW = no reply seen) · 10-23 washer line referred by Liberty City Septic, BOOKED · 10-23 Hallsville shower leak, booked then cancelled (got someone sooner) · 10-28 msg kitchen faucet install (DECLINED) · 10-30 Marshall emergency plumbing, after-hours, BOOKED · 11-02 msg 40 gal gas water heater, BOOKED · 11-10 Beckville gas + water leak · 11-12 Longview gas repipe, visit same afternoon · 11-12 msg gray line sink (only the auto-reply on record) · 11-13 La Fama Foods meter running / leak · 11-14 Joinerville septic line · 11-15 new homeowner Longview toilet leak + 20-yr water heater, plumber sent same morning · 11-16 St. Luke's church heaters not coming on (answering service msg) · 11-16 Gilmer clogged toilet · 11-17 evening burst ball valve, on-call.
Existing (12): 10-20 appointment follow-up · 10-22 yard sewer blockage (regular) · 10-22 approving a ~$1,000 estimate · 10-29 Longfellow Arms sewage emergency · 11-02 KV Pizza Gilmer AC back down · 11-03 one-time AC inspection (installed by Napps), BOOKED · 11-03 Huntington Hills boiler bid question · 11-10 Willow Lake apartments tub replacement quote · 11-13 apartments boiler pump follow-up · 11-13 Gilmer commode (customer since July) · 11-16 Marshall gas test/certification follow-up · 11-17 fall maintenance already paid.
Not counted (7): 10-23 07:48 no conversation (CHARGED) · 10-23 wrong number · 11-04 wrong company (Shawnee AC) · 11-04 x2 no conversation · 11-07 no conversation (CHARGED) · 11-14 no conversation. Charged non-leads to rate bad = 10-23 07:48 + 11-07 11:37 (fu-161, ours).
LSA budget $154.29/day but spends ~$55/day over the cycle (~$97/day last week): not budget-limited.

## Row (to write)

| Field | Value |
|---|---|
| period | 2026-10-19 → 2026-11-17 |
| ad_spend | 3994.10 |
| qualified_leads | 35 (21 new + 14 existing) |
| cpl | 114.12 (new only $190.20; LSA $54.66; Google $441.08) |
| recommend_budget | 5300 (hold every setting; this is what the current settings spend in a full month: NB $100/d full month ~$3,040 + Branded ~$150 + LSA ~$2,000 in heating season + Meta ~$150) |

## Written to AT 2026-11-19 ~13:05 UTC
- KPI row **cadd5d83-042c-42f0-b484-82e47a841237** created + linked on the Napps client (3994.10 / 35 / 114.12 / rec 5300, agency fee + total spend blank).
- `additional_paid_ads_notes` written on 0de4a6cc (6 bullets: how counted, LSA, Google, Meta, budget, open items to Angela).
- Stage NOT submitted (Edu). Twin 6db957ea untouched.
- Rec $5,300 = Claude's estimate of a full month at current settings, not a change; Edu can edit the row.
- Spend pulls: clients/napps/napps_review_1119.py + napps_review_1119b.py (run from google-ads-ratos/scripts via tsd.sh).
- 2026-11-19 ~12:54 UTC: Edu said 'sent' (stage submitted by Edu in the UI).
