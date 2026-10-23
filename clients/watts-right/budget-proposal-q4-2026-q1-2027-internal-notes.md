# Watt's Right: Q4 2026 / Q1 2027 budget proposal, internal notes

Not client-facing. Draft built 2026-10-23 (Gui + Claude) for AT Client Request `7b72529c` ("Budget Proposal", requested by Allen via
Angela: proposal for Q4 2026 & Q1 2027 to increase leads, client OK with higher CPL, wants leads to keep coming in the slow season).
Status: **DRAFT, waiting for Gui to validate.** Nothing uploaded to AT, nothing changed in any account.

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

## Option math (monthly, 30.4 days)

| | Current | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| NB daily | $105 | $140 | $170 | $210 |
| Branded daily | $35 | $35 | $45 | $45 |
| PMax daily | $95 | $115 | $130 | $150 |
| Meta extra | 0 | +$30/d TOF | +$60/d TOF, ARL $10→$20/d | +$100/d TOF, ARL $10→$35/d |
| Assumed marginal CPL | | NB ~$110, PMax ~$85, Meta ~$55 | NB ~$115, Brand +5 leads, PMax ~$90, Meta ~$58 | NB ~$125, PMax ~$95, Meta ~$62 |
| Extra leads | | ~34 | ~65 | ~98 |

LSA kept at ~$12,700 (pay per lead, follows demand). Totals are rounded in the PDF.

## Before executing (if the client approves)

- Signed proposal = written budget approval up to that monthly total ([[tsd-budget-approval-scope]]). Log the approval in the AT task.
- **Raise NB tCPA with the budget** (Edu set $80 on 10-20): with a tCPA at $80 a bigger budget may not spend. Client accepted higher CPL → ~$100-110.
- Build the new NB ad group: Whole-Home Generator Installation + Whole-Home Surge Protector Installation (both listed on callwattsright.com).
  Verify the landing pages exist first.
- Meta: scale TOF (cold) first; MOF/BOF retargeting is not cheaper than TOF today. Awareness ARL stays uncapped ([[tsd-meta-ads-methodology]]).
- No-cost LSA levers to check in the UI (API can't see them): service area vs the 19 site cities, job types, hours (site says 24/7).
- Monthly check vs plan; move money between platforms inside the approved total (no new approval needed).

## Draft for the AT Execution stage (Request Completion Notes), for Gui to paste after validating

> Budget proposal for Nov 2026 to Mar 2027 attached. Three options on top of current budgets (~$27.7k/mo all platforms): Keep It Steady +$2.6k/mo (~495 leads/mo),
> Grow +$5.5k/mo (~525 leads/mo, our recommendation), Push +$9k/mo (~560 leads/mo). LSA stays as is (pay per lead, its cap isn't the limit);
> the extra goes to Google Search, Performance Max and Facebook/Instagram. Cost per lead goes from ~$60 to ~$61-65, which the client said is OK.
> Once Allen picks an option, we need it in writing on this ticket before we change budgets.
