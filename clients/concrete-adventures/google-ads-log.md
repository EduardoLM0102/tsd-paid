# Concrete Adventures — Google Ads log

Google Ads 9215192296 "Concrete Adventures - SC, MS" (inherited from the previous agency, BCJ = bookcleaningjobs). LSA 2898153501 (separate).
Plan and rules: Ryan's Paid Media Packet (`~/Documents/ConcreteAdventures_Paid_Media_Packet (2).docx`). Oxford MS only, $3,000/mo total, Search is small capture.

## 2026-11-04 — fu-083 first check on the Oxford Search campaigns (read-only, nothing changed)

Script `concrete_check_1104.py` (this folder). Window 10-22 → 11-03 (13 days since launch).
| | Budget/cap | Spend | Clicks / impr | CPC | IS / rank-lost | Leads |
|---|---|---:|---|---:|---|---:|
| Branded 24379794681 | $5 / $4 | $0.00 | 0 / 1 | n/a | 100 / 0 | 0 |
| Nonbranded 24379794684 | $10 / $10 | $57.10 | 7 / 95 | $8.16 | 57 / 41 | 0 |
- **Everything approved:** 4 RSAs (go. pages), 6 sitelinks, 6 callouts, snippet, call asset (662) 498-5409.
- **Spend ~$4.40/day of $15.** Oxford is as small as the packet said: 95 non-brand impressions in 13 days. **Branded: 1 impression total** (almost
  nobody searches the brand yet). Nonbranded is LIMITED by the $10 cap (41% rank-lost), but more bid would buy research clicks, not leads.
- **0 leads:** no form conversions, 0 ad calls in call_view. Website calls to 498-5409 are only visible in the client's own CallRail (not ours).
- **Search terms (7 clicks):** stained concrete floors $10.00, **yasen epoxy $9.74 + yasen epoxy flooring $9.72** (Yasen = DIY epoxy product brand),
  stained concrete floor colors $3.48 (+3 not shown). Other impressions: dabin epoxy, stontec stonhard, apex coatings, hc concrete stain, microcement,
  garage floor coating ideas, epoxy sand coating = product/DIY research.
