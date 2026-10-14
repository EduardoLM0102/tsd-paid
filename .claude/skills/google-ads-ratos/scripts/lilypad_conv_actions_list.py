import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "3797438623"

q = """
SELECT conversion_action.id, conversion_action.name, conversion_action.status,
       conversion_action.type, conversion_action.category, conversion_action.primary_for_goal,
       conversion_action.owner_customer
FROM conversion_action
"""
rows = list(run_query(CID, q))
for r in rows:
    ca = r.get("conversion_action", {})
    print(f"id={ca.get('id')} name={ca.get('name')!r} status={ca.get('status')} type={ca.get('type')} "
          f"category={ca.get('category')} primary={ca.get('primary_for_goal')} owner={ca.get('owner_customer')}")
