# C&S Air LSA review, 2026-11-02 (read-only, nothing changed)

Asked by Edu (fu-091 leftover from fu-088): why LSA, the best C&S channel, gets so little reach, and whether settings can unlock more.
LSA campaign `15794404030` inside Google Ads `5563867754` (MCC 4155514468). Scratch scripts not kept; resources used as in `clients/zen-air/2026-10-14-lsa-review.md` section 1 (verification artifact fields: `artifact_type`, `status`, `insurance_verification_artifact.rejection_reason`).

## Bottom line

**Reach collapsed on 2026-09-11 and the timing matches a failed insurance verification, not a settings problem.**
- Daily impressions: 60–90/day on 09-07..09-10, then 5–15/day from 09-11 onward (Oct total 206 vs 526 in Sept and 672 in July).
- Insurance status in the account: **FAILED**. History: the policy on file (uploaded 2025-12-10) is EXPIRED; a new document uploaded **2026-09-09** was rejected as **WRONG_DOCUMENT_TYPE**. No valid insurance since. License (TX Class B ACR) PASSED.
- Google limits LSA ads when insurance verification lapses. Nothing else changed: no campaign changes in the last 30 days, budget/schedule/services/area all as before.

## Settings (all reasonable, none of them is the limit)

| Setting | Value | Read |
|---|---|---|
| Status | ENABLED, ELIGIBLE | The API shows no "limited" flag, but insurance FAILED at account level |
| Budget | $23.26/day | ~$163/week. At $65 per charged lead that is ~2.5 charged leads/week max. Fine today (reach-limited), becomes the limit once insurance is fixed |
| Bidding | Maximize leads. A $25 "max per lead" is stored but not used (charged leads cost $65) | Same pattern as Zen Air's dormant $12 |
| Schedule | Mon–Fri 7am–9pm, Sat–Sun 9am–5pm | Fine. Most impressions Mon–Thu |
| Job types | 15, incl. heating repair/install/maintenance, thermostats, ducts, ductless | Complete |
| Service area | 41 locations: 26 ZIPs + 15 cities (Fort Worth, Arlington, Mansfield, Burleson, Grand Prairie, Midlothian...) | Wide, not the limit |
| Reviews | UI only, not checked | Check in the LSA dashboard |

## Lead handling (also hurts ranking)

Since 08-01: 47 leads, ~16 BOOKED, ~24 DECLINED (half), 7 ACTIVE (never marked, 6 of them since 10-22). Several declined leads were charged. Google ranks LSA partly on responsiveness and how leads are handled, and charged leads that were job seekers/spam/out-of-area can be disputed.

## Recommendation

1. **AM ticket (most important):** C&S uploads a current certificate of insurance (general liability, the policy declarations page / COI, not an invoice or another document) in the LSA dashboard. Expect reach to recover once it passes.
2. Mark the 7 ACTIVE leads, and dispute charged leads that weren't real jobs.
3. Once insurance passes and impressions recover: raise the LSA budget from $23.26 to ~$50–60/day using part of the spare ~$100/day (same approved total, no client approval needed). LSA is the cheapest booked-job channel this account has.
4. Check reviews count/rating in the LSA dashboard (UI only).

## Update 2026-11-02 (later): a valid COI already exists in Drive

- **File:** Drive folder "Insurance" (1kY1OTUQd0KUpR3fyQHtPB-jYpExjey_9, created 2026-09-23), `City of Fort Worth DevelopmentalMechanical_C _ S Air Inc_2627 MASTER_7-20-2026_131863860.pdf` (file id 1DxgAUj-glJD4VG8TmpgP0GjTCaecUM2r).
- **What it is:** ACORD 25 Certificate of Liability Insurance dated 7/20/2026. Insured: C & S Air Inc, Kennedale TX. Producer: Patterson & Associates Insurance Agency (Richardson TX). Insurer: Employers Mutual Casualty Co (NAIC 21415). Certificate holder: City of Fort Worth Development/Mechanical.
- **General liability:** policy 6D57934, **7/31/2026 → 7/31/2027**, $1M each occurrence, $2M general aggregate (matches the $2M Google had on file). Also auto (6E57934), umbrella (6J57934, $2M) and workers comp (6H57934), same dates.
- It landed in Drive 09-23, two weeks AFTER the rejected 09-09 LSA upload, and the API shows no LSA upload since. So the valid document was probably never submitted to LSA.
- **Licenses (Agency Titan client note):** TACLA003204C exp 01/03/2027, TACLB26092E exp 08/17/2027 (TX ACR), OK170981 exp 05/31/2027, RMP40972 (plumbing, to delete). LSA shows TX Class B PASSED. TDLR doesn't publish insurance; the license lookup isn't needed for this fix.
- Agency Titan: task "Proof of Insurance" 741de862 (process "Missing or Expiring License", created 2026-11-02, not started) is the place to attach it. Older task 4d6a7419 "DELIVERY STOPPED - C&S LSA has served nothing since 17-Aug" (Aug 18-26 outage) is related history.

**Next step:** upload this PDF in the LSA dashboard (Profile & budget → Business details → Insurance) for C&S. UI only, not possible via the API.
**2026-11-02: Edu submitted the COI in the LSA dashboard.** Verify status ~11-05 (fu-116).
