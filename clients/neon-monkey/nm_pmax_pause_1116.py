# fu-115 checkpoint 2026-11-16: pause TSD_04.25_PMAX_Evergreen 21225221220.
# Rule set 11-02 (Edu's go): keep PMax only if Nov 2-15 brings >= 3 real transcribed calls at <= ~$200/lead. Otherwise pause, run Branded + LSA.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
import sys; sys.path.insert(0, ".")
from lib import init_client
CID, P = "7953905280", "21225221220"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
st = lambda: list(ga.search(customer_id=CID, query=f"SELECT campaign.name, campaign.status, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {P}"))[0]
c = st(); print("before:", c.campaign.name, c.campaign.status.name, f"${c.campaign_budget.amount_micros/1e6:.0f}/d")
if c.campaign.status.name != "ENABLED": sys.exit("ABORT: campaign not ENABLED")
op = client.get_type("MutateOperation")
op.campaign_operation.update.resource_name = ga.campaign_path(CID, P)
op.campaign_operation.update.status = client.enums.CampaignStatusEnum.PAUSED
op.campaign_operation.update_mask.paths.append("status")
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.validate_only = not APPLY; req.mutate_operations.append(op)
ga.mutate(request=req)
print("pause PMax:", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY: print("read-back:", st().campaign.status.name)
