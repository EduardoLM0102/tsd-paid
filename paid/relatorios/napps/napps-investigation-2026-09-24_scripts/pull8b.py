from h import *
from collections import Counter
q2 = """
SELECT change_event.change_date_time, change_event.user_email, change_event.client_type, change_event.change_resource_type,
       change_event.resource_change_operation, change_event.changed_fields, change_event.campaign, change_event.ad_group,
       change_event.change_resource_name
FROM change_event
WHERE change_event.change_date_time >= '2026-08-26 00:00:00' AND change_event.change_date_time <= '2026-09-24 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 10000
"""
rows=list(run_query(CID,q2))
json.dump(rows, open(OUT+"change_events.json","w"), default=str)
print(len(rows))
print(Counter((r["change_event"].get("user_email"), r["change_event"].get("client_type")) for r in rows))
print(Counter((r["change_event"].get("change_resource_type")) for r in rows))
for r in rows:
    ce=r["change_event"]
    if ce.get("change_resource_type") in ("CAMPAIGN_BUDGET","CAMPAIGN","CAMPAIGN_CRITERION","CONVERSION_ACTION","AD_GROUP","AD_GROUP_CRITERION","AD","CUSTOMER") :
        print(ce.get("change_date_time"), ce.get("user_email"), ce.get("client_type"), ce.get("change_resource_type"), ce.get("resource_change_operation"), str(ce.get("changed_fields"))[:120], (ce.get("campaign") or "")[-12:])
