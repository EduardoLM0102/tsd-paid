# Napps — 6-month investigation: "spent more, revenue down"

**Prepared:** 2026-09-24, for Edu (internal, to relay to Angela/AM). Not client-facing.
**Window:** last 6 months = 2026-03-24 to 2026-09-23. Compared to the same window in 2025 (2025-03-24 to 2025-09-23).
**Systems read (read-only, no account changes):** Google Ads PPC `9509605037`, Google LSA `9239407401`, Meta `438790276573563`, GA4 property `383876275`, Slack, Drive (Q3 media plan, Sep 8 call-tracking audit). Queries are in `napps-investigation-2026-09-24_scripts/`.

Tags used: **[data]** pulled from a platform API, **[doc]** stated in Slack/Drive, **[inference]** my reading, **[unverified]** could not confirm.

---

## 1. The answer in six lines

1. **"Spent more" is true.** All paid media (Google PPC + LSA + Meta) was **$51,948 vs $39,476** in the same window last year (**+32%**). YTD $63,135 vs $49,709 (+27%). Meta is the whole increase (+$13.4k). Google PPC +$5.8k. **LSA is down $6.7k.** [data]
2. **Nothing in the data proves or disproves the revenue drop.** We have no revenue, jobs or booking data. Every number below is leads or traffic. [unverified]
3. **The Google PPC lead engine changed on Jul 5.** PMax Plumbing went from $551/week to $17/week (impressions −98%) while still enabled. Non-brand Google cost per counted conversion went from **$107 (Apr 8–Jul 5) to $380 (Jul 6–Sep 23)**. [data]
4. **The client told us to stop HVAC ads (Jul 3) and AC tune-up ads (Jul 22). The Google HVAC campaign is still running.** `TSD_07.21_Search_Nonbranded_AC_Summer` spent **$5,024** since Jul 23, the AC Tune-Up ad group is ENABLED. Only the Meta AC tune-up ad set was turned off. I found no record of the client re-approving HVAC. [doc + data]
5. **LSA (the cheapest channel, ~$38/lead) has fewer leads: 499 → 366 (−27%), and the business status-declined 111 of 366.** 62 of 118 leads since Aug 1 are `DECLINED`. This is the only hard data point that matches "we turned leads away". It hits plumbing too (29 of 54 in Aug), not only HVAC. [data]
6. **We cannot currently show which channel produced a booked job.** Napps' CallRail was dismantled (9 numbers released), GBP publishes the client's own line, LSA has no tracked number, and the site's phone-tap tag stopped in Aug. [doc + data]

---

## 2. Spend and lead evidence side by side

### Spend (USD)

| Channel | 2025-03-24 → 09-23 | 2026-03-24 → 09-23 | Change |
|---|---|---|---|
| Google PPC | 17,543 | 23,345 | +5,802 (+33%) |
| LSA | 20,787 | 14,066 | −6,721 (−32%) |
| Meta | 1,146 | 14,537 | +13,391 |
| **Total** | **39,476** | **51,948** | **+12,472 (+32%)** |

YTD Jan 1–Sep 23: Google 20,067 → 29,933 · LSA 28,496 → 18,066 · Meta 1,146 → 15,136 · Total 49,709 → 63,135.
Not included: TSD fees. Meta 2025 comes from the only queryable account. Two older closed Napps Meta accounts exist (`1908505679437547`, `1908493696105412`) and could not be read, so 2025 Meta may be understated. [data]

### Lead-side evidence that does not depend on conversion tags

| Source | 2025 window | 2026 window | Note |
|---|---|---|---|
| Google Ads calls via call assets (call_view) | 87 (41 missed) | 90 (2 missed) | ≥60s: 25 → 55. **Excludes PMax and website phone taps** |
| LSA leads | 499 (400 charged) | 366 (227 charged) | HVAC 137 → 92 · plumbing 324 → 231 · other 38 → 43 |
| LSA cost per lead | $42 | $38 | efficiency flat, volume down |
| Meta leads | 34 | 181 | 31 are job-applicant leads from the hiring campaign; quality of the rest unknown |
| GA4 sessions, Paid Search + Cross-network, Jul/Aug/Sep | 543 / 447 / 417 | 119 / 92 / 88 | **−80%** |
| GA4 sessions, Organic Search, Mar–Sep avg | 202 | 198 | flat |

Reading: paid website traffic collapsed, organic did not. LSA volume fell. Google phone calls via ads are flat but answered calls went up (2025 had 41 missed). Meta added volume of unknown quality. I did not add these into one blended lead number because the definitions differ.

Monthly detail is in the appendix.

---

## 3. Findings

