# TSD Paid guardrails log

Account-wide settings TSD keeps off across current client accounts (MCC 4155514468). Newest entry on top.

---

## 2026-10-21 — UI-only auto-apply turned off (Edu, via the browser extension)

Edu turned off auto-apply in the Google Ads UI on the 4 accounts the API couldn't change. Read-back with `ai_max_auto_apply_off_1016.py` (validate only): All Seasons 4467722415, Integrate Comfort 4571881760 and ICS LSA Bellevue 2895702982 are clean. Napps 9509605037 still lists 1 UNKNOWN subscription as ENABLED in the API, but the UI says "Auto-apply is on for 0 recommendation types". It was created 2024-04-24 and never modified (the other 3 UNKNOWN were paused 2025-03-11). That makes it a retired type with no UI toggle, so it's treated as off. **The audit script will keep flagging it. Ignore that one for Napps.** fu-049 and fu-061 closed.

---

## 2026-10-16 — AI Max OFF + auto-apply PAUSED on all current clients. APPLIED

**Ask (Edu):** "can you deactivate AI Max in GENERAL and any autoapply shit we have?"

**Why:** the 10-16 campaign checks showed AI Max / broad automation buying junk: Proud Pops Search Electrical's AI Max matches cost $3,622 (Sep 15–Oct 8) incl. plumbing searches and "goodman phone number"; All Seasons' auto-apply had added 156 broad keywords on 10-11.

**Changed (`ai_max_auto_apply_off_1016.py`, validated first, read-back clean on every account):**
- **AI Max OFF on 67 Search campaigns** (paused ones too, so re-enabling a campaign doesn't bring AI Max back). Live campaigns affected (7): All Seasons `TSD_Search_LeadGen`, Hawkins `TSD_03.16_Search_Branded_Evergreen`, King's `TSD_28.04_Search_Nonbranded_Evergreen`, Napps `TSD_03.22_Search_Branded_Evergreen`, Neon Monkey `TSD_08.05_Leads_Search_Nonbranded_Trimming`, Zen Air `A/C Service (Lead Gen) … Max Conversions` + `Lead Gen Campaign (2024)`. In the same operation, AI Max text customization (TEXT_ASSET_AUTOMATION) and final URL expansion were opted out (the API refuses AI Max off while they're on: `AI_MAX_MUST_BE_ENABLED`).
- **7 auto-apply subscriptions PAUSED:** Integrate Comfort 4571881760 (TARGET_CPA_OPT_IN, MAXIMIZE_CONVERSIONS_OPT_IN, OPTIMIZE_AD_ROTATION, RAISE_TARGET_CPA, RESPONSIVE_SEARCH_AD_IMPROVE_AD_STRENGTH, SET_TARGET_CPA) + ICS LSA Bellevue 2895702982 (OPTIMIZE_AD_ROTATION).
- Accounts covered: All Seasons (+LSA), C&S, Cool Hand, Hawkins, Integrate Comfort (+3 LSA), King's, Lilypad, Mission Accomplished (+LSA), Napps (+LSA), Neon Monkey (+LSA), Nick's, Proud Pops (+2 LSA), Spencer, Watt's Right (Tulsa + Broken Arrow), Zen Air (+LSA), Golden Plumbing, TopServ own account.

**Not done:**
- **UI only:** 13 auto-apply subscriptions of type UNKNOWN, which the API can't change: All Seasons 7 (also fu-049), Integrate Comfort 4, ICS LSA Bellevue 1, Napps 1. Turn off in Google Ads → Recommendations → Auto-apply.
- **Left out, offboarded (Edu 10-16: nothing needed):** All Heart 9205826499 (offboarded; 13 AI Max incl. 1 live), Strickland 9049508615 (On Purpose Media; 2 paused), DFW _Unsuspended 1932181525 (15 paused), Gray Duct 6191956550 (1 paused), Bucksworth HVAC 4072088295 (21 auto-apply types), Bucksworth Weed 7024049980 (2).
- PMax final URL expansion is a separate setting, still ON in live PMax at C&S (2), Hawkins, My Favorite Service Co, Nick's, Watt's Right. Not part of this ask.

**Expect:** possible volume dip on the 7 live campaigns (no more AI Max query expansion). Watch search terms + conversions in each client's next weekly pass. To audit again: `paid/guardrails/ai_max_auto_apply_off_1016.py` without `--apply` lists anything still ON.
