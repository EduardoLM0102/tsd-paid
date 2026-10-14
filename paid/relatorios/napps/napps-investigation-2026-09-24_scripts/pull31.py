from h import *
S="8810470846"
q="""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.category, conversion_action.primary_for_goal
FROM conversion_action WHERE conversion_action.status != 'REMOVED'"""
for r in run_query(S,q):
    c=r["conversion_action"]; print(c["id"], "|", c["name"], "|", c.get("type_") or c.get("type"), "|", c["status"], "|", c.get("category"), "| primary=", c.get("primary_for_goal"))
print("\n--- conversions by action name, last 120d ---")
q="""SELECT segments.conversion_action_name, segments.month, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-05-01' AND '2026-09-23'"""
from collections import defaultdict
d=defaultdict(lambda:defaultdict(float))
for r in run_query(S,q):
    n=r["segments"].get("conversion_action_name"); 
    if n: d[n][r["segments"]["month"][:7]]+=f(r["metrics"].get("all_conversions"))
for n,v in d.items(): print(n, dict(v))
