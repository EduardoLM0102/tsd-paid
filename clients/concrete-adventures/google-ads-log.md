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
