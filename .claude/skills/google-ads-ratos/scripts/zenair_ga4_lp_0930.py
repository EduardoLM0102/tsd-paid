"""Zen Air GA4: what happens on /book-hvac-service/ and contact page for google/cpc traffic, 09-15..09-29."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ga4_setup import data_service

PROP = "350001559"


def rep(title, dims, mets, start, end, filt=None, limit=200):
    body = {"dateRanges": [{"startDate": start, "endDate": end}],
            "dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets], "limit": limit}
    if filt:
        body["dimensionFilter"] = filt
    r = data_service().properties().runReport(property=f"properties/{PROP}", body=body).execute()
    print(f"\n=== {title} ({start}..{end})")
    for row in r.get("rows", []):
        print("  " + " | ".join(d["value"] for d in row["dimensionValues"]) + " || " + " ".join(m["value"] for m in row["metricValues"]))
    if not r.get("rows"):
        print("  (no rows)")


cpc = {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}

rep("google/cpc: events by landing page", ["landingPage", "eventName"], ["eventCount", "totalUsers"],
    "2026-09-15", "2026-09-29", cpc)
rep("ALL sources: events on /book-hvac-service/", ["eventName", "sessionSourceMedium"], ["eventCount"],
    "2026-09-15", "2026-09-29",
    {"filter": {"fieldName": "pagePath", "stringFilter": {"matchType": "CONTAINS", "value": "book-hvac-service"}}})
rep("google/cpc sessions + engagement by landing page", ["landingPage"],
    ["sessions", "engagedSessions", "averageSessionDuration", "bounceRate"], "2026-09-15", "2026-09-29", cpc)
rep("google/cpc key events by day", ["date", "eventName"], ["keyEvents"], "2026-08-27", "2026-09-29", cpc)
rep("all key events by source (post LP)", ["sessionSourceMedium", "eventName"], ["keyEvents"], "2026-09-15", "2026-09-29")
