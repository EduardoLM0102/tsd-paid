---
name: tsd-zen-air
description: "Zen Air (Gwinnett GA HVAC) account IDs, the 2026-07-31 spend-cut ticket outcome, and the finding that the client paused his own LSA"
metadata: 
  node_type: memory
  type: project
  originSessionId: ee64c040-ed6d-4c05-8de3-d240f7d761eb
  modified: 2026-09-15T09:02:59.874Z
---

**Zen Air Heating and Cooling** — HVAC, Gwinnett / North Atlanta GA. Client: Eddie (eddie@callzenair.com). AM/analyst: Andrea.

**Accounts:**
- Google PPC `4360840956` (MCC Topservdigital `4155514468`)
- Google LSA `3740502923` — **separate account**, not nested in the PPC account (unlike [[tsd-golden-plumbing]] where LSA sits inside the Google Ads account)
- Meta `381256660973192` — "Zen Air - Third Ad account ( Active Account)", business `905124767666377`. There are two decoy Zen Air Meta accounts; `10203380240686685` is CLOSED. Pick the third one.

Working log: `topserv-workspace/clients/zen-air/`. Earlier findings doc `2026-07-09-geo-and-account-findings.md` (billing stop, geo/network artifact, broad-keyword problem) still relevant.

## 2026-07-31 spend-reduction ticket — what was found

Baseline, last 30 days (PPC only served 21 of them, resumed Jul 10 after the June billing stop):

| Channel | Spend | Leads | CPL |
|---|---|---|---|
| PPC Search `TSD_05.13_Search_Branded_Evergreen` (23675783172) | $4,551 | 14 | $325 |
| PPC PMax `TSD_03.23_PMAX_HVAC_Calls` (22959264938) | $2,479 | **1** | $2,479 |
| LSA | $766 | 10 | $77 |
| Meta | $2,804 | 297 | $9 |

- **PMax spends 73% ($1,814) on YouTube/Display/Discover/Search Partners for zero conversions.** Only its Search slice converted, once. This became the single recommendation.
- **Search campaign is on MAXIMIZE_CONVERSIONS with no CPA cap**, so it spends whatever budget it is given at whatever CPC it wants. Brand keywords cost **$18.45 average CPC** (`zen air heating and cooling` $22.76) at QS 8 with Above Average relevance and landing page. Quality Score is not the cause, the uncapped bid strategy is. Brand only gets ~5.5 impressions/day and sits at 81–100% IS, so true brand-defense need is ~$15/day, not the $28/day it currently costs.
- **63.3% of impression share lost to Ad Rank vs 22.6% to budget.** The campaign is overpaying, not underfunded. `hvac contractors near me` (broad, 75% of campaign spend, $571 CPL) rates **Below Average on landing page experience** — this is the number that justifies fixing landing pages before touching budget.
- **Negatives and match-type changes do NOT cut spend** on a budget-capped campaign, they redirect it. I initially counted them as cash savings and Edu caught it. Only lowering the daily budget, or pausing, is a real cut.

## The client paused his own LSA

`change_event` on LSA account 3740502923: **2026-07-03 13:33:47, `eddie@callzenair.com`, GOOGLE_ADS_WEB_CLIENT, campaign 20752144554, status ENABLED → PAUSED.** Only event in the window. Evidence exported to `clients/zen-air/lsa-pause-evidence-2026-07-03.txt`.

He turned off his cheapest source ($57–77/lead, only ~$1,860 all year) and then raised a ticket saying he overspends for the results. Handling: do NOT put "you paused it" in the reply. Escalation material for Ryan only. Brief the CSR so she isn't blindsided.

**Gotchas found doing this:** `change_event` API retention is only 30 days and the query **requires a LIMIT**; the Google Ads UI keeps ~2 years. LSA accounts may not expose Change history in the UI, and the campaign selector defaults to excluding paused campaigns, which hides exactly the event you are looking for.

## What was actually delivered

Ticket reply scoped to **PMax only**, ~$3,000/mo saved. Search budget deliberately left alone because a landing-page restructure is coming that should lower CPL first. Meta awareness campaign explicitly protected — brand video exposure is part of Brandformance and Edu said it is never a cut candidate; it is also the argument that justifies cutting PMax ("we already do that on Meta where we control audience, creative and frequency").

Plan doc: `clients/zen-air/2026-07-31-spend-reduction-plan.md`. Message style for the reply itself is in [[tsd-client-message-style]].

## 2026-07-31 — EXECUTED (supersedes "Search left alone" above)

Edu then asked to actually pull the trigger, and to move half the PMax budget into Search. Applied and verified in-account via `clients/zen-air/change_pmax_off_search_up.sh`:

- PMax `TSD_03.23_PMAX_HVAC_Calls` (22959264938): ENABLED $100/day → **PAUSED**
- Search `TSD_05.13_Search_Branded_Evergreen` (23675783172): **$150 → $200/day**
- PPC account daily budget $250 → $200. The other $50/day left the account with no destination decided.

