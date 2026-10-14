import json
from collections import defaultdict, Counter
rows=json.load(open("call_view.json"))
calls=[]
for r in rows:
    c=r["call_view"]; 
    calls.append(dict(t=c["start_call_date_time"], dur=int(c.get("call_duration_seconds") or 0), status=c.get("call_status"), disp=c.get("call_tracking_display_location"), typ=c.get("type_"), area=c.get("caller_area_code"), camp=r["campaign"]["name"], ag=r["ad_group"]["name"]))
calls.sort(key=lambda x:x["t"])
print("first", calls[0]["t"], "last", calls[-1]["t"], "n", len(calls))
print(Counter(c["status"] for c in calls))
print(Counter(c["disp"] for c in calls))
print(Counter(c["typ"] for c in calls))
by=defaultdict(list)
for c in calls: by[c["t"][:7]].append(c)
print("\nmonth  calls  received  missed  other | <10s  10-29s  30-59s  60-179s  180s+ | median_dur | avg_dur")
for mo in sorted(by):
    L=by[mo]; st=Counter(c["status"] for c in L)
    d=[c["dur"] for c in L]; d.sort()
    b=[sum(1 for x in d if x<10), sum(1 for x in d if 10<=x<30), sum(1 for x in d if 30<=x<60), sum(1 for x in d if 60<=x<180), sum(1 for x in d if x>=180)]
    print(f"{mo}  {len(L):4d}  {st.get('RECEIVED',0):6d}  {st.get('MISSED',0):5d}  {len(L)-st.get('RECEIVED',0)-st.get('MISSED',0):4d} | {b[0]:3d} {b[1]:5d} {b[2]:6d} {b[3]:7d} {b[4]:5d} | {d[len(d)//2]:4d} | {sum(d)/len(d):6.1f}")