### F1. Where the extra spend went [data]
Meta went from ~$0 to $2.6–3.7k/month (May–Aug 2026). Google PPC was $5.1–5.3k in Apr–May 2026 vs $1.9k in Apr–May 2025. LSA fell from $3.5–3.9k/month (Mar–Jul 2025) to $1.4–2.0k (Jan–May 2026), then $3.1–3.2k in Jun–Jul.
Slack Apr 1: "Approved Napps Media Budget for Q2 2026 = $10,500" (unit not stated; the Q3 sheet uses $10,500 as the July monthly total for all three channels). Monthly totals Apr–Jun 2026: $7.1k, $9.9k, $10.0k.
**Check:** Google Ads UI cost by month; LSA account `923-940-7401`; Meta Ads Manager.

### F2. Google PPC lead engine changed on Jul 5 [data + inference]
- PMax Plumbing (`23590336249`) by week: week of Jun 29 **$551, 133 clicks, 5,058 impressions** → week of Jul 6 **$17, 1 click, 116 impressions**. Daily: Jul 4 $38, Jul 5 $5, Jul 6 $0. Campaign stayed ENABLED with a $110–130/day budget until it was paused (last spend Aug 10).
- Same day, per Google `change_status` (timestamps show what changed, not who): 2026-07-05 08:55 a shared negative list "TSD - Master Negatives NonBranded (Jul 2026)" (142 terms) was attached to 5 campaigns including PMax, and at 08:56 11 campaign criteria on PMax changed. A new campaign `Leads_Search_Nonbranded_Plumbing` was also built that morning.
- PMax carries a **$80 target CPA** (`maximize_conversions.target_cpa_micros = 80000000`). I cannot see when it was set.
- Slack Jul 3 (#topserv-paid-ads-department, Andrea): the process is hard because "everything that was converting was going toward HVAC", Meta is paused, new things are launching on Google, "the results will have an impact, a big one."
- Windows (Google PPC only, counted conversions = Calls from ads + Click to call):
  - Apr 8–Jul 5 (89 days): $13,985 spend, 132 conversions. Non-brand $13,255 / 124 = **$107**.
  - Jul 6–Sep 23 (80 days): $9,344 spend, 54 conversions. Non-brand $6,846 / 18 = **$380**. Brand $2,498 / 36.
- ~~**Caveat [unverified]:** 106 of the 186 counted conversions in the 6-month window came from PMax "Calls from ads", and `call_view` has **zero PMax rows**, so I cannot confirm those were real calls.~~
  **CORRECTED 2026-09-30:** `call_view` does have PMax rows. The original query selected `ad_group.name`, and because PMax has no ad groups its rows were silently dropped. PMax 2026-03-24 → 09-23: 760 calls, 18 missed, median 24s, 458 under 30s, **124 at 60s or longer** (Apr 51, May 24, Jun 39, Jul 10, Aug 0). This supports F2: real calls of a minute or more disappeared along with PMax delivery in July. The search-only figures elsewhere in this doc are unaffected. Details are in the 09-30 entry of `clients/napps/google-ads-log.md`.
- I did not find what caused the collapse. The Jul 5 changes are coincident, not proven. **Check:** Google Ads UI → Tools → Change history, filter Campaign = PMax Plumbing, Jun 28–Jul 10 (API only keeps 30 days). That shows who and what.

### F3. HVAC still running after the client said stop [doc + data]
- Jul 3 (Mia Kelly, AM at the time): needs to tell Napps "we are not running HVAC ads for them and only plumbing"; later "since we paused the hvac campaigns". Agency Titan task linked in that message.
- Jul 22 (Andrea, per your Jul 22 notes in a group DM): Napps asked to stop the AC tune-up ads and focus only on plumbing, "so I turned off the ads". Meta log: ad set `AC_$79_TuneUp_30.65_Leads` created Jul 22, activated 01:29, set to Inactive Jul 23 00:17.
- Google: `TSD_07.21_Search_Nonbranded_AC_Summer` launched Jul 21–23 and is ENABLED today. Since Jul 21: AC Repair $2,599 (4 conv), **AC Tune-Up $1,683 (8 conv)**, AC Replacement $741 (2), AC Installation $0. Total **$5,024, 14 counted conversions** (22 calls in call_view).
- Workspace log: Aug 3 budget moved $20/day from PMax to AC Summer; Aug 31 negatives, ad group split, landing page changes; Sep 15 budget $100 → $1 → $50.
- I found no message where the client re-authorised HVAC. Agency Titan is not readable from here. **Check:** the Titan task from Jul 3 and any client reply.
- Why it matters: the client says they turned HVAC leads away in the hot months. This is HVAC spend during that period.

### F4. Brand campaign CPC blew up in August [data]
- `TSD_03.22_Search_Branded_Evergreen`: Apr–Jul 71 clicks, $954 = **$13.4/click**. Aug–Sep 68 clicks, $2,289 = **$33.7/click**.
- Search term "napps ac": $3.19/click (Apr–Jul, 6 clicks) → **$54.78/click** (Aug–Sep, 16 clicks). Aug 26 and Aug 28: **$239 per day for 2 clicks each**.
- Brand demand is small: Keyword Planner shows "napps longview tx" 30/month, "napps ac" 10/month. The campaign gets 150–310 impressions/month.
- Brand is now most of the reported wins: 36 of 54 counted conversions since Jul 6 (67%), 16 of 17 in Sep. That is people who already know Napps, not new demand.
- Bidding is Maximize Conversions with no CPA cap, $60/day budget. Cause of the CPC jump is **[unverified]** (competitor bidding on the name is one candidate). **Check:** Auction Insights for that campaign, Aug–Sep vs Apr–Jul (not available through the API).

### F5. The plumbing focus has produced nothing on Google Search yet [data]
- `TSD_06.05_Leads_Search_Nonbranded_Plumbing`: $1,391, 0 conversions (May 7 run + Sep 15 restart). `Leads_Search_Nonbranded_Plumbing` (Jul 7–20): $977, 13 clicks, 0 conversions. Together **$2,368 for 0 counted conversions**.
- Market price: Keyword Planner top-of-page bid for "plumber longview tx" (590 searches/month) is **$34–$93**; "ac repair longview tx" $31–$67. So $30–$100 clicks are what this auction costs, not a setup glitch. At those prices Google Search cannot produce cheap leads here. LSA at ~$38/lead can. **[inference]**
- Keyword Planner returns only 12 months, so I cannot give demand year over year.

### F6. Campaign churn [data]
Five non-brand builds launched Apr–Sep spent **$7,595 (32% of Google spend in the window) for 22 counted conversions ($345 each)**: PMax Emergency $1,929/13 · Nonbranded Evergreen $1,736/4 · Nonbranded HVAC $1,562/5 · TSD_06.05 Plumbing $1,391/0 · Leads Plumbing $977/0. Each restarts learning with a fresh budget.

### F7. Nobody can currently prove channel ROI [doc + data]
- Sep 8 call-tracking audit (Ryan): Napps' CallRail account "was dismantled. 9 numbers released including GMB, the website pool, Facebook and 5 Google Ads extensions. 2 numbers remain." Crystal shows 20 calls in 90 days vs 139–774 for comparable accounts.
  My check: Google's own call records show **55 ad calls in Jun 10–Sep 8**, so the tracking layer is missing most calls.
- Sep 10–11 (Ryan): GBP publishes Napps' own line (903-686-1289), "every GMB call goes straight to them and we see none of it". LSA has no tracking number. "Napps is running two paid channels blind." LSA at that time: "$549 spend and 13 call leads this period."
- Same audit, section 6: "All Seasons Air and Napps are pushing conversions into Supreme's Google Ads account." **[unverified by me]**: Supreme's upload actions (`Phone Call`, `Form Capture`) show no conversions May–Sep. What I can confirm is that Napps' own `GHL Form Fill` action never recorded a conversion in the account's history.
- Site tags (GA4): `phone_link_click` fell to 2 in Aug and 0 in Sep, replaced by `phone_click` (21, 16). Old and new events do not overlap, so trend lines across Aug are not comparable. Website form events are tiny in both years (~3–10/month).
- Consequence: any statement about which channel drives revenue is a guess until Napps supplies booked-job data by source.

### F8. Feb–Mar 2026 junk traffic poisoned the account's conversion history [data]
PMax Plumbing, Feb 20–Mar 3: 193k clicks, 4,005 counted conversions, $665 spend (mostly YouTube and Display placements at under $0.01/click). The HVAC PMax spent another $361 in the same days. GA4 logged 67,948 (Feb) and 49,453 (Mar) "Cross-network" sessions and 3,499 / 2,216 `phone_link_click` events. Feb–Mar conversion counts are unusable. Real damage in dollars is small; the harm is what Smart Bidding learned.

### F9. LSA: fewer leads, and many declined [data]
- Monthly LSA leads: 2025 = 61, 67, 86, 92, 95, 86, 89, 66, 64, 70, 62, 65 · 2026 = 46, 34, 42, 42, 45, 76, 71, 81, 41 (Sep to the 23rd). Jan–May 2026 is roughly half of Mar–Jul 2025.
- Not budget-limited: LSA budget is $154.29/day (~$4.7k/month) while spend was $1.4–2.0k/month in Jan–May 2026. Why volume dropped is **[unverified]**. **Check in the LSA app:** profile status, review count/rating, business hours, job types, response time.
- `DECLINED` status per Google's API enum means declined by the business (confirm in the LSA app by filtering leads on Declined). By month (declined / total): Feb 16/34 · Mar 24/42 · Apr 14/42 · May 6/45 · Jun 6/76 · Jul 17/71 · **Aug 44/81 · Sep 18/41**. The week of Aug 17 alone has 21.
- Aug split: 15 HVAC, 29 plumbing declined. So this is not only an HVAC capacity story.
- Feb–Apr also had ~46% declined, so declining leads is not only a summer behaviour.
- 71 of the 111 declined leads (window) were charged. Declining costs money.
- Call lengths on LSA leads are normal (median ~2 min in Aug), so calls were answered. Statuses depend on what someone marked in the LSA app, so "BOOKED" is not a reliable job count.

### F10. Site and organic [data]
Organic Search sessions are flat (~200/month) and Direct is flat to slightly up, so no evidence of an organic collapse. Slack #seo-team (Sep 10): Napps is one of 6 WordPress sites "that had spam pages injected"; a malware/backdoor check is a card for Sha. Date and duration of the injection are unknown. Today's homepage fetch showed no spam and a single phone number (903-758-6482). Google call assets use 903-289-7073 at campaign level and 903-758-6482 at account level. **[unverified]** which one is a live tracked line.

### F11. Meta [data + doc]
- Campaigns: `TSD_04.24_TOF_LEADS_CBO` (May–Sep, $11,732, 150 leads, ~$78 each, monthly CPL $129 → $58 → $77 → $69 → $87), awareness `TSD_02.24_TOF_AWARENESS_CBO_Creatives` (Feb–Jun, $2,228, 0 leads), `Ad Recall Lift` ($383), `Hiring_HVAC_Refrigerator` ($676, 31 applicant leads, Jun 5–Jul 2).
- The hiring campaign is a data point for the staffing constraint: the client was recruiting HVAC/refrigeration techs from early June.
- Edu on Slack Sep 23: awareness campaign paused around end of August by Andrea, reason not found. Andrea is no longer at TSD.
- Meta lead quality is **[unverified]**: we do not know how many of the 150 became jobs.

---

## 4. Timeline (source in brackets)

| Date | Event |
|---|---|
| 2024-04 → 2025-01 | Prior agency "BC" campaigns, $2.1–2.5k/month, 32–61 ad calls/month [data] |
| 2025-02 | Google PPC spend $0 [data] |
| 2025-03 → 06 | ~85% of Google clicks from Search Partners at ~$1.20/click; "conversions" were site click events [data] |
| 2025-07 → 12 | Partners taper off; Google Search CPC $16–19; paid sessions fall from 1,289 (Jun) to 139 (Dec) per month [data] |
| 2026-02-20 → 03-03 | PMax junk traffic (F8) [data] |
| 2026-04-01 | Q2 budget approved, $10,500 [Slack] |
| 2026-04-08 | PMax Plumbing restarted; PMax Emergency Apr 9 [data] |
| 2026-06-04/05 | Meta hiring campaign for HVAC/refrigeration techs [Meta log] |
| 2026-07-01/02 | Nonbranded HVAC campaign changed, last spend Jul 1; Meta hiring paused Jul 2 [Google change_status, Meta log] |
| 2026-07-03 | Client wants plumbing only; team warns of "a big" impact [Slack] |
| 2026-07-05 | Master negative list attached, PMax criteria changed, PMax delivery collapses [data] |
| 2026-07-21 | AC Summer (HVAC) launches on Google [data] |
| 2026-07-22 | Client asks to stop AC tune-up ads; Meta ad set off Jul 23; Google unchanged [Slack, Meta log, data] |
| 2026-08-03 | Budget moved $20/day PMax → AC Summer [workspace log] |
| 2026-08-10 | PMax last spend; paused by Aug 12 [data] |
| 2026-08-17 week | 21 LSA leads declined [data] |
| 2026-08 (end) | Meta awareness paused [Slack] |
| 2026-09-08 | CallRail audit: Napps account dismantled [Drive] |
| 2026-09-15 | Tracking rebuilt; AC Summer $100 → $1 → $50; Plumbing search re-enabled at $50 [workspace log, change history] |
| 2026-09-23 | Angela meets Napps [Slack] |

---

## 5. What I could not verify

1. Revenue, jobs, booked jobs, average ticket, by month or by service line. **This is the missing piece.**
2. Whether PMax "Calls from ads" (106 in the window) were real calls.
3. What caused the Jul 5 PMax collapse and who paused PMax in August (Google change history older than 30 days is UI-only).
4. Why brand CPC jumped in August.
5. Why LSA volume dropped in Jan–May 2026, and why leads were declined.
6. Quality of the 150 Meta leads.
7. The client's exact words. I only have Slack relays of them.
8. The Supreme conversion misrouting, beyond what the audit states.
9. When the CallRail numbers were released.

## 6. What to ask for next

**From Napps (via Angela):** monthly revenue and job counts Jan 2025 → now, split HVAC vs plumbing, with lead source per job if their system has it; who is working the LSA app and what "Declined" meant; whether they want HVAC ads on or off from today; when HVAC capacity returns.
**Internal:** Google Ads change history Jun 28–Jul 10 (PMax) and Aug 3–12; Auction Insights for the brand campaign; the Agency Titan Jul 3 task; whether 903-289-7073 is a live tracked line; date the CallRail numbers were released.
**Decision needed from you, not from data:** AC Summer is still spending HVAC budget against the client's Jul 3 and Jul 22 requests. I did not change anything. Say if you want it paused pending the client's answer.

---

## Appendix. Monthly detail

| Month | Google PPC $ | LSA $ | Meta $ | Total $ | Google ad calls (missed) | LSA leads | Meta leads | GA4 paid sessions | GA4 organic sessions |
|---|---|---|---|---|---|---|---|---|---|
| 2025-01 | 2,060 | 1,968 | 0 | 4,028 | 41 (1) | 61 |  | 62 | 207 |
| 2025-02 | 0 | 2,887 | 0 | 2,887 | 7 (4) | 67 |  | 0 | 199 |
| 2025-03 | 897 | 3,512 | 0 | 4,409 | 5 (2) | 86 |  | 651 | 213 |
| 2025-04 | 1,944 | 3,875 | 0 | 5,820 | 5 (1) | 92 |  | 1,074 | 194 |
| 2025-05 | 1,871 | 3,821 | 0 | 5,692 | 8 (7) | 95 |  | 954 | 168 |
| 2025-06 | 3,067 | 3,865 | 0 | 6,932 | 34 (25) | 86 |  | 1,289 | 219 |
| 2025-07 | 4,131 | 3,904 | 60 | 8,095 | 19 (5) | 89 |  | 543 | 248 |
| 2025-08 | 3,139 | 2,934 | 626 | 6,699 | 7 (0) | 66 | 17 | 447 | 208 |
| 2025-09 | 3,712 | 2,158 | 597 | 6,466 | 13 (1) | 64 | 27 | 417 | 168 |
| 2025-10 | 3,292 | 2,628 | 401 | 6,321 | 10 (0) | 70 | 21 | 335 | 161 |
| 2025-11 | 2,438 | 2,700 | 0 | 5,139 | 15 (0) | 62 |  | 156 | 165 |
| 2025-12 | 2,935 | 2,384 | 0 | 5,319 | 15 (0) | 65 |  | 139 | 145 |
| 2026-01 | 3,287 | 1,585 | 0 | 4,872 | 21 (0) | 46 |  | 182 | 141 |
| 2026-02 | 3,076 | 1,395 | 137 | 4,608 | 8 (0) | 34 |  | 68,066 | 155 |
| 2026-03 | 225 | 1,595 | 622 | 2,442 | 0 (0) | 42 |  | 49,456 | 168 |
| 2026-04 | 5,098 | 1,416 | 598 | 7,111 | 9 (0) | 42 |  | 3,036 | 136 |
| 2026-05 | 5,259 | 1,963 | 2,707 | 9,929 | 12 (0) | 45 | 21 | 1,127 | 276 |
| 2026-06 | 3,270 | 3,064 | 3,698 | 10,032 | 9 (1) | 76 | 63 | 361 | 207 |
| 2026-07 | 2,174 | 3,220 | 2,938 | 8,332 | 16 (0) | 71 | 38 | 119 | 213 |
| 2026-08 | 3,959 | 2,553 | 2,617 | 9,128 | 25 (0) | 81 | 38 | 92 | 235 |
| 2026-09 (to 23rd) | 3,586 | 1,276 | 1,820 | 6,682 | 19 (1) | 41 | 21 | 88 | 152 |

Notes: Google ad calls exclude PMax and website phone taps. GA4 paid sessions = Paid Search + Cross-network; Feb–Mar 2026 is the PMax junk. Google PPC $ for Feb 2025 is zero, but 7 ad calls (4 missed) were logged that month from the prior agency's campaigns.
