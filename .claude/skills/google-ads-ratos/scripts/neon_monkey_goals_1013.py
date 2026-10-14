"""Read-only: biddable goals on live campaigns + creation/change event for [TSD] Click to call."""
from lib import run_query
cid = "7953905280"
rows = run_query(cid, """SELECT campaign.id, campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
  FROM campaign_conversion_goal WHERE campaign.status = 'ENABLED'""")
for r in sorted(rows, key=lambda r: r["campaign"]["name"]):
    g = r["campaign_conversion_goal"]
    if g.get("biddable"):
        print(f"  {r['campaign']['name'][:34]:<34} BIDDABLE {g['category']}/{g['origin']}")
rows = run_query(cid, """SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields, change_event.new_resource
  FROM change_event WHERE change_event.change_date_time >= '2026-10-09' AND change_event.change_resource_type = 'CONVERSION_ACTION' LIMIT 50""")
for r in rows:
    e = r["change_event"]
    print("  change:", e["change_date_time"], e.get("user_email"), e.get("resource_change_operation"), str(e.get("new_resource",{}).get("conversion_action",{}).get("name","")))
