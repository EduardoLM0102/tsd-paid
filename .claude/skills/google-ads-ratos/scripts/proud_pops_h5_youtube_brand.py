"""Checklist H5 (read-only): has YouTube (launched Aug 8, 2026) lifted branded search? Weekly Branded campaign impressions,
IS, estimated eligible brand searches (impr / IS), by city (San Antonio vs New Braunfels), plus YouTube delivery."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, BRANDED = "1051843378", "23853361615"; S, U = "2026-05-18", "2026-10-04"
f = lambda x: float(x or 0)
print("== Branded search, weekly (Mon weeks). est. eligible = impressions / search IS")
for r in sorted(run_query(CID, f"""SELECT segments.week, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.search_impression_share,
metrics.search_budget_lost_impression_share FROM campaign WHERE campaign.id = {BRANDED} AND segments.date BETWEEN '{S}' AND '{U}'"""), key=lambda r: r["segments"]["week"]):
    m = r["metrics"]; imp = f(m.get("impressions")); isx = f(m.get("search_impression_share"))
    tag = "  <- YouTube live" if r["segments"]["week"] >= "2026-08-03" else ""
    print(f"   {r['segments']['week']}  impr {imp:5.0f}  clk {f(m.get('clicks')):4.0f}  IS {isx * 100:5.1f}%  lostBudget {f(m.get('search_budget_lost_impression_share')) * 100:5.1f}%  est.eligible {imp / isx if isx else 0:6.0f}{tag}")
print("\n== Branded impressions by city, 8 weeks before vs 8 weeks after Aug 8")
city = defaultdict(lambda: [0.0, 0.0])
names = {}
for per, (a, b) in (("pre", ("2026-06-13", "2026-08-07")), ("post", ("2026-08-08", "2026-10-03"))):
    for r in run_query(CID, f"""SELECT segments.geo_target_city, metrics.impressions FROM geographic_view
WHERE campaign.id = {BRANDED} AND segments.date BETWEEN '{a}' AND '{b}'"""):
        c = r["segments"].get("geo_target_city", "?"); city[c][0 if per == "pre" else 1] += f(r["metrics"].get("impressions"))
ids = [c.split("/")[-1] for c in city if c != "?"]
if ids:
    for r in run_query(CID, f"SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"):
        names[r["geo_target_constant"]["resource_name"]] = r["geo_target_constant"]["name"]
for c, (pre, post) in sorted(city.items(), key=lambda x: -(x[1][0] + x[1][1]))[:10]:
    print(f"   {names.get(c, c)[:28]:28s} pre {pre:5.0f}  post {post:5.0f}  change {((post - pre) / pre * 100) if pre else 0:+6.1f}%")
print("\n== YouTube campaigns (since launch)")
for r in run_query(CID, """SELECT campaign.name, metrics.impressions, metrics.video_views, metrics.cost_micros, metrics.video_view_rate, metrics.average_cpv,
metrics.video_quartile_p100_rate, metrics.clicks FROM campaign WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date BETWEEN '2026-08-08' AND '2026-10-07'"""):
    m = r["metrics"]
    print(f"   {r['campaign']['name'][:42]:42s} ${f(m.get('cost_micros')) / 1e6:7,.0f}  impr {f(m.get('impressions')):8,.0f}  views {f(m.get('video_views')):7,.0f}  view rate {f(m.get('video_view_rate')) * 100:4.1f}%  CPV ${f(m.get('average_cpv')) / 1e6:.3f}  100% watched {f(m.get('video_quartile_p100_rate')) * 100:4.1f}%  clicks {f(m.get('clicks')):.0f}")
