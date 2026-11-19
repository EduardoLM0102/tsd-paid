# READ-ONLY. ./tsd.sh <abs path>. ICS LSA delivery after the 11-11 restore (fu-150): Belleville 2895702982, Englewood 8323145223, Carlstadt 2175964343.
import sys; sys.path.insert(0, ".")
from lib import run_query
M=lambda x:int(x or 0)/1e6
for cid, lab in (("2895702982","Belleville"),("8323145223","Englewood"),("2175964343","Carlstadt")):
    print(f"== {lab} {cid}")
    for r in run_query(cid,"SELECT campaign.id, campaign.status, campaign_budget.amount_micros, campaign.advertising_channel_type FROM campaign WHERE campaign.status != 'REMOVED'"):
        print("  camp", r["campaign"]["id"], r["campaign"]["status"], r["campaign"]["advertising_channel_type"], f"${M(r['campaign_budget']['amount_micros']):.2f}/d")
    for r in run_query(cid,"SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-11-08' AND '2026-11-19' AND campaign.advertising_channel_type = 'LOCAL_SERVICES' ORDER BY segments.date"):
        m=r["metrics"]; print(f"  {r['segments']['date']} ${M(m.get('cost_micros')):6.2f} impr {m.get('impressions',0):>4} clk {m.get('clicks',0)}")
    for r in run_query(cid,"SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-01 00:00:00'"):
        l=r["local_services_lead"]; print("  LEAD", l["creation_date_time"][:16], l["lead_type"][:5], l["lead_status"], "charged" if l.get("lead_charged") else "-")
