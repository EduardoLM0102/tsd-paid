# READ-ONLY: detail on outside-party / unexplained changes
import os
import sys, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
def detail(cid, label, extra=""):
    print(f"\n===== {label} {cid}")
    camps = {r["campaign"]["resource_name"]: (r["campaign"]["name"], r["campaign"]["status"]) for r in run_query(cid, "SELECT campaign.resource_name, campaign.name, campaign.status FROM campaign")}
    rows = run_query(cid, f"""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
        change_event.resource_change_operation, change_event.changed_fields, change_event.campaign
        FROM change_event WHERE change_event.change_date_time >= '2026-09-09' AND change_event.change_date_time <= '2026-10-08 23:59:59' {extra}
        ORDER BY change_event.change_date_time DESC LIMIT 10000""")
    agg = collections.Counter()
    for r in rows:
        e = r["change_event"]
        cn = camps.get(e.get("campaign"), ("-",""))[0]
        agg[(e["change_date_time"][:10], e.get("user_email","")[:30], e["change_resource_type"], e["resource_change_operation"], str(e.get("changed_fields",""))[:70], cn[:45])] += 1
    for k, v in sorted(agg.items(), reverse=True)[:40]: print(v, k)
    print("CAMPAIGNS:", [(n, s) for n, s in camps.values() if s != "REMOVED"])
detail("1056617442", "Live Wire")
detail("9049508615", "Strickland")
detail("9865206319", "Cool Hand")
detail("2375064049", "GC PPC")
detail("2974002658", "GC LSA")
detail("1854100356", "Nick's")
