import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "7410489772"
q = """
SELECT conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.status, conversion_action.counting_type,
       conversion_action.resource_name
FROM conversion_action
"""
for r in run_query(CID, q):
    ca = r.get("conversionAction", r.get("conversion_action", {}))
    print(ca)
