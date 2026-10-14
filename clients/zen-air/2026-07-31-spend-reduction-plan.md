# Zen Air — spend reduction plan (internal)

**Date:** 2026-07-31 · **Analyst:** Edu (Head of Paid Ads)
**Accounts:** Google PPC 4360840956 · Google LSA 3740502923 · Meta 381256660973192 ("Zen Air - Third Ad account")
**Window:** last 30 days (2026-07-01 → 2026-07-30). PPC only served **21 of those days** (resumed 2026-07-10 after the June billing stop).
**Trigger:** ticket — client wants to cut spend, feels he is paying too much for the results.

---

## 1. Where the money actually goes

| Channel | Spend (30d) | Leads | CPL | Status now |
|---|---|---|---|---|
| Google PPC — Search Branded Evergreen | $4,551.22 | 14 | $325.09 | ENABLED, $150/day |
| Google PPC — PMax HVAC Calls | $2,478.62 | **1** | **$2,478.62** | ENABLED, $100/day |
| Google LSA | $766.40 | 10 | $76.64 | **PAUSED — dark since Jul 3** |
| Meta | $2,804.32 | 297 | $9.44 | only $20/day awareness live |
| **Total** | **$10,600.56** | | | |

PPC run rate over its 21 serving days = **$334.75/day (~$10,000/mo)** for ~21 leads/month → **~$480 per lead**.
That is the number behind Eddie's complaint. It is concentrated in two places.

---

## 2. Cut #1 — PMax is buying video views, not customers

Network split, PMax, last 30 days:

| Network | Spend | Clicks | Conversions |
|---|---|---|---|
| YouTube | $1,071.22 | 3,519 | **0** |
| Content (Display) | $439.79 | 996 | **0** |
| Discover | $165.21 | 132 | **0** |
| Search Partners | $137.58 | 26 | **0** |
| Search | $664.82 | 30 | 1 |

**$1,813.80 (73%) bought 4,673 clicks and zero conversions of any kind.** Not a tracking artifact — the "Calls from ads" tag fired 10 times account-wide in the same window, it works.

The only converting slice is Search, at $664.82 for 1 lead. Nothing here justifies $100/day.

**Action: pause `TSD_03.23_PMAX_HVAC_Calls` (22959264938).** Saves ~$3,540/mo. Costs 1 lead/month.

---

## 3. Cut #2 — the Search campaign is paying for competitors' names

Keyword spend, last 30 days ($4,551.22 total):

| Keyword | Match | Spend | Clicks | Conv | CPL |
|---|---|---|---|---|---|
| hvac contractors near me | **BROAD** | $3,425.62 | 106 | 6 | $570.94 |
| emergency heating service ga | **BROAD** | $507.91 | 12 | 2 | $253.96 |
| zen air heating and cooling | EXACT | $455.14 | 20 | 6 | **$75.86** |
| all other brand terms | EXACT/PHRASE | $162.55 | 13 | 0 | — |

`hvac contractors near me` is 75% of the campaign at $32.32 per click.

Where those clicks went — competitor brand and off-service search terms, last 30 days:

allgood heating and air $322.36 · shumate heating and air $219.32 · reliable heating and air $165.24 · b mays $122.61 · shumate mechanical $97.39 · allgood hvac $86.17 · acs covington ga $83.51 · seasons comfort hvac $83.29 · casteel (3 variants) $201.05 · andrews heating and air $75.82 · cool air / coolair mechanical $138.91 · estes (2 variants) $128.09 · rs andrews (3 variants) $97.56 · coolray (3 variants) $115.61 · four/4 seasons (3 variants) $70.15 · bardi heating and air $36.89 · stuart mechanical $35.59 · brhvac $20.51 · ful bro engineering $40.45

**≈ $2,140 (47% of the campaign) on competitors' brand names, returning 2 conversions.** Plus off-service junk: ahri certified air conditioner $141.82, thumbtack hvac $52.22, daikin technical support number $24.96, fresh air ducts cleaning $22.90.

**Action:**
1. Add competitor brand negatives (list above) at campaign level.
2. Drop `hvac contractors near me` from BROAD to PHRASE, or move it to its own non-brand campaign with a capped budget so it can't eat the brand budget.
3. Leave `zen air heating and cooling` EXACT alone — $75.86/lead is the best line in the Google account.

