# All Seasons AC — Meta Ads Log

**Ad account:** All Seasons Air Conditioning `2405306059725517` (owned by the client's business `154875572175833`,
ACTIVE, USD). Readable through the Meta Ads MCP.

> Running log of paid-social work on this account. Newest entry on top. One entry per work session: what we looked at,
> what we found, what we changed, and what's still open.

---

## 2026-10-19 — Weekly 7-day Meta pass (AT task 39ad03fd, Gui): campaign PAUSED since 10-15

`TSD_10.09_Awareness_Brand_TOFU_ARL` 120250742056430607 PAUSED 10-15 (~09:31 ET, same day as the Google cuts). $54.98 on 10-13..10-15, reach 9,937, freq 1.32, $0 since 10-16. KPI - Meta 10-19 $54.98 / Unclear. fu-030 frequency check is moot while paused. Keep off unless the client approves a Meta budget (client asked Meta OFF 04-15).

---

## 2026-10-12 — AT check: was Meta budget ever approved? No. Angela's "within budget" was the Google Branded task

**Read-only.** Edu remembered a task where he asked for Meta budget and Angela approved it herself as "within budget".
Went through all 150 All Seasons tasks in AT.

- **The "within budget" approval exists, but it's for Google, not Meta:** Internal Request `99d49b0e` "Extra $15/day
  Branded Investment" (08-31, requester Edu, Execution = Angela). Angela's execution note: "Thank you, please keep me
  posted on performance. Since we are still in budget I am not sending to client." Covers the Google Branded
  Evergreen campaign only.
- **The Meta task never went to Angela:** Internal Request `2758649a` "Create awareness campaign" (09-02, requester
  Edu, Execution = Andrea Mejia Vasquez, Review & Close = Edu, closed 09-03 00:10). Execution notes end with "Budget is
  not in the Q3 media plan... flagging so it gets added to the plan or approved separately." 0 comments, Angela on no
  stage, activity feed shows only Edu, Andrea and automation.
- Other Meta-ish tasks: "Client wants new FB ads" `d1bc29ad` (05-14, Jonathan, no notes) sits in Jonathan's 05-14
  batch of "(TEST)" entries, so not evidence of approval.
- The report request itself is Client Request `7a4c9a19` "Paid Ads Reporting" (Donna, 10-09): Execution on Edu,
  then Communicate on Angela.

---

## 2026-10-09 (later) — Client asked for Meta OFF on 04-15; nobody passed it on. Awareness still LIVE, decision pending

**Read-only. Nothing changed in the account.** Started from Angela's Slack question (10-09 11:52): she found a client
note from April 15 saying they want Meta turned off and asked if it was ever done.

### The note
Agency Titan, client **Notes** tab, 04-15, by Marissa Young: **"Meta Ads Turned Off: 04.15 - email - confirmed ALL
Meta campaigns are paused."** Before Edu joined (Eve's intro DM was 06-24).

### Was it done? Yes
- Meta activity log: campaign "Brand Awareness - TOFU -" (`120211947601150607`) set Active → Inactive on
  **4/15/2026 1:33 PM** by Armando Cabrera Calderon (Power Editor).
- Hiring lead-form campaign `TSD_03.12_Leads_Forms_Hiring` (`120240785878630607`): $374.92 in April, $0 since. Still
  shows ACTIVE but its ad sets ended 04-13 (see 10-05 entry).
- **Meta spend May–Aug: $0.**
- TSD relaunched awareness 09-02 (`TSD_09.02_Awareness_Brand_TOFU`, Edu's internal request `2758649a`, company-wide
  brand-formance rollout). Spend since: Sep $556.40 + Oct 1–9 $175.26 + new ARL campaign $0.63 = **~$732**.

### Did anyone tell Edu? No
- **Slack** (all "seasons" mentions since 04-14): nothing about the client wanting Meta off. Closest is Eve on 08-11:
  "are we only running google ads, not meta or LSA?" A question, not a heads-up.
