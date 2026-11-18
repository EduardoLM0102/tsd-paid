# Concrete Adventures — Meta Ads Log

**Ad account:** Concrete Adventures AD Account `25459480633691833` (client BM `409642571461958`, USD, payment on file).
**Page:** Concrete Adventures - Decorative Concrete & Resurfacing `103174475835689`. No Instagram account returned by
`ads_get_ig_accounts` for this ad account (11-10); IG placements run on the Page identity.
**Pixel:** `1475311421329137` "[TSD] Concrete Adventures" (TSD-owned). Not used by this campaign (Reach objective).

> Running log of paid-social work on this account. Newest entry on top.

---

## 2026-11-17 — First video ad PUBLISHED: SCRIPT 4 POOL DECK (AT 01452b1d, Jessica; Edu: "publish this video")

**Source:** Drive folder 11Z47WwDF2axhJXXqrcMqWp2nqeC-LgUD (editor, 11-11): only SCRIPT 4 POOL DECK in 16:9 / 1:1 / 9:16 (h264 1080p 60fps, ~56 MB each, 23-24 s), nothing newer.
Reviewed by contact sheet + local faster-whisper transcript: Logan on camera at a finished pool deck, burned-in captions, logo end card, no offer or price.
Script: "Same slab, same afternoon, same sun. Runs cooler than bare concrete, doesn't chalk up on your feet, and it stops tracking into the house every time somebody walks in off the deck.
Pool decks are the hardest thing we do because this surface is wet half the year and the full sun the other half. Which is exactly why a pool deck is where bad prep job shows up first."

**Upload:** `ads_create_upload_url` is not rolled out on this MCP ("gradually rolled out"), so `ads_creative_upload_media` with `upload_source=URL` pointed at Drive's direct-download endpoint
(`drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`, unlisted files serve bytes without sign-in). Videos (all `ready`): 1x1 **1145662371544083**, 9x16 1170157309113061, 16x9 2264935437786039.

**First attempt, placement customization (9:16 on FB Reels + IG Story/Reels, 1:1 fallback), creative 1485505573486919 → draft ad blocked: "Instagram Account Is Missing".**
`ads_get_ig_accounts` still returns none for this ad account, and a PAC creative can't be given the Page-backed Instagram identity through the MCP (single-media creatives get it automatically, which is why the 3 statics publish fine).
The PAC creative is left unused in the library. Lesson: on this account, until an IG account is connected, build video ads as single-video creatives.

**Published (`ads_activate_entity`, publish_as_active, ~10:15 BRT):** ad **52558128029446** `CA | video1 pool deck (script 4) | 1x1 | V1` in ad set 52556556309046 (campaign 52556556297446), creative **1505937024796666**:
single video 1x1 1145662371544083 (native in FB/IG feed = ~60% of delivery; centered in Reels/Stories), Page 103174475835689, Learn More → https://www.concrete-adventures.com/pool-deck-resurfacing/,
2 primary texts + 2 headlines (DOF, same pattern as the statics), every Advantage+ creative feature OPT_OUT, no description (the first PAC attempt had auto-pulled the site's meta description with the (662) 729-8852 tracker into `description`; the single-video creative didn't), no url_tags, self-AI disclosure unset.
- Text 1: "Same slab, same afternoon, same sun. / We resurface the pool deck you already have. It runs cooler than bare concrete and stops the chalk tracking into the house. / Concrete Adventures. Decorative concrete in Oxford, MS."
- Text 2: "Wet half the year. Full sun the other half. / 🏊 Resurfaced over the slab you already have / 🦶 Cooler on bare feet than plain concrete / 🏠 No chalk tracking into the house / Pool decks are the hardest thing we do, so the prep has to be right. / Concrete Adventures. Decorative concrete in Oxford, MS."
- Headlines: "Same slab. Cooler deck." / "Pool decks are the hardest thing we do".
Read-back: status ACTIVE, effective_status IN_PROCESS (review), delivery pending_process; draft empty. Budget, audience, placements, cap and the 3 statics untouched.
Preview (FB feed): https://business.facebook.com/ads/api/preview_iframe.php?d=AQKU_AHOp5uNOnIjzOzYtgdOLsy151_32yKBQ10lU1GhS1h_Ii7HqNyaBdZyfmySYLUx5b6dpy282HOmF7w7eIElLAeEbn9v4w10-6EVZ7BFjn03ketsxb21rB-aYAfHNifc-m7sw6aXhTGMm9eyY-7pNdO_SAxChft_DSReQstQBBK0qLDppwKTPcRYzeYbstcyS_RPCbFrkSFhrdPENezu8aSzQkwKj1-t9ceRZib0BQ&t=AQJPxYzSxOYWD2zEwdE
AT 01452b1d: execution notes written, Execution complete, Review & Close → Jessica. Next: fu-174 (11-24) reads the video's share of spend vs the statics; if the client connects IG, re-cut as PAC with the 9:16 for Reels/Stories.

