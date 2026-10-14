import sys
sys.path.insert(0, ".")
from lib import run_query
import datetime

CID = "9509605037"
today = datetime.date.today()
start = today - datetime.timedelta(days=6)

q = f"""
SELECT change_event.change_date_time, change_event.user_email,
       change_event.campaign, change_event.changed_fields,
       change_event.old_resource, change_event.new_resource
FROM change_event
WHERE change_event.change_resource_type = 'CAMPAIGN_BUDGET'
  AND change_event.change_date_time BETWEEN '{start.isoformat()} 00:00:00' AND '{today.isoformat()} 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 10
"""
rows = run_query(CID, q)
for r in rows:
    ce = r.get("change_event", {})
    print(f"{ce.get('change_date_time')} by {ce.get('user_email')} campaign={ce.get('campaign')}")
    print(f"  old_resource={ce.get('old_resource')}")
    print(f"  new_resource={ce.get('new_resource')}")
