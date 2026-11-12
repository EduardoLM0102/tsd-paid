# READ-ONLY. Napps 11-10: location targeting on NB campaigns + which enabled campaigns bid on conversions + Click to call 90d volume.
import sys
sys.path.insert(0, ".")
from lib import run_query
q = lambda s: run_query("9509605037", s)
for r in q("""SELECT campaign.id, campaign.name, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant,
  campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units, campaign_criterion.proximity.address.city_name,
  campaign.geo_target_type_setting.positive_geo_target_type FROM campaign_criterion
  WHERE campaign.id IN (24049055193,23819717682,23685615826) AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"""):
    print(r["campaign"]["name"][:40], r["campaign"].get("geo_target_type_setting"), r["campaign_criterion"])
for r in q("SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.bidding_strategy_type FROM campaign WHERE campaign.status = 'ENABLED'"):
    print("enabled:", r["campaign"])
for r in q("""SELECT segments.conversion_action_name, campaign.name, metrics.all_conversions, metrics.conversions FROM campaign
  WHERE segments.date DURING LAST_90_DAYS AND segments.conversion_action_name = 'Click to call' AND metrics.all_conversions > 0"""):
    print("tap90d:", r["campaign"]["name"], r["metrics"])