Saves ~$3,050/mo, keeps ~12 of the 15 conversions.

---

## 4. Do NOT cut — LSA

LSA is the cheapest real intent Zen Air has on Google, and it is already off.

| Month | Spend | Leads | CPL |
|---|---|---|---|
| Jan | $184.08 | 3 | $61.36 |
| Feb | $124.80 | 2 | $62.40 |
| Mar | $244.80 | 4 | $61.20 |
| Apr | $228.63 | 4 | $57.16 |
| May | $62.40 | 1 | $62.40 |
| Jun | $249.60 | 4 | $62.40 |
| Jul | $766.40 | 10 | $76.64 |

**Last spend 2026-07-03; campaign 20752144554 is PAUSED.** YTD it has cost $1,860 total. It is not the spend problem — it is the channel we should be feeding with what PMax gives back.

### Who paused it — the client did

Pulled from `change_event` on LSA account 3740502923, 2026-07-31. Only event in the retrievable window:

```
change_date_time  : 2026-07-03 13:33:47.955208
user_email        : eddie@callzenair.com
client_type       : GOOGLE_ADS_WEB_CLIENT
campaign          : customers/3740502923/campaigns/20752144554
changed_fields    : status
old_resource      : { campaign: { status: "ENABLED" } }
new_resource      : { campaign: { status: "PAUSED" } }
```

`GOOGLE_ADS_WEB_CLIENT` = done by hand in the Google Ads interface, not a script or automated rule.

**PPC account in the same window:** only two non-ClickCease events, both `eddie@callzenair.com` on 2026-07-03 (asset creations, 10:08). The other 148 are ClickCease IP blocks. No TSD-side budget, keyword or bidding change in the last 30 days.

**Retention:** the API `change_event` resource only holds 30 days, so this window starts 2026-07-02. The Google Ads **UI** change history keeps ~2 years — pull the screenshot there (MCC 415-551-4468 → account 374-050-2923 → Tools → Troubleshooting → Change history) if earlier context is needed. Note LSA accounts have a reduced UI feature set; if that page isn't exposed, the API record above is the same underlying data.

**Context, not asserted as fact:** PPC was dark on Jul 3 (billing stop, resumed Jul 10), so LSA would have been the only channel visibly spending when Eddie was in the account. Plausible reading of why he pulled that lever and not another. The log does not prove intent.

**Handling:** do not put "you paused it" in the ticket reply. Frame as "LSA has been inactive since July 3 — recommending we restore at a $50/day cap." Evidence stays here for Ryan/AM if it is questioned, and supports the written-approval gate on client-side changes.

---

## 5. Meta — cheapest CPL, but quality is unverified

| Campaign | Spend (30d) | Leads | CPL | Status |
|---|---|---|---|---|
| CBO \| LEADS \| ANIV SALE (02JUL2026) | $1,233.81 | 133 | $9.28 | PAUSED |
| TSD_04.13_TOF_P.LEADS_CBO_$49Offer | $975.93 | 122 | $8.00 | PAUSED |
| TOFU - Brand Awareness_Reach_OA_FQ4_7 | $594.54 | 42 | $14.16 | **ACTIVE** |

The two campaigns producing $8–9 leads are paused; the one still running is the Reach campaign.

**The Reach campaign stays — brand awareness is a deliberate part of the strategy and $20/day is a controlled, cheap layer. Do not put it on any cut list.** It is also the argument that protects us on the PMax cut: we are not cutting awareness, we are moving awareness spend out of inventory Google allocates on its own ($100/day, unmanaged) and keeping it in the channel where we control audience, creative and frequency.

Two things to be straight about internally:
- These are Instant Form leads off a $49 tune-up offer. Tune-up shoppers, not system replacements. Comparing their $9 CPL to a $325 Search CPL is not apples to apples, and we should not tell Eddie "move it all to Meta."
- If Eddie's real complaint is "the leads don't book," 297 Meta leads is the likely source of it. **We need booked-job outcomes from the CRM on those 297 before restoring that line.**

**Action:** hold the paused lead campaigns until CRM outcomes come back. No change to the awareness line.

