# Proud Pops — Ad Rank Loss Diagnosis & Remediation

**Account:** 1051843378 (PPC) · **Date:** 2026-07-23 · **Source:** Google Ads API + GTM API
**Companion to:** `budget-analysis-2025-2026.md`, `budget-brackets-and-keyword-research.md`

---

## 1. The problem, measured

Post-cut window **Jul 8–22, 2026** (after Andrea's Jul 7 budget reduction):

| Campaign | ID | Spend | Search IS | Lost to **Rank** | Lost to Budget | Avg CPC |
|---|---|---|---|---|---|---|
| Search Nonbranded Plumbing | 23853484024 | $802 | 15.0% | **85.0%** | 0.0% | $3.16 |
| PMax HVAC | 23853595615 | $1,217 | 13.5% | **82.2%** | 4.3% | $0.87 |
| PMax Electrical | 23866982084 | $919 | 15.5% | **73.9%** | 10.6% | $0.78 |
| Search Nonbranded Electrical | 23866999121 | $780 | 11.1% | **50.0%** | 38.9% | $10.26 |

Top-of-page IS is **under 10%** on both Search campaigns. Only Nonbranded Electrical is
genuinely budget-constrained; the other three are pure Ad Rank problems where added budget
does nothing.

---

## 2. Root causes, in order of impact

### 2.1 Smart bidding had no conversion signal (dominant cause)

All four campaigns run `MAXIMIZE_CONVERSIONS`. The primary conversion actions feeding that
bidding recorded effectively nothing over the trailing 30 days:

| Conversion action | Primary | 30-day volume |
|---|---|---|
| `Website lead` | Yes | **0.0** |
| `Calls from ads` | Yes | **0.0** |
| `TSD - Website Call` | Yes | **0.3** |
| `www.txproblemsolvers.com (web) instant_quote_h` | No | 575 |

Maximize Conversions cannot estimate conversion rate without conversions, so it bids at the
floor. That collapses Ad Rank directly — and simultaneously produces the QS surcharge that
drives $20–30 CPCs when the account *does* win an auction.

The only high-volume action, `instant_quote_h`, is non-primary and is a **button click**
(~4:1 over known-real LSA leads). Do not make it biddable — that fabricates leads.

**Status: FIXED.** GTM container GTM-WBFDB6L8, **live version 38** "TSD - Fix conversion
labels (2026-07-23)" is published and verified:

- `05 | G.Ads - Lead` — awct, label `u5lXCI2jk7kYEKrcxssp` ✅
- `02 | G.Ads - Phone Call` — awct (flipped from awcc), label `LPUbCN6nosgcEKrcxssp` ✅
- `03 | G.Ads - Email` — awct, label `eFIRCJ7do8gcEKrcxssp` ✅

First signal confirmed: `TSD - Website Call` moved 0.3 (Jul 22) → **1.7 counted (Jul 23)**.
`Website lead` has not registered a first conversion yet — verify within 48h.

### 2.2 Quality Score averages 4.4, and the decomposition is unanimous

Expected CTR is `BELOW_AVERAGE` on **17 of 17** scored keywords. Landing page experience is
`BELOW_AVERAGE` on the single largest spender.

| Keyword | Match | QS | Ad relevance | LP exp. | Exp. CTR | Cost | CPC |
|---|---|---|---|---|---|---|---|
| plumber san antonio tx | Phrase | **3** | Above avg | **Below avg** | Below avg | $543 | $20.87 |
| electrician san antonio | Exact | **3** | Below avg | Average | Below avg | $177 | $14.75 |
| electrician san antonio tx | Phrase | **3** | Below avg | Average | Below avg | $119 | $29.75 |
| electrical services san antonio | Phrase | 5 | Above avg | Average | Below avg | $114 | $28.44 |
| electrical repair | Phrase | 5 | Above avg | Average | Below avg | $202 | $11.22 |

### 2.3 Match/routing pollution is suppressing expected CTR

Of **$1,972** in visible search-term spend over 30 days, roughly **$1,520 (77%)** went to
queries that cannot become a lead. (Visible terms only — privacy-thresholded terms are
excluded, so true waste is higher.)

| Bucket | Cost | Notes |
|---|---|---|
| Competitor brand names | ~$809 | `airtron` $101, `allgood electric` $65, `mr electric` $51, `elmers plumbing` $50, `abc plumbing` $49, `reliabee` $44, `aaron plumbing` $41 … mostly 1 click each at $30–68 |
| Wrong service line in Electrical | ~$325 | `hvac contractors in my area` $89, `hvac companies in my area` $92, `plumbing contractors in my area` … |
| Own brand leaking into nonbranded | ~$221 | `proud pops san antonio` $116, `proud pops plumbing` $35 — while the Branded campaign sits PAUSED |
| Non-lead / non-residential | ~$165 | `cps gas leak` $39 (utility), `repair electric motors` $29, `handyman` $22, `plumbers and pipefitters` $15 |

Driver: **AI Max + text asset automation + final URL expansion** were enabled by
brandon@proudpops.com on 2026-06-26 on `TSD_05.20_Leads_Search_Nonbranded_Electrical` and
are still on. This is what pushes HVAC and plumbing queries through an *electrical* campaign
at a $10.26 CPC.

Compounding it: **$6,623 of ~$8,000 in click spend lands on `proudpops.com/`** — the
homepage — even though `/services/plumbing`, `/services/electrical` and `/services/hvac`
all exist. Service queries on a generic page is what holds LP experience down.

---

## 3. Change list

> **Blocked:** Google Ads mutations are denied by the auto-mode classifier in this
> environment. GTM writes are permitted; Ads writes are not. Items 2–5 below need to be
> executed in the UI or with an explicit Bash permission grant.

### ✅ 1. Publish the GTM conversion-label fix — **DONE** (live v38, verified above)

### 2. Add negatives *before* touching bids
Order matters. Loosening bid control before the negatives are in will buy more junk.

**Own brand → add to BOTH nonbranded campaigns** (23853484024, 23866999121), phrase match:
```
proud pops
problem solvers
```

**Competitor brands → new shared negative list, applied to both Search campaigns**, phrase:
```
airtron            allgood electric    mr electric        mr sparky
elmers plumbing    abc plumbing        reliabee           aaron plumbing
quarter moon       zeus plumbing       infinity plumbing  mission plumbing
bryco              casa mechanical     wright ac          elbel
specialty plumbing alamo electric      ventura plumbing   primo plumbing
damien electrical  champion home services                 anchor plumbing
```
⚠️ `pops heating and air` ($21) is a distinct company but collides with Proud Pops brand
recall. Review manually before adding — a negative here may block real brand searches.

**Non-lead → both Search campaigns**, phrase:
```
cps            electric motor    motor repair    pump repair
handyman       pipefitters       electrical shops                electrical testing
jobs           salary            apprentice
```

**Cross-service → `TSD_05.20_Leads_Search_Nonbranded_Electrical` (23866999121) only**, phrase:
```
hvac    plumbing    plumber    air conditioning    ac repair
water heater        furnace     drain    sewer     heating
```

### 3. Turn off AI Max on 23866999121
Campaign → Settings → uncheck **AI Max**, **final URL expansion**, and **automatically
created assets**. This is the source of the cross-service bleed.

### 4. Interim bid control on the two Search campaigns
See §4 — decision required before executing.

### 5. Unpause the Branded campaign — 23853361615
Verified ready: 5 ad groups (`Brand_Electrical`, `Brand_Plumbing`, `Brand_HVAC`,
`Brand_OldName`, `Brand ProudPops`), ~30 keywords, all ENABLED, ads ENABLED at $20/day.
`Brand_OldName` still covers "the problem solvers" — correct to keep through the rebrand.

Note: `Brand ProudPops`, `Brand_HVAC` and `Brand_OldName` ads are **POOR** ad strength.
Acceptable for brand defense, worth refreshing later.

### 6. Landing page routing (QS lever, no bid change)
Point ad groups at matching service pages instead of the homepage:
`/services/plumbing`, `/services/electrical`, `/services/hvac`,
`/services/hvac/air-conditioning/repair`.

---

## 4. Open decision — the interim bid strategy

The original recommendation was to move the two Search campaigns to Manual CPC or
Maximize Clicks *while the conversion signal rebuilt*. **That premise changed**: the GTM fix
is already live as of today, so signal is flowing now.

**Option A — leave on Maximize Conversions.** It starts learning from real data immediately,
no strategy churn. Cost: rank stays suppressed for 2–4 weeks while conversion history
accumulates from near zero.

**Option B — switch to Maximize Clicks with a CPC ceiling (~$12 plumbing / ~$18 electrical)
for 2–3 weeks, then back.** Restores impression share now, and the extra traffic feeds the
newly fixed tracking faster. Cost: a learning reset on the way back.

**Recommendation: Option B, but only after §3 item 2 (negatives) is live.** The
"learning reset" objection is weak here because there is no learning to protect — these
campaigns have ~0 conversions in 30 days, so Maximize Conversions is stalled, not learning.
The real risk in Option B is Maximize Clicks chasing cheap junk, which the negatives and the
AI Max shutdown directly address. Sequence: negatives → AI Max off → bid change.

Do **not** add a tCPA target until there is a real observed CPA (≥ 2–3 weeks of clean data).

---

## 5. Verification checklist (48h / 2 weeks)

- [ ] `Website lead` registers its first conversion (48h) — if not, re-check the Lead trigger in GTM Preview
- [ ] `TSD - Website Call` continues accumulating past 1.7/day
- [ ] Search-term report shows competitor/cross-service terms gone
- [ ] Branded campaign absorbs `proud pops *` traffic; nonbranded brand spend → ~$0
- [ ] Rank-lost IS on 23853484024 falls below 85%
- [ ] Re-pull QS after 2 weeks — expected CTR should move off Below Average on the head terms
