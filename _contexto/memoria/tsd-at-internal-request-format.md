---
name: tsd-at-internal-request-format
description: "How Edu wants AM update tasks in Agency Titan: Internal Request draft, no client name in title, no greeting, Department = Account Management/Customer Success; API recipe + the stage-department gap"
metadata:
  type: feedback
---

When Edu asks for "a ticket/task for Angela" (or another AM) to keep them updated, create an **Agency Titan Internal Request as a DRAFT** (left in Intake; Edu reviews and clicks Submit Request himself).

Rules Edu set on 2026-11-04 (said "remember"):
- **Title without the client's name** (the task is already linked to the client), e.g. "Google Ads update: branded campaign and call tracking". He also stripped client names from the titles he submitted that day.
- **No "Hi Angela"** or other greeting. Start straight with the update ("Update on X's Google Ads. Total budget is unchanged.").
- **Department Assigned = "Account Management/Customer Success"** (id 5c5a5b65-722a-4799-864d-53c433e97f81).
- FYI only unless he asks for asks: on Napps he had the 2 asks removed. On Nick's he also cut the LSA bullet before submitting. Keep it short: what changed, the numbers, next check date.

**Why:** these tasks go to the AM's queue; the client is already on the record, and Edu edits out filler before submitting.

**How to apply (AT MCP):** `agencytitan_start` → `tasks_create` with process_definition_id c3d1c482-ae6a-47c5-b0e2-3efc5a9fd128 (Internal Request), `name` = title, `client_id`, `department_id` = Customer Success, `assigned_to` = AM, field_values {5093804f-e706-40b0-a1ad-4a2ffa3f0336 (requester) = Edu b86625af-f9dc-414c-ac3c-e9a9586e9d1e, 28ef66cf-4abd-428d-b526-c5f8128e8e41 (request_details) = HTML}. Then `task_stages_list` + `task_stages_manage assign`: Intake = Edu, Execution = AM (Angela b8924b58-f336-43e0-b0a9-1a0dc0d1543b), Review & Close = Edu. ⚠ `department_id` on tasks_create did NOT stick (2026-11-04); set it after with `update_process_instance` field_values {department_id}. ⚠ The intake form's required "Set Assigned Department" is the **Execution stage's** department (stage_department_id); no MCP tool can set a stage department, so Edu picks it in the UI when he submits. Check the client's AM with `find_clients` (assigned_to): Angela owns Napps, ICS, Nick's, Spencer.

**2026-11-09 update:** the AT MCP pack now names the tools `data_tasks_create`, `list_task_stages` and `data_task_stages_manage` (`update_process_instance` unchanged). Same recipe and field ids worked as is (C&S Air draft 9d3573c2). Angela also owns C&S Air. Budget figure for a note to the AM: read the client's `ads_budget_marketing` in `find_clients`, don't quote a sum of daily caps as "approved".

Related: [[tsd-client-message-style]], [[tsd-agency-titan-weekly-tasks]].

**2026-11-10 (browser fallback):** when the AT connector is down/unauthorized, create the draft through Claude in Chrome (AT is signed in on Browser 1): top bar + → Add Task → Process Type "Internal Request" → Client → Request Title → Create Task. Intake opens in a side panel: Requester dropdown, Request Details is a Jodit editor inside an iframe (insert HTML via the iframe document's execCommand('insertHTML'), then one real keystroke so it saves; a typed space + Backspace ate a letter once, use "x" + Backspace), and "Who Should Handle" at the bottom DOES let you set the Execution department + Assign to User in the UI. Never click Submit Request. First one: Mission Accomplished 3de43e31.
