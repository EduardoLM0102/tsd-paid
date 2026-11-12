# Mission Accomplished: Meta relaunch buildout (internal)

Source: AT Client Request ea5df64f "Relaunch ads" (Brian, 2026-11-03). Prepared 2026-11-06. Nothing built in Meta yet.

## What Brian approved
- Run ads once the campaigns are migrated (new ad account in his portfolio).
- Budget split: Replacement ~60% / Tune-up ~25% / Retargeting + social proof ~15%. **No total given.**
- Higher Intent form on every ad: review/confirm step, required phone, at least one question the customer must answer. "Fewer, real leads."
- Each campaign separate so ServiceTitan can track it.
- Monthly spend export by campaign + past spend Nov 2024 to now (done, see below).

## Blockers before anything can be built or published
New account **2671066020034494** "Mission Accomplished Heating and Cooling" (Brian's business 876938854443027), checked 2026-11-06:

| Item | Status | Who |
|---|---|---|
| Payment method | Missing | Brian |
| Facebook Page (244596582074505) assigned to the ad account | Missing | Brian (Business Settings) |
| ServiceTitan Marketing Pro connected + "Marketing Pro Ads" dataset shared with TSD | No dataset on the account | Brian + Angela |
| Lead Gen ToS on the Page | Unknown until Page is linked | Brian |
| Total monthly budget, in writing | Missing | Brian via Angela |
| Creative approval (winter tune-up, AT #1057) | Still open | Brian via Angela |
| Lead routing test (form → GHL → Hatch with phone), GHL gate | Never confirmed since 09-09 | Mo / Angela |

Why the dataset comes first: it is picked at the ad set level and is locked after publish. Launching without it means rebuilding every ad set.

## Structure (3 campaigns, all CBO, Advantage+ audience, geo only)
Geo for all: people living within 40 km of Lake Havasu City, Bullhead City, Kingman, Parker, Needles (same as the Sep 2026 awareness set). Age 30-65 as a suggestion only.

| Campaign | Share | Objective / optimization | Form | Audience |
|---|---|---|---|---|
| TSD_2026-11_LEADS_CBO_Replacement | 60% | Leads, instant form (conversion leads once the ST dataset is live) | Replacement form | Broad, geo only |
| TSD_2026-11_LEADS_CBO_TuneUp-35 | 25% | Leads, instant form | Tune-up form | Broad, geo only |
| TSD_2026-11_LEADS_CBO_Retargeting-Proof | 15% | Leads, instant form | Replacement form | Page + IG engagers 365d, video viewers 365d, form openers who didn't submit; site visitors once a pixel is on the account |

Naming follows the current pattern; swap when the division naming standard is locked.

Note vs our doctrine: Brian asked for separate campaigns per category, so this is 3 CBOs instead of 1 CBO with angle ad sets. Inside each campaign, angles still go one per DCT ad set. No awareness campaign in his split (he paused it 10-30); adding it back is Edu's call with Brian.

## Lead forms (build in Ads Manager, the MCP can't create forms)
Both: **Higher Intent** type, review screen on, fields = full name, phone (required), ZIP. Thank-you screen with a "Call now" button (confirm which number ServiceTitan wants shown; old ads used 928-517-7702).

**Form 1: "MA Replacement - Higher Intent"** (Brian asked for all three questions, so this goes past the SOP's one-question rule on purpose)
1. How old is your current heating/cooling system? Under 10 years / 10-15 years / 15+ years / Not sure
2. When are you looking to replace it? As soon as possible / In the next 1-3 months / Just getting prices
3. Do you own the home? Yes / No

**Form 2: "MA $35 Tune-Up - Higher Intent"**
1. What time works best for your tune-up? Weekday morning / Weekday afternoon / Flexible
(Optional second question if Brian wants it: system age, same options as Form 1.)

## Creatives
⚠ Lead ad posts carry the form they were built with. Reusing an old post ID brings its old form back, so the old tune-up post can't be reused as-is if it ran on the one-swipe form. New posts with the new forms are the safe default; social proof restarts.

Past ads worth bringing back (Page 244596582074505):

| Ad | Lifetime | Use in |
|---|---|---|
| "35$ tune-up_video" (BOFU-March Special), post 122305140860238337 | $13,370 / 448 leads / ~$30 CPL, but per Brian mostly phantom leads | Tune-up: rebuild the video as a new ad on Form 2 |
| "Image Feed & Reel" (BOFU-0% Financing), post 122233435058238337 | $6,027 / 58 leads | Replacement |
| "Biggest Savings" (BOFU-Rebates Program), post 122257961084238337 | $2,722 / 27 leads | Replacement (check the rebate is still real before reuse) |
| "New system" / "Repair or Replace? We Can Help" ($125/mo), post 122318746304238337 | $385 / 8 leads | Replacement |
| "A New AC for as Low as $125/mo" (Tech + Van), posts 122325075578238337 / 122324092124238337 | ~$271 / 3 leads | Replacement (copy says "Havasu summer", rewrite for winter) |
| Testimonial videos Roger + Kelly, posts 122325082112238337 / 122325082190238337 | Awareness only (no form) | Retargeting + proof, as new lead ads |

Plus Hector's winter tune-up statics once #1057 is approved.

## Past spend export (done)
`Mission Accomplished - Facebook spend by campaign (Nov 2024 - Nov 2026).csv` in this folder. Old account 79203382, Nov 1 2024 to Nov 5 2026, incl. archived/deleted campaigns. Total **$30,754.64**, 18 campaigns; campaign sums match account totals month by month. Jan-Mar 2025 = $2,155.40, matches Brian's $2,155. Leads column = Facebook-reported, not ServiceTitan.

## Build order once unblocked
1. Edu builds the 2 forms in Ads Manager (Page level).
2. Claude builds the 3 campaigns + ad sets + ads as drafts via MCP, dataset selected at ad set level.
3. Joint test lead per form (Meta lead testing tool) → GHL → Hatch with phone → ServiceTitan.
4. Edu publishes. Monthly spend export by campaign goes to Brian on the 1st via Angela.

## AM update draft (for an AT Internal Request to Angela, not created yet)
**Title:** Meta relaunch: what we need from Brian before launch

Update on the Meta relaunch Brian approved in "Relaunch ads".

Done: past Facebook spend by campaign, month by month, Nov 2024 to Nov 2026 (CSV attached). Total $30,754.64. Jan to Mar 2025 comes to $2,155.40, which matches his number.

Needed from Brian on his new ad account (Mission Accomplished Heating and Cooling, in his own business portfolio):
1. Add a payment method.
2. Assign the Mission Accomplished Facebook Page to the ad account.
3. Connect ServiceTitan Marketing Pro to this ad account and share the "Marketing Pro Ads" dataset with TopServ Digital. We pick it when we build the ad sets and it can't be changed after launch, so we wait for it.
4. The total monthly Facebook budget. We'll split it 60/25/15 the way he asked.
5. Approval on the winter tune-up creatives (ticket #1057).

Once those are in, we build the three campaigns (Replacement, $35 Tune-Up, Retargeting and reviews), each with a Higher Intent form: review step, required phone, and the questions he listed. A test lead goes through before anything goes live. The spend export by campaign goes out at the start of each month.
