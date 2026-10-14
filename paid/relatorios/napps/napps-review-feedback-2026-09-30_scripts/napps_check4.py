import os
import sys
from collections import defaultdict
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="9509605037"
for lo,hi in [("2025-03-24","2025-09-23"),("2026-03-24","2026-09-23")]:
    q=f"""SELECT call_view.call_status, call_view.call_duration_seconds, campaign.name FROM call_view
    WHERE call_view.start_call_date_time >= '{lo} 00:00:00' AND call_view.start_call_date_time <= '{hi} 23:59:59'"""
    t=defaultdict(lambda:[0,0,0])
    for r in run_query(CID,q):
        n=r['campaign']['name']
        if 'PMAX' in n: continue
        d=int(r['call_view'].get('call_duration_seconds') or 0)
        t[n][0]+=1; t[n][1]+= r['call_view']['call_status']!='MISSED'; t[n][2]+= d>=60
    print(lo[:4],"(calls, connected, >=60s)")
    for n,v in sorted(t.items(), key=lambda x:-x[1][0]): print(f"  {n:45s} {v}")
