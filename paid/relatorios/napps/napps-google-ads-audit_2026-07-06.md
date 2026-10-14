# Napps Cooling, Heating & Plumbing — Google Ads Account Audit

**Client:** Napps Cooling, Heating & Plumbing (HVAC + Plumbing, Longview, TX)
**Account:** 950-960-5037 · Currency USD
**Window:** Last 30 days (through 2026-07-05)
**Prepared:** 2026-07-06 · Paid Ads Division (TSD)

---

## 1. Executive summary

Napps spends **~$3,280/mo (~$109/day)** on Google Ads, concentrated almost entirely (82%) in a single Performance Max campaign. On the numbers Google can currently see, the account produces **42 conversions/mo at $78 CPL** — but that number is built on a broken measurement foundation and should not be trusted as the true lead count.

**The single most important issue is conversion tracking.** Only *click-to-call from the ad* is being counted. Website form fills, website phone calls, and the **GHL offline "Form Fill" import (0 conversions in 30 days) are all invisible to Smart Bidding.** Everything else in this audit is secondary to fixing that, because every optimization decision the account makes is currently based on a partial signal.

**Priorities:**
- **P0 — Fix conversion tracking & GHL offline import** (attribution integrity; blocks trustworthy optimization)
- **P1 — Strengthen the PMAX (assets + signal) and add negative-keyword hygiene**
- **P2 — Clean up account structure and fix the nonbranded landing-page/QS problem**

---

## 2. Account KPIs (last 30 days)

| Metric | Value |
|---|---|
| Spend | $3,279.62 |
| Impressions | 25,296 |
| Clicks | 715 |
| CTR | 2.83% |
| Avg CPC | $4.59 |
| Conversions (calls from ads only) | 42 |
| Conversion rate | 5.87% |
| Cost / conversion | $78.09 |
| Search Impression Share | **9.99%** |

Daily spend ranged ~$30–$247. Volume is modest; the account is nowhere near saturating available search demand (sub-10% impression share).

---

## 3. P0 — Conversion tracking is broken

All 42 counted conversions come from a **single** action: `Calls from ads` (AD_CALL, one-per-click, primary). Everything else that represents a real lead is either hidden or not flowing:

| Conversion action | Type | Status | 30d conv |
|---|---|---|---|
| Calls from ads | AD_CALL | ENABLED · primary | **42** |
| GHL Form Fill | Offline upload · Qualified Lead | ENABLED · primary | **0** |
| bct_form_ContactUs / ContactUsToday / Homepage / Sidebar / CouponPopup / MobilePopup | GA4 form | **HIDDEN** | not counted |
| bct_calls_all (website calls) | GA4 | **HIDDEN** | not counted |
| ghl_career_form | GA4 | HIDDEN | not counted (correctly — recruitment) |
| GA4 purchase / page_view | GA4 | HIDDEN | not counted |

**Implications:**
- Smart Bidding on PMAX is optimizing toward phone calls only. It is blind to form submissions and website calls — likely a large share of real leads.
- The **GHL "Form Fill" offline import is enabled and marked primary but recorded 0 conversions in 30 days** → the GHL → Google Ads offline conversion pipeline is not delivering. This is the exact attribution gap our GHL/Verified-Live process exists to catch.
- Reported CPL ($78) is almost certainly **overstated** vs. true blended CPL, because the denominator (leads) is undercounted.

**Actions:**
1. Confirm which web actions are genuine leads (recommend the form-fill set + `bct_calls_all` website calls) and set them **Primary**; dedupe against `Calls from ads` to avoid double-counting the same call.
2. **Repair the GHL → Google offline import** (Form Fill / Qualified Lead). Do a joint test with Mo and require **Verified Live** before we report any of this to the client.
3. Demote page_view / purchase to Secondary (not lead events).
4. Re-baseline all KPIs only after tracking is validated. Do not change bidding strategy until the signal is trustworthy.

---

## 4. P1 — Performance Max (82% of spend)

`TSD_02.20_PMAX_Plumbing_CoreServices` — ENABLED · $100/day budget · $2,677 spend · 37 conv · **$72 CPL**

- Drives **82% of spend and 88% of conversions** — this campaign *is* the account.
- **Single asset group ("Asset Group 1"), Ad Strength = UNKNOWN** → assets are thin (likely missing images/video and/or full text). Weak asset coverage caps reach and quality.
- **Losing ~85% of search impression share to Ad Rank** (only ~13% lost to budget) → the ceiling here is relevance/assets/signal, not money. Raising budget alone will not fix it.

