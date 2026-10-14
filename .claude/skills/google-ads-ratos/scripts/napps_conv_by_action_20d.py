import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "9509605037"
SINCE = "2026-08-26"
UNTIL = "2026-09-14"

print("=" * 100)
print(f"NAPPS — CONVERSIONS BY ACTION NAME, LAST 20 DAYS ({SINCE} to {UNTIL}, account-level)")
print("=" * 100)
q = f"""
SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.all_conversions, metrics.conversions
FROM customer
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
rows = list(run_query(CID, q))
agg = {}
for r in rows:
    name = r.get("segments", {}).get("conversion_action_name")
    cat = r.get("segments", {}).get("conversion_action_category")
    m = r.get("metrics", {})
    if not name:
        continue
    a = agg.setdefault(name, {"conversions": 0.0, "all_conversions": 0.0, "cat": cat})
    a["conversions"] += m.get("conversions", 0.0) or 0.0
    a["all_conversions"] += m.get("all_conversions", 0.0) or 0.0

total_conv = 0.0
total_allconv = 0.0
for name, v in sorted(agg.items(), key=lambda x: -x[1]["all_conversions"]):
    print(f"  {name:30s} [{v['cat']:20s}]  conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")
    total_conv += v["conversions"]
    total_allconv += v["all_conversions"]

print(f"\n  TOTAL  conversions={total_conv:.2f}  all_conversions={total_allconv:.2f}")

print("\n" + "=" * 100)
print("BREAKDOWN BY CAMPAIGN (same window)")
print("=" * 100)
q2 = f"""
SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions, metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
camp_agg = {}
for r in run_query(CID, q2):
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not aname or not (m.get("all_conversions") or m.get("conversions")):
        continue
    key = (cname, aname)
    a = camp_agg.setdefault(key, {"conversions": 0.0, "all_conversions": 0.0})
    a["conversions"] += m.get("conversions", 0.0) or 0.0
    a["all_conversions"] += m.get("all_conversions", 0.0) or 0.0

for (cname, aname), v in sorted(camp_agg.items(), key=lambda x: -x[1]["all_conversions"]):
    if v["all_conversions"] == 0 and v["conversions"] == 0:
        continue
    print(f"  {cname:45s} | {aname:25s} conversions={v['conversions']:.2f} all_conversions={v['all_conversions']:.2f}")
