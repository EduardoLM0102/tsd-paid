from h import *
from collections import defaultdict
# current config of enabled campaigns
q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type,
       campaign.maximize_conversions.target_cpa_micros, campaign.target_cpa.target_cpa_micros,
       campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
       campaign.network_settings.target_google_search, campaign.network_settings.target_partner_search_network,
       campaign_budget.amount_micros, campaign_budget.name, campaign.geo_target_type_setting.positive_geo_target_type
FROM campaign
WHERE campaign.status IN ('ENABLED')
"""
for r in run_query(CID,q):
    print(json.dumps(r, default=str))
print("\n=== change events last 30d (all resource types) ===")
import datetime
q2 = """
SELECT change_event.change_date_time, change_event.user_email, change_event.client_type, change_event.change_resource_type,
       change_event.resource_change_operation, change_event.changed_fields, change_event.campaign, change_event.ad_group
FROM change_event
WHERE change_event.change_date_time >= '2026-08-24 00:00:00' AND change_event.change_date_time <= '2026-09-24 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 10000
"""
rows=list(run_query(CID,q2))
json.dump(rows, open(OUT+"change_events.json","w"), default=str)
print(len(rows))
