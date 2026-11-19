import sys; sys.path.insert(0, ".")
from lib import run_query
CID="9865206319"
for r in run_query(CID,"SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields, change_event.old_resource, change_event.new_resource, change_event.client_type FROM change_event WHERE change_event.change_date_time >= '2026-11-10 00:00:00' AND change_event.change_date_time <= '2026-11-19 23:59:59' LIMIT 50"):
    e=r["change_event"]
    if "topservdigital" in (e.get("user_email") or ""): continue
    print(e["change_date_time"][:19], e.get("user_email"), e.get("client_type"), e["change_resource_type"], e.get("resource_change_operation"), e.get("changed_fields"))
    print("   OLD", str(e.get("old_resource"))[:400]); print("   NEW", str(e.get("new_resource"))[:400])
