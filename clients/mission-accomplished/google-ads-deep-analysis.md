# Mission Accomplished — Google Ads Deep Analysis

**Prepared:** 2026-07-02 · **Analyst:** Edu (Head of Paid Ads, TSD)
**Account:** Mission Accomplished — Customer ID `8634274092` (MCC Topservdigital `4155514468`)
**Scope:** PPC only. Read-only — **no changes were made to the account.** LSA account (`4904262993`) excluded per client focus.
**Data window:** Last 30 days unless noted. Pulled live via `google-ads-ratos` scripts.

---

## 1. Executive summary

Mission Accomplished is a **call-driven HVAC business** in the Mohave County tri-state area (Lake Havasu City, Fort Mohave, Mohave Valley, Parker AZ · Needles CA). The account runs on essentially **one engine**: a single Performance Max campaign that carries ~91% of spend. It is performing well right now — but that performance is riding **peak desert-summer AC demand**, a **single unstructured asset group**, and a **conversion-tracking setup that is messy on paper**, even if the live bidding signal is cleaner than it first looks.

| KPI (last 30d) | Value |
|---|---|
| Spend | **$5,376** |
| Conversions (counted) | **94** |
| CPA | **$57** |
| Clicks | 3,195 · CTR 2.33% · avg CPC $1.68 |
| Search impression share | 46.5% |

**Bottom line:** the account is healthy on the surface but **fragile** — one campaign, one asset group, one season, and a conversion config that needs cleanup before we scale budget. The upside (structure + non-branded expansion) is real and largely untapped.

---

## 2. Where the money goes

| Campaign | Type | Status | Spend | Conv | CPA | Search IS |
|---|---|---|---|---|---|---|
| **TSD_04.07_PMAX_Evergreen_HVAC** | PMax | ENABLED | $4,884 (90.8%) | 88 | **$55.50** | 46.0% |
| TSD_04.08_Search_Branded_Evergreen_Mix | Search (branded) | ENABLED | $491 | 6 | $81.90 | 98.3% |
| ~70 legacy "Levergy \| … \| City" + stale TSD builds | Search/Display/PMax | PAUSED | — | — | — | — |

Only **two campaigns are live**. Everything else is paused clutter. The whole account effectively *is* the PMax campaign.

---

## 3. Trajectory — the season is doing a lot of the work

Account-level, calendar months (both live campaigns):

| Month | Conv | Spend | CPA |
|---|---|---|---|
| April | 33 | $3,450 | **$104** |
| May | 37 | $4,344 | **$117** |
| June | 100 | $5,591 | **$56** |

CPA **halved** from May to June while conversions nearly tripled. That is not a single optimization win — it is **PMax maturing + peak AC season** in a 110°F+ desert market. PMax lifetime is **388 conversions / $18,325 spend**.

> ⚠️ **Plan for regression.** As summer heat fades (Sept onward), demand and CPA will normalize back toward the $80–110 range. Do **not** panic-cut budget when that happens, and start shifting messaging to **heating/furnace** ahead of the shoulder season.

---

## 4. Conversion tracking — refined finding (important correction)

The prior pass flagged tracking as "polluted, bidding chases cheap junk." The live data **refines that**: the config *is* a mess, but the **bidding-counted signal is actually call-dominated and mostly real.**

**Config reality:** 29 enabled conversion actions — **23 marked Primary, 6 Secondary.**

**What actually counts into `conversions` (the bidding signal), last 30d:**

| Action | Counted conv | Real lead? |
|---|---|---|
| ServiceTitan Inbound Call – Website | 36.0 | ✅ real call |
| ServiceTitan Inbound Call – Extension | 34.0 | ✅ real call |
| Calls from ads (PMax + Branded) | 14.0 | ⚠️ likely duplicates the ext calls |
| ServiceTitan Calls Conversion Action | 3.0 | ⚠️ duplicate pipe |
| ServiceTitan JVP (Call Extension) | 3.0 | ⚠️ duplicate pipe |
| ServiceTitan JVP (Website) | 2.0 | ⚠️ duplicate pipe |
| book_now_link_click | 2.0 | 🟡 micro-action |
| **Total** | **~94** | |

**Two things this tells us:**

1. **The good news:** ~74% of counted conversions are ServiceTitan inbound calls (Website 36 + Extension 34). The junk web micro-events — `phone_link_click` (53.7 in *all-conversions*), Local actions (Directions/Menu/Website visits), `button_click_buy_air_filter` — are landing in **all_conversions, NOT in the counted `conversions`**. So Smart Bidding today is largely optimizing to **actual phone leads.** The earlier "chases junk" framing was too harsh.

2. **The real problem is double-counting, not junk.** The same phone call is very likely counted **2–3×** through parallel pipes: `Calls from ads` (14) + `ServiceTitan Inbound Call – Extension` (34) + `ServiceTitan JVP (Call Extension)` (3) plausibly all fire on the same call-extension calls. Website side: `ServiceTitan Inbound Call – Website` (36) + `ServiceTitan JVP (Website)` (2). **This inflates the 94 and understates true CPA.**

**Config hygiene risk (still worth fixing):**
- **Inverted labeling:** the two best, cleanest signals — *ServiceTitan Inbound Call – Website / – Extension* — are marked **Secondary**, while Google Business "Local actions" (map taps, direction clicks) and GA4 micro-clicks sit as **Primary**. It works today only by luck of which actions fire; it's fragile.
- **Three overlapping systems** un-deduped: native GA4/GTM web events + **GoHighLevel** (`ghl_*`) + **ServiceTitan**.
- Every action is **MANY_PER_CLICK** → repeat callers inflate further.

