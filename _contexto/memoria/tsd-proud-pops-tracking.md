---
name: tsd-proud-pops-tracking
description: "Proud Pops conversion-tracking diagnosis (acct 1051843378) — what died, what never fired, and why the account-level \"fixes\" are traps"
metadata: 
  node_type: memory
  type: project
  originSessionId: a14912a3-1233-479f-bfd0-59d88fcab22f
  modified: 2026-10-07T14:17:02.491Z
---

Diagnosed 2026-07-23 via Google Ads API on acct 1051843378. Edu said he would fix it site-side
that day, so **re-verify all of this before reusing it.** Companion to [[tsd-proud-pops]].

**What died and when** (last fire date per conversion action):
- `Local actions - *`, `Clicks to call`, `Store visits` — stopped 2026-02-12 → 02-18
- GA4-sourced actions (`phone_link_click`, `book_now_link_click`, `mailto_link_click`) — 03-16/17
- `www.txproblemsolvers.com (web) *` — 03-18 → 03-27
- `Calls from ads` — **2026-05-04** (10 days before the May 14 rebuild; call assets ARE present
  on the TSD campaigns, so this one is unexplained — check call reporting settings)
- Still alive: `instant_quote_hvac_click`, `local_services_phone_lead/message_lead`,
  `Business profile - Call`

**Never fired at all in 2026** — so un-hiding/enabling them does NOTHING until tags actually ship:
`Proud Pops (web) ads_conversion_Form_1` (HIDDEN), `Proud Pops (web) purchase` (HIDDEN),
`TSD - Website Call` (enabled+primary), `Website lead` (enabled+primary).

**TWO TRAPS — I fell into both and had to walk them back:**
1. "Un-hide the HIDDEN Proud Pops actions" achieves nothing — they have zero data, not hidden data.
2. "Recategorize `instant_quote_hvac_click` from PURCHASE to SUBMIT_LEAD_FORM so it counts" would
   **fabricate ~600 leads/quarter**: it fired 987x in 2026 vs ~228 real LSA leads. A 4:1 ratio over
   real leads = button click, not submission. **Always check volume ratio vs known-real leads before
   recategorizing any conversion action.**

**Goal config (current):** 6 biddable goals — CONTACT/WEBSITE, CONTACT/CALL_FROM_ADS, DEFAULT/WEBSITE,
PHONE_CALL_LEAD/WEBSITE, PHONE_CALL_LEAD/CALL_FROM_ADS, SUBMIT_LEAD_FORM/WEBSITE. Clean today.
**Historically it was NOT** — and the junk was in `metrics.conversions` (the bidding signal), not just
reporting: Jan 2026 = 230 of 430 counted conversions were `Local actions - Directions`; Aug 2025 =
1,005 of 1,394 were `button_schedule_online`. So pre-Apr-2026 lead counts and CPLs are inflated.

**Useful GAQL:** `SELECT segments.date, segments.conversion_action_name, metrics.all_conversions,
metrics.conversions FROM customer` — the gap between `all_conversions` and `conversions` is exactly
what is firing but not being counted.

**Why:** the account looks like performance collapsed in Apr 2026 and it did not; and the obvious
account-level repairs either do nothing or manufacture fake leads.

**How to apply:** measurement gaps like this are fixed at the tag/site layer, then verified as
actually receiving hits, and only then enabled in the account. Never make a conversion action
biddable to close a reporting gap without confirming what the event represents.

---

**GTM-LAYER ROOT CAUSE (added 2026-07-23, via the new GTM API access [[tsd-gtm-tag-manager-setup]]).**
GTM account 6255217830, container GTM-WBFDB6L8 (id 198527160), Web|Proud Pops. Default workspace
is id **38** (NOT "1" — listing workspace 1 returns empty and is misleading). Live version v37, 22
tags/14 triggers — container IS fully built; the site fires fine. Conversion ID is CORRECT
(`{{Conversion ID}}`=11164298794, `{{Google Tag}}`=AW-11164298794). The defect was **wrong/dead
conversion labels on the G.Ads tags**:
- `05 | G.Ads - Lead` (awct, fires cEvent-Lead + Appointment Scheduled) sent label
  `S8EPCK-U7oscEMCazMM-` = NOT in AW-11164298794 (legacy label) → form leads counted nothing.
- `03 | G.Ads - Email` (awct) sent label `11164298794` (the ID pasted into the label field) →
  broken. Correct labels: Website lead=`u5lXCI2jk7kYEKrcxssp`, TSD-Email Click=`eFIRCJ7do8gcEKrcxssp`,
  TSD-Website Call=`LPUbCN6nosgcEKrcxssp`. Version history shows v33 "TSD Fix - Initial Tag Setup"
  then v34 "Revert - Remove incorrect Proud Pops tags" — the correct setup was reverted, which is why
  the "Proud Pops (web)" actions sit HIDDEN.
