"""Read-only: pre-change state for Neon Monkey 10-19 (Branded ad groups/keyword bids, PMax geo setting, NB bidding)."""
from lib import run_query
cid = "7953905280"
for r in run_query(cid, """SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, campaign.geo_target_type_setting.positive_geo_target_type,
  campaign.geo_target_type_setting.negative_geo_target_type, campaign.network_settings.target_search_network FROM campaign WHERE campaign.status='ENABLED'"""):
    c = r["campaign"]; print(c["id"], c["name"], c.get("bidding_strategy_type"), c.get("geo_target_type_setting"))
print("\nBranded ad groups")
for r in run_query(cid, """SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id=23739724064 AND ad_group.status!='REMOVED'"""):
    a = r["ad_group"]; print(" ", a["id"], a["name"], a["status"], int(a.get("cpc_bid_micros", 0))/1e6)
print("Branded keywords (bids)")
for r in run_query(cid, """SELECT ad_group.id, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.cpc_bid_micros
  FROM ad_group_criterion WHERE campaign.id=23739724064 AND ad_group_criterion.type='KEYWORD' AND ad_group_criterion.negative=FALSE AND ad_group_criterion.status!='REMOVED'"""):
    k = r["ad_group_criterion"]; print(" ", r["ad_group"]["id"], k["criterion_id"], k["keyword"]["text"], k["keyword"]["match_type"], k["status"], int(k.get("cpc_bid_micros", 0))/1e6)
print("\nPMax locations")
for r in run_query(cid, """SELECT campaign_criterion.criterion_id, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units, campaign_criterion.negative, campaign_criterion.type
  FROM campaign_criterion WHERE campaign.id=21225221220 AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"""):
    k = r["campaign_criterion"]; print(" ", k["type_"] if "type_" in k else k.get("type"), k.get("negative"), k.get("location", ""), k.get("proximity", ""))
