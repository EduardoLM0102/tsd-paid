"""Cool Hand 2026-10-09 (Edu's go): sitelinks for campaigns whose ads land on the go. homepage.
ALREADY APPLIED 2026-10-09, don't re-run.
- Creates 3 sitelink assets pointing to the go. service pages, links them to TSD_Search_Branded + TSD_YouTube.
- Unlinks the old main-site sitelinks from those 2 campaigns (assets kept; they're shared with Electrical/HVAC).
- Unlinks the 3 ad-group sitelinks on AC-Repair (they overrode the HVAC campaign set; one was 'Electrician In Mansfield').
Policy: each sitelink in a campaign must go to a different page, not the ad's own page. Branded/YouTube ads -> go./ so the 3 service pages are fine.
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys, time
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client, run_query

CID = "9865206319"
BRANDED, YOUTUBE = "TSD_Search_Branded", "TSD_YouTube"
NEW = [
    ("Electrician Services", "https://go.coolhandelectric.com/electrician/", "Licensed, local electricians", "Ask about our $37 inspection"),
    ("AC Repair", "https://go.coolhandelectric.com/ac-repair/", "Licensed techs find the cause", "Easy payment plans available"),
    ("Heating & HVAC Repair", "https://go.coolhandelectric.com/hvac-repair/", "AC, furnace and heat pump", "Family-owned, licensed techs"),
]
client = init_client()
ga = client.get_service("GoogleAdsService")
camp_ids = {r["campaign"]["name"]: r["campaign"]["id"] for r in run_query(CID, f"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name IN ('{BRANDED}','{YOUTUBE}')")}

# 1) old campaign-level sitelink links on Branded + YouTube, and ad-group sitelink links on AC-Repair
old_c = [r["campaignAsset"]["resourceName"] if "campaignAsset" in r else r["campaign_asset"]["resource_name"]
         for r in run_query(CID, f"""SELECT campaign_asset.resource_name, campaign.name FROM campaign_asset
            WHERE campaign_asset.field_type = 'SITELINK' AND campaign_asset.status = 'ENABLED' AND campaign.name IN ('{BRANDED}','{YOUTUBE}')""")]
old_ag = [r["adGroupAsset"]["resourceName"] if "adGroupAsset" in r else r["ad_group_asset"]["resource_name"]
          for r in run_query(CID, """SELECT ad_group_asset.resource_name, ad_group.name FROM ad_group_asset
            WHERE ad_group_asset.field_type = 'SITELINK' AND ad_group_asset.status = 'ENABLED' AND ad_group.name = 'AC-Repair'""")]
print("old campaign links:", len(old_c), "| old AC-Repair ad-group links:", len(old_ag))

# 2) unlink old (link removal only; assets stay)
cas = client.get_service("CampaignAssetService"); agas = client.get_service("AdGroupAssetService")
ops = []
for rn in old_c:
    op = client.get_type("CampaignAssetOperation"); op.remove = rn; ops.append(op)
if ops: print("removed campaign links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
ops = []
for rn in old_ag:
    op = client.get_type("AdGroupAssetOperation"); op.remove = rn; ops.append(op)
if ops: print("removed ad-group links:", len(agas.mutate_ad_group_assets(customer_id=CID, operations=ops).results))
time.sleep(2)

# 3) create the 3 assets once, link to both campaigns
asvc = client.get_service("AssetService"); ops = []
for text, url, d1, d2 in NEW:
    assert len(text) <= 25 and len(d1) <= 35 and len(d2) <= 35, text
    op = client.get_type("AssetOperation"); a = op.create
    a.sitelink_asset.link_text = text; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    a.final_urls.append(url); ops.append(op)
assets = [r.resource_name for r in asvc.mutate_assets(customer_id=CID, operations=ops).results]
print("created assets:", assets)
ops = []
for cname in (BRANDED, YOUTUBE):
    for arn in assets:
        op = client.get_type("CampaignAssetOperation"); l = op.create
        l.campaign = ga.campaign_path(CID, camp_ids[cname]); l.asset = arn
        l.field_type = client.enums.AssetFieldTypeEnum.SITELINK; ops.append(op)
print("new links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
