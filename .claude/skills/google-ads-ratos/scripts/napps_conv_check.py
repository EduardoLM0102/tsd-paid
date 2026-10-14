import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "9509605037"

print("=" * 100)
print("CONVERSIONS BY ACTION NAME, SINCE TRACKING REBUILD (2026-08-03 to today, account-level)")
print("=" * 100)
q = """
SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.all_conversions, metrics.conversions
FROM customer
WHERE segments.date BETWEEN '2026-08-03' AND '2026-08-31'
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

for name, v in sorted(agg.items(), key=lambda x: -x[1]["all_conversions"]):
    print(f"  {name:30s} [{v['cat']:20s}]  conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")

print("\n" + "=" * 100)
print("NETWORK SETTINGS + NETWORK-SPLIT PERFORMANCE, LIVE SEARCH CAMPAIGNS, LAST 30 DAYS")
print("=" * 100)
q2 = """
SELECT campaign.id, campaign.name, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network
FROM campaign
WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    ns = c.get("network_settings", {})
    print(f"  {c.get('name'):40s} id={c.get('id')} target_search_network={ns.get('target_search_network')} target_content_network={ns.get('target_content_network')}")

q3 = """
SELECT campaign.name, segments.ad_network_type, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH' AND segments.date DURING LAST_30_DAYS
"""
netagg = {}
for r in run_query(CID, q3):
    cname = r.get("campaign", {}).get("name")
    net = r.get("segments", {}).get("ad_network_type")
    m = r.get("metrics", {})
    key = (cname, net)
    a = netagg.setdefault(key, {"clicks": 0, "impressions": 0, "conversions": 0.0, "cost": 0.0})
    a["clicks"] += int(m.get("clicks", 0) or 0)
    a["impressions"] += int(m.get("impressions", 0) or 0)
    a["conversions"] += m.get("conversions", 0.0) or 0.0
    a["cost"] += float(m.get("cost_micros", 0) or 0) / 1_000_000

for (cname, net), v in sorted(netagg.items()):
    print(f"  {cname:40s} | {net:16s} clicks={v['clicks']:4d} impr={v['impressions']:5d} conv={v['conversions']:.2f} cost=${v['cost']:.2f}")

print("\n" + "=" * 100)
print("NEGATIVE KEYWORDS CHECK (campaign + ad group level)")
print("=" * 100)
q4 = """
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.negative = true AND campaign_criterion.type = 'KEYWORD'
"""
neg_count = {}
for r in run_query(CID, q4):
    cname = r.get("campaign", {}).get("name")
    neg_count[cname] = neg_count.get(cname, 0) + 1
if neg_count:
    for cname, n in neg_count.items():
        print(f"  {cname:40s} negatives={n}")
else:
    print("  NENHUMA negativa de campanha encontrada na conta.")
