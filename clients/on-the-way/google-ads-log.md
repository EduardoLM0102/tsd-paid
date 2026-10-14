# On The Way AC Plumbing & Electric — Google Ads Log

Convention: newest entry on top. One entry per work session — researched → found → did → open items. See `clients/README.md`.

---

## 2026-10-05 — Client revoked TSD's Google Ads access (we lost visibility)

**What we found:** the weekly 7-day pull failed with "User doesn't have permission to access customer". The
`customer_client_link` from the TSD MCC (`4155514468`) to `3454686129` shows **INACTIVE**. Edu's login has no direct
access either (tried with the MCC and with the account itself as login-customer-id). It worked on 10-01 (session 8).
The MCC change history doesn't expose when or by whom the link was changed. **Edu confirmed: the client revoked the
access.**

**Effect:** no visibility into spend, leads, search terms or settings, and no way to make changes. Nothing promised in
the 10-01 AM reply (auto-apply off, Display off on Branded, Search Partners off, competitor negatives) was done before
the access went away.

**Agency Titan:** this week's 7-Day Google Search Ads task closed with a comment that we lost visibility. KPI entry
logged as $0 spend / 0 leads, Account Health "Unclear", with the same note.

### Open
- [ ] Any future work on this account needs the client to re-grant access (relink to MCC `4155514468`).
- [ ] The weekly 7-day tasks will keep generating for this client (next ~10-10) and will hit the same wall.

---

## 2026-10-01 (session 8) — Change-history audit (TSD vs client vs auto-apply), launch conversion goals, were the client's edits fixing a real leak, AM reply

Trigger: the client sent the Google Ads change history to the AM. Every recent change is theirs, the ones before are Auto-Apply, and the last manual TSD change is 09-09. They say they don't want recommendations used and want TSD to make all changes. AM asked for a valid explanation of the 3-week gap. Read-only session, no account changes.

**1. Who changed what (`change_event`, 09-02 → 10-01, 251 events):**
- **TSD** (`eduardo@topservdigital.com`, `GOOGLE_ADS_API`): 170 events, **all on 09-09** (sessions 2–6). Nothing from TSD since. The PMax-1 brand exclusion owed since session 4 was never added.
- **Recommendations Auto-Apply**: 33 events, 09-11 → 09-14.
  - 09-11: Branded Display ON (`target_content_network` false → true). NonBranded Manual CPC → Max Conversions (so the per-ad-group CPC ceilings no longer apply). PMax-2 tCPA $58.48 → $4.33 (PMax-2 is paused, so no effect).
  - 09-12: NonBranded Display ON.
  - 09-13: 5 BROAD brand keywords added to Branded (broad copies of our exact brand terms).
  - 09-14: NonBranded, 9 phrase/exact keywords removed and 15 BROAD added (the "use broad match" recommendation).
  - **This resolves the session-7 open item.** Display was not a `create.py` regression. The 09-11/12 `old_value` is `false`, so we built both campaigns Search-only.
- **Client** (`ontheway@onthewaypros.com`, web + mobile app): 47 events.
  - Budgets: LSA on 09-08, 09-18, 09-22, 09-23, 09-29 (x2) and 10-01. NonBranded $197 → $50 → $30 on 09-10. PMax-1 on 09-17 and 09-30.
  - **09-21 21:22, mobile app:** applied the **"Google search partners" recommendation** on both Search campaigns. Edu's UI change-history paste confirms the label "Applied recommendation: Google search partners". In the same minute they removed 20 keywords (19 are the phrase/exact twins of the auto-applied broads, so probably the "remove redundant keywords" recommendation, but the API doesn't show the label and it's unconfirmed) and added "ac compressor repair" BROAD.
  - 09-29: 12 campaign-level PHRASE negatives on NonBranded: parts near me, parts store, parts supply, ac parts, air conditioner parts, air conditioning parts, hvac parts, ac supply, hvac supply, plumbing supply, electrical supply, supply house.
  - 09-30: NonBranded Display OFF.
  - **The client never turned Display on.** Auto-Apply did. The client turned it off on NonBranded only.

**2. Auto-apply subscriptions (`recommendation_subscription`):** all created **2023-10-29**, before TSD. Most were paused **2026-09-15 14:53**, and the API doesn't say by whom. **Still ENABLED:** `OPTIMIZE_AD_ROTATION`, `RESPONSIVE_SEARCH_AD`, and one type the API returns as `UNKNOWN` (modified 2026-03-25). Edu: auto-apply not being turned off at launch is on him, it should have been checked during pre-launch.

