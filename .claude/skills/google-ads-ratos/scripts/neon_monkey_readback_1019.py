"""Read-only read-back after the 10-19 Neon Monkey changes."""
from lib import run_query
cid = "7953905280"
for r in run_query(cid, "SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.status='ENABLED'"):
    c = r["campaign"]; print(c["name"], c.get("bidding_strategy_type"), c.get("target_spend"), c.get("geo_target_type_setting", {}).get("positive_geo_target_type"))
for r in run_query(cid, "SELECT ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id=23739724064 AND ad_group.status='ENABLED'"):
    print("Branded ad group max CPC", int(r["ad_group"]["cpc_bid_micros"])/1e6)
for r in run_query(cid, "SELECT conversion_action.name, conversion_action.category, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.id=7835384828"):
    print(r["conversion_action"])