**2026-11-17 (later) — copy V2 on the same ad (Edu: "a better copy that doesn't just transcribe what the video says" → "use the multiple variants").**
V1 was a caption of the video. V2 says what the video doesn't (Schwartz: unaware prospect, want not need; Ogilvy: one fact, no adjectives; spine = "the concrete you already have" like the statics).
New creative **963849176518418** swapped onto ad 52558128029446 (renamed `… | V2`), published ~10:21 BRT, read-back ACTIVE / IN_PROCESS, draft empty. Same video, link, CTA, A+ off.
- Text A (misconception): "Most people assume a tired pool deck means tearing it out. / It doesn't. The deck in this video is the same concrete that was always there, coated and finished in place. No demolition, no new pour, about a week for the average home. / Concrete Adventures. Decorative concrete in Oxford, MS."
- Text B (the want): "Pool season in Oxford runs from Double Decker to kickoff. Every one of those days starts with a barefoot walk across the deck. / We finish the concrete that's already there so that walk is one you look forward to. No tear-out, about a week of work, then it's yours for a lot of summers. / Concrete Adventures. Decorative concrete in Oxford, MS."
- Headlines: "Keep the slab. Lose the gray." / "Same concrete. New pool deck." / "Finished over the slab you already have" / "The deck you walk out onto all summer".
- Option C (crew equity: "The crew that finishes your pool deck owns a share of the company…", headline "Built by a crew that owns a piece of it") written but NOT used: needs Ryan/Justin's OK on the wording (packet: 5% rising to 35% at ten years). Creative 1505937024796666 (V1 copy) left unused.

---

## 2026-11-16 — Week-1 frequency read (fu-148), read-only via the Meta MCP + Google API

Campaign 52556556297446, 11-10 (from 14:13 CT) to 11-16 (partial, ~09:00 CT): **$345.90 / 60,078 impressions / reach 20,317 / frequency 2.96 / CPM $5.76**. Full days 11-11..11-15 spent $57-62 of the $61.18 budget every day, so the 4-per-7-days cap is NOT binding yet.
- **Full-week math (added later the same day, Edu asked):** the 5 full days 11-11..11-15 = 51,910 impr / reach 19,958 / frequency 2.60 in 5 days. Adding the two partial days (11-10 afternoon, 11-16 morning) raised reach by only 359 people (19,958 → 20,317), so the pool is saturated at ~20k. A full 7 days at ~10.4k impr/day ≈ 72k impressions on ~20.5k people = **~3.5x per 7 days**, above the 3x target, and close to the 4-per-7-days cap. That is why CPM is creeping. Week 2 will show whether the cap cuts delivery.
- **Frequency ~3x/week, on target.** The 11-11 estimate (~2.4x on a 32-37k audience) was too pessimistic: the people actually reached in the 3.5 mi / 25+ circle are ~20k, not 35k, so the same $61/day holds them at ~3x. Packet rule (shrink only if < 3): no change to the radius.
- **CPM is creeping up**: $5.02 → $5.43 → $5.39 → $5.51 → $6.05 → $6.98 (Sun) → $7.53 (Mon partial). Reach per day fell from ~10.3k to 7.7k on Sunday. That is the early sign of the cap starting to bind as more people hit 4 views. Next week: if daily spend drops under ~$55 with CPM still rising, widen the radius a little (packet: cap hit + underspend = fence too small).
- **CPM vs plan:** $5.76 vs the packet's $16.20 (already raised to Ryan 11-11). Practical meaning: the $1,860/mo holds ~20k people at 3x instead of ~9k.
- **Angle Meta spends on:** ad4 team-logo court $169.91 (49%), ad3 wood-look patio $94.42 (27%), ad5 before-after $81.57 (24%). Per the packet, the first video cuts go behind the team/logo angle.
- **Placements:** FB feed 37%, IG feed 23%, IG stories 16%, FB reels 12%, IG reels 11%, all at $5.6-5.9 CPM. Nothing to change.
- **Branded search (Google 9215192296):** Branded Oxford 1 impression in the 2 weeks before launch, 1 impression / 1 click since. No movement yet, expected this early in a town this size. Nonbranded 29 impr / 6 clicks / $53.86 since launch, 0 conv.
- IG account still not linked to the ad account (placements run under the Page).
Decision for Ryan (he picks after this read): keep 3.5 mi and $61.18/day. Next read fu-174 11-24.

---

## 2026-11-11 — Day-1 check (fu-147), read-only via the Meta MCP

