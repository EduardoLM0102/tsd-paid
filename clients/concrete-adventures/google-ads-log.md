# Concrete Adventures — Google Ads log

Google Ads 9215192296 "Concrete Adventures - SC, MS" (inherited from the previous agency, BCJ = bookcleaningjobs). LSA 2898153501 (separate).
Plan and rules: Ryan's Paid Media Packet (`~/Documents/ConcreteAdventures_Paid_Media_Packet (2).docx`). Oxford MS only, $3,000/mo total, Search is small capture.

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
- First check ~10-27: approvals, spend vs $15/d, CPC vs caps, search terms (new negatives), impression share on Branded.
