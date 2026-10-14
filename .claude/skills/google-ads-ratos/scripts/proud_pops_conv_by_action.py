import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"
SINCE = "2026-08-04"
UNTIL = "2026-09-02"

print("=" * 100)
print(f"PROUD POPS — CONVERSIONS BY ACTION + CAMPAIGN, {SINCE} to {UNTIL}")
print("=" * 100)
q = f"""
SELECT campaign.name, campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
rows = list(run_query(CID, q))
agg = {}
agg_all = {}
for r in rows:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not aname:
        continue
    key = (cname, aname)
    agg[key] = agg.get(key, 0.0) + (m.get("conversions") or 0.0)
    agg_all[key] = agg_all.get(key, 0.0) + (m.get("allConversions") or m.get("all_conversions") or 0.0)

print("Using metrics.conversions (primary, matches report totals):")
for (cname, aname), v in sorted(agg.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  conversions={v:.2f}")

print("\nUsing metrics.all_conversions (includes secondary/local actions, for comparison):")
for (cname, aname), v in sorted(agg_all.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  all_conversions={v:.2f}")
