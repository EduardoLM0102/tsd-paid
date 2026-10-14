import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "2524618054"

print("=" * 100)
print("CHANGE HISTORY for Nonbranded Search campaign 23822363451")
print("=" * 100)
import datetime
today = datetime.date.today()
start = today - datetime.timedelta(days=89)
q = f"""
SELECT change_event.change_date_time, change_event.change_resource_type,
       change_event.resource_change_operation, change_event.user_email,
       change_event.campaign, change_event.changed_fields,
       change_event.old_resource, change_event.new_resource
FROM change_event
WHERE change_event.campaign = 'customers/2524618054/campaigns/23822363451'
  AND change_event.change_date_time BETWEEN '{start.isoformat()} 00:00:00' AND '{today.isoformat()} 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 30
"""
try:
    for r in run_query(CID, q):
        ce = r.get("change_event", {})
        print(f"\n{ce.get('change_date_time')}  by {ce.get('user_email')}")
        print(f"  resource_type={ce.get('change_resource_type')}  op={ce.get('resource_change_operation')}")
        print(f"  changed_fields={ce.get('changed_fields')}")
        old = ce.get('old_resource', {})
        new = ce.get('new_resource', {})
        if 'campaign' in old or 'campaign' in new:
            print(f"  old.status={old.get('campaign', {}).get('status')}  new.status={new.get('campaign', {}).get('status')}")
except Exception as e:
    print(f"ERROR: {e}")
