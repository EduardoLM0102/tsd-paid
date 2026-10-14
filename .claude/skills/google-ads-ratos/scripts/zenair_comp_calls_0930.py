"""Zen Air 2026-09-30: which days competitor-name searches converted, next to that day's ad calls (read-only)."""
import sys
from collections import defaultdict
sys.path.insert(0, ".")
from lib import run_query
from zenair_st_classify_0930 import cls
CID = "4360840956"
conv = defaultdict(list)
for r in run_query(CID, """SELECT segments.date, search_term_view.search_term, segments.conversion_action_name, metrics.conversions
  FROM search_term_view WHERE campaign.id = 24100030790 AND segments.date BETWEEN '2026-08-27' AND '2026-09-29' AND metrics.conversions > 0"""):
    t = r["search_term_view"]["search_term"]
    conv[r["segments"]["date"]].append(f"{t} [{cls(t)}] -> {r['segments']['conversion_action_name']} x{r['metrics']['conversions']}")
calls = defaultdict(list)
for r in run_query(CID, """SELECT call_view.start_call_date_time, call_view.call_duration_seconds, campaign.id FROM call_view
  WHERE call_view.start_call_date_time >= '2026-08-27 00:00:00'"""):
    c = r["call_view"]
    if r["campaign"]["id"] == "24100030790":
        calls[c["start_call_date_time"][:10]].append(f"{c['start_call_date_time'][11:16]} ({c.get('call_duration_seconds', 0)}s)")
for d in sorted(conv):
    print(d, "| calls:", ", ".join(calls.get(d, [])) or "none")
    for x in conv[d]:
        print("    ", x)
