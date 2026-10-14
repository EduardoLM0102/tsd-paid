---
name: tsd-activity-log-verification
description: Two mistakes made reading a Meta/Google activity log for a TSD client report — confirm actor identity and check status at the right entity level before writing either into a report
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46b245a7-1645-439f-aa07-bce2601fc21d
  modified: 2026-08-21T18:49:04.607Z
---

When reading a Meta (or Google) Ads activity log to write a client/internal report, two specific
mistakes cost a rebuild on [[tsd-gc-home-service]] (2026-08-21) and are worth avoiding elsewhere:

1. **Don't assume an unfamiliar actor name in the log is an outside/client-side actor.** An
   unrecognized name (e.g. "Jonathan Bannister") was assumed to be someone external who'd touched
   the account without coordination — it was actually TSD's own person, and the change (a new
   Meta campaign launch) should have been the headline of the report, not a flagged anomaly.
   **Why:** Edu corrected this sharply ("how the fuck do we have no further changes on meta if we
   published the new Yeti campaign"). Guessing at actor identity from a name alone, especially
   when it changes how positively or cautiously something gets framed, is a real error.
   **How to apply:** if a name in an activity log doesn't match anyone already known from prior
   session context, ask or flag it as unconfirmed rather than asserting it's external — and don't
   default to the more cautious/negative framing while it's unconfirmed.

2. **A status change on an ad SET is not a status change on the CAMPAIGN.** Read one ad set going
   Active→Inactive and reported "the awareness campaign was paused." In fact the campaign had two
   ad sets; only the older one was retired, and the campaign kept delivering through the other.
   **Why:** the client caught it immediately ("awareness isn't paused... we still have ours") —
   this would have been a false claim in a client-facing report.
   **How to apply:** before characterizing a campaign as changed/paused/stopped from an activity
   log entry, pull the entity itself (or its children) fresh and confirm status at the level
   you're about to describe — ad set-level and campaign-level status are independent facts.
