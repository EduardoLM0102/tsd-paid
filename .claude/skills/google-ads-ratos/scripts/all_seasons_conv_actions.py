import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"
q = """
SELECT conversion_action.name, conversion_action.status, conversion_action.type,
       conversion_action.value_settings.default_value,
       conversion_action.value_settings.always_use_default_value,
       conversion_action.include_in_conversions_metric,
       conversion_action.primary_for_goal
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
"""
for r in run_query(CID, q):
    print(json.dumps(r, indent=2))
