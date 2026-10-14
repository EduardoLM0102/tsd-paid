# Proud Pops — Budget cut 2026-10-13: change record + baseline for the review

Account 1051843378 (America/Chicago). Internal. Follow-ups in the Command Center: fu-046 (YouTube SA pause),
fu-047 (pacing recheck 10-20), fu-048 (calls check once CallRail access is in, due 10-16).

## 1. What changed

Applied **2026-10-13 17:17:25 CT** as eduardo@topservdigital.com (change_event), script `budget_cut_50k_2026-10-13.py`,
read back OK. Budgets only. Nothing else (bidding, targets, ads, keywords) was touched in this change.

| Campaign | ID | Type / bidding | Before | After | Change |
|---|---|---|---:|---:|---:|
| PMax HVAC | 23853595615 | PMax, Max Conv, tCPA $27 | $295 | **$50** | −$245 (−83%) |
| PMax Electrical | 23866982084 | PMax, Max Conv | $230 | **$75** | −$155 (−67%) |
| Search HVAC | 23848895678 | Search, Max Conv, tCPA $265 | $375 | **$300** | −$75 (−20%) |
| Search Electrical | 23866999121 | Search, Max Conv | $600 | **$500** | −$100 (−17%) |
| YouTube San Antonio (VideoViews) | VIDEO | Target CPV | $100 | **pause pending (Edu, UI)** | −$100 |
| **Total daily caps** | | | **$1,960** | **$1,385** (→ $1,285 after SA pause) | −$575 (−$675) |

**Unchanged (comparison group):** Search Plumbing $160 (Max Clicks, $45 cap since 10-08), Branded $100, YouTube New
Braunfels $100, in-account LSA.

## 2. Why

- The client approved **$50k/month**, but the account was spending about $60k/month. September came to $59,635 (PPC
  account) and October was pacing at about $60k.
- **Root cause:** the $50k was the August pool. By Aug 10 only $6,005 had been spent, so the Aug 10 and Aug 17 raises
  (plus YouTube $200/d from Aug 8) were sized to spend about $44k in 21 days, roughly $2,100/d. Nobody rolled that rate
  back on Sep 1. Caps of $1,960/d × 30.4 = $59.6k/month.
- **October so far:**
  - Oct 1–12: $24,185
  - Oct 13: about $2,000, mostly at the old caps
  - That leaves about $23.8k for Oct 14–31, which means about $1,285/d of caps.
