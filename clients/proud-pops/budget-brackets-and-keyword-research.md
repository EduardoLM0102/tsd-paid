# Proud Pops — Budget Brackets + Keyword Research (July–August)

**Prepared by:** Eduardo Marinho, Paid Ads · **Date:** July 23, 2026
**Covers the two open commitments:** (1) good/better/best budget brackets for maximum impression share, with AC campaign strategy; (2) water-treatment / water-softener keyword research to work around expensive mainstream plumbing terms.
**Source:** Google Ads API + Keyword Planner, San Antonio (geo 1026339), pulled 2026-07-23. Impression-share and CPC figures are LAST_30_DAYS actuals from account 1051843378. Companion to the spend/performance review (past-PPC section is covered there).

---

## 1. Good / Better / Best budget brackets

**The honest ceiling first.** The account is budget-limited, but that is *not* its main constraint right now. Across the four live non-branded campaigns it loses **57–83% of impression share to Ad Rank** and only **3.5–29.5% to budget.** Money buys back the budget-lost share; it does **not** buy back the rank-lost share — that needs ad relevance, landing pages and bidding. So these brackets are sized to what budget can actually recover, not to a theoretical 100% impression share.

Current run rate (last 30 days): PPC non-branded **$9,164/mo**, LSA **$3,390/mo**.

| Bracket | PPC/mo | LSA/mo | **Total/mo** | Daily | What it buys |
|---|---:|---:|---:|---:|---|
| **GOOD** | $16,600 | $3,390 | **$19,990** | ~$658 | Clears budget loss on the two most-constrained campaigns (Nonbranded Electrical, PMax HVAC) |
| **BETTER** | $18,100 | $3,390 | **$21,490** | ~$707 | Recovers **all** impression share currently lost to budget across the four campaigns |
| **BEST** | $20,800 | $3,390 | **$24,190** | ~$796 | BETTER + ~15% headroom so the rank/quality fixes can convert into volume as they land |

**Per-campaign budget loss (last 30 days) — where the money should go:**

| Campaign | Spend/mo | Impr. share | Lost to budget | Lost to rank |
|---|---:|---:|---:|---:|
| Nonbranded Electrical | $2,486 | 13.9% | **29.5%** | 56.6% |
| PMax HVAC | $3,081 | 16.6% | **11.7%** | 71.7% |
| PMax Electrical | $1,755 | 15.5% | 8.9% | 75.6% |
| Nonbranded Plumbing | $1,842 | 13.7% | 3.5% | 82.9% |

**Reading it:** Nonbranded Electrical is the one genuinely starving for budget — nearly a third of its available impressions are lost purely because it runs out of money. That is where the first incremental dollars return the most. Nonbranded Plumbing, by contrast, loses almost nothing to budget (3.5%) and 83% to rank — throwing budget at it does nothing until its Quality Score and landing page improve.

**My recommendation: start at GOOD ($19,990), move to BETTER within 2–3 weeks** once the Electrical budget-loss closes and CPL holds. Only go to BEST after the tracking fix is verified and the rank issues on Plumbing/PMax are being worked — otherwise the extra headroom pays for impressions the ads aren't good enough to win.

**One thing to raise in the meeting:** the campaign budgets were cut on **July 7** (PMax HVAC $130→$80/day, Nonbranded Electrical $108→$50/day, Nonbranded Plumbing $90→$60, PMax Electrical $80→$60 — total $409→$250/day, by andrea@topservdigital.com). Every bracket above is an *increase* on that reduced level. Whoever approves the bracket should know the starting point moved down two weeks ago.

---

## 2. AC campaign strategy — service/repair vs install/replace

These are two different buyers and must not share a campaign or a bid. Market data, San Antonio:

**AC service / repair — the volume engine.**

| Keyword | Monthly vol | Competition | Top-of-page bid |
|---|---:|---|---|
| ac repair / air conditioning repair | 2,900 | LOW | $33–$112 |
| ac repair near me | 1,600 | MEDIUM | $38–$112 |

- Roughly **4,500+ searches/month** in the repair cluster, and competition reads LOW-MEDIUM — unusually soft for this bid range. High intent, immediate need, short path to a call.
- **Strategy:** dedicated Search campaign, tight exact/phrase match on the repair terms, call asset + call-only where possible, bid to a target CPA anchored on the phone-lead conversion. This is where the LSA and the call-tracking fix matter most — repair is a phone-call sale.

