---
name: tsd-agency-titan-change-history
description: What the AT MCP can and can't show about who changed a client profile field and when (tested 2026-10-12 on Zen Air)
metadata:
  type: reference
---

Tested 2026-10-12 on Zen Air (client id 9f71ee73-c77b-4842-a7d9-ccdeebcf34a8) when Edu asked if AT logs show when a client profile was modified.

- `data_field_history_list` (REST GET /v1/field-history) works only on an allowlist of built-in fields. `status` worked (returned INSERT 2026-02-13 by Jonathan B.). Custom fields are rejected "Unsupported field path": tried `target_cities`, `icp_target_cities`, `field_values.*`, `custom_fields.*`.
- Target Cities' real key is `icp_target_cities` (label "ICP - Target Cities", simple_list); `target_cities` is the alias find_clients shows.
- `data_activity_list` (REST GET /v1/activity, full client audit feed with old_data/new_data) exists but returned **internal error** on every call, even unfiltered. Not exposed via agencytitan_call_api (must add via request_additional_tools). Retry later; if still broken it's an AT bug to report.
- Fallback: find_clients returns the client record `updated_at` (any field, not per field). Zen Air = 2026-09-22 02:03 UTC.
- The AT web UI may have its own history view; not checked.

Related: [[tsd-agency-titan-weekly-tasks]], [[tsd-zen-air]].
