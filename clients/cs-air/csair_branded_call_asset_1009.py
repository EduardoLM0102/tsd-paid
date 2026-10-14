# ALREADY APPLIED LIVE 2026-10-09. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-09. Edu: "go for it on #1". Branded 23653583753 call asset: main line (817) 477-2665
(asset 339651005960, bypasses CallRail) -> CallRail Google Ads tracker 817-442-6949 (asset 343525874146, forwards to the
same main line). Same number the new PMax and Nonbranded use. One atomic batch: link new, remove old.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, OLD, NEW = "5563867754", "23653583753", "339651005960", "343525874146"
APPLY = "--apply" in sys.argv
client = init_client()
ga = client.get_service("GoogleAdsService")

for r in ga.search(customer_id=CID, query=f"""SELECT campaign.id, ad_group.name, ad_group_asset.asset FROM ad_group_asset
        WHERE campaign.id = {BR} AND ad_group_asset.field_type = 'CALL' AND ad_group_asset.status = 'ENABLED'"""):
    print("   note: ad-group-level call asset", r.ad_group.name, r.ad_group_asset.asset)

ops = []
m = client.get_type("MutateOperation")
m.campaign_asset_operation.create.campaign = ga.campaign_path(CID, BR)
m.campaign_asset_operation.create.asset = ga.asset_path(CID, NEW)
m.campaign_asset_operation.create.field_type = client.enums.AssetFieldTypeEnum.CALL
ops.append(m)
m = client.get_type("MutateOperation")
m.campaign_asset_operation.remove = f"customers/{CID}/campaignAssets/{BR}~{OLD}~CALL"
ops.append(m)

ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"batch of {len(ops)} ops: {'APPLIED' if APPLY else 'validate_only OK'}")
for r in ga.search(customer_id=CID, query=f"""SELECT campaign.id, campaign.name, campaign.status, asset.call_asset.phone_number, campaign_asset.status
        FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' AND campaign_asset.status = 'ENABLED' AND campaign.status = 'ENABLED'"""):
    print(f"   {r.campaign.name[:42]:42s} call asset {r.asset.call_asset.phone_number}")
