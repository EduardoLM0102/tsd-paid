"""Are any legacy Problem Solvers LSA accounts still live? (read-only)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
LEGACY = {"8497583415": "PS HVAC SA 2", "5229329621": "PS HVAC SA 4", "3490305409": "PS Plumbing SA 2", "5504504691": "PS Plumbing SA 3",
          "3477779749": "PS Roofing SA", "5037427931": "PS Roofing SA 2", "4931459362": "PS Roofing SA 3"}
f = lambda x: float(x or 0)
for cid, name in LEGACY.items():
    try:
        camps = run_query(cid, "SELECT campaign.id, campaign.status, campaign.primary_status, campaign_budget.amount_micros FROM campaign WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES'")
        perf = run_query(cid, "SELECT metrics.impressions, metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-06-01' AND '2026-10-08'")
        leads = run_query(cid, "SELECT local_services_lead.id FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-06-01 00:00:00'")
    except SystemExit:
        print(f"{cid} {name:18s} unreadable"); continue
    impr = sum(f(r["metrics"].get("impressions")) for r in perf); cost = sum(f(r["metrics"].get("cost_micros")) for r in perf) / 1e6
    print(f"{cid} {name:18s} " + "; ".join(f"camp {c['campaign']['id']} {c['campaign'].get('status')}/{c['campaign'].get('primary_status')} ${f(c.get('campaign_budget',{}).get('amount_micros'))/1e6:.0f}/d" for c in camps)
          + f" | since Jun-01: {impr:.0f} impr, ${cost:,.2f}, {len(leads)} leads")
