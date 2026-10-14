import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "7410489772"

print("CONVERSION ACTIONS - last 30 days (trust check)")
q2 = """
SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.conversions
FROM customer
WHERE segments.date DURING LAST_30_DAYS AND metrics.conversions > 0
"""
for r in run_query(CID, q2):
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    print(f"  {seg.get('conversionActionName', seg.get('conversion_action_name'))} | category={seg.get('conversionActionCategory', seg.get('conversion_action_category'))} | conversions={m.get('conversions')}")

print()
print("NETWORK SPLIT ON NON-BRANDED - last 30 days")
q4 = """
SELECT segments.ad_network_type, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.id = 24155674204 AND segments.date DURING LAST_30_DAYS
"""
for r in run_query(CID, q4):
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    print(f"  network={seg.get('adNetworkType', seg.get('ad_network_type'))} | clicks={m.get('clicks')} | impressions={m.get('impressions')} | conversions={m.get('conversions')} | cost_micros={m.get('costMicros', m.get('cost_micros'))}")

print()
print("DAILY SPEND/CLICKS/CONVERSIONS - last 30 days (non-branded, to see budget-change impact)")
q6 = """
SELECT segments.date, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.id = 24155674204 AND segments.date DURING LAST_30_DAYS
ORDER BY segments.date
"""
for r in run_query(CID, q6):
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    cost = m.get("costMicros", m.get("cost_micros", 0))
    print(f"  {seg.get('date')} | clicks={m.get('clicks')} | impr={m.get('impressions')} | conv={m.get('conversions')} | cost=${cost}")
