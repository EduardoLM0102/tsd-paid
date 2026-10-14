import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "1219885876"
q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
       campaign_budget.amount_micros, campaign_budget.period
FROM campaign WHERE campaign.status != 'REMOVED'
"""
for r in run_query(CID, q):
    print(r["campaign"], r.get("campaign_budget"))
q = """
SELECT segments.week, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM customer WHERE segments.date BETWEEN '2026-07-06' AND '2026-10-07'
"""
for r in sorted(run_query(CID, q), key=lambda r: r["segments"]["week"]):
    m = r["metrics"]
    print(f"  wk {r['segments']['week']} ${int(m.get('cost_micros',0))/1e6:8.2f} clk={m.get('clicks',0):>4} imp={m.get('impressions',0):>5} conv={float(m.get('conversions',0)):4.1f}")
q = """
SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
       change_event.changed_fields, change_event.client_type, change_event.old_resource, change_event.new_resource
FROM change_event WHERE change_event.change_date_time >= '2026-09-09' AND change_event.change_date_time <= '2026-10-08 23:59:59'
ORDER BY change_event.change_date_time DESC LIMIT 50
"""
try:
    for r in run_query(CID, q):
        ce = r["change_event"]
        print(f"  {ce['change_date_time']} {ce.get('user_email','?')} {ce['change_resource_type']} {ce.get('client_type','')} fields={ce.get('changed_fields','')}")
        print(f"     old={str(ce.get('old_resource',''))[:250]}\n     new={str(ce.get('new_resource',''))[:250]}")
except Exception as e:
    print("change_event failed:", str(e)[:300])
