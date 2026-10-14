import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"
SINCE = "2026-09-01"
UNTIL = "2026-09-15"

print("=" * 100)
print(f"PROUD POPS — CONVERSIONS BY ACTION + CAMPAIGN, {SINCE} to {UNTIL}")
print("=" * 100)
q = f"""
SELECT campaign.name, campaign.id, campaign.status, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
rows = list(run_query(CID, q))
agg = {}
for r in rows:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not aname:
        continue
    key = (cname, aname)
    agg[key] = agg.get(key, 0.0) + (m.get("conversions") or 0.0)

q2 = f"""
SELECT campaign.name, metrics.cost_micros
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
rows2 = list(run_query(CID, q2))
cost_by_camp = {}
for r in rows2:
    cname = r.get("campaign", {}).get("name")
    m = r.get("metrics", {})
    cost_by_camp[cname] = cost_by_camp.get(cname, 0.0) + float(m.get("costMicros") or m.get("cost_micros") or 0) / 1e6

print("Conversions by campaign + action (metrics.conversions):")
for (cname, aname), v in sorted(agg.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  conversions={v:.2f}")

print("\nSpend by campaign:")
for cname, cost in sorted(cost_by_camp.items(), key=lambda x: -x[1]):
    print(f"  {cname:45s}  cost=${cost:,.2f}")

print("\n" + "=" * 100)
print("Real leads only (Website lead + Calls from ads), by campaign:")
real_actions = {"Website lead", "Calls from ads"}
totals_by_camp = {}
for (cname, aname), v in agg.items():
    if aname in real_actions:
        totals_by_camp[cname] = totals_by_camp.get(cname, 0.0) + v
grand_total = 0.0
for cname, v in sorted(totals_by_camp.items(), key=lambda x: -x[1]):
    print(f"  {cname:45s}  real_leads={v:.2f}")
    grand_total += v
print(f"\nTOTAL real leads (Website lead + Calls from ads), {SINCE} to {UNTIL}: {grand_total:.2f}")
total_cost = sum(cost_by_camp.values())
print(f"TOTAL spend: ${total_cost:,.2f}")
if grand_total > 0:
    print(f"REAL CPL: ${total_cost/grand_total:,.2f}")