**Recommendation:** pick **one** source of truth per lead type — **ServiceTitan connected call** for calls, **ServiceTitan booked job / genuine form** for web — mark *those* Primary, demote everything else (Local actions, GA4 micro-clicks, duplicate call pipes) to Secondary, and switch lead actions to **ONE_PER_CLICK**. This is a UI change (not in the script toolkit). Do it **before** scaling budget so we re-baseline a clean, de-duplicated CPA.

---

## 5. PMax — the single-asset-group ceiling

- **One asset group ("Services")**, status ENABLED, **Ad Strength EXCELLENT** (52 headlines, 15 long headlines, 14 descriptions, 45 YouTube videos, 31 images, logos, business name). Creative is not the constraint.
- **Impression share is rank-limited, not budget-limited:** loses **36.3% to Ad Rank** vs **17.7% to budget** (IS 46.0%). More budget alone won't fix rank loss.
- **PMax is buying heavy competitor-brand and generic queries** (new finding). Top search categories: `ambient edge` (5 conv), `air control home services` (4), `ac pro lake havasu` (5), `comfort air solutions`, `tri state air conditioning`, `the weatherman lake havasu`, plus equipment-brand terms (`carrier dealer`, `trane heat pump`, `bryant ac installers`). Good conquesting — but a black box with almost no query-level control or negatives.

**Recommendation:** split "Services" into service-line asset groups — **AC Repair / AC Install & Replace / Heating & Furnace / Maintenance** — each with tailored copy, **search themes**, and **audience signals** (upload ServiceTitan customer list + in-market HVAC). This lets us bid up high-value install queries and recover rank-lost impressions more cheaply than raising budget.

---

## 6. Non-branded Search is entirely OFF

Every non-branded Search campaign is paused. **PMax is the only non-brand engine** — meaning no query-level control, no negative-keyword hygiene, no diversification. This is the single biggest structural gap.

**Recommendation:** launch a **controlled Non-Branded Search campaign (built PAUSED for review)** on bottom-funnel intent — `ac repair near me`, `emergency ac repair`, `ac not cooling`, `hvac repair <city>` — at ~$30–50/day on tCPA against the cleaned goal. Gives us search-term control, negatives, and a second engine that isn't a black box.

---

## 7. Branded Search — small, mostly fine, one leak

Genuinely branded-only (all `mission accomplished *` keywords), 98.3% IS, tiny volume. One leak: the **EXACT `mission accomplished heating and cooling`** spent **$343 with 0 conversions**, while **EXACT `mission accomplished`** drove all 6 conversions for ~$56 total (QS 8). Low priority, but that one keyword is burning budget with no return — worth a look.

---

## 8. Geography

Confirmed live cities (PMax): **Lake Havasu City** (volume driver) and **Fort Mohave** carry most conversions; **Needles CA** is efficient; **Mohave Valley** and **Parker** show spend with thin conversion. Directional — a clean city-level CPA read requires the de-duplicated conversion signal from §4 first.

---

## 9. Budget discrepancy — verify in UI

Both live campaigns show a **$70/day** budget, yet June PMax spend (~$5,110 / 30) implies **~$170/day**. Either a shared budget, a recent trim, or a reporting quirk. **Confirm directly in the UI before any budget move** — don't act on the $70 figure.

---

## 10. Prioritized action plan

| # | Action | Owner | Type | Why first |
|---|---|---|---|---|
| 1 | **Fix conversion config** — one source of truth per lead type, dedup call pipes, demote Local actions/micro-clicks, set lead actions ONE_PER_CLICK | Edu (UI) | Foundational | Everything downstream depends on a clean, de-duplicated CPA |
| 2 | **Re-baseline true CPA** after cleanup | Edu | Measurement | Current $57 is inflated by double-counted calls |
| 3 | **Restructure PMax** into 4 service-line asset groups + audience signals | Edu (build) | Growth | Recovers 36% rank-lost IS cheaper than budget |
| 4 | **Launch Non-Branded Search (PAUSED)** on BOF intent, ~$30–50/day | Edu (build) | Growth + control | Only non-brand engine today is the PMax black box |
| 5 | **Verify $70 vs ~$170/day** budget in UI | Edu | Hygiene | Don't move budget on a wrong number |
| 6 | **Fix branded leak** — the $343/0-conv exact keyword | Edu | Hygiene | Pure waste |
| 7 | **Archive ~70 dead Levergy/stale campaigns** | Edu (script) | Hygiene | Readability; no perf impact |
| 8 | **Seasonality plan** — shift to heating/furnace messaging Sept+, don't panic-cut on CPA rise | Edu | Strategic | Summer CPA will not hold |

**Sequence:** #1 → #2 gate everything. Do not scale budget (#3/#4 spend) until the conversion signal is clean and re-baselined.

---

## 11. Open questions for the client / AM
1. Confirm **ServiceTitan connected call** as the single call source of truth (vs GHL vs native).
2. Confirm the **$70/day** budget figure and whether it's shared.
3. Approve archiving the paused Levergy legacy campaigns.
4. Written budget approval before any scale (per TSD paid rule — never execute first).

*Reversibility: no account changes were made in this analysis. All recommendations are proposals pending approval.*
