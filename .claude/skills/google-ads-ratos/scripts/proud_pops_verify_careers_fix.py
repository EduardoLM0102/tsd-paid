"""
Proud Pops — verify the careers/job-application GTM fix (live v42, published 2026-10-07 10:32 America/Chicago).
Checklist Block E (E1–E3) in clients/proud-pops/internal-checklist-2026-10.md. Read-only.

Run:  ./tsd.sh proud_pops_verify_careers_fix.py            (default: since 2026-10-07)
      ./tsd.sh proud_pops_verify_careers_fix.py 2026-10-08 (custom start date)

Pass criteria:
  - GA4 generate_lead on /careers = 0 for every hour after 2026-10-07 10:00 CT
  - GA4 job_application appears on /careers (if anyone applied)
  - Google Ads `Website lead` per day drops vs the Sep 23–Oct 6 baseline (~6/day → ~1.5/day),
    PMax Electrical most (~3.4/day → ~0)
  - (after B1) no google/cpc sessions landing on /careers
"""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
from ga4_setup import data_service

CID = "1051843378"
PROP = "properties/438523825"
START = sys.argv[1] if len(sys.argv) > 1 else "2026-10-07"
BASE_S, BASE_U = "2026-09-23", "2026-10-06"
f = lambda x: float(x or 0)
ga = data_service()

def ga4(dims, mets, flt, s=START, u="today", limit=2000):
    body = {"dateRanges": [{"startDate": s, "endDate": u}], "dimensions": [{"name": d} for d in dims],
            "metrics": [{"name": m} for m in mets], "dimensionFilter": flt, "limit": limit}
    r = ga.properties().runReport(property=PROP, body=body).execute()
    return [([d["value"] for d in x["dimensionValues"]], [m["value"] for m in x["metricValues"]]) for x in r.get("rows", [])]

ev_in = {"filter": {"fieldName": "eventName", "inListFilter": {"values": ["generate_lead", "job_application"]}}}
print(f"=== GA4 generate_lead / job_application by hour (CT) and page, since {START}")
rows = ga4(["dateHour", "eventName", "pagePath", "sessionSourceMedium"], ["eventCount"], ev_in)
for d, m in sorted(rows):
    flag = "  <-- FAIL: lead on /careers after fix" if (d[1] == "generate_lead" and "career" in d[2] and d[0] >= "2026100711") else ""
    print(f"  {d[0]}  {d[1]:16s} {d[2]:32s} {d[3]:30s} {m[0]}{flag}")
if not rows:
    print("  (no events yet)")

print(f"\n=== GA4 google/cpc sessions LANDING on /careers by campaign, since {START} (should go to 0 after checklist B1)")
land = {"andGroup": {"expressions": [
    {"filter": {"fieldName": "landingPage", "stringFilter": {"matchType": "CONTAINS", "value": "/careers"}}},
    {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}]}}
rows = ga4(["date", "sessionGoogleAdsCampaignName"], ["sessions"], land)
for d, m in sorted(rows):
    print(f"  {d[0]}  {d[1]:46s} {m[0]}")
if not rows:
    print("  (none)")

print(f"\n=== Google Ads `Website lead` (all_conversions, by click date) per campaign per day")
q = f"""SELECT campaign.name, segments.date, segments.conversion_action_name, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '{BASE_S}' AND '{START if START > BASE_U else BASE_U}' OR segments.date >= '{START}'"""
# GAQL has no OR across date ranges in all versions; do two queries instead
def website_lead(s, u):
    out = defaultdict(lambda: defaultdict(float))
    for r in run_query(CID, f"""SELECT campaign.name, segments.date, segments.conversion_action_name, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '{s}' AND '{u}'"""):
        if r["segments"].get("conversion_action_name") == "Website lead":
            out[r["campaign"]["name"]][r["segments"]["date"]] += f(r["metrics"].get("all_conversions"))
    return out
import datetime
today = datetime.date.today().isoformat()
base = website_lead(BASE_S, BASE_U)
post = website_lead(START, today)
days_post = sorted({d for c in post.values() for d in c})
names = sorted(set(base) | set(post))
print(f"  {'campaign':46s} {'base/day':>8s}  " + "  ".join(d[5:] for d in days_post))
tb = 0.0
tp = defaultdict(float)
for n in names:
    b = sum(base[n].values()) / 14
    tb += b
    for d in days_post:
        tp[d] += post[n].get(d, 0)
    print(f"  {n[:46]:46s} {b:8.2f}  " + "  ".join(f"{post[n].get(d, 0):5.1f}" for d in days_post))
print(f"  {'TOTAL':46s} {tb:8.2f}  " + "  ".join(f"{tp[d]:5.1f}" for d in days_post))
print("  note: 2026-10-07 is a split day (fix live from 10:32 CT); recent days fill in as conversions lag.")
