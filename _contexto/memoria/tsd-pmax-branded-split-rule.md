---
name: tsd-pmax-branded-split-rule
description: Performance Max campaigns always classify as unbranded when splitting conversions/CPL by branded vs unbranded
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c91aab69-87d2-4297-af22-a30096a254aa
  modified: 2026-09-15T09:05:48.308Z
---

When splitting a TSD account's conversions/spend into branded vs. unbranded buckets (per [[tsd-weekly-ppc-snapshot]]), Performance Max campaigns always go in the **unbranded** bucket — never a separate third category, never left out of the total.

**Why:** Edu's explicit rule (2026-09-15, On The Way snapshot). PMax isn't a Search campaign so it has no brand/nonbrand-named ad groups to key off of, but it still needs a bucket — unbranded is the default.

**How to apply:** Total conversions/spend = Branded (named Branded Search campaign) + Unbranded (named NonBranded Search campaign + any PMax campaigns, summed together). Note: Google doesn't report `search_impression_share` for PMax, so Impression Share stays Search-only (Branded IS, NonBranded IS, combined Search IS) — there's no "unbranded IS" to extend PMax into.
