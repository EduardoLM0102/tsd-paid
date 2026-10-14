import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from ga4_setup import data_service
from collections import defaultdict
PROP = "properties/438523825"
svc = data_service()
def report(S, U, dims, mets, flt=None, limit=1000):
    body = {"dateRanges": [{"startDate": S, "endDate": U}], "dimensions": [{"name": d} for d in dims],
            "metrics": [{"name": m} for m in mets], "limit": limit}
    if flt: body["dimensionFilter"] = flt
    resp = svc.properties().runReport(property=PROP, body=body).execute()
    return [([d["value"] for d in r["dimensionValues"]], [m["value"] for m in r["metricValues"]]) for r in resp.get("rows", [])]
lead = {"filter": {"fieldName": "eventName", "stringFilter": {"value": "generate_lead"}}}
cpc = {"andGroup": {"expressions": [lead, {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}]}}

print("== google/cpc generate_lead: campaign x event pagePath, Sep 7 - Oct 6")
for d, m in sorted(report("2026-09-07", "2026-10-06", ["sessionGoogleAdsCampaignName", "pagePath"], ["eventCount"], cpc), key=lambda x: (x[0][0], -int(x[1][0]))):
    print(f"   {d[0]:46s} {d[1]:35s} {m[0]}")

print("\n== ALL sources generate_lead by pagePath, Sep 7 - Oct 6")
for d, m in sorted(report("2026-09-07", "2026-10-06", ["pagePath"], ["eventCount"], lead), key=lambda x: -int(x[1][0])):
    print(f"   {d[0]:35s} {m[0]}")

print("\n== google/cpc generate_lead weekly by pagePath bucket, Jul 20 - Oct 6")
wk = defaultdict(lambda: defaultdict(int))
for d, m in report("2026-07-20", "2026-10-06", ["isoYearIsoWeek", "pagePath"], ["eventCount"], cpc):
    b = "careers" if "career" in d[1] else "schedule" if "schedule" in d[1] else "other"
    wk[d[0]][b] += int(m[0])
for w in sorted(wk):
    print(f"   {w}  careers={wk[w]['careers']:3d} schedule={wk[w]['schedule']:3d} other={wk[w]['other']:3d}")

print("\n== /careers page views from google/cpc by campaign + landing page, Sep 7 - Oct 6")
car = {"andGroup": {"expressions": [{"filter": {"fieldName": "pagePath", "stringFilter": {"value": "/careers"}}},
        {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}]}}
for d, m in sorted(report("2026-09-07", "2026-10-06", ["sessionGoogleAdsCampaignName", "landingPage"], ["screenPageViews", "sessions"], car), key=lambda x: -int(x[1][0]))[:15]:
    print(f"   {d[0]:46s} landing={d[1]:30s} views={m[0]} sessions={m[1]}")

print("\n== events fired on /careers (all sources), Sep 7 - Oct 6")
for d, m in sorted(report("2026-09-07", "2026-10-06", ["eventName"], ["eventCount"], {"filter": {"fieldName": "pagePath", "stringFilter": {"value": "/careers"}}}), key=lambda x: -int(x[1][0])):
    print(f"   {d[0]:35s} {m[0]}")
