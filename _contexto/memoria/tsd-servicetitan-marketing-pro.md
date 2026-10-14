---
name: tsd-servicetitan-marketing-pro
description: "TSD ServiceTitan Marketing Pro knowledge + the Mission Accomplished/Brian escalation — full doc lives in the workspace, read it before any ServiceTitan work"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5654f4b3-8e2d-4b44-96cd-c1ebf21bbfbd
  modified: 2026-07-22T01:05:17.722Z
---

The ServiceTitan Marketing Pro thread (mechanics, the Mission Accomplished escalation, the leadership action items, and the Scheduling Pro API research) is written up in full at
`~/Documents/GitHub/topserv-workspace/clients/mission-accomplished/servicetitan-marketing-pro-escalation.md`, with a pointer entry in that folder's `google-ads-log.md`. **Read the doc — don't work from this summary.**

The load-bearing distinction, because it caused the client blowup on 2026-07-07: **Marketing Pro sends GCLID + revenue value via Google's offline conversion upload; it does NOT send hashed identity (Enhanced Conversions).** Ads Optimizer's "daily customer list" is Customer Match (audience enrichment), a third and different thing. Call-extension clicks carry no GCLID at all and fall back to a phone+timestamp proxy match. Goal depth (which conversion action is Primary) and identity matching (Enhanced Conversions) are independent levers — fixing one does not fix the other.

Mission Accomplished (HVAC, owner **Brian C.**) paused spend after that call. Root cause was configuration, not tracking depth: ServiceTitan's Booked Job / Completed Jobs / JVP actions existed but **none were Primary**, so bidding optimized on "unbooked call >60s" and learned to buy spam calls. Client plan (~80% LSA + Meta ad recall lift + branded search) is drafted but **not sent** — do not send it before the conversion config is fixed.

**Updated 2026-07-21 (see §7b of the doc — it supersedes the older "pending" statuses):** ownership is decided (the **Media Buyer** on the account owns ST monitoring, folded into the optimization checklist); the Enhanced Conversions path is **Peach AI**, not the Scheduling Pro API build; EC is deliberately framed as important-but-not-a-blocker, with the conversion-goal fix as the immediate action; reporting moves to **ServiceTitan numbers leading, Google's conversion count below as a platform metric**. The full approved reply to CS (Eve/Mia) is quoted verbatim in §7b.3.

**Conversion config EXECUTED 2026-07-21** (log entry + correction in that folder's `google-ads-log.md`): all 12 campaigns were already paused, and the ST deep actions were **already Primary** (Completed Jobs had 13 conv / $26,790.78 in 2026, not "1 in 8 months" — §3.2 of the doc is stale). Real fix was `campaign_conversion_goal` on the only two campaigns with 30-day impressions (PMax Evergreen HVAC `22319188947`, Search Branded Mix `23731240233`): biddable = BOOK_APPOINTMENT + CONVERTED_LEAD + SUBMIT_LEAD_FORM; **PHONE_CALL_LEAD off** at Edu's call, since "call happened" is exactly the signal that trained bidding toward Brian's spam calls. Leaves only ~6-9 biddable events/month, well under 30-in-30 — honest signal, thin volume, so expect a long learning period at relaunch. Bidding already Maximize Conversions with no tCPA on both; left alone. Still open: the other 10 paused campaigns inherit account-level goals where `DEFAULT / WEBSITE` is still biddable.

**Mechanic worth remembering (now in the skill's `aprendizados.md`):** on the conversion-goals model, `conversion_action.primary_for_goal` is not the lever and mutating it succeeds silently without changing anything; biddability lives in `customer_conversion_goal` / `campaign_conversion_goal`. Also `protobuf_helpers.field_mask` drops `False` values, so boolean-off writes need an explicit `FieldMask(paths=[...])`. **Never report a write as done without reading it back** — that failed twice in one session here.

**Why:** Edu is Head of Paid Ads and the escalation landed on him; the team had no ServiceTitan process and the two-layer confusion is the thing that gets re-litigated every time this comes up.

**How to apply:** when any ServiceTitan/Marketing Pro question arises (this account or the pending audit of other ServiceTitan-connected clients), open the doc first. Never assert Marketing Pro "feeds job quality to Google" without naming which layer. Related: [[topserv-google-ads-location]], [[topserv-client-report-format]], [[tsd-paid-launch-sops]].
