# Hawkins: Jared's "Feedback on ads" (AT Client Request 3a267fb1, Execution on Edu)

Task: https://app.agencytitan.com/tasks/instance/3a267fb1-a9f3-4996-9a2d-164a27f4c6dd
Status: SENT to Angela 10-28 (AT completion notes + PDF). Follow-ups fu-104..107. Goes in the Execution notes for Angela to relay to Jared.

| # | Jared's point | Status |
|---|---|---|
| 1 | Pause Branded | Done 10-28 (google-ads-log.md) |
| 2 | Where the 29 booked LSA jobs came from | Done 10-28, LSA Booked Leads Review PDF |
| 3 | Approved monthly budget | Drafted below |
| 4 | Spend strategy across Search ad groups | Drafted (v2) |
| 5 | Process to catch bad traffic before he raised it | Drafted (v2, timeline checked) |
| 6 | Month over month trends | Drafted |
| 7 | Attribution: campaigns + CallRail to leads, estimates, closed jobs | Drafted, UTMs applied 10-28 |
| 8 | Budget based on lead quality, not cost per form | Drafted, PMax sentence kept |

---

## 3. Monthly budget

**Client text:**

**Monthly budget**
We don't have a signed monthly budget on file for your account. What we do have are the media plans from the team that managed your account before. June was planned at $2,900 for Google Search and $7,000 for Local Services, and September at $3,630 for Google Ads and $5,929 for Local Services. We can't confirm whether those numbers were approved with you at the time. September came in under that plan, at about $2,805 on Google Ads and $5,636 on Local Services. We'd like to agree on a monthly budget with you for November and December, split by channel, so we're all working from the same number.

**Internal (not for the client):**
- Source: Media Plan Q2 (Google Sheet 1yXcPF--RJge9zlH35o4Y-3iikIuvO4CKV-eELUEVaLc) and Media Plan Q3.xlsx (17c1JJpruMEauwE15yXu8SfGDN--XQXeV). No plan exists for October or Q4.
- The Q3 plan was built from actual pacing (sheet header: "budgets reset to actual channel pacing ... Jul 6"), then +10% a month. Edu can't confirm or deny whether Eve/Mia got client approval for Q2 or Q3.
- September actual: Nonbranded $2,409.78 + PMax $395.70 (Branded ~$0), LSA $5,635.98.

---

## 4. Spend across the Search ad groups

**Data (pulled 10-28, read-only).** Nonbranded campaign 23805382277, one shared daily budget, no per-ad-group budgets.
"Leads" = form fills + calls of 60s or more (call_view), the same rule the September report used.

September:

| Ad group | Spend | Forms | Calls 60s+ | Leads | Cost per lead | Google conv (old 10s call rule) |
|---|---|---|---|---|---|---|
| Siding General | $1,312.22 | 2 | 7 | 9 | $145.80 | 12 |
| Siding Repair | $461.77 | 2 | 0 | 2 | $230.89 | 2 |
| Siding Replacement | $261.14 | 2 | 1 | 3 | $87.05 | 4 |
| Vinyl Siding | $374.64 | 3 | 0 | 3 | $124.88 | 7 |
| **Total** | **$2,409.77** | **9** | **8** | **17** | **$141.75** | **25** |

October 1 to 27 (internal only until the 10-29 review; most October calls were wrong-company or supplier callers per the recordings):

| Ad group | Spend | Forms | Calls 60s+ | Google conv |
|---|---|---|---|---|
| Siding General | $691.20 | 6 | 4 | 12 |
| Siding Repair | $508.86 | 1 | 1 | 4 |
| Siding Replacement | $561.58 | 2 | 2 | 6 |
| Vinyl Siding | $257.03 | 0 | 1 | 1 |
| **Total** | **$2,018.67** | **9** | **8** | **23** |

