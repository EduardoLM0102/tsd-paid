# Zen Air — Google Ads findings (internal)

**Date:** 2026-07-09 · **Analyst:** Edu (Head of Paid Ads)
**Accounts:** PPC 436-084-0956 (4360840956) · LSA 374-050-2923 (3740502923)
**Source:** Google Ads API, pulled 2026-07-09. Period Jun 1–15, 2026 unless stated.
**Trigger:** CSR asked for more context on the location findings in Andrea's Jun 1–15 summary, to share with Eddie.

---

## 0. STOP — the account has not served since June 13

This outranks everything in the ticket.

- Last impression in the PPC account: **2026-06-12**, across *every* campaign simultaneously.
- **Zero impressions, zero spend, June 13 → July 8 (26 days).**
- The entire "$7,669 for Jun 1–15" was spent in 12 days (Jun 1–12) → real pace was **$639/day**, not $511/day.
- Not an API artifact: All Heart and Mission Accomplished both return data through Jul 7–8 on the same credentials.
- Not a campaign-level cause: `TSD_05.13_Search_Branded_Evergreen` is `primary_status = ELIGIBLE`, its ad is `APPROVED/REVIEWED`; `TSD_03.23_PMAX_HVAC_Calls` is `SERVING` with an `ELIGIBLE` asset group. Budgets are funded ($150 + $100/day).
- Not the Emergency PMax pause: Andrea paused that on **Jun 16**, three days *after* serving stopped.
- `customer.status = ENABLED`, both `billing_setup`s `APPROVED`, `account_budget` spending limit `INFINITE`. The API exposes no payment-hold flag, so the cause must be confirmed in the UI.

**Most likely:** a payment-method failure / billing hold on the PPC account. LSA (separate billing) kept spending — $124.80 on Jul 1, $471.92 on Jul 2, $169.68 on Jul 3 — which is consistent with a PPC-account-specific payment issue.

**Actions:** check Billing → Summary and account notifications in the PPC account. Escalate to Ryan + AM before any narrative goes to Eddie. Andrea's Jul 1 budget increases ($60→$100, $110→$150) went into a dark account.

---

## 1. The location answer the CSR asked for

**The city CPL ranking is not a geography signal. It is a network-mix artifact.**

Both PMax campaigns spent almost all their money on **YouTube**, not Search:

| Campaign | Spend | YouTube share | YouTube CPC | Search CPC |
|---|---|---|---|---|
| TSD_03.23_PMAX_HVAC_Calls | $2,553.08 | **98.8%** | $0.21 | — |
| TSD_PMAX_HVAC_Heating_Emergency_TX | $2,485.05 | **89.0%** | $0.37 | $7.43 |
| TSD_05.13_Search_Branded_Evergreen | $2,610.98 | 0% (Search) | — | $30.01 |

PMax bought **18,000+ YouTube clicks at ~$0.25**. Search clicks cost $17–$82. So a city's CPL is essentially determined by *what fraction of its spend landed on cheap YouTube inventory*:

| City | Spend | CPL | % of conversions from YouTube | Search $ | Search conv |
|---|---|---|---|---|---|
| Doraville | $273.50 | $11.89 | 96% | $110.97 | 1 |
| Snellville | $205.66 | $11.43 | 94% | $70.22 | 0 |
| Sandy Springs | $269.47 | $12.84 | 100% | $95.83 | 0 |
| Lilburn | $453.55 | $16.20 | 100% | $72.39 | 0 |
| Lawrenceville | $1,183.56 | $16.91 | 94% | $314.03 | 3 |
| Cumming | $702.79 | $39.05 | 100% | $446.68 | **0** |
| Duluth | $355.81 | $44.48 | 75% | $249.73 | 2 |
| Brookhaven | $254.11 | $254.11 | **0%** | $246.09 | 1 |

Read the last two columns. **Brookhaven's "$254 CPL" is 44 Search clicks and one conversion** — it never received meaningful YouTube delivery. It is a sample-size artifact, not a bad market. **Cumming, the "weak" city, spent $446.68 on Search for zero conversions** — that is the genuinely bad number, and it is invisible in the blended CPL.

So: the "efficient" cities are where YouTube delivered; the "weak" cities are where Search delivered. Nothing in this data says Doraville homeowners are better customers than Duluth homeowners.

### What the geo data *does* legitimately show
**97.8% of spend went to people physically in the service area** (`LOCATION_OF_PRESENCE` $7,438.54 vs `AREA_OF_INTEREST` $167.09). The radius targeting is not leaking to out-of-area searchers. That is a real, defensible win.

---

## 2. Corrections to the Jun 1–15 summary before anything reaches Eddie

**a) "Branded Search defends the brand name" — 79% of it is not branded.**

Keyword spend in `TSD_05.13_Search_Branded_Evergreen`:

