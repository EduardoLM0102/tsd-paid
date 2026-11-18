# Neon Monkey — Google Ads change log (PPC 7953905280)

## 2026-11-16 — fu-115 PMax checkpoint: FAILED, PMax PAUSED (rule set 11-02, Edu's go)

**Rule (11-02):** keep PMax only if Nov 2-15 brings >= 3 real transcribed calls at <= ~$200/lead. Pull: scratchpad `nm_pmax.py` + `nm_clicks.py` (gclid -> click_view), CallRail via call-wins `pull_calls.py` (no CallRail transcription on this account, local whisper).

**PMax 21225221220, 11-02..11-15:** $1,743.12 / 716 clicks / 2 primary conv ('Phone Call') / 17 all (GA4 contact_us 8, call-button taps 7). By network: Search $1,175 (67%), Search partners $236, YouTube $168 (10%, was 35% on 10-27..11-01), Content $139, Discover $25. 8 call-asset calls in call_view, none reached the 90s minimum, 2 reached 60s (11-05 67s palm wrapping, 11-14 71s).
**Ad calls (CallRail, all 11 gclid calls in the window trace to PMax Search; NB brought none):** 11-02 09:18 51s no recording; 11-02 16:52 wrong company (Gecko Green); 11-03 08:06 IVR; **11-03 13:47 113s real (tree transplant, open)**; 11-03 19:45 1s; 11-05 08:05 IVR; 11-05 09:24 68s palm wrapping, not a fit; 11-05 13:52 IVR; 11-06 13:34 IVR; 11-07 20:02 after hours; 11-11 11:41 43s wrong number; 11-11 13:58 10s IVR; 11-12 13:10 18s LSA IVR; **11-12 16:18 157s real (Tonya J., Arlington, trimming 3 trees, Kip to call back)**; **11-14 08:58 Sat 71s real request left on voicemail (trimming bid)** (transcripts finished after the pause, call-wins-log.md). **Real calls: 3** (11-03, 11-12, 11-14) on $1,743 = **$581 each**: the count met the rule, the cost is 3x the $200 limit. 2 of the 3 came in the last 4 days, so call quality improved at the tail after the 11-02 fixes; the cost did not. YouTube share fell as hoped, Search junk didn't turn into leads.
**Rest of the account:** NB Trimming paused 11-11 ($365.77 / 19 clicks / 0 conv in the window before that). Branded $9.41 / 2 clicks / 13 impressions in 14 days: there is almost no brand search demand.

**APPLIED 14:25 UTC (`nm_pmax_pause_1116.py`, validate-only then --apply):** PMax 21225221220 ENABLED -> PAUSED, read-back PAUSED. Google PPC now = Branded only (~$1/day); LSA 1219885876 runs separately (~$30-40/day). November PPC lands ~$2.6k vs the $6,930 cap.
**Google Search has now failed twice on this account** (NB 3 weeks / 0 real leads; PMax 2-week test / <=3 real calls on $1,743). Per the 11-11 plan item 4, the reallocation question in the 11-12 AM note (Meta Tree Wellness form restart, Holiday Lights form, does the cap cover Facebook) now covers ~$150/day, not ~$44. Nothing moves until Brock answers (new Meta spend = written approval). **AM note = AT Internal Request DRAFT `d2878945-41c4-419e-bfff-a2e8fbd0136e`** "Google Ads update: Performance Max paused, Google now brand-only" (https://app.agencytitan.com/tasks/instance/d2878945-41c4-419e-bfff-a2e8fbd0136e), created via API 14:40 UTC, left in Intake for Edu to submit: PMax pause + numbers, Google = Branded + LSA, the Nov 13 email to Brock now decides ~$150/day (chase him, holiday lights close ~12-10), Ray Martinez / Valerie Fox booked?, next read 11-23. Command Center fu-173.
**AT status 11-16:** the 11-12 note 793d6686 is at Review & Close with Edu; Angela's only comment: "email sent to Brock on 11/13/2026" (task update "shared feedback with Eduardo"). No answer from Brock on record, so the reallocation is still open. The phone-menu note f5d99155 (11-11) sits in Execution with Angela, no update since. All 11 CallRail gclid calls in the window map to PMax SEARCH clicks via click_view (`nm_clicks.py`): NB brought none.

---

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
