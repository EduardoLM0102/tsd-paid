import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"
q = """
SELECT conversion_action.name, conversion_action.primary_for_goal, conversion_action.status
FROM conversion_action
WHERE conversion_action.name = 'TSD - Website Call'
"""
for r in run_query(CID, q):
    print(r)
