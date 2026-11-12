# Neon Monkey — Google Ads change log (PPC 7953905280)

## 2026-11-02 — PMax 2-week test: call length, utility-company negatives, brand exclusions (APPLIED)
Approved: Edu in chat ("Can you work on those 3 to-dos?"). Why: 6 first-time 60s+ PMax ad calls Oct 19-Nov 1 transcribed, only 2 real (142s, 161s); 3 wrong-company (Davey Tree, Asplundh/Oncor, plant nursery, 63-73s) + 1 out of range, all counted as 'Calls from ads' conversions. Findings: `one-week-check-2026-10-19.md` RECHECK 2026-11-02 + CORRECTION, `call-wins-log.md`. Script `scripts/neon_monkey_apply_1102.py` (validated, applied, read back). Budgets unchanged.
1. 'Calls from ads' 833426830 (AD_CALL, primary): minimum call length 60s → 90s. Account-wide, so NB + Branded too. ~25s of every call is the phone menu + connecting, so 90s ≈ a minute of real conversation.
2. Phrase negatives davey, asplundh, oncor, utility, fertilizer on PMax 21225221220 (now 66) and NB 23825900343 (now 17). 30-day NB replay: 0 terms blocked (these come through PMax, not NB).
3. New brand list 'TSD | Utility tree companies' (shared set 12300954509: Davey Tree Expert Company, Asplundh Tree Expert Company, Oncor Electric Delivery) excluded on PMax (negative BRAND_LIST campaign criterion; CampaignSharedSet is rejected for PMax).
Expect: fewer counted PMax conversions short term (junk calls no longer count), possible learning dip. Checkpoint 2026-11-16 (Command Center): pause PMax unless ≥3 real calls (transcribed) at ≤~$200/lead in Nov 2-15.

## 2026-10-26 — Fixes from the one-week recheck (APPLIED)
Approved: Edu in chat ("Yes, apply 1 to 3"). Findings: `one-week-check-2026-10-19.md`, RECHECK 2026-10-26. Script `scripts/neon_monkey_apply_1026.py` (validated, then applied), read back with `neon_monkey_readback_1026.py`. Budgets unchanged.
1. NB Trimming 23825900343: PHRASE "remove tree stump from yard" PAUSED (EXACT kept). Campaign negatives added: PHRASE rental, rent, how to, diy, chemical, jack, vs, remover + EXACT stump grinder. Why: 67% of term spend 10-20..25 was DIY/rental stump searches, 0 real calls. $20 cap kept.
2. Branded ad group 193951349406: max CPC $5 -> $6 (IS 57%, under the 90% rule).
3. PMax 21225221220 (Phase 4): positive geo now = the same 36 West FW locations as NB; negatives Arlington, Dallas, Grand Prairie, Irving (TX); Fort Worth city + the 5 radius circles (20/17/5/5/5 mi) removed. Presence-only stays. Expect lower PMax spend (whole-city Fort Worth was its biggest geo).
Recheck ~11-02 (Command Center fu-094): NB real calls + junk terms, Branded IS, PMax spend/calls on the narrower geo.

## 2026-10-20 — "The Tree Place" negatives (APPLIED)
Ask: Angela (Slack DM 10-20 16:42 BRT), "please add The Tree Place as a negative keyword".
Before: no negative containing "tree place" anywhere (campaign, ad group, shared lists CSMS_Negatives / Competitos May).
90d cost (07-20..10-20): "the tree place" 1 clk $13.13 + "the tree place in fort worth" 2 clk $67.43 = $80.56, all on TSD_08.05_Leads_Search_Nonbranded_Trimming.
Applied: PHRASE negatives `tree place` + `treeplace` at campaign level on the 3 ENABLED campaigns (NB Trimming 23825900343, PMax Evergreen 21225221220, Branded Mix 23739724064). Script `scripts/nm_neg_treeplace_1020.py`, read back via `nm_neg_check_1020.py`.
