---
name: tsd-spencer-air
description: Spencer Air (DFW HVAC) TSD client — Google PPC 2524618054 + Meta 1845825982372184; 2026-07-28 lead-quality ticket findings (Google = LSA maintenance shoppers; Meta = hold until CRM outcomes)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8050edc5-1d01-4428-9daf-2ff9c7ff24db
  modified: 2026-09-25T13:38:39.834Z
---

Spencer Air Conditioning — TSD client, HVAC in the **Dallas–Fort Worth metroplex** (Dallas, Plano, Arlington, Irving, Grand Prairie, Carrollton, Coppell, Flower Mound, Grapevine, Southlake, Lewisville, Addison, Allen, Bedford, Farmers Branch, Highland Village, The Colony). Client folder now exists at topserv-workspace/clients/spencer-air/ (google-ads-log.md, Q1 2027 strategy + marketing calendar), but it's still **NOT in the google-ads-ratos contas.yaml** (found it by listing children under the TSD MCC 4155514468). See [[topserv-google-ads-location]].

**Accounts**
- Google Ads PPC (LSA lives inside same account): customer_id **2524618054**, under TSD MCC 4155514468 (local google-ads-ratos skill + tsd.sh wrapper).
- Meta ad account **1845825982372184** (business_id 1664180080536776; pixel/dataset "Spencer Air's Pixel" 1258997717469696).

**2026-07-28 ticket** — Michele relayed Rosie: leads are now local but still not converting to opportunities; Tiffany follows up by call + email and prospects don't answer/respond. Asked to review Google + Meta lead quality. (Ignore Meta execution for now per Edu.)

**Google findings (last 30d)** — geo is tight/managed DFW (city targets + negative-location block), so location is NOT the problem.
- Active = LSA (system-gen campaign 15789372405, ~$164/day, Maximize Leads) + Branded Search "TSD_07.05_Leads_Search_Branded" 23822436393 ($50/day, Max Conversions). Nonbranded "TSD_07.05_Leads_Search_Nonbranded_Cooling" 23822363451 is BUILT but PAUSED / $0.
- LSA = the whole new-customer engine: 86 leads, ~$5,338, **~10% booked** (9/86), 60/86 stuck ACTIVE, mix skews **maintenance/tune-up** (24 maint vs 21 repair, 36 uncategorized), 8 message leads. All-time 810/1614 leads WIPED_OUT.
- Branded: 65 "conversions" but **37 are repeat phone calls (existing customers)**, only 15 first-time; search terms 100% pure brand → brand harvesting, not growth.
- Conversion goals POLLUTED: "Local actions – Website visits / Directions / Other engagements" + "Clicks to call" all set PRIMARY → inflates reported conversions.
- Recos: tighten LSA service mix toward repair/install + dispute junk/missed-call leads weekly; reactivate nonbranded search; demote junk primary conversions; speed-to-lead (auto-text + fast callback).

**Meta findings (last 30d)** — 103 campaigns, 97 dead legacy discount promos ($109 tune-up / $139 new-system). Live: "07/01/26 - CBO | Leads" (campaign 120253359511240155, CBO $51/day Highest volume, 1 ad set DCT "Texas Locations", 1 DCT ad, optimized LEAD_GENERATION instant form, Advantage+ audience, DFW 16 cities @25mi with non-DFW TX excluded) = **21 leads @ $64 CPL**. Plus Awareness video ABO ($424, brand, fine). Pixel fires browser-side but **CAPI/server events last fired June 2023** (no offline/CRM feedback loop).
- **Edu correction: the Meta form DOES have pre-qual questions.** So do NOT conclude the form is the problem. HOLD Meta conclusions until we get the **CRM dispositions/outcomes** on the 21 leads (reached/quoted/booked/cold). 21 leads is a small sample.

