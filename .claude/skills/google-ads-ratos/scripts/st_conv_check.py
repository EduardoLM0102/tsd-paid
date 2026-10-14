import sys
sys.path.insert(0, ".")
from lib import run_query

CID = sys.argv[1] if len(sys.argv) > 1 else "8634274092"

q1 = """
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.category,
  conversion_action.origin,
  conversion_action.primary_for_goal,
  conversion_action.include_in_conversions_metric
FROM conversion_action
ORDER BY conversion_action.name
"""

rows = run_query(CID, q1)
print("=" * 118)
print(f"ALL CONVERSION ACTIONS — customer {CID}   (total {len(rows)})")
print("=" * 118)
print(f"{'NAME':<52} {'STATUS':<9} {'ORIGIN':<18} {'CATEGORY':<19} {'PRIM':<5} {'INCL':<5}")
print("-" * 118)
for r in rows:
    ca = r.get("conversion_action", {})
    print(f"{str(ca.get('name'))[:51]:<52} "
          f"{str(ca.get('status')):<9} "
          f"{str(ca.get('origin')):<18} "
          f"{str(ca.get('category'))[:18]:<19} "
          f"{str(ca.get('primary_for_goal')):<5} "
          f"{str(ca.get('include_in_conversions_metric')):<5}")

q2 = """
SELECT
  conversion_action.name,
  metrics.all_conversions,
  metrics.all_conversions_value
FROM conversion_action
WHERE segments.date DURING LAST_30_DAYS
"""
print("\n" + "=" * 118)
print("VOLUME — LAST 30 DAYS (all_conversions, only actions with >0)")
print("=" * 118)
rows2 = run_query(CID, q2)
agg = {}
for r in rows2:
    name = r.get("conversion_action", {}).get("name")
    m = r.get("metrics", {})
    d = agg.setdefault(name, {"conv": 0.0, "val": 0.0})
    d["conv"] += float(m.get("all_conversions") or 0)
    d["val"] += float(m.get("all_conversions_value") or 0)

live = {k: v for k, v in agg.items() if v["conv"] > 0}
for name, d in sorted(live.items(), key=lambda x: -x[1]["conv"]):
    print(f"  {str(name)[:58]:<60} conv={d['conv']:>8.1f}   value={d['val']:>10.2f}")
if not live:
    print("  (none fired in last 30 days)")
print(f"\n  actions with ZERO conversions in 30d: {len(agg) - len(live)} of {len(agg)}")
