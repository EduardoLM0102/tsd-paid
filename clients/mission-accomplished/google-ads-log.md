# Mission Accomplished — Google Ads Log

**Client:** Mission Accomplished (HVAC — Mohave County tri-state: Lake Havasu City, Bullhead City, Fort Mohave, Mohave Valley AZ · Laughlin NV · Needles/Big River CA · Parker AZ)
**Account:** Mission Accomplished — Customer ID `8634274092` (under MCC Topservdigital `4155514468`)
**Platform:** Google Ads (PPC). A separate LSA account exists (`4904262993`) — out of scope for this log.

> Running log of paid-search work on this account. Newest entry on top. One entry per work session: what we looked at, what we found, what we changed, and what's still open. Meta Ads work lives in `meta-ads-log.md` in this same folder.

---

## ⚡ Quick access (read this first — don't re-discover the account)

- **Customer ID (no hyphens):** `8634274092`
- **MCC / login-customer-id:** `4155514468` (Topservdigital)
- **Skill:** `google-ads-ratos` — scripts at `~/.claude/skills/google-ads-ratos/scripts/`
- **Interpreter on this machine:** `python` (NOT `python3` — that alias isn't installed)
- **CRM / conversion source of truth:** ServiceTitan. Account is **call-driven** (phone leads are the primary KPI).

**Ready-to-run commands** (from `~/.claude/skills/google-ads-ratos/`):
```bash
python scripts/read.py campaigns    --customer-id 8634274092
python scripts/insights.py account  --customer-id 8634274092 --date-range LAST_30_DAYS
python scripts/insights.py campaign --customer-id 8634274092 --date-range LAST_30_DAYS
python scripts/read.py search-terms --customer-id 8634274092        # not campaign-filterable; filter by GAQL
python scripts/read.py quality-scores --customer-id 8634274092
```

**Key campaign IDs (only 2 are live — everything else is paused):**
| Campaign | ID | Channel | Status |
|---|---|---|---|
| TSD_04.07_PMAX_Evergreen_HVAC (the workhorse — ~91% of spend) | `22319188947` | PERFORMANCE_MAX | ENABLED |
| TSD_04.08_Search_Branded_Evergreen_Mix | `23731240233` | SEARCH (branded) | ENABLED |
| Mission Accomplished // All Services // Google Build (PMax) | `—` | PERFORMANCE_MAX | PAUSED |
| ~70 legacy "Levergy \| … \| City" campaigns + newer TSD builds (BOF Search CBO, NonBranded, Display) | — | SEARCH/DISPLAY | PAUSED |

**GAQL gotchas:** `LAST_90_DAYS` is NOT a valid date literal — use `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`. `search_term_view` has no campaign-id flag in the skill script → write a custom query filtered by `campaign.id = <id>`. `segments.conversion_action_name` can't be selected alongside `cost_per_conversion` (PROHIBITED_SEGMENT error) — drop the cost metric.

---

## 2026-10-05 — Weekly 7-day check (Agency Titan tasks): PPC still fully paused

**Read-only, no account changes.** Pulled `8634274092`: no ENABLED campaigns, $0 spend 09-28 → 10-04. Still paused since
07-07 at the client's request (LSA runs in its own account).

**Agency Titan:** two 7-Day Google Search Ads tasks were open (09-28 and 10-05, the 09-28 one never got closed before the
next cycle created a duplicate). Both closed 10-05 with a note. KPI - Google Search entry 10-05: $0 / 0 leads, Account
Health "Unclear", note "N/A - Client's PPC is paused until further notice".

---

## 2026-09-16 — Verified Google PPC status (live pull) + flagged stale contas.yaml note

**Scope:** PPC account (`8634274092`). Read-only, live pull via `google-ads-ratos` (`tsd.sh`). No account changes.

**What we checked:** Daily account spend since the 7/7 pause, and current status of every campaign, to answer "when did Google PPC stop."

**Findings:**
- Daily spend ran normally through 2026-07-07, then drops to exactly $0 and stays at $0 straight through today (2026-09-16) — confirmed via `insights.py daily`, not just the log narrative.
- Current campaign statuses confirm the pause is still total: **every campaign in the account is PAUSED**, including the two `contas.yaml` calls "Live" — `TSD_04.07_PMAX_Evergreen_HVAC` (`22319188947`) and `TSD_04.08_Search_Branded_Evergreen_Mix` (`23731240233`). Both are `PAUSED` with $0 spend, not `ENABLED`.
- **`contas.yaml` is stale** — its note ("Live: PMax Evergreen HVAC + Branded Search; resto pausado") describes a pre-pause or planned state that isn't what's actually live. Should be corrected to reflect the account is 100% paused since 7/7.

**Answer delivered:** Google PPC has been fully stopped since **2026-07-07** (Brian's pause from the review call — see entry below), with zero spend and zero enabled campaigns ever since.

*Reversibility: no account changes made.*

---

## 2026-07-07 → 07-16 — Client escalation (Brian paused spend) + ServiceTitan Marketing Pro thread

**Full write-up: [`servicetitan-marketing-pro-escalation.md`](./servicetitan-marketing-pro-escalation.md)** — read that, not this summary, before touching the account or replying to leadership.

- **7/7 review call** (Mia Kelly, Eduardo, Brian C.) went badly. Brian: "all my PPC calls are spammers." He **paused spend**. His numbers: $28k spent / 36 opportunities since January (~$1,000 per real opportunity).
- **Root cause = configuration, not tracking depth.** ServiceTitan was already sending Booked Job / Completed Jobs / JVP into Google Ads as conversion actions — **none set to Primary**. The only signal live for bidding was *"any unbooked call over 60s, not marked Excused"* → every spam call Brian hung up on trained Smart Bidding to find more. Completed Jobs has been live since December and fed **1** counted conversion in 8 months.
- **Second, separate layer:** Marketing Pro does **not** send hashed identity (Enhanced Conversions). It sends GCLID + revenue via offline upload; call-extension clicks have no GCLID at all and fall back to a phone+timestamp proxy match. Ads Optimizer's "daily customer list" is **Customer Match**, not Enhanced Conversions. Goal depth and identity matching are independent problems.
- Other findings: 99% of clicks land on the homepage (0.69% CVR vs 9–27% on service pages); non-branded leakage ("rv ac repair near me", "auto ac servicing near me"); branded search is the account's best asset (12 conv / 42 clicks / $79 CPA).
- **Client plan drafted, NOT sent:** shift budget to LSA, keep branded-only search, fix conversion config + negatives during the pause window.
- **Leadership escalation open:** Ryan meeting (Friday), Marketing Pro audit checklist, ownership decision, CS playbook, audit of other ServiceTitan clients for the same issue, + add ServiceTitan conversion verification to the 14-day post-launch checklist.

*Reversibility: no account changes made.*

---

## 2026-07-02 — Deep analysis (live data refresh) + priority fix plan → PDF

**Scope:** PPC account (`8634274092`). Read-only, live pull via `google-ads-ratos`. **No account changes.** Second pass over the same day's data, going deeper than the morning audit.

**Deliverables (this folder):**
- `google-ads-deep-analysis.md` — full written analysis (11 sections)
- `mission-accomplished-google-ads-deep-analysis.pdf` — same, formatted (5 pp)

**What the live pull refined vs the morning audit:**
1. **Conversion signal is cleaner than first stated (correction).** The counted `conversions` (bidding signal) is **~74% real ServiceTitan inbound calls** (Website 36 + Extension 34). The junk web micro-events (`phone_link_click` 53.7, Local actions, `buy_air_filter`) land in **all_conversions, NOT in counted `conversions`** — so Smart Bidding is largely optimizing to real calls. The earlier "chases junk" framing was too harsh.
2. **Real inflation = call double/triple-counting**, not junk: same call counted via `Calls from ads` (14) + `ServiceTitan Inbound Call – Extension` (34) + `JVP call-ext` (3); website side ST Inbound Call Website (36) + JVP Website (2). This inflates the 94 and understates true CPA.
3. **Config still needs cleanup:** 29 actions enabled, **23 Primary / 6 Secondary**; the two best signals (ST Inbound Call Website/Extension) are mislabeled **Secondary**; all MANY_PER_CLICK.
4. **New finding — PMax buys heavy competitor-brand queries:** top categories `ambient edge` (5 conv), `air control home services` (4), `ac pro lake havasu` (5), `the weatherman`, `comfort air solutions`, + equipment-brand terms. Good conquesting, no query control.
5. **PMax structure confirmed:** single asset group "Services", Ad Strength EXCELLENT (52 headlines / 45 videos / 31 images), lifetime 388 conv / $18,325. IS 46% — **36.3% lost to rank vs 17.7% to budget** (rank-limited, not budget-limited).
6. Cities confirmed: Lake Havasu City + Fort Mohave (volume), Needles CA (efficient), Mohave Valley + Parker (thin).
7. Branded leak: EXACT `mission accomplished heating and cooling` = **$343 / 0 conv**; all 6 branded conv came from EXACT `mission accomplished` (QS 8).
8. Budget: both live campaigns show **$70/day**, June PMax pace ~**$170/day** — verify in UI.

**Priority fix plan (delivered):** (1) fix conversion config — one source of truth per lead type, dedup call pipes, demote Local/micro-clicks, ONE_PER_CLICK; (2) re-baseline true CPA (likely > $57); *then* (3) restructure PMax into 4 service-line asset groups + audience signals; (4) launch Non-Branded Search PAUSED (~$30–50/day BOF); parallel hygiene: (5) verify $70 vs $170 budget, (6) fix branded leak, (7) archive ~70 dead Levergy campaigns; ongoing (8) seasonality — shift to heating/furnace Sept+, don't panic-cut when summer CPA regresses. **#1→#2 gate all spend/scaling; budget moves need written client approval via AM ticket.**

*Reversibility: no account changes were made this session.*

---

## 2026-07-02 — Full account deep-dive + optimization plan

**Scope:** Whole PPC account (`8634274092`). Read-only audit — **no changes made to the account.** LSA account reviewed separately and excluded per client's request to focus on PPC.

### What we researched
- Account + campaign KPIs (LAST_30_DAYS), monthly trajectory (Apr–Jun), daily trend.
- Conversion-action configuration (primary/secondary, category, counting type).
- Device split, geo/city breakdown, impression-share loss reasons.
- PMax asset-group structure + Ad Strength; branded-campaign keyword list; search terms.

### Performance snapshot (LAST_30_DAYS, PPC)
- **Spend $5,376 · 94 conv · CPA $57 · 3,195 clicks · CTR 2.33% · avg CPC $1.68 · Search IS 46.5%.**
- **PMax Evergreen HVAC** = $4,884 (91% of spend), 88 conv, **CPA $55.50** — the whole account rides this.
- **Branded Search Mix** = $491, 6 conv, CPA $82. Genuinely branded-only (all `mission accomplished *` kw); 98.3% IS, tiny volume → low priority.
- **Trajectory:** Apr 33 conv / CPA $104 → May 37 / $117 → **Jun 100 / $56.** Jump = PMax maturing **+ peak desert-summer AC season** (Lake Havasu/Bullhead 110°F+). Expect CPA to rise as heat fades.
- **Device:** ~94% mobile (correct for a call business). Desktop CPA good but negligible volume.
- **Geo:** 🟢 Needles CA (CPA **$25**), Lake Havasu (CPA $56, volume driver), Fort Mohave/Laughlin OK · 🔴 Mohave Valley (CPA **$138**), Big River/Parker (spend, ~0 conv).

### Key findings
1. **Conversion tracking is polluted — THE top issue.** ~30 conversion actions enabled, ~24 marked **Primary**, and both live campaigns auto-bid → Smart Bidding is optimizing to a dirty blended signal:
   - **Google Business "Local actions" counted as Primary** (Website visits, Directions, Menu views, Other engagements) — those are profile/map taps, **not leads**.
   - **Micro web-clicks set Primary** (`button_click_buy_air_filter`, `phone_link_click`, `book_now_link_click`, page-view actions).
   - **Same phone call counted 3–6×** across `Phone Call`, `Clicks to call`, `click_to_call`, `phone_link_click`, `Calls from ads`, `ServiceTitan Calls`.
   - **Three overlapping systems** un-deduped: native GTM web events + **GoHighLevel** (`ghl_*`) + **ServiceTitan**.
   - **Inconsistent hierarchy:** the two best real signals — *ServiceTitan Inbound Call – Website (36 conv)* and *– Extension (34 conv)* — are marked **Secondary**, while page-views are Primary.
   - All actions are **MANY_PER_CLICK** → repeat callers inflate further.
   - ⇒ The "94 conv / $57 CPA" is inflated & unreliable; bidding chases cheap junk.
2. **PMax is rank-limited, not budget-limited:** loses **36% impr. share to Ad Rank** vs 18% to budget. But Ad Strength is already **EXCELLENT** — the constraint is that there's **only ONE asset group ("Services")** covering all service lines (can't bid up high-value install queries).
3. **Non-branded Search is entirely OFF** — every non-branded Search campaign is paused. PMax is the *only* non-brand engine (a black box with almost no search-term control/negatives).
4. **Budget vs spend mismatch — verify in UI:** both live campaigns show **$70/day**, yet PMax has been spending ~$120–180/day recently. Either budget was just trimmed or a shared-budget quirk. Confirm before any budget move.
5. **Clutter:** ~70 paused legacy Levergy campaigns + stale April TSD builds make the account hard to read (no perf impact — hygiene only).

### What we did
- Nothing on the account (read-only deep-dive). Delivered the prioritized plan below.

### Recommendations — priority order (delivered to Edu)
1. **Fix conversion tracking FIRST (foundational).** Pick ONE source of truth for calls = **ServiceTitan connected call**; make ServiceTitan call + genuine form lead the only **Primary** goals; demote everything else (Local actions, micro-clicks, GHL/native call duplicates) to **Secondary**; switch lead actions to **ONE_PER_CLICK**. *(Not in the script toolkit — UI change.)* Do this before scaling budget.
2. **Restructure PMax by service line** — split the single "Services" asset group into **AC Repair / AC Install & Replace / Heating & Furnace / Maintenance & Tune-up**, each with tailored copy + **search themes** + **audience signals** (upload ServiceTitan customer list, in-market HVAC). Recovers rank-lost impressions cheaper than adding budget.
3. **Launch a controlled Non-Branded Search campaign** (paused for review) on bottom-funnel intent (`ac repair near me`, `emergency ac repair`, `ac not cooling`, `hvac repair <city>`), ~$30–50/day on tCPA against the cleaned goal. Gives query-level control + negatives + diversification off the single PMax.
4. **Rebalance by city:** scale Needles CA ($25) + Lake Havasu; trim Mohave Valley ($138), Big River/Parker.
5. **Hygiene + seasonality:** archive the ~70 dead Levergy/stale builds; as summer fades, pivot messaging to **heating/furnace** (keywords already exist) and don't panic-cut budget when CPA rises.

### Open items / next steps
1. **Conversion-action cleanup (Edu, UI):** produce the exact list of which actions to flip Primary→Secondary as a copy-paste job.
2. **Build the Non-Branded Search campaign PAUSED** (script-side) for review.
3. **Archive dead Levergy/stale campaigns** (script-side, safe) once approved.
4. **Verify the $70/day vs ~$150/day spend discrepancy** directly in the UI.
5. **Re-audit after conversion cleanup** — re-baseline true CPA once Smart Bidding is on a clean signal.

*Reversibility: no account changes were made this session.*

---

## 2026-07-21 — Conversion goal cleanup EXECUTED (campaign-level)

**Account:** 8634274092 · **Changed by:** Edu (via Claude, google-ads-ratos scripts) · **Approval:** Edu, verbally in-session; no AM ticket (Edu: "it's all approved")

### State found (corrects earlier entries in this log and §3.2 of the escalation doc)
- **All 12 campaigns PAUSED.** Brian's pause is total; nothing was spending.
- **ServiceTitan deep actions were ALREADY Primary** — Completed Jobs, Call Extension Completed Job, JVP (Website), JVP (Call Extension). Completed Jobs has **13 conv / $26,790.78 in 2026**, not "1 conversion in 8 months". Cause of the discrepancy unknown; conversion-action edits don't appear in change history.
- 22 conversion actions carried `primary_for_goal = true`, incl. Local actions (Directions, Menu views, Website visits, Other engagements) and click-proxies (phone_link_click = 251 conv YTD, click_to_call, GHL button events).

### Key mechanic learned (important for every ServiceTitan/TSD account)
This account runs Google's **conversion goals** model. **`conversion_action.primary_for_goal` is NOT the lever** — biddability is set by `customer_conversion_goal` / `campaign_conversion_goal` rows, one per (category, origin).
- Mutating `primary_for_goal` on web actions **returns success and silently does nothing**. Verify every write with a read-back; do not trust "mutate accepted".
- Google-hosted actions (Local actions) reject the mutate outright with INVALID_ARGUMENT — but they were **already non-biddable** (`PAGE_VIEW`/`GET_DIRECTIONS`/`CONTACT`/`ENGAGEMENT` + `GOOGLE_HOSTED` all biddable=None), so they never polluted bidding. Earlier "Primary sprawl" read overstated this.
- Junk and legitimate web forms share one row (`DEFAULT / WEBSITE`), so **account-level goals cannot separate them.** Hence the campaign-level approach below.

### What was actually changed
`campaign_conversion_goal` set on the only two campaigns with impressions in LAST_30_DAYS:
- **TSD_04.07_PMAX_Evergreen_HVAC** `22319188947` — 125,055 impr / 2,477 clicks / $1,684.86 / 67.8 conv
- **TSD_04.08_Search_Branded_Evergreen_Mix** `23731240233` — 43 impr / 6 clicks / $36.36 / 6.0 conv

| Goal (category / origin) | Biddable |
|---|---|
| PHONE_CALL_LEAD / WEBSITE · CALL_FROM_ADS | **yes** |
| BOOK_APPOINTMENT / WEBSITE · CALL_FROM_ADS | **yes** (Booked Job, JVP) |
| CONVERTED_LEAD / WEBSITE · CALL_FROM_ADS | **yes** (Completed Jobs) |
| SUBMIT_LEAD_FORM / WEBSITE | **yes** |
| DEFAULT / WEBSITE | **no** |
| OUTBOUND_CLICK / WEBSITE | **no** |
| PURCHASE / WEBSITE | **no** |

**Verified by read-back of `campaign_conversion_goal` on both campaigns.**

### Trade-off accepted
Turning off `DEFAULT / WEBSITE` removes the junk (phone_link_click, book_now/button clicks, GHL click events) **but also** Phone Call, Form Capture, web `form` and `contact_form_submission`, which share that category. Accepted because PHONE_CALL_LEAD carries the real call volume (~36/mo: ST Inbound Call Website 131 + Extension 120 + ST Lead Extension 38 + ST Calls 36 + Calls from ads 36 YTD). To keep those web forms biddable later, they must be **re-categorized** out of DEFAULT.

### Volume reality vs. the 30-in-30 rule (matters for the CS message)
Over ~7 months: Completed Jobs **13** (~2/mo), JVP both **23**, Booked Job both **23**, ServiceTitan inbound calls both **251** (~36/mo). **Mission Accomplished cannot support Completed Jobs as its bidding goal** — by Edu's own rule it's a call-level account. The message sent to Eve covers this ("calls or form fills only on the accounts too small for that"), but Brian may read "Completed Jobs" as applying to him.

### Not done / still open
- The other 10 paused campaigns still inherit account-level goals — set their campaign goals before any relaunch.
- `phone_link_click` still Primary at action level (cosmetic, distorts headline conversion counts; only fixable by re-categorizing).
- Account-level `customer_conversion_goal` untouched — `DEFAULT / WEBSITE` and `OUTBOUND_CLICK / WEBSITE` remain biddable there.
- Nothing was unpaused. No budget touched.

*Reversibility: re-run the same mutate with the biddable flags inverted to restore.*

### CORRECTION + final state (same session, 2026-07-21)

**Two errors in the entry above, both now fixed:**

1. **`protobuf_helpers.field_mask(None, pb)` silently drops fields whose value equals the proto default** — so `biddable = False` was never sent. Only the `True` flips ever applied. The "off" rows reported in the first pass (DEFAULT, OUTBOUND_CLICK, PURCHASE) were **already off at campaign level**; that entry wrongly credited them to this session. **Always use an explicit `field_mask_pb2.FieldMask(paths=[...])` for boolean-to-False writes.**
2. Edu then called out that **PHONE_CALL_LEAD was the core of Brian's complaint** — `Calls from ads`, `ServiceTitan Calls Conversion Action`, `ST Inbound Call - Website/Extension` all fire on a call *occurring*, not on it being worth anything. That is the exact signal that trained bidding toward spam calls. Turned **off**.

**FINAL VERIFIED STATE — both `22319188947` (PMax Evergreen HVAC) and `23731240233` (Search Branded Mix):**

| Goal | Biddable |
|---|---|
| BOOK_APPOINTMENT / WEBSITE · CALL_FROM_ADS | **yes** — Booked Job + JVP |
| CONVERTED_LEAD / WEBSITE · CALL_FROM_ADS | **yes** — Completed Jobs |
| SUBMIT_LEAD_FORM / WEBSITE | **yes** |
| PHONE_CALL_LEAD / WEBSITE · CALL_FROM_ADS | **no** |
| DEFAULT / WEBSITE · OUTBOUND_CLICK / WEBSITE · PURCHASE / WEBSITE | no |
| PAGE_VIEW · GET_DIRECTIONS · CONTACT · ENGAGEMENT (GOOGLE_HOSTED) | no |

**VOLUME RISK — read before relaunch.** Biddable events now run roughly **6–9/month** (Booked Job ~3.3/mo, JVP ~3.3/mo, Completed Jobs ~2.7/mo, forms ~0). That is far under the ~30-in-30 Smart Bidding threshold. The signal is finally *honest*, but it is thin. At relaunch: expect a real learning period, start on Maximize Conversions without a tCPA (or tROAS against JVP value, which carries $ and fires earliest), and do not judge the account on the first weeks. This is also part of why ~80% of budget going to LSA is the right short-term call.
