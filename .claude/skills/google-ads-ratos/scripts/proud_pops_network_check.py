import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"

print("=" * 100)
print("NETWORK SETTINGS + AI MAX (search campaigns)")
print("=" * 100)
q = """
SELECT campaign.id, campaign.name, campaign.status,
       campaign.network_settings.target_google_search,
       campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network,
       campaign.network_settings.target_partner_search_network
FROM campaign
WHERE campaign.advertising_channel_type = 'SEARCH'
AND campaign.status != 'REMOVED'
"""
for r in run_query(CID, q):
    c = r.get("campaign", {})
    ns = c.get("networkSettings", c.get("network_settings", {}))
    print(f"  {c.get('name','')[:45]:45s} status={c.get('status')} | search_partners={ns.get('targetSearchNetwork', ns.get('target_search_network'))} | "
          f"display/content_net={ns.get('targetContentNetwork', ns.get('target_content_network'))}")