Two months together: Siding Repair $970.63 for 3 forms + 1 call, Vinyl Siding $631.67 for 3 forms + 1 call (all 4 September Vinyl calls were under 60s).

**Client text (v2, 10-28: Edu cut v1 for oversharing; no table, no re-telling of the September call problem):**

**Spend across the Search ad groups**
The four ad groups share one daily budget, and Google's bidding splits it based on where it expects to find leads, so the spend won't be even across them. Siding General carried most of it in September because the other three were only split out of it on August 31 and were still building history. We review each ad group on the leads it actually brings in, form fills and calls we listen to, not just the cost Google reports. On October 29 we'll compare them side by side, and any ad group that isn't bringing in leads at a reasonable cost gets cut back so that money goes to the ones that are.

**Internal (not for the client):**
- Per-ad-group table above stays internal (Jared already has the Sept numbers; repeating the $231 Repair CPL only highlights it). Vinyl Siding is the likely cut at 10-29 but not named to the client before the review.
- Siding Repair is also weak (2 months, $971, 3 forms + 1 call) but "siding repair" is core service intent, so the fix there is search terms, not pausing.
- Fits the 10-29 staged plan item 4 (narrow NB to service-intent keywords, drop product words like vinyl siding / home siding).
- Script: scratchpad hawkins_adgroups.py (read-only, ad_group + call_view, Jul 1 to Oct 27).

---

## 5. Process to catch bad traffic and poor lead quality

**When did Jared raise it? (checked 10-28: all 36 Hawkins AT tickets + Slack)**
- Jared's FIRST written Search/LSA critique = AT #983 "Re: Monthly call", 2026-10-19 03:45 UTC (Oct 18 evening CT), replying to the Sept report. He raised: LSA leads not actionable (abandoned / no name / no phone, CPL $125-188), Search conversions under-reported, spend on Siding General/Repair at the highest cost per conversion, no UTMs, no month-over-month trends, no branded search, monthly budget.
- He NEVER mentioned junk/irrelevant search terms, competitor or supplier traffic, or wrong-company calls. TSD brought that up first, in our 10-26 answer (call recording finding).
- Earlier tickets: #493 (08-07) and #631 (08-20) = META lead quality (Meta paused 08-20, before Jared's requests). #368 (07-23) = "are our Google ads running?" (volume, during GBP/LSA outage). #628 (08-20 to 09-01) = reporting/inventory request, no quality complaint. #677 = 08-25 re-onboarding recap.
- So everything below predates his first complaint: Aug 31 restructure, Sep 14 review, Oct 5 negatives, Oct 14 negatives, Oct 16 call-recording review + 26 negatives + call rule. Only the Oct 19/21/22 changes came after (they continue the Oct 16 work).

**Client text (v2, uses the timeline; no "you're wrong" framing, the dates make the point):**

**How we manage the account**
Every week we review each channel on spend, cost per lead, search terms and how often the ads show, block searches that don't fit your business, and log the numbers so trends are visible over time. Some of what came out of that work:
- August 31: rebuilt Search into separate ad groups for siding repair, replacement and vinyl siding, each with its own ads and keywords
- September 14: reviewed every keyword and search term the Search campaign had run since April, to see which ones bring leads and which only spend
- October 5: blocked searches that weren't bringing real customers, such as handyman, Angi, grants, "how to" and supply store searches
- October 16: started reviewing every Search call recording each week, and blocked 26 more searches for other companies, product brands and job seekers

**Internal (not for the client):**
- Left out on purpose: Branded (point 1), the PMax/YouTube budget shift (point 8 dislikes cost-per-form logic), the 10-13 brand leak ($57 brand clicks in Nonbranded), July (07-06 negatives came from a car-window complaint).
- Weekly KPI entries in AT exist from 09-09 onward (also 08-10).
- For Angela: his line "reactions to problems I've identified" doesn't match the record on search traffic. Don't argue it in writing; if it comes up on the call, the dates above are the answer.

---

