from h import *
q = """
SELECT change_status.last_change_date_time, change_status.resource_type, change_status.resource_status, change_status.campaign, change_status.ad_group, change_status.campaign_budget
FROM change_status
WHERE change_status.last_change_date_time >= '2026-06-26 00:00:00' AND change_status.last_change_date_time <= '2026-09-25 00:00:00'
ORDER BY change_status.last_change_date_time
LIMIT 10000
"""
try:
    rows=list(run_query(CID,q))
except Exception as e:
    print("ERR", str(e)[:400]); raise SystemExit
print(len(rows))
json.dump(rows, open(OUT+"change_status.json","w"), default=str)
for r in rows:
    c=r["change_status"]
    if c.get("resource_type") in ("CAMPAIGN","CAMPAIGN_BUDGET","CAMPAIGN_CRITERION","CONVERSION_ACTION","CUSTOMER","AD_GROUP") or True:
        print(c.get("last_change_date_time"), c.get("resource_type"), c.get("resource_status"), (c.get("campaign") or "")[-12:], (c.get("ad_group") or "")[-12:])
