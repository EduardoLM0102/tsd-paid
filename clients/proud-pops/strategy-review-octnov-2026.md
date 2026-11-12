# Proud Pops: Client Strategy Review "Oct Review" (cycle 2026-10-16 to 2026-11-14)

AT task: https://app.agencytitan.com/tasks/instance/fc4041bd-72c3-4bad-84c0-84db5839bb06 (created by Angela 11-11, replaces the 10-02..10-31 task 4ae4f4a8, which is gone from AT).
Stage: Performance Reporting (assigned to Gui's AT user 7f88768a). Call 2026-11-16 11:00 CT. Cycle 2026-10-16 to 2026-11-14.
Pulled 2026-11-11 (`strategy_review_pull_2026-11-11.py`, GA4 438523825, CallRail export 10-14..11-03 in ~/Downloads). Data through 11-10; refresh after 11-14.
Slack overview drafted for Angela 11-11 (same format as 11-05), Edu sends it.

## KPI row (Client Performance KPIs)

| Field | Value |
|---|---|
| period_start_date | 2026-10-16 |
| period_end_date | 2026-11-14 |
| ad_spend | 8038.27 |
| agency_fees | 5000 (carried from the 10-02 row, filled by the AM after 11-05) |
| total_spend | 13038.27 |
| qualified_leads | 55 |
| cpl | 146.15 |
| recommend_budget | 25000 |

## How the numbers were built (10-16..11-10)

Ad spend $8,038.27
- Google Ads PPC 1051843378 excl. its LSA: $6,552.43 (Elec $2,543.48, Branded $2,069.06, Plumbing $1,012.08, HVAC $873.97, YouTube $53.83 on 10-16 only)
- LSA: $1,485.84 (in-account $806.21 + SA [1] 7261668241 $270.95 + SA [2] 6621969129 $408.68)
- Not included: My Favorite Service 9815330464 $457.06 (Smart campaign paused 11-09)

Qualified leads 55
- Forms 7 = Google Ads 'Website lead' (careers excluded since GTM v43): Branded 3 (10-16..11-03), Elec 3 + Plumbing 1 (11-04..11-10). GA4 google/cpc generate_lead on /schedule shows 5 (consent mode undercounts).
- Calls 27 = 12 (CallRail export, Google Ads source, Website pool, first-time, 60s+, 10-16..11-03, test caller ...8301 excluded, 4 GLSA-tracker calls excluded as LSA overlap) + 15 (11-04..11-10: Google 'First Time Phone Call' 10 = CallRail uploads 60s first-time, + 'Calls from ads' 60s+ 5 via call asset 225-5767; 3 of those Branded from area codes 818/206/361, not transcribed).
- LSA 21 = non-declined leads: PPC-account 11 of 14 (2 DECLINED + 1 CONSUMER_DECLINED out), SA [1] 5 of 5, SA [2] 5 of 5. All ACTIVE/NEW/BOOKED.
- Not counted: 'TSD - Website Call' taps (48), Repeat Phone Call (5), GBP/organic calls.

Split
- 10-16..11-03 Branded only: $2,685.01 / 26 leads (3 forms, 12 calls, 11 LSA) = $103.27
- 11-04..11-10 restored: $5,353.26 / 29 leads (4 forms, 15 calls, 10 LSA) = $184.60
- By channel: Google Ads $6,552.43 / 34 = $192.72; LSA $1,485.84 / 21 = $70.75

## Text written to AT

budget_rationale (table):
> Keep $25k/mo. Oct 16 to Nov 3 was Branded only after the mid-October cut ($2,685, 26 leads, $103 per lead). The service campaigns came back on Nov 4 at the $25k pace and now bid only on real calls and forms ($5,353, 29 leads, $185 per lead through Nov 10). Electrical carries most of the volume, Plumbing got its first leads the week of Nov 10, HVAC is capped at $30 per click. November is pacing to about $21k because the service campaigns are limited by ad rank, not budget; the gap can go to YouTube awareness or stay unspent. Numbers run through Nov 10, row to be refreshed after Nov 14.

additional_paid_ads_notes (task long text): see the block in the log entry 2026-11-11 (later) or the AT task.

## Status
- [x] KPI row created in AT 2026-11-11: record 73060891-c33c-44c8-8f35-53178eeb58b1, linked to the client field c72c4f7e (relationship f619cda1, link_origin runtime_embedded_create); fee + total added in a second write
- [x] additional_paid_ads_notes written (applied, rewritten once to add the fee)
- [x] Stage: the task had already moved to Host Review Call (Angela) before Paid wrote; Performance Reporting was not completed by us
- [ ] Refresh row after 11-14 (Command Center follow-up)
- [x] Client PDF report: `Proud Pops - Performance Report (Oct 16 - Nov 10).pdf` + HTML source in this folder (11-11). [ ] Attach to the AT task (Drive upload blocked by the permission classifier; Edu attaches in the UI or allows the Drive write).

## Call review (added 11-11, transcripts)
22 recorded Search-ad calls (CallRail Conversation Intelligence transcripts, `transcription` field) + 17 LSA calls (local whisper) + 7 LSA message threads. Logs: `call-wins-log.md`, `lsa-call-wins-log.md`.
- Search-ad calls 27: 22 reviewed = 9 booked new jobs, 3 existing-customer service, 4 open, 6 not leads; 5 call-button calls not recorded (recording OFF on 210-225-5767).
- LSA 21: 3 booked, 10 open real requests, 8 not customer requests.
- Verified leads = 55 tracked − 14 not leads − 3 existing-customer = **38** (forms 7 + calls 13 verified + 5 unreviewed + LSA 13). CPL **$211.53** (Search $6,498.60/25 = $259.94; LSA $1,485.84/13 = $114.30). Confirmed booked jobs on the calls: 12 (9 ads + 3 LSA).
- Stretches: 10-16..11-03 verified 12 of 26 → $223.75 (Branded calls = existing customers, job seekers, admin); 11-04..11-10 verified 26 of 29 → $205.89, 7 booked.
- KPI row UPDATED to 38 / $211.53 (rationale says 55 tracked, 38 verified). Task notes rewritten with the review at the top. PDF v2 rebuilt with a call-review section.
- AM asks → Command Center fu-157 (recording on 225-5767, 2 LSA disputes, weekend fees, lead statuses, LSA text sequence, $299 fee consistency, tag test calls).
- 11-11 later: CLIENT version rebuilt as a designed 3-page navy/gold PDF (`Proud Pops - Performance Report (Oct 16 - Nov 10).pdf`, source `Proud-Pops-Performance-Report_2026-10-16_11-10_client.html`): verified numbers only, 4 KPI tiles, call-outcome bar, staff-sensitive items (lead-status marks, text sequence, $299 fee) kept out and left in Angela's notes / fu-157. The plain 5-page version is now `... - internal.pdf`.
- 11-11 final: Edu wants the client PDF PLAIN (no colors). Rebuilt black-on-white Times with the designed structure kept (`..._client.html` = plain, `..._client_designed.html` = the navy/gold pass, not used). `Proud Pops - Performance Report (Oct 16 - Nov 10).pdf` = the plain client version.
