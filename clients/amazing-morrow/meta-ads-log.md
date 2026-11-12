# Amazing Morrow — Meta Ads Log

**Ad account:** Morrow Ads Ad Account `1308410608018843` (owned by the client's business "Morrow Ads" `976611347499623`,
ACTIVE, USD, TSD has partner access). **No payment method on the account as of 2026-11-09** (`has_payment_method: false`).
**Facebook Page:** Amazing Morrow `163803990312902` (reachable through Edu's user page access; it is NOT listed under the
ad account's promoted pages nor under the business's pages, so `ads_get_ad_account_pages` returns empty).

> Running log of paid-social work on this account. Newest entry on top. One entry per work session: what we looked at,
> what we found, what we changed, and what's still open.

---

## 2026-11-09 — Brand campaign built as a DRAFT (not published). Ads pending Héctor's statics

**Source of truth:** Ryan's "Amazing Morrow Campaign Build Brief" v2, revised Oct 29 (Slack DM `D0BB5KT3NLU`
`p1793288568220509`, file `F0CD75RPC2J`). Justin approved $12,500/mo for Nov + Dec, launch Nov 9, fence = 77389 /
77379 / 77375, planning CPM $16.20, ~59,400 adults held at 3.0x. Objective changed in v2 from Ad Recall Lift to
**Awareness / Reach with a frequency cap**, so the floor can be held, not only watched.

**What was found before building**
- Account had zero campaigns (live or draft). Alex's portal flagged the same at 18:36 (DM `D0BNRQZRZNJ`).
- The brief said to launch on existing Wizard of Ads assets. None exist in Drive. Only: two radio spots
  (`Amazing Morrow FIXING FIRST 020426.mp3`, `Morrow Mechanical NEVER TOO LATE 041824.mp3`, uploaded by
  justin@morrowmechanical.com), the Priority Care Club brochure PDF, the logo, the van wrap design, 20 photos and
  12 raw GoPro clips. All seven `TopServ Creative Files` subfolders are empty. Marlo and Alex were asked (no answer yet).
- Héctor is producing **6 awareness statics, Meta only**, on overtime (DM `D0BFF3ATDUN` 18:53). ETA ~Nov 10.
  Video shoot is Nov 17–18 (Marlo, Angela).
- Alex's measured radius was never delivered in Slack (searched "radius" after 10-28: only Ryan's own message).
  Brief's planning figure "about 3.33 mi" was used as a placeholder.

**What was built (Ads Manager DRAFT via Meta MCP, both objects `active_errors: []`)**

| Level | ID | Name | Settings |
|---|---|---|---|
| Campaign | `120251240402700167` | `AM \| BRAND \| AWARENESS \| REACH \| NOV26` | OUTCOME_AWARENESS, AUCTION, **CBO daily $411.00** (41100¢ = $12,500 ÷ 30.4), LOWEST_COST_WITHOUT_CAP, special ad categories NONE, no end date. Draft `validation_status: VALIDATED`. |
| Ad set | `120251240405070167` | `AM \| FENCE-3.33MI \| WEIGHTED-PIN \| 18+` | Optimization REACH, billing IMPRESSIONS. Geo: custom location pin **30.079602, -95.552464** (adults-weighted centre from the brief, not the office), **radius 3.33 mi**, `location_types: home` (people living there). Age 18+ (Meta returned age_range 18–65, i.e. 65+), all genders, no detailed targeting, Advantage+ Audience on. **Manual placements:** FB Feed, FB Reels, IG Feed, IG Reels, IG Stories (`facebook_positions: feed, facebook_reels`; `instagram_positions: stream, reels, story`). Everything else, including Marketplace, Audience Network and FB Stories, is off at the ad set. **Frequency cap 4 impressions / 7 days.** No ad set budget (CBO), no schedule. |
| Ads | — | `AM \| <creative> \| <vertical\|feed> \| V1` | **Not created.** Waiting on Héctor's 6 statics. Use Page `163803990312902`. |

**Deliberate deviations from the brief's naming (section 5 was written before the objective changed)**
- Campaign says `REACH`, not `ADRECALL`. Keeps the `AM | BRAND` prefix Alex's portal searches for.
- Ad set says `FENCE-3.33MI` and `18+`, not `3.83MI` / `18-65`.

**Open before publishing (`ads_activate_entity` on campaign `120251240402700167`)**
1. **No payment method on the ad account.** Launch blocker. Client adds it (through Marlo).
2. **Radius from Alex.** 3.33 mi is a placeholder. Update ad set targeting with `ads_update_entity` once his measured
   figure lands; it changes the ad set name too.
3. **Frequency cap 4/7d** is in the ad set per Ryan's brief. It conflicts with Edu's doctrine (no cap on awareness,
   2026-10-09). Frequency controls lock once the campaign starts (removing later = new campaign), so decide now.
4. **Special Ad Category** set to NONE. Reasoning: Meta's Housing category covers housing sale/rental, home insurance
   and mortgages/home equity; HVAC and plumbing service is not listed. Not verified against a Meta policy article in
   this session. Meta's review of the first ads is the real check.
5. **Account-level Marketplace / Audience Network exclusions** (Ryan: "confirm where they live in this account") cannot
   be read or set through the MCP. The ad set already hard-excludes them. Confirm in Ads Manager account settings.
6. **Ads.** Create 6 ads from Héctor's statics (Reach-objective statics, brand only, no duct cleaning per David, no
   offer), then re-read the draft for errors, then publish.
7. Launch date was Nov 9; earliest realistic publish is Nov 10. At $411/day November lands under the $12,500 cap
   (brief accepts this: 22-day month, no ramp).
8. Instagram: the client's IG login/2FA issue (11-05, Sara) is unresolved. Page-backed IG placements still run.

**Weekly obligation from launch day (Eduardo, every Monday, in writing):** frequency against the fence ≥ 3.0x as a
range measured from delivery; fence adults reached ≥ 90%; impressions within 5% of plan; Marketplace + AN share = 0;
brand CPM reported on brand campaigns only, never account-level. First portal check runs Mon Nov 16.