Campaign 52556556297446 / ad set 52556556309046 "CA | OXFORD-SQUARE-3.5MI | 25+" (Reach, cap 4 per 7 days, start 11-10 20:13 UTC = 14:13 CT).
- **All 3 V2 ads ACTIVE and delivering** (review passed again after the copy swap): ad4 team logo court $16.16 / 3,165 impr; ad3 wood-look patio $12.13 / 2,385; ad5 before-after $12.18 / 2,413. Meta leans on the team-logo court (ad4) so far.
- **Spend:** 11-10 (10 hours) $33.53, 6,682 impr, **reach 6,254**, frequency 1.07, **CPM $5.02**; 11-11 to ~10:40 BRT $6.94, 1,281 impr, CPM $5.42. Day-1 pace is in line with $61/day.
- **CPM is a third of the plan.** The packet assumed $16.20; the market is paying ~$5. At $5 the $61/day buys ~12k impressions/day ≈ 85k/week. Against the ~9k-person target that is ~9x/week, so the 4-per-7-days cap will bind within days and the ad set will underspend, OR the real audience is well above 9k (reach already hit 6,254 people in 10 hours). Either way the geography math changes → packet rule: raise to Ryan. The 11-17 frequency read (fu-148) decides: cap binding + underspend = widen the radius a little; frequency under 3 = audience too big, shrink it.
- **Audience size (Ads Manager, 11-11 ~10:50 BRT, via Claude in Chrome): 31,800–37,400 people** vs the packet's ~9k. So the campaign is not cap-bound, it is under-frequency: ~85k impressions/week over ~35k people ≈ 2.4 views per person per week, below the 3x rule. At 3x the same $1,860/mo holds ~28k people; the 3.5 mi circle is a bit too big. Options for Ryan: shrink the radius to roughly 3 mi (aim ~26–28k) and keep the budget, or keep 3.5 mi at ~2.4x. Edu posted the note to Ryan in #onboarding-concrete-adventures 11-11 (~11:00 BRT): CPM $5 vs $16, 32–37k people vs ~9k, ~2.4x/week, early to call, radius to ~3 mi if it holds, decision at Monday's frequency read.
- **Instagram:** `ads_get_ig_accounts` still returns none for the ad account. IG placements run under the Page. Link the client's IG in Business settings if it exists.
- CTR (link) 0.39% day 1, not a KPI here (packet: report frequency, reach, branded search).

---

## 2026-11-10 (later) — Copy V2 swapped into the 3 live ads

Edu asked for better copy, then for the company name in it. V1 mostly repeated the on-image headline. V2 adds facts from
the client's site (overlay goes over the existing slab, no replacement, average home project about a week) and the
company name. Written with the ogilvy-copy skill. No phone number: no Meta tracking number exists ((662) 498-5409 is the
Google Ads one).

Same ad IDs, new creatives (ads renamed V1 → V2), published ~evening 11-10, read-back IN_PROCESS (back in review):
- ad3 `52556556374646` → creative `1145419057935793`
- ad4 `52556556376446` → creative `1456143782829081`
- ad5 `52556556378446` → creative `1112144548120966`

Copy V2:
- Wood-look (ad3): "No boards. No tear-out. That's the same slab. / Concrete Adventures finishes the concrete you already
  have to look like wood planks. The average home project takes about a week." + "Wood rots. Concrete doesn't. /
  🪵 Wood plank look over your existing slab / 🔨 No demolition, no new pour / 📅 About a week for the average home
  project / Built to look as good in year five as it does on day one. / Concrete Adventures. Decorative concrete in
  Oxford, MS." Headlines: "Day one. Year five." / "The wood look, without the wood"
- Team logo (ad4 + ad5): "That court started as a plain gray slab. / Concrete Adventures put the team's logo and colors
  into concrete the owner already had. We do courts, garages and patios around Oxford." + "It usually starts with one
  backyard. / 🏀 Your team's logo and colors / 🏠 Courts, garages, patios and carports / 🧱 Done over the concrete you
  already have / Then the neighbors come over. / Concrete Adventures. Decorative concrete in Oxford, MS." Headlines:
  "The backyard the neighbors ask about" / "Your team's colors, built into the slab"

Not used: site FAQ "most systems last 10 to 20+ years when resealed" (needs the resealing condition). The copy text
listed in the entry below is V1 and no longer live.

---

## 2026-11-10 — Brand awareness campaign PUBLISHED (Morrow template)

**Ask (Edu):** launch today, "similar to Amazing Morrow, location tight enough so we have the same frequency as Amazing".
Creatives = Drive folder `Approved` `1W1zXdrQ0uhkWKtJAW7cMBPx4UJqx94iS` (Angela confirmed approved 11-10 11:10 BRT).
Source of truth for budget/geo = Ryan's Paid Media Packet (Oxford only, Meta ~$1,860/mo at 3x/week, brand only, no
lead forms, no offers).

