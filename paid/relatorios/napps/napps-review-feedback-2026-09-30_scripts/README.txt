Read-only pulls behind the 2026-09-30 client-feedback entry in clients/napps/google-ads-log.md.
Run from .claude/skills/google-ads-ratos/scripts via: ./tsd.sh <abs path to script>
napps_check.py  = 2025 missed-call detail (call_view) + current enabled campaigns/budgets + spend since 09-15
napps_check2.py = 2026 call_view rows by month/campaign (found the PMax rows)
napps_check3.py = PMax vs Search call durations, 2026 window
napps_check4.py = Search calls per campaign (calls, connected, >=60s), 2025 vs 2026
Gotcha: do NOT select ad_group.* on call_view; it silently drops Performance Max rows.
