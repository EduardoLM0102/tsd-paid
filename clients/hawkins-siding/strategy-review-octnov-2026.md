# Hawkins Siding — Client Strategy Review "Oct/Nov Review" (AT eeb41f98), Paid row WRITTEN 2026-11-20

Cycle 2026-10-24 → 2026-11-22, call 2026-11-24 15:17 UTC. **Data through 11-19** (3 days left in the cycle): Edu refreshes before the call. Stage Performance Reporting `a5e10018` (Gui), NOT submitted (task flipped to in_progress on write). No twin review task found (list_tasks active on the client 11-20: only this one + 4 Weekly Agency Analytics Checks + Internal Request "Need Before & After Photos" from July, not Angela's).
Client TERMINATED 11-02 (30-day notice, ads to ~12-02): factual review, no growth pitch.
Rules: existing customers count (labelled; none this cycle), every LSA lead judged from the transcript / message text, never Google's status.

## Written to AT (2026-11-20, Gui via Claude)
- KPI row **a57b3633-2a10-420b-9120-fcf1520b96aa** created + linked on client cc8f5d01 (field c72c4f7e). agency_fees + total_spend blank (no prior Hawkins rows).
- `additional_paid_ads_notes` written on eeb41f98, read back OK.

| Field | Value |
|---|---|
| period | 2026-10-24 → 2026-11-22 |
| ad_spend | **5909.07** = LSA $3,423.97 + Nonbranded $1,830.72 + PMax $633.08 + Branded $21.30 (10-25..10-27, paused 10-28). Meta $0 visible (see below) |
| qualified_leads | **54** = LSA 25 (all new: 20 calls + 5 msgs) + Branded 1 call + 28 Google lead forms (unverified) |
| cpl | **109.43** (LSA $136.96; Google $85.69 with forms as-is; verified-only 26 = $227.27) |
| recommend_budget | **blank** (cleared 2026-11-20 on Edu's call: "ta em offboarding, n precisa recomendar budget - deixa rodar como ta"). Pace for reference: ~$210/d, ~$2,750 from 11-20 to 12-02 |

## Method
- Spend + forms + call_view + LSA leads: `clients/hawkins-siding/hawkins_review_1120.py` (READ-ONLY, run via tsd.sh). Google 2198608170, LSA inside (21211420266, not migrated to PPL PMax).
- LSA: `pull_lsa.py hawkins-siding-review-1120 2198608170 2026-10-24 2026-11-19` → 34 leads (29 calls, 5 msgs; 25 charged = 20 calls + 5 msgs), 33 recordings, transcribed locally (faster-whisper base.en, 3 parallel shards, scratch hk_tx.py). Files in `_pessoal/call-wins/hawkins-siding-review-1120/` (gitignored).
- Google ad calls: CallRail API 403 since ~10-28 (client terminated, access removed) → recordings not accessible. call_view in cycle: Branded 10-26 08:06 32s (under 60s, not counted), Branded 10-26 14:13 147s (counted; verified real in the 10-28 Jared doc), NB 11-17 16:36 no duration (not counted). NB 'First Time Phone Call' CallRail upload 11-09 in All conv: unverifiable, not counted. Click-to-call taps (NB 11-04, 11-17; LSA 11-01) not counted.
- Google lead forms: lead_form_submission_data 10-24..11-19 = 28 (PMax 25, NB 3; 11-20 one excluded), all with name/phone/email/city/ZIP, no duplicate phone/email. Delivered to office.hawkinssiding@gmail.com (11-02 confirmed), outcome not visible → counted as submitted, unverified. One Tulsa OK (74106, no gclid), one 'Dallas 79903' (El Paso ZIP, likely typo), one Sun Valley 75416. Google's own count: PMax 24 / NB 3 'Lead form - Submit'.
- Meta 10086442468052740: 11-20 still "Ad account not found or you do not have access" (since 11-03). Last confirmed 10-26: all 9 campaigns PAUSED since 08-20 (client request). Counted $0.

## LSA leads (Google status / charged beside the transcript outcome)
| Created | Google | Charged | Transcript | Counted |
|---|---|---|---|---|
| 10-24 12:46 | BOOKED | yes | garage-front siding repair/replacement after storm, estimate booked | new |
| 10-24 13:00 | ACTIVE | yes | door-jamb wrap hit by a car, will text photos for a quote | new |
| 10-26 11:57 | ACTIVE | yes | rotted wood at back of garage → siding, estimate; caller put office on hold mid-call | new |
| 10-26 13:42 | ACTIVE | yes | wants to buy vinyl siding material only | no (materials) · already CREDITED by Google |
| 10-29 11:50 | DECLINED | no | 0s, nothing | no |
| 10-31 15:23 | BOOKED | yes | Bedford soffit/fascia pulled away, estimate booked | new |
| 11-02 10:41 | DECLINED | no | client-side test call checking the number | no |
| 11-02 12:54 | BOOKED | yes | partial replacement of wood boards, scheduling evening/weekend | new |
| 11-02 14:33 | BOOKED | yes | Corinth, repair in multiple areas | new |
| 11-02 14:48 | BOOKED | yes | builder, new-construction wood cladding + soffit/fascia, Heath | new |
| 11-02 15:56 | BOOKED | yes | SW Fort Worth (Benbrook) siding problem, visit next day | new |
| 11-03 11:33 msg | ACTIVE | yes | siding around a sliding glass door, gave address, "tomorrow" | new |
| 11-03 16:48 | ACTIVE | yes | wants estimate for home, asked siding types / insulated siding, will circle back | new (weak) |
| 11-05 09:05 | DECLINED | yes | DIY, looking for LP SmartSide install gauges | no · charged, not credited → rate bad (fu-161, ours) |
| 11-05 14:18 | DECLINED | no | no conversation | no |
| 11-06 14:19 | DECLINED | no | 5s, nothing | no |
| 11-09 08:54 | ACTIVE | yes | Bedford, water getting in around a window, repair estimate | new |
| 11-09 12:17 | BOOKED | no | concrete contractor, water intrusion through siding at a client's home, Highland Village walk Friday | new |
| 11-09 12:37 | DECLINED | no | Spanish caller, wrong number (parks) | no |
| 11-10 15:18 (+11-16) | ACTIVE | yes | loose siding repair, estimate; 11-16 called back: "I signed Friday", when does work start | new · SIGNED |
| 11-11 11:58 | ACTIVE | yes | Fort Worth repair or replace, estimate next day | new |
| 11-11 13:43 | ACTIVE | no | no conversation | no |
| 11-12 10:49 | ACTIVE | yes | roofer needs siding removed/reinstalled, wanted same day, info taken | new |
| 11-12 12:35 msg | ACTIVE | yes | siding repair/replace (dog chewed), Mesquite, scheduling | new |
| 11-13 11:30 | ACTIVE | yes | Murphy, hole above front door to attic, estimate | new |
| 11-13 12:25 msg | ACTIVE | yes | siding replacement info, brick home with siding on 2 sides + chimney (office replied, no answer yet) | new |
| 11-14 09:41 msg | ACTIVE | yes | small 2nd-floor siding/trim repair, animal/weather damage | new |
| 11-16 14:08 | ACTIVE | yes | Garland, squirrel damage, small repair, free quote | new |
| 11-16 18:03 (+11-18 empty) | ACTIVE | yes | piece of siding back on the house, estimate | new |
| 11-18 08:22 | ACTIVE | no | no conversation | no |
| 11-18 13:49/14:12 | ACTIVE | no | Hardie board + chimney work, estimate this week | new |
| 11-18 18:07 | ACTIVE | yes | window trim carpentry, estimate (address said Tyler then 75001) | new |
| 11-19 08:50 msg | ACTIVE | yes | skirting for a new double-wide (office replied 11-20, happy to help) | new |
| 11-19 12:56 | ACTIVE | yes | siding replacement, Dallas 75252, estimate next day | new |
Counted 25 (20 calls + 5 msgs), 0 existing. Not counted 9 (5 no conversation, 1 wrong number, 2 materials/DIY, 1 test).
LSA rating (ours, fu-161, not done here): 11-05 09:05 DIY gauges (charged, DECLINED, not credited). 10-26 13:42 already CREDITED.

## budget_rationale (as written, updated 2026-11-20)
> Data through Nov 19 (cycle Oct 24 to Nov 22; the last days get added before the call). No budget recommendation: Hawkins is offboarding, so the current settings keep running as they are until the end of the notice period (around Dec 2). Ad spend $5,909.07, all Google: LSA $3,423.97, Nonbranded Search $1,830.72, Performance Max $633.08, Branded $21.30 (paused Oct 28 at the client's request). Meta $0: campaigns paused since Aug 20 at the client's request, and the Meta account has not been visible to TopServ since Nov 3. 54 leads, $109.43 each: 25 LSA leads checked one by one (20 calls listened to + 5 messages read, all new customers, none existing), 1 Branded call (Oct 26, 147s, heard before call-tracking access ended) and 28 Google lead forms (25 Performance Max, 3 Search) counted as submitted, not verified, because they go straight to the office email. 26 verified leads alone = $227 each. LSA $137 per lead; Google $85.69 per lead counting forms as is.

## additional_paid_ads_notes (as written, HTML in AT, Budget line updated 2026-11-20)
**Data through Nov 19** (cycle Oct 24 to Nov 22; we add the last days before the call). Ads keep running on the current settings until the end of the notice period, around Dec 2.
- **Totals:** $5,909.07 ad spend, 54 leads, about $109 each. LSA $3,423.97 for 25 leads ($137 each). Google Search and Performance Max $2,485.10 for 29 leads (1 call + 28 Google lead forms). Meta $0: the Meta campaigns have been paused since Aug 20 at the client's request, and the Meta account hasn't been visible to TopServ since Nov 3, so we couldn't recheck it.
- **How leads were counted:** we listened to every LSA call (33 recordings, 29 call leads) and read the 5 LSA messages. 25 were real siding and exterior requests, all from new customers (20 calls, 5 messages), and most were given an estimate visit on the call. Not counted: 9 calls (5 with no conversation, 1 wrong number, 2 people looking to buy materials or install parts, 1 test call to check the number). The Google call recordings aren't accessible to us since late October, so the one Google call counted is the 147-second Branded call from Oct 26, heard before access ended. The 28 Google lead forms (25 from Performance Max, 3 from Search) go straight to the office email, so they are counted as submitted, not verified; one of them gave a Tulsa address.
- **LSA:** the strongest channel this cycle. About $116/day over the last two weeks, 25 new requests (repairs, soffit and fascia, partial and full siding replacement, trim, a new-construction builder). The Nov 10 caller with loose siding called back Nov 16 to say she had signed and asked when the work starts.
- **Google:** Performance Max $633.08, 25 lead forms (about $25 each). Nonbranded Search $1,830.72, 3 lead forms. Branded $21.30 (Oct 25 to 27), 1 call; paused Oct 28 at Jared's request. During the cycle we tracked campaigns by UTM (Oct 28), paused the Vinyl ad group (Oct 30) and kept Nonbranded on service searches only, blocking material and how-to searches (Oct 28, Nov 2, Nov 6).
- **Budget:** no recommendation, since Hawkins is offboarding. The current settings keep running as they are until the end of the notice period, around Dec 2.
- **Open ask:** could you check with Hawkins how many of the 28 Google lead-form contacts since Oct 24 turned into estimate visits? They arrive in the office inbox, so we can't see what happened after the form.

## Refresh before the 11-24 call (Edu)
- Re-run `hawkins_review_1120.py` with B = 2026-11-22 (spend, forms) + `pull_lsa.py ... 2026-11-20 2026-11-22` and transcribe the new LSA calls; update row a57b3633 (ad_spend, qualified_leads, cpl) + the notes' numbers and drop "Data through Nov 19".
- ~~Decide recommend_budget~~ DONE 11-20: blank, no recommendation (Edu). Row + notes updated in AT and read back.
