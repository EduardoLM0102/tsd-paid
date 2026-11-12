"""Zen Air LSA (3740502923): is the stored $12 target CPL still there / any change since 10-14? Read-only."""
import json
from datetime import date, timedelta
from lib import run_query

CID = "3740502923"

print("=== 1. Campaign bidding state ===")
q1 = """
SELECT campaign.id, campaign.name, campaign.status,
  campaign.bidding_strategy_type,
  campaign.bidding_strategy_system_status,
  campaign.maximize_conversions.target_cpa_micros,
  campaign.local_services_campaign_settings.category_bids,
  campaign_budget.amount_micros
FROM campaign
WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES'
"""
for row in run_query(CID, q1):
    print(json.dumps(row, indent=2))

print("=== 2. change_event last 29 days ===")
start = (date.today() - timedelta(days=29)).isoformat()
end = date.today().isoformat()
q2 = f"""
SELECT change_event.change_date_time, change_event.user_email,
  change_event.client_type, change_event.change_resource_type,
  change_event.changed_fields, change_event.resource_change_operation
FROM change_event
WHERE change_event.change_date_time BETWEEN '{start}' AND '{end}'
LIMIT 50
"""
rows = run_query(CID, q2)
if not rows:
    print(f"(no change events {start}..{end})")
for row in rows:
    print(json.dumps(row))

print("=== 3. Daily spend/impr/charged-leads Oct 1-18 ===")
q3 = """
SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '2026-10-01' AND '2026-10-18'
ORDER BY segments.date
"""
tot_cost = 0.0
for row in run_query(CID, q3):
    m = row.get("metrics", {})
    cost = int(m.get("cost_micros", 0)) / 1e6
    tot_cost += cost
    print(f"{row['segments']['date']}  cost ${cost:.2f}  impr {m.get('impressions', 0)}  conv(charged) {m.get('conversions', 0)}")
print(f"TOTAL Oct 1-18 cost ${tot_cost:.2f}")

print("=== 4. Leads since 10-14 ===")
q4 = """
SELECT local_services_lead.id, local_services_lead.creation_date_time,
  local_services_lead.lead_type, local_services_lead.lead_status,
  local_services_lead.lead_charged
FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '2026-10-14 00:00:00'
"""
rows = run_query(CID, q4)
if not rows:
    print("(no leads since 10-14)")
for row in rows:
    print(json.dumps(row))
