# Neon Monkey — Google Ads check (2026-10-08)

PPC `7953905280` + LSA `1219885876`. Pulled via `tsd.sh` (`neon_monkey_check_1008.py`, `neon_monkey_lsa_1008.py`).
Nothing changed in the account. Recommendations below are staged for Edu's decision.

## 7-day snapshot (Oct 1–7, PPC only)

| | Spend | Clicks | CPC | Leads | CPL |
|---|---|---|---|---|---|
| Account | $1,941 | 335 | $5.79 | 5 | $388 |
| Branded Search | $105 | 7 | $14.97 | 0 | — |
| Unbranded (NB Trimming + PMax) | $1,836 | 328 | $5.60 | 5 | $367 |
| ↳ NB Trimming | $1,124 | 38 | $29.57 | 1 | $1,124 |
| ↳ PMax | $713 | 290 | $2.46 | 4 | $178 |

Conv rate 1.16%. Search IS 32%. Leads = Calls from ads (3) + GA4 `ghl_contact_us` (2); `contact_us` junk is
already out of the column (08-31 fix), so these are clean.

30 days: $8,430 / 32 leads / **$263 CPL**. PMax $205, NB $307, Branded $549 (1 lead).

## Findings
1. **NB Trimming CPC up ~50%.** Weekly CPC was $19–22 in August; it has been $29–34 since mid-September, on
   Maximize Conversions with no target and no CPC cap. Clicks fell from ~50/wk to ~32/wk at the same ~$1,050/wk.
   Since the 08-31 cleanup it gets ~3 leads/wk, not enough data for Max Conv to bid well.
   Worst clicks last 7d: "tree trimming dallas" **$210 for 1 click**, "tree trimming services in my area" $124/1.
   Top keyword "tree trimming service fort worth" [exact]: $1,866/30d at $35.88 CPC.
2. **New search-term leaks (not lawn):** Dallas, competitors (trugreen north richland hills $76, mercer tree
   service $49, jc tree service, blue ox), landscaping (legacy landscaping, landscaping fort worth), tree planting,
   plant removal.
3. **Lawn fix verified.** 0 "lawn" search terms on either Search campaign since 09-29.
4. **Branded overpaying.** 100% IS, ~40 imp/wk, yet $15–41 per brand click on Max Conv. "neon monkey" [phrase]
   $394/30d at $28 CPC. $549/30d for 1 lead.
5. **Spend above the documented cap.** Sept PPC = $8,356 vs the $6,930/mo cap in the 08-10 log; Oct pacing ~$10k.
   NB budget is $150/day (was $100 on 08-10); that change is older than the 30-day change history, so who made
   it is not visible. Only change in the last 30 days = Edu's 09-28 lawn negatives.
6. **LSA shrinking.** Budget still $214/day, ELIGIBLE, no changes in 30 days, but spend ~$600/wk (Jul–mid Aug)
   → ~$240/wk since (two $0 weeks). 30d: $898, 27 leads, 11 booked, ~$75 CPL. Still the cheapest lead source.
   Not budget-limited, so it's ranking or settings (hours, reviews, response rate, bid mode). Check the LSA
   dashboard. 3 leads are DECLINED but still charged; dispute them if out of area.
7. Geo: CORRECTION (same day) both Search campaigns already target a 36-location West FW list (Presence),
   applied before 09-09. PMax (5 circles, PRESENCE_OR_INTEREST) and LSA are the ones still on the old geo.
   Full plan: `action-plan-2026-10-08.md`.

## Staged recommendations (not applied)
- NB Trimming: move off uncapped Max Conv to Maximize Clicks with a ~$20 max CPC cap (or Manual CPC).
- Negatives on NB (phrase): dallas, trugreen, mercer, jc tree, blue ox, landscaping, planting.
- Branded: Manual CPC or Target IS (absolute top) with a ~$5 cap.
- Confirm the approved monthly budget with the AM before October closes.
- LSA: dashboard review + dispute the 3 charged declines.
