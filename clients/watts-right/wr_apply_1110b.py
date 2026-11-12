# APPLIED LIVE 2026-11-10 09:14 -03, read-back 145.0. Do NOT re-run with --apply.
# Watt's Right 2026-11-10 correction: Branded $95 -> $145 (= $50 + PMax's full $95, Edu: "Move the $95 from pmax to branded"; 09:13 apply set $95 by mistake).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>  (validate-only without --apply)
import sys
sys.path.insert(0, ".")
from lib import init_client
CID, BR, OLD, NEW = "3651667805", "23690645223", 95.0, 145.0
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
r = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location,
    campaign.target_impression_share.location_fraction_micros, campaign_budget.resource_name, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared, campaign_budget.reference_count FROM campaign WHERE campaign.id = {BR}""")[0]
cur = r.campaign_budget.amount_micros / 1e6
print(f"bidding {r.campaign.bidding_strategy_type.name} ceiling ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.2f} "
      f"{r.campaign.target_impression_share.location.name} {r.campaign.target_impression_share.location_fraction_micros/1e4:.0f}% | budget ${cur:.2f} -> ${NEW:.2f}")
if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1 or abs(cur - OLD) > 0.01: sys.exit("ABORT")
op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = r.campaign_budget.resource_name
op.update.amount_micros = int(NEW * 1e6); op.update_mask.paths.append("amount_micros")
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY: print("READ-BACK:", q(f"SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = {BR}")[0].campaign_budget.amount_micros / 1e6)
