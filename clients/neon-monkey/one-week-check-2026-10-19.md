# Neon Monkey: One-week check (2026-10-19)

Read-only. Nothing changed in Google Ads, GTM or GA4. Script: `.claude/skills/google-ads-ratos/scripts/neon_monkey_check_1019.py` (Ads via tsd.sh; GA4 via gtm.sh).

## Tracking is back and recording
- GA4 `328458299`, neonmonkeytree.com sessions: 10-13 23 (partial), 10-14 65, 10-15 83, 10-16 60, 10-17 55, 10-18 (Sun) 14. Back in the 40-80/day weekday norm.
- Google Ads conversions recorded since 10-13: Calls from ads 7 (10-10 to 10-15), `Phone Call` upload 1 (10-14, the CallRail upload resumed), `Submit lead form - web` 1 (10-17), GA4 `contact_us` 8 (10-14 to 10-16, non-biddable), GA4 `ghl_contact_us` 1 (10-17, biddable), `[TSD] Click to call` 1 (10-16, shows biddable 0).
- Not confirmed: whether these are real leads or tests. No clean "test form + test call" marker, so the end-to-end test is still owed.

## Last 7 days (10-12 to 10-18), by campaign
| Campaign | Cost | Clicks | Avg CPC | Conv (biddable) | Note |
|---|---:|---:|---:|---:|---|
| PMax | $714 | 211 | $3.39 | 5 (15 all) | Search IS 24% |
| Branded | $142 | 5 | $28.39 | 1 | IS 100% |
| Nonbranded Trimming | $771 | 34 | $22.68 | 2 | IS 35%; was $29-34 CPC mid-Sept |

NB search terms since 10-13 are clean of competitors, landscaping and Dallas. Only stray: "tree service granbury" ($64, 2 clicks), "yardwork near me" ($57), "stump grinder rental" ($19), "hedge trimming" ($14).

## Still not applied (plan Phases 3 and 4)
- All three campaigns are still Maximize Conversions. NB has no CPC cap; Branded is still at ~$28-34 per click with 100% IS.
- PMax geo not checked in this pass.
- `[TSD] Click to call` `7835384828` is still CLICK_TO_CALL / PHONE_CALL_LEAD / primary. Only 1 tap so far, so recategorizing to CONTACT is still clean. Needs Edu's OK. Creator of v11 still unknown.

## Needs a decision
1. Apply Phase 3 now that tracking is verified: NB to Maximize Clicks, max CPC $20, keep $150/day; Branded to Manual CPC $5.
2. Recategorize `[TSD] Click to call` to CONTACT.
3. Tell Angela before PMax goes Presence-only (PMax conversions will drop).

## APPLIED 2026-10-19 (Edu's OK in chat; script `neon_monkey_apply_1019.py`, read back with `neon_monkey_readback_1019.py`)
- Nonbranded Trimming `23825900343`: Maximize Conversions -> Maximize Clicks (TARGET_SPEND), max CPC $20. Budget $150/day unchanged.
- Branded `23739724064`: Maximize Conversions -> Manual CPC; ad group `193951349406` max CPC $0.01 -> $5 (no keyword-level bids).
- `[TSD] Click to call` `7835384828`: category PHONE_CALL_LEAD -> CONTACT (still primary_for_goal, no longer in a biddable goal on the Search campaigns).
- PMax `21225221220`: positive geo PRESENCE_OR_INTEREST -> PRESENCE. Locations list unchanged (20/17/5/5/5 mi circles + Fort Worth). Still owed: swap the circles for the Search West FW list, add Dallas/Grand Prairie/Arlington/Irving exclusions, copy negatives into PMax (Phase 4 steps 2-4).
- Not sent: nothing to Angela yet (PMax conversions will drop; Edu to tell her).
- Recheck 2026-10-26: calls + forms per $1,000 vs prior 30 days; Branded IS must stay >= 90% (else raise cap $1 at a time); NB close-variant junk.

