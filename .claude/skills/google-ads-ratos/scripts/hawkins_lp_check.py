import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "2198608170"
q = """
SELECT ad_group.name, ad_group_ad.ad.final_urls, ad_group_ad.status
FROM ad_group_ad
WHERE campaign.id = 23805382277 AND ad_group_ad.status = ENABLED
"""
for r in run_query(CID, q):
    print(r.get('ad_group',{}).get('name'), '->', r.get('ad_group_ad',{}).get('ad',{}).get('final_urls'))
