from h import *
from collections import defaultdict
q = """
SELECT call_view.start_call_date_time, call_view.end_call_date_time, call_view.call_duration_seconds, call_view.call_status,
       call_view.type, call_view.call_tracking_display_location, call_view.caller_area_code, call_view.caller_country_code,
       campaign.name, campaign.id, ad_group.name
FROM call_view
WHERE call_view.start_call_date_time >= '2024-01-01 00:00:00'
"""
try:
    rows = list(run_query(CID, q))
except Exception as e:
    print("ERR", e); raise
json.dump(rows, open(OUT+"call_view.json","w"), default=str)
print("calls", len(rows))
if rows: print(json.dumps(rows[0], default=str, indent=1))
