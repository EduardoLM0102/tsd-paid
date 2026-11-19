# READ-ONLY. ./tsd.sh <abs path>. Neon Monkey LSA 1219885876 reach check (fu-173, 'no' branch: Meta off until video, no holiday lights)
import sys; sys.path.insert(0, ".")
from lib import run_query
CID = "1219885876"
M = lambda x: int(x or 0) / 1e6
for r in run_query(CID, "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros, campaign_budget.period FROM campaign WHERE campaign.status != 'REMOVED'"):
    print("CAMP", r["campaign"]["id"], r["campaign"]["name"][:50], r["campaign"]["status"], r["campaign"]["advertising_channel_type"], M(r["campaign_budget"].get("amount_micros")), r["campaign_budget"].get("period"))
print("== daily 10-20..11-18")
wk = {}
for r in run_query(CID, "SELECT segments.date, segments.day_of_week, metrics.cost_micros, metrics.impressions, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-18' ORDER BY segments.date"):
    d = r["segments"]["date"]; m = r["metrics"]
    print(f"  {d} {r['segments']['day_of_week'][:3]} ${M(m.get('cost_micros')):6.2f} impr {m.get('impressions',0):>4} clk {m.get('clicks',0)}")
print("== leads 10-20..11-18")
for r in run_query(CID, "SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-10-20 00:00:00' AND local_services_lead.creation_date_time <= '2026-11-18 23:59:59'"):
    l = r["local_services_lead"]; print("  ", l["creation_date_time"][:16], l["lead_type"], l["lead_status"], "charged" if l.get("lead_charged") else "-")
print("== hourly impressions 10-20..11-18")
h = {}
for r in run_query(CID, "SELECT segments.hour, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-18'"):
    h[int(r["segments"]["hour"])] = h.get(int(r["segments"]["hour"]), 0) + int(r["metrics"].get("impressions", 0))
print("  ", dict(sorted(h.items())))