## RECHECK 2026-10-26 (fu-063). Read-only, nothing changed
Script `.claude/skills/google-ads-ratos/scripts/neon_monkey_recheck_1026.py` (+ CallRail company COM601166…, account ACC319477…; `.env.callrail`'s numeric account id 400s on this company, use the ACC id). Raw output kept out of the repo.
Windows: prior 30 = 09-19..10-18 (site tag dead until 10-13, so forms undercounted there), pre = 10-13..10-18 (tag back, old bidding), post = 10-20..10-25 (6 full days after the 10-19 changes).

**Account: calls + forms per $1,000.** Real call = CallRail source Google Ads, 60s+. Form = `ghl_contact_us`.
| Window | Spend | Real calls | Forms | Per $1k | $ per real call |
|---|---:|---:|---:|---:|---:|
| Prior 30 | $7,851 | 28 | 5 | 4.2 | $280 |
| Pre (6d) | $1,225 | 5 | 1 | 4.9 | $245 |
| Post (6d) | $1,119 | 3 | 2 | 4.5 | $373 |
Spend down from ~$262/d (prior 30) to ~$187/d. Lead rate per $1k about flat, but post = 5 leads total, too small to call.

**Nonbranded Trimming (Max Clicks $20 cap).** $509, 26 clicks, CPC $19.56 (was $29.31 prior 30), IS 53% (was 38%), budget-lost 0% (was 25%). Spends ~$85/d of $150 because every click sits at the cap (rank-lost 47%). **0 real calls post** (prior: 10 on $3,541; pre: 2 on $533). Its only conversions (10-25: 1 form + 1 tap, plus a 15s call) came from "tree stump remover rental" / keyword "remove tree stump from yard". **Junk: 67% of visible term spend ($236 of $351) matched the phrase keyword "remove tree stump from yard"** → stump grinder rental, how to remove, farm jack, stump removal chemical, removal vs grinding. NB has only 3 campaign negatives and no shared lists attached to any enabled campaign.

**Branded (Manual CPC $5).** $9 in 6 days (was $673 / 30d, ~$22/d), CPC ~$4.45. IS 57%, abs-top 29%, rank-lost 43%, **below the 90% rule**. But brand demand is tiny (22 impressions in 13 days, all real "neon monkey…" terms), so 43% = ~3 impressions.

**PMax (Presence only).** $601 vs $590 pre, clicks 118 vs 189, CPC $5.09 vs $3.12. Real calls 3 vs 3, forms 1 vs 1, biddable conv 4 vs 4. Only non-biddable GA4 `contact_us` fell (8 → 2), which is what reports will show as the "drop". Geo is now 100% presence. Still east of target: Irving $56, Arlington $29, Grand Prairie $3 (~$87, 14%) + Euless/Hurst/NRH ~$57. Search IS 24%, budget-lost 25%. 3 junk PMax calls 10-24 (0-11s). Circles still 20/17/5/5/5 mi + Fort Worth; 62 negatives on PMax.

**Proposed (needs Edu's go, total budget unchanged):**
1. NB: pause phrase "remove tree stump from yard"; add phrase negatives rental, rent, how to, diy, chemical, jack, vs, remover + exact "stump grinder". Keep "stump grinding". Don't raise the $20 cap until NB books a real call.
2. Branded: cap $5 → $6 (the $1-step rule), recheck in a week.
3. PMax Phase 4: swap circles for the Search West FW list, exclude Dallas/Grand Prairie/Arlington/Irving.
4. Edu → Angela: real calls from PMax held; only a GA4 contact event dropped.

## RECHECK 2026-11-02 (fu-094) + Phase 8 re-baseline (fu-029). Read-only, nothing changed
Script `.claude/skills/google-ads-ratos/scripts/neon_monkey_recheck_1102.py` + CallRail (ACC319477…/COM601166…) + LSA 1219885876. Windows: pre = 10-20..10-25, post = 10-27..11-01 (6 full days after the 10-26 changes), Phase 8 = 10-19..11-01 (14 days).

**NB Trimming (Max Clicks $20).** Post $272, 14 clicks, CPC $19.46, 0 conversions, 0 ad calls. The stump junk is gone: only 7 visible terms, all tree service (tree trimming near me / fort worth, tree removal, tree service near me) plus 2 competitors (four seasons arbor service, wright tree service fort worth). Spends ~$45/d of $150 (IS 56%, rank-lost 44%, every click at the cap). Phase 8: $858, 1 form (10-25, the stump-rental term, junk), 0 real calls in 14 days.

**Branded ($6 cap).** Basically no brand searches: 0 spend 10-27..11-01, 1 impression on 10-28. Phase 8 $19. The IS % is noise at this volume. Nothing to do.

**PMax (West FW list, presence only).** Geo fix worked: post spend is all inside the list (Fort Worth $207, Hudson Oaks $107, Benbrook $98, Azle $66...), Irving/Arlington/GP gone. **But money moved to YouTube:** YouTube $22 (4%) pre → $189 (35%) post, 603 clicks, 0 conv. Search part $347 / 4 conv (pre Search + partners $571 / 4), so the Search side got more efficient. Narrower geo = less Search inventory, PMax fills the budget with YouTube. Budget-lost IS 39%.

**Real calls (CallRail, source Google Ads).** Pre: 3 new 60s+ (10-20 73s, 10-21 63s, 10-22 72s) + 3 junk 10-24. Post: 1 new 60s+ (10-29 161s, Glendale), 1 repeat 124s (10-27), 2 website-pool calls with gclid from repeat callers (10-29 194s, 270s; these are PMax's 2 'Phone Call' upload conv), 2 junk (8s, 23s). 11-02 so far: 1 call 51s. New-customer calls 3 → 1.

**Phase 8 re-baseline, 10-19..11-01 (14 days).**
| Channel | Spend | Leads | Per lead |
|---|---:|---|---:|
| PMax | $1,455 | ~6 new 60s+ ad calls + 3 forms | ~$160 |
| NB Trimming | $858 | 0 real (1 junk form) | n/a |
| Branded | $19 | 0 | n/a |
| LSA | $778 | 13 leads, 10 marked BOOKED, 11 charged | ~$78 per booked |
PPC = $2,332 / 14d ≈ $167/day ≈ $5.1k/month, already under the $6,930 cap (NB underspends its $150 budget by ~$90/d). LSA is the best channel by far.

**Side flag (not paid):** 10-26..10-28 a wave of ~35 first-time Google My Business calls, almost all exactly 56-57s, from scattered towns (Cleburne, Glendale, Grapevine, Azle, Weatherford...). Same length every time = probably the IVR menu loop (see AT card 3442f6b5) or robocalls. Worth a look by whoever owns GBP/phones.

**For Edu to decide:**
1. NB: 2 weeks, $858, 0 real leads even with clean terms. Options: add competitor negatives 'four seasons' + 'wright tree' and give it one more week, or pause NB and let the account run on PMax + LSA. Moving NB money to LSA won't spend: LSA already has a $214/d budget and spends ~$55/d.
2. PMax YouTube: $189/6d with 0 conv. Watch one more week, or widen the geo a little (more Search inventory) instead of letting PMax fill with YouTube.
3. November budget: hold the $6,930 cap. Current pace (~$5.1k PPC) is under it, so nothing to ask Brock unless he wants more volume.

**CORRECTION 2026-11-02 (after transcribing the calls, see call-wins-log.md):** "60s+ from Google Ads" is NOT a real-lead filter here. Of the 6 first-time 60s+ PMax call-extension calls Oct 19-Nov 1, only 2 are real leads (10-26 fallen tree in 76116, 10-29 estimate in Crowley, both handed to Kip). 3 were wrong-company calls (Davey Tree, Asplundh/Oncor utility trimming, a plant nursery) and 1 out of range (DeSoto). The 10-26 recheck's "PMax real calls 3 vs 3" counted 10-20/21/22, which were all wrong-company calls, so "real calls held" is not supported. Real PMax read: pre 10-20..10-25 = 0 real calls, post 10-27..11-01 = 1 (10-29), plus 10-26. Phase 8 PMax ≈ $1,455 for 2 real calls + 3 forms (unverified) ≈ $290/lead. Do NOT send Angela the "real calls held" line.
Proposed (Edu's go): PMax + NB phrase negatives davey, asplundh, oncor, utility, fertilizer (not present today; PMax has 'nursery' + 'tree place' already).

## 2026-11-04 — Edu's decisions on the 11-02 recheck (fu-029)

Edu: "Let's add the negatives and wait another week. Regarding the budget, ok, and no note for Angela needed."
- **APPLIED** (`clients/neon-monkey/nm_nb_negs_1104.py`, validate-only then `--apply`, read-back OK): PHRASE negatives **four seasons**, **wright tree**
  on NB Trimming 23825900343. 30d replay: 4 terms, $59.08, 0 conv, no keyword conflicts. Budget $150 and $20 cap unchanged.
- **NB gets one more week**: kill-or-keep read 11-11 (fu-122). Pause if still 0 real leads (transcribe any 60s+ call before counting it).
- **November budget:** hold the $6,930 cap, nothing to ask Brock.
- **No note to Angela** (the "PMax real calls held" line is dropped for good).
- PMax YouTube watch stays with the 11-16 checkpoint (fu-115).

## 2026-11-11 — fu-122: NB Trimming PAUSED + reallocation plan

**APPLIED 2026-11-11 06:06 CT (Edu's go):** NB Trimming 23825900343 → PAUSED (`nm_nb_pause_1111.py`, read-back PAUSED). Budget $150 and $20 cap left as they are.
Why: 11-04..11-10 $306 / 16 clicks / 0 calls / 0 forms / 0 all_conversions, no CallRail gclid from an NB click. 3 weeks ≈ $1,164, 0 real leads. All 9 ad calls that week transcribed (call-wins-log.md): 0 new real leads account-wide, 6 of 9 IVR/after-hours only.

**What was actually freed:** NB spent ~$44/day, not $150. ≈ $840 for the rest of November, ≈ $1,340/month after.
**November pacing without NB:** PPC MTD $1,438.54 (11-01..11-10) + ~$107/day (PMax ~$106, Branded ~$1) ≈ **$3.6k vs the $6,930 cap**. LSA separate ($41/day).

**Where it could go (`realloc_options_2026-11-11.py` + Meta MCP):**
| Option | Can it absorb? | Evidence | Verdict |
|---|---|---|---|
| PMax (budget $110) | Yes, 29% lost to budget | 0 real calls 11-04..11-10 on $770; checkpoint fu-115 11-16 | No, not before 11-16 |
| Branded | No (~$0.67/day, almost no brand searches) | | No |
| LSA (budget $214) | No, spends $41/day, reach-limited | 24 leads / 17 marked booked in 30d (~$72/booked) | Fix reach (geo/ranking), not budget |
| Google Holiday Lighting 18787352551 | Yes | Nov 2023 $1,207 / 32 conv; Oct–Nov 2024 $1,555 / 9 conv. Ads point to old domain, 2 disapproved, Display+partners ON, Manual CPC; **site has no holiday lighting page** | Not on Google this late |
| Google Leaf Cleanup 19146431184 | Yes | Dec–Jan only historically, weak; no page | No |
| **Meta Tree Wellness Check instant form** 120251344730960755 | Yes | 08-13..09-15: **$3,344 / 111 form leads / $30.13**; paused 09-15 (who/why unknown); lead quality never checked | **Best candidate**, after Angela |
| **Meta Holiday Lights instant form** 120200265744190755 | Yes, until ~12-10 | 2023: $957 / 47 leads / $20.37 | Good, only if Brock offers it this year |
| Meta awareness ARL 120251667360150755 (TSD, built 09-03, $20/d) | Yes | 0 impressions ever (never delivered) | Brandformance layer, low cost |

Instant forms also skip the phone menu, which ate 6 of 9 ad calls this week.

**Plan:**
1. **Now:** nothing moves inside Google. The ~$44/day stays unspent until the 11-16 PMax checkpoint (fu-115).
2. **Angela (one note, with the IVR + bamboo items):** (a) did the 111 Tree Wellness Check leads turn into jobs, and who paused it on 09-15? (b) holiday lighting this season, with crew capacity? (c) is Meta in TSD's scope, and does the $6,930 cap cover Meta or only Google? Meta spend outside the Google cap = new budget → written approval.
3. **If yes:** Meta CBO, NB's ~$44/day to start (~$1,340/mo): Tree Wellness Check form ~$30/day + Holiday Lights form ~$15/day until 12-10 (then into Tree Wellness), plus the ARL awareness ad set at $20/day if the cap allows. Doctrine: CBO, one angle = one DCT ad set.
4. **11-16:** if PMax fails its checkpoint too, Google Search has failed here twice over → bigger reallocation (PMax $110/day too) toward Meta + LSA reach, same note path.

**2026-11-11 (later): AM note on the phone menu DRAFTED** in Agency Titan, Internal Request `f5d99155-7bcd-40db-a1d4-1f2f0b956c8f` "Calls from ads are getting lost in the phone menu" (client Neon Monkey Tree Services 944a8139, Intake = Edu, Execution = Angela, Review & Close = Edu, department Account Management/Customer Success). Left in Intake: Edu reviews, picks the Execution department and clicks Submit Request. Content: all ad numbers ring 800-315-2374, menu with no default; Nov 4–10 6 of 9 ad calls never reached a person (4 new in-area callers in business hours, 2 from LSA); 24 of 59 since Oct 1; CallRail shows them as answered; fix = ad numbers straight to a person or a default to the representative option. Phone menu only: NB pause, bamboo lead and Meta questions are still open in fu-149. ⚠ AT client record's assigned user is 6142e4bb (not Angela); assigned Execution to Angela per Edu.

**2026-11-11 (later 2): Meta history checked.** Edu confirmed Meta 705877631084699 is TSD's (we manage it).
- Tree Wellness Check instant form 120251344730960755: built + launched 08-13 by Manuel Lizarralde (11:41 / 14:20 CT). **Paused 09-15 16:04 CT by 'Jonathan Bannister' (Power Editor)**, one minute after Angela's DM to Edu (09-15 18:02 BRT): "Neon Monkey wants Facebook leads shut off for now", Edu: "let me do that right now". 'Jonathan Bannister' in the Meta log = Edu (Edu confirmed 11-11), so Edu paused it on the **client's request**, not as a performance call. Reason not in Slack.
- ARL awareness campaign 120251667360150755: created 09-03 by Manuel Lizarralde; its ad set '09/03/2026 - ZIP Codes | Broad' went Pending Process → Inactive at creation and was **never turned on**. No delivery ever.
- Not Gui: no Gui actor in the Meta log since 08-01 (actors: Manuel Lizarralde 72, Jonathan Bannister 1, Meta system).
Impact on the reallocation plan: Meta lead forms need the client's OK to restart (they asked to stop 09-15). Awareness ARL is not lead gen, but it is new Meta spend.

**2026-11-12: second AM note SUBMITTED by Edu** (AT Internal Request created via Cowork, Execution = Angela): NB pause FYI, bamboo follow-up gap, Facebook leads (why off 09-15, did the 111 leads become jobs, restart?), holiday lighting this season, whether the $6,930 cap covers Facebook. fu-149 closed; answers drive the Meta reallocation plan above.
