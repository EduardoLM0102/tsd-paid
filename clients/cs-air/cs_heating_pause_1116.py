# fu-141 decision 2026-11-16: pause TSD_10.23_Search_Nonbranded_Heating (24383234148).
# Heating Repair alone 11-10..11-15: $123.62 / 16 clicks / 0 leads; since 10-27: 35 Repair clicks, 0 leads (rule set 11-09: still 0 -> pause).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
import sys; sys.path.insert(0, ".")
from lib import init_client
CID, H = "5563867754", "24383234148"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
st = lambda: list(ga.search(customer_id=CID, query=f"SELECT campaign.name, campaign.status FROM campaign WHERE campaign.id = {H}"))[0].campaign
c = st(); print("before:", c.name, c.status.name)
if c.status.name != "ENABLED": sys.exit("ABORT: campaign not ENABLED")
op = client.get_type("MutateOperation")
op.campaign_operation.update.resource_name = ga.campaign_path(CID, H)
op.campaign_operation.update.status = client.enums.CampaignStatusEnum.PAUSED
op.campaign_operation.update_mask.paths.append("status")
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.validate_only = not APPLY; req.mutate_operations.append(op)
ga.mutate(request=req)
print("pause Heating:", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY: print("read-back:", st().status.name)
