"""Spencer GA4 313187998 realtime: events in last 30 min (read-only)."""
import sys
sys.path.insert(0, ".")
from ga4_setup import data_service
r = data_service().properties().runRealtimeReport(property="properties/313187998", body={
    "dimensions": [{"name": "eventName"}, {"name": "minutesAgo"}], "metrics": [{"name": "eventCount"}], "limit": 200}).execute()
rows = [([d["value"] for d in x["dimensionValues"]], x["metricValues"][0]["value"]) for x in r.get("rows", [])]
for (ev, mins), c in sorted(rows, key=lambda x: int(x[0][1])):
    print(f"  {mins:>3} min ago  {ev:30s} {c}")
print("generate_lead total:", sum(int(c) for (ev, _), c in rows if ev == "generate_lead"))