| Keyword | Match | Spend | Clicks |
|---|---|---|---|
| hvac contractors near me | **BROAD** | $1,705.88 | 58 |
| local hvac repair company | **BROAD** | $359.95 | 8 |
| zen air heating and cooling | EXACT | $404.24 | 12 |
| zen air / zen air hvac / callzenair | EXACT | ~$161 | 11 |

Two broad-match generic keywords = **$2,065.83 of $2,610.98 (79%)**. Actual Zen Air brand terms ≈ $565 (22%).

Consequence: the campaign paid ~$685 for **competitor brand searches** — shumate mechanical ($119.07), shumate heating and air ($89.39), estes heating and air ($88.03), rs andrews phone number ($63.80), capital city hvac ($53.24), bardi hvac ($48.06), anytime heating and cooling ($43.75), bardi heating and air ($42.80), pv heating and air ($42.58), spencer ($34.13), casteel ($33.43), total heating and air ($26.55). Plus $121.08 on "blower door testing near me", a service Zen Air doesn't sell.

The $30.01 CPC and 3.0% CTR confirm it: real branded campaigns run $2–5 CPC and 40–70% CTR. **Do not tell Eddie this campaign is protecting his brand.** Fix: strip the broad keywords into a separate non-brand campaign, add competitor names as negatives (or bid them deliberately), rename.

**b) "Outlier cities are monitored/excluded" — nothing is excluded.**
There are **zero negative location criteria** in the account. Active geo targeting is `PMax: 15-mile proximity` and `Branded: 5 × 7-mile proximity + one location group`. Duluth appears as a *targeted* city only in the two legacy campaigns, both `primary_status = ENDED` with $0 spend. Saying "excluded" to Eddie is a factual claim we cannot support.

**c) Marietta/Monroe was never a live problem.**
May 2026: Marietta $4.38 (6 clicks), Monroe $0.00. June 1–15: $2.43 and $0.85. There is no month where these cities absorbed real budget. Andrea's instinct to not claim "June data revealed the issue" is right, and the May pull confirms it. Do not raise Marietta/Monroe with Eddie at all — it invites a question we'd answer with "nothing happened."

**d) "324 form submits" is one unvalidated tag.**
97% of all 403.9 conversions (392.9) come from a single action: **`Submit lead form - web`** (type `WEBPAGE`, `ONE_PER_CLICK`). 320.2 of those came from **YouTube clicks** — a 2.67% form-fill rate from YouTube video traffic for an HVAC company. Implausible.

Also note `TSD_03.23_PMAX_HVAC_Calls` generated **zero calls**. All 10 call conversions in the account came from Branded Search (7) and the Emergency PMax (3).

---

## 3. Lead quality and spam — what we can and cannot say

**Spam: actively filtered, and real.** ClickCease is installed (`adwords%clickcease.com@gtempaccount.com`) and wrote **16+ IP-block criteria between Jun 11–12** across the Branded Evergreen campaign and two legacy campaigns. Invalid-click filtering is running on Search. Its last write is Jun 12, matching the blackout.

**Lead quality: Google Ads cannot answer this today.** The account already has the right tags —

- `LP | Qualified Lead` (`SUBMIT_LEAD_FORM`)
- `LP | Disqualified Lead (Out of Area)` (`SUBMIT_LEAD_FORM`)

— both `ENABLED`, both `include_in_conversions_metric = false`, and **both with zero recorded conversions Jun 1 – Jul 9**. They are not firing. Until they do, no per-city lead-quality or out-of-area claim is defensible from Google Ads. Route to GHL/CRM for the real count.

**Tracking hygiene, primed to pollute:** these GA4 events are set to count in `conversions` —
`ghl_city_page`, `ghl_service_area`, `ghl_contact_us`, `ghl_rating_form`, `ghl_schedule_services`, `ghl_request_estimate`, `book_now_link_click`. Two of them (`ghl_service_area`, `book_now_link_click`) are miscategorized as **PURCHASE**. Several are `MANY_PER_CLICK`. They didn't fire in this window, but they will.

---

## 4. Recommended sequence

1. **Today:** diagnose the June 13 serving stop (Billing → Summary, account notifications). Escalate to Ryan + AM. Nothing else matters until ads run.
2. Pull actual Zen Air lead count from GHL for Jun 1–12 and reconcile against 392.9. That single number decides whether the PMax story is a win or a tracking failure.
3. Fix `Submit lead form - web`; get `LP | Qualified Lead` / `LP | Disqualified Lead` firing and marked primary. Demote the GA4 GHL micro-events out of `conversions`.
4. Split the broad keywords out of `TSD_05.13_Search_Branded_Evergreen`; add competitor negatives; rename to reflect reality.
5. Force PMax off pure-YouTube delivery (or accept it as awareness and stop calling it a lead engine).
6. Only then re-open the geo conversation, using Search-only data, which is the only place city-level intent is measurable.

## 5. What to send back to the CSR

See `2026-07-09-csr-reply.md`.