- **How the cuts were chosen:** by cost per real customer FORM. **Calls were not measurable:** Google Ads sees 0 confirmed
  calls (the call asset is disapproved, CallRail isn't linked, and CallRail swaps no number on the site). Phone taps are
  clicks on the number, not calls.
- **The open question (fu-048):** campaigns with few forms may drive calls instead. That matters most for electrical
  and plumbing emergencies.

## 3. Baseline (before the cut)

### 3a. Sep 8–Oct 7, customer forms (from the 30-day report; /careers job applications removed via GA4 split)

| Campaign | Spend | Clicks | CPC | Customer forms | $/form | Phone taps |
|---|---:|---:|---:|---:|---:|---:|
| Search Electrical | $18,596 | 758 | $24.53 | 17 | $1,094 | 101 |
| Search HVAC | $11,153 | 306 | $36.45 | 12 | $929 | 38 |
| Search Plumbing (ctl) | $5,012 | 134 | $37.40 | 6 | $835 | 28 |
| Branded (ctl) | $2,117 | 203 | $10.43 | 7 | $302 | 19 |
| PMax HVAC | $9,808 | 8,558 | $1.15 | 2 | $4,904 | 344 |
| PMax Electrical | $6,889 | 16,139 | $0.43 | 3 | $2,296 | 697 |
| YouTube SA / NB | $3,015 / $3,014 | 23 / 175 | | 0 | | 0 |

### 3b. Sep 13–Oct 12 (30 days), same query the review script runs (`budget-cut-2026-10-13/pre30.json`)

"Forms" here still include job applications before 10-07, so use 3a or 3c for forms.

| Campaign | $/day | CPC | Search IS | Lost to budget | Lost to rank | Taps (of which Display/YouTube) |
|---|---:|---:|---:|---:|---:|---:|
| Search Electrical | $595 | $25.55 | 27% | 25% | 48% | 95.5 (0) |
| Search HVAC | $387 | $40.35 | 28% | 22% | 50% | 38 (0) |
| PMax HVAC | $322 | $1.13 | 10% | 90% | 1% | 374 (373) |
| PMax Electrical | $229 | $0.47 | 17% | 14% | 69% | 791 (735) |
| Search Plumbing (ctl) | $160 | $33.29 | 19% | 28% | 53% | 23 (0) |
| Branded (ctl) | $73 | $10.36 | 70% | 21% | 9% | 25.5 (0) |
| YouTube SA / NB | $100 / $100 | | | | | 0 |

### 3c. Oct 8–12 (5 days, clean: careers fix live, before the cut) (`postfix5.json`)

| Campaign | $/day | Customer forms | Phone taps (Display/YouTube) | Search IS | Lost to budget | Lost to rank |
|---|---:|---:|---:|---:|---:|---:|
| Search HVAC | $541 | 0 | 8 (0) | 40% | 0% | 60% |
| Search Electrical | $533 | 5 ($533/form) | 11 (0) | 39% | 19% | 41% |
| PMax HVAC | $314 | 0 | 72 (72) | 10% | 90% | 0% |
| PMax Electrical | $226 | 0 | 184 (182) | 10% | 17% | 75% |
| Search Plumbing (ctl) | $152 | 1 | 0 | 27% | 62% | 10% |
| Branded (ctl) | $104 | 1 | 7 | 83% | 13% | 4% |

Also saved: `pre7.json` (Oct 6–12). Each JSON has spend by network, taps by network, conversions by action, and daily
spend per campaign.

## 4. How to review

**After window:** start **Oct 14** (first full day). Leave out Oct 13 (mixed day). Two weeks = Oct 14–27.
`./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/budget_cut_review_2026-10-13.py --since 2026-10-14 --until 2026-10-27 --label post14`

**Questions to answer:**
1. **Did form volume drop where we cut?** Compare clean forms per day against 3c (and 3a for $/form).
2. **Did calls drop? (fu-048, needs CallRail)**
   - Answered calls of 60s or more per campaign, before vs after.
   - If the cut campaigns lose calls and the comparison group doesn't, the cut cost real leads.
   - Electrical and Plumbing first.
3. **Is the cut binding?**
   - On Search Electrical / HVAC: if lost-to-budget IS jumps and forms/calls fall, that budget was buying leads.
   - If lost-to-rank still dominates, the money wasn't doing much.
4. **Did taps turn into calls?** PMax taps are about 98% Display/YouTube. If CallRail shows few calls from PMax, the taps were noise and PMax HVAC can be paused (P-2).
5. **Pacing:** daily spend vs the new caps. Max Conversions can run well over cap on single days (Search HVAC ran $541/d on a $375 cap Oct 8–12).

**What to do with the answer:** about $315/d comes back on Nov 1 ($50k/month steady state ≈ $1,600/d caps). Put it
wherever the call + form data says the cut hurt most. If nothing was hurt, put it in Branded/Plumbing (budget-limited, cheapest per form).

## 5. Confounders (don't credit or blame the cut for these)

- **10-08 changes on the same campaigns:**
  - Search Electrical: AI Max off, 39 negatives, ads moved to /services/electrical
  - Search HVAC + Plumbing: competitor negatives
  - Location: HVAC/Plumbing widened to the 20-city metro, plus presence-only targeting
  - PMax: brand exclusion + /careers exclusion
  - Branded: widened to 47 cities, + "pops electric" keywords
  - YouTube: kids' content excluded
- **Under review / still to come:**
  - 14 new RSAs (G2b cutover)
  - AG4_Plumbing_General (H7a)
  - Block F (phone taps → Secondary, HVAC tCPA off): this changes what Max Conversions optimizes for. Note its date
    if it lands inside the after window.
- **Measurement and season:**
  - Careers fix (10-07 10:32 CT): any form count crossing that time mixes job applications in.
  - Season: HVAC demand shifts from cooling to heating in late October.
  - LSA call volume has been collapsing since June (profile-side, unrelated to this change).
