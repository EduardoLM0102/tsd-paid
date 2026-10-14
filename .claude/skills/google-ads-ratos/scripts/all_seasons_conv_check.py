import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"

print("=" * 100)
print("ALL SEASONS AC — CONVERSIONS BY ACTION + CAMPAIGN, LAST_7_DAYS")
print("=" * 100)
q = f"""
SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
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

for (cname, aname), v in sorted(agg.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  conversions={v:.2f}")

print()
print("=" * 100)
print("NETWORK SETTINGS + NETWORK-SPLIT PERFORMANCE (Search campaigns), LAST_7_DAYS")
print("=" * 100)
q2 = """
SELECT campaign.id, campaign.name, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network
FROM campaign
WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    ns = c.get("networkSettings", c.get("network_settings", {}))
    print(f"  {c.get('name'):45s} id={c.get('id'):15s} search_partners={ns.get('targetSearchNetwork', ns.get('target_search_network'))}  display={ns.get('targetContentNetwork', ns.get('target_content_network'))}")

print()
q3 = """
SELECT campaign.name, segments.ad_network_type, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH' AND segments.date DURING LAST_7_DAYS
"""
netagg = {}
for r in run_query(CID, q3):
    cname = r.get("campaign", {}).get("name")
    net = r.get("segments", {}).get("ad_network_type") or r.get("segments", {}).get("adNetworkType")
    m = r.get("metrics", {})
    key = (cname, net)
    if key not in netagg:
        netagg[key] = {"clicks": 0, "impr": 0, "conv": 0.0, "cost": 0}
    netagg[key]["clicks"] += int(m.get("clicks") or 0)
    netagg[key]["impr"] += int(m.get("impressions") or 0)
    netagg[key]["conv"] += float(m.get("conversions") or 0.0)
    netagg[key]["cost"] += int(m.get("costMicros") or m.get("cost_micros") or 0)

for (cname, net), v in sorted(netagg.items()):
    print(f"  {cname:45s} | {str(net):20s} clicks={v['clicks']:5d} impr={v['impr']:6d} conv={v['conv']:6.2f} cost=${v['cost']/1_000_000:.2f}")
