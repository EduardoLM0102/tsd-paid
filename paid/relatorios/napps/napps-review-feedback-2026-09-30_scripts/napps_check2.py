import os
import sys
from collections import Counter
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="9509605037"
q="""SELECT call_view.start_call_date_time, call_view.call_status, call_view.call_duration_seconds, campaign.name, call_view.resource_name
FROM call_view WHERE call_view.start_call_date_time >= '2026-03-24 00:00:00'"""
rows=list(run_query(CID,q))
print("rows",len(rows),"unique resource names",len({r['call_view']['resource_name'] for r in rows}))
print("by month:",sorted(Counter(r['call_view']['start_call_date_time'][:7] for r in rows).items()))
print("by campaign:",Counter(r.get('campaign',{}).get('name') for r in rows).most_common())
m=[r for r in rows if r['call_view']['call_status']=='MISSED']
print("missed by month:",sorted(Counter(r['call_view']['start_call_date_time'][:7] for r in m).items()))
print("missed by campaign:",Counter(r.get('campaign',{}).get('name') for r in m).most_common())
w=[r for r in rows if r['call_view']['start_call_date_time']<='2026-09-23 23:59:59']
print("window to 09-23:",len(w),"missed",sum(1 for r in w if r['call_view']['call_status']=='MISSED'))