**Fence sizing (same math as Morrow's brief):**
- Planning CPM $16.20 (Morrow's). Observed check: the old agency's 'Oxford Garage Leads' (Feb 2026, sales objective,
  all placements) ran $16.65 CPM in this account.
- $1,860 / $16.20 × 1000 = 114,815 impr/mo ÷ 13.03 (3x/wk × 30.4/7) = **~8,800 people held at 3x/week**.
- Census 2020 block groups (TIGERweb, keyless) around the Oxford Square: 3 mi = 21.8k pop, 4 mi = 28.6k. With age 25+
  (≈45–50% of pop here, students) × ~80% on Meta → **3.5 mi ≈ 9–10k**, on target.
- Household-weighted centre landed on campus (BG 280719503012 = 5,254 people / 294 housing units = dorms), so the pin
  is the Square, and hard age_min 25 removes most students.
- ⚠ Census-based estimate. Check Ads Manager's "Estimated audience size" on the ad set; if far off ~9k, resize.

| Level | ID | Name | Settings |
|---|---|---|---|
| Campaign | `52556556297446` | `CA \| BRAND \| AWARENESS \| REACH \| NOV26` | OUTCOME_AWARENESS, AUCTION, **CBO $61.18/day** (6118¢ = $1,860 ÷ 30.4), LOWEST_COST_WITHOUT_CAP, no SAC, no end date |
| Ad set | `52556556309046` | `CA \| OXFORD-SQUARE-3.5MI \| 25+` | Reach / IMPRESSIONS. Pin 34.3665, -89.5193 r 3.5 mi, `home` only. age_min 25 hard (A+A on, age_range 25–65+). Manual placements FB Feed, FB Reels, IG Feed, IG Reels, IG Stories (same 5 as Morrow). **Freq cap 4 / 7 days** (same as Morrow). |
| Ad | `52556556374646` | `CA \| ad3 transformation wood-look patio \| 4x5 \| V1` | creative `1436611771784260`, img hash a22dbaa1… |
| Ad | `52556556376446` | `CA \| ad4 team logo court \| 4x5 \| V1` | creative `1664535175461160`, img hash 5c2925bf… |
| Ad | `52556556378446` | `CA \| ad5 team logo before-after \| 4x5 \| V1` | creative `2112070049412921`, img hash 07cbb69c… |

All ads → `https://www.concrete-adventures.com/` (new Next.js site is LIVE on www as of 11-10, carries GTM-53FXJRN4),
CTA Learn More, every Advantage+ creative feature OPT_OUT. Copy (2 primary texts + 2 headlines per angle):
- Transformation (ad3): "That patio is still concrete. It just stopped looking like it. / Wood-look finish over the
  existing slab. Built to look as good in year five as it does on day one." + "Your old slab doesn't have to come out.
  / We grind it, repair it and finish it so it looks like wood and wears like concrete. Patios, pool decks and
  driveways around Oxford." Headlines: "Day one. Year five." / "Looks like wood. Wears like concrete."
- Team logo (ad4 + ad5): "Your team's colors, on concrete you already own. / Logo floors for backyard courts, garages
  and patios in Oxford. Built to still look like game day years from now." + "It usually starts with one backyard
  court. / Then the neighbors see it. Team logo floors for courts, garages and patios around Oxford." Headlines:
  "Put your team on your concrete" / "Game day starts in the backyard".

Images uploaded via `ads_creative_upload_local_image` → curl POST to rupload (needs headers `offset: 0`,
`X-Entity-Name`, `X-Entity-Length`, `X-Entity-Type`) → `ads_finalize_local_ad_image_upload`. 1x1 versions also
uploaded (hashes 8a08fd7f…, 310ee6f6…, 65d75e3c…) but unused: 4:5 fits all 5 placements and PAC would cap copy at 1 variant.

**Published ~17:15 BRT 11-10** (`ads_activate_entity`, publish_as_active). Draft empty after; live read-back = all 5
objects present, status IN_PROCESS (ad review).

**Open**
1. Confirm ads pass review (IN_PROCESS → ACTIVE) on 11-11.
2. Check Estimated audience size in Ads Manager vs ~9k.
3. Cap 4/7d copies Morrow (Ryan's brief v2) but clashes with Edu's no-cap awareness doctrine; frequency controls lock
   once the campaign starts.
4. Instagram account not linked to the ad account (API returns none).
5. Weekly read (Mondays, from 11-16): actual frequency ≥3.0/wk, reach vs ~8.8k, CPM vs $16.20. CPM well below plan +
   cap hit = fence too small (underspend); frequency < 3 = fence too big → shrink, never cut frequency (packet).
6. Video cuts were due Nov 12 per packet; swap onto winning angle when they land.