- **AT tasks assigned to Edu for this client (19)**, details + comments read:
  - 30-Day Meta task (`350e8ced`, July) closed as "N/A nothing is active" with no reason given.
  - 7-Day Meta tasks kept arriving weekly 09-09 → 10-07.
  - Edu's own 09-02 "Create awareness campaign" task flagged "Budget is not in the Q3 media plan... flagging so it
    gets added to the plan or approved separately". Closed through Review & Close with no mention of the note.
  - Co-op task `099d11b4` (32 comments, Jun–Aug): Google/Mitsubishi only, nothing on Meta being off.
- **Tickets:** #935 "Facebook Charges", opened by the client 10-07, assigned to Angela (not Edu).
- **Client comments:** 0. The Notes tab is a separate entity.

### Correction owed
Edu's 10-08 Slack reply to Angela said "There's no record anywhere of All Seasons asking us to turn Meta off." **That
was wrong.** The AT tools used (`data_comments_list`, `search_tickets`, task details) don't return the client Notes
tab, so the search couldn't see it. Next time "did the client ask for X" comes up, ask for the Notes tab (UI or
screenshot) before saying there's no record.

### Current state
`TSD_10.09_Awareness_Brand_TOFU_ARL` (`120250742056430607`) LIVE at $20/day since this morning. That's against the
April request, and the client has a charges ticket open.

### Open
- [ ] Send Angela the correction + offer to pause (reply drafted in session).
- [ ] Decision (Angela/client): pause now until the client OKs Meta, or get approval / carve it out of the PPC budget.
  If paused, the 10-16 frequency check (fu-030) and the 10-09 open items below go on hold.

---

## 2026-10-09 — Awareness rebuilt: new ARL campaign LIVE (no frequency cap, Nassau + Suffolk ZIPs), old one paused

_Session read top to bottom: first attempt blocked by auto mode, then the cap turned out locked, then Edu ruled out any cap. Final state is under "Published (Edu's go) + self-QA"._

**Nothing changed in the account.** The first write (`optimization_goal` → `AD_RECALL_LIFT` on ad set
`120250180921990607`) was denied by the Claude Code auto-mode permission classifier, so the rest was staged.

Live state confirmed 10-09 (unchanged since 10-05): goal REACH, cap 2 impressions / 7 days, 21 cities × 25 mi,
location types home + recent, age 24–65 with Advantage+ audience on, locales English (US/UK). Campaign is CBO
$20/day, no campaign-level frequency control. Last 7 days $134.59 / 37,815 reached / freq 1.43.

Meta help (Frequency controls for auction): with Ad Recall Lift, **frequency cap stays available**; only *target
frequency* is unavailable. So the cap is raised, not dropped.

### First staged plan (SUPERSEDED: the 7/7 cap was dropped, Edu wants no cap; live spec in `meta_awareness_live_spec_2026-10-09.json`)
- `optimization_goal`: REACH → **AD_RECALL_LIFT**. Try in place first: it keeps both ads and their post IDs. If
  Meta rejects it, duplicate the ad set with the same 2 ads and turn the old one off.
