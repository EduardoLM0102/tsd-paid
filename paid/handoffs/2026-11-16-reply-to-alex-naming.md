Hey Alex,

Answers below. I pulled every Google Ads account under the MCC (56 accounts, 192 campaigns that spent in 2026) and read the Meta accounts we manage through the connector, so most of this comes from the accounts, not from memory. Where it's my call instead of a fact, I say so.

Files in the same folder (`alex-naming-audit-2026-11-16/`):
- `google-campaign-intent-2026.csv`: every Google campaign that spent in 2026, with the intent bucket I'd put it in (LEAD / BRANDSEARCH / AWARE / HIRE / LSA / INTERNAL), 2026 spend, first spend date and notes. This is the corrections list you asked for, so you can fix the old and paused ones on your side without renames.
- `call_assets.csv`, `customer.csv`, `pmax_brand.csv`, `brand_lists.csv`, `mix_keywords.csv`, `video_conv.csv`: the raw pulls behind the answers.
- `alex_naming_audit_readonly.py`: the read-only script, in case you want to rerun it.

## Three things to fix in the premise first

1. **The date in a `TSD_` name is the build date, not the first spend date.** We build paused and launch later, sometimes weeks later. All Seasons' three `TSD_07.01` campaigns first spent on Jul 20 and 21. Watt's `TSD_08.03_Search_EVCharger` first spent Sep 3. Concrete's `TSD_10.22_Search_Branded_Oxford` first spent Nov 13. Don't derive a launch date from the name.
2. **`Pay-per-lead-PMax-*` and `[LSA] Watt's Right Electric` are LSA, not PMax.** Google migrated several LSA accounts into pay-per-lead PMax campaigns on Nov 3 and 4 (Watt's Right, Amazing Morrow, Golden, Gray Duct, King's Window, Nick's, Spencer). The API reports them as `PERFORMANCE_MAX`. Detect them by the name prefix or by `asset_group.name LIKE 'xcat:%'`. They're lead gen priced per lead, and lead-level data still comes from `local_services_lead`.
3. **There are no hiring campaigns on Google.** Zero spent in 2026. Everything hiring is on Meta.

## Your 12 questions

**1. Branded search: brand or lead?**
Count it as lead gen, with a note on it saying it's branded search. Keep it visible as its own line inside lead gen, so blended cost per lead includes it and non-brand cost per lead shows next to it. That's how I already report Google every week (branded vs unbranded, each with its own CPL). Hiding brand search inside Awareness makes CPL look better than it is, and we can't defend that to a client. 2026 brand search spend is $67.6k across 29 campaigns, so it's not small.

**2. PMax and brand searches.**
Of 36 PMax campaigns that spent in 2026, 5 have a brand exclusion list: Neon Monkey `TSD_04.25_PMAX_Evergreen` (live), Nick's `TSD_02.20_PMAX_Q1` (live), Proud Pops `TSD_05.14_Leads_Pmax_HVAC` and `TSD_05.20_PMax_Electrical` (paused since Oct 14), C&S `TSD_10.09_PMax_Leads_Mansfield` (paused). Everything older has none. Live PMax without exclusion today: Hawkins `TSD_Pmax_Siding`, Golden `TSD_02.19_Pmax` (client on freeze), My Favorite Service `Pmax_AC Repair & Replacement` (not eligible, not serving). So yes, part of the historical PMax spend bought the client's own name, and it can't be split after the fact: Google doesn't expose PMax search terms by brand in the API. Count PMax as LEAD and footnote it. Every PMax we've built since October gets a brand exclusion list; it's in our Google launch SOP (PMax section).

**3. Demand Gen / YouTube.**
Both go in AWARE. Cool Hand's `TSD_YouTube` 153 "conversions" are 143 "Click to call" (phone number taps on the site), 3 YouTube channel subscriptions and 7 follow-on views. Zero verified leads. Never count Video or Demand Gen conversions as leads. ICS "Mitsubishi YouTube" ($5,995 in 2026) is a Video campaign inside the Belleville LSA account that nobody on paid owns right now. On The Way's "Demand Gen - 2026-05-26" was built before we took the account and the client revoked our access in October, so it's out of scope.

**4. Boosted posts.**
No. We never run boosted posts, it's always the client. Keep them out of cost per lead and out of awareness too, and show them as client-run spend if you show them at all. The only exception would be a campaign that starts with our naming tag (`TSD_`), which marks it as ours. Meta names boosted posts `Post: "…"` on its own, so those are easy to catch. Also, Watt's Right's Meta account isn't managed by TSD at all (it sits in the client's own business, "kandkelectric").

**5. Hiring campaigns.**
Yes, separate HIRE bucket, out of CPL. Only Meta has them (Zen Air "Now Hiring (Employment)", the `_Hiring` ones you listed).

**6. What `_Mix` means.**
Brand term plus a service word, in mixed match types. All 28 enabled keywords in Mission Accomplished's `_Mix` and all 22 in Neon Monkey's contain the client's name ("mission accomplished ac repair", "neon monkey tree service"), in exact, phrase and broad together. No non-brand keywords. BRANDSEARCH.

**7. `TSD_07.01_Lead_Search_Mitsubishi-Brand`.**
LEAD. It's a manufacturer's name, not the client's. Same for All Seasons' `TSD_04.07_Search_MitsubishiHeatPump` and `TSD_04.08_PMAX_Daikin_Calls`. One trap: All Seasons has a Google brand list called "Mitsubishi" attached to those Search campaigns as a brand *inclusion* (Google's brand setting for broad match). So a BRAND_LIST criterion on a Search campaign doesn't mean "branded". Only a negative brand list on PMax means "brand excluded".

**8. ICS `TOF_P.LEADS` on Awareness, and MA `BOF_Awareness`.**
Go by objective and ad-set optimization goal, never by the name. ICS: that account isn't enabled on our Meta connector, so I can't read it. It's a June 2025 build, before my time. If it runs on the Awareness objective, it's AWARE. Mission Accomplished `TSD_04.27_BOF_Awareness_CBO_Evergreen` (old account 79203382): confirmed Awareness objective, ad set optimized for Ad Recall Lift, paused, $1,249 in 2026. AWARE. The "BOF" in the name is wrong. Built before I joined.

**9. Date format.**
Month.day, and it's the build date (see premise 1). Of the `TSD_dd.dd` campaigns that spent in 2026, 58 read as month.day and 11 as day.month. The 11 day.month names were all built in the same week of early May 2026, before I started in June (Neon Monkey `08.05` x3, Watt's `07.05` x2, Spencer `07.05` x2, Napps `06.05` x2, C&S `07.05`, King's `28.04`). Everything built since June is month.day. I'm leaving those 11 as they are, so please take their real dates from the CSV. Four of them are still live: Watt's `TSD_07.05_Leads_Search_Nonbranded`, Spencer `TSD_07.05_Leads_Search_Branded`, King's `TSD_28.04_Search_Nonbranded_Evergreen` and Napps `TSD_06.05_Leads_Search_Nonbranded_Plumbing`.

**10. Who names campaigns, and is there a written convention.**
Since June: me, and Gui since October (Google). On Meta: me, Jonathan built Zen Air's lead CBO (9/17), and Clay Manus renamed Watt's ad sets on 10/06. Before June: the previous paid seat, plus whatever agency the account came from (Levergy on Mission Accomplished, RYNO on Lily Pad, BCJ on Concrete Adventures, On Purpose Media on Strickland). Those inherited names are tagged in the CSV. Written convention: no. Our own Meta launch SOP says "the division-wide naming convention is still being finalized". Your proposal can be it, with the tweaks at the bottom.

**11. Call tracking on Google.**
- **Auto-tagging:** on in all 56 accounts.
- **Tracking template:** 13 accounts have one at account level, 11 of those include `{keyword}`. Four are ClickCease redirect templates (All Seasons, Zen Air, Integrate, All Heart), which pass through to the page. Mission Accomplished uses ServiceTitan parameters (`sts/stm/stc/stad`), no keyword. No template at all: Proud Pops, Hawkins, Golden, King's, Nick's, Spencer, Napps, Cool Hand, Lily Pad, Amazing Morrow. Hawkins' two paused `03.16` campaigns hardcode `utm_campaign=Search+Brand` on both Branded and NonBranded, a legacy bug, both paused. Google has no ValueTrack for the campaign name, only `{campaignid}`, so a UTM can carry the ID and you map it to the name (you already track by ID).
- **Call assets:** per client below. "CallRail" means the number is a tracker in our agency CallRail account.

| Client | Call asset number | What it is |
|---|---|---|
| Proud Pops | (210) 225-5767 | CallRail tracker "CALL POP" in the client's own CallRail account (533681324) |
| Watt's Right | 918-818-3928 | CallRail "Call Extension PPC" (client's own CallRail, 537241053) |
| Hawkins | 972-829-0989 | CallRail "Google Ads Call Extension" |
| Neon Monkey | (817) 409-8954 | CallRail "Google Ads Call Extension". (800) 315-2374 on one campaign is the client's 800 line with the IVR menu |
| All Seasons | (631) 212-8021 | CallRail "All Season Call Extension". (631) 694-1616 on one campaign is not a tracker |
| King's Window | 817-512-7341 | CallRail "Google Ads Extension". 817-510-8654 is a CallRail *website pool* number used as a call asset on "Branded - Search - King's Window Services #2" (enabled, no 2026 spend). Pool numbers rotate between visitors, so that's wrong. I'll remove it |
| Spencer Air | (972) 449-4282 | CallRail "Google Ads". Account-level (972) 433-5498 = CallRail "Homepage Calls" |
| Napps | 903-289-7073 | CallRail "Google Ads". Account-level (903) 758-6482 = main line, untracked |
| C&S Air | 817-442-6949 | CallRail "Google Ads". (817) 477-2665 = main line |
| Integrate Comfort | 866-658-2987 | CallRail "Call Extension (Google Ads)" |
| Cool Hand | 469-270-1146 | ServiceTitan tracking number, not CallRail |
| Mission Accomplished | 928-517-7778 and others | ServiceTitan / client numbers, not CallRail |
| Nick's | (985) 999-4785 | not in our CallRail, checking what it is |
| Zen Air | 678-329-9929, 678-606-8817 | not in our CallRail, checking what they are |
| Concrete Adventures | (662) 498-5409 | client's own CallRail, not under our agency account. The other 3 numbers belong to paused BCJ-era campaigns |
| Lily Pad | 785 numbers | client's real lines (RYNO-era), untracked |
| My Favorite Service | (210) 361-5569, (830) 212-4076 | not CallRail agency trackers |
| Amazing Morrow | none | no call asset yet |

- **Why only half the calls reach you with a campaign name.** Call-asset calls go through a Google forwarding number. CallRail receives them on the "Call Extension" tracker with no gclid, so no campaign. Google logs those calls itself: 1,809 call-asset calls from Aug 1 to Nov 15 across 19 accounts in `call_view`, each with campaign, start time and duration. Join `call_view` to the CallRail call by start time (within a minute) and you get the campaign for the other half. That's exactly how we reconcile Watt's Right today. Website calls (the CallRail pool, DNI) get a campaign through the gclid, which needs the CallRail to Google Ads integration switched on per company. As of early November it's working on Spencer and Watt's, broken or pending on Napps (needs a pool), Cool Hand (pool dark since Oct 15), Proud Pops (integration points at the old Ads account), Integrate (0 uploads), Hawkins and Lily Pad (uploads stalled). Location asset sets (the GBP numbers CallRail can't attribute) exist only on paused legacy campaigns (C&S Air's old Smart campaign, Integrate's old RTM campaigns in the Belleville account, one paused Proud Pops Smart campaign) and on the LSA campaigns Google migrated, where Google sets them. No live TSD Search campaign carries one, so that limitation isn't what's hurting us.

**12. Meta leads.**
Every TSD lead campaign uses Instant Forms (destination ON_AD): Zen Air, Mission Accomplished, Napps. The forms go to GHL: Zen Air through a Zapier zap, Mission Accomplished straight into GHL with Hatch sending the notification. The only website-conversion lead campaign is Zen Air's hiring ad (pixel event Lead, callzenair.com/about-us/join-our-team/). UTMs: none. Zero `url_tags` on any TSD-managed creative in Zen Air, Spencer, Mission Accomplished (old and new), Napps and Concrete Adventures. The only UTMs found are on Watt's Right's own FourMode website campaign, which isn't ours. So today the Meta campaign name reaches you through the API only, not through CallRail or GHL. Two notes: for Instant Forms the campaign, ad set and ad IDs ride on the lead object itself (the leadgen webhook carries `campaign_id`, `adset_id`, `ad_id`), so UTMs wouldn't add anything there. UTMs only help the ads that click to a site. From now on every new Meta ad gets these url_tags: `utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_id={{campaign.id}}&utm_content={{ad.id}}`.

## On your proposal

I'm in. The fixed intent field is the right fix, and it's what we were missing anyway. Four tweaks:
1. Add `LSA` as a fifth intent value, or just detect it by channel on your side. Google names those and we can't rename them.
2. Read Meta by objective and optimization goal, not by name, like you do today. Rename only so a human can read the account.
3. Intent for Search = what the keywords are, not what the name says. For the two accounts where branded campaigns carried non-brand keywords (Zen Air until October, Nick's until Nov 11), the CSV notes it.
4. Date stays the build date, written `YYYY-MM-DD`.

Rename plan: once your naming plan is final, I'll rename the live campaigns in one pass so the change history shows one person on one day. Until then I'm not renaming anything. For everything paused or old, use the CSV.

Eduardo
