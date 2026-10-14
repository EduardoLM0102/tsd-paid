import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "3797438623"

def segment(label, since, until):
    print("=" * 100)
    print(f"{label}  ({since} to {until})")
    print("=" * 100)
    q = f"""
    SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.all_conversions, metrics.conversions
    FROM customer
    WHERE segments.date BETWEEN '{since}' AND '{until}'
    """
    rows = list(run_query(CID, q))
    agg = {}
    for r in rows:
        name = r.get("segments", {}).get("conversion_action_name")
        cat = r.get("segments", {}).get("conversion_action_category")
        m = r.get("metrics", {})
        if not name:
            continue
        a = agg.setdefault((name, cat), {"conversions": 0.0, "all_conversions": 0.0})
        a["conversions"] += m.get("conversions", 0.0) or 0.0
        a["all_conversions"] += m.get("all_conversions", 0.0) or 0.0

    for (name, cat), v in sorted(agg.items(), key=lambda x: -x[1]["all_conversions"]):
        if v["all_conversions"] <= 0:
            continue
        print(f"  {name:40s} [{cat:25s}] conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")

segment("SINCE LAUNCH", "2026-08-20", "2026-09-14")
print()
segment("LAST 7 DAYS", "2026-09-07", "2026-09-13")
