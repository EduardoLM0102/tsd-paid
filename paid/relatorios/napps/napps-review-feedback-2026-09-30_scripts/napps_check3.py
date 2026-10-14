import os
import sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="9509605037"
q="""SELECT call_view.start_call_date_time, call_view.call_status, call_view.call_duration_seconds, campaign.name
FROM call_view WHERE call_view.start_call_date_time >= '2026-03-24 00:00:00' AND call_view.start_call_date_time <= '2026-09-23 23:59:59'"""
rows=list(run_query(CID,q))
def d(r): return int(r['call_view'].get('call_duration_seconds') or 0)
grp=defaultdict(list)
for r in rows:
    n=r['campaign']['name']; grp['PMAX' if 'PMAX' in n else 'SEARCH'].append(r)
for k,v in grp.items():
    ds=sorted(d(r) for r in v)
    print(k, "calls",len(v),"missed",sum(1 for r in v if r['call_view']['call_status']=='MISSED'),
      "0s",sum(1 for x in ds if x==0),"<30s",sum(1 for x in ds if x<30),">=60s",sum(1 for x in ds if x>=60),"median",ds[len(ds)//2])
p=[r for r in grp['PMAX']]
bym=defaultdict(lambda:[0,0])
for r in p:
    m=r['call_view']['start_call_date_time'][:7]; bym[m][0]+=1; bym[m][1]+= d(r)>=60
print("PMax by month (calls, >=60s):",sorted((k,tuple(v)) for k,v in bym.items()))
