import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import Counter, defaultdict
f = lambda x: float(x or 0)
months = [("Jun", "2026-06-01", "2026-06-30"), ("Jul", "2026-07-01", "2026-07-31"), ("Aug", "2026-08-01", "2026-08-31"), ("Sep", "2026-09-01", "2026-09-30"), ("Oct1-6", "2026-10-01", "2026-10-06")]
for cid in ("1051843378", "7261668241", "6621969129"):
    print("==", cid)
    for m, s, u in months:
        rows = run_query(cid, f"""
SELECT local_services_lead.lead_type, local_services_lead.lead_charged FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '{s} 00:00:00' AND local_services_lead.creation_date_time <= '{u} 23:59:59'""")
        calls = sum(1 for r in rows if str(r['local_services_lead'].get('lead_type')) == 'PHONE_CALL')
        charged_calls = sum(1 for r in rows if str(r['local_services_lead'].get('lead_type')) == 'PHONE_CALL' and r['local_services_lead'].get('lead_charged'))
        sp = defaultdict(float)
        for r in run_query(cid, f"SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros FROM campaign WHERE segments.date BETWEEN '{s}' AND '{u}' AND metrics.cost_micros > 0"):
            sp[str(r['campaign']['advertising_channel_type'])] += f(r['metrics'].get('cost_micros'))/1e6
        print(f"   {m:7s} leads={len(rows):3d} calls={calls:3d} charged_calls={charged_calls:3d}  spend_by_channel={ {k: round(v) for k, v in sp.items()} }")
