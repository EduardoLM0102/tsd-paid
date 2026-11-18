# APPLIED LIVE 2026-11-17 09:44 -03, read-back Heating Tyler modifier 0.5, Plumbing untouched. Do NOT re-run with --apply.
# Napps (9509605037), 2026-11-17. Edu's go in-session ("yes please") on the fu-144 second look.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
"""Tyler (geo 1026855) location bid adjustment -50% on NB Heating 24049055193 ONLY (ad + page say "Longview"; Tyler = 23 clk / $462 / 0 calls since 10-27).
Plumbing 23819717682 untouched (its only conversion, the 11-14 form, came from Tyler; verify first). Budgets $65/$35 and the $25 Max Clicks cap untouched.
Aborts if Tyler isn't a targeted location on Heating, already has a modifier, or the campaign isn't ENABLED Max Clicks."""
import sys
sys.path.insert(0, ".")
from lib import init_client
CID, HT, PL, TYLER = "9509605037", "24049055193", "23819717682", "1026855"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
c = q(f"SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {HT}")[0]
print(f"{c.campaign.name}: {c.campaign.status.name} {c.campaign.bidding_strategy_type.name} cap ${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} bud ${c.campaign_budget.amount_micros/1e6:.0f}")
if c.campaign.status.name != "ENABLED" or c.campaign.bidding_strategy_type.name != "TARGET_SPEND": sys.exit("ABORT: unexpected campaign state")
rows = q(f"""SELECT campaign_criterion.resource_name, campaign_criterion.bid_modifier, campaign_criterion.negative, campaign_criterion.location.geo_target_constant
    FROM campaign_criterion WHERE campaign.id = {HT} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.location.geo_target_constant = 'geoTargetConstants/{TYLER}'""")
if len(rows) != 1 or rows[0].campaign_criterion.negative: sys.exit(f"ABORT: Tyler criterion on Heating: {len(rows)} rows")
cur = rows[0].campaign_criterion.bid_modifier
print(f"Tyler on Heating: {rows[0].campaign_criterion.resource_name} current modifier {cur if cur else 'none (1.0)'} -> 0.5 (-50%)")
if cur and abs(cur - 1.0) > 0.001: sys.exit("ABORT: a modifier already exists")
op = client.get_type("CampaignCriterionOperation"); op.update.resource_name = rows[0].campaign_criterion.resource_name
op.update.bid_modifier = 0.5; op.update_mask.paths.append("bid_modifier")
client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    print("READ-BACK:")
    for r in q(f"""SELECT campaign.id, campaign_criterion.location.geo_target_constant, campaign_criterion.bid_modifier FROM campaign_criterion
        WHERE campaign.id IN ({HT},{PL}) AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.location.geo_target_constant = 'geoTargetConstants/{TYLER}'"""):
        print(f"   campaign {r.campaign.id} Tyler modifier = {r.campaign_criterion.bid_modifier}")
