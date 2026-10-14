import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "3797438623"

print("=" * 100)
print("CONVERSIONS BY ACTION NAME, SINCE LAUNCH (2026-08-20 to today, account-level)")
print("=" * 100)
q = """
SELECT segments.conversion_action_name, segments.date, metrics.all_conversions, metrics.conversions
FROM customer
WHERE segments.date BETWEEN '2026-08-20' AND '2026-08-30'
"""
rows = list(run_query(CID, q))
agg = {}
by_date = {}
for r in rows:
    name = r.get("segments", {}).get("conversion_action_name")
    date = r.get("segments", {}).get("date")
    m = r.get("metrics", {})
    if not name:
        continue
    a = agg.setdefault(name, {"conversions": 0.0, "all_conversions": 0.0})
    a["conversions"] += m.get("conversions", 0.0) or 0.0
    a["all_conversions"] += m.get("all_conversions", 0.0) or 0.0
    if (m.get("all_conversions", 0.0) or 0.0) > 0:
        by_date.setdefault(name, []).append((date, m.get("all_conversions", 0.0)))

for name, v in sorted(agg.items(), key=lambda x: -x[1]["all_conversions"]):
    print(f"  {name:45s}  conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")
    if name in by_date:
        for date, val in by_date[name]:
            print(f"      {date}: {val}")

print("\n" + "=" * 100)
print("CONVERSIONS BY ACTION NAME + CAMPAIGN, SINCE LAUNCH")
print("=" * 100)
q2 = """
SELECT campaign.name, segments.conversion_action_name, segments.date, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '2026-08-20' AND '2026-08-30'
"""
rows2 = list(run_query(CID, q2))
agg2 = {}
for r in rows2:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    date = r.get("segments", {}).get("date")
    m = r.get("metrics", {})
    if not aname:
        continue
    val = m.get("all_conversions", 0.0) or 0.0
    if val <= 0:
        continue
    key = (cname, aname)
    agg2.setdefault(key, []).append((date, val))

for (cname, aname), vals in sorted(agg2.items(), key=lambda x: (x[0][0], -sum(v for _, v in x[1]))):
    total = sum(v for _, v in vals)
    print(f"  {cname:45s} | {aname:35s}  all_conversions={total:.2f}")
    for date, val in vals:
        print(f"      {date}: {val}")

print("\n" + "=" * 100)
print("CAMPAIGN SPEND + CLICKS, SINCE LAUNCH (sanity check)")
print("=" * 100)
q3 = """
SELECT campaign.name, metrics.cost_micros, metrics.clicks
FROM campaign
WHERE segments.date BETWEEN '2026-08-20' AND '2026-08-30'
"""
rows3 = list(run_query(CID, q3))
agg3 = {}
for r in rows3:
    cname = r.get("campaign", {}).get("name")
    m = r.get("metrics", {})
    a = agg3.setdefault(cname, {"cost": 0.0, "clicks": 0})
    a["cost"] += float(m.get("costMicros", m.get("cost_micros", 0)) or 0) / 1_000_000
    a["clicks"] += int(m.get("clicks", 0) or 0)

for cname, v in agg3.items():
    print(f"  {cname:45s}  spend=${v['cost']:.2f}  clicks={v['clicks']}")
