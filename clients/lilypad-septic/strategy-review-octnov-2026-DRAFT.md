# Lilypad Septic — Client Strategy Review, Oct/Nov (AT f0398cbf), Paid row DRAFT 2026-11-11

Cycle 2026-10-12 → 2026-11-10. Angela's call 2026-11-12 09:32 ET. Row goes in the client's "Client Performance KPIs" (object 4038154a, field c72c4f7e). NOT written to AT yet (permission + Edu's go).

| Field | Value | Source |
|---|---|---|
| period | 2026-10-12 → 2026-11-10 | task |
| ad_spend | **$983.12** (Google only: Branded $154.63, NonBranded $828.49; Meta $0, no LSA) | Google Ads API; Meta MCP (acct 123589321338300, $0) |
| qualified_leads | **40** = 11 call-extension calls ≥60s (call_view) + 20 first-time website-pool calls ≥60s with a gclid (CallRail) + 9 RYNO lead forms | call_view, CallRail, conversion actions |
| cpl | **$24.58** | |
| agency_fees | (blank, Angela) | |
| recommend_budget | $2,000/mo (the approved plan: Google ~$1,400 + Meta ~$600) | memory 08-20 |
| budget_rationale | Google ran at ~$33/day of the $46/day it has, so the account underspent the plan; Meta's $600 was never built. Cost per qualified lead ~$25. Hold $2,000 and either build the Meta awareness piece or let Google NB use its budget after the 11-06 audit fixes (recheck 11-13). | |

Notes for additional_paid_ads_notes:
- Google counts 43 conversions, but 21 of them are "[EB] Click to call" taps; the 40 above are calls people actually made plus forms.
- Business Profile brought 287 calls in the same window (175 ≥60s, 121 first-time), none paid. Paid Search is a small share of their phone volume.
- 11-06 audit fixes applied (sitelinks to /contact/, restroom ad to /portable-restrooms/, bids to first page, brand misspellings to Branded, QS2 keyword paused); first read 11-13 (fu-133).
- Still open: RSAs at 8 headlines, logo disapproved, /specials/ offers expired 10-31, nights/Sunday cut + presence geo (AM).


---

## 2026-11-12 — TRANSCRIPT PASS (final numbers for the row)

All 35 CallRail calls from Google Ads (gclid or source Google Ads) 10-12..11-10 pulled; 33 recordings transcribed locally (faster-whisper small.en, audio + transcripts in _pessoal/call-wins/lilypad-ads/, never in clients/). 2 unrecorded = the City of Hutchinson's first two unanswered attempts.

| Outcome | Calls |
|---|---:|
| New customer / new job | **8** (10-15 odor + gurgling north of Salina, VM; 10-17 pumping price Hutchinson, after-hours VM; 10-26 septic full New Cambria, VM; 10-27 new residence, booked into the system; 10-28 trailer restroom pricing, VM; 10-29 overflowing septic McPherson/Galva; 11-03 City of Hutchinson rent 5 porta-potties; 11-03 porta restrooms Wichita, VM) |
| Repeat customer, new order | 3 (10-20 running race 2 porta-potties; 11-09 disc golf event; 11-09 sewer backup at a porta-potty customer) |
| Existing customer, service/billing only | 13 (pickup requests x4, maintenance plan x4, billing x2, realtor re past work, zoo route day, plumber update) |
| Not a lead | 2 (10-12 caller wanting the owner, 11-05 complaint about a driver on the road) |
| Hang-up / empty voicemail | 7 |

- **15 of 33 calls during business hours ended in voicemail** after "please hold while I try to connect you" (5 of the 8 new leads only reached voicemail). 13 existing-customer calls came through ads because customers google the company name and click the ad.
- Call-extension calls (11 in call_view, Google forwarding numbers) have no recordings, can't be verified, left OUT of the count. 9 RYNO form fills counted (GHL forms, not verifiable here).

**Row values (final):** ad_spend $983.12 · qualified_leads **20** (8 new + 3 repeat new orders from calls + 9 forms) · cpl **$49.16** · recommend_budget $2,000/mo · agency fee blank (Angela).

**2026-11-12 WRITTEN TO AT (Edu: "put that in the task"):** KPI row 1523de86-c328-4c29-8074-8e6c74326a09 linked to Lilypad (spend 983.12 / 20 leads / CPL 49.16 / rec 2000, rationale = "ramp first, ask for more at the December review") + additional_paid_ads_notes on task f0398cbf. Stage NOT completed. Fee/total spend blank for Angela.

**2026-11-12 UPDATED (existing-customers rule):** row 1523de86 → 33 leads (20 + 13 existing) / CPL $29.79, rationale + notes rewritten.