**Ticket reply that shipped** (TSD client-facing voice per [[tsd-client-facing-voice]]): measured on Meta (form has pre-qual; "Do we have access to CRM dispositions?" before changing anything), clear on Google (LSA service mix + weekly disputes + reactivate high-intent search), framed as "What we can do", speed/auto-text as the biggest Tiffany-side win. Do NOT include the "Meta isn't feeding outcomes back" line in client-facing copy (kept internal only).

**There is NO Performance Max campaign in this account** — never has been. Verified 2026-07-31: the only ENABLED campaigns are the LSA (15789372405, $164.29/day) and the branded Search (23822436393, $50/day); everything else is PAUSED. If a PMax question comes up "for Spencer Air", it is almost certainly [[tsd-zen-air]] (PMax `TSD_03.23_PMAX_HVAC_Calls`) — that mix-up already happened once. Check the account before acting.

**Nonbranded history (checked 2026-09-21)** — `TSD_07.05_Leads_Search_Nonbranded_Cooling` (23822363451) was NOT just "built": it served 2026-05-07 → 2026-05-19 only (13 days, $712.88, 59 clicks, 0 counted conversions), launched same day as Branded (name 07.05 = 7 May). Last serving day 05-19, so paused ~05-19/20, BEFORE Edu started (06-17). Exact date/actor/reason NOT recoverable via API (change_event only holds ~30 days; returned 0 rows) and no Slack/ClickUp record of a pause decision. Search terms were mostly competitor brands + DIY junk (r 10 heat & air, elmers ac, chill brothers dallas, freon DIY). "Failed trial" is an inference from data, not a documented decision. Prior team = Manuel Cabrera (paid), Marissa Young (AM); his 05-22 Slack note says Meta budget moved to Google (client card failing) — no mention of nonbranded. His Media Plan sheet (Drive id 1yXcPF--RJge9zlH35o4Y-3iikIuvO4CKV-eELUEVaLc) is "source of truth" for pacing notes but the Drive connector can't open it. The ClickUp connected here is not TSD's ticket system (Agency Titan not reachable).

**Tracking check 2026-09-25 (live pull, "did we fix tracking in last 30d?" → no evidence of any fix).** Site = spencerairconditioning.com (GoHighLevel, GA4 events imported into Ads as `... - GA4 (web) ghl_*`). All 6 imported GA4 web actions (ghl_request_estimate/contact_us/service_area, phone_link_click, mailto, book_now) = ZERO conversions every month Mar–Sep; "Form Capture" first fired Sept (2), "Submit lead form - Web" never primary (3+2 all-conv May/Jun). Google-hosted Local actions/Clicks to call: not in conversions metric, 0 primary since March (only All-conv, 42 in Mar), so not currently inflating. **Repeat Phone Call (existing customers) is still primary + counted**: Jun 4.1 → Jul 43.1 → Aug 27.8 → Sep 9.0 MTD; that explains the July branded "spike" (22→72). Meta pixel last fired 2026-08-29 and only 4 PageView + 2 Lead in the whole 28d window (all one hour 08-29); server/CAPI last 2023-06-15, still dead. API can't show who changed what: `change_event` returns 0 rows, `change_status` has no conversion_action field, `conversion_action.tag_snapshots` unrecognized; only UI Tools > Change history can. Not yet checked: GTM container / GA4 property / the live site itself.

**Open / next:** get Meta lead outcomes from CRM; then decide Meta changes. Google actions to stage as scripts (writes are Edu's to run): reactivate nonbranded search, demote polluted primary conversions. Consider adding Spencer to contas.yaml + a clients/ folder.

**2026-10-06 Meta weekly (AT task closed, KPI added):** only spend is awareness campaign `Spencer Air | Awareness | ABO | Videos | 30Jun2026` ($40/d ad set), $280/wk, 91.8k reach, freq 1.30, CPM $2.34; lead-gen not spending. Same setup issues as All Seasons: Reach not Ad Recall Lift, freq cap 2/7d, 16 cities × 25 mi + 'recent', ABO not CBO. Second Meta acct 1900919440286623 = $0. Log: clients/spencer-air/meta-ads-log.md.
