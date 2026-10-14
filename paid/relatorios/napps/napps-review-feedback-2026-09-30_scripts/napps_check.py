import os
import sys, json
from collections import defaultdict, Counter
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="9509605037"
def g(r,*k):
    for x in k: r = r.get(x, {}) if isinstance(r, dict) else {}
    return r
q="""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
 call_view.type, call_view.call_tracking_display_location, call_view.caller_area_code, campaign.name
FROM call_view WHERE call_view.start_call_date_time >= '2025-03-24 00:00:00' AND call_view.start_call_date_time <= '2025-09-23 23:59:59'"""
rows=list(run_query(CID,q))
print("2025 window calls:", len(rows))
missed=[r for r in rows if g(r,"call_view","call_status")=="MISSED"]
print("missed:", len(missed))
print("\nMISSED by month:", sorted(Counter(g(r,"call_view","start_call_date_time")[:7] for r in missed).items()))
print("MISSED by campaign:", Counter(g(r,"campaign","name") for r in missed).most_common())
print("MISSED by type:", Counter(str(g(r,"call_view","type")) for r in missed).most_common())
print("MISSED by display loc:", Counter(str(g(r,"call_view","call_tracking_display_location")) for r in missed).most_common())
print("MISSED by area code:", Counter(str(g(r,"call_view","caller_area_code")) for r in missed).most_common(10))
print("MISSED duration (s):", sorted(int(g(r,"call_view","call_duration_seconds") or 0) for r in missed))
hrs=Counter()
for r in missed:
    t=g(r,"call_view","start_call_date_time"); hrs[t[11:13]]+=1
print("MISSED by hour (acct tz):", sorted(hrs.items()))
wd=Counter()
import datetime
for r in missed:
    d=datetime.date.fromisoformat(g(r,"call_view","start_call_date_time")[:10]); wd[d.strftime("%a")]+=1
print("MISSED by weekday:", wd.most_common())
print("\nAll June 2025 missed, chronological:")
for r in sorted(missed, key=lambda r:g(r,"call_view","start_call_date_time")):
    t=g(r,"call_view","start_call_date_time")
    if t.startswith("2025-06"):
        print(" ", t, g(r,"call_view","call_duration_seconds"), g(r,"call_view","caller_area_code"), g(r,"campaign","name"))
# RECEIVED duration for comparison
rec=[int(g(r,"call_view","call_duration_seconds") or 0) for r in rows if g(r,"call_view","call_status")!="MISSED"]
print("\nRECEIVED durations:", sorted(rec))
q2="""SELECT call_view.start_call_date_time, call_view.call_status FROM call_view WHERE call_view.start_call_date_time >= '2026-03-24 00:00:00'"""
r2=list(run_query(CID,q2))
print("\n2026 since 03-24:", len(r2), "missed:", sum(1 for r in r2 if g(r,"call_view","call_status")=="MISSED"))
print("\n=== Current campaigns (enabled) + spend since 2026-09-15 ===")
q3="""SELECT campaign.name, campaign.id, campaign.status, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.impressions
FROM campaign WHERE segments.date BETWEEN '2026-09-15' AND '2026-09-28' AND metrics.impressions > 0"""
for r in run_query(CID,q3):
    print(f"  {g(r,'campaign','name'):45s} {g(r,'campaign','status'):8s} budget ${int(g(r,'campaign_budget','amount_micros') or 0)/1e6:.0f}/d  spend ${int(g(r,'metrics','cost_micros') or 0)/1e6:,.0f}  clicks {g(r,'metrics','clicks')}  conv {g(r,'metrics','conversions')}")
q4="""SELECT campaign.name, campaign.status, campaign_budget.amount_micros FROM campaign WHERE campaign.status = 'ENABLED'"""
print("\n=== All ENABLED campaigns now ===")
for r in run_query(CID,q4):
    print(f"  {g(r,'campaign','name'):45s} budget ${int(g(r,'campaign_budget','amount_micros') or 0)/1e6:.0f}/d")
