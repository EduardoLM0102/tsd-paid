---
name: feedback-platform-vocabulary-google-vs-meta
description: "When a TSD client runs both Google and Meta and Edu's request doesn't name a platform, read the vocabulary (Max Conversions, headlines/descriptions = Google) before touching any tool; never default to whichever MCP is loaded"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e32d228a-2d28-4037-8011-46af375f99fc
  modified: 2026-09-26T11:24:08.012Z
---

"Max Conversions" is a Google Ads bidding strategy. On 2026-09-26 Edu asked for Gillespie's: "snapshot the actual ads we have for them on Meta (descriptios, headlines etc) but recreate two new campaigns from scratch using Max Conversions". I anchored on the Meta account because the Meta MCP was what I loaded first, pulled the whole Meta account, wrote a Meta snapshot file, and only then hit a blocker. Edu cut in: "i'm talking about google". The request read "Meta" in the first line, but the bidding term and the two existing Google campaigns (Branded + Non-Branded) were the real signal.

**Why:** Gillespie's has both a Google Ads account (`7410489772`) and a Meta account (`2014320269203822`). Platform-specific words map cleanly: Max Conversions / tCPA / RSA headlines and descriptions / keywords / negatives = Google; CBO / ad set / Advantage+ / DCT / Highest volume / primary text = Meta. When the words and the named platform disagree, that's a conflict to resolve up front, not a tie to break silently.

**How to apply:** Before any tool call on a multi-platform client, map the request's vocabulary to a platform. If a term fits only one platform, work in that one. If the named platform and the vocabulary disagree, or the words fit both, ask one short question instead of building. Related: [[tsd-gillespie-heating-cooling]], [[tsd-verify-meta-account-live]].
