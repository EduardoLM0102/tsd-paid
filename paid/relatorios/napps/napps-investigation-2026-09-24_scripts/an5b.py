import json
from collections import defaultdict, Counter
rows=json.load(open("call_view.json"))
calls=[]
for r in rows:
    c=r["call_view"]
    calls.append(dict(t=c["start_call_date_time"], dur=int(c.get("call_duration_seconds") or 0), status=c.get("call_status"), typ=c.get("type_"), area=c.get("caller_area_code"), camp=r["campaign"]["name"], ag=r["ad_group"]["name"]))
# 2025-05/06 missed calls - which campaigns, which days/hours
print("== MISSED calls detail 2025-02..2025-07")
for c in calls:
    if c["status"]=="MISSED" and "2025-02"<=c["t"][:7]<="2025-07":
        print(c["t"], c["dur"], c["camp"], "|", c["ag"])
print()
# by campaign per year-phase
by=defaultdict(Counter)
for c in calls: by[c["camp"]][c["t"][:7]]+=1
for k,v in by.items(): print(k, dict(sorted(v.items())))
# hour-of-day, weekday for 2026 calls
import datetime
print("\n2026 calls by weekday / hour")
wd=Counter(); hr=Counter()
for c in calls:
    if c["t"]>="2026-04-01":
        d=datetime.datetime.strptime(c["t"],"%Y-%m-%d %H:%M:%S")
        wd[d.strftime("%a")]+=1; hr[d.hour]+=1
print(dict(wd)); print(dict(sorted(hr.items())))
# out of area codes
print("\narea codes 2026-04+:", Counter(c["area"] for c in calls if c["t"]>="2026-04-01").most_common(12))
print("area codes 2024:", Counter(c["area"] for c in calls if c["t"]<"2025-01-01").most_common(12))
