# Concrete Adventures — Meta Ads Log

**Ad account:** Concrete Adventures AD Account `25459480633691833` (client BM `409642571461958`, USD, payment on file).
**Page:** Concrete Adventures - Decorative Concrete & Resurfacing `103174475835689`. No Instagram account returned by
`ads_get_ig_accounts` for this ad account (11-10); IG placements run on the Page identity.
**Pixel:** `1475311421329137` "[TSD] Concrete Adventures" (TSD-owned). Not used by this campaign (Reach objective).

> Running log of paid-social work on this account. Newest entry on top.

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