- Keywords: 'concrete coating' (49 impr), 'decorative concrete' (21), 'concrete staining' (14) carry it; pool deck + resurfacing keywords 0 impressions. QS 3-5 where rated.
**Proposed (Edu's go):** PHRASE negatives on list 12280924077: yasen, dabin, stonhard, stontec, ideas. Keep budgets/caps (packet: never expand for volume).
The unspent ~$300/month of the $450 Search line could go back to YouTube/Meta (total stays $3k), Edu's call.
**APPLIED later 11-04 (Edu's go):** `concrete_negs_1104.py`, read-back OK: yasen, dabin, stonhard, stontec, ideas (PHRASE) on list 12280924077 (43 → 48). Replay: 7 terms, $19.46, no keyword conflicts. Budget question still open.

---

## 2026-10-22 — audit + first TSD Search build (PAUSED)

**Read-only audit** (script: google-ads-ratos/scripts/concrete_audit_1022.py)
- Billing: client's own payments account (Concrete Adventures, LLC), approved. Packet fix 5 done.
- 8 old BCJ campaigns all PAUSED. Last spend 09-22 to 10-01: MS Search $482 (0 conv), MS PMax $141 (3 conv). Nothing since 10-01.
- Old "MS" campaigns targeted **DeSoto County** (Southaven), not Oxford. SC/GA on Aiken County and GA counties.
- ~860 enabled keywords across the old Search campaigns (MS 327). AI Max not on. Shared negatives "Universal (BCJ)" 251.
- 16 conversion actions, many primary: BCJ website calls (10s), Calls From Ads (10s), Lead Form Submission, Chat Lead upload, GHL Import (SPM), plus `[TSD] Click to call` and `[TSD} Submit lead form`. Last 30d: 3 conversions.
- Account-level assets from the old agency: sitelinks incl. "Get Your Free Quote", callouts incl. "5-Year Warranty" (unverified) and "Head-Resistant" (typo). No account-level call asset. Old call assets: (662) 715-4215 MS, (803) 408-5505 SC, (762) 320-5013 GA.
- GTM: the live concrete-adventures.com HTML loads only **GTM-KV5TR7CK** (old agency, contains GA4 G-DDSJGR9XVM only). TSD's container GTM-53FXJRN4 (account 6382574349, workspace 3) has the full tag set, published, Ads tags to AW-16809872504 (matches the [TSD] actions). CORRECTION same day: I first read it as empty (wrong workspace); Edu confirms it's installed and working. Still to confirm which site/domain carries it.
- Site (concrete-adventures.com) is multi-state, (803) SC number is the main CTA on every page, form/chat in old agency's GHL.

**Build** (Edu: "if its creating the campaigns, go for it and leave paused"). Script: `build_search_oxford_1022.py` (validate, then --apply, one atomic mutate).
- `TSD_10.22_Search_Branded_Oxford` 24379794681: $5/day, Maximize Clicks $4 cap. "concrete adventures" exact + phrase. Final URL homepage.
- `TSD_10.22_Search_Nonbranded_Oxford` 24379794684: $10/day, Maximize Clicks $10 cap. Ad groups Garage Floor Coatings (6 phrase), Pool Deck Resurfacing (5), Concrete Coatings (7), each to its service page.
- Both: PAUSED, Google Search only (no partners, no Display), Oxford city 1020795 + ZIP 38655, presence-only, English, text + final URL expansion opted out.
- Shared list "TSD Negatives - Oxford (10.22)" 12280924077: 43 phrase negatives from the packet (aggregate, millings, asphalt, supply, wholesale, DIY, jobs, hiring, salary...) + retail/DIY/other-city terms, on both campaigns.
- Campaign-level sitelinks (5), callouts (6), snippet (Services) so the old account-level ones don't show. No call asset on purpose (waiting for CallRail).
- 4 RSAs, no offers/discounts/"free"/warranty claims; copy only uses claims from the site (family owned, nearly 10 years, limited projects each month, slip-resistant + UV-stable pool deck coatings).
- AI Max / auto-apply guardrail (paid/guardrails/ai_max_auto_apply_off_1016.py) now includes both CA accounts: 0 to change.

**Before enabling** (Command Center fu-081): CallRail number → call asset; confirm the ads' final URLs are on the site that runs GTM-53FXJRN4, BCJ actions → secondary; GHL form ownership; ads approved.
Search budget $15/day (~$450/mo) comes out of YouTube's remainder; Meta 3x floor (~$1,860) untouched, total stays $3k.

## 2026-10-22 (later) — ads repointed to the go. pages + call asset

Edu: tracking runs on TSD GTM-53FXJRN4, which is on **go.concrete-adventures.com** (root + /decorative-concrete/), not on www. Both go. pages checked: GTM-53FXJRN4, phone (662) 498-5409, form on link.leadnurturemachine.com.
Script `repoint_go_pages_1022.py` (validate, then --apply, campaigns still PAUSED):
- Branded RSA → https://go.concrete-adventures.com/ ; the 3 Nonbranded RSAs → https://go.concrete-adventures.com/decorative-concrete/ (form on page). Ads back in review.
- Sitelinks: the 5 www ones unlinked from both campaigns; 6 go. sitelinks added (Garage Floor Coatings, Pool Deck Resurfacing, Concrete Overlays, Concrete Staining, Customer Reviews on go./?src=1-4,6; Request an Estimate on /decorative-concrete/?src=5).
- Call asset (662) 498-5409 on both campaigns. Johnny (Slack DM 2026-10-21): Ads number in the client's OWN CallRail account (not TSD's agency account), source 'Google Ads Assets', forwards to 662-291-7755. Call reporting = account default call action.
Still before enabling: ads approved; set the old BCJ conversion actions to secondary (account default call action is probably 'Calls From Ads (BCJ)' at 10s, TSD standard is 60s).

## 2026-10-22 (later 2) — conversion cleanup (packet fix 4)

Edu: "Make it not count the BCJ stuff. Let's keep the Click to call we created as secondary", then chose "Google native, 60s" for call-asset calls.
- `conv_cleanup_1022.py`: SECONDARY now: Calls From Website SC/MS/GA (BCJ), Lead Form Submission (BCJ), Chat Lead (BCJ), [TSD] Click to call.
- `ad_calls_60s_1022.py`: 'Calls From Ads (BCJ)' 6959959574 renamed **[TSD] Calls from ads (60s)**, 10s → 60s, primary. It is the account's call reporting action, so it counts call-asset calls (Google forwarding number).
- Primary now (lead categories): [TSD} Submit lead form + [TSD] Calls from ads (60s). (Also primary but irrelevant to Search: 'Lead form - Submit' Google-hosted, 2 YouTube actions.)
- Found: NO CallRail swap script on the go. pages or in GTM-53FXJRN4, and 498-5409 is hardcoded. CallRail can only upload calls with a gclid, so Edu's CallRail integration (60s+) covers website calls only after the swap script is added (Google Ads source tracker). Call-asset calls never have a gclid → covered by the Google native action above, no double count.
Ads, sitelinks and call asset still in review at 10-22 evening.

## 2026-10-22 (later 3) — Search LIVE

Edu: skip the CallRail session pool for now (fixed 498-5409 already records every call for lead-quality review; Max Clicks doesn't bid on conversions; add the pool when Meta/YouTube start sending traffic to the go. pages), then "ok so can we just push live now?".
- `enable_search_1022.py`: both TSD_10.22 campaigns ENABLED (Branded $5/d, Nonbranded $10/d). Status LEARNING. Ads/sitelinks/call asset were still in review, they serve once approved.
- Counting: [TSD} Submit lead form + [TSD] Calls from ads (60s). Website calls from ad clicks are NOT counted in Google Ads until a CallRail pool + integration exist; judge them in CallRail (all calls to 498-5409 show as source 'Google Ads Assets', mixed sources).
- First check ~10-27 (Command Center fu-083): approvals, spend vs $15/d, CPC vs caps, search terms (new negatives), impression share on Branded.

## 2026-10-28 — GTM v4 for Alex's new site + 10-27 test lead check

Alex (Slack DM 10-28, from the site agent) asked 6 things for the new site (staging https://tsd-concreteadv.vercel.app, launch Mon-Wed next week). Edu: "You have my approval to make the changes on the GTM that he requested, just don't forget to also change the tags that are affected by the cEvent he wants to swap".
**Done: GTM-53FXJRN4 v4 PUBLISHED** (scripts in google-ads-ratos/scripts: `concrete_gtm_launch_draft_1028.py`, `concrete_gtm_version_env_1028.py`, `concrete_gtm_headless_test_1028.py`, `concrete_gtm_publish_v4_1028.py`). Default workspace is now 4.
- Ask 2: trigger 10 → `cEvent - Lead (generate_lead + old GHL)`, regex `^(generate_lead|ghl_form_submit)$`, drives Google Ads Lead (29) + Meta Lead (22). ghl_form_submit kept so the live go. GHL pages (where Search ads point) keep counting until launch. Remove it after launch.
- Ask 3: Meta Lead eventID = `{{dlv - event_id}}`. Advanced matching moved to new `cJS - Lead Email/Phone/First Name/Last Name` (read ghl_user.*, flat keys, user_data.*; already-hashed values pass through), since the site's leadUser keys can't be seen client-side.
- Ask 4: GA4 Lead (11, event `lead`) moved to `cEvent - ghl_form_submit (old GHL pages only)`. New site: GA4 gets generate_lead from Alex's server only.
- Headless test before publish (hits aborted): generate_lead raw + hashed → Ads Lead + Meta Lead with eventID + user data, no GA4; ghl_form_submit same as v3; decoy event nothing.

**Ask 5 check (test lead 10-27 ~8:35 pm CDT):** Meta dataset 1475311421329137 = 2 BROWSER Leads from staging (18:00 PT hour), ZERO server events ever, so no CAPI and no dedup. GA4 560003215 = no generate_lead 10-27/28; property has NO key events at all.
**Ask 1:** CallRail swap.js for (662) 729-8852 not reachable: no Concrete company in any CallRail account our API key sees (client's own CallRail).

**OPEN (come back to this):**
- Edu: get the swap.js URL from the client's CallRail UI and send to Alex.
- Edu: send Alex the reply (GTM done + test lead result: 0 server events in Meta, 0 generate_lead in GA4; is server side off on staging or token/secret wrong?).
- Decide GA4 route: server-only generate_lead (Alex's ask, done) vs Spencer v11 route (GTM generate_lead tag + Alex drops server MP), because on Spencer the server MP lead landed in GA4 with source (not set). Also mark generate_lead as key event in GA4 UI (our token is read-only).
- Decide consent gating: new site defaults consent to denied but Meta tags here fire regardless (same issue fixed on Spencer v10: ad_storage required + PageView on `site:consent-change` grant). Recommended, not done.
- 2 browser Leads for 1 test: on staging the site calls fbq Lead itself while `__trackingLeadEvent` is null; recheck counts at launch.
- Launch day: joint GTM Preview with Alex (1 Ads conversion, 1 deduped Meta Lead, 1 GA4 generate_lead). After launch: drop ghl_form_submit from the trigger, pause GA4 Lead 11 + GHL Listener 7 if GHL pages are gone.
- Command Center fu-102 (due 11-05). fu-083 (first Search check, due 10-27) still open.

## 2026-11-02 — Alex's 10-29 asks: capiParamBuilder fix (v6 built) + staging browser check in progress

Alex (Slack DM 10-29, nudged 10-30) asked for (a) a 10-min browser-only check on staging and (b) optionally removing Meta's capiParamBuilder (~37 KB) from the container for page speed.

**(b) capiParamBuilder:** not a separate tag. It sits inside the gallery "Meta Pixel" template (tags 6 PageView / 22 Lead / 23 ViewContent): after fbevents.js the template injects clientParamBuilder.bundle.js, switched on by Meta server-side (`gateCheck('enable_gtm_parambuilder')`). No tag setting turns it off (`optInMetaCAPI` is a different feature). The template skips the download when `window._fbq_param_builder_status` is already 'complete'.
- Built: tag 40 `00 | cHTML - Skip Meta ParamBuilder` (Initialization - All Pages, sets that flag). Template untouched, keeps gallery updates. **Version 6** created, test env 41.
- Headless test (hits aborted, fbq stub passes Meta's gate): v5 = 1 param builder request, v6 = 0. Meta PageView, Meta Lead (eventID) and Ads Lead fire the same on the go. GHL page and staging.
- **NOT PUBLISHED:** auto-mode blocked the publish. Edu runs `./gtm.sh concrete_gtm_publish_v6_1102.py` (aborts unless live is v5, syncs ws 6, deletes env 41). Live still v5 at 10:30 BRT.
- Scripts (google-ads-ratos/scripts): `concrete_gtm_inspect_parambuilder_1102.py`, `concrete_gtm_tpl_dump_1102.py`, `concrete_gtm_parambuilder_draft_1102.py`, `concrete_gtm_parambuilder_test_1102.py`, `concrete_gtm_publish_v6_1102.py`, `concrete_gtm_live_check_1102.py`.

**(a) staging browser check (running through Cowork in Edu's browser):**
- Cowork prompt written: GTM Preview on https://tsd-concreteadv.vercel.app/contact + Meta Test events on dataset 1475311421329137; Lead 1 "TEST TopServ" without touching the cookie notice (expect 1 generate_lead with event_id, Ads Lead 29 + Meta Lead 22 once each, Meta eventID = event_id, ad_storage Granted, GA4 Lead 11 not fired); optional Lead 2 after footer "Cookie settings" > Reject non-essential (Meta Lead blocked, Ads Lead still fires = cookieless ping); record submit times (CDT + BRT) for the Google Ads exclusion.
- Gotcha hit: Edu's browser had an ad blocker (Tag Assistant couldn't see the container) and was sending **GPC**, so the site denied all consent (it denies on GPC/DNT). Not a site default problem: headless with no GPC gets ad_storage granted. After turning both off: GPC false, DNT null, all consent Granted, Meta PageView fires on load.
- 09:39 BRT Edu asked Alex to switch the lead event to generate_lead. Checked staging: `window.__trackingLeadEvent` still `null` (site pushes lead_submitted, GTM lead tags won't fire), so Cowork is holding. 10:20 BRT Alex replied he's on it.

**OPEN:**
- Edu: publish v6, then tell Alex it's live (message to Alex at 09:3x said "going live in the next few minutes").
- Run Lead 1 (+ optional Lead 2) once Alex confirms; send him the submit times; exclude them in Google Ads; Alex clears the event name after.
- After the test: check dataset 1475311421329137 for the browser Lead(s).
- Still from 10-28: launch-day full test (browser + server dedup, GA4 server generate_lead, GHL); after launch drop ghl_form_submit from trigger 10.

## 2026-11-02 (later) — staging TEST leads done (Alex's 11:51 BRT DM) + v6 publish still blocked

Alex 11:51 BRT: staging now pushes generate_lead (`__trackingLeadEvent` = 'generate_lead', confirmed), asked for 2 TEST leads + submit times; also saw clientParamBuilder.bundle.js still loading (live = v5, so expected).
Run by Claude in a headed Playwright Chromium (no GPC, no ad blocker), real hits, nothing blocked. Scripts in session scratchpad (leadtest.py / lead2.py / adsbreak.py), not kept.
- **Lead 1, 09:21:53 CST / 12:21:53 BRT**, cookie notice untouched (all consent granted): 1 generate_lead, event_id `00ed1aab-5649-459d-baea-758b74b59f57`; Meta Lead x1 to pixel 1475311421329137 with eid = that event_id; Ads Lead fired (5 requests = fan-out of one conversion, dry run with hits aborted shows one fire = 3 requests sharing one random id); went to /thank-you. Also Meta ViewContent + SubscribedButtonClick (automatic event), PageView on thank-you.
- **Lead 2, 09:23:13 CST / 12:23:13 BRT**, footer Cookie settings > Reject non-essential (ad_storage/analytics/ad_user_data/ad_personalization update = denied): 1 generate_lead, event_id `59901303-8ee6-4fe6-9f51-990d9df4ec17`; **0 Meta hits**; Ads Lead = 1 cookieless ping (pagead2.googlesyndication, expected).
- Both: name "TEST TopServ", test@fawe-test.invalid, 555-010-0100, city Oxford. Neither came from an ad click (no gclid), so Google Ads shouldn't record them as conversions.
- clientParamBuilder.bundle.js still downloads on live v5 (headed browser, 12:1x BRT). v6 publish blocked by auto-mode again; Edu runs `./gtm.sh concrete_gtm_publish_v6_1102.py` (script now exists; aborts unless live = v5 and v6 has tag 40; v5→v6 diff verified = only tag 40 added).
- **12:4x BRT v6 PUBLISHED** (Edu ran it via Claude): live = 6, Default Workspace (id 7) synced 0 conflicts, env 41 deleted. Note: Edu's 12:26 Slack to Alex said "published" before it was; Alex's agent caught live = v5 at 12:40 and suggested tag sequencing (not needed: tag 40 is on Initialization, runs before Meta tags). Post-publish check, headed browser on staging home x2: `_fbq_param_builder_status` = complete, 0 clientParamBuilder requests, fbevents + Meta PageView still fire.
- Edu sent Alex the v6-live reply on Slack (after the publish; publish missed at 12:26, v6 live, no sequencing needed, staging no longer loads param builder, asked him to confirm). **Open:** Alex confirms on his side + switches staging lead event back (`__trackingLeadEvent` → null) per his own plan.

## 2026-11-11 — CallRail inventory (client account, via Cowork)

Account "Concrete Adventures, LLC" #971-364-987, 4 source trackers, no pool: Website NAP - Oxford (662) 729-8852 → (662) 291-7755 (1 call 11-10); Google Ads Assets (662) 498-5409 → 291-7755 (0 calls in 2026); Google Local Services Ads (803) 715-2140 → 291-7755 (0 calls); first number (803) 721-4373 → (803) 408-5505 (2 calls 10-21). **Main line = (662) 291-7755; 729-8852 is a tracker.** Social tracker (662) 960-6539 staged, not activated, destination must be 291-7755. Note: 0 calls on the Google Ads Assets tracker all year matches the 11-04 read (0 ad calls); worth a test call once Search has volume.
