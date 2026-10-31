# Mission Accomplished — Meta Ads Log

**Client:** Mission Accomplished (HVAC — Mohave County tri-state: Lake Havasu City, Bullhead City, Fort Mohave, Mohave Valley AZ · Laughlin NV · Needles/Big River CA · Parker AZ)
**Ad account:** `79203382` ("Mission Accomplished", business Topservdigital, USD)
**Platform:** Meta Ads, queried via Meta MCP (no local script toolkit for this account).

> Running log of paid-social work on this account. Newest entry on top. Google Ads work lives in `google-ads-log.md` in this same folder.

---

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

**Scope:** read-only (Meta MCP), no account changes. 7-Day + 30-Day Meta tasks completed.

- **7d 10-19..10-25:** awareness only, ARL campaign ($30/d) $210.96 (prior $206.49), reach 21,602, freq 1.85 (prior 1.78), CPM $5.29, CTR 0.29%, 960 est. recallers ($0.22). 0 leads.
- **30d 09-26..10-25:** $901.06, 175,542 impr, reach 60,883, freq 2.88, recallers 2,610 = 4.29% of reach, hook 18.42%, retention 11.20%. Control = Video 01 How Often to Service Your AC (39% of spend, 2.40% ThruPlay/impr); testimonials weakest (Kelly 1.39%).
- **Off doctrine (found 10-26):** weekly freq under 3x; Advantage+ audience OFF (age 30-65 + 40 km radii); location type home + **recent**; **Kingman** targeted but not in our service-area list. No freq cap (correct).
- **Staged, not applied:** home-only location; confirm/remove Kingman with AM; Advantage+ audience on; heating/fall creative refresh (all 6 videos AC/summer, live since 09-03); pause Video 06 Kelly when refresh goes in; lead gen relaunch only after GHL to Hatch joint test, lead with New System $125/mo.
- KPI - Meta row 0a07bc40 (weekly + 30d keys). Tasks: https://app.agencytitan.com/tasks/instance/6def4a53-2f3c-4211-8c0c-3695ad9cd092 · https://app.agencytitan.com/tasks/instance/bebf170d-13fe-4ca8-bca7-2f2396c960ca

---

## 2026-09-29 — Client Facebook report built (lead gen pre-pause + awareness)

**Scope:** Ad account `79203382`. Read-only, live pull via Meta MCP. No account changes. Ticket from Angela (AM): "Client has requested a performance report for Facebook leads."

**Deliverable:** `Mission Accomplished - Facebook Ads Report (Sep 2026).pdf` (source `Mission-Accomplished-Facebook-Ads-Report_2026-09-29.html`), 3 pages, plain format.

**Windows:** lead gen = 30 days ending on the pause day, **Aug 11 to Sep 9** (lead campaign `52605597930342` set Active→Inactive 9/9 5:11 AM by Jonathan Bannister; 9/9 had $7.68 partial). Awareness = **Aug 30 to Sep 28**, but the campaign `52605605054542` only went live 9/3.

**Lead gen numbers (internal read):** $1,283.02 / 22,086 impr / 148 link clicks / **5 leads / $256.60 CPL**, CPM $58.09. Leads on 8/13, 8/14 (Your Friendly Pros), 8/31, 9/6, 9/7 (New System $125/mo, Tech + Van image, $90 CPL across both runs). Free Second Opinion, Overpaying, $75 Tune Up, Comfort Club = $0 leads. No lead spend 8/20 to 8/27 (creative wait, see 09-16 entry). Honest read: CPL is poor; only the $125/mo offer earned its keep.

**Awareness numbers:** $476.86 / reach 37,249 / 92,789 impr / freq 2.49 / CPM $5.14 / 1,710 est. ad recall lift ($0.28) / 1,698 ThruPlays / 69 link clicks. Budget stepped ~$10/d → ~$20/d on 9/15 → ~$30/d on 9/21 (Jonathan's edits). IG 57% of impr, FB 40%, Threads 3%. Targeting: 30 to 65, 40 km around Lake Havasu City, Bullhead City, Kingman, Parker, Needles.

**Pause context (from Slack, not in any log before this):** client said Meta leads weren't arriving → Edu paused lead gen 9/9. Angela 9/14: leads DO land in GHL with phone, but the **Hatch** notification email doesn't carry the phone number (Zapier/GHL→Hatch mapping). Angela's view: not on our side. Status of that connection as of 9/29 unknown. Per the GHL gate, lead gen shouldn't be called live again until a joint test lead passes end to end.

**Framing in the client PDF:** pause presented as protecting spend while the GoHighLevel→Hatch handoff gets sorted; no blame assigned; Aug 20–27 break mentioned neutrally as creative production; next steps = test lead → relaunch leading with $125/mo offer → keep awareness on.

**Status:** PDF done and reviewed by Edu 09-29, to hand to Angela through the AM ticket (not sent directly to the client). Open before sending: confirm Hatch connection status, keep or cut the Aug 20–27 line, confirm the $125/mo relaunch plan. Report is Meta only; Angela's 09-29 question on "what's been running" also covers Google PPC (paused since 7/7) and LSA.

*Reversibility: no account changes made.*

---

## 2026-09-16 — Mapped lead-gen shutdown, awareness campaign start, and the Aug 26–27 gap

**Scope:** Ad account `79203382`. Read-only, live pull via Meta MCP (`ads_get_ad_entities`, campaign + daily spend). No account changes.

**What we checked:** When lead-gen spend stopped, when the current awareness campaign started, and whether there was a dead stretch with nothing running in between.

**Findings:**
- **Meta lead-gen (OUTCOME_LEADS) stopped 2026-09-09.** Last live lead campaign was `TSD || LEADS || 03Sep26 - New Creatives` (id `52605597930342`) — spent through 9/9 (partial day, $7.68), then paused. No lead-objective spend since.
- **Current awareness campaign `TSD_2026-09_TOF_AWARENESS_CBO_Evergreen - Ad Recall Lift`** (id `52605605054542`, objective OUTCOME_AWARENESS) was **created and started spending 2026-09-03**, still active today (~$10–19/day). It's the only thing running on the account right now.
- **Real 2-day hiatus found: Aug 26–27, 2026 — $0 account-wide, no campaign of any kind active.** Sequence: lead campaigns "9JUL26" and "11AUG26 - Free Second Opinion" wound down by 8/19; a small BOF awareness campaign (`TSD_04.27_BOF_Awareness_CBO_Evergreen`) carried ~$5/day through 8/25 then dropped to $0.85 and stopped; nothing ran 8/26–8/27; `TSD || LEADS || 28AUG26 - New Creatives` picked lead-gen back up on 8/28.
- Note: the weekly "New Creatives" campaign swaps (28AUG26 → 03Sep26 → next) are creative refreshes, not real gaps — spend is continuous across those transitions.

**Answer delivered to Edu:** Google PPC off since 7/7 (still fully paused today); Meta lead-gen off since 9/9; Meta awareness live since 9/3; one real gap on Meta, 8/26–8/27, otherwise continuous.

*Reversibility: no account changes made.*
