# APPLIED LIVE 2026-10-20, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-10-20 ("go for it"), Command Center fu-040.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
"""Spencer (2524618054) Branded 23822436393: Maximize Conversions (no target) -> Target Impression Share,
absolute top of page 95%, max CPC ceiling $8. Budget $50/d unchanged. Rollback = back to Maximize Conversions."""
import sys
sys.path.insert(0, ".")
from lib import init_client
CID, BR = "2524618054", "23822436393"
APPLY = "--apply" in sys.argv
c = init_client(); ga = c.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
r = q(f"SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {BR}")[0]
print(r.campaign.name, r.campaign.status.name, r.campaign.bidding_strategy_type.name, f"portfolio='{r.campaign.bidding_strategy}'", r.campaign_budget.amount_micros / 1e6)
if r.campaign.bidding_strategy: sys.exit("ABORT: portfolio strategy")
if r.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: unexpected current strategy")
op = c.get_type("CampaignOperation"); u = op.update
u.resource_name = ga.campaign_path(CID, BR)
u.target_impression_share.location = c.enums.TargetImpressionShareLocationEnum.ABSOLUTE_TOP_OF_PAGE
u.target_impression_share.location_fraction_micros = 950000
u.target_impression_share.cpc_bid_ceiling_micros = 8_000_000
op.update_mask.paths.extend(["target_impression_share.location", "target_impression_share.location_fraction_micros",
                             "target_impression_share.cpc_bid_ceiling_micros"])
c.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("OK", "(validate_only)" if not APPLY else "APPLIED")
if APPLY:
    r = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros,
        campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id = {BR}""")[0]
    t = r.campaign.target_impression_share
    print("read-back:", r.campaign.bidding_strategy_type.name, t.location.name, t.location_fraction_micros / 1e4, "%", "ceiling $", t.cpc_bid_ceiling_micros / 1e6,
          "budget $", r.campaign_budget.amount_micros / 1e6, r.campaign.primary_status.name)