**3. Conversion goals on OUR two Search campaigns at launch** (Edu asked to keep this answer for later use):
- Both use account-level goals (`conversion_goal_campaign_config.goal_config_level = CUSTOMER`), with no custom goal and no selective optimization. `create.py` has no goal code. The only campaign-level goal edit we ever made was on PMax-2 (session 5).
- At launch they bid on 4 categories / 7 actions. The session-5 cleanup ran before the session-6 enable.
  - `PHONE_CALL_LEAD/CALL_FROM_ADS`: Calls from ads (`445477902`), Calls from ads (1) (`7575044326`), Calls from Smart Campaign Ads (`313494939`), [TSD] Click to call (`7754982884`).
  - `PHONE_CALL_LEAD/WEBSITE`: empty.
  - `SUBMIT_LEAD_FORM/WEBSITE`: [TSD] Submit lead form (`7754995862`), Call ((409) 310-1464) (`7717494704`).
  - `SUBMIT_LEAD_FORM/CALL_FROM_ADS`: Calls from ads (2) (`7717741803`).
- **Store visits, App installs and Directions were NOT biddable at launch.** They were only on during the paused window between the session-2 build and the session-5 cleanup.
- Actual results 09-09 → 10-01: Conversions = **19 Calls from ads** (BR 13, NB 6) + **5 [TSD] Click to call** (BR 3, NB 2). 0 forms. 0 Store visits or App installs ever, even in `all_conversions`. Non-biddable actions appear in All conv only: Local actions - Other engagements 68, Clicks to call 7, Directions 5, Menu views 4, Website visits 2.
- Caveat: the API has no history of goal settings, so the launch state rests on the session-5/6 entries. It matches today's settings.

**4. Were the client's edits fixing a real leak? No.** Each was judged on the data available at the time.
- **09-21 keyword removals.** The removed keywords had $267.05 / 25 clicks / **7 conv** from 09-09 to 09-21, almost all on Brand exact. "on the way plumbing" EXACT alone had 16 clicks, $152.10 and 5 conv, the best keyword in the account. The 14 NonBranded ones had $21.82 / 2 clicks / 0 conv. Their traffic moved to the broad twins: "on the way plumbing" BROAD after 09-21 had 18 clicks, $149.96 and 6 conv.
- **09-29 parts/supply negatives.** Search terms they would have blocked, 09-09 → 09-28: $69.30 / 5 clicks. Of that, $65.02 was one term, "home ac parts near me" (2 clicks on 09-22), which produced **1 Calls from ads conversion**. Real junk was $4.28 / 3 clicks ("ac supply near me" $2.04, "plumbing supply store" $1.52, "ferguson plumbing supply" $0.72), against $836.66 of NonBranded Search spend in the same window. Every one of these terms came through the auto-applied BROAD keywords "ac repair", "plumber" and "plumber near me".
- **Display.** It only spent 09-12 → 09-15: NonBranded $59.34 / 25 clicks / 0 conv, Branded $10.36 / 8 clicks / 1 conv ([TSD] Click to call). It spent $0 after 09-15 even though the setting stayed on, so the client's 09-30 switch-off hit nothing. **Branded still has Display ON.**
- **Search Partners** since 09-21: 5 impressions, 0 clicks, $0.
- **The one real leak was in OUR build, and the client never touched it.** NonBranded `plumber` PHRASE spent **$242.55 / 10 clicks / 0 conv** from 09-09 to 09-21. The visible terms are competitor names: "moore plumbing league city" $24.87, "all about plumbing league city" $24.72, "az remodeling and plumbing reviews" $23.78, "plumbing co near me" $23.43. That's $96.80 visible out of the $242.55. It has had 0 clicks since 09-21, probably because of the $30/d budget, and it's still ENABLED.
- Caveat: the search-term report hides low-volume terms, so the numbers above are what's visible, which is the same data the client sees.

**Current budgets (from the API):** Branded $20/d, NonBranded $30/d, PMax-1 $30/d, all on Max Conversions. LSA is outside this log (client-managed).

**Did:**
- Drafted the AM reply. Final text as approved by Edu:

> Sept 9 was the full build and launch. We built the new Branded and NonBranded Search campaigns, paused the old campaigns that weren't bringing real leads, and set conversions to count only calls and form submissions. No store visits or anything like that.
>
> After a launch we avoid changes for the first weeks while Google's bidding learns, so we act on real data and not a few days of noise. On Sept 10 the NonBranded budget went from $197 to $30 a day, so it gets about 2 clicks a day and data comes in slowly. We reviewed it on Sept 15 and again this week.
>
> The auto-apply changes: Google auto-apply was turned on in this account in Oct 2023, before we started. It made changes from Sept 11 to 14 (Display, broad match keywords, NonBranded bidding) and was paused on Sept 15. It not being turned off at launch is my fault, I should have checked it.
>
> On the recent edits they made, the data didn't show a real leak. The parts/supply negatives they added would have blocked 5 clicks in 3 weeks, about $4 of real waste, and one of those searches became a call. The keywords they removed on Sept 21 had 7 calls, so they weren't wasting money. They turned off Display on Sept 30, but it had already stopped spending on Sept 15.
>
> On Sept 21 they also applied Google's Search Partners recommendation from the mobile app (ads on other sites that use Google search). We launched with it off on purpose, because at the start we want clean data from Google search only. So far it got 5 impressions and $0.
>
> Next on our side:
> 1. Turn off the last 3 auto-apply options that are still on
> 2. Turn off Display on Branded
> 3. Turn Search Partners back off on both campaigns
> 4. Review the broad keywords Google added and add competitor negatives
>
> Going forward all changes come from us. If they want something changed, they can send it over and we'll check the data and make it.

