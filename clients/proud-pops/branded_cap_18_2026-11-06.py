# APPLIED LIVE 2026-11-06, read-back confirmed (Target IS 95% abs-top, ceiling $18, budget $130). Do NOT re-run with --apply.
# Edu's go 2026-11-06 ("Let's move the max click and maintain tImp Share").
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
"""Proud Pops (1051843378) Branded 23853361615: Target IS max CPC ceiling $10 -> $18.
Strategy stays Target Impression Share, absolute top 95%. Budget $130/d unchanged.
Why: since the 11-04 switch Branded served 2 impressions and 0 on 11-05; brand CPC before the switch was $11.78-17.55.
Rollback = ceiling back to $10."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR = "1051843378", "23853361615"
NEW_CEILING = 18_000_000
APPLY = "--apply" in sys.argv
c = init_client(); ga = c.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.target_impression_share.location,
    campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
    campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id = {BR}"""

def show(tag):
    r = q(SEL)[0]; t = r.campaign.target_impression_share
    print(tag, r.campaign.name, r.campaign.bidding_strategy_type.name, t.location.name, t.location_fraction_micros / 1e4, "%",
          "ceiling $", t.cpc_bid_ceiling_micros / 1e6, "budget $", r.campaign_budget.amount_micros / 1e6, r.campaign.primary_status.name)
    return r

r = show("before:")
if r.campaign.bidding_strategy: sys.exit("ABORT: portfolio strategy")
if r.campaign.bidding_strategy_type.name != "TARGET_IMPRESSION_SHARE": sys.exit("ABORT: not Target IS")
if r.campaign.target_impression_share.cpc_bid_ceiling_micros != 10_000_000: sys.exit("ABORT: ceiling is not $10, someone changed it")

op = c.get_type("CampaignOperation"); u = op.update
u.resource_name = ga.campaign_path(CID, BR)
u.target_impression_share.cpc_bid_ceiling_micros = NEW_CEILING
op.update_mask.paths.append("target_impression_share.cpc_bid_ceiling_micros")
c.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("ceiling $10 -> $18", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY: show("read-back:")
