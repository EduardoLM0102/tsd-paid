---
name: tsd-portal-lsa-handoff
description: "2026-11-11 LSA tools handoff .md sent to Alex for the TopServ Portal LSA agent (pull, recordings, local transcription, rating rules); 14 flagged bugs; write-back + PII-in-cloud are open decisions"
metadata:
  type: project
---

**2026-11-11: LSA tooling handed to Alex Castro** so he can build LSA lead handling into the TopServ Portal (agent that listens to each LSA call, names the caller + reason, books or archives, rates/disputes, at least daily, ~32 clients). Origin: 2026-11-10 Client Status meeting. Angela raised that "Justin's uncle" bills hours for LSA updates (Watt's Right, King's, Neon Monkey, Spencer) and does not do them. Alex offered the portal agent, and Edu promised to send his LSA tools.

- **File:** `paid/handoffs/lsa-tools-handoff-2026-11-11.md` (~73 KB, local only, NOT committed/pushed, per Edu). Sent as a file in Edu↔Alex Slack DM (D0BNRQZRZNJ, file F0CGHCZTREK) on 2026-11-11.
- **Format Alex asked for:** handoff for another coding agent, scripts verbatim, no summarizing/fixing, bugs marked not solved, no keys, client names OK. Contents: call-wins SKILL.md + pull_lsa.py / pull_calls.py / transcribe.py, google-ads-ratos lib/__init__.py, tsd.sh, lsa_report.py, lsa_health_check.py, proud_pops_lsa_lead_handling.py, account map, LSA API gotchas, PMax-migration notes ([[tsd-lsa-ppl-pmax-migration]]).
- **14 flags in section 6.** Top ones:
  - lsa_health_check `TODAY = date(2026, 8, 27)` is hardcoded.
  - Both LSA_ACCOUNTS lists are stale. They miss Napps / Spencer / King's / Morrow / Concrete and still include offboarded clients.
  - The health check filters on LOCAL_SERVICES, so migrated accounts falsely show "paused".
  - transcripts.json is keyed `lsa_<conversation id>`, not the lead id.
  - `run_query` calls sys.exit on any error.
- **Open decisions, not code (owner Jonathan/Ryan):**
  1. Team rule says recordings and transcripts stay local (PII). A portal that sends them to a cloud model breaks that rule.
  2. No write-back exists. Nothing marks booked, archives or disputes. `ProvideLeadFeedback` / `AppendLeadConversation` are listed as UNVERIFIED pointers only.
- **Angela's condition:** test on a smaller client before Watt's Right (LSA ≈ 40% of Watt's Right revenue, ~$12M/yr).

**Why:** the portal LSA agent is the fix for unowned daily LSA lead handling. This file records what Alex already has, so it doesn't get re-sent or contradicted.

**How to apply:** if Alex or the portal asks about LSA tools, point him to this handoff. If any of the 14 flagged scripts gets fixed, tell Alex, because his copy is a snapshot. The rating step is still Claude following [[tsd-call-wins-log-process]], not code.
