---
name: tsd-lsa-no-disputes
description: "LSA has no dispute flow anymore: rating a lead bad is the only route, Google refunds or not; if a rated lead has no credit, it's closed"
metadata:
  type: feedback
---

Google Local Services no longer has disputes. The only route is rating the lead (bad / not a valid lead); Google then auto-credits it or doesn't. A lead can be rated once ("Rating submitted" in the UI, no further option). If the rating is in and `local_services_lead.credit_details.credit_state` is not CREDITED/PENDING, it's final: nothing more to do. No support chats, no re-rating attempts.

**Why:** Edu, 2026-11-12, after a Cowork "dispute" run on Mission Accomplished found both leads already rated with no credit (fu-140 closed).

**How to apply:** never write "file a dispute" in follow-ups, AM notes or call-wins logs. Say "rate it bad in the LSA inbox (credit is Google's call)". The useful ask goes to the office/AM: rate non-leads promptly with the right reason. Check outcome via credit_state (UNSPECIFIED = no credit). Related: [[tsd-portal-lsa-handoff]].
