---
name: tsd-verify-meta-account-live
description: "before reporting \"no Meta presence\" for a TSD client, query the Meta Ads MCP directly, don't trust absence of a workspace log file"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 291aa929-006c-49b9-a277-9070515ae330
  modified: 2026-08-21T18:57:01.041Z
---

For any TSD client, absence of a `meta-ads-log.md` (or any Meta mention) in `topserv-workspace/clients/<client>/` does NOT mean the client has no live Meta account. Always call `ads_get_ad_accounts` and `ads_get_ad_entities` directly to check before concluding a channel is unbuilt.

**Why:** Missed a real, active Meta campaign for [[tsd-gillespie-heating-cooling]] (running since July 2026, $1,062 lifetime spend) because I only grepped the workspace's Google Ads/GTM logs, which only covered the Search build. The Meta ad account (`2014320269203822`) is owned by the client's own Meta business, not the Topservdigital business manager, so it never surfaced in any TSD-side doc. Edu had to correct me.

**How to apply:** When asked to check "Google and Meta" (or produce a weekly report spanning channels) for any client, always hit the Meta MCP tools directly for that client's account first, rather than inferring channel scope from what's logged in the workspace. Workspace logs document what TSD's paid team has *touched*, not what exists on-platform. Same caution likely applies to Google Ads accounts owned outside the TSD MCC, though less likely given `contas.yaml` is built from `read.py accounts` against the MCC.
