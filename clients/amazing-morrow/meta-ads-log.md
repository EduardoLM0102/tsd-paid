# Amazing Morrow — Meta Ads Log

**Ad account:** Morrow Ads Ad Account `1308410608018843` (owned by the client's business "Morrow Ads" `976611347499623`,
ACTIVE, USD, TSD has partner access). **No payment method on the account as of 2026-11-09** (`has_payment_method: false`).
**Facebook Page:** Amazing Morrow `163803990312902` (reachable through Edu's user page access; it is NOT listed under the
ad account's promoted pages nor under the business's pages, so `ads_get_ad_account_pages` returns empty).

> Running log of paid-social work on this account. Newest entry on top. One entry per work session: what we looked at,
> what we found, what we changed, and what's still open.

---

## 2026-11-16 — PUBLISHED. Campaign live with 12 ads (Edu: "do the adjustments you need and push live")

**Built ad6 + ad12** from Héctor's 11-13 4x5 exports (16:05 UTC set), uploaded via `ads_create_upload_url` → curl → `ads_finalize_upload`:

| Ad | ID | Creative | Image hash |
|---|---|---|---|
| `AM \| ad6 say there fella \| 4x5 \| V1` | `120251380325360167` | `2207182750179920` | 36b7aba9… |
| `AM \| ad12 say there fella alt \| 4x5 \| V1` | `120251380326210167` | `1116068334378719` | 6a40a7f2… |

Same structure as the other 10 (Page + IG `17841468361617084`, Learn More → www, A+ creative features OPT_OUT, self-AI disclosure unset).
Copy V1 (only facts already verified in the 11-12 copy, no phone, no offer):
- "Houston comfort is one call away. / Cooling, heating or plumbing, one call to Ammmazing Morrow brings the same family crew
  that has served Spring and north Houston since 2000. Upfront prices, fixed right the first time."
- "Say there, fella! Too hot, too cold or the pipes acting up? A call to Morrow is all it takes. / 🚐 One crew in blue for
  cooling, heating and plumbing / 🌙 After-hours service at no extra charge / 🏠 Locally and veteran owned since 2000 /
  Ammmazing Morrow. Spring and north Houston."
- Headlines: "Houston comfort is one call away" / "A call to Morrow is all it takes"

**Publish:** first `ads_activate_entity` was REFUSED: the 10 ads staged 11-12 still carried the `1359188 No Payment Method`
error saved at staging, even though the card is on the account. **Fix = re-save each staged ad** (`ads_update_entity` with
its same `name`) → Meta re-validates, error gone. Then `ads_activate_entity` campaign `120251240402700167`, publish_as_active.

**Live read-back:** campaign, ad set and all 12 ads `status ACTIVE`, `effective_status IN_PROCESS` (Meta review).
Ad set confirmed: cap 4 impressions / 7 days, pin 30.079602/-95.552464 r 3.33 mi, home, 18–65+, A+A on, FB feed + reels,
IG stream + story + reels only.

**Kept as built (Edu said push live, no change asked):** cap 4/7d (now locked), 3.33 mi radius placeholder.

**Open:** confirm review passed + first delivery (~11-17); first weekly frequency read moved to 11-23 (fu-143); Alex's radius;
Sara's social CallRail number; AT onboarding 5a–5d + 7b and the portal checklist.

---

## 2026-11-16 — Go/no-go check (read-only, nothing changed)

- **Payment method is now on the account** (`has_payment_method: true` on 11-16). Activity log shows no entries since 11-12
  (billing changes don't appear there), so who added it and when is not visible via the MCP.
- **Still not published:** 0 live campaigns. Draft campaign + ad set `VALIDATED`; the 10 ads still carry the stored
  `1359188 No Payment Method` error from staging (stale, expected to clear on publish; if publish refuses, re-check billing in Ads Manager).
- **ad6/ad12 fixed:** Héctor's `_2026-11-13_` exports (ad6 4x5 `14p0hdAowoOjvyBDiLUbR-kfLm56vgtzN`, ad12 4x5
  `1MYcRDy86SMphdJFYoKP4Rd3elnrKWTCZ`, both 16:05 UTC) checked by eye: van wrap now reads "Cooling, Heating & Plumbing".
  An earlier 15:54 UTC set also exists in another folder; use the 16:05 files. Ads not created yet.
- Still open from 11-09: frequency cap 4/7d (locks at start), radius 3.33 mi placeholder (Alex). Portal weekly check is today and will see nothing live.

---

## 2026-11-12 — 10 ads STAGED in the draft. Only blocker left: no payment method on the ad account