**AC install / replacement — lower volume, higher ticket, longer consideration.**

| Keyword | Monthly vol | Competition | Top-of-page bid |
|---|---:|---|---|
| ac installation / air conditioner installation | 480 | LOW | $20–$83 |
| hvac installation | 260 | LOW | $9–$32 |
| ac replacement | 210 | MEDIUM | $15–$90 |

- Under **1,000 searches/month** combined — a tenth of repair volume — but each job is worth many times a repair.
- **Strategy:** separate Search campaign so its budget and bids aren't eaten by the much higher repair volume. Longer conversion window, expect form-fills and quote requests as much as calls, and a landing page built around financing / free estimate rather than "we'll be there today."

**Why split them:** in one campaign, repair's 4,500 searches would consume the budget and starve install entirely, and a target CPA tuned for a $200 repair call is wrong for a $6,000 system quote. Two campaigns, two budgets, two bid strategies.

---

## 3. Water treatment / water softener — the workaround research

**The question was whether water treatment can be leveraged to get around the expensive mainstream plumbing keywords.** Short answer: **yes, but it's a small, specific play — not a volume replacement.** Here's what the San Antonio data actually shows.

**Finding 1 — most "water" search volume is retail/DIY, not a service lead.** The largest clusters are `reverse osmosis filter`, `brita`, `berkey`, `under sink filter`, `whole house water filter` — people shopping for a product on Amazon, not hiring a plumber. Bidding on those spends money against e-commerce intent. They are **not** the workaround.

**Finding 2 — the genuine service-intent, installable cluster:**

| Keyword | Monthly vol | Competition | Top-of-page bid |
|---|---:|---|---|
| whole house water filter / filtration (system) | 880 | HIGH | $3.41–$11.32 |
| water softener | 480 | HIGH | $2.96–$8.62 |
| **hard water softener / system** | **480** | **MEDIUM** | **low/no bid data** |
| **water softener for hard water** | **480** | **MEDIUM** | **low/no bid data** |
| water softener system | 320 | HIGH | $3.27–$10.94 |

**Finding 3 — this is genuinely cheaper than core plumbing.** Water-softener top-of-page bids run **$3–$11**. For comparison, the account's live **Nonbranded Plumbing campaign is paying a $3.10 avg CPC but on terms where it loses 83% of impression share to rank**, and mainstream emergency-plumbing terms bid far higher. Softener clicks are a fraction of the cost of "plumber near me" style terms.

**The actual workaround (what to bring back as "the possibilities"):**

1. **A dedicated water-treatment Search campaign** built on the softener/treatment cluster (~1,600 service-intent searches/mo), **not** the retail filter terms. Tight match types, negatives for `brita`, `berkey`, `pitcher`, `countertop`, `refrigerator`, `replacement cartridge` — those are shoppers, not leads.
2. **Lean on the two MEDIUM-competition terms** — `hard water softener` and `water softener for hard water` (480/mo each). Medium competition in a HIGH-competition category is the seam. Cheaper clicks, and San Antonio has famously hard water, so local intent is real.
3. **Frame it as a wedge, not a pillar.** It's ~1,600 qualified searches/month vs 4,500+ for AC repair alone. It won't replace plumbing volume — it captures cheaper, high-ticket install leads (a softener install is a $2–5k job) that the expensive core-plumbing terms price you out of. That is exactly the "work around the expensive keywords" Jonathan asked about.
4. **The account already has a `Water Softening Equipment` campaign** (currently paused, spent $601 historically). This is a re-activation and re-scope, not a build from zero.

---

## Status of all four commitments

| Commitment | Status |
|---|---|
| Historical spend pull (was Problem Solvers' budget higher?) | **Done** — `budget-analysis-2025-2026.md` + chart |
| Google deck: LSA-to-PPC connection doesn't matter | **Done** — confirmed on the June 29 call, recorded in §6 of the review |
| Good/better/best budget brackets + AC strategy + past-PPC review | **Done** — this doc (§1–2) + past-PPC in the review |
| Water treatment / softener keyword research | **Done** — this doc (§3) |

**Open dependency across all of it:** the conversion-tracking fix. The budget brackets assume the account can measure a lead again — spending toward BETTER/BEST only makes sense once the signal is back, otherwise smart bidding scales on noise.
