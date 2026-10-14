import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "4360840956"
q = """SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.origin,
  conversion_action.phone_call_duration_seconds, conversion_action.counting_type, conversion_action.tag_snippets
FROM conversion_action WHERE conversion_action.id IN (7769293652, 1058843888, 7539810847, 7676608944)"""
for r in run_query(CID, q):
    ca = r["conversion_action"]
    print(ca.get("id"), ca.get("name"), "type=", ca.get("type", ca.get("type_")), "origin=", ca.get("origin"), "dur=", ca.get("phone_call_duration_seconds"), "snippets=", len(ca.get("tag_snippets", [])))
    print("   keys:", sorted(ca.keys()))
q = """SELECT customer.call_reporting_setting.call_conversion_action, customer.call_reporting_setting.call_conversion_reporting_enabled FROM customer"""
for r in run_query(CID, q):
    print("account default call conv action:", r["customer"].get("call_reporting_setting"))
