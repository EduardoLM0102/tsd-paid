---
name: tsd-golden-plumbing
description: "TSD client Golden Plumbing — Google Ads acct 4193142570, LSA lives in the SAME account, PPC paused 2026-07-17, ROI unmeasurable because site conversions died 2026-04-01 and ServiceTitan booked-job never fired"
metadata: 
  node_type: memory
  type: project
  originSessionId: dade687a-c4bf-42dd-ad47-7ddbb6c69b32
  modified: 2026-07-21T18:10:14.679Z
---

Golden Plumbing (TopServ Digital, plumbing). Google Ads customer_id **4193142570**, MCC Topservdigital 4155514468.

**LSA is inside the same account** (campaign `21051260085`, LOCAL_SERVICES, ~$500-750/day) — not a separate customer ID like most TSD clients. Easy to miss when someone says "pause all ad spend."

2026-07-21 ticket: client asked to pause all PPC and wanted an ROI report claiming negative return.
- All PPC was **already paused**; last PPC spend 2026-07-17. **Edu's call: do NOT pause LSA, report covers PPC only.**
- PPC TSD-managed era (Dec 15 2025 – Jul 17 2026): $19,247.85 / 5,503 clicks / 731 recorded leads / $26.34 CPL. Split: Phase 1 Dec–Mar $8,545 @ $13.67 CPL, Phase 2 Apr–Jul $10,703 @ $101.05 CPL.

**Two root causes that matter more than the numbers:**
1. Every website conversion tag went to zero on **2026-04-01** and stayed there (only "Calls from ads" + "Submit lead form - Web" still record). Those tags were 81% of recorded leads (507/625) in Phase 1 — so the $101 Phase 2 CPL is cost-per-*recorded*-lead, not real CPL, and Smart Bidding was optimizing on a dead signal.
2. `ServiceTitan – Booked Job` conversion action exists but has **never recorded a single conversion**, and is set non-primary. No conversion value anywhere. **ROI is not computable from Google Ads** — don't fabricate one; it needs a ServiceTitan revenue-by-source export. Same shape as [[tsd-servicetitan-marketing-pro]].

Also: site conversion tags are named "**Gardner's Plumbing** (web)" not Golden Plumbing — confirm the brand with the AM.

Deliverables in `topserv-workspace/clients/golden-plumbing/`: honest internal `README.md` + 2-page client PDF (navy/gold, per [[topserv-client-report-format]]). Note this report **deliberately breaks** the usual "never signal anything was wrong" rule — see that memory for the tension.

**2026-10-08 (Edu): Golden Plumbing is ON FREEZE.** Not offboarded, but no active management. Don't count it as an unchecked account or add it to the weekly 7-day tasks. Its LSA spent $2.2k / 21 leads in the last 30 days but $0 in the last 7 (as of 10-08). The client (thomas@gardnersplumbing.com) made ~180 edits on 09-10 and 2 asset creates on 09-17 themselves.
