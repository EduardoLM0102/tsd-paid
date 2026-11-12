# APPLIED LIVE 2026-10-28 (read-back cap $10.00). Re-running aborts (guard expects $8).
# Spencer Air (2524618054), 2026-10-28, fu-100, Edu: "Raise the cap yes". Branded 23822436393 Target IS cap $8 -> $10.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>  (validate-only without --apply)
import sys; sys.path.insert(0, ".")
from lib import init_client
CID, BR, OLD, NEW = "2524618054", "23822436393", 8.0, 10.0
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
r = q(f"SELECT campaign.bidding_strategy_type, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros FROM campaign WHERE campaign.id = {BR}")[0]
cur = r.campaign.target_impression_share.cpc_bid_ceiling_micros / 1e6
print(f"before: {r.campaign.bidding_strategy_type.name} cap ${cur:.2f} {r.campaign.target_impression_share.location.name} {r.campaign.target_impression_share.location_fraction_micros/1e4:.0f}%")
if r.campaign.bidding_strategy_type.name != "TARGET_IMPRESSION_SHARE" or abs(cur - OLD) > 0.01: sys.exit("ABORT: not as expected")
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, BR)
op.update.target_impression_share.cpc_bid_ceiling_micros = int(NEW * 1e6)
op.update_mask.paths.append("target_impression_share.cpc_bid_ceiling_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    r = q(f"SELECT campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location_fraction_micros, campaign.primary_status FROM campaign WHERE campaign.id = {BR}")[0]
    print(f"read-back: cap ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.2f} target {r.campaign.target_impression_share.location_fraction_micros/1e4:.0f}% {r.campaign.primary_status.name}")
