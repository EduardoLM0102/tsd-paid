# Proud Pops: Client Strategy Review, Oct/Nov (row ENTERED in AT 2026-11-05, record bbedb9e0; stage not completed)

AT task: https://app.agencytitan.com/tasks/instance/4ae4f4a8-b8c4-464a-bc14-7bf8484ba4e2
Stage: Performance Reporting (Edu + Gui), was due 11-02. Cycle 2026-10-02 to 2026-10-31.
What the stage needs: one row in the client's "Client Performance KPIs" field (custom object 4038154a, client field c72c4f7e, embedded_list).
Pulled 2026-11-05 (Google Ads API read-only, GA4 438523825, CallRail export 10-14..11-03).

## Values for the KPI row

| Field | Value |
|---|---|
| period_start_date | 2026-10-02 |
| period_end_date | 2026-10-31 |
| ad_spend | 29011.70 |
| agency_fees | (blank, Angela/Edu to fill) |
| total_spend | (blank until fee is known) |
| qualified_leads | 44 |
| cpl | 659.36 |
| recommend_budget | 25000 |

budget_rationale:
> Client capped total spend at $25k/mo on 10-14, so Oct 15-31 ran Branded only. Recommend holding $25k for November: service campaigns were restored on 11-04 at $880/day and now bid only on real leads (CallRail first-time calls 60s+, ad calls 60s+, customer forms), not on call-button taps. Ad calls were not tracked before 10-14, so the full-cycle CPL ($659) undercounts leads. The first fully tracked stretch (Oct 14-31) was $4,370.74 for 32 leads = $137 CPL (PPC $180, LSA $64). Revisit the budget once November gives a full month of clean data.

## How the numbers were built

Ad spend Oct 2-31 = $29,011.70
- PPC 1051843378 (excl. its in-account LSA): $28,087.73 (Elec Search $8,030, HVAC Search $5,607, PMax HVAC $3,817, Branded $2,875, PMax Elec $2,729, Plumbing $2,141, YouTube x2 $2,889)
- LSA: $923.97 (in-account $376.71 + 7261668241 $225.31 + 6621969129 $321.95)
- Meta: $0

Qualified leads = 44
- PPC customer forms: 17 (GA4 generate_lead, google/cpc, /schedule 13 + /proud-pops-hvac-services 4; 25 /careers job apps excluded)
- PPC calls: 15 (CallRail, Google Ads source, Website pool tracker, first-time caller, 60s+). CallRail data starts 10-14, so Oct 2-13 calls are missing.
- LSA leads: 12 (Google LSA lead list, declined leads excluded; 16 total)
- NOT counted: Google Ads "conversions" (664 reported, 607 are TSD - Website Call taps, not leads). 3 GLSA calls in CallRail overlap the LSA leads.

Clean slice Oct 14-31: $4,370.74 / 32 leads (15 calls + 5 forms + 12 LSA) = $136.59
- PPC $3,608.65 / 20 = $180.43
- LSA $762.09 / 12 = $63.51

## Open for Edu
1. Which CPL goes in the row: full cycle $659 (as above) or the clean Oct 14-31 $137 with matching dates?
2. Agency fee for Proud Pops (needed for total_spend).
3. My Favorite Service Company acct 9815330464 has a Smart campaign "HVAC Contractor Services" that spent $614.49 in Oct ($372 after 10-14). Not included above. Is it ours / should it still be running?
4. After the row goes in: mark Performance Reporting complete, which hands the task to Angela for the call.