## 6. Month over month trends

**Data (pulled 10-28, read-only, scratchpad hawkins_mom.py).** Same lead rules as the September report: Search = form fills + ad calls 60s+ (call_view); PMax = form fills + calls 60s+; LSA = billed leads. October = Oct 1-27.

| | July | August | September | Oct 1-27 |
|---|---|---|---|---|
| LSA spend | $2,402.86 | $5,420.58 | $5,635.98 | $2,351.99 |
| LSA leads, total / billed | 35 / 26 | 60 / 49 | 69 / 49 | 27 / 23 |
| LSA cost per billed lead | $92 | $111 | $115 | $102 |
| LSA booked (marked) | 1 | 0 | 29 | 10 |
| Search spend (NB + Branded) | $2,408.55 | $2,432.68 | $2,409.78 | $2,085.47 |
| Search forms / calls 60s+ | 7 / 31 | 4 / 6 | 9 / 8 | 9 / 9 |
| Search cost per lead | $63 | $243 | $142 | $116 |
| PMax spend | $517.73 | $395.10 | $395.70 | $554.25 |
| PMax forms / calls 60s+ | 10 / 1 | 6 / 1 | 12 / 0 | 20 / 1 |
| PMax cost per lead | $47 | $56 | $33 | $26 |
| **Total spend** | **$5,329** | **$8,248** | **$8,441** | **$4,992** |
| **Total leads** | **75** | **66** | **78** | **62** |
| **Cost per lead** | **$71** | **$125** | **$108** | **$81** |
| Media plan total | $7,900 | $8,690 | $9,559 | none |

