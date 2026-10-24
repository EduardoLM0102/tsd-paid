---
name: tsd-callrail-api-access
description: "TSD CallRail API access set up 2026-10-09 — key in topserv-workspace/.env.callrail, helper callrail.py, agency account covers 122 client companies"
metadata:
  node_type: memory
  type: reference
  originSessionId: 95bf6dc3-049a-423a-9094-ea958ab31f81
  modified: 2026-10-09T13:47:01.458Z
---

CallRail API v3, read-only use. Set up 2026-10-09 (Edu created the key via Claude in Chrome).

- Key + account in `~/Documents/GitHub/topserv-workspace/.env.callrail` (gitignored, chmod 600): `CALLRAIL_API_KEY`, `CALLRAIL_ACCOUNT_ID=792265907` ("TopServ Digital Clients").
- Helper: `topserv-workspace/.claude/skills/google-ads-ratos/scripts/callrail.py` → `get(path, **params)`, `get_all(path, key, **params)`. Run plain `python3`, not via tsd.sh.
- **Covers 122 companies** (TSD's whole agency CallRail): incl. C&S Air (580688522), Napps, Spencer, Integrate Comfort, many others. Use it for Proud Pops / ICS CallRail checks too.
- The key carries Edu's full CallRail rights. GET only, never write.
- Only 14 of the 122 companies are active. 10-09: all 10 GBP integrations sit on TSD's OLD login thecsms@gmail.com ("Cornerstone Marketing Solutions" = TSD's former name), 9 failed + 1 pending; of 7 Google Ads integrations only C&S's failed. Reconnecting needs Google OAuth in the CallRail UI (Edu via Claude in Chrome), not the API. TSD's current shared Google account for integrations = **access@topservdigital.com** (Edu, 10-09); it needs MCC 4155514468 access + manager on each client GBP.
- Useful endpoints: `/companies.json`, `/integrations.json?company_id=` (Google Ads / GA4 / GBP integration `state`), `/trackers.json?company_id=`, `/calls.json?company_id=&start_date=&fields=source,source_name,gclid,first_call,duration,answered,landing_page_url,utm_source,utm_medium`.
- Read pattern: a Google Ads integration in state `failed` = why CallRail conversion actions (`First Time Phone Call` / `Repeat Phone Call`, type UPLOAD_CLICKS) sit at 0. But also count calls with gclid: no gclid calls = nothing to upload even when it works.

Related: [[tsd-cs-air]], [[tsd-proud-pops-tracking]], [[tsd-integrate-comfort]].

**10-09 reconnect session (Edu via browser):** C&S Google Ads + GBP → active (access@, Ads now direct to 5563867754). SIDE EFFECT: the 3 Google Ads integrations routed via MCC 4155514468 (Spencer, ICS, All Heart) went active → DISABLED; cause unconfirmed. Spencer had 25 CallRail conv/30d. Command Center fu-031. Lesson: after any CallRail OAuth reconnect, re-scan ALL companies' integrations, not just the one touched. Also: Napps / All Seasons Air / Supreme Ads integrations point to 8810470846, not the client accounts.

**10-10: the same key sees 10 CallRail ACCOUNTS, not just the agency one.** GET https://api.callrail.com/v3/a.json lists them; callrail.py is hardwired to ACC 792265907, so for others call /v3/a/<ACC id>/... directly. Accounts: Watt's Right Electric (537241053), TopServ Digital Clients (792265907), Potomac (723007586), OnTime Service Pros (535631172), Neon Monkey Tree (377441370), Live Wire Electric (438658328), Lilypad Septic (350598565), Kings Window Services (202875206), Hawkins Siding and Exteriors (232929821), Cool Hand Electric & Air PPC TopServe (235299530, ACC019e095affd97f04849c939538f341f1). Check here before saying a client's CallRail is out of reach.

**10-10 map of active CallRail companies → clients** lives in `topserv-workspace/paid/funnels/clients.json` (account + company ids for 11 clients).

**Rate limit (10-10):** after a 122-company tracker sweep + repeated funnel --all runs, the TopServ Digital Clients account (ICS, Spencer, C&S, All Seasons, Napps) returned HTTP 429 for 1h+ while client-owned accounts (Watt's Right, Cool Hand) kept working. Looks like a per-account cap. Avoid full sweeps; cache tracker lists; refresh one client at a time.

**10-22 all-clients number list** (Ryan asked, for Agency Titan profiles): `paid/callrail-numbers/` (pull_trackers.py → trackers_raw.json → build_sheet.py → xlsx). Live Wire's account no longer appears in /v3/a.json. OnTime Service Pros (ACC019ce325bf31714684e10256ccd739c0) returned 429 for 80+ min straight while other accounts worked fine, so it's probably blocked or cancelled, not a normal rate limit (On Time ended 10-16 per audit sheet).

**10-23 gotcha:** `callrail.py` urlencodes params, so commas in `fields=` become %2C and CallRail answers HTTP 400 (looks like a new block right after a 429). Use `paid/weekly-7day/callrail_calls_pull.py` (builds the URL by hand, pages through, writes JSON). For recordings + transcription use the `call-wins` skill (packaged 10-23; `pip install -r .claude/skills/call-wins/requirements.txt`, model small.en cached in ~/.cache/huggingface).

**10-23: Gui uses Edu's key** (shared via Bitwarden item "CallRail API (.env.callrail)", ONBOARDING step 8), so CallRail API activity from either of them shows as Edu.
