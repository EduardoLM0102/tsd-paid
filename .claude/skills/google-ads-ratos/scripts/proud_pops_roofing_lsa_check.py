"""Legacy Problem Solvers roofing LSA account 3477779749: what is running and spending (read-only)."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID = "3477779749"
f = lambda x: float(x or 0)
for r in run_query(CID, "SELECT customer.descriptive_name, customer.status, customer.time_zone FROM customer"):
    print("ACCOUNT:", r["customer"])
for r in run_query(CID, """SELECT campaign.id, campaign.name, campaign.status, campaign.serving_status, campaign.primary_status,
campaign.primary_status_reasons, campaign.advertising_channel_type, campaign_budget.amount_micros FROM campaign"""):
    c = r["campaign"]; print("CAMPAIGN:", c["id"], c["name"], c.get("advertising_channel_type"), c.get("status"), c.get("serving_status"),
                             c.get("primary_status"), c.get("primary_status_reasons"), "budget $", f(r.get("campaign_budget", {}).get("amount_micros")) / 1e6)
m = defaultdict(lambda: [0.0, 0.0, 0.0])
for r in run_query(CID, "SELECT segments.month, metrics.impressions, metrics.clicks, metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2025-01-01' AND '2026-10-08'"):
    x = m[r["segments"]["month"]]; x[0] += f(r["metrics"].get("impressions")); x[1] += f(r["metrics"].get("clicks")); x[2] += f(r["metrics"].get("cost_micros")) / 1e6
print("MONTHLY (impr / clicks / cost):")
for k in sorted(m):
    if any(m[k]): print(f"   {k[:7]}  {m[k][0]:6.0f} {m[k][1]:4.0f}  ${m[k][2]:,.2f}")
leads = run_query(CID, """SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status,
local_services_lead.lead_charged, local_services_lead.category_id FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '2025-01-01 00:00:00'""")
print(f"LEADS since 2025: {len(leads)}")
for r in sorted(leads, key=lambda r: r["local_services_lead"]["creation_date_time"])[-15:]:
    l = r["local_services_lead"]; print("   ", l["creation_date_time"][:16], l.get("lead_type"), l.get("lead_status"), "charged" if l.get("lead_charged") else "not charged", l.get("category_id"))
