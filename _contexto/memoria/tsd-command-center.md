---
name: tsd-command-center
description: "TSD Command Center artifact (built 2026-10-08) — Edu's web ops board; every \"revisit on X\" and every channel check must be written to its DB"
metadata:
  node_type: memory
  type: project
  originSessionId: 715c702a-049e-427e-a580-f1c760b49680
  modified: 2026-10-09T00:07:55.956Z
---

TSD Command Center = private claude.ai artifact https://claude.ai/artifact/1gah5xuCXDADf4kYVYp95q (built 2026-10-08). Source: topserv-workspace/paid/command-center/ (tsd-command-center.html, seed.py = initial 10-08 seed, google_channels.py = read-only 7d spend by channel type, run via tsd.sh). Republish by passing the URL after an Artifact `read`.

DB (ArtifactData): `clients/<slug>` {name, market, status active|confirm|onboarding|offboarding|frozen|offboarded, statusNote, channels.{google,lsa,meta,youtube}.{state live|missing|noaccess|confirm|paused, spend7, accounts, lastChecked, checkSource, note}}; `followups/<id>` {client slug|null, title, due, details (what's needed; '- ' lines = bullets; end with 'Source: ...'), note, status open|done, doneAt, createdBy}; `checks` (log from the page); `meta/sync` {channelsAsOf, window, source}. Write rule = admin only.

Layout v2 (10-08, Edu's ask): NO separate follow-up section; client cards in a list (tallies double as quick filters, General card for client-less follow-ups) → click opens client popup (channels, stale checks, follow-up warning) → warning opens 2nd popup with each follow-up's details + Done/Snooze/Add/Reopen. Edu uses Done on the page (fu-007, fu-008 marked by him 10-08), so always re-read and pin if_version before writing. 7-day rule counts only live channels on active clients. OPEN QUESTION to Edu: exclude awareness-only channels (e.g. Cool Hand Meta) from the 7-day rule? Gaps column = missing/noaccess/confirm channels + clients with status confirm (onboarding excluded).

**Why:** Edu wants to work from a website, not VS Code, and Claude can't nudge him proactively; the page's flags are the reminder. He explicitly does NOT want Slack DMs as the main channel; the flag on the interface is crucial (Slack optional extra).

**How to apply:** whenever we say "revisit X on Y", add a `followups` doc. After any weekly channel check, update that channel's lastChecked/spend7/state. When a client comes up, read its open follow-ups first. Same protocol is in topserv-workspace/CLAUDE.md. Not yet built: auto Google/LSA refresh, live Meta/AT pulls from the page, SessionStart hook. Related: [[tsd-weekly-ppc-snapshot]], [[tsd-weekly-meta-snapshot]], [[tsd-agency-titan-weekly-tasks]].

**Lead funnel (10-10):** collection `funnels/<client slug>` renders a 'Lead funnel' section in the client pop-up (date-range chips Today/Yesterday/Last 3-7-14-30 days/This week/Last week/Custom; 'Last N days' = full days through yesterday like Google Ads; doc holds one row per DAY per campaign from 08-10 and the page sums the range; Search/YouTube/All, website path clicks→taps→CallRail calls→answered→60s+, ad-button path placed→answered→60s+, per-campaign table) + a 'Lead funnel' chip on the card. Cool Hand only so far: refresh = run `clients/cool-hand-electric/funnel_build.py` via tsd.sh, then ArtifactData set funnels/cool-hand-electric with file_path = the JSON it writes. Do it on every Cool Hand check AND whenever Edu says 'refresh the Cool Hand funnel' (page tells him to ask). ~48 KB at 62 days.

**Funnel refresh (10-10):** page v5 declares mcp host:tsd_funnel (local MCP server `.claude/skills/google-ads-ratos/scripts/funnel_mcp_server.py`, tool refresh_funnel({client}), registered in Claude desktop config + Claude Code user scope; desktop config backup *.bak-2026-10-10). 'Refresh now' button + auto-refresh on open when data >6h old, ONLY in the Claude desktop app, owner only; the page writes funnels/<slug> itself. Twice-daily unattended push (funnel_refresh_daily.sh = pull + headless Claude ArtifactData set, needs the VS Code-bundled claude binary; npm claude 2.1.195 lacks ArtifactData) was BLOCKED by the auto-mode safety check as unauthorized persistence; NOT scheduled. Only install a launchd job if Edu explicitly approves.

**Funnels for 11 clients (10-10):** shared builder `topserv-workspace/paid/funnels/funnel_build.py` + `clients.json` (cid, CallRail account/company, optional overrides) + `log.md` (tracking gaps table). Clients: watts-right, spencer-air, napps, integrate-comfort, cs-air, all-seasons-ac, neon-monkey, lilypad-septic, kings-window, hawkins-siding, cool-hand-electric. Auto-picks actions (taps=CLICK_TO_CALL else GA4 phone; forms=TSD tags else GA4 ghl_/form_submit, never both; button=AD_CALL+Smart calls; uploads=CallRail call uploads); marks taps untracked if 0 in 60d with 200+ clicks. Page scopes by campaign type (Search/PMax/Smart/YouTube). Refresh tool tsd_funnel covers all; Watt's Right ~30s. Excluded: Live Wire (confirm), OnTime (offboarding, Meta only), Potomac + Supreme (not CC clients).