---

## 6. Also flagged

- **Two ENABLED campaigns not serving:** `A/C Service (Lead Gen)` ($60/day budget) and `Lead Gen Campaign (2024)` ($10/day). $0 spend in 30 days, but $70/day of live budget sitting there. Pause them or they will start spending unannounced.
- **Conversion tracking still polluted.** 26 of 30 conversion actions recorded zero in 30 days, including `LP | Qualified Lead` and `LP | Disqualified Lead (Out of Area)`. `book_now_link_click` and `ghl_service_area` are still categorized as **PURCHASE** and set primary. None of the cuts above depend on this — they are zero-on-every-tag lines — but any CPL we quote Eddie is soft until this is fixed. Carries over from the 2026-07-09 findings.

---

## 7. The plan

> **FINAL SCOPE (decided 2026-07-31, Edu).** The ticket reply covers **PMax only**. Search budget is deliberately NOT cut, because a landing-page restructure is coming and it is better to do that as one piece of work than trim in isolation. Meta awareness is not a cut candidate at all. Everything below Phase 1 is parked, not recommended.

**Phase 1 — what actually goes in the ticket**
| Move | Monthly saving |
|---|---|
| Pause PMax `TSD_03.23_PMAX_HVAC_Calls` (22959264938) | **~$3,000** ($100/day budget) |

That is the whole ask. Needs Eddie's written approval via the AM ticket before execution.

**Correction worth remembering:** an earlier version of this plan counted competitor negatives and a match-type change as ~$3,050/mo of savings. That was wrong. The Search campaign is budget-capped on Maximize Conversions, so negatives *redirect* spend, they do not reduce it. Only lowering the daily budget or pausing is a real cut.

**Parked — not being recommended now**
- Search budget $150/day → $60–75/day (objective floor: $50/day brand with margin, plus ~$24/day for the seasonal `emergency heating service ga`). Superseded by the landing-page restructure decision.
- Add a target CPA or move brand to Manual CPC with a $5–6 ceiling. **This is the real fix for the $18.45 brand CPC** and it should ride along with the restructure. Landing pages will help the non-brand side; they will not fix brand, because brand already rates Above Average on landing page experience.
- Pause the two idle ENABLED Search campaigns (`A/C Service (Lead Gen)` $60/day, `Lead Gen Campaign (2024)` $10/day). $0 spend today but $70/day of live budget sitting exposed.
- Restore LSA at a $50/day cap. Flagged softly in the reply as "worth talking through," not requested as an action.

**Why `hvac contractors near me` and not `emergency heating service ga`** — the keyword CPLs ($571 vs $254) sit on 6 and 2 conversions and are too thin to rank on. The real distinction: `hvac contractors near me` is a generic shopping term on broad match eating 75% of the budget at $32/click, and the search terms report shows where it went. `emergency heating service ga` is a *heating* keyword in Georgia in July with 176 impressions in 21 days. It self-limits at ~$24/day and is not a budget decision either way until October.

**Framing rule for anything that reaches Eddie:** none of this is presented as cleanup. The competitor-term detail, the zero-conversion network split and the tracking pollution stay in this file.

The accepted framing for PMax, in order: the campaign is set up to bring in calls and hasn't been pulling its weight on that → the money still bought real brand exposure on YouTube and display, and brand exposure is part of what we do (Brandformance) → we already run a dedicated awareness campaign on Meta doing that same job, where we choose who sees it, which video and how often, and Google decides all of that inside PMax → so he is covering the same ground twice and we can cut it.

Do **not** present PMax as purely a brand play. It is named `PMAX_HVAC_Calls` and that framing does not survive one follow-up question. Name the underperformance, then soften it with what the spend did buy.

**On the search budget, the client-facing line is:** new landing pages are coming, Google charges less per click when the page matches what was searched, and our main non-brand keyword currently rates *below average* on that. So the pages come first, then we reassess budget. (True — and it is the proactive version of the Ad Rank problem.)

**Phase 3 — gate**
Do not restore Meta lead spend until CRM booked-job data on the 297 July leads is back. That number decides whether Meta is the cheapest channel or the source of the complaint.

**Approval:** budget changes need Eddie's written approval via the AM ticket before anything is executed.
