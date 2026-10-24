# Watt's Right: Q4 2026 / Q1 2027 budget proposal, internal notes

Not client-facing. Draft built 2026-10-23 (Gui + Claude) for AT Client Request `7b72529c` ("Budget Proposal", requested by Allen via
Angela: proposal for Q4 2026 & Q1 2027 to increase leads, client OK with higher CPL, wants leads to keep coming in the slow season).
Status: **v2.1 FINAL, READY TO SEND (2026-10-24, Gui validated).** Nothing uploaded to AT, nothing changed in any account.

## v2.1 (2026-10-24, Gui's call): client table back on RAW leads, PMax explained by quality

Gui wanted the client-facing baseline on raw counts (Google conversions = calls from ads + Phone Call + forms; taps still excluded),
not the verified counts, with the verified finding used only to explain why PMax gets no extra budget ("good volume, but many calls
weren't service requests; lots of room to improve, so the extra goes to Search"). The verified table in the v2 section below stays
internal. Options were recomputed on the same raw basis so "today" and "Current" agree:

| Raw basis, 09-23..10-22 | Spend | Leads | CPL |
|---|---|---|---|
| LSA | $12,737 | 219 | $58 |
| Search (Branded 27 + NB 28 + EV 2, paused 09-29) | $4,251 | 57 | $75 |
| PMax (19 calls from ads + 6 Phone Call + 11 forms) | $2,585 | 36 | $72 |
| Meta | $7,836 | 152 | $52 |
| **Total** | **$27,409** | **464** | **$59** |

| | Current | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| Daily Branded / NB / PMax | $35 / $105 / $95 | $45 / $150 / $95 | $45 / $205 / $95 | $50 / $260 / $95 |
| Meta extra | 0 | +$30/d TOF | +$60/d TOF, ARL $20/d | +$100/d TOF, ARL $35/d |
| Assumed raw marginal CPL | | Brand ~$30, NB ~$125, Meta ~$55 | Brand ~$30, NB ~$130, Meta ~$58 | Brand ~$35, NB ~$140, Meta ~$62 |
| Extra leads | | ~38 (10 + 11 + 17) | ~70 (10 + 23 + 37) | ~108 (13 + 34 + 61) |
| Leads / CPL in PDF | ~460 / $60 | ~500 / $61 | ~530 / $63 | ~570 / $64 |

Remember these are raw counts: on the verified basis Google Search runs ~$115 and PMax ~$199 per lead (v2 section).

## v2 (2026-10-24, internal only after v2.1): verified-lead basis

v1 counted Google leads as Google conversions (calls from ads + Phone Call + forms). The PMax CallRail check (section below) showed
most of PMax's counted calls were wrong numbers, so v2 counts **Google Search + PMax leads = verified service calls + form fills
from 09-30 on** (after the 09-29 careers-form block). LSA = charged leads, Meta = form leads (unchanged, stated in the PDF).

| Channel (09-23..10-22) | Spend | Verified call leads | Forms (09-30+) | Leads | CPL |
|---|---|---|---|---|---|
| LSA | $12,737 | | | 219 | $58 |
| Search: Branded | $548 | ~16 (11 reviewed + ~5 est.) | 5 | ~21 | ~$26 |
| Search: Nonbranded | $3,154 | ~9 (7 reviewed + ~2 est.) | 7 | ~16 | ~$197 |
| Search: EV Charger (paused 09-29) | $549 | 0 (1 call = job seeker) | 0 | 0 | |
| **Google Search row** | **$4,251** | | | **37** | **$115** |
| PMax | $2,585 | 7 (all 42 recordings reviewed: 5 new + 2 existing-customer service) | 6 | 13 | $199 |
| Meta | $7,836 | | | 152 | $52 |
| **Total** | **$27,409** | | | **421** | **$65** |

- EV Charger's $549 is now inside the Search row (v1 had left it out of the 30-day spend).
- "Reviewed" = transcript classified (Edu's call-wins log 10-01..10-19 matched by time + duration, plus Claude's transcripts). The ~7 "est."
  Search call leads apply each campaign's reviewed lead rate (NB ~30%, Branded ~79%) to the 17 calls still being transcribed on 10-24.
  Swap in the real count when `_pessoal/call-wins/watts-right-search/` finishes, rebuild if the row moves more than a lead or two.
- **NB and PMax cost about the same per verified lead (~$200).** NB wins on booked new jobs (~3-6 booked new in 30d vs PMax 1 that stuck,
  ~$525 vs $1,300-2,600 per booked job), and its booked jobs are high-ticket (EV chargers, panels, generator estimate). Branded is by far the
  cheapest (~$26) but capped by brand search volume. That's why the PMax increment went to Search, Branded first.
- Branded still lost 22% IS to budget on 10-20..10-22 after Edu's $35 change → $45 in Options 1-2, $50 in Option 3.
- NB on 10-20..10-22: budget-lost 7%, rank-lost 68% under tCPA $80. **The NB increase only spends if the tCPA goes up with it.**

### v2 option math (monthly, 30.4 days)

| | Current | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| Branded daily | $35 | $45 | $45 | $50 |
| NB daily | $105 | $150 | $205 | $260 |
| PMax daily | $95 | $95 | $95 | $95 |
| Meta extra | 0 | +$30/d TOF | +$60/d TOF, ARL $10→$20/d | +$100/d TOF, ARL $10→$35/d |
| Assumed marginal CPL (verified basis) | | Brand ~$40, NB ~$230, Meta ~$55 | Brand ~$40, NB ~$240, Meta ~$58 | Brand ~$45, NB ~$260, Meta ~$62 |
| Extra leads | | ~30 (8 + 6 + 17) | ~57 (8 + 13 + 37) | ~89 (10 + 18 + 61) |
| Leads / CPL | ~420 / $66 | ~450 / $67 | ~480 / $69 | ~510 / $72 |

Most of the extra volume comes from Meta TOF ($42 form leads), which has NOT been checked against booked jobs. Say so if Allen asks
where the leads come from. The v1 option math below is superseded.

Files: `budget-proposal-q4-2026-q1-2027.md` (source) → `build_budget_proposal.py` → `Watts-Right-Budget-Proposal_Q4-2026-Q1-2027.pdf` (2 pages).

## Baseline (09-23..10-22, pulled 10-23)

| Channel | Spend | Leads | CPL | Notes |
|---|---|---|---|---|
| LSA (in-account, 17732780541) | $12,737.32 | 219 (183 phone + 36 msg) | $58 | budget $1,714.29/d ($12k/wk), spends ~$425/d = 25% of cap. Maximize leads, no target (stale manual bid $17 in settings is unused) |
| Search Branded | $547.91 | 27 | $20 | Target IS, $8 cap, $35/d; budget-lost IS 35% over the window; Edu changed its ad schedule 10-20 |
| Search Nonbranded | $3,153.71 | 28 real (+6 taps) | $113 | $105/d, tCPA $80 set by Edu 10-20; IS 29%, budget-lost 26%, rank-lost 45%. Ad groups: Panel Upgrade, Emergency Electrician, EV charger |
| PMax | $2,585.29 | 36 real (+41 taps) | $72 | $95/d, budget-lost 27%, rank-lost 45% |
| Meta lead campaigns + ARL | $7,835.47 | 152 | $52 | TOF $3,418 / 81 ($42), MOF $1,981 / 34, BOF $578 / 10, FourMode $1,558 / 27, ARL $10/d $301 |

- "Leads" = calls from ads + Phone Call + forms. **[TSD] Click to call taps excluded** (47 in 30d).
- **Excluded from Meta:** ~$468 of boosted engagement posts (non-TSD, client/Manus side, 0 leads).
- **Meta ownership caveat:** TOF and FourMode keep non-TSD names; Clay Manus (Manus Dash) reverted TSD renames 10-06 and launched an RT ad set.
  Confirm with Edu/AM who executes the Meta increase before promising it.

## Seasonality evidence

LSA charged leads (lead report): 2025 Oct 122, Nov 137, Dec 130, 2026 Jan 131, Feb 105, Mar 143. Summer 2026 peak Jul 326, Sep 209, Oct pace ~235.
YoY: Sep 1.7x, Oct ~1.9x → "70 to 90% more". PPC history before TSD is not usable (2025-2026 PMax counted junk: e.g. Jan 2026 2,465 all_conv).
Meta barely ran Dec 2025 to Apr 2026, so there is no Meta winter baseline. **Assumed:** Nov–Jan ≈ current level, Dec ~0.95, Feb ~0.85.

## v1 option math (SUPERSEDED by v2 above)

| | Current | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| NB daily | $105 | $140 | $170 | $210 |
| Branded daily | $35 | $35 | $45 | $45 |
| PMax daily | $95 | $115 | $130 | $150 |
| Meta extra | 0 | +$30/d TOF | +$60/d TOF, ARL $10→$20/d | +$100/d TOF, ARL $10→$35/d |
| Assumed marginal CPL | | NB ~$110, PMax ~$85, Meta ~$55 | NB ~$115, Brand +5 leads, PMax ~$90, Meta ~$58 | NB ~$125, PMax ~$95, Meta ~$62 |
| Extra leads | | ~34 | ~65 | ~98 |

LSA kept at ~$12,700 (pay per lead, follows demand). Totals are rounded in the PDF.

## ⚠ PMax CallRail check (2026-10-23, Gui + Claude): the PMax lead count does not hold up

Cross-checked the baseline's PMax "36 real leads" against CallRail (Watt's Right account 537241053), 09-23..10-22.
Attribution: CallRail's Google Ads integration stamps the campaign on gclid calls; calls without it were matched to
Google `call_view` by start time (±2 min, all 69 Google-logged ad calls matched). **PMax = 45 calls** (42 recorded),
all transcribed locally (faster-whisper small.en, audio + transcripts in `_pessoal/call-wins/watts-right-pmax/`, never committed).