Edu chose **not** to pause the broad keyword in the same change, after I flagged it. So the +$50/day lands mostly on `hvac contractors near me` (BROAD, 75% of campaign spend, $571 CPA) rather than the brand exacts (`zen air heating and cooling`, $76 CPA). **Expect the Search blended CPA to get worse before it gets better** — this is a known, accepted consequence, not a regression to go hunting for. Recheck ~2026-08-14; the real fix is splitting non-branded into its own campaign so the "Branded" campaign is actually branded.

Executed on Edu's verbal authority, so an **AM ticket (Andrea) is still owed** to register the budget change in writing — MasterOps requires written client approval. That is now the third open ticket debt of this kind (All Heart 07-10, GC Home Service 07-28). Logged in `clients/zen-air/google-ads-log.md` (created in this session) + `tarefas.md`.

Watch out: Edu opened this asking to do it on **Spencer Air**, which has no PMax at all — see [[tsd-spencer-air]]. Confirm the account before executing when a client name and a symptom don't line up.

## 2026-08-24 — full review, found the branded/nonbranded split (good) has a network bug (bad)

The 07-31 recommendation to split branded from non-branded got implemented: `TSD_08.03_Search_NonBranded_Evergreen` (24100030790, $100/day) launched alongside the existing branded campaign (also now $100/day). PMax stays correctly paused.

**But the new non-branded campaign has Search Partners AND Display Network both switched on** (`network_settings.target_search_network=true`, `target_content_network=true`), unlike branded which is correctly Google-Search-only. Lifetime since launch (Aug 3–24): real Google Search = 422 clicks/$341/10 conv ($34 CPL, actually a good number); Search Partners = 9,286 clicks/$1,771/494 conv ($3.59 CPL — 80% of spend, 97% of "leads"); Display = 2,525 clicks/$102/3 conv. Search Partners converting *better* than real Search (5.3% vs 2.4%) is backwards and reads as junk/bot form-fills, not real HVAC demand — 494 leads in 3 weeks from this account is implausible against the July baseline of 14 real leads/month. The conversion actions themselves are legit categories (`SUBMIT_LEAD_FORM`: "Submit lead form - web", "ghl_contact_us") — this isn't a tracking-goal problem like Proud Pops, it's a network-targeting problem. ClickCease is active on the account (auto-adding IP-block negatives to this campaign) but can't fix a network-settings checkbox.

**Real vs. reported, Aug 3–24**: reported/blended = 510 leads, $8.27 CPL. Real (Search-only) = 13 leads, $180.46 CPL (branded alone: 3 leads, $668 CPL — climbing CPC, still on uncapped `MAXIMIZE_CONVERSIONS`, never addressed since 07-31). 22x gap between what the dashboard shows and reality.

**FIXED 2026-08-24**: `target_search_network`/`target_content_network` flipped to `false` on campaign 24100030790, verified live. First attempt was blocked by the local Claude Code permission classifier (live client-account mutation); Edu added a project-scoped Bash allow rule (`.claude/settings.local.json` in topserv-workspace, matching `cd .../google-ads-ratos/scripts/ && ./tsd.sh *`) and it went through on retry.

