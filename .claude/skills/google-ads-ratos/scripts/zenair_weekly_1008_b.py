"""Zen Air 10-08: GA4 google/cpc quality before vs after the 09-30 Max Clicks switch + campaign settings + call assets."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ga4_setup import data_service
from lib import run_query

PROP, CID = "350001559", "4360840956"
cpc = {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}

def rep(title, dims, mets, ranges, filt=None, limit=200):
    body = {"dateRanges": [{"startDate": s, "endDate": e, "name": n} for n, s, e in ranges],
            "dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets], "limit": limit}
    if filt:
        body["dimensionFilter"] = filt
    r = data_service().properties().runReport(property=f"properties/{PROP}", body=body).execute()
    print(f"\n=== {title}")
    for row in sorted(r.get("rows", []), key=lambda x: [d["value"] for d in x["dimensionValues"]]):
        print("  " + " | ".join(d["value"] for d in row["dimensionValues"]) + " || " + " ".join(m["value"] for m in row["metricValues"]))
    if not r.get("rows"):
        print("  (no rows)")

R = [("before_0917_0929", "2026-09-17", "2026-09-29"), ("after_1001_1007", "2026-10-01", "2026-10-07")]
rep("google/cpc sessions + engagement", [], ["sessions", "engagedSessions", "averageSessionDuration", "bounceRate"], R, cpc)
rep("google/cpc events of interest", ["eventName"], ["eventCount"], R,
    {"andGroup": {"expressions": [cpc, {"filter": {"fieldName": "eventName", "inListFilter": {"values": [
        "phone_click", "generate_lead", "form_submitted", "form_start", "click_to_call", "ghl_contact_us", "book_now_link_click"]}}}]}})
rep("google/cpc landing pages after", ["landingPage"], ["sessions", "engagedSessions", "averageSessionDuration"],
    [R[1]], cpc)
rep("ALL sources key events, after", ["sessionSourceMedium", "eventName"], ["keyEvents"], [R[1]])

print("\n=== CAMPAIGN SETTINGS")
q = """SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type,
  campaign.target_spend.cpc_bid_ceiling_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
  campaign_budget.amount_micros FROM campaign WHERE campaign.status = 'ENABLED'"""
for r in run_query(CID, q):
    print("  ", r["campaign"], r.get("campaign_budget"))

print("\n=== CALL ASSETS + phone metrics 10-01..10-07")
for r in run_query(CID, """SELECT asset.id, asset.call_asset.phone_number, customer_asset.status
  FROM customer_asset WHERE asset.type = 'CALL'"""):
    print("  account-level", r["asset"].get("id"), r["asset"].get("call_asset", {}).get("phone_number"), r["customer_asset"].get("status"))
for r in run_query(CID, """SELECT campaign.name, asset.id, asset.call_asset.phone_number, campaign_asset.status
  FROM campaign_asset WHERE asset.type = 'CALL'"""):
    print("  campaign-level", r["campaign"]["name"][:40], r["asset"].get("id"), r["asset"].get("call_asset", {}).get("phone_number"), r["campaign_asset"].get("status"))
for r in run_query(CID, """SELECT campaign.name, metrics.phone_impressions, metrics.phone_calls
  FROM campaign WHERE segments.date BETWEEN '2026-09-17' AND '2026-10-07' AND metrics.impressions > 0"""):
    print("  phone metrics 09-17..10-07", r["campaign"]["name"][:40], r.get("metrics"))
