"""Checklist H4 (read-only): why does /pricing get 20–26% of Search clicks, and does it lead to bookings?"""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
from ga4_setup import data_service
CID = "1051843378"; S, U = "2026-09-08", "2026-10-07"
f = lambda x: float(x or 0)

print("== sitelink assets (account + campaign level)")
links = {}
for r in run_query(CID, "SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls FROM asset WHERE asset.type = 'SITELINK'"):
    a = r["asset"]; links[a["id"]] = (a.get("sitelink_asset", {}).get("link_text"), (a.get("final_urls") or ["?"])[0])
for r in run_query(CID, f"""SELECT campaign.name, campaign.status, asset.id, campaign_asset.status, metrics.clicks, metrics.impressions, metrics.cost_micros
FROM campaign_asset WHERE campaign_asset.field_type = 'SITELINK' AND campaign.status = 'ENABLED' AND segments.date BETWEEN '{S}' AND '{U}'"""):
    t, u = links.get(r["asset"]["id"], ("?", "?")); m = r["metrics"]
    print(f"   campaign {r['campaign']['name'][24:50]:26s} '{t}' -> {u.replace('https://proudpops.com', '')}  clk {m.get('clicks', 0)} impr {m.get('impressions', 0)}")
for r in run_query(CID, f"""SELECT asset.id, customer_asset.status, metrics.clicks, metrics.impressions FROM customer_asset
WHERE customer_asset.field_type = 'SITELINK' AND segments.date BETWEEN '{S}' AND '{U}'"""):
    t, u = links.get(r["asset"]["id"], ("?", "?")); m = r["metrics"]
    print(f"   ACCOUNT-level '{t}' -> {u.replace('https://proudpops.com', '')}  clk {m.get('clicks', 0)} impr {m.get('impressions', 0)} [{r['customer_asset'].get('status')}]")

print("\n== Search clicks by click type (30d)")
ct = defaultdict(lambda: [0.0, 0.0])
for r in run_query(CID, f"""SELECT campaign.name, campaign.advertising_channel_type, segments.click_type, metrics.clicks, metrics.cost_micros FROM campaign
WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date BETWEEN '{S}' AND '{U}' AND metrics.clicks > 0"""):
    x = ct[(r["campaign"]["name"][24:50], str(r["segments"]["click_type"]))]; x[0] += f(r["metrics"]["clicks"]); x[1] += f(r["metrics"]["cost_micros"]) / 1e6
for (c, t), (clk, cost) in sorted(ct.items()):
    print(f"   {c:26s} {t:22s} clk {clk:4.0f}  ${cost:7,.0f}")

print("\n== GA4: google/cpc sessions by landing page → customer leads (generate_lead, excluding /careers), last 30 days")
ga = data_service()
def rep(dims, mets, flt):
    body = {"dateRanges": [{"startDate": S, "endDate": U}], "dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets], "dimensionFilter": flt, "limit": 500}
    r = ga.properties().runReport(property="properties/438523825", body=body).execute()
    return [([d["value"] for d in x["dimensionValues"]], [m["value"] for m in x["metricValues"]]) for x in r.get("rows", [])]
cpc = {"filter": {"fieldName": "sessionSourceMedium", "stringFilter": {"value": "google / cpc"}}}
sess = defaultdict(float)
for d, m in rep(["landingPage", "sessionGoogleAdsCampaignName"], ["sessions"], cpc):
    if "Search" in d[1] or "Branded" in d[1]:
        sess[d[0].split("?")[0]] += f(m[0])
leads = defaultdict(float)
lf = {"andGroup": {"expressions": [cpc, {"filter": {"fieldName": "eventName", "stringFilter": {"value": "generate_lead"}}},
      {"notExpression": {"filter": {"fieldName": "pagePath", "stringFilter": {"matchType": "CONTAINS", "value": "careers"}}}}]}}
for d, m in rep(["landingPage", "sessionGoogleAdsCampaignName"], ["eventCount"], lf):
    if "Search" in d[1] or "Branded" in d[1]:
        leads[d[0].split("?")[0]] += f(m[0])
for lp in sorted(sess, key=lambda k: -sess[k])[:12]:
    print(f"   {lp[:45]:45s} sessions {sess[lp]:5.0f}  customer leads {leads.get(lp, 0):3.0f}  rate {leads.get(lp, 0) / sess[lp] * 100 if sess[lp] else 0:4.1f}%")
pr = {"andGroup": {"expressions": [cpc, {"filter": {"fieldName": "landingPage", "stringFilter": {"matchType": "BEGINS_WITH", "value": "/pricing"}}}]}}
print("\n== GA4: where /pricing landers go next (pagePath views in those sessions)")
for d, m in sorted(rep(["pagePath"], ["screenPageViews"], pr), key=lambda x: -f(x[1][0]))[:8]:
    print(f"   {d[0][:45]:45s} views {m[0]}")
