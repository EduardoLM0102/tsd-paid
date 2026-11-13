---
name: tsd-amazing-morrow
description: Amazing Morrow / Morrow Mechanical, new client Oct 2026; Meta acct 1308410608018843 (NO payment method = only launch blocker), page 163803990312902; 11-12 10 draft ads staged under the 11-09 brand campaign draft (Awareness/Reach CBO $411/d, 3.33mi pin, cap 4/7d), ad6/ad12 held for plumbing logo; GA4 473596484 readable; CallRail accepted 10-21
metadata:
  type: project
---

New client (Morrow Mechanical, site www.amazingmorrow.com). AM = Marlo Fedeli. 2026-10-28 Johnny handed GA4 to Edu in Slack thread C0CANNR1L82/p1793206379855699 (Marlo asked: is GA4 fully set up or do we still need anything from Justin, before the media plan goes to Justin).

State checked 2026-10-28:
- GA4: account 52466601 "Morrow Mechanical", property 473596484 "Amazing Morrow - GA4", stream G-F7ZTSBV7YE. TSD token (eduardo@) reads it. Live and collecting (28d: 1,038 users, 2,026 page views). Nothing needed from Justin for GA4.
- Key events already set: phone_click 83, form_submit 15, contact_form 10, maintenance_form 3, career_form 2. ⚠ form_submit = sum of the 3 named forms (double count), and career_form = job applications, not leads. Clean up before importing into Google Ads (keep phone_click + contact_form + maintenance_form).
- GTM: live site runs GTM-KLMTK37X; invite was for the old GTM-T88GP5C. TSD GTM API login (eduardo@ token) sees NO Morrow account, BUT Edu confirmed 2026-10-28 we DO have GTM access through another email. Nothing needed from Justin.
- CallRail: accepted 10-21 (access@ + johnny@), Johnny made the Google Ads tracking number.
- Site returns ModSecurity 406 to curl; check tags in a real browser.

**How to apply:** if Ryan's brief / media plan still says "GA4 access needed", strike it, nothing is owed by Justin. For GTM API work, use the other login (not the default token). Read [[tsd-ga4-data-api-access]] for the ga4.py recipe.

**2026-10-29 Ryan plan v2 (DM D0BB5KT3NLU/p1793288568220509):** planning CPM $16.20 (Q4), ~59,400 adults held at 3x on $12,500/mo, radius ~3.33 mi pending from Alex (don't derive it), objective → Reach + freq cap 4/7d (⚠ clashes with [[tsd-meta-ads-methodology]] "never cap awareness"; a cap is a ceiling, it doesn't hold a 3x floor), Special Ad Category check first, launch Nov 9. Ryan asked by Nov 4 for the export behind "$5.04 Texas CPM": it is Cool Hand Electric Meta ARL campaign 120249398248040716 (acct 1517373248873821), Sep 9–Oct 8: $599.11 / 118,984 impr / 35,423 reach / freq 3.36 / CPM $5.04, 20 Mansfield–Arlington–S Fort Worth ZIPs, age 30–65, Marketplace on, NO special ad category. Alex missed it because he searched Google data. Ryan also asked where the "205,000 adults at 5 mi" radius table came from (implies 2,610/sq mi vs Census ~1,843); not found in workspace or Slack.

**2026-11-09 Meta build (Edu's go: "build the campaign draft already"):** Meta ad account = "Morrow Ads Ad Account" `1308410608018843`, business "Morrow Ads" `976611347499623`, partner access, **no payment method** (`has_payment_method: false`, launch blocker). Page "Amazing Morrow" `163803990312902` (visible only via Edu's user pages, not under the account or business). Built as an Ads Manager DRAFT, not published: campaign `120251240402700167` `AM | BRAND | AWARENESS | REACH | NOV26` (OUTCOME_AWARENESS, auction, CBO $411/day = $12,500/30.4, no SAC) + ad set `120251240405070167` `AM | FENCE-3.33MI | WEIGHTED-PIN | 18+` (Reach, pin 30.079602/-95.552464 radius 3.33 mi `location_types: home`, 18+, A+A on, manual placements FB Feed/FB Reels/IG Feed/IG Reels/IG Stories, freq cap 4/7d). Zero ads: Wizard of Ads assets the brief said to launch on DO NOT exist in Drive (only 2 radio mp3s, brochure, logo, van design, 20 photos, 12 raw clips); Héctor is making 6 awareness statics on overtime, ETA 11-10. Alex never delivered the measured radius (3.33 is the brief's placeholder). Full build + open list in `clients/amazing-morrow/meta-ads-log.md`.
- Open before publish: payment method; Alex's radius; cap 4/7d vs Edu's no-cap doctrine (locks at start); SAC left NONE (HVAC/plumbing service isn't Housing by policy, unverified this session, Meta review is the check); account-level Marketplace/AN exclusions not readable via MCP, ad set already hard-excludes them; publish = `ads_activate_entity` on the campaign after ads are added and the draft re-read.
- First portal weekly check Mon 11-16 looks for the `AM | BRAND` prefix. Mechanics in [[tsd-meta-mcp-write-mechanics]]; doctrine clash in [[tsd-meta-ads-methodology]].


**2026-11-12 build (Edu: "help with the launch"):** Justin approved Héctor's statics (Marlo 11:49 BRT) on condition every ad carries
the new "Cooling, Heating & Plumbing" logo. Drive `FOR APPROVAL` (`1901ha0BvUXBKZPOss4iUpelkm_CXnxIr`) = 12 statics, 6 angles × 2
layouts (`Var 2` ads 1–6, `Var 1` ads 7–12), 1x1/4x5/9x16 each. The 10 re-exported on 11-10 (ads 1–5, 7–11, `_2026-11-10_` files)
have the plumbing logo (checked by eye). **ad6 + ad12 (van, "Say there, fella!") only exist as `_2026-11-09_` files with no logo
block** → held. Never use a `_2026-11-09_` file. 10 ads STAGED in the draft under ad set `120251240405070167` (IDs + copy V1 in
`clients/amazing-morrow/meta-ads-log.md`), 4x5 only, 2 primary texts + 2 headlines per angle, Learn More → www, A+ creative all
OPT_OUT, IG `17841468361617084` attached. Every object VALIDATED; the only `active_error` is **No Payment Method (1359188)**.
Publish = `ads_activate_entity` campaign `120251240402700167` publish_as_active, once the card is in. **11-12 evening: Edu asked Marlo
to have Justin add the card** (billing hub link for business `1664180080536776` / asset `1308410608018843` is in the log).
⚠ Edu can't add the card himself, even with the number: his IP country doesn't match the account currency and Meta rejects it,
so it must be Justin or someone on the client's side.

**How to apply:** Meta refuses Drive `uc?export=download` URLs → download with curl, then `ads_create_upload_url` → curl POST →
`ads_finalize_upload`. Concrete template = Morrow template (same ad structure, copy pattern, no PAC). Follow-ups: payment method
via Marlo (nobody had asked as of 11-12), ad6/ad12 logo (Héctor), Alex radius still missing, Sara needs a social CallRail number
(Johnny), AT onboarding stages 5a–5d + 7b and the portal checklist are Edu's to tick. Related: [[tsd-concrete-adventures]],
[[tsd-meta-mcp-write-mechanics]], [[tsd-meta-ads-methodology]].
