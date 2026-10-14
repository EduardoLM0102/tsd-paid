"""Cool Hand 2026-10-10 (Edu's go): call asset number 469-550-1102 (main line) -> 469-351-1738 (CallRail, same number as the go. pages).
ALREADY APPLIED 2026-10-10, don't re-run.
Creates a new call asset (same settings: US, account-level call conversion action, no schedule), links it to the 3 Search
campaigns, then unlinks old asset 415288389635. Old asset is kept (unlinked), so rollback = relink it.
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys, time
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client

CID = "9865206319"
OLD_ASSET = "415288389635"
NEW_NUMBER = "4693511738"
CAMPAIGNS = ("TSD_Search_HVAC", "TSD_Search_Electrical", "TSD_Search_Branded")

c = init_client(); ga = c.get_service("GoogleAdsService")
def q(s): return list(ga.search(customer_id=CID, query=s))
names = "','".join(CAMPAIGNS)
camp = {r.campaign.name: r.campaign.id for r in q(f"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name IN ('{names}')")}
old_links = [r.campaign_asset.resource_name for r in q(f"""SELECT campaign_asset.resource_name, campaign.name FROM campaign_asset
  WHERE campaign_asset.field_type='CALL' AND campaign_asset.status='ENABLED' AND asset.id = {OLD_ASSET} AND campaign.name IN ('{names}')""")]
print("old links:", len(old_links))

# 1) new call asset, same settings as the old one
op = c.get_type("AssetOperation"); a = op.create
a.name = "Cool Hand CallRail 469-351-1738"
a.call_asset.country_code = "US"
a.call_asset.phone_number = NEW_NUMBER
a.call_asset.call_conversion_reporting_state = c.enums.CallConversionReportingStateEnum.USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION
new_rn = c.get_service("AssetService").mutate_assets(customer_id=CID, operations=[op]).results[0].resource_name
print("created:", new_rn)

# 2) link new first, so the campaigns are never without a call asset
cas = c.get_service("CampaignAssetService"); ops = []
for cname in CAMPAIGNS:
    op = c.get_type("CampaignAssetOperation"); l = op.create
    l.campaign = ga.campaign_path(CID, camp[cname]); l.asset = new_rn
    l.field_type = c.enums.AssetFieldTypeEnum.CALL; ops.append(op)
print("new links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
time.sleep(2)

# 3) unlink old
ops = []
for rn in old_links:
    op = c.get_type("CampaignAssetOperation"); op.remove = rn; ops.append(op)
print("old unlinked:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
