"""Read-only: did GA4 G-WF5DBMQ644 come back on neonmonkeytree.com? daily + hourly sessions by host, key events."""
from ga4_setup import data_service
svc = data_service(); prop = "properties/328458299"
def rep(body): return svc.properties().runReport(property=prop, body=body).execute().get("rows", [])
print("DAILY sessions by hostname (10-01 → today)")
rows = rep({"dateRanges":[{"startDate":"2026-10-01","endDate":"today"}],"dimensions":[{"name":"date"},{"name":"hostName"}],
            "metrics":[{"name":"sessions"},{"name":"screenPageViews"}],"orderBys":[{"dimension":{"dimensionName":"date"}}],"limit":500})
for r in rows:
    d, h = [x["value"] for x in r["dimensionValues"]]; s, v = [x["value"] for x in r["metricValues"]]
    print(f"  {d}  {h:<32} sessions {s:>4}  views {v:>4}")
print("\nHOURLY sessions on neonmonkeytree.com, last 4 days (property tz)")
rows = rep({"dateRanges":[{"startDate":"3daysAgo","endDate":"today"}],"dimensions":[{"name":"dateHour"}],
            "metrics":[{"name":"sessions"}],"dimensionFilter":{"filter":{"fieldName":"hostName","stringFilter":{"value":"neonmonkeytree.com","matchType":"CONTAINS"}}},
            "orderBys":[{"dimension":{"dimensionName":"dateHour"}}],"limit":200})
print("  " + "  ".join(f"{r['dimensionValues'][0]['value'][4:]}:{r['metricValues'][0]['value']}" for r in rows))
print("\nEVENTS since 10-10 on site host")
rows = rep({"dateRanges":[{"startDate":"2026-10-10","endDate":"today"}],"dimensions":[{"name":"eventName"},{"name":"hostName"}],
            "metrics":[{"name":"eventCount"}],"orderBys":[{"metric":{"metricName":"eventCount"},"desc":True}],"limit":50})
for r in rows:
    print(f"  {r['dimensionValues'][0]['value']:<28} {r['dimensionValues'][1]['value']:<30} {r['metricValues'][0]['value']}")
print("\nSTREAM tz check:", svc.properties().runReport(property=prop, body={"dateRanges":[{"startDate":"today","endDate":"today"}],"metrics":[{"name":"sessions"}]}).execute().get("metadata",{}).get("timeZone"))