**This turned out to be a book-wide issue, not a Zen Air one-off** — see the network-trust-check section added to [[tsd-weekly-ppc-snapshot]] for the full cross-account audit (11 of 18 accounts affected). Root cause: `create.py` hardcoded Search Partners on for every Search campaign build, no opt-out. **Also fixed 2026-08-24**: `create.py` now defaults new Search campaigns to Google-Search-only (`target_content_network=False`, `target_search_network` gated behind a new `--include-search-partners` opt-in flag, off by default). The other 9 already-affected live accounts (Cool Hand Electric, All Heart, Lilypad Septic, Gillespie's, Watt's Right, All Seasons AC, Proud Pops, King's Window) were NOT touched — that's a separate rollout decision per account, not done as part of this Zen Air fix.

Meta side (381256660973192) is clean: only the protected TOFU Brand Awareness campaign is live, 7d = $459.85 spend/34 leads/$13.53 CPL — softer than July's ~$9 CPL/~69 leads-per-week pace but not urgent.

## 2026-08-31 — checked account after the 08-24 fixes, found a new unrelated problem

The 08-24 network fix and branded bid-strategy fix both confirmed holding: non-branded (24100030790) has served 100% real Google SEARCH since 08-25 (no more Search Partners/Display), branded (23675783172) still correctly on TARGET_IMPRESSION_SHARE 90%/$4 ceiling.

**New issue, unconnected to the 08-24 work**: `change_event` shows that on 08-26 12:29–12:31pm, non-branded campaign 24100030790 got 5 new PROXIMITY criteria added (7-mile radius circles, via GOOGLE_ADS_API under eduardo@topservdigital.com) and its `geo_target_type_setting.positive_geo_target_type` was toggled PRESENCE_OR_INTEREST→PRESENCE→PRESENCE_OR_INTEREST→PRESENCE (3x in 2 min, via GOOGLE_ADS_WEB_CLIENT, same user — looks like manual testing that didn't get reverted). Current state: these 5 circles are the campaign's *only* location targeting (no LOCATION-type criteria present), set to PRESENCE (physical-presence-only, no "or interest").

Effect: campaign nearly stopped serving. 08-25/26 still had 739/953 impressions (old broader targeting still propagating); 08-27 and 08-28 = 0 impressions; 08-29 = 5; 08-30 = 23. `search_budget_lost_impression_share` dropped to 0% those days — this isn't a budget or Ad Rank constraint, the auction pool itself collapsed because the geo footprint is now just 5 small 7-mile circles instead of whatever broader area was targeted before. Plausible read: someone was consolidating the old paused single-city campaigns (Suwanee/Cumming/Buford/Alpharetta/Lawrenceville, all paused, see the full campaign list) into proximity circles inside this one campaign, but left it too narrow and/or on Presence-only. **Not yet confirmed with Edu whether this was intentional** — flagged to him 2026-08-31, waiting on answer before touching it.

**2026-08-24, same session — branded bid strategy fixed too**: branded (23675783172) was still on uncapped `MAXIMIZE_CONVERSIONS` from before, letting CPC climb to $37–39 on its own brand name with only 1–3 real conversions/week (too little signal for Smart Bidding to optimize on). Switched to `TARGET_IMPRESSION_SHARE`: TOP_OF_PAGE, 90% target, $4.00 CPC ceiling — matches the campaign's real job (brand-defense visibility) instead of forcing conversion-based bidding onto a campaign that structurally can't feed it enough data. Confirmed live via GAQL. Non-branded (24100030790) left on Maximize Conversions — it has real signal now (10 real conversions/21 days, $34 CPL post-fix) but not enough volume yet for Target CPA; revisit in 3-4 weeks. Full reasoning and before/after numbers logged in `clients/zen-air/google-ads-log.md` (2026-08-24 entry). Open follow-ups: AM ticket to Andrea now covers three unlogged changes (07-31, 08-03, 08-24) — worth bundling; confirm with Eddie/GHL whether the ~500 Search-Partners "leads" from Aug 3-23 were real; recheck actual achieved impression share on branded in ~7-10 days (raise the $4 ceiling if it's landing well under 90%).

**Same day — GTM audit found a second, unresolved tracking anomaly.** GTM account `6069423387` ("Zen Air Heating & Cooling - active", decoy "Zen air 1" = 6366481766 ignore), container `100567467` (GTM-KCZ2GTP, callzenair.com), workspace 29. Checked whether "leads" are really page-views in disguise (the All Seasons AC `book_now_link_click` pattern) — mixed result:

- **"Submit lead form - web" is genuinely verified**: tag `cHTML - GHL Form Listener` [84] only pushes `form_submitted` to the dataLayer when a GHL embedded-form `postMessage` contains a real captured email; trigger `cEvent - Lead` [54] (plus `Booked Appointment` [96] and `Quote Lead` [95], the results-page reached) fire the actual Lead tags off that. Not the problem.
- **`ghl_contact_us`, `ghl_service_area`, `ghl_city_page`, `ghl_schedule_services`, `ghl_request_estimate` (and `book_now_link_click`) don't exist anywhere in this GTM container** — no tag or trigger creates them. Almost certainly a native GoHighLevel→GA4 push bypassing GTM entirely, one event per funnel page, most likely firing on page view not submission. Not confirmed with GHL/Eddie — inferred from absence-of-evidence + naming pattern, don't assert as fact.
- **Why it matters for bidding, not just reporting**: Google Ads goals bundle by category+origin, not per action. `ghl_contact_us` shares the `SUBMIT_LEAD_FORM`/`WEBSITE` bucket with the verified form action (and carries more weekly volume — 82 vs the form's share of 113 total), so Smart Bidding can't currently separate real signal from suspected page-view noise. `ghl_service_area` shares `PURCHASE`/`WEBSITE`, biddable on non-branded.
- **Not fixed** — recategorizing these out of the shared bucket is a bigger, more visible change than the network/bid-strategy fixes (changes how leads get counted/reported on a live account), so it's parked pending confirmation with GHL/Eddie on what these events actually measure. Full writeup in `clients/zen-air/google-ads-log.md`, second 2026-08-24 entry.

## 2026-09-15 — GA4 corroborates the Aug 23-24 Display leak was junk, not real demand

Checked GA4 property `350001559` (Zen Air Heating & Cooling - GA4) for phone-number-click-without-lead gap. Real verified form lead event is `generate_lead` (GTM-gated on the real GHL form listener capturing an actual email, per the 08-24 GTM audit above — trustworthy). `phone_click` is a raw tap on the tel: link, no connection/duration signal (unlike Google Ads' PHONE_CALL_LEAD "Calls from ads" which requires 60s+ connected).

**Last 30 days**: 203 `phone_click` events, but 137 of them (109 users) are bucketed under GA4's "Display" channel and landed almost entirely on **2026-08-23 (87) and 08-24 (46)** — the exact tail end of the Search-Partners/Display network leak on non-branded (24100030790) fixed 08-24 (see above). Only 3 of those 137 Display-bucketed sessions produced a real `generate_lead` in the whole 30-day window — ~98% went nowhere. Since 08-25 this Display-channel phone_click volume is essentially zero (0-1/day), confirming the network fix held and this was a one-time leak artifact, not an ongoing pattern.

On the clean channel (google/cpc, i.e. actual Search): `phone_click` = 49/30d vs `generate_lead` = 223/30d from the same source — form conversion is doing the real work here, phone isn't a meaningful leak point on legitimate traffic.

**Also confirmed while in there**: Google Ads-side `Submit lead form - web` shows 160 conversions over LAST_30_DAYS (healthy, roughly matches GA4's `generate_lead` order of magnitude — no evidence of a lead-import gap between GA4 and Google Ads on this account). `ghl_contact_us` (the suspected page-view-not-submit action flagged 08-24, still unconfirmed) logged 113 more in the same bucket.

Non-branded 14-day pull (09-01/02 through 09-15) shows the account isn't at zero — 6 conversions/$1,806 spend over 14 days vs. just 1 conversion in the most recent 7 — so week-to-week noise, not a full collapse. Still worth revisiting whether the 08-26 proximity-circle/geo-targeting issue (flagged to Edu 08-31, never confirmed resolved) is suppressing volume, since that's still open.

## 2026-09-07/08 — phone number ambiguity on CALL assets, still unresolved

09-07 weekly check found **3 different phone numbers** live across CALL assets on this account ((770) 282-1481 account-level, (678)-853-7440 campaign-level on branded, 678-329-9929 on a dormant campaign). Edu said not to use any phone extension until it's clear which number is correct, so all 3 were paused (status PAUSED, not deleted).

09-08: Edu then asked to add a **4th number**, 678-606-8817, as a new account-level CALL asset — created and left ENABLED per his direct request. This contradicts the "don't use any until clarity" instruction from the day before; flagged it back to him in the log (`clients/zen-air/google-ads-log.md`, 2026-09-08 entry) rather than assuming it's the resolution. **Not confirmed** whether 678-606-8817 is the definitive number or what should happen to the other 3 (delete vs. leave paused) — check before touching call assets on this account again.

Also same 09-07 check: ceiling on branded Target IS raised $4→$8 on the read that branded was rank-limited on its own name. **That read was WRONG (found 09-30):** the lost IS came from the `zen air` BROAD keyword entering generic HVAC auctions. The raise let it win them ($665, 0 conv since). Always split branded IS by keyword/match type before blaming bid competition.

## 2026-09-30 — cost-per-conversion deep dive (read-only). Doc: `clients/zen-air/2026-09-30-ppc-cost-deep-dive.md`

Clean 30d (08-31..09-29): $5,038, 20 reported conv ($252) but ~13-14 real leads (12 connected 60s+ calls via `call_view` + 1-2 forms) = **~$360-390/real lead**. Non-branded = 84% of spend at $28 CPC.
- **87% of visible non-branded spend = competitor names** (Shumate, Coolray, Bardi, Goodman, Lennox help line, e dennis plumbing x3 conv...). Cause: 4 BROAD kws in 1 ad group, zero negatives, uncapped Max Conv at $150/d. `hvac contractors near me` BROAD = 60% of account spend, QS 3.
- Branded `zen air` BROAD: $1,625 since 08-17, 0 conv. Real brand need ~$4/day vs $50 budget.
- LP `/book-hvac-service/` (live 09-15): 41 paid sessions, 0 forms (GA4). Account is ~all phone.
- `[TSD] Click to call` (09-15 rebuild) = type CLICK_TO_CALL (a tap), primary+biddable, shares bucket with `Calls from ads`.
- LSA re-enabled 09-10 by access@topservdigital.com; ~15 impr/day, most LSA leads DECLINED business-side.
- 7 recommendations handed to Edu, nothing executed. Order: pause brand broads + ceiling ~$5 → cap NB bidder (Max Clicks ~$15-18) → shared competitor negatives → phrase/exact service ad groups → LP CRO → demote tap/ghl actions → ad schedule.

## 2026-09-30 — EXECUTED after the deep dive (Edu approved in chat)

Via `scripts/zenair_change_0930.py`, verified by read-back; rollback snapshot `clients/zen-air/snapshot-2026-09-30-pre-negatives-bidcap.json`.
- NB 24100030790: **Max Conv → Max Clicks, $18 CPC cap**; 202 negatives on ad group 205687909824 (competitors phrase, supply/tech-support phrase, manufacturers EXACT only, zen air brand phrase). Budget unchanged $150.
- BR 23675783172: **all 8 BROAD brand kws paused** (10 exact + 10 phrase live); 206 new campaign negatives (+ jobs/careers). **Ceiling kept at $8**: exact brand kws 81-100% IS at $4.23-5.26 avg CPC, still 12-16% rank-lost; $8 only hurt because of the broad. 90d data: exact/phrase brand kws matched 100% brand queries.
- Correction to deep dive: NB has 30 kws (20 broad), not 4; only 5 served.
- **Competitor-name calls look REAL, not misdials** (65-367s; 7 of ~10 real NB calls). Negating them cuts most NB call volume. Edu wants a dedicated competitor campaign later if meaningful — my view: likely yes, after Eddie verifies the 7 call times listed in the deep-dive doc.
- Recheck NB search terms ~2026-10-03/04 (Max Clicks + broad can chase junk).

## 2026-10-05 — weekly 7-day pass (AT task closed)
NB since Max Clicks $18 cap (09-30): CPC $29.50→$17.44 but 0 conv 10-01..10-04 (~$590). Competitor leak mostly gone. Added 11 NB campaign negatives (metus, jc lane, omega heating, res air, johnson controls, stand for PHRASE; top notch buford, what is hvac, 3 model numbers EXACT). Duct cleaning is a REAL service (site: Ventilation & Duct Cleaning), never negate it. Legacy ENDED campaigns 20525621445/21453417561 are trial campaigns, API can't pause them. Next: 1 more week of Max Clicks, then phrase/exact service ad groups.

## 2026-10-08 — results check (read-only, nothing changed)
PPC 10-01..10-07: $1,075, 85 clk, CPC $12.64, 1 reported conv (a branded Click-to-call TAP 10-05, no matching call_view call) = **0 real leads**. NB $1,050/81 clk/0 conv. **No call_view calls at all since 09-28** (before: 4 calls 60s+ in 09-17..09-28 at ~$485/call). GA4 google/cpc 65 sessions, 0 generate_lead, avg duration 59s→36s. Max Clicks did cut CPC but bought junk: 98% of NB spend on 2 BROAD kws (`hvac contractors near me` QS3 $872, `hvac contractors ga` $178); terms = error codes, DIY, "what is hvac", price research, new competitors (e smith, metro, peachtree service experts, schmidt, t&b). Recommended: don't wait to ~10-12, do the phrase/exact service rebuild now.
**Meta is NOT awareness-only anymore**: `09/17/26 - CBO | Leads` (120247267872090711) live since 09-17, ~$1,030/wk, instant-form leads 39→58→42/wk, CPL $26→$19→$24, freq 3.0/wk. Awareness TOFU still on ($452/wk, CPM $3.40). LSA 10-01..10-07: 4 phone leads, 0 charged. Scripts: `zenair_weekly_1008.py`, `zenair_weekly_1008_b.py`.
**Same day, Edu asked → NB 24100030790 PAUSED** (verified). Only branded live ($50/d); PPC daily $200→$50. Budget/Max Clicks $18 left intact on the paused campaign. Owed: service phrase/exact rebuild + AM ticket (total spend changed). Logged in `clients/zen-air/google-ads-log.md`.

## 2026-10-12 — Meta lead geo is WRONG (client ticket: "FB leads getting worse by location")
Read-only check, nothing changed yet. Lead CBO `09/17/26 - CBO | Leads` (120247267872090711, built by **Jonathan Bannister** 09-17; live ad set 120247339585910711) targets **Duluth, Marietta, Monroe city-only, no radius**, location type home+recent, Optimize locations OFF. Awareness ad set `Open Audience` (120227295614750711) has the same 3 cities (unchanged since before 08-18). Site service area (callzenair.com/service-area, office now 3400 Corporate Way Duluth 30096) = 14 cities: Suwanee, Cumming, Lawrenceville, Duluth, Lilburn, Flowery Branch, Hoschton, Sugar Hill, Alpharetta, Johns Creek, Dacula, Buford, Norcross, Peachtree Corners. **Marietta (23 mi) and Monroe (29 mi) are NOT served**; 13 of 14 real cities untargeted. Earlier lead campaigns (Apr–Jul $49 offer / ANIV SALE) used Duluth +15 mi. No Meta lead campaign ran 08-03..09-16. Delivery 100% Georgia. Since 09-17: $3,739 / 168 leads. Proposed fix: service-city ZIPs on both ad sets (or Duluth +15 mi); open question whether Eddie asked JB for Marietta/Monroe.

**10-12 EXECUTED (Edu: "just remove the wrong cities"):** Marietta + Monroe removed AND excluded (excluded_geo_locations, 09:46) on BOTH ad sets (lead 120247339585910711, awareness 120227295614750711), now **Duluth city-only**, everything else unchanged, published + read back. Edu did NOT want the full ZIP/county rebuild offered (rejected the question) — do the narrow ask. Still open: Duluth-only is tiny; AT Target Cities list = 14 cities + Gwinnett/Forsyth/Hall/Fulton counties, not added. Log: `clients/zen-air/meta-ads-log.md`. Mechanics: Meta rejects legacy `page_types` on write, resend placements as publisher_platforms + *_positions; IG `explore` deprecated.
**10-12 ~09:49 AT list ADDED:** both ad sets now = 131 ZIPs (Gwinnett + WHOLE Fulton + Hall + Forsyth counties + Hoschton 30548), Marietta/Monroe still excluded, Duluth city key dropped (Meta error 1487756: city conflicts with its own ZIPs). Edu chose whole Fulton (incl. Atlanta/South Fulton) by sending the list as-is. List file `clients/zen-air/meta_zips_service_area_2026-10-12.txt`.
**AT note:** Zen Air's AT field "Notes - Paid Advertising" (`notes_paid_advertising`) says "Please do not target Marietta/Monroe ever for campaigns". Edu suspects it was added AFTER the 09-17 build. Date NOT provable via MCP (field history rejects custom fields, audit feed errors, no ticket/task/comment hit). Only data point: client record `updated_at` 2026-09-22 02:03 UTC (= 09-21 10:03 PM ET, any field). Marietta/Monroe were already an "outlier cities" topic in Andrea's Jun 1–15 summary (see 2026-07-09 docs). Awareness ad set had Duluth/Marietta/Monroe since before 08-18, so the 09-17 lead build likely copied it (inference).

## 2026-10-14 — services inventory for the LP request
- **AT service catalog is near-empty**: only "Commercial AC Services" marked offered. Real list lives on callzenair.com: HVAC repair/install/replacement/maintenance, AC, Heating & Furnace, Heat Pumps (each with repair/install/replace/maintenance subpages), Ductless/Mini-Splits, IAQ (purifiers, UV, humidifiers, duct cleaning), Residential, Commercial, Lennox products, Club Zen membership, Instant System Quote, filter shop, ZenFlo thermostat.
- AT `current_specials` is stale (July 10-yr anniversary $1,500 off Lennox, "$1,500 off if we can't install today", $49 tune-up). Site /about-us/specials/ shows only "$49 Furnace Tune-up and Safety Check" (banner file named "Spring Version"). Club Zen: annual inspections, priority, discounts, $119/yr loyalty credit toward a new system, free for military/vets/65+/first responders/teachers; no price published.
- AT conflict: `affiliations` = Lennox, `manufactures` = Carrier; site sells Lennox.
- LP briefs must follow AT `pin_paid_advertising` + `brand_voice_style` (Wizard of Ads, Zen Ben/Cricket, approved "bits and chunks", no generic HVAC clichés) and `web_design_guidelines`. Avg job value: service $225, install $12,500.
- Mid-Oct recommendation given to Edu: heating first (furnace repair, heat pump repair, $49 furnace tune-up, furnace/heat pump replacement); AC pages wait for spring.
- **Edu's decision, same day:** start with 2 BROAD pages (repair + replacement + tune-ups), one heating, one cooling. H1s: "Heating Repair, Replacement & Tune-Ups in Duluth, GA" and "AC Repair, Replacement & Tune-Ups in Duluth, GA". Subheads use approved brand lines (Stress Free HVAC / Your Neighborhood HVAC), no rating claimed until the GBP numbers are pulled. Full plan + open items (confirm $49 offer, phone number, GBP rating) in `clients/zen-air/landing-pages/2026-10-14-lp-plan.md`. Not requested from WebDev yet.

## 2026-10-14 — LSA wins pull for the CS call (read-only)
LSA 3740502923 live since 09-10 (budget field $642.86). 09-10..10-14: **13 phone leads, 5 BOOKED** (09-11, 09-19, 10-02, 10-05, 10-07), 4 DECLINED (09-10 x2, 09-14, 09-18; three were calls of 4-25s), 4 still ACTIVE/unmarked (09-24 x2, 10-07, 10-09). Spend **$169.01**, Google billed only 2 of 13 (the 09-10 declined 25s call $106.61, the 10-07 booked $62.40) = **~$34 per booked job**. Booked calls ran 2-21 min, and 3 of the 5 booked callers called back (09-11 lead: 15 + 21 min). Best week 10-05..10-11: 4 calls, 2 booked. Impressions flat ~70-100/wk, so the gain is booking rate, not reach. Before the July pause (05-01..07-03): 29 leads, 8 booked (28%), $1,078 = ~$135/booked job; 07-02 alone had 8 leads, mostly declined + charged. The 09-30 note "most LSA leads DECLINED" is superseded. Which lead became the "won" job isn't visible in LSA (only BOOKED); ask Eddie/GHL. Never mention the July pause to the client.
**Same day, ~1h later:** 344561908 (10-07 10:47) flipped ACTIVE→BOOKED, so **6 booked, 3 unmarked, ~$28/booked job**. Client notes on the booked leads: 10-02 = existing customer (maintenance, not a new-customer win); 09-19 = AC not cooling, $79 diagnostic; 10-05 = repair, part ordered (callback 10-13); 10-07 16:42 = AC repair but note says "let me get back to you". LSA times are America/New_York. Per-call recording links come from `local_services_lead_conversation.phone_call_details.call_recording_url`; caller phone from `local_services_lead.contact_details` (select the whole message); client notes from `local_services_lead.note.description`. Don't store caller phones/addresses in the repo.
**10-14 LSA reach diagnosis (read-only, nothing changed):** budget is NOT the limiter ($642.86/day budget field, spends ~$5/day). Bidding = MAXIMIZE_CONVERSIONS ("Maximize leads") but category_bids has **target_cpa_bid_micros = $12** for HVAC (manual_cpa $350 dormant). Real charged leads cost $62-107, 2025 avg ~$80, so a $12 target would choke auctions. **UI check (Edu's screenshot):** 'Set a target cost per lead (optional)' box is UNticked; ticking it auto-fills Google's suggested $80 and lists '$12 (current)'. Hidden-but-active target looked UNLIKELY from the data: campaign-level maximize_conversions.target_cpa empty, bidding_strategy_system_status ENABLED, fall lead volume on par with last fall (Sep/Oct 2025 = 10/8 leads vs ~11/mo now), and off-season blended $/lead was always $12-25 (Oct 2024 $11.96, May 2026 $12.48), so $13 now proves nothing. Only Google LSA support can confirm 100% / clear the stored $12. **Settled for practical purposes (same day):** UI forecast = 3 leads/wk at BOTH $24 and $80 (no forecast shown for $12). Volume is flat to the bid, so the target question doesn't matter: demand in the current area/hours caps at ~3/wk. Levers = service area, hours, ranking, season. **Edu correction:** individual leads above the target prove NOTHING (Google's tCPL is an AVERAGE, single leads can cost more; support.google.com/localservices/answer/15406075). Don't use it as evidence. LSA optional targets only exist since Sep 2024, so the $12 was set Sep 2024 or later. If no target, plain Maximize leads with a huge budget = no bid cap. Google's own forecast at an $80 target = ~3 leads/week, the same as current volume. Google recommends no target under 15 leads/month (Zen ~11). The API's `target_cpa_bid_micros` can't tell you if the box is ticked, so never call it active from the API alone. Reach is down YoY, not just seasonal: Jun 2026 414 impr vs Jun 2025 1,306; Oct 2026 pace ~330 vs Oct 2025 639; Jan-Apr 2026 were ABOVE 2025, so the drop started ~May 2026. Service area = 15 cities, city limits only (Alpharetta, Auburn, Buford, Cumming, Dacula, Duluth, Grayson, Johns Creek, Lawrenceville, Lilburn, Loganville, Norcross, Snellville, Sugar Hill, Suwanee); missing Flowery Branch, Hoschton, Peachtree Corners + all unincorporated/county area. Schedule Mon-Fri 8-20, Sat 8-17, Sunday OFF (0 of 216 leads since 2025 on Sunday). 13 MESSAGE leads since 2025, none this run. License + insurance PASSED (GA). Raising the target lifts real spend, so run it via AM/Eddie before changing.
**10-14 LSA access audit:** Google Ads UI Change history on 3740502923 shows ONLY account/user-access events (latest Dec 3 2025); no campaign changes at all, not even Eddie's 07-03-2026 pause that the API logged. So LSA bid/target/area changes are NOT recoverable from UI history, and when the $12 target was set is unknowable. Active manager links: TSD MCC 4155514468 AND **SearchLight Digital 6263403407** (LSA management platform; linked 2024-11-21 by elena@searchlightdigital.io via bulk upload, one day after TSD's link). Admin users: eddie@, access@topservdigital, khrystyna@topservdigital, plus **localservicesteam@gmail.com (ADMIN since 2024-01-29, owner unknown, pre-TSD)**; emily@callzenair STANDARD, rachel.shaffer22@gmail READ_ONLY. Open: is SearchLight a TSD vendor or a leftover? Who owns localservicesteam@gmail? API change_event shows no changes since 09-15 by anyone. Nothing removed.

## 2026-10-14 — Meta lead geo audit (ad 09/22 Ad 02, 173 leads)
Only **28/173 (16%) in the core service area** by self-reported city; +36 Atlanta/Fulton/Hall maybes; 47 Marietta/Monroe (all pre-fix); 56 clearly elsewhere in GA or out of state. $3,435 spend = ~$123 per core lead. After the 10-12 ZIP fix: 0 Marietta/Monroe but 13/27 still outside (travelers/south metro), likely whole Fulton incl. airport ZIP 30320 + home+recent. Form collects city only (profile prefill), no ZIP. Detail: `clients/zen-air/meta-ads-log.md` 10-14.
**Full 10-14 LSA write-up:** `clients/zen-air/2026-10-14-lsa-review.md` (pull recipes, lead tables, monthly history Oct 2024-Oct 2026, reach diagnosis, the $12 tCPL evidence both ways, access audit, open items). Log entry in `google-ads-log.md` 2026-10-14. Command Center follow-up **fu-051**.

## 2026-10-16 — weekly pass (Gui, AT tasks 539f28ea / fd47eaff / fc797a2f, left open for review)
PPC Branded-only $71.27, 1 tap conv, 89% IS, Health Poor. LSA $62.40 / 1 counted lead (3 in lead report, 1 booked), 100% top. Meta $1,535 / 98 leads / $15.67 CPL, rated Mixed (geo). **Found: awareness ad set `Open Audience` 120227295614750711 optimizes for REACH with a frequency CAP 4/7d, freq 1.85/wk** = off the no-cap ARL doctrine ([[tsd-meta-ads-methodology]]). Rebuild as new ARL campaign staged, not applied.

**2026-10-23 weekly pass (Gui, AT 54ce2840 / 7f983d3f / ff291b11, completed):** PPC Branded-only $54.49 / 3 conv incl. **2 real ad calls (60s+), first since 09-28**; LSA $0, 5 uncharged phone leads (1 booked, 4 declined); Meta $1,500.82 / 137 / $10.95, lead ad set CPL $11.68 → $14.03 after Edu's 10-20 home-only change (CPM up, expected), recheck ~10-27; awareness ARL rebuild still staged.

## 2026-10-20 — Meta location type fix (Angela: "FB targeting NOT working, crazy leads from various places")
Region breakdown 10-13..10-20 = 100% Georgia, Audience Network $0, so out-of-state leads were travelers/commuters INSIDE our ZIPs (location type home+recent; list had airport ZIP 30320 + downtown hotel ZIPs). Negative states/cities would do nothing. **APPLIED on both ad sets: location_types → home only ("people living in"), 30320 removed + excluded** (Meta normalizes exclusion location_types to home). Published 15:33 ET, read back live. Recheck ~10-27 vs 10-19 baseline (24% workable / 52% outside). Next lever if still junky: ZIP question on the instant form. Log: `clients/zen-air/meta-ads-log.md` 10-20.

## 2026-10-23 — NB relaunched on the 2 new LPs (Edu's go)
Pages live: `/heating-repair-replacement-duluth-ga/` + `/ac-repair-replacement-duluth-ga/` (GHL form, GTM listener verified in live container, 678-853-7440). NB 24100030790 **ENABLED at $100/day**, Max Clicks $18 kept: new ad groups Heating (201482056277, 20 phrase/exact kws) + AC (201482056557, 13 kws), 1 RSA each to its page; old broad ad group 205687909824 PAUSED; its 202 negatives copied to campaign level + 28 DIY/jobs/vehicle/water-heater (241 total). Commercial/IAQ/thermostat terms dropped (no page). PPC total $150/d (Branded $50). Script `clients/zen-air/zen_lp_rebuild_1023.py`, log 10-23. Recheck terms ~10-27, conv ~10-30; GHL Verified Live (Mo) before telling client; AM ticket still owed.

## 2026-10-23 — lead outcomes pull (read-only)
LSA since 10-18: 4 calls, 1 BOOKED (10-21, 28-min call, 2 addresses booked for Nov, "both paid for"), 1 DECLINED (fleet-services sales pitch), 2 unmarked. 10-15 PM lead flipped to BOOKED (returning customer). Since 09-10: 20 calls, 8 booked (2 existing/returning), 5 declined, 7 unmarked. Same day, transcribed 10-19 + 10-22 calls (both new furnace/heating breakdowns): BOTH booked on the call (next-day visits), not marked in LSA, so real tally = 10 booked, 5 unmarked. LSA recording download needs Bearer token from client.credentials; faster-whisper venv is NOT persistent, reinstall in scratchpad. $0 charged 10-14..10-23. PPC: 2 Branded calls 10-16 (68s/118s), first since 09-28, outcome unknown (no CallRail). Script `zenair_leads_1023.py` (run_query keys are snake_case). Log 10-23.

## Approved monthly budget (AT, checked 2026-10-23)
AT Client Request **"BUDGET UPDATE"** `3f291790-9d64-4d4b-9cc6-88f5ab2eeb38` (Mia Kelly, 2026-07-31, client approved): total **$10k → $8k/mo = $6k Google (Search only, PMax paused) + $2k Meta (awareness only, lead-gen PAUSED)**. Re-confirmed in "Confirm August Ad Budget & Campaign Setup" `16310a80-…` (08-13, Eddie): Google $200/d, Meta $65/d. No AT task found approving the Meta `09/17/26 - CBO | Leads` campaign ($150/d, live since 09-17); as of 10-23 Meta = $215/d ≈ $6.5k/mo vs $2k approved, and the full budget ≈ $11.1k/mo vs $8k. Ask the AM whether that was approved somewhere outside AT.
