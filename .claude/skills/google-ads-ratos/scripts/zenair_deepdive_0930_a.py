"""Zen Air deep dive 2026-09-30, part A: weekly trend, conversion mix, campaign settings."""
import sys
from collections import defaultdict
from datetime import date, timedelta
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"
START, END = "2026-06-29", "2026-09-29"


def wk(d):
    dt = date.fromisoformat(d)
    return (dt - timedelta(days=dt.weekday())).isoformat()


print("=" * 110)
print("1) WEEKLY TREND BY CAMPAIGN (Mon-start weeks), enabled + paused w/ spend")
print("=" * 110)
q = f"""
SELECT campaign.id, campaign.name, segments.date,
       metrics.cost_micros, metrics.clicks, metrics.impressions,
       metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_rank_lost_impression_share,
       metrics.search_budget_lost_impression_share
FROM campaign
WHERE segments.date BETWEEN '{START}' AND '{END}' AND metrics.impressions > 0
"""
agg = defaultdict(lambda: defaultdict(float))
names = {}
for r in run_query(CID, q):
    c, s, m = r["campaign"], r["segments"], r.get("metrics", {})
    k = (c["id"], wk(s["date"]))
    names[c["id"]] = c["name"]
    a = agg[k]
    a["cost"] += int(m.get("cost_micros", 0)) / 1e6
    a["clicks"] += int(m.get("clicks", 0))
    a["impr"] += int(m.get("impressions", 0))
    a["conv"] += float(m.get("conversions", 0))
    a["allconv"] += float(m.get("all_conversions", 0))
    # impression-weighted IS pieces (approx)
    imp = int(m.get("impressions", 0))
    if "search_impression_share" in m:
        a["is_w"] += float(m["search_impression_share"]) * imp
        a["rank_w"] += float(m.get("search_rank_lost_impression_share", 0)) * imp
        a["bud_w"] += float(m.get("search_budget_lost_impression_share", 0)) * imp
        a["is_imp"] += imp

for cid in sorted(names):
    print(f"\n--- {names[cid]} ({cid})")
    print(f"  {'week':10s} {'cost':>9s} {'clk':>5s} {'impr':>6s} {'CPC':>7s} {'conv':>6s} {'allcv':>6s} {'CPL':>9s} {'CVR':>6s} {'IS':>5s} {'rkL':>5s} {'bdL':>5s}")
    tot = defaultdict(float)
    for (c2, w), a in sorted(agg.items()):
        if c2 != cid:
            continue
        for kk, vv in a.items():
            tot[kk] += vv
        cpc = a["cost"] / a["clicks"] if a["clicks"] else 0
        cpl = a["cost"] / a["conv"] if a["conv"] else float("nan")
        cvr = a["conv"] / a["clicks"] * 100 if a["clicks"] else 0
        isv = a["is_w"] / a["is_imp"] * 100 if a["is_imp"] else float("nan")
        rk = a["rank_w"] / a["is_imp"] * 100 if a["is_imp"] else float("nan")
        bd = a["bud_w"] / a["is_imp"] * 100 if a["is_imp"] else float("nan")
        print(f"  {w:10s} {a['cost']:9.2f} {a['clicks']:5.0f} {a['impr']:6.0f} {cpc:7.2f} {a['conv']:6.1f} {a['allconv']:6.1f} {cpl:9.2f} {cvr:5.1f}% {isv:5.1f} {rk:5.1f} {bd:5.1f}")
    print(f"  {'TOTAL':10s} {tot['cost']:9.2f} {tot['clicks']:5.0f} {tot['impr']:6.0f} {tot['cost']/max(tot['clicks'],1):7.2f} {tot['conv']:6.1f} {tot['allconv']:6.1f}")

print("\n" + "=" * 110)
print("2) CONVERSIONS BY ACTION x CAMPAIGN x WEEK (all_conversions > 0)")
print("=" * 110)
q = f"""
SELECT campaign.name, segments.date, segments.conversion_action_name,
       segments.conversion_action_category, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '{START}' AND '{END}' AND metrics.all_conversions > 0
"""
cv = defaultdict(lambda: [0.0, 0.0])
for r in run_query(CID, q):
    s, m = r["segments"], r["metrics"]
    k = (wk(s["date"]), r["campaign"]["name"][:38], s["conversion_action_name"][:34], s["conversion_action_category"])
    cv[k][0] += float(m.get("conversions", 0))
    cv[k][1] += float(m.get("all_conversions", 0))
for k, v in sorted(cv.items()):
    print(f"  {k[0]} | {k[1]:38s} | {k[2]:34s} | {k[3]:20s} conv={v[0]:5.1f} all={v[1]:5.1f}")

print("\n" + "=" * 110)
print("3) CAMPAIGN SETTINGS (non-removed)")
print("=" * 110)
q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.serving_status,
       campaign.advertising_channel_type, campaign.bidding_strategy_type,
       campaign.maximize_conversions.target_cpa_micros,
       campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros,
       campaign.target_impression_share.cpc_bid_ceiling_micros,
       campaign.network_settings.target_google_search, campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network,
       campaign.geo_target_type_setting.positive_geo_target_type,
       campaign.geo_target_type_setting.negative_geo_target_type,
       campaign_budget.amount_micros, campaign.primary_status, campaign.primary_status_reasons
FROM campaign
WHERE campaign.status != 'REMOVED'
"""
for r in run_query(CID, q):
    c, b = r["campaign"], r.get("campaign_budget", {})
    if c["status"] != "ENABLED":
        print(f"  [{c['status']}] {c['name']} ({c['id']})")
        continue
    print(f"\n  [ENABLED] {c['name']} ({c['id']})")
    print(f"    channel={c['advertising_channel_type']} bidding={c['bidding_strategy_type']} budget=${int(b.get('amount_micros',0))/1e6:.0f}/d")
    print(f"    maxconv={c.get('maximize_conversions')} tis={c.get('target_impression_share')}")
    print(f"    networks={c.get('network_settings')} geo={c.get('geo_target_type_setting')}")
    print(f"    primary_status={c.get('primary_status')} reasons={c.get('primary_status_reasons')}")

