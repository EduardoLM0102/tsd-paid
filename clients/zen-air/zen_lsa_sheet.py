"""Zen Air LSA daily rollup for the AgencyAnalytics Google Sheet.

AgencyAnalytics' native LSA connector has no booked/declined status and its lead
widgets undercount (most Zen Air LSA leads are not charged), so this writes the
real numbers by day: all leads, booked, declined, not yet marked, charged, free, spend.

Run from google-ads-ratos/scripts:
  ./tsd.sh /abs/path/zen_lsa_sheet.py <out.csv> [start YYYY-MM-DD] [end YYYY-MM-DD]
Read-only against Google Ads (LSA account 3740502923).
"""
import csv, sys, collections
from datetime import date, timedelta
sys.path.insert(0, ".")
from lib import run_query

CID = "3740502923"
out = sys.argv[1]
start = sys.argv[2] if len(sys.argv) > 2 else "2026-01-01"
end = sys.argv[3] if len(sys.argv) > 3 else date.today().isoformat()

days = collections.defaultdict(collections.Counter)
for r in run_query(CID, f"""SELECT local_services_lead.creation_date_time, local_services_lead.lead_status,
 local_services_lead.lead_charged FROM local_services_lead
 WHERE local_services_lead.creation_date_time >= '{start} 00:00:00' AND local_services_lead.creation_date_time <= '{end} 23:59:59'"""):
    l = r["local_services_lead"]; d = l["creation_date_time"][:10]; st = l.get("lead_status")
    c = days[d]; c["leads"] += 1
    c["booked"] += st == "BOOKED"
    c["declined"] += st == "DECLINED"
    c["open"] += st not in ("BOOKED", "DECLINED")
    c["charged"] += bool(l.get("lead_charged"))
    c["free"] += not l.get("lead_charged")
spend = collections.Counter()
for r in run_query(CID, f"""SELECT segments.date, metrics.cost_micros FROM campaign
 WHERE segments.date BETWEEN '{start}' AND '{end}' AND campaign.advertising_channel_type = 'LOCAL_SERVICES'"""):
    spend[r["segments"]["date"]] += int(r["metrics"]["cost_micros"]) / 1e6

with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "LSA Leads", "LSA Booked", "LSA Declined", "LSA Not Marked", "LSA Charged Leads", "LSA Free Leads", "LSA Spend"])
    d0, d1 = date.fromisoformat(start), date.fromisoformat(end)
    while d0 <= d1:
        k = d0.isoformat(); c = days.get(k, collections.Counter())
        w.writerow([k, c["leads"], c["booked"], c["declined"], c["open"], c["charged"], c["free"], f"{spend.get(k, 0):.2f}"])
        d0 += timedelta(days=1)
tot = collections.Counter()
for c in days.values(): tot.update(c)
print("totals", dict(tot), "spend", round(sum(spend.values()), 2))
