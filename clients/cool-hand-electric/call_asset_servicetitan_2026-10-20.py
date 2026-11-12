"""Cool Hand 2026-10-20 APPLIED 10-20 on Edu's go, do NOT re-run: call asset 469-351-1738 (CallRail 'Google Ads' tracker) -> 469-270-1146
(ServiceTitan PPC number Angela sent 10-12 in the group DM: "Phone numbers to be used for Cool Hands ... PPC 469-270-1146").
Same pattern as call_asset_callrail_2026-10-10.py: create new asset (US, account-level call conversion action), link it to the
3 Search campaigns first, then unlink 429092777632. Old asset is kept, so rollback = relink it.
Run: ./tsd.sh <abs path>            (validate-only: creates nothing)
     ./tsd.sh <abs path> --apply    (live)
"""
import os, sys, time
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client

CID = "9865206319"
OLD_ASSET = "429092777632"
NEW_NUMBER = "4692701146"
CAMPAIGNS = ("TSD_Search_HVAC", "TSD_Search_Electrical", "TSD_Search_Branded")
APPLY = "--apply" in sys.argv

c = init_client(); ga = c.get_service("GoogleAdsService")
def q(s): return list(ga.search(customer_id=CID, query=s))
names = "','".join(CAMPAIGNS)
camp = {r.campaign.name: r.campaign.id for r in q(f"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name IN ('{names}')")}
old_links = [r.campaign_asset.resource_name for r in q(f"""SELECT campaign_asset.resource_name, campaign.name FROM campaign_asset
  WHERE campaign_asset.field_type='CALL' AND campaign_asset.status='ENABLED' AND asset.id = {OLD_ASSET} AND campaign.name IN ('{names}')""")]
dupe = q(f"SELECT asset.id FROM asset WHERE asset.type='CALL' AND asset.call_asset.phone_number LIKE '%2701146%'")
print("campaigns:", camp, "| old links:", len(old_links), "| existing asset for new number:", [d.asset.id for d in dupe])
if len(camp) != 3 or len(old_links) != 3: sys.exit("ABORT: unexpected campaigns/links")

op = c.get_type("AssetOperation"); a = op.create
a.name = "Cool Hand ServiceTitan PPC 469-270-1146"
a.call_asset.country_code = "US"
a.call_asset.phone_number = NEW_NUMBER
a.call_asset.call_conversion_reporting_state = c.enums.CallConversionReportingStateEnum.USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION
res = c.get_service("AssetService").mutate_assets(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
if not APPLY:
    print("asset create OK (validate_only). Links not validated: they need the real asset id."); sys.exit()
new_rn = res.results[0].resource_name; print("created:", new_rn)

cas = c.get_service("CampaignAssetService"); ops = []
for cname in CAMPAIGNS:
    op = c.get_type("CampaignAssetOperation"); l = op.create
    l.campaign = ga.campaign_path(CID, camp[cname]); l.asset = new_rn; l.field_type = c.enums.AssetFieldTypeEnum.CALL; ops.append(op)
print("new links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
time.sleep(2)
ops = []
for rn in old_links:
    op = c.get_type("CampaignAssetOperation"); op.remove = rn; ops.append(op)
print("old unlinked:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
for r in q("SELECT campaign.name, asset.id, asset.call_asset.phone_number, campaign_asset.status, asset.policy_summary.approval_status FROM campaign_asset WHERE campaign_asset.field_type='CALL' AND campaign_asset.status='ENABLED'"):
    print("  ", r.campaign.name, r.asset.id, r.asset.call_asset.phone_number, r.asset.policy_summary.approval_status.name)