**Context:** Marlo (#onboarding-amazing-morrow 11:49 BRT): Justin approved the creatives but wants the new logo with plumbing on
ALL of them; at 13:49 she asked everyone to close onboarding by Thursday (4-week mark). Edu replied: campaign launched before EOD.
Alex's portal runs its first weekly check Mon 11-16 looking for `AM | BRAND` campaigns.

**Creative audit (Drive `FOR APPROVAL` `1901ha0BvUXBKZPOss4iUpelkm_CXnxIr`, Héctor):** 12 statics = 6 angles × 2 layouts
(`Var 2` = ads 1–6, bold-serif layout; `Var 1` = ads 7–12, rounded-card layout), each in 1x1 / 4x5 / 9x16. Johnny re-exported
ads 1–5 and 7–11 on 11-10 21:57 UTC (after Marlo posted the plumbing logo 19:28 UTC); every one of those 10 verified by eye
to carry "COOLING, HEATING & PLUMBING". **ad6 and ad12 ("Say there, fella! Houston comfort is one call away", van photo)
only exist in 11-09 versions, have NO logo block, and the van wrap reads "Cooling & Heating"** → held back, Héctor to add the
plumbing logo. Stale 11-09 files for ads 1, 2, 5, 7, 8 are still in the folders (cannot trash, shared drive read-only for the
Drive token): never use a `_2026-11-09_` file.

**Build (Concrete template, 4x5 only, no PAC so copy keeps 2+2 variants):** 10 ads under ad set `120251240405070167`, each
`creative_id` with `primary_texts` ×2 + `headlines` ×2, link `https://www.amazingmorrow.com/`, CTA Learn More, every
Advantage+ creative feature OPT_OUT, Page `163803990312902`, Instagram `17841468361617084` (Meta attached it by default,
so the Page does have an IG linked; asset 407921932404735). Images via `ads_create_upload_url` → curl → `ads_finalize_upload`
(the Drive `uc?export=download` URL is refused by Meta's fetcher; curl -L from the Mac works).

| Ad | ID | Creative | Image hash |
|---|---|---|---|
| `AM \| ad1 we fix first \| 4x5 \| V1` | `120251319807400167` | `1129298579645052` | 43dfd1ad… |
| `AM \| ad7 we fix first alt \| 4x5 \| V1` | `120251319807430167` | `1442578380758109` | da9fc47a… |
| `AM \| ad2 still locally owned \| 4x5 \| V1` | `120251319807530167` | `2919239175119733` | 4082f70a… |
| `AM \| ad8 still locally owned alt \| 4x5 \| V1` | `120251319807680167` | `1146695227759017` | f89a065e… |
| `AM \| ad3 now ammmazing morrow \| 4x5 \| V1` | `120251319807770167` | `1476304934409024` | 9ce72951… |
| `AM \| ad9 now ammmazing morrow alt \| 4x5 \| V1` | `120251319807980167` | `1133188329424268` | 819721a2… |
| `AM \| ad4 now plumbing \| 4x5 \| V1` | `120251319808230167` | `1611007866915609` | 08ce4f8c… |
| `AM \| ad10 now plumbing alt \| 4x5 \| V1` | `120251319808370167` | `1486930819979279` | 54bef942… |
| `AM \| ad5 top 5 lennox \| 4x5 \| V1` | `120251319808440167` | `1028824943570880` | ef94e3fa… |
| `AM \| ad11 top 5 lennox alt \| 4x5 \| V1` | `120251319808470167` | `1758102438600487` | 7897946c… |

(Creatives `2401942893966504` / `4838545756390953` = first versions of ad1/ad7 without the IG id, unused.)

**Copy V1 (ogilvy-copy skill; facts from amazingmorrow.com, the approved statics and the Wizard of Ads style guide
"Say there fella!", "technicians first, sales second", "no replacements without proper diagnosis"; no phone, no offer, no duct cleaning):**
- We fix first (ad1/ad7): "Most companies push a new system. Mr. M fixes what can be fixed. / Ammmazing Morrow has sent
  technicians first and salespeople second since 2000. No replacement without a proper diagnosis, and after-hours service at
  no extra charge." + "Say there, fella! Before anyone sells you a new system, let us look at the old one. / 🔧 We fix first.
  Replacement only when it's really needed / 🧾 Upfront price, fixed right the first time / 🌙 After-hours service at no
  extra charge / Ammmazing Morrow. Honest cooling, heating and plumbing in Spring and north Houston since 2000."
  Headlines: "We fix first. Since 2000." / "Technicians first. Sales second."
- Still locally owned (ad2/ad8): "No investment group calling the shots. Just your neighbors keeping Houston comfortable
  since 2000. / Ammmazing Morrow is still locally and veteran owned. Same family, same crew in blue that has been on your
  street for over two decades." + "Houston born. Houston run. / 🏠 Locally and veteran owned since 2000 / 👕 The same
  family and the same crew in blue / ⭐ BBB A+ rated, Winner of Distinction for 10+ years / Ammmazing Morrow. Cooling,
  heating and plumbing in Spring and north Houston." Headlines: "Still locally owned. Since 2000." / "Your neighbors, not a corporation."
- Now Ammmazing Morrow (ad3/ad9): "Morrow Mechanical is now Ammmazing Morrow. Same family. Same promise. / New name on the
  vans, same crew that has kept Spring and north Houston comfortable since 2000. Honest work, upfront prices, fixed right
  the first time." + "Say there, fella! You've seen the orange vans for years. Now they say Ammmazing Morrow. / 🚐 Same
  family, same technicians / 🤝 Same promise: honest work, fixed right the first time / 🚿 Plumbing now too, alongside
  cooling and heating / Ammmazing Morrow, formerly Morrow Mechanical. Spring and north Houston since 2000."
  Headlines: "Morrow Mechanical is now Ammmazing Morrow" / "New name. Same family. Same promise."
- Now plumbing (ad4/ad10): "Cooling. Heating. Now plumbing. / The team Houston has trusted for comfort since 2000 now takes
  care of your pipes, drains and water heaters too. Same technicians-first approach, same upfront pricing." + "Say there,
  fella! Mr. M does plumbing now. / ❄️ Cooling / 🔥 Heating / 🚿 Now pipes, drains and water heaters / One crew in blue for
  the whole house. Ammmazing Morrow, Spring and north Houston since 2000." Headlines: "Now plumbing, too." / "Cooling. Heating. Now plumbing."
- Top 5% Lennox (ad5/ad11): "Top 5% of Lennox dealers in North America. That's the Lennox Centurion Award, and Ammmazing
  Morrow earned it. / Add a BBB A+ rating, Winner of Distinction for 10+ years and NATE-certified technicians, and you know
  who to call for cooling, heating and plumbing in Spring." + "Say there, fella! Awards don't fix air conditioners.
  Technicians do. Ours just happen to be recognized for it. / 🏆 Lennox Centurion Award, top 5% of dealers in North America /
  🛡️ BBB Winner of Distinction, 10+ years / 🎓 NATE-certified technicians / Ammmazing Morrow. Cooling, heating and plumbing
  in Spring and north Houston since 2000." Headlines: "Top 5% of Lennox dealers in North America" / "Lennox Centurion Award winner"

**Draft state after the build:** campaign + ad set + 10 ads, every object `VALIDATED`; the ONLY `active_error` on every ad is
`1359188 No Payment Method` (account-level). Nothing else blocks `ads_activate_entity` on campaign `120251240402700167`
(publish_as_active). Not published.

**Open**
1. **Payment method** on `1308410608018843`: client adds it (through Marlo). Nobody had asked for it in Slack as of 11-12 18:45;
   Edu's ask to Marlo went out 11-12 evening with the billing link
   `https://adsmanager.facebook.com/adsmanager/billing_hub/accounts/details/?business_id=1664180080536776&asset_id=1308410608018843&payment_account_id=1308410608018843`
   (session_id stripped; it was Edu's own session). **Justin or someone on his side has to add the card: Edu cannot add it
   himself even with the card number, because his IP's country doesn't match the account's currency and Meta blocks the
   payment method.** Marlo was also told ad6/ad12 are held for the plumbing logo and that we launch with the other 10.
2. ad6/ad12 plumbing logo (Héctor) → then upload 4x5 + create 2 more ads (`AM | ad6 say there fella | 4x5 | V1`, `AM | ad12 … alt`).
3. Alex's measured radius still not delivered (3.33 mi placeholder stays). Concrete lesson: check Ads Manager audience size vs ~59,400 at publish.
4. Frequency cap 4/7d kept (same as Concrete / Ryan's brief); locks at start.
5. Self-AI disclosure left unset on all creatives (none of the statics are AI-generated; Edu's call).
6. Sara (social) still needs: FB+IG connected confirmation and a social CallRail tracking number (Johnny owns CallRail; Concrete got (662) 960-6539).
7. AT onboarding `3f6ca7c5…` stage 5 "Paid Ads Setup" 5a–5d and 7b "Paid Ads Strategy Audit Deliverable" are not started; Alex's portal checklist also has Edu items to tick.
8. First portal weekly read Mon 11-16 (campaign must be live with the `AM | BRAND` prefix, which it has).

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

**2026-11-17 10:29 CT, 24h post-launch check (read-only, no changes):**
- Campaign/ad set/12 ads all ACTIVE, no errors. Spend $412 total (11-16: $327.05, 11-17 so far: $84.95). 64,929 impr, reach 59,214, freq 1.10, CPM $6.35 (plan assumed $16.20).
- Placements even: IG Feed $132 / IG Reels $87 / IG Stories $75 / FB Feed $74 / FB Reels $42, all ~$6.3 CPM. Marketplace + AN = 0 ("unknown" 66 impr, $0.36).
- Creative split: ad3 $121.50, ad5 $89.96, ad8 $53.63, ad9 $37.39, ad12 $33.72; ad1/ad7/ad10 under $6 each.
- ⚠ Pacing math: at $6.35 CPM, $411/day buys ~453k impr/week = ~7.6x/week on ~59k adults, but cap 4/7d allows only ~238k/week (~$1.5k/week, ~$215/day). Expect spend to fall once people hit the cap (~11-19/20). Options for Ryan: accept underspend, or widen the fence (the same budget holds 3–4x on roughly 2x the adults). Cap can't be removed without a new campaign.