- Note on Search Partners: launching with it off is general practice (cleaner early read, less control over partner placements). Our Google SOP doesn't mention it.

**Open items (new, the first 4 were promised to the client in the AM reply):**
- [ ] Turn off the 3 auto-apply subscriptions still ENABLED (`OPTIMIZE_AD_ROTATION`, `RESPONSIVE_SEARCH_AD`, `UNKNOWN`).
- [ ] Branded: Display OFF.
- [ ] Both Search campaigns: Search Partners OFF.
- [ ] Review the auto-applied BROAD keywords, and add competitor negatives (Moore Plumbing, All About Plumbing, AZ Remodeling, and others from search terms) to stop the `plumber` PHRASE leak.
- [ ] Decide whether NonBranded stays on Max Conversions (auto-applied 09-11) or goes back to Manual CPC with ceilings.
- [ ] In the UI change history, confirm whether the 09-21 keyword removals show "Applied recommendation". If they do, it can go in the client explanation.
- [ ] AM reply not confirmed sent as of this entry.
- [ ] Carried forward: PMax-1 brand exclusion (manual UI step), phone-answering hours, redundant call/form conversion actions, PMax-1 asset group split, Phase 2 build.

---

## 2026-09-15 (session 7) — First real-data read: weekly PPC snapshot + conversion action audit

Edu asked for the standard weekly PPC metric bundle (spend/CPL/CPC/conversions/conv rate, branded vs. unbranded, impression share) — first real look since launch, six days in, past the "don't read before day 3" mark set in session 6.

**Found (7-day window, PPC only — Branded Search + NonBranded Search + Performance Max-1; LSA excluded per standard doctrine):**
- Account totals: $715.11 spend, 97 clicks, 10 conversions, 10.31% conv rate, $71.51 blended CPL, $7.37 CPC.
- Branded: 5 conversions, $112.12 spend, $22.42 CPL, 91.7% IS (3.3% lost to budget, 5.0% lost to rank) — healthy.
- NonBranded: 1 conversion, $434.15 spend/CPL — thin sample this early, 22.6% IS (34.7% lost to budget, 42.7% lost to rank) — capped on both fronts, real headroom.
- Performance Max-1: 4 conversions, $168.84 spend, $42.21 CPL.
- Combined Search-only IS (Branded + NonBranded weighted by eligible impressions): **26.0%**. The raw customer-level `search_impression_share` (14.15%) isn't usable on its own — it blends in non-Search campaign types and GAQL won't let you filter the `customer` resource by `campaign.advertising_channel_type` to isolate it.
- Per Edu's standing rule, PMax always buckets as unbranded: Unbranded (NonBranded Search + PMax-1) = 5 conversions, $602.99 spend, $120.60 CPL.
- **Conversion-action audit**: all 10 conversions this week are `PHONE_CALL_LEAD`, split between "Calls from ads" (8: 4 PMax-1, 3 Branded, 1 NonBranded) and "[TSD] Click to call" (2, Branded only). No junk categories fired. The two previously-flagged dead actions ("Calls from Smart Campaign Ads," "Calls from ads (1)") stayed silent — consistent with them being inert legacy.
- **New finding**: both Branded and NonBranded Search campaigns have `target_content_network: True`, despite being built 09-09 — after the 08-24 book-wide fix that was supposed to default new Search campaigns to Search-only (`target_content_network=False`). Display/Content pulled 15 clicks / $33.82 / 0 conversions on NonBranded and 8 clicks / $10.36 / 1 conversion on Branded this week — small dollars so far, but it means the `create.py` fix either isn't holding for this account or these two campaigns weren't built through that path. Of Branded's 5 conversions, 4 are Search-attributed and 1 is Content-attributed; PMax-1's 2 Search / 2 Maps split is normal for PMax, not a leak.

**Did:** read-only reporting session — no account mutations.