- `frequency_control_specs`: 2 / 7 days → **7 / 7 days** (about once a day max, leaves room for ~3x/week).
- Geo: 21 cities × 25 mi → **all 204 Nassau + Suffolk ZIP codes** (GeoNames US postal file, county = Nassau or
  Suffolk), **home only**. List in `meta_awareness_zips_nassau_suffolk.txt` (Ads Manager accepts it via "Add
  locations in bulk" → ZIP). The Meta MCP has no location search, so county keys couldn't be looked up; in
  Ads Manager, typing "Nassau County" / "Suffolk County" works if it shows a County option.
- Age, Advantage+ audience, locales, brand safety: unchanged.

### Retry after Edu added the allow rule (same day)
- `ads_update_entity` went through but **as an Ads Manager draft** (`is_draft: true`), nothing live.
- Goal → ARL and geo → 202 ZIPs (dropped the IRS-only 00501/00544) staged OK on ad set `120250180921990607`.
- **Frequency cap is locked:** error 3858722 "Frequency control settings can't be changed on campaigns that have
  already started." In a CBO campaign the cap is a campaign-level setting, so a new ad set in this campaign would
  inherit 2/7 too. **Getting all three fixes needs a new campaign.**
- Putting the cap back to 2/7 in the draft did NOT clear the error (the draft keeps the field as changed). The MCP
  has no discard, so that ad set draft sits in Ads Manager with HAS_ERRORS and can't publish. Discard it in the UI.
- `ads_create_campaign` (new `TSD_10.09_Awareness_Brand_TOFU_ARL`, $20/day CBO) was blocked by auto mode.

### Edu's call: NO frequency cap at all, need at least 3x/week → new campaign built as a DRAFT (not published)
Edu added allow rules for the create tools. Staged, all 4 objects VALIDATED, no errors:
- Campaign `120250742056430607` `TSD_10.09_Awareness_Brand_TOFU_ARL`: Awareness, CBO $20/day, highest volume.
- Ad set `120250742067740607` `Nassau + Suffolk | Advantage+ Audience | 24-65 | ARL`: AD_RECALL_LIFT, **no
  frequency control**, 202 ZIPs home-only, age 24–65 as Advantage+ suggestion, locales/brand safety as before,
  Advantage+ placements.
- Ads (same creative IDs → same posts): Testimonial (Scott) `120250742075770607` (creative 1581058560422281),
  AC Video `120250742077520607` (creative 1997814800900727).
- ARL has no "minimum frequency" control. Meta's target frequency only works with Reach/ThruPlay + lifetime budget.
  So 3x/week is a thing to watch after week 1, not something the setup forces.

### Published (Edu's go) + self-QA
- New campaign published live; old `TSD_09.02_Awareness_Brand_TOFU` paused (only the campaign-level pause was
  published, not the broken ad set draft). Re-read live:
  - New campaign ACTIVE, $20/day, highest volume. Old campaign PAUSED, its 2 ads CAMPAIGN_PAUSED.
  - Ad set ACTIVE: AD_RECALL_LIFT, billing impressions, **no frequency control on it**, location type home only,
    202 ZIPs. Age reads 18–65+ hard with Advantage+ audience on (24–65 sent as suggestion), locales English US/UK.
    Placements: FB, IG, Threads; Meta dropped WhatsApp Status and Audience Network vs the old one (Advantage+
    placements' choice for ARL).
  - Ads: Testimonial (Scott) IN_PROCESS, AC Video PENDING_REVIEW (normal right after publish). No delivery errors.
  - Page: "All Seasons Air Conditioning" `142627692503960` (only page on the account), same IG account.
  - **Same posts as the old ads**: Testimonial `142627692503960_1736003831868966` (IG 17965229915966010), AC Video
    `142627692503960_1736003745202308` (IG 18154209307506847). Social proof carries.
  - CTA Learn More → seasonsair.com.
  - ⚠ 47 of the 202 ZIPs come back with no linked city in Meta (`primary_city_id: 0`). Most are PO-box ZIPs with no
    residents, but some are residential: 11509 Atlantic Beach, 11577 Roslyn Heights, 11579 Sea Cliff, 11729 Deer Park,
    11732 East Norwich, 11755 Lake Grove, 11767 Nesconset, 11778 Rocky Point, 11786 Shoreham, 11797 Woodbury, plus
    North Fork ones (11939, 11942, 11947, 11948, 11956, 11970, 11972). Meta accepted all 202 as targets; whether
    those deliver can't be checked from the MCP. Look at the map in Ads Manager.

### Still open
- [ ] Discard the broken draft on old ad set `120250180921990607` in Ads Manager (still HAS_ERRORS; harmless now).
- [ ] Check the ZIP map in Ads Manager for the 47 unmapped ZIPs.
- [ ] ~10-16: first full week. Frequency toward ≥3/week with reach holding; CPM vs old ~$2.50.
- [ ] Creative: 1–2 brand-recall pieces from the video team.
- [ ] Close AT task `630fe022`.
- [ ] Creative: 1–2 brand-recall pieces from the video team.
- [ ] After: frequency should climb toward ~3/week with reach holding; CPM likely up from ~$2.50.
- [ ] Close AT task `630fe022`.

---

## 2026-10-05 — Weekly 7-day check (Agency Titan task), changes logged for Edu to make 10-06

**Read-only. Nothing changed in the account.** Agency Titan task "7-Day Meta Ads Optimization" (`630fe022`, due 10-06)
left open for Edu. KPI - Meta entry for 10-05 added to the client.

### What's live
One campaign: `TSD_09.02_Awareness_Brand_TOFU` (`120250180921760607`), objective Awareness, $20/day, running since
09-02. One ad set: `Long Island | Advantage+ Audience | 24-65` (`120250180921990607`). Two ads: "Testimonial (Scott)"
(`120250180922650607`) and "AC Video" (`120250180923270607`). Two lead-form ad sets from March
(`NewBabylon_InstantForms_HVAC`, `..._SeniorHVAC`) still show ACTIVE but ended 04-13 and spend $0.

### Last 7 days (09-28 → 10-04)

| Spend | Impressions | Reach | Frequency | CPM | CTR | Cost per 1,000 reached | Leads |
|---|---|---|---|---|---|---|---|
| $139.57 | 55,251 | 37,707 | 1.47 | $2.53 | 0.05% | $3.70 | 0 (awareness) |

By ad: Testimonial (Scott) $120.11 (86%), AC Video $19.46 (14%).

Weekly since launch (Wed–Tue weeks): 09-02 $117 / 33.1k reached / freq 1.43 · 09-09 $138 / 39.5k / 1.41 ·
09-16 $140 / 37.3k / 1.44 · 09-23 $142 / 37.8k / 1.41. CPM $2.48–2.66 throughout. Activity log since 09-21: no
changes by anyone, only Meta automation (auto custom audiences, billing, spending-limit reset to $2,000 on 10-01).

### What's off vs the TSD Meta method
1. **Optimization goal is Reach**, not Ad Recall Lift. Reach optimization spreads spend over as many new people as
   possible, which keeps frequency low by design.
2. **Frequency cap: 2 impressions per 7 days.** Makes the ~3x/week awareness target impossible. Actual sits at ~1.4.
3. **Geo is far wider than the service area.** 21 North Shore towns + West Babylon, each with a 25-mile radius. A
   25-mile circle around Great Neck / Kings Point covers Queens, the Bronx, Manhattan, Westchester and the CT shore.
   Location type is "home + recent" (people recently in the area), not people living there only. Google targets
   Suffolk County, Nassau County and West Babylon.
4. **Creative is thin and aging:** 2 ads for 5 weeks, one taking 86% of spend.

### To do (Edu, 10-06)
- [ ] Switch the ad set to **Ad Recall Lift** optimization. This resets learning, and Meta may require a new ad set
  for the switch (duplicate the ad set, keep the same post IDs, turn the old one off).
- [ ] **Raise or remove the frequency cap** so it can reach ~3x/week.
- [ ] **Geo:** replace the 21 cities × 25 mi with Nassau County + Suffolk County, "people living in this location" only.
- [ ] **Creative:** request 1–2 new brand-recall pieces from the video team (purpose-built for awareness, not
  conversion creative).
- [ ] After the changes, watch frequency climb toward ~3x/week with reach holding, CPM likely up from $2.50.
- [ ] Close the AT task (`630fe022`) once done.
