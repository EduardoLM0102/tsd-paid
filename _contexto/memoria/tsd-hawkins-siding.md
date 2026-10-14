---
name: tsd-hawkins-siding
description: Hawkins Siding and Exterior (TSD) account IDs, Meta going dark since 2026-08-20, and the 2026-08-31 Google Ads Nonbranded Search ad group restructure
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0c7367ff-a084-48ad-94ff-8899b92d635f
  modified: 2026-08-31T14:09:13.235Z
---

**Client:** Hawkins Siding and Exterior (TopServ Digital, Dallas metro/Lewisville TX, siding/exterior only — window/door discontinued 2026-07). Full history in `topserv-workspace/clients/hawkins-siding/`.

**Accounts:**
- Google Ads customer ID `2198608170` (MCC Topservdigital `4155514468`)
- Meta ad account `10086442468052740` ("Hawkins Siding Ads", business `hawkinssidingandexteriors`)

**Awareness campaign video assets:** https://drive.google.com/drive/folders/186DH4KLn3IWM04qToXmvaPTvVq2CxfJa
**Why:** Edu flagged this folder (2026-08-10) as the source videos for an upcoming Meta awareness campaign on this account.
**How to apply:** When building/launching the Hawkins awareness campaign, pull creative from this folder first before asking Edu for assets. See [[tsd-meta-ads-methodology]] for the always-on Awareness / Ad Recall Lift doctrine this campaign should follow.

**2026-08-31 findings + changes:**
- **Meta is dark**: all 9 campaigns PAUSED since 2026-08-20, including the awareness campaign built from the Drive folder above (`TSD_2026-08_TOF_AWARENESS_CBO_Siding - Ad Recall Lift`) — it exists but shows $0 spend ever, so it was never actually launched. The one campaign that carried all historical Meta spend (`Lead Gen | Siding/Promos | DFW | Jul 2026`, $47.78 CPL) also went quiet on the same date. Needs a decision from Edu on whether to relaunch.
- **Google Ads Branded campaign** (`TSD_03.16_Search_Branded_Evergreen`, id 23233882685) is technically ELIGIBLE/SERVING but gets ~0 impressions — root cause is genuinely thin brand search volume (708 impressions total over 8 months), not a technical fault. Not worth fixing with budget/bids.
- **Nonbranded Search campaign** (`TSD_04.29_Leads_Nonbranded_Evergreen`, id 23805382277) restructured: pruned 19 zero-impression keywords in the old single "Siding" ad group (now renamed "Siding - General", 12 keywords left) and split proven keywords into 3 new themed ad groups with dedicated RSAs — "Siding Replacement" (202830041434), "Siding Repair" (200448960715), "Vinyl Siding" (199267778626). Goal: fix the 60%+ rank-lost impression share by improving ad relevance/QS per theme. Check back ~2026-09-10 once new ad groups have real serving data.
- Also found and archived (renamed, left PAUSED, not deleted — ad group REMOVED is blocked by the local auto-mode classifier as an irreversible action) two dead ad groups for the discontinued window/door line: "ARCHIVED - Window Replacement" (196112762557, had a broken duplicated final URL) and "ARCHIVED - Doors" (197090787018).
- PMax (`TSD_Pmax_Siding`, id 21291552209) converts cheaper than Search (~$48 CPL over 30d) and is budget-constrained (~25% IS lost to budget, not rank) — a good candidate for a budget increase, not yet actioned.

**2026-10-05 weekly pass (AT task closed):** $60.54 CPL, 9 leads (6 calls from ads, 3 forms). 13 NB negatives (handyman, angi, grants, senior citizens, how to, where to buy/purchase, norandex, qxo, building a house PHRASE; construction company/ies EXACT). Competitor names CONVERT here (bee builders, hometown building center, homeland vinyl), don't blanket-block. PMax $29 vs NB $76 CPL, PMax $13/d budget-limited: reallocation still the main lever.
**2026-10-05 budget shift (Edu approved, constant total $93/d):** NB 23805382277 $80→$75/d, PMax 21291552209 $13→$18/d. ⚑ Recheck ~10-12: PMax spending full $18 and holding ~$29 CPL? If yes consider another step, if CPL jumps roll back to $13.

**10-13 weekly pass:** 10-05 shift held (PMax full $18, $22.50 CPL) but 92% of PMax spend = YouTube. **Brand leak:** Branded 23233882685 got 1 impression in 30d (Max Conv + $25 tCPA, no history → doesn't bid); Nonbranded broad buys 'hawkins siding' ($148.50/30d, up to $57/click). Staged (fu-044): PMax $18→$23 / NB $75→$70, 'hawkins' phrase negative on NB + Branded to Manual CPC ~$5 together.
**10-14 APPLIED (Edu's go), `hawkins_apply_1014.py`:** PMax $18→$23/d, NB $75→$70/d; Branded → Manual CPC, ad group bid $5 (was $0.01); NB phrase negatives hawkins / charities / in stock. ⚑ Recheck ~10-21 (fu-050): Branded IS on brand terms, PMax CPL at $23.
