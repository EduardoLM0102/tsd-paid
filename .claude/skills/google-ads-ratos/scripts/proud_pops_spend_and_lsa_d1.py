"""Proud Pops: monthly spend across the whole client cluster + LSA weekly snapshot (checklist D1). Read-only.
Run: ./tsd.sh proud_pops_spend_and_lsa_d1.py [YYYY-MM-01 YYYY-MM-LAST]"""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
f = lambda x: float(x or 0)
S, U = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("2026-09-01", "2026-09-30")
PP = {"1051843378": "Proud Pops PPC (incl. in-account LSA)", "7261668241": "Proud Pops LSA [1] Electrician", "6621969129": "Proud Pops LSA [2] HVAC"}
LEGACY = {"8497583415": "PS HVAC SA 2", "5229329621": "PS HVAC SA 4", "3490305409": "PS Plumbing SA 2", "5504504691": "PS Plumbing SA 3",
          "3477779749": "PS Roofing SA", "5037427931": "PS Roofing SA 2", "4931459362": "PS Roofing SA 3"}
MFSC = {"9815330464": "MFSC PPC", "4127524472": "MFSC LSA New Braunfels", "4905286019": "MFSC LSA San Antonio"}

def spend(cid):
    by = defaultdict(float)
    try:
        for r in run_query(cid, f"SELECT campaign.advertising_channel_type, metrics.cost_micros FROM campaign WHERE segments.date BETWEEN '{S}' AND '{U}' AND metrics.cost_micros > 0"):
            by[str(r["campaign"]["advertising_channel_type"])] += f(r["metrics"].get("cost_micros")) / 1e6
    except SystemExit:
        return None
    return by

print(f"=== SPEND {S} .. {U}")
for title, group in (("PROUD POPS", PP), ("LEGACY Problem Solvers LSA", LEGACY), ("MY FAVORITE SERVICE CO (separate set, don't blend)", MFSC)):
    tot = 0.0
    print(f"-- {title}")
    for cid, name in group.items():
        by = spend(cid)
        if by is None:
            print(f"   {cid} {name:40s} unreadable"); continue
        t = sum(by.values()); tot += t
        if t or group is PP:
            print(f"   {cid} {name:40s} ${t:>10,.2f}  " + "  ".join(f"{k}=${v:,.0f}" for k, v in sorted(by.items(), key=lambda x: -x[1])))
    print(f"   TOTAL {title}: ${tot:,.2f}")

print("\n=== D1: LSA weekly snapshot (impressions / clicks / cost / leads), Aug 10 .. today")
for cid in PP:
    wk = defaultdict(lambda: [0.0, 0.0, 0.0, 0])
    for r in run_query(cid, """SELECT segments.week, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign
WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES' AND segments.date BETWEEN '2026-08-10' AND '2026-10-07'"""):
        w = wk[r["segments"]["week"]]; m = r["metrics"]
        w[0] += f(m.get("impressions")); w[1] += f(m.get("clicks")); w[2] += f(m.get("cost_micros")) / 1e6
    import datetime
    for r in run_query(cid, """SELECT local_services_lead.creation_date_time, local_services_lead.lead_type FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '2026-08-10 00:00:00'"""):
        d = datetime.date.fromisoformat(r["local_services_lead"]["creation_date_time"][:10])
        wk[(d - datetime.timedelta(days=d.weekday())).isoformat()][3] += 1
    print(f"-- {cid} {PP[cid]}")
    for w in sorted(wk):
        i, c, cost, leads = wk[w]
        print(f"   wk {w}: impr {i:5.0f}  clicks {c:3.0f}  ${cost:7,.0f}  leads {leads}")
