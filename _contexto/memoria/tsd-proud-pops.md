---
name: tsd-proud-pops
description: "Proud Pops (ex-The Problem Solvers, merged w/ My Favorite Service Company, San Antonio TX) — account map, the Mar 2026 tracking break, and the budget answer for Jonathan"
metadata: 
  node_type: memory
  type: project
  originSessionId: a14912a3-1233-479f-bfd0-59d88fcab22f
  modified: 2026-10-08T20:06:40.240Z
---

TSD client, San Antonio TX. Full analysis + chart in `topserv-workspace/clients/proud-pops/`
(`budget-analysis-2025-2026.md` + `spend-chart.png`). All accounts now registered in
`contas.yaml` — see [[topserv-google-ads-location]].

Key facts established 2026-07-23 (Google Ads API, MCC Topservdigital 4155514468):

- **PPC account 1051843378 was RENAMED, not replaced.** Problem Solvers history and Proud Pops
  history are the same account, unbroken since Jan 2025. There is no separate old PPC account
  whose budget was cut.
- **BASIS MATTERS: the client cluster is 11 accounts** (Proud Pops PPC + 2 LSA + 7 legacy PS LSA
  + canceled 9776908250). My Favorite Service Company's 3 accounts are a SEPARATE set — report
  them separately, don't blend.
- **Answer to Jonathan is two-sided and both halves must be said.** vs the same 6 months a year
  ago spend is UP 27.8% ($90,002 → $115,033); but vs H2-2025 the run rate is DOWN 41%
  ($20,468/mo → $12,174 in Jun 2026), and down 48% from the Mar-2026 peak of $23,576.
  Jonathan is remembering autumn 2025 and on that framing he is RIGHT. Spend ramped all through
  2025, peaked Q1-2026, fell at the 2026-05-14 rebuild. Leading with only "+27.8%, you're wrong"
  loses the room.
- **THE BIG ONE — tracking is broken.** All `www.txproblemsolvers.com` web tags died
  2026-03-16→03-27 at the rebrand cutover. Replacement `Proud Pops (web)` actions exist but are
  **HIDDEN**. `TSD - Website Call` is primary but records nothing. All 8 TSD_ campaigns
  ($8,534) have zero conversions. Any CPL crossing March 2026 is meaningless.
- Conversion goals are polluted on both PPC accounts (Local actions, Store visits, GA "Shop";
  MFSC counts raw `page_view` as primary). Pre-Apr-2026 lead counts are inflated.
- **Google rep deck is contradicted:** it claims "not budget limited"; the account lost 23–59%
  of Search IS to budget in 17 of 18 months. BUT that budget-limited story is HISTORY (pre-rebuild).
  Post the 2026-05-14 rebuild the bottleneck FLIPPED to Ad Rank and stayed there: budget-lost fell
  to single digits while rank-lost climbed to ~78% (Jun AND Jul 2026). See [[tsd-proud-pops-impression-share]]
  — adding budget now buys almost nothing; the lever is Quality Score.
- `9776908250 [Old Account] The Problem Solvers (no LSA connected)` is CANCELED and unreadable via
  API (CUSTOMER_NOT_ENABLED). **Already checked — Edu confirmed in the UI it spent $0 across 2025.**
  It is a shell; don't re-flag it as a gap.
- People: Jonathan Bannister (TSD, client-facing), Justin Pearce (TSD, did the June optimization
  week), Jacob (owner of My Favorite Service Company, merged in), Andrea (TSD, made the Jul 7 budget
  cut), Brandon (brandon@proudpops.com, client-side; enabled AI Max himself), Eve (TSD, asked to
  confirm what was agreed in prior meetings got done).

**2026-10-08 CPC check (colleague thought CPC "$6-7, too low"):** 30d Sep 8–Oct 7 nonbranded Search CPC Electrical $24.53 / HVAC $36.45 / Plumbing $37.40, Branded $10.43, single clicks up to $172. That's in market: Keyword Planner San Antonio DMA (200641) top-of-page low–high ac repair san antonio $55–154, plumber san antonio $37–120, electrician near me $13–75. The blended number looks low only because PMax buys 24,697 clicks at $0.68 (PMax HVAC 99% of spend on Display). Two YouTube video campaigns spent ~$6k in 30d with 0 conv.

**Post-June-29 account changes (found 2026-07-23 via change_event history):**
- **Jul 7 budget CUT by andrea@topservdigital.com** — PMax HVAC $130→$80/day, Nonbranded Electrical
  $108→$50, Nonbranded Plumbing $90→$60, PMax Electrical $80→$60. Total PPC $409→$250/day. This was
  AFTER the meeting called to RAISE budget — flag/confirm it was client-requested.
- **Jun 26 (3 days pre-call) brandon@proudpops.com enabled AI Max + text asset automation + final URL
  expansion** on TSD_05.20_Leads_Search_Nonbranded_Electrical — still ON. This is exactly the Google-rep
  AI Max upsell Justin flagged; the client acted on it directly in-account.
- Justin's Jun 26 optimization confirmed: 110 criterion changes across the 3 accounts (access@topservdigital.com).
- **Current spend ~$15k/mo** (July MTD $10,855 for 1-22, pacing $15,300). Below the GOOD bracket.

**Four commitments (2 meetings) + status:** (1) historical spend pull = DONE (budget-analysis doc);
(2) Google deck LSA-to-PPC doesn't matter = DONE (backed Justin on the call); (3) good/better/best
budget brackets + AC service-vs-install strategy + past-PPC review = DONE (budget-brackets doc);
(4) water-treatment/softener keyword research = DONE (same doc). See [[tsd-proud-pops-deliverables]].

**Why:** the account looks like it collapsed in April 2026 and it did not — anyone reading the
raw numbers without the tracking context will reach the wrong conclusion and recommend the
wrong thing.

**How to apply:** always give the run-rate table (H1-25 $15,000/mo, H2-25 $20,468/mo, Q1-26
$22,215/mo, Q2-26 $16,130/mo) — it reconciles both answers. Recommendation is $22-24k/mo gated
on fixing tracking. Watch the UI date picker: "2025" ending Jan 1/26 is inclusive and shows
$188,706.61 for the PPC acct vs $187,625.23 on calendar months (the $1,081.37 is Jan 1 2026).
Before quoting any Proud Pops CPL or lead count, check whether the window crosses March 2026. Use LSA leads + call-extension calls ("Google-side leads") as the only
lead series comparable end to end. Fix tracking before recommending any budget increase.
