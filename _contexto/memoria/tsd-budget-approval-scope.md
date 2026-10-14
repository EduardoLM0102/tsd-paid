---
name: tsd-budget-approval-scope
description: "TSD's budget-change approval rule only gates the total account figure, not reallocation among campaigns at a constant total"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5a343a4f-4edd-4011-889f-7acc7d9b1ed7
  modified: 2026-08-31T12:14:20.078Z
---

TopServ's doctrine ("budget change needs written client approval via AM ticket," in `topserv-workspace/CLAUDE.md`) only applies when the **total account budget figure** is changing. Reallocating dollars between campaigns while the account total stays fixed does NOT need that approval — Edu can execute it directly.

**Why:** Edu corrected this 2026-08-31 while reallocating All Seasons AC campaign budgets ($196/day total, unchanged) — see `clients/all-seasons-ac/google-ads-log.md` 2026-08-31 (3) entry for the worked example (donor: Mitsubishi-Brand, recipients: Nonbranded Evergreen + MiniSplit-General).

**How to apply:** Before asking for approval on a TSD budget mutation, check whether the account's total daily/monthly spend is actually changing. If it's a pure reallocation (some campaigns down, others up, net zero), proceed without gating on a ticket. Only pause for approval when the account-level total itself moves up or down.

**A client-approved media plan counts as written budget approval.** When Edu sends a Media Approval (the media plan with a monthly $ total) and the client approves it, setting budgets up to that total is approved. It doesn't need a separate ticket. Corrected 2026-09-30 after On The Way's 09-09 raise was wrongly called unapproved, only because the approval wasn't in the repo. See [[tsd-on-the-way-client]]. **How to apply:** before calling a budget change unapproved, ask Edu whether a media plan or Media Approval covering that total was signed off. The repo logs don't always record approvals. A missing approval in the logs means "not on file," never "not approved."
