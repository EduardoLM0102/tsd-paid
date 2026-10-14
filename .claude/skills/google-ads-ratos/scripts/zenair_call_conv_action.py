import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"

q = """
SELECT conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.status, conversion_action.phone_call_duration_seconds
FROM conversion_action
WHERE conversion_action.category = 'PHONE_CALL_LEAD'
"""
for r in run_query(CID, q):
    ca = r.get("conversionAction") or r.get("conversion_action") or {}
    name = ca.get("name")
    typ = ca.get("type")
    status = ca.get("status")
    dur = ca.get("phoneCallDurationSeconds") if "phoneCallDurationSeconds" in ca else ca.get("phone_call_duration_seconds")
    print(f"name={name!r} type={typ} status={status} duration_threshold_seconds={dur}")
