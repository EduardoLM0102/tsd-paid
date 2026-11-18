---
name: tsd-lsa-rating-is-ours
description: "Edu rule 2026-11-12: rating LSA / pay-per-lead leads (bad leads for credit, booked etc.) is TSD Paid's job; never put 'ask the office to rate/mark leads' in AM notes or client reports"
metadata:
  type: feedback
---

Rating LSA / Pay-per-lead leads in the Google Ads lead inbox (rate bad so Google may credit, mark booked/archived) is **our** work, not the client office's and not the AM's. Keep it OUT of AM notes, strategy-review notes and client reports.

**Why:** Edu, 2026-11-12, reviewing the King's and Spencer strategy reviews ("the rate as bad is ours, keep it out of the report for Angela").

**How to apply:** when a call review finds charged non-leads, put them on our own follow-up (fu-161 "Migrated LSA accounts: check and rate every lead") with date/time + reason, and rate them ourselves (Cowork or UI). In AM notes just report lead counts and quality. Supersedes older notes that said "ask the office to mark/dispute leads". Related: [[tsd-lsa-no-disputes]], [[tsd-existing-customers-count-as-leads]].

**2026-11-17 API write-back WORKS (Watt's Right, 117 leads rated):** `LocalServicesLeadService.ProvideLeadFeedback` (API v24) rates a lead; script pattern `clients/watts-right/wr_lsa_rate_1117.py` (reads a local ratings.json, skips leads already `lead_feedback_submitted`). No validate_only, one shot per lead. Response `credit_issuance_decision`: SUCCESS_REACHED_THRESHOLD = credit granted (credit_state → PENDING), FAIL_OVER_THRESHOLD = account hit Google's credit cap, FAIL_NOT_ELIGIBLE = satisfied ratings and also leads <~1 day old (all 11-16 bad leads got it).
- **Credit cap is small and first-come:** only the first 5 bad charged leads (chronological) got credit, the next 16 were FAIL_OVER_THRESHOLD. So rate bad leads continuously (weekly at least) and, in a backlog, submit the charged bad ones FIRST, worst/most-expensive first, then the satisfied ones.
- `lead_feedback_submitted` read-back lags (only 44 of 117 showed True minutes later), trust the API response.
- Rating map used: booked → VERY_SATISFIED/BOOKED_CUSTOMER; real request not booked → SATISFIED/SERVICE_RELATED; commercial, out-of-scope services → JOB_TYPE_MISMATCH; hang-ups, wrong number, job seekers, cancels → OTHER (+comment); vendors → SOLICITATION; repeat of an earlier charged lead (same phone) → DUPLICATE. A request the client declines by its OWN policy (e.g. owner-permission rule) is SERVICE_RELATED, not bad.
