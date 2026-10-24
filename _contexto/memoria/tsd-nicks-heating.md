---
name: tsd-nicks-heating
description: Nick's Heating & Air (Hammond LA) TSD client, Google 1854100356 with LSA inside; first-ever check 2026-10-08 found Nonbranded AC leaking ($1,257/1 conv), no negatives, no site tracking
metadata:
  type: project
---

Nick's Heating and Air Conditioning, Hammond LA. Google Ads `1854100356` (LSA inside the same account), AT client `0400fd40-cff2-46eb-ab46-c9befc4f7c7a`. Active per [[tsd-client-accounts-audit-sheet]]. Log: `topserv-workspace/clients/nicks-heating/google-ads-log.md` (read it first).

**2026-10-08 first check (read-only, nothing changed):** nobody had checked it before (no folder, no AT 7-day task, 0 changes in 30d). Nonbranded AC $1,257 / 1 conv in 30d, 68% of it on the PHRASE keyword "air conditioner repair Louisiana", Max Conv with no signal, CPC up to $46. Zero negatives in the whole account. Branded campaign holds a BROAD non-brand keyword "hvac contractors near me" (4 of 7 "branded" conv); brand keywords themselves sit at 98–100% IS. No website call tracking, web form fired once in 30d, no GA access. LSA is the best channel (~$93 CPL, ~22 leads/mo) but runs Mon–Fri 7–16 only. API shows LSA insurance PASSED, but the audit sheet says the COI expired 08-05. Recommendations are in the log, waiting on Edu.

**2026-10-08 lead-quality check:** the leads are real. Calls from ads: all 18 counted calls (≥60s) were 1–7 min from local area codes (985/504/225). LSA: 14 of 18 charged leads with an outcome were BOOKED. Lead forms: real names with Northshore ZIPs. The web form tag works at low volume (1–7/mo); the gap is no website call tracking. Lead-handling issues for the AM: 3 missed ad calls in business hours, an LSA message unmarked since 09-14, 3 charged DECLINED leads to review for dispute.

**Next:** Edu works the account 2026-10-09. Checklist is in `topserv-workspace/tarefas.md` under "Nick's Heating — TRABALHAR 2026-10-09". Book-wide context: `paid/relatorios/google-ads-cadence-audit-2026-10-08/README.md`.

**2026-10-18 GA4/GTM:** GTM-5RH7XW36 (acct 6294341662) live v8 sends GA4 G-GKLMFEE54S. Real form submit = `generate_lead`: GHL listener (origin link.leadnurturemachine.com, matches the site's form iframes) pushes `form_submitted` → GA4 generate_lead + Ads Lead + Meta Lead. `contact_us` is NOT sent by GTM or the page source, so it's likely a GA4-side "create event" rule (probably /contact-us/ page views); confirm in GA4 Admin > Events before trusting it. Edu has no GA4 API access to property 385318676.
