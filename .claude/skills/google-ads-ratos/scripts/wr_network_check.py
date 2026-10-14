import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
for cid, name in [("24094882200","EVCharger"), ("23832838033","Nonbranded"), ("23690645223","Branded")]:
    print(f"=== {name} ({cid}) settings ===")
    qs = f"""
    SELECT campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
           campaign.network_settings.target_partner_search_network
    FROM campaign WHERE campaign.id = {cid}
    """
    for r in run_query(CID, qs):
        print(json.dumps(r))
    print(f"=== {name} network breakdown (7d) ===")
    q = f"""
    SELECT segments.ad_network_type, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
    FROM campaign WHERE campaign.id = {cid} AND segments.date DURING LAST_7_DAYS
    """
    for r in run_query(CID, q):
        print(json.dumps(r))
