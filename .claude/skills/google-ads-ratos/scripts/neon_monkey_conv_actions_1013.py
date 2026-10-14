"""Read-only: Neon Monkey 7953905280 conversion actions (status/primary/category/tag label) + daily all_conversions since 10-06."""
from lib import run_query
cid = "7953905280"
rows = run_query(cid, """SELECT conversion_action.id, conversion_action.name, conversion_action.status, conversion_action.type,
  conversion_action.category, conversion_action.primary_for_goal, conversion_action.tag_snippets, conversion_action.counting_type
  FROM conversion_action WHERE conversion_action.status = 'ENABLED'""")
for r in rows:
    ca = r["conversion_action"]
    labels = set()
    for t in ca.get("tag_snippets", []):
        import re
        labels |= set(re.findall(r"send_to': 'AW-\d+/([A-Za-z0-9_-]+)", t.get("event_snippet", "")))
    print(f"{ca['id']:>12} {ca['name'][:40]:<40} {ca.get('type_', ca.get('type','')):<22} {ca.get('category',''):<22} primary={ca.get('primary_for_goal')} {ca.get('counting_type','')} labels={','.join(labels)}")
print("\nall_conversions by action+day since 10-06 (nonzero)")
rows = run_query(cid, """SELECT segments.date, segments.conversion_action_name, metrics.all_conversions, metrics.conversions
  FROM customer WHERE segments.date BETWEEN '2026-10-06' AND '2026-10-13'""")
for r in sorted(rows, key=lambda r: (r["segments"]["date"], r["segments"]["conversion_action_name"])):
    m = r["metrics"]
    if float(m.get("all_conversions", 0)):
        print(f"  {r['segments']['date']}  {r['segments']['conversion_action_name'][:40]:<40} all={float(m.get('all_conversions',0)):.1f}  biddable={float(m.get('conversions',0)):.1f}")