**Actions:**
- Rebuild the asset group to full strength: 15 headlines, 5 descriptions, full image set (1200×1200, 1200×628, 1200×1200 logo), 1+ video, sitelinks/callouts/structured snippets. Target Ad Strength ≥ Good.
- Add **audience signals** (customer list from GHL, high-intent search themes) — especially important once web/GHL conversions feed bidding.
- Add PMAX **brand exclusions** so it doesn't absorb branded traffic that Search should own.
- Split plumbing vs. HVAC into separate asset groups (or campaigns) so creative and search themes match intent.

---

## 5. P1 — Negative keywords & search-term hygiene

**There are zero negative keywords on any active campaign.** The only negatives in the account are an employment-exclusion list attached to a *paused* branded campaign. No account-level negative list is applied.

Waste already visible in search terms:
- `cheap ac repair near me` — low-value "cheap" intent
- `etr tyler`, `lagrone ac carthage tx` — competitor / navigational
- Nonbranded HVAC terms converting at **$20–$38 CPC**

**Actions:**
- Build and apply an **account-level negative list** for home-services: `job/jobs/career/hiring/salary`, `DIY/how to/diagram/manual`, `parts/capacitor/filter` (unless selling), `free/cheap`, `rental/warranty/recall`, competitor brand names.
- Add brand terms as negatives to nonbranded campaigns (and vice-versa) to keep branded/nonbranded clean.
- Set a **weekly search-term review** SOP for this account.

---

## 6. P2 — Account structure cleanup

18 campaigns exist; only **3 are meaningfully serving** (PMAX Plumbing, Branded, and the just-launched Nonbranded Plumbing search). ~14 are paused legacy shells:
- `BC - CG-Branded / Plumbing / HVAC` (old agency build)
- `Search_AC_Maintenance`, `Search_HVAC_Repair`, `Search_Emergency AC Repair`, `Search_Plumbing`, `Search_Drain Cleaning`, `Search_Plumbing_GEO`, `Search_Emergency_Plumbing`
- Abandoned launches: `TSD_04.07_PMAX_Evergreen_HVAC_Emergency`, `TSD_04.07_Search_Nonbranded_Evergreen`, `TSD_04.05_PMAX_Emergency`, `TSD_06.05_Leads_Search_Nonbranded_Plumbing`

**Actions:** archive/remove dead campaigns to clean reporting; migrate any useful keyword/negative learnings from the old `Search_*` builds before removing. Standardize on the `TSD_MM.DD_...` naming convention.

---

## 7. P2 — Nonbranded search: landing page & Quality Score

- Paused `TSD_06.05_Search_Nonbranded_HVAC`: **$246 CPL**, CPCs $20–$38 — correctly paused.
- Only keyword with QS data — "air conditioning repair" — scored **QS 3**: Landing Page *Below Average*, Predicted CTR *Below Average*, Ad Relevance Above Average.
- New `Leads_Search_Nonbranded_Plumbing` (ENABLED) is Ad Strength AVERAGE and losing 77% IS to rank — same landing-page/QS risk if launched against the current pages.

**Actions:** before scaling nonbranded search, ship dedicated service landing pages (service + location + click-to-call above the fold, fast mobile load, trust signals). Nonbranded search will keep burning at $20+ CPCs until post-click quality improves.

---

## 8. Branded search (minor)

`TSD_03.22_Search_Branded_Evergreen` — EXCELLENT ad strength, 92% IS, $37 CPL. Healthy, but **$10 CPC on the brand's own name** suggests competitor conquesting.

**Actions:** keep defending brand; monitor auction insights for conquesters. Fix headline typo "Napp AC" → "Napps AC".

---

## 9. Prioritized action plan

| # | Priority | Action | Owner | Gate |
|---|---|---|---|---|
| 1 | P0 | Set true lead actions Primary; dedupe calls | Paid | — |
| 2 | P0 | Repair GHL → Google offline import (Form Fill) | Paid + Mo | **Verified Live** before client comms |
| 3 | P0 | Re-baseline KPIs after tracking validated | Paid | after #1–2 |
| 4 | P1 | Rebuild PMAX asset group to full strength + audience signals + brand exclusion | Paid + Creative | — |
| 5 | P1 | Account-level negative list + weekly search-term SOP | Paid | — |
| 6 | P2 | Archive ~14 dead campaigns; standardize naming | Paid | — |
| 7 | P2 | Dedicated nonbranded landing pages before scaling search | Paid + Web | budget change = written client approval via AM ticket |

**Note:** any budget shift (e.g., funding a rebuilt nonbranded search push) requires written client approval via the AM ticket before execution.

---

*Data pulled live from Google Ads API (customer 950-960-5037), 30-day window through 2026-07-05. All conversion figures reflect the account's current (incomplete) tracking configuration and should be treated as provisional until P0 is resolved.*