**Open items (new):**
- [ ] Investigate why `target_content_network=True` on both Search campaigns despite the 08-24 fix — confirm whether `create.py` was actually used for this build or if it's a regression, then flip both to Search-only if unintended.
- [ ] Everything from session 6 carries forward unchanged (phone-answering hours, redundant call/form conversion actions, PMax-1 single asset group, brand exclusion manual step, Phase 2 go-ahead).

---

## 2026-09-09 (session 6) — LAUNCH: Branded + NonBranded Search enabled

Edu: "Turn them on." Closes the Phase 1 Search launch opened in session 2.

**Did — enabled at all three levels, per the skill's own safety rule (campaign → ad groups → ads, never just the top level):**
- Campaigns: `TSD_09.09_Search_Branded_Evergreen` (`24232091690`) and `TSD_09.09_Search_NonBranded_Evergreen` (`24226524120`) → ENABLED.
- Ad groups: Brand (`200718634515`), AC-Repair (`200077915917`), Plumbing-Emergency (`203111572234`), Electrical (`200077923037`) → ENABLED.
- Ads: all 4 RSAs → ENABLED.

**Verified post-launch, not just assumed:**
- All 4 RSAs show `policy_summary.approval_status = APPROVED` (cleared review after the session-2 policy fix — ★ symbol and phone number in ad text).
- Full account snapshot: LSA $285.71/day (ENABLED, untouched) + Performance Max-1 $30/day (ENABLED) + Branded $20/day (ENABLED) + NonBranded $197/day (ENABLED) + PMax-2 $30/day (PAUSED) + Demand Gen $20/day (PAUSED). Total ENABLED spend across the account: **~$532.71/day (~$16,194/mo)**, of which the $9k/mo plan (Meta $1,500 + PPC $7,509 = Branded $20 + NonBranded $197 + PMax-1 $30 ≈ $247/day) accounts for the non-LSA piece — LSA sits outside that figure by Edu's explicit call.

**Where this leaves the account, end to end:**
- **Live:** LSA (pre-existing), Performance Max-1 (reinstated, auto-generated assets off, but still a single asset group covering all 7 services — not split by service line yet), Branded Search, NonBranded Search (AC-Repair / Plumbing-Emergency / Electrical only — Phase 2 services researched and copy-ready in `google-ads-search-launch-brief.md`, not built).
- **Paused, by design:** Leads-Performance Max-2 (conversion goals now fixed, but still paused — no request yet to bring it back), Demand Gen (zero real conversions in 30 days, no case made to revive it), 4 legacy dead campaigns from before TSD's involvement.
- **Conversion tracking:** account-wide goals now bid only on real lead categories (phone calls + form submissions, web + ad-based) — the App-install/Store-visit/Directions pollution is gone from both the account default and PMax-2's override. Still open: 3 redundant `PHONE_CALL_LEAD/CALL_FROM_ADS` actions and 2 redundant `SUBMIT_LEAD_FORM/WEBSITE` actions sitting in the same biddable buckets as the clean `[TSD]`-prefixed ones — can't be resolved from the Ads side alone, needs Edu to confirm against the real tracking implementation which pipes are actually still wired.

**Open items carried forward (unchanged, still real):**
- [ ] **Phone-answering hours** — ad schedule runs on the posted Mon–Sun 8am–6pm, never confirmed as the real answering window. Highest-value thing to nail down now that money is actually moving.
- [ ] Which of the redundant call/form conversion actions are genuinely still connected vs. dead — Edu to check against CallRail/GTM/whatever forwards the number.
- [ ] PMax-1's single asset group should eventually split by service line.
- [ ] Brand exclusion on PMax-1 still needs to be added manually in the Ads UI (API gap, see session 4).
- [ ] **Don't read performance before day 3** — impression share and call-conversion data are both unreliable same-day/intraday, per division doctrine. First real look: 2026-09-12.
- [ ] Phase 2 (Heating, Roofing, Insulation, Generators, Energy-Audit, Water-Heater, Drain-Sewer, Leak-Detection) — fully researched, RSAs written, sitting in the brief, needs a go-ahead to build.

---

## 2026-09-09 (session 5) — Account-wide conversion-goal cleanup

Edu confirmed: go ahead with the conversion-goal cleanup flagged in session 4 (redundant call-tracking actions, junk goal categories).

**Mechanics check first** (per [[tsd-google-conversion-goals-mechanics]] — `conversion_action.primary_for_goal` is a no-op for bidding): the real levers are `customer_conversion_goal` (account-wide default, by category+origin) and `campaign_conversion_goal` (per-campaign override). Also confirmed these are bucketed by **category+origin, not per individual conversion action** — so if two actions share a bucket (e.g. "Calls from ads" and "[TSD] Click to call" are both `PHONE_CALL_LEAD/CALL_FROM_ADS`), the API cannot bid toward one while excluding the other. That constrained what "cleanup" could mean here.

