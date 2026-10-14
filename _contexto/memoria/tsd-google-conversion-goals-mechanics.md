---
name: tsd-google-conversion-goals-mechanics
description: "How Google Ads conversion GOALS actually work when retargeting bidding (biddable vs primary_for_goal, the Conversions-column reporting artifact, call-duration thresholds)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 10ac7dae-7a18-48b0-b4b9-a0a220dea0d0
  modified: 2026-07-31T14:52:44.360Z
---

Mechanics learned rebuilding GC Home Service's bid targets (2026-07-28, verified 07-31). Applies to
any TSD account on the conversion-**goals** model, which is most of them.

**Biddability lives in `campaign_conversion_goal.biddable`, at the category/origin level.**
Mutating `conversion_action.primary_for_goal` **succeeds silently and does nothing**. Writing
`False` needs an explicit `FieldMask(paths=["biddable"])` because the field_mask helper drops falsy
values. Verify every write with a read-back.

**The reporting artifact that will make you think an account died.** Turning a goal non-biddable
also drops it out of the **Conversions** column; it still reports under **All Conversions**. GC read
`counted=0 / all=1` for the days after the change. **Use `metrics.all_conversions` for any
week-over-week comparison that spans a goal change**, and warn whoever reads the UI.

**Read the call-duration threshold before calling anything a "click."** `conversion_action.
phone_call_duration_seconds` is the real qualifier. On GC:
- `Calls from ads` (PHONE_CALL_LEAD / CALL_FROM_ADS) = **15s connected call**, not a button tap.
- `First Time` / `Repeat Phone Call` (DEFAULT / WEBSITE) = **60s**.
- A `tel:` link tap is its own action and usually low volume.

An audit that labels a duration-thresholded call action a "call-extension click" is wrong, and the
client can see it in their own account. I made exactly that mistake and it reached a client draft.
See [[tsd-client-message-style]] on not asserting inferences as fact.

**Goals can't split actions inside one category/origin bucket.** First Time and Repeat Phone Call
share DEFAULT/WEBSITE, so you take both or neither. Splitting means recategorizing one action into
its own lead category.

**Count the signal you're leaving behind.** GC's biddable volume went 31 → 21 events/90d, which put
both campaigns back into learning on thin data. Check the 90d firing count of what you're turning
on before turning off what's feeding the algorithm today.

Related: [[tsd-gc-home-service]], [[tsd-proud-pops-tracking]], [[tsd-servicetitan-marketing-pro]]
(the offline-import play that's the real fix once tracking is honest).
