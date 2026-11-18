---
name: tsd-lsa-ppl-pmax-migration
description: "Google is auto-migrating LSA into 'Pay-per-lead-PMax' campaigns (Nov 2026); 7 TSD accounts switched 11-03/11-04; how to detect"
metadata:
  type: project
---

**2026-11-06 sweep of all 57 enabled MCC accounts.** Google (not us) creates a PERFORMANCE_MAX campaign named
`Pay-per-lead-PMax-<business>` (Max Conv, same daily budget as the old LSA, one asset group `xcat:service_area_business_<category>`)
and pauses the old `LocalServicesCampaign:SystemGenerated`. LSA history stays on the old campaign.

Migrated (new campaign id / created):
- Watt's Right 3651667805: 24425981973, 11-04 (renamed `[LSA] Watt's Right Electric` 11-04 by access@topservdigital.com) — see [[tsd-watts-right]]
- Amazing Morrow 9677746935: 24421977066, 11-03, no spend on old or new; budget field shows $4.69M/d (inherited from old LSA)
- Golden Plumbing 4193142570: 24426143517, 11-04, spending since 11-05 — [[tsd-golden-plumbing]]
- Gray Duct 6191956550: 24431188313, 11-04, no spend old or new
- King's Window 6769493219: 24431038949, 11-04, spending since 11-05 — [[tsd-kings-window]]
- Nick's Heating 1854100356: 24425921001, 11-04, serving normally, $0 = no charged lead yet — [[tsd-nicks-heating]]
- Spencer Air 2524618054: 24436741588, 11-04, serving normally, $0 = no charged lead yet — [[tsd-spencer-air]]

Still classic LSA on 11-06 (enabled): C&S Air, AC Cornerstone, All Heart, Chisholm, Concrete Adventures, Cool Hand, DFW Unsuspended,
Eaglepoint, Hawkins, Integrate Comfort x3 LSA accts, Mission Accomplished LSA, Modern Comfort, MFSC x2, Napps LSA, Neon Monkey LSA,
Proud Pops x3, Steadfast, Supreme AC, Ultimate Comfort, Zen Air LSA, + unnamed 8655979348. Expect more to flip.

**How to detect:** GAQL per account `SELECT campaign.id, asset_group.name FROM asset_group WHERE campaign.advertising_channel_type =
'PERFORMANCE_MAX' AND asset_group.name LIKE 'xcat:%'` (don't match on name, it can be renamed). Scratch sweep used customer_client
under MCC 4155514468. `campaign.start_date` is gone in this API version, use `campaign.start_date_time`.

**Correction 11-06 (same day):** `local_services_lead` STILL returns leads after the switch (Watt's Right: leads 11-05 and 11-06,
charged/booked flags intact), so lsa_report.py lead-level data keeps working. What breaks is anything keyed on channel LOCAL_SERVICES
for SPEND/metrics (google_channels.py, campaign-type filters): spend now sits on the PMax campaign. New campaign's Google Ads
conversion action = `Phone calls (Pay-per-lead goals)`. API shows target_content_network=True but delivery so far only SEARCH + MAPS.

**What actually changes (SEJ 2026-07-20 + agency blogs, Google Help 17213585):** still pay per valid lead, still Search + Maps only,
badge carries over. Manual bidding gone (Amazing Morrow was MANUAL_CPA), one campaign-level tCPA across all service categories
(multi-trade clients can't price categories separately unless split into separate campaigns), weekly budget -> daily average,
old LSA dashboard reports don't migrate (lead history does), lead inbox moves into Google Ads, BBB callouts dropped.
Unverified (Invoca only): missed calls >~20s in business hours billable since 2026-10-01; Reserve with Google bookings count as paid leads.

**How to apply:** PMax rechecks/branded splits must separate the pay-per-lead PMax from TSD's own PMax ([[tsd-pmax-branded-split-rule]]).
Export old LSA campaign reports for accounts not yet migrated if we need YoY.

**Exposure check 11-06 (enabled LSA, leads by category 08-08..11-06):** MULTI-TRADE LSA = Napps LSA 9239407401 (plumber 80 / HVAC 40 /
bath remodel 24), Proud Pops PPC-account LSA 1051843378 (HVAC 12 / plumber 11), Cool Hand 9865206319 (HVAC 24 / electrician 14, LSA out of
TSD scope). These get the single blended tCPA on migration. Still MANUAL_CPA (will be forced to auto): Mission Accomplished LSA 4904262993,
Modern Comfort 9020391433. Everyone else already Max Conversions.
Per-trade targets actually SET (campaign.local_services_campaign_settings.category_bids.target_cpa_bid_micros, 11-06): Napps NONE (all 0,
pure Max Conv, so no blended-target impact); Proud Pops only HVAC $62 (plumber/bath 0); Cool Hand HVAC $62 + electrician $45 (out of scope).
manual_cpa_bid_micros values are leftovers and ignored under Max Conv.

**$0 spend != dark (checked 11-06):** spend on these campaigns = charged leads only; clicks/impressions cost nothing. The old LSA also had $0 days
with clicks. Nick's/Spencer/King's 11-05 impressions matched their pre-switch daily level, all SERVING, asset groups ELIGIBLE, billing approved,
verifications passed. To judge "dark", look at impressions + local_services_lead by day, never cost alone.

**2026-11-12 (Nick's, Cowork check): verification after migration.**
- Migrated accounts DISAPPEAR from the old LSA manager (ads.google.com/localservices shows "MCC Reports", 20 live accounts, Nick's not listed). So the old Business verification / Proof of Insurance page is no longer reachable for them.
- In Google Ads the only verification page is **Admin → Policy → Account → "Advertiser Verification" tab** (not a top-level Admin entry). Nick's showed only the 4 generic advertiser-verification tasks (org questions, SSN, EU political ads, who pays), nothing about insurance/license/GBP.
- Google's pay-per-lead screening doc (support.google.com/google-ads/answer/18260066) lists GBP + business registration + representative (+ license for some verticals); insurance isn't named. Missing items show as campaign status "Not Eligible: Verification required" with a 30-day grace period.
- Rule: for a migrated account, an expired LSA-era insurance artifact in the API (local_services_verification_artifact) is NOT a blocker while the PPL campaign is Eligible with no warning. Don't chase COIs for migrated accounts unless the campaign status says so. Migration support line +1-844-205-0011.
- Side flags: old LSA manager shows a "New Verification Requirements" banner (affects the non-migrated accounts, not read yet); Nick's "Ads funded by" = "Mallory Olivia" (not Nick's name), probably old, unverified.

**2026-11-16 (Edu, Watt's Right review):** in any client-facing number for a migrated account (KPI rows, reports, Slack), explain that LSA now runs inside Google Ads as a Pay-per-lead campaign, so "Google Ads spend" includes LSA. Give the split (LSA vs Search/PMax we manage), say not to add LSA on top, and say the Pay-per-lead campaign is not our PMax. Also state the counts are paid-ads only (CallRail total calls vs ad calls) so big LSA call volumes don't read as all-calls.
