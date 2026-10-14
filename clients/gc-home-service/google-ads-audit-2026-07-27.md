# GC Home Service — Google Ads Audit

**Account:** `2375064049` (under Topservdigital MCC). **Pulled:** 2026-07-27, newest complete day 2026-07-26.
**INTERNAL ONLY** — honest root cause. Client-facing framing later per `topserv-client-report-format`.
Timezone caveat: account runs on `Africa/Kampala`, so "days" are shifted ~7h.

---

## Headline (last 30 days)

| Metric | Value |
|---|---|
| Spend | **$3,752** |
| Conversions | **15** (100% phone-call *clicks*) |
| Cost / conv | **$250** |
| Search impression share | **13%** (losing ~87% of the market) |
| **Last 7 days** | **$1,330 spend → 1 conversion** |

Live campaigns: only **2** of 12 — `TSD_PMAX_Calls` and `TSD_Leads_Search_Branded_08.06`.
`Cooling` and `Competitorattack` were re-enabled around Jul 16 and are **paused again** now.

---

## The 3 things that actually matter

### 1. The Jul 16 PMax budget 3x is bleeding — reverse it. (Highest priority)
`TSD_PMAX_Calls` was raised $50 → $155/day on Jul 16 while its CPL was already ~$293. Since the bump:

| Window | PMax spend | Conv |
|---|---|---|
| Jul 18–26 | ~$963 | 1 |
| Account, last 7d | $1,330 | 1 |

PMax is now **59% of all account spend** and buying almost nothing. The extra budget bought impressions, not customers (Jul 20 alone: $310 spend, 0 conv). **Recommendation: pull PMax back to ~$50–60/day immediately** until it proves conversions again. This is the single biggest live bleed.

### 2. We're optimizing to phone-call *clicks*, not booked jobs.
All 15 conversions are `Calls from ads` (call-extension clicks) + `[TSD] Website Call Link` (a `tel:` click on the site). **Zero form leads, zero offline/CRM import.** So Maximize Conversions is steering bids toward *someone tapping a call button* — not a qualified, booked job. That makes the $250 CPL a vanity number and starves PMax's algorithm of a real signal (part of why it can't optimize). Same tracking-integrity gap we hit on Golden and Proud Pops.
**Recommendation:** import booked-job / qualified-lead conversions from their intake system (offline conversion import or GA4 + call tracking with a "qualified" status). Fix this *before* scaling anything.

### 3. PMax is losing 89% of impressions — mostly to Ad Rank, and it's the wrong vehicle here.
PMax impression-share breakdown: **11% IS, 56% lost to Ad Rank, 33% lost to budget.** The 56% rank loss = weak quality (landing page + asset relevance), not money. For a ~$150/day *local* HVAC account, PMax also gives up query control — it's already the channel that's hardest to keep clean (can't add normal negative keywords). Branded Search, by contrast, runs at **87% IS and $84 CPL**.
**Recommendation:** shift weight from PMax toward tightly-matched Search (exact/phrase) + the branded campaign, and treat PMax as a small controlled test, not the main engine. Fix landing-page/asset quality to recover rank-lost share instead of throwing budget at it.

---

## Secondary findings

- **Competitor conquesting was pure waste (now paused — keep it off).** `Competitorattack` spent ~$350 for 9 clicks / **0 conv**; broad `Cooling` pulled rival brands and junk (`arlinghaus` $132/0-conv, `apollo home`, `logan heating`, `five star`, `lennox`, "how much does it cost to get ac fixed") for ~1 conversion on $853. Conquesting only works with its own tight structure + a steal-the-customer landing page, not the generic site.
- **Brand defense is defensible but pricey.** The branded campaign spent ~$295 of its $335 on our own name (`gc home service/services/hvac`) at $8+/click (one $155 single-click artifact). Competitors *do* bid on us (arlinghaus/apollo show up), so a lean branded campaign is worth keeping — but check brand-term Quality Score; paying $8/click on your own name usually means landing-page relevance or bid caps are off.
- **Account hygiene:** 12 campaigns, 10 dead — archive them. The `Africa/Kampala` timezone shifts every reporting day and resets the budget mid-afternoon local; decide whether it's worth a Google-support fix (it wipes historical stats).
- **Nonbrand impression share ~11% = huge headroom** — but do NOT scale into it until #2 (real conversions) and the quality/rank issue are fixed. Scaling a leaky funnel just spends faster.

---

## Priority order

1. **Cut PMax budget** $155 → ~$55/day (stops the bleed today; needs the client-budget-change ticket per doctrine).
2. **Instrument real conversions** (booked-job import). Everything else is guesswork until this exists.
3. **Rebalance toward Search**, fix PMax landing-page/asset quality to recover rank-lost share.
4. Keep conquesting paused; archive the 10 dead campaigns.
5. Audit brand-term Quality Score; keep brand defense lean.
