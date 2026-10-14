import sys
sys.path.insert(0, ".")
from lib import run_query
LSA = "3740502923"
for r in run_query(LSA, """SELECT campaign.id, campaign_budget.amount_micros, campaign_budget.period, campaign.bidding_strategy_type FROM campaign"""):
    print("budget", r.get("campaign_budget"), r["campaign"].get("bidding_strategy_type"))
q = """SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.category_id,
       local_services_lead.service_id, local_services_lead.lead_status, local_services_lead.lead_charged
FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-06-01 00:00:00'
ORDER BY local_services_lead.creation_date_time"""
for r in run_query(LSA, q):
    l = r["local_services_lead"]
    print(f"  {l.get('creation_date_time','')[:16]} {l.get('lead_type','')[:8]:8s} {l.get('service_id','')[:30]:30s} {l.get('lead_status','')[:12]:12s} charged={l.get('lead_charged')}")
for r in run_query(LSA, """SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-09-10' AND '2026-09-29' AND metrics.impressions > 0"""):
    m = r["metrics"]
    print(f"  {r['segments']['date']} cost=${int(m.get('cost_micros',0))/1e6:.2f} imp={m.get('impressions')} clk={m.get('clicks')}")