| Outcome (42 recorded PMax calls) | Calls | Detail |
|---|---|---|
| New lead, booked | 2 | main breaker tripping (cancelled 8 min later: found someone faster and free); permanent eave lighting estimate |
| New lead, open / weak | 3 leads (5 calls) | out of service area (McAlester, "exception" pending); Wagner seller with GFCI questions, declined appointment; garbled Spanish caller "need work" |
| Existing customer | 3 | warranty/QC callback, breaker trip on an existing account (booked), tech left a tool |
| Wrong number / other business | 15 | utility bills and outages (PSO, Claremore, OG&E, "Tulsa Oklahoma Electric"), Generator Supercenter x2, city inspector, Mr. Sparky customer, other contractors, hearing aid, pharmacy |
| Retail / parts, job seeker, out of area, vendor | 6 | wire, light bulb, generator oil, buy generators; apprenticeship; Kansas / Washington |
| No conversation | 11 | silence, noise, 10-30s hang-ups |

- **Real new-customer calls: 2 booked (1 cancelled) + 3 open, out of 45.** That's ~$520 per real call lead and ~$2,585 for the one job that stuck, vs the $72 CPL in the proposal.
- Google counted 19 "Calls from ads" + 6 "Phone Call" on PMax. Utility/wrong-number calls run 60-300s, so they pass the duration threshold and **Max Conversions is learning from them** (bidding toward more of the same).
- PMax search terms match the calls: top term `generator supercenter tulsa` (11 clicks), `city of tulsa utilities`, `electric company`, `tulsa oklahoma electric company`, apprenticeship/union/job terms, competitor names.
- PMax's 11 "Submit lead form - web" are NOT verified (5 fall on or before the 09-29 careers-form block). Check them in GHL before counting them.
- Spend split: Search $2,075, Display $200, YouTube $169 (YouTube's 54 "follow-on views" are the all_conv inflation).
- Not yet checked: Nonbranded (34 calls, ~136 audio min) and Branded (22 calls, ~138 min). The "Call Extension PPC" junk in Edu's 10-01..10-15 call-wins log is spread across campaigns, so Search's 55 leads may be inflated too.

**Implication for the proposal (applied in v2):** don't put more money into PMax as it stands (Option 2 adds ~$1,060/mo there). Either hold PMax flat and
move that increment to Nonbranded/Meta TOF, or fix PMax first (utility/retail/job/competitor negatives via account-level list, brand
exclusions, and a call conversion that doesn't reward 60s wrong-number calls) and re-read in 2-3 weeks. The client-facing baseline table
(PMax 36 leads / $72) overstates PMax and should be corrected before sending.

## Before executing (if the client approves)

- Signed proposal = written budget approval up to that monthly total ([[tsd-budget-approval-scope]]). Log the approval in the AT task.
- **Raise NB tCPA with the budget** (Edu set $80 on 10-20): with a tCPA at $80 a bigger budget may not spend. Client accepted higher CPL → ~$100-110.
- Build the new NB ad group: Whole-Home Generator Installation + Whole-Home Surge Protector Installation (both listed on callwattsright.com).
  Verify the landing pages exist first.
- Meta: scale TOF (cold) first; MOF/BOF retargeting is not cheaper than TOF today. Awareness ARL stays uncapped ([[tsd-meta-ads-methodology]]).
- No-cost LSA levers to check in the UI (API can't see them): service area vs the 19 site cities, job types, hours (site says 24/7).
- Monthly check vs plan; move money between platforms inside the approved total (no new approval needed).

## Draft for the AT Execution stage (Request Completion Notes), for Gui to paste after validating

> Budget proposal for Nov 2026 to Mar 2027 attached. Three options on top of current budgets (~$27.7k/mo all platforms): Keep It Steady +$2.6k/mo (~500 leads/mo),
> Grow +$5.5k/mo (~530 leads/mo, our recommendation), Push +$9k/mo (~570 leads/mo). LSA and Performance Max stay at today's budgets (LSA isn't
> budget-limited; Performance Max has a lot of room to improve call quality first); the extra goes to Google Search and Facebook/Instagram.
> Cost per lead goes from ~$60 to ~$61-64, which the client said is OK. Once Allen picks an option, we need it in writing on this ticket before we change budgets.