Notes behind the numbers:
- July Search includes the window/door ad groups ($437, 4 forms + 7 calls), turned off mid-July. Siding only: $1,971 / 27 = $73.
- Search Aug: $243 per lead. Calls 60s+ fell 31 to 6 (all-length calls 54 to 28). Not diagnosed; broad keywords + off-target terms (08-24/08-25 findings, 43% off-target), restructured 08-31.
- Oct Search calls: Oct 1-15 recordings = mostly wrong-company/supplier (1 of 16 booked). So Oct Search $116 overstates real performance.
- PMax October = 20 Google lead-form fills, ~89% YouTube; quality never verified (no CRM access).
- LSA booked marks only started in September (office wasn't marking before), so the booked row can't trend before Sept. Real scheduled estimates (LSA review PDF): 30 Sept, 12 Oct 1-27.
- **LSA October drop, cause (10-28):** budget unchanged ($357.14/day, ENABLED, SERVING). Impressions/day ~79 vs ~89 in Sept (-11%), clicks/day 12.1 vs 12.6 (flat). Leads/day 1.0 vs 2.3. So the listing showed and got clicked about as much; far fewer people called or messaged. Not a budget, pause or setting change. Possible: reviews/rating, profile content, seasonality; not verified. change_event query errored, so account change history not checked via API.

**Edu's calls (10-28):** start at August (Aug 25 review baseline; he has the 12-month history from 09-01), LSA first, October Search counts only calls we listened to and confirmed, PMax just reported (no "confirm with the office" ask).

October calls checked (call_view + call-wins-log.md + google-ads-log.md):
- Search 60s+ calls in Oct: 10-01 148s new-home siding (real, open) ✓, 10-02 357s wrong company, 10-06 134s existing-customer complaint, 10-14 104s job seeker, 10-15 256s partial wood repair (real, open, caller ID Oregon, no address) ✓, 10-16 92s materials, 10-17 105s materials, 10-21 71s 'cat exteriors' wrong company, 10-26 147s Branded ✓ (logged as the real ad call). = 3 confirmed. Search Oct = 9 forms + 3 calls = 12, $173.79.
- PMax 60s+ in Oct: 10-18 111s Pierre Ingram down-payment complaint (existing customer) ✗. PMax Oct = 20 forms, $27.71.
- Not counted: 10-12 207s Website-pool call from a Google Ads click (booked, Plano). Website calls weren't in the Sept rule either.

**Client text:**

**Month over month**

| | August | September | October 1 to 27 |
|---|---|---|---|
| **Local Services** spend | $5,421 | $5,636 | $2,352 |
| Billed leads | 49 | 49 | 23 |
| Cost per lead | $111 | $115 | $102 |
| **Google Search** spend | $2,433 | $2,410 | $2,085 |
| Leads | 10 | 17 | 12 |
| Cost per lead | $243 | $142 | $174 |
| **Performance Max** spend | $395 | $396 | $554 |
| Leads | 7 | 12 | 20 |
| Cost per lead | $56 | $33 | $28 |
| **Total** spend | $8,248 | $8,441 | $4,992 |
| Leads | 66 | 78 | 55 |
| Cost per lead | $125 | $108 | $91 |

Search and Performance Max leads are form fills plus calls of a minute or more. From October, we only count the Search calls we listened to and confirmed were customers.

**What changed and why**
- Local Services is still the strongest channel, at $100 to $115 per billed lead every month. In October the listing showed about as often as in September, but fewer homeowners called or messaged, so it brought in and billed for fewer leads.
- Google Search went from $243 per lead in August to $142 in September after we rebuilt it on August 31. October is at $174 for two reasons: the stricter call count above, and fewer clicks while the campaign settles after the October changes that cut searches that weren't bringing customers.
- Performance Max went from $56 per lead in August to $28 in October and now brings in the most leads on the Google Ads side, mostly form fills.

---

## 7. Attribution (campaigns + CallRail to leads, estimates, closed jobs)

**Edu (10-28):** keep it at "what we track today + what we're adding". No Crystal Insights, no JobNimbus ask.

**Checked 10-28 (read-only):**
- Auto-tagging (gclid) ON at account level.
- UTMs: Nonbranded Search 23805382277 (the main live campaign) has NO tracking template / final URL suffix → no UTMs. PMax has `{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign=Pmax+Windows+Siding` (stale "Windows" label). Paused Branded had UTMs but utm_campaign=Search+Brand. So Jared's 10-19 UTM point is fair for Search.
- All 4 NB ad groups land on the same page, /services/siding-installation/.
- CallRail: Hawkins' own account 232929821 (Hawkins owns, TSD manages tracking); call sources already split (Google Ads call extension / Website pool from Google Ads / Google LSA), recordings available.
- Not checked: whether GHL form submissions store UTMs/gclid on the contact.

**Client text (v3, 10-28: Edu cut the monthly lead list + job-records lines; that list was Claude's proposal, never planned):**

**Attribution**
Here's how leads are tracked today:
- Every call from Google Ads, Local Services and the website runs through CallRail, which records where the call came from and keeps the recording.
- Google Ads tracks form fills and calls of a minute or more for each campaign.
- Local Services tracks each lead in its inbox, with the status your office sets.

**Internal (not for the client):**
- ✅ UTMs APPLIED 10-28 (google-ads-log.md): NB suffix utm_campaign=search_nonbranded (+ ad group id + keyword), PMax suffix utm_campaign=pmax_siding (old 'Windows' template cleared). Still unchecked: GHL forms storing UTMs on the contact.
- Cut 10-28: the monthly lead list (not a real commitment) and the 'closed jobs live in your job records' line.

---

## 8. Budget based on lead quality and business outcomes, not cost per form

**Context:** this is aimed at our 10-22/10-26 budget paragraph (moved Search $ into PMax "form leads at about $26 each"). PMax still bids on Google lead-form fills (10-22 change), ~89% YouTube, quality never verified. No CRM access, so "business outcome" we can measure = estimate visits scheduled, from call recordings (LSA + Search calls), not from forms.

**Client text (draft):**

**Budget and lead quality**
Cost per form is one input, not the deciding one. On calls, we listen to the recordings and count only real customers, and we reviewed every Local Services lead from September and October the same way. That's how we know Local Services is the channel that turns into estimate visits: 42 scheduled between September 1 and October 27. It stays the priority, and its budget is set high enough that budget is never what holds it back. On Google Ads, Google no longer gets credit for every call that comes in, and Search is judged on confirmed customers. Before we move more budget into Performance Max, we'll look at how many of its form leads turn into estimates, not just what each form costs.

**Internal (not for the client):**
- Last sentence KEPT (Edu 10-28) = real commitment: no more PMax budget increases on cost per form alone; needs a form → estimate check before any PMax step up.
- Avoided: "LSA has the largest share" (false for October: LSA $2,352 vs Google $2,640); the $357/day cap figure (sits well above the $5,929 plan); the 1-of-16 Search call stat (already sent 10-26).
- 42 scheduled estimates = LSA Booked Leads Review (30 Sept + 12 Oct 1-27).

---

## FINAL client message (assembled 10-28, for Angela to post in the Execution notes / send to Jared)

Attach: `Hawkins-Siding-Month-over-Month_2026-10-28.pdf` (table + "What Changed and Why", 1 page, plain style).

Here are answers to each point in your October 26 message.

**Branded search**
Branded search was paused on October 28 and stays off unless you decide otherwise.

**Spend across the Search ad groups**
The four ad groups share one daily budget, and Google's bidding splits it based on where it expects to find leads, so the spend won't be even across them. Siding General carried most of it in September because the other three were only split out of it on August 31 and were still building history. We review each ad group on the leads it actually brings in, form fills and calls we listen to, not just the cost Google reports. On October 29 we'll compare them side by side, and any ad group that isn't bringing in leads at a reasonable cost gets cut back so that money goes to the ones that are.

**Monthly budget**
We don't have a signed monthly budget on file for your account. What we do have are the media plans from the team that managed your account before. June was planned at $2,900 for Google Search and $7,000 for Local Services, and September at $3,630 for Google Ads and $5,929 for Local Services. We can't confirm whether those numbers were approved with you at the time. September came in under that plan, at about $2,805 on Google Ads and $5,636 on Local Services. We'd like to agree on a monthly budget with you for November and December, split by channel, so we're all working from the same number.

**Booked Local Services leads**
The Local Services review we sent on October 28 covers this lead by lead: where the 29 come from, what each call and message shows, and how to find each one in the Local Services inbox.

**How we manage the account**
Every week we review each channel on spend, cost per lead, search terms and how often the ads show, block searches that don't fit your business, and log the numbers so trends are visible over time. Some of what came out of that work:
- August 31: rebuilt Search into separate ad groups for siding repair, replacement and vinyl siding, each with its own ads and keywords
- September 14: reviewed every keyword and search term the Search campaign had run since April, to see which ones bring leads and which only spend
- October 5: blocked searches that weren't bringing real customers, such as handyman, Angi, grants, "how to" and supply store searches
- October 16: started reviewing every Search call recording each week, and blocked 26 more searches for other companies, product brands and job seekers

**Month over month**
You can check the trends in the PDF attached.

**Attribution**
Here's how leads are tracked today:
- Every call from Google Ads, Local Services and the website runs through CallRail, which records where the call came from and keeps the recording.
- Google Ads tracks form fills and calls of a minute or more for each campaign.
- Local Services tracks each lead in its inbox, with the status your office sets.

**Budget and lead quality**
Cost per form is one input, not the deciding one. On calls, we listen to the recordings and count only real customers, and we reviewed every Local Services lead from September and October the same way. That's how we know Local Services is the channel that turns into estimate visits: 42 scheduled between September 1 and October 27. It stays the priority, and its budget is set high enough that budget is never what holds it back. On Google Ads, Google no longer gets credit for every call that comes in, and Search is judged on confirmed customers. Before we move more budget into Performance Max, we'll look at how many of its form leads turn into estimates, not just what each form costs.

---

## Message to Angela (Edu, 10-28), wraps the final client message above

Hi Angela, here's the answer for Jared on the "Feedback on ads" task. It covers every point from his October 26 email.

A few notes before you send it:
- Attach the PDF Hawkins-Siding-Month-over-Month_2026-10-28.pdf. It has the month over month trends.
- The LSA review went to Damon on ticket #1043. Please make sure Jared has it too, since the answer points to it.
- The budget numbers come from the old media plans (internal only, don't share the links):
  - Q2: https://docs.google.com/spreadsheets/d/1yXcPF--RJge9zlH35o4Y-3iikIuvO4CKV-eELUEVaLc/edit?pli=1&gid=201159127#gid=201159127
  - Q3: https://docs.google.com/spreadsheets/d/17c1JJpruMEauwE15yXu8SfGDN--XQXeV/edit?gid=1740491738#gid=1740491738
  I can't tell if Eve or Mia got his approval on those, so the answer says that.
- Branded is already paused.

Here's the answer:

Here are answers to each point in your October 26 message.

**Branded search**
Branded search was paused on October 28 and stays off unless you decide otherwise.

**Spend across the Search ad groups**
The four ad groups share one daily budget, and Google's bidding splits it based on where it expects to find leads, so the spend won't be even across them. Siding General carried most of it in September because the other three were only split out of it on August 31 and were still building history. We review each ad group on the leads it actually brings in, form fills and calls we listen to, not just the cost Google reports. On October 29 we'll compare them side by side, and any ad group that isn't bringing in leads at a reasonable cost gets cut back so that money goes to the ones that are.

**Monthly budget**
We don't have a signed monthly budget on file for your account. What we do have are the media plans from the team that managed your account before. June was planned at $2,900 for Google Search and $7,000 for Local Services, and September at $3,630 for Google Ads and $5,929 for Local Services. We can't confirm whether those numbers were approved with you at the time. September came in under that plan, at about $2,805 on Google Ads and $5,636 on Local Services. We'd like to agree on a monthly budget with you for November and December, split by channel, so we're all working from the same number.

**Booked Local Services leads**
The Local Services review we sent on October 28 covers this lead by lead: where the 29 come from, what each call and message shows, and how to find each one in the Local Services inbox.

**How we manage the account**
Every week we review each channel on spend, cost per lead, search terms and how often the ads show, block searches that don't fit your business, and log the numbers so trends are visible over time. Some of what came out of that work:
- August 31: rebuilt Search into separate ad groups for siding repair, replacement and vinyl siding, each with its own ads and keywords
- September 14: reviewed every keyword and search term the Search campaign had run since April, to see which ones bring leads and which only spend
- October 5: blocked searches that weren't bringing real customers, such as handyman, Angi, grants, "how to" and supply store searches
- October 16: started reviewing every Search call recording each week, and blocked 26 more searches for other companies, product brands and job seekers

**Month over month**
You can check the trends in the PDF attached.

**Attribution**
Here's how leads are tracked today:
- Every call from Google Ads, Local Services and the website runs through CallRail, which records where the call came from and keeps the recording.
- Google Ads tracks form fills and calls of a minute or more for each campaign.
- Local Services tracks each lead in its inbox, with the status your office sets.

**Budget and lead quality**
Cost per form is one input, not the deciding one. On calls, we listen to the recordings and count only real customers, and we reviewed every Local Services lead from September and October the same way. That's how we know Local Services is the channel that turns into estimate visits: 42 scheduled between September 1 and October 27. It stays the priority, and its budget is set high enough that budget is never what holds it back. On Google Ads, Google no longer gets credit for every call that comes in, and Search is judged on confirmed customers. Before we move more budget into Performance Max, we'll look at how many of its form leads turn into estimates, not just what each form costs.