- **PHONE tag gotcha:** `02 | G.Ads - Phone Call` was type **awcc (Google Ads Call Conversion =
  number-swap)**, phoneConversionNumber 210-225-5767, firing on a phone-CLICK trigger. An awcc tag
  NEVER counts on fire/click — it swaps the page number for a Google forwarding number and counts
  only a real call ≥ min duration (60s). GTM Preview showing it "fire" is a FALSE POSITIVE for this
  tag type. Compounded: should fire on All Pages not click; CallRail-All-Pages tag also present (2nd
  number-swap, conflict); target action `TSD - Website Call` is origin CALL_FROM_ADS (+ account
  call-conv action = "Calls from ads", also CALL_FROM_ADS) — neither is fed by the website. Result:
  TSD - Website Call = 0. Edu chose click-based (awct) tracking to match Lead/Email; CallRail keeps
  owning real calls.

**NO NEW ACTION NEEDED (corrected via Edu's screenshot 2026-07-23):** the API's `origin=CALL_FROM_ADS`
on `TSD - Website Call` is MISLEADING — the Google Ads UI shows Source = **"Phone number clicks"**, i.e.
it IS already a click-based phone conversion (label LPUbCN6nosgcEKrcxssp). So the phone fix was NOT a
new conversion action — it was purely the GTM tag TYPE: awcc (call/number-swap, never counts on click)
→ awct (standard click conversion). Trust the Ads UI over the API `origin` enum for phone actions.

**FIX STATE (2026-07-23): PUBLISHED AND VERIFIED LIVE.** Workspace 39 is gone; it shipped as
**live container version 38** "TSD - Fix conversion labels (2026-07-23)" (only workspace 38
"Default Workspace" remains). Verified against the live version via API: Lead = awct label
`u5lXCI2jk7kYEKrcxssp`; Email = awct label `eFIRCJ7do8gcEKrcxssp`; Phone = **awct** (successfully
flipped from awcc) label `LPUbCN6nosgcEKrcxssp`. First signal confirmed: `TSD - Website Call` went
0.3 (Jul 22) → **1.7 counted (Jul 23)**. **`Website lead` had still not registered a first
conversion as of Jul 23 — re-verify; if still zero, check the Lead trigger (ids 80/73) in Preview.**
Note the earlier plan to CREATE a `TSD - Phone Click` action was unnecessary.
GTM writes (workspaces/tags) ARE allowed, **Google Ads mutate writes are NOT** — re-confirmed
2026-07-23, `update.py campaign --status` is denied by the auto-mode classifier. Any Ads change
must go to Edu for UI execution or needs an explicit Bash permission rule.

**STILL UNFIXED as of 2026-09-03 — this is now the account's central problem, not a side note.**
`TSD - Website Call` is still `primary_for_goal=True` / biddable (confirmed live via
`conversion_action` GAQL query). It now dominates reported conversions: 94% of PMax HVAC's, 83% of
PMax Electrical's, 84–88% of both Search Electrical and Search Plumbing's. Real leads (`Website lead`
form fills only) over Aug 4–Sep 2: 143, against ~$41.5k PPC spend = **~$290/real lead**, roughly double
the $137.70 figure that was already flagged as too high on Jul 30. Every August budget-ramp decision
was made partly on this inflated signal. **The fix is finally executable without Edu** — unlike the
GTM-layer work, demoting `primary_for_goal` on a conversion action is a normal
`ConversionActionService.mutate_conversion_actions` call, inside what the skill tooling can do — it
was diagnosed 3x (Jul 23, Aug 10, Aug 19) but never actually flipped. See
[[tsd-proud-pops-sept-oct-plan]] for the full Sept/Oct sequencing built around fixing this first.

**Sept 1-24 check (2026-09-24): STILL UNFIXED, 3 weeks after the plan.** `TSD - Website Call` still primary:
916 of 1,048 reported conversions (87%); Google's reported CPL $45.8 is meaningless. Real form leads
(`Website lead`, all_conversions) 147 vs 117 in Aug 1-24. Lead-gen spend (Search+PMax, excl YouTube + LSA):
$43,076 vs $28,104 = +53% spend, +26% forms, CPA $240 → $293, marginal ~$500 per extra form lead.
Branded $103/form, PMax Electrical $70, Nonbranded Search $507-584. **PMax HVAC form leads: 27 (wk Aug 10)
→ 2 → 0 for 5 straight weeks at constant ~$2.3k/wk spend** (only phone clicks report); Electrical PMax forms
and Search HVAC forms are fine, so site form tag works, cause unknown (tracking vs traffic). `change_event`
only reaches back 30 days so the ~Aug 17 trigger needs the UI change history. 2 YouTube campaigns
(Aug 2026, $100/d each, ~$4.8k MTD) added since; total daily budget caps ~$1,960/d, MTD pace ~$60k vs
$50k Aug approval, no Sept approval on record. GAQL gotcha: segmented `FROM campaign` queries return
`cost_micros` as real micros in a string (divide 1e6); unsegmented insights.py returns it pre-converted.

**2026-10-07 check: Gate 0 STILL not done.** `TSD - Website Call` = PHONE_CALL_LEAD/CALL_FROM_ADS, biddable on every
lead campaign; shares that bucket with `Calls from ads` (0 since May), so turning the bucket off costs no real signal.
**PMax HVAC zero-forms SOLVED: it turned into a Display campaign.** Search share of spend 70% (wk Jul 27) → 31% (Aug 10)
→ 7% (Aug 17) → 0% from Aug 24, ~$2.3k/wk all CONTENT, 0 forms. Lines up with the $27 tCPA set Aug 10: phone-click
signal + cheap Display taps = target met. All PMax forms come from the Search slice. PMax Electrical drifting the same
way (Display 0% → 46% by wk Sep 28, 0 forms from it). Check `segments.ad_network_type` weekly on any PMax here.
Wk Sep 30–Oct 6: $11,674 lead-gen, 47 forms, $248/form; Sept $309/form; Oct pacing ~$59.8k, no Sept/Oct approval.
**⚠ 10-07 BIGGEST FINDING — ~3 in 4 `Website lead` "forms" are JOB APPLICATIONS.** /careers embeds a GHL job form
(widget ThmcYYHImwSoYS9oBt3n) that fires the same ghl_form_submit → G.Ads Lead tag. GA4 google/cpc generate_lead by
pagePath Sep 7–Oct 6: /careers 99 vs customer 32; Aug: 104 vs 28. PMax Electrical 79 of 81 = careers (PMax final URL
expansion OPTED_IN sends traffic straight to /careers); PMax HVAC's Aug "44 forms" = 41 careers. Real cost per customer
form ~$1,115 (30d, $53k spend, ~48 est. customer forms), not $296. **This overrides the "PMax HVAC zero-forms SOLVED" read
above: it lost job applicants, not customers. And Gate 0 must come AFTER the careers GTM exclusion, or PMax chases job
seekers harder.** Aug client report (129 forms/$256 CPL, "1,069 calls") was built on this. **How to apply: before quoting ANY
Proud Pops form CPL, split GA4 generate_lead by pagePath (exclude /careers) until the GTM fix ships and is verified.**

**10-07 GTM facts (was live v41/ws 43; careers fix PUBLISHED as v42 2026-10-07 10:32 CT, ws now 44):** trigger [80] cEvent - Lead (ghl_form_submit) feeds G.Ads Lead [82], GA4 Lead [90],
G.Ads UPD [94], Meta Lead [111]. Fix = Page Path does not contain /careers on [80] (+ dlv ghl_form_id != ThmcYYHImwSoYS9oBt3n).
TWO listeners push ghl_form_submit: [99] (flat keys, feeds the dlv email/phone vars) and [123] (ghl_form_id + nested ghl_data);
don't delete [99] or enhanced conversions break. Meta Lead [111] actually sends PageView. **Gate 0 trap:** TSD - Website Call
shares PHONE_CALL_LEAD/CALL_FROM_ADS with Calls from ads, so set the action Secondary in UI, don't turn the goal off.
Plans: clients/proud-pops/internal-action-plan-2026-10-07.md + am-client-action-plan-2026-10-07.md.
**ACTIVE CHECKLIST: clients/proud-pops/internal-checklist-2026-10.md (Blocks A-G) — start at its "▶ RESUME HERE" section (next steps, decisions D-1..D-6, AM/client tracker P-1..P-12, baselines). Block A LIVE v42 10-07; Block E check = `./tsd.sh proud_pops_verify_careers_fix.py`. Re-read it at the start of any
Proud Pops session, tick + fill results only after a read-back. Block F (phone taps → Secondary, HVAC tCPA off) waits
on GTM fix verified live 3 days + AM heads-up sent.** Negatives: CSMS_Negatives already has job/jobs/career/salary +
george/bearded plumber; CSMS_Competitors (23 plumbing names) is attached to nothing; PMax needs account-level negatives.

**10-08 LSA:** legacy roofing LSA 3477779749 was LIVE (charged $83.52 on Sep 11 for a declined roofing call) → campaign
20805107400 PAUSED; the other 6 legacy PS LSA accounts were already paused. Lead handling (`proud_pops_lsa_lead_handling.py`):
calls answered fine (0 missed in Sept), but messages unanswered, leads left 'active', heavy declines (61/109 in Jun), credits
0 in Sept. The impression collapse is NOT explained by call handling → profile settings (D2).

**Confirmed calls (10-07):** PPC = 0 (call asset 794-7570 still DISAPPROVED, phone_calls 0). **LSA collapsed**, 3 surfaces
combined: calls Jun 88 → Jul 71 → Aug 33 → Sep 21 → Oct 1-6 2; spend $6.8k → $0.9k. Campaigns ENABLED/ELIGIBLE, no
change events → cause is in the LSA dashboard, not Ads. Recipe: `local_services_lead` (filter on creation_date_time)
+ LOCAL_SERVICES campaign cost, run on each of 1051843378 / 7261668241 / 6621969129 and summed.

**Update 2026-09-25 (First Repair banner check):** live GTM version is now **v41** (23 tags/14 triggers) and the
Default Workspace id is now **43** (38 is gone, so listing it returns empty). Site is a React SPA behind GTM-WBFDB6L8 + GA4
G-C7QTE9ZZXQ, Consent Mode v2 defaults DENIED (GA4 undercounts non-consenting visitors; hits show gcs=G100 vs G111 after Accept).
SPA route changes already send a GA4 page_view with the correct dl/dr. Homepage-only banner "Received our First Repair Is on Pops
letter? / View your offer" links to `/first-repair` (only homepage link to it); no GTM trigger matches `/first-repair` yet, so no
dedicated click event exists. Measure via /first-repair page_view with referrer = homepage, or add linkClick trigger + GA4 event tag.

**2026-10-14 status check (log entry 10-14 in clients/proud-pops/google-ads-log.md):** every 10-08 ad, the 14 G2 RSAs, AG4 RSA and the
unlinked 225-5767 call asset are APPROVED; G2b + H7a cutovers validated, not run. Careers fix holds in Ads (PMax Elec 0 forms); one
GA4-only /careers `generate_lead` leak 10-12. **Block F still not started:** 97% of counted conversions are phone taps (321 in Oct 8–14,
1,312 in 30d, ~83–90% Display/YouTube; GA4 sees ~⅓ of them; 0 calls). Real customer forms ≈ 11/wk, ~$1,090 each; only Search
Electrical is under ~$500. Search HVAC ran 2× cap on weekdays after the 10-08 geo widening, 0 forms; Plumbing on Max Clicks: CPC
halved, 0 conv in 6 days. Branded `Website lead` still not biddable. Meta Lead now arrives (~2× GA4, likely double fire).
Call extension follow-up = Command Center fu-052.

**10-16 campaign check (Oct 1–15, read-only, same recipe as Hawkins/All Seasons):** unlike those two, Search traffic is mostly clean: ~80% of $10.1k visible search-term spend = real service searches, brand 9%, competitors only 6% (Elmer AC, Above All Air, Gillette, Sigma Air, Service Experts, Wattsmith, 'goodman phone number' $176), off-service 2%, 'plumer' $172 for 1 click. Real problems: (1) 617 of 666 counted conversions (93%) = `TSD - Website Call` taps, 0 tracked calls, so Max Conversions chases taps (PMax HVAC 99% Display, PMax Elec ~86% Display+YouTube); (2) Search CPCs very high: HVAC $45.68 avg ('ac repair near me' $393/2 clicks), Electrical $28.95, Plumbing $26.07, IS 26–33%; (3) customer forms per campaign: HVAC Search 3 on $5,985 (~$2k), PMax HVAC 2 on $4,152, Plumbing 3 on $2,242, Electrical Search 17 on $8,483 (~$500), PMax Elec 23 on $2,901, Branded 4 on $1,271; ~52 forms on ~$25k lead-gen; (4) AI_MAX-matched terms ran on Electrical Search through 10-08 ($3,622 Sep 15–Oct 8, bought plumbing/junk), none after; setting now reads off. No Proud Pops company in any CallRail account our key sees (site's CallRail tag belongs to another account), so no call transcripts possible. Most campaigns paused 10-15 (client cut); YouTube x2 still enabled ($3k in-window, fu-046). Nothing changed.
**10-16 APPLIED (Edu's go):** 40 PHRASE negatives into the account-level list 'TSD - Account negatives (job seekers)' 12263521315 (now 66 terms; competitors incl. the 26 CSMS_Competitors + goodman phone / appliance repair / roofing / error code / how to / diy). NOT: 'phone number' (blocks Branded), stove/oven/washer/dryer/refrigerator (block electrician jobs). Client is getting CallRail (Edu 10-16) → then import calls ≥60s + taps secondary. Recommended for Nov 1 (fu-053): PMax HVAC stays off until clean signal; URL expansion OFF on all PMax; HVAC LP + RSA rewrite. Log: clients/proud-pops/google-ads-log.md 10-16.
