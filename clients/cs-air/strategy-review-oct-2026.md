# C&S Air — Client Strategy Review "Oct Review" (AT 03fff3a7, Gui's copy), Paid row 2026-11-13

Cycle 2026-10-17 → 2026-11-15, call Mon 2026-11-17 09:45 ET. **Data through 11-12** (3 days left in the cycle): top up Monday before the call. Twin task fd5eb77f ("Oct/Nov Reviewwe", same cycle) left untouched.
Rule: 2026-11-12 (existing customers who reach the office through an ad COUNT, labelled). Every call judged from the transcript.

| Field | Value | Source |
|---|---|---|
| period | 2026-10-17 → 2026-11-15 | task |
| ad_spend | **2062.53** (thru 11-12) = Branded $570.40 + Heating NB $520.01 + PMax $684.55 (paused 10-23) + Cooling NB $114.41 (paused 10-23) + LSA $173.16 | Google Ads API 5563867754 |
| qualified_leads | **16** = Google 6 (5 ad calls + 1 form) + LSA 10. 3 new + 12 existing + 1 form | CallRail on 817-442-6949 + LSA transcripts |
| cpl | **128.91**. Branded $95.07 (6), LSA $17.32 (10), PMax/Cooling/Heating $1,318.97 for 0 | |
| agency_fees / total_spend | blank | |
| recommend_budget | **5500** (keep the approved total, no increase) | AT client record |

## Google 6 (all Branded; PMax, Cooling and Heating had 0 calls and 0 forms)
CallRail tracking number 817-442-6949 (call asset on every campaign), 5 calls in the cycle, all transcribed:
- 10-19 10:18 · 84s · Arlington — existing: heater part estimate never emailed. ✅ existing
- 10-19 16:07 · 105s · Arlington — existing: moving an appointment to Nov 5. ✅ existing (reschedule)
- 10-20 08:28 · 95s · Arlington, gclid, first call — kitchen unit no air, booked same day 12-3. ✅ **NEW**
- 11-06 08:54 · 297s · Arlington — existing membership customer (2 systems) booking maintenance. ✅ existing
- 11-11 13:32 · 205s · Grand Prairie — existing customer booking maintenance (Nov 24, 12-3). ✅ existing
- Form: `[TSD] Submit lead form` 11-03 on Branded (1). Not verified in GHL.
Google taps (`[TSD] Click to call` 17: PMax 13, Branded 4) not counted.

## LSA 10 of 12 (transcripts in `_pessoal/call-wins/cs-air-review/`, outcomes in lsa-call-wins-log.md)
| Created | Google | Charged | What happened | Counted |
|---|---|---|---|---|
| 10-19 08:19 | BOOKED | no | existing (Steve) going ahead with UV bulb + antimicrobial upsell | existing |
| 10-20 08:59 (+10-21) | DECLINED | no | existing (Justin) no cold air, fixed by phone with Phil, cancelled visit | existing (weak: no job) |
| 10-21 18:57 msg | BOOKED | yes | **NEW** Mansfield, "time for unit replacement", quote | new |
| 10-22 12:05 (+10-26) | ACTIVE | yes | **NEW** Bailey, Fort Worth, referral, repair quote, comparing a 2nd opinion | new |
| 10-23 14:24 (+10-29 same contractor) | DECLINED x2 | no | existing commercial: Midland warranty job, callback owed | existing (1 contact) |
| 10-27 09:17 | DECLINED | no | existing moving a 2-system tune-up | existing (reschedule) |
| 10-30 13:16 | BOOKED | yes | existing asking filter size | existing (weak: question) |
| 10-30 16:02 | ACTIVE | no | existing booking winter check-up, offered $165/yr membership | existing |
| 11-02 10:12 | BOOKED | no | existing commercial (Burleson boutique) unit down | existing |
| 11-04 15:23 | ACTIVE | no | job seeker | no |
| 11-05 14:35 (+11-09) | ACTIVE | no | existing commercial: hotel room offline ~2 months, part on order | existing |
No LSA leads 11-06..11-12. LSA $173.16 = 3 charged leads ($57.72 each).
If Edu wants the 2 weak ones out (solved by phone, filter question): 14 / $147.32, LSA 8 / $21.65.

## Written to AT — budget_rationale
> Keep the approved $5,500/mo, no increase. The account spends about $1,700/mo right now on purpose: Performance Max and cooling search were paused Oct 23 (PMax $685 and cooling $114 this cycle, 0 calls), and heating search has $520 and 0 leads so far, with a final read on Nov 16. What works is Branded Search ($570, 6 leads, $95 each) and LSA ($173, 10 leads, $17 each, back to normal reach since the insurance was fixed Nov 2). 16 qualified leads on $2,063, $129 each, but 12 of them are existing customers who called through the ad; 3 were new (plus 1 form). The account needs new demand, which is why we asked for a seasonal heating offer. Data runs through Nov 12; final numbers for Nov 13 to 15 get added before the call.

## Written to AT — additional_paid_ads_notes
(see the AT task; same text as sent)