**Found the account default was already mostly right** — only 3 of the ~19 category/origin combinations were wrongly biddable=True: `GET_DIRECTIONS/WEBSITE`, `DOWNLOAD/APP`, `STORE_VISIT/STORE`. The real bug was **Leads-Performance Max-2 had its own campaign-level override** re-enabling those same 3 junk categories (plus keeping the legit 4) — explaining exactly the Store-Visit/App-install pollution found in session 2.

**Did:**
- `customer_conversion_goal`: set `GET_DIRECTIONS/WEBSITE`, `DOWNLOAD/APP`, `STORE_VISIT/STORE` to biddable=**False**, account-wide. Left `PHONE_CALL_LEAD/WEBSITE`, `PHONE_CALL_LEAD/CALL_FROM_ADS`, `SUBMIT_LEAD_FORM/WEBSITE`, `SUBMIT_LEAD_FORM/CALL_FROM_ADS` biddable=True (the 4 legitimate lead types).
- `campaign_conversion_goal` on Leads-Performance Max-2 (`23105415240`): matched the same 3 categories to biddable=False, removing its override. Confirmed post-fix: both the account default and PMax-2's campaign-level goals now bid on exactly the same 4 legitimate categories, nothing else.
- Conversion action `445477902` ("Calls from ads" — confirmed in session 4 as the one actually driving PMax-1's conversions): counting_type `MANY_PER_CLICK` → **`ONE_PER_CLICK`**. Directly fixes the double-counting risk on the one pipe proven to be live.
- Attempted to hide/remove `313494939` ("Calls from Smart Campaign Ads" — dead weight, no Smart campaign is live in this account anymore): **blocked by the API** (`MUTATE_NOT_ALLOWED` / status field on a deny-list — this conversion action's type appears to be system-managed, tied to the Smart Campaigns product feature, not editable via the general API). Left as-is; it's inert since nothing live feeds it.

**Deliberately NOT touched — flagged instead of guessed:**
- **4 conversion actions share the `PHONE_CALL_LEAD/CALL_FROM_ADS` bucket**: `Calls from Smart Campaign Ads` (313494939), `Calls from ads` (445477902, the proven-live one), `Calls from ads (1)` (7575044326), `[TSD] Click to call` (7754982884). Couldn't determine from Ads-API data alone which of the non-`[TSD]` ones are still actually wired into real call tracking (CallRail/GTM/whatever forwards the number) vs. dead leftovers — disabling the wrong one risks zeroing out real signal. **Needs Edu to confirm from the tracking-implementation side** which pipes are actually still connected before any of these get disabled.
- Similarly, `SUBMIT_LEAD_FORM/WEBSITE` has 2 occupants (`Call ((409) 310-1464)` 7717494704 despite its call-sounding name, and `[TSD] Submit lead form` 7754995862) — same open question.
- `Calls from ads (2)` (7717741803) is miscategorized as `SUBMIT_LEAD_FORM/CALL_FROM_ADS` despite the name suggesting it's call-related — left alone (sole occupant of its bucket, no duplication risk from it specifically, but worth a look).
- Didn't touch counting_type on the ~10 other MANY_PER_CLICK actions (Local actions - Directions, Store visits, Menu views, etc.) — all now non-biddable already, so it's cosmetic/reporting-only at this point, not a bidding-integrity issue. Lower priority.

---

## 2026-09-09 (session 4) — PMax-1 reinstated with fixes, budget rebalanced

Edu's call after session 3's audit: bring Performance Max-1 back (it was the one campaign with real results — 12 calls at ~$78 each), fund it by taking $30/day back out of NonBranded, and fix whatever needs fixing on PMax-1 while doing it — per SOP 7.7's mandatory PMax hygiene checklist.

**Audited PMax-1 against SOP 7.7 before turning it back on:**
- **Single asset group** ("Asset Group 1") covering all 7 services — the exact "never a single Services asset group" defect the SOP warns about. Not fixed this session (would mean rebuilding the asset group structure, bigger job) — flagged for a follow-up pass.
- **Auto-generated assets were ON**, not off — `TEXT_ASSET_AUTOMATION` and `GENERATE_IMAGE_EXTRACTION` were both `OPTED_IN`, which explains 59 headlines (vs. a normal ~15) and 82 auto-generated YouTube videos sitting in the asset group. **Fixed:** opted out `TEXT_ASSET_AUTOMATION`, `FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION` (required together — Google rejects opting out text automation while URL expansion stays opted in), `GENERATE_IMAGE_EXTRACTION`, `GENERATE_IMAGE_ENHANCEMENT`, `GENERATE_DESIGN_VERSIONS_FOR_IMAGES`, `GENERATE_ENHANCED_YOUTUBE_VIDEOS`. Four other video-automation types (`GENERATE_VIDEOS_FROM_OTHER_ASSETS`, `GENERATE_SHORTER_YOUTUBE_VIDEOS`, `GENERATE_VERTICAL_YOUTUBE_VIDEOS`, `GENERATE_LANDING_PAGE_PREVIEW`) rejected the opt-out (`ENUM_VALUE_NOT_PERMITTED`) — not settable for this campaign, left as-is.
- **No brand exclusion configured.** Confirmed the brand exists in Google's Knowledge Graph (`BrandSuggestionService.suggest_brands` → `/g/11l20ct1gp`, "On The Way AC Plumbing & Electrical", matches onthewaypros.com exactly) so exclusion is technically possible — but `campaign_criterion.brand_list` requires a `BrandList` resource, and **`BrandListService` doesn't exist in this SDK's API version (v24)**. Can't do this via API right now. **Manual step owed:** in the Ads UI, Performance Max-1 → Settings → Brand exclusions → add "On The Way AC Plumbing & Electrical" (`/g/11l20ct1gp`), so PMax stops being able to absorb branded queries that should route to the cheap Branded Search campaign once that's live.
- Audience signal: only 1 signal attached (thin, for 7 services across 16 cities) — not modified this session, noted as a lighter-priority improvement.
- Channel mix checked: last-30-day spend is 81% Search ($759) / 19% Maps ($177), effectively $0 into Display/YouTube despite the 82 video assets — so the auto-generation was clutter, not an active budget leak. Not a channel-mix emergency, but worth knowing why it wasn't (the video assets probably just weren't winning many auctions, not that they were harmless).

**Did:**
- `TSD_09.09_Search_NonBranded_Evergreen` budget: $227/day → **$197/day** (freed $30/day).
- `Performance Max-1` (`21618497437`): re-**ENABLED**, budget unchanged at $30/day (its pre-existing setting), auto-generated assets opted out as above.
- Net: still $247/day (~$7,509/mo) total across the PPC bucket (Branded $20 + NonBranded $197, both still PAUSED, + PMax-1 $30, now ENABLED) — same total as session 3, just reshuffled. LSA untouched.

**Open items (new, this session):**
- [ ] Add the brand exclusion in the Ads UI (API can't do it — see above).
- [ ] PMax-1's single asset group should eventually split by service line (AC / Plumbing / Electrical at minimum, matching what Search is doing) — not done this session.
- [ ] Leads-Performance Max-2 and Demand Gen remain PAUSED from session 3 — PMax-2 still needs its Store-Visit/App-install goal pollution fixed before it's a candidate to ever come back.

---

## 2026-09-09 (session 3) — Legacy campaigns paused, PPC budget set ($9k total: $1,500 Meta / rest PPC, LSA managed apart)

**Diagnosed real vs. noise on the 3 non-LSA live campaigns** (Edu asked directly), by breaking down each campaign's "conversions" metric by `segments.conversion_action_name` over the last 30 days instead of trusting the topline number:
- **Performance Max-1**: legit — all 12 conversions are `Calls from ads` (PHONE_CALL_LEAD). $936/12 ≈ $78/call, within the media plan's own PMax benchmark ($70–90).
- **Leads-Performance Max-2**: mostly fake despite the name. 33 of 35 "conversions" are `Store Visits` (Google's modeled foot-traffic estimate — meaningless for a company with no retail walk-in). Only 2 are real calls. Real cost-per-lead is ~$465, not the ~$27 the blended number implies.
- **Demand Gen**: $628 spent, 407 clicks, its only real goal (phone calls) fired **zero** times. Dead weight.

**Did, per Edu's direction ("pause the rest and keep only ours"; "$9k total — $1,500 already on Meta, distribute the rest [$7,500] in the PPC account; LSA is separate, don't touch it"):**
- Paused `Performance Max-1` (`21618497437`), `Leads-Performance Max-2` (`23105415240`), `Demand Gen` (`23880220071`).
- Left the LSA campaign (`15790329543`, $285.71/day cap) untouched — managed as its own separate budget line, not counted against the $9k/$7,500 figures.
- Set `TSD_09.09_Search_Branded_Evergreen` (`24232091690`) budget to **$20/day** (~$608/mo).
- Set `TSD_09.09_Search_NonBranded_Evergreen` (`24226524120`) budget to **$227/day** (~$6,901/mo).
- Combined PPC: **$247/day ≈ $7,509/mo**, matching the $7,500 target. Both still **PAUSED** — this was a budget-sizing pass, not a launch. Verified final state via direct query (all 6 relevant campaigns' status + budget).

**Open items (carried forward):**
- [ ] Enable decision still pending — Pre-Launch QA (Stage 8) not yet run: phone-answering-hours not confirmed as real (using posted hours), conversion-goal cleanup on the account's ~20 conversion actions still undecided.
- [ ] PMax-2's conversion goal (Store Visits/App installs mixed with real calls) should be fixed before it's ever unpaused again, or it'll keep misreporting.
- [ ] Confirm with Edu whether pausing PMax-1 (the one campaign that *was* producing real calls at a fair CPL) is intentional now that Search is taking that budget, or whether it should come back once Search has its own read.

---

## 2026-09-09 (session 2) — Account found, Phase 1 Search build (Branded + 3 ad groups), PAUSED

**Researched:** why the account search in session 1 (below) found nothing — Edu confirmed the account was real and gave "345-468-6129," which was mis-read as a phone number instead of a Customer ID. Re-ran the MCC hierarchy search and found the bug: the earlier script was reading `customerClient` (camelCase) but `run_query` actually returns `customer_client` (snake_case) — every name/status filter in session 1 was silently comparing against empty dicts. Real search, done correctly, found it immediately.

**Found:**
- **Customer ID `3454686129`** ("On The Way AC Plumbing & Electrical"), status ENABLED, sitting directly under the TSD MCC (`4155514468`) at level 1 — it was there the whole time.
- **Not a blank account.** Already running: a system-generated **LOCAL_SERVICES (LSA)** campaign (773 clicks / 151 conversions to date), two **Performance Max** campaigns, and one **Demand Gen** campaign. Plus 4 legacy PAUSED campaigns from a prior effort: 3 Smart campaigns (one named "Licensed Plumber Pearland" — Pearland is outside the 16-city service area, worth confirming whether that's intentional) and a dead Search shell "HVAC AD" with a single ad group at the $0.01 bid floor — never actually built out, not worth reviving.
- **Conversion tracking: mixed.** ~20 conversion actions exist, almost all flagged `primary_for_goal=True`, several `MANY_PER_CLICK` (Local actions - Website visits, Store visits, Local actions - Directions, even Android app installs). Two correctly-built actions exist — **`[TSD] Click to call`** (`7754982884`) and **`[TSD] Submit lead form`** (`7754995862`), both `ONE_PER_CLICK` and Primary — confirming Edu's tracking work was real. But checking `campaign_conversion_goal` directly (not just the vestigial `primary_for_goal` flag) shows the *live* campaigns aren't actually bidding toward those two: `Leads-Performance Max-2` is biddable on `DOWNLOAD/APP` and `STORE_VISIT` alongside real call/form goals. **Flagged to Edu, not yet actioned** — this is Stage 3 territory and affects the account's existing live spend, not just today's build.

**Did — Phase 1 build (Edu chose to launch lean: AC-Repair, Plumbing-Emergency, Electrical — the 3 highest-volume, core-licensed-trade services — holding Heating/Roofing/Insulation/Generators/Energy-Audit for Phase 2):**
- `TSD_09.09_Search_Branded_Evergreen` (`24232091690`) — $10/day placeholder budget, Maximize Conversions no target. Ad group "Brand" (`200718634515`), 9 EXACT brand terms, 1 RSA.
- `TSD_09.09_Search_NonBranded_Evergreen` (`24226524120`) — $45/day placeholder budget, Manual CPC (this API version doesn't expose "Maximize Clicks" as a direct bidding field — Manual CPC with an ad-group-level bid ceiling and enhanced CPC off is the established workaround, per `aprendizados.md`). 3 ad groups, each PHRASE+EXACT keywords + 1 RSA + real per-service final URL:
  - AC-Repair (`200077915917`), $20 CPC ceiling, → `/ac-repair/`
  - Plumbing-Emergency (`203111572234`), $25 CPC ceiling, → `/plumbing/`
  - Electrical (`200077923037`), $18 CPC ceiling, → `/electrical/`
- 24 base negatives + 9 brand-term EXACT cross-negatives on the non-branded campaign.
- Geo: 16 service-area cities, presence-only, on **both** campaigns (verified via direct `campaign_criterion` query per the division's location-targeting safety rule — 16 rows on each, not zero).
- Ad schedule: Mon–Sun 8am–6pm on both campaigns (7 `AD_SCHEDULE` criteria each, verified) — from the published site hours, **not** confirmed as actual phone-answering hours.
- **First RSA attempt was disapproved** (`POLICY_FINDING`): the `★` symbol in "4.8★ From 1,650+ Reviews" trips the SYMBOLS policy, and a phone number in a Branded headline trips PHONE_NUMBER_IN_AD_TEXT. Fixed (star → "4.8 Stars", phone headline → "Talk to Our Team Today") and rebuilt clean. Worth remembering for any future RSA copy on this or other accounts.
- Everything built **PAUSED**. Nothing enabled, nothing spending.

**Open items:**
- [ ] Written monthly Search budget from the client — placeholders above ($10 branded + $45 non-branded = $55/day, ~$1,675/mo) need real numbers before Stage 8/9.
- [ ] Confirm Mon–Sun 8am–6pm is actual phone-answering hours, not just posted business hours.
- [ ] Decide on the conversion-goal cleanup (live campaigns bidding toward App installs/Store visits) — separate from today's build but urgent, real budget is burning against it right now.
- [ ] Confirm "Licensed Plumber Pearland" legacy Smart campaign — in or out of service area on purpose?
- [ ] Phase 2: Heating, Roofing, Insulation, Generators, Energy-Audit, + Water-Heater/Drain-Sewer/Leak-Detection plumbing sub-groups — full keyword research and RSA copy already written in the brief, just needs the go-ahead and ad groups built.
- [ ] Pre-Launch QA (SOP Stage 8) before anything gets enabled.

---

## 2026-09-09 (session 1) — Search launch: account access blocked, campaign brief + RSAs built

**Researched:** whether a Google Ads account exists for On The Way, and whether we're ready to build the branded/non-branded Search campaigns per [`google-ads-launch-buildout.md`](../../paid/sops/google-ads-launch-buildout.md).

**Found:**
- No account under the TopServ MCC (`4155514468`) — checked all 127 child accounts (all levels of `customer_client`) by name, no match for "On The Way," "onthewaypros," "plumbing," or "electric."
- Edu's OAuth login has direct access to exactly one account outside the MCC: **customer ID `3525426278`**. It is **not** linked into the TSD MCC hierarchy.
- That account returns `CUSTOMER_NOT_ENABLED` on every API call (read and presumably write) — Google Ads' error for an account that hasn't finished setup, almost always a missing billing/payment profile. Could not confirm the account name from the API side because of this — name/phone (`On The Way AC Plumbing & Electrical`, 345-468-6129) came from Edu directly, not verified against the account record.
- Tracking is reportedly fully implemented, done outside Claude Code by Edu directly — not yet logged here in detail; that write-up is still owed (Edu's note, 2026-09-09).

**Did:**
- Confirmed destination: `https://www.onthewaypros.com/` — found real per-service pages via site fetch (`/ac-repair/`, `/ac-maintenance/`, `/ac-replacement/`, `/heating/`, `/plumbing/`, `/electrical/`, `/roofing/`, `/insulation/`, `/generator-installation/`, `/energy-efficiency/`) and used those as final URLs per ad group instead of the bare homepage, for Quality Score / relevance.
- Ran Keyword Planner (`keyword_planner.py ideas`) across 12 service themes, geo'd to Galveston + Harris + Brazoria counties (the counties the 16-city service area sits in), English, Search network only.
- Resolved geo target constant IDs for all 16 service-area cities (`GeoTargetConstantService.suggest_geo_target_constants`).
- Built the full Campaign Brief + RSA deck: [`google-ads-search-launch-brief.md`](google-ads-search-launch-brief.md) — 2 campaigns (Branded + NonBranded Evergreen), 13 themed non-branded ad groups, PHRASE+EXACT keywords, negative list, geo, RSAs for all 14 ad groups (char-limit validated), bidding plan per SOP 7.3.
- Did **not** attempt to link `3525426278` into the TSD MCC (a manager-link invite is visible to the client) or attempt any write — held for confirmation.

**Open items:**
- [ ] Confirm `3525426278` is actually the On The Way account (name unverifiable via API while `CUSTOMER_NOT_ENABLED`).
- [ ] Get billing/payment profile completed on that account in the Ads UI — nothing (read or write) works via API until it clears `CUSTOMER_NOT_ENABLED`.
- [ ] Decide: link into TSD MCC (`4155514468`) for standard team access, or manage as a standalone account? SOP Stage 2 wants MCC access.
- [ ] **Monthly Search budget, in writing** — the Jul–Sep media plan splits $9k/mo fluidly across LSA/Google Ads/Meta, no locked Search-only number and no written approval on file yet (SOP 1C hard requirement before anything launches).
- [ ] Phone-answering hours — using the published Mon–Sun 8am–6pm as the ad-schedule input; confirm this is also when a human actually answers (vs. just business hours), since the "24/7 emergency" framing implies after-hours coverage might differ.
- [ ] Once the account is enabled and budget is confirmed: build everything in the brief (PAUSED), then Pre-Launch QA (Stage 8) before Stage 9 launch.
- [ ] Add to `contas.yaml` and move up from "Prospects / not in the book" to the Clients list in `clients/README.md` — holding until the account ID is confirmed live.
