---
name: tsd-ai-max-auto-apply-off
description: "TSD rule (Edu 2026-10-16): AI Max OFF and auto-apply recommendations PAUSED on every current client account; how to do it via API and what only the UI can do"
metadata:
  type: feedback
---

Edu, 2026-10-16: "deactivate AI Max in GENERAL and any autoapply shit we have." Applied to all current clients the same day (log: `paid/guardrails/log.md`, script `paid/guardrails/ai_max_auto_apply_off_1016.py`): AI Max off on 67 Search campaigns (7 live), 7 auto-apply subscriptions paused.

**Why:** AI Max and auto-apply keep buying junk without anyone noticing: Proud Pops Electrical AI Max matches cost $3,622 in 3 weeks (plumbing + "goodman phone number"); All Seasons auto-apply added 156 broad keywords overnight on 10-11.

**How to apply:**
- New campaigns: never launch with AI Max on; turn off auto-apply when onboarding an account. Re-run the script without `--apply` in weekly passes; it lists anything that came back ON.
- API mechanics: `campaign.ai_max_setting.enable_ai_max = False` fails with `AI_MAX_MUST_BE_ENABLED` unless the same op also sets `asset_automation_settings` TEXT_ASSET_AUTOMATION and FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION to OPTED_OUT (mask both). `campaign.ai_max_setting` can't be SELECTed as a whole; select `.enable_ai_max`. Auto-apply = `recommendation_subscription` (status → PAUSED). Type UNKNOWN subscriptions can't be changed via the API: UI only (13 left 10-16: All Seasons 7, ICS 4, ICS Bellevue 1, Napps 1). 10-21: Edu cleared them in the UI. Napps 9509605037 still shows 1 UNKNOWN ENABLED in the API (created 2024-04-24, never modified), but the UI says 0 types on: it's a retired type with no toggle, so IGNORE it when the audit flags it.
- Left out on purpose: All Heart, Strickland, DFW _Unsuspended, Gray Duct, Bucksworth HVAC + Weed are OFFBOARDED (Edu 10-16), nothing needed there.

Related: [[tsd-all-seasons-ac]], [[tsd-proud-pops-tracking]].
