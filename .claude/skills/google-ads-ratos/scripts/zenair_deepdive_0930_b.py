"""Zen Air deep dive 2026-09-30, part B: keywords, search terms, device/hour/geo, LPs, calls, changes.
Clean window = 2026-08-27 (day after geo fix) .. 2026-09-29. LP switch = 2026-09-15."""
import sys
from collections import defaultdict
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"
S, E, LP = "2026-08-27", "2026-09-29", "2026-09-15"
CAMPS = "(23675783172, 24100030790)"
BR = "23675783172"


def f(m, k, cast=float):
    return cast(m.get(k, 0) or 0)


def hdr(t):
    print("\n" + "=" * 120 + f"\n{t}\n" + "=" * 120)


hdr("B1) KEYWORDS (clean window) — cost-sorted, with QS components")
q = f"""
SELECT campaign.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       ad_group_criterion.status, ad_group_criterion.quality_info.quality_score,
       ad_group_criterion.quality_info.creative_quality_score,
       ad_group_criterion.quality_info.post_click_quality_score,
       ad_group_criterion.quality_info.search_predicted_ctr,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions,
       metrics.search_impression_share, metrics.search_rank_lost_impression_share
FROM keyword_view
WHERE campaign.id IN {CAMPS} AND segments.date BETWEEN '{S}' AND '{E}'
"""
kw = defaultdict(lambda: defaultdict(float))
meta = {}
for r in run_query(CID, q):
    agc, m = r["ad_group_criterion"], r.get("metrics", {})
    k = (r["campaign"]["id"], r["ad_group"]["name"], agc["keyword"]["text"], agc["keyword"]["match_type"])
    qi = agc.get("quality_info", {})
    meta[k] = (agc.get("status"), qi.get("quality_score", "-"), qi.get("creative_quality_score", "-")[:6],
               qi.get("post_click_quality_score", "-")[:6], qi.get("search_predicted_ctr", "-")[:6])
    kw[k]["cost"] += f(m, "cost_micros", int) / 1e6
    kw[k]["clk"] += f(m, "clicks", int)
    kw[k]["imp"] += f(m, "impressions", int)
    kw[k]["conv"] += f(m, "conversions")
tot = sum(v["cost"] for v in kw.values())
print(f"  {'camp':3s} {'ad group':24s} {'keyword':38s} {'match':7s} {'stat':7s} QS {'ad':6s} {'LP':6s} {'CTR':6s} {'cost':>8s} {'%':>5s} {'clk':>4s} {'imp':>5s} {'CPC':>6s} {'conv':>5s}")
for k, v in sorted(kw.items(), key=lambda x: -x[1]["cost"]):
    if v["imp"] == 0:
        continue
    st, qs, cq, lq, pc = meta[k]
    cpc = v["cost"] / v["clk"] if v["clk"] else 0
    print(f"  {'BR' if k[0]==BR else 'NB':3s} {k[1][:24]:24s} {k[2][:38]:38s} {k[3][:7]:7s} {str(st)[:7]:7s} {str(qs):2s} {cq:6s} {lq:6s} {pc:6s} {v['cost']:8.2f} {v['cost']/tot*100:5.1f} {v['clk']:4.0f} {v['imp']:5.0f} {cpc:6.2f} {v['conv']:5.1f}")

hdr("B2) SEARCH TERMS (clean window) — top 70 by cost")
q = f"""
SELECT campaign.id, search_term_view.search_term, search_term_view.status,
       segments.search_term_match_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view
WHERE campaign.id IN {CAMPS} AND segments.date BETWEEN '{S}' AND '{E}'
"""
st = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    m = r.get("metrics", {})
    k = (r["campaign"]["id"], r["search_term_view"]["search_term"], r["segments"].get("search_term_match_type", ""))
    st[k]["cost"] += f(m, "cost_micros", int) / 1e6
    st[k]["clk"] += f(m, "clicks", int)
    st[k]["imp"] += f(m, "impressions", int)
    st[k]["conv"] += f(m, "conversions")
stot = sum(v["cost"] for v in st.values())
print(f"  search-term rows={len(st)} cost covered=${stot:,.2f} (keyword total ${tot:,.2f})")
for k, v in sorted(st.items(), key=lambda x: -x[1]["cost"])[:70]:
    cpc = v["cost"] / v["clk"] if v["clk"] else 0
    print(f"  {'BR' if k[0]==BR else 'NB':3s} {k[1][:55]:55s} {k[2][:14]:14s} ${v['cost']:7.2f} clk={v['clk']:3.0f} imp={v['imp']:4.0f} cpc={cpc:6.2f} conv={v['conv']:4.1f}")
conv_terms = [(k, v) for k, v in st.items() if v["conv"] > 0]
print(f"\n  terms WITH conversions ({len(conv_terms)}):")
for k, v in sorted(conv_terms, key=lambda x: -x[1]["conv"]):
    print(f"    {'BR' if k[0]==BR else 'NB':3s} {k[1][:60]:60s} conv={v['conv']:.1f} cost=${v['cost']:.2f}")

hdr("B3) DEVICE (clean window)")
q = f"""
SELECT campaign.id, segments.device, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM campaign WHERE campaign.id IN {CAMPS} AND segments.date BETWEEN '{S}' AND '{E}'
"""
dv = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    m = r.get("metrics", {})
    k = ("BR" if r["campaign"]["id"] == BR else "NB", r["segments"]["device"])
    dv[k]["cost"] += f(m, "cost_micros", int) / 1e6
    dv[k]["clk"] += f(m, "clicks", int)
    dv[k]["conv"] += f(m, "conversions")
for k, v in sorted(dv.items()):
    if v["cost"]:
        print(f"  {k[0]} {k[1]:10s} cost=${v['cost']:8.2f} clk={v['clk']:4.0f} cpc={v['cost']/max(v['clk'],1):6.2f} conv={v['conv']:4.1f}")

hdr("B4) HOUR OF DAY + DAY OF WEEK, non-branded (clean window)")
q = f"""
SELECT segments.hour, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM campaign WHERE campaign.id = 24100030790 AND segments.date BETWEEN '{S}' AND '{E}'
"""
hr = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    m = r.get("metrics", {})
    h = int(r["segments"]["hour"])
    hr[h]["cost"] += f(m, "cost_micros", int) / 1e6
    hr[h]["clk"] += f(m, "clicks", int)
    hr[h]["conv"] += f(m, "conversions")
for h in range(24):
    v = hr.get(h, {"cost": 0, "clk": 0, "conv": 0})
    print(f"  {h:02d}h cost=${v['cost']:7.2f} clk={v['clk']:3.0f} conv={v['conv']:3.1f}")
q = f"""
SELECT segments.day_of_week, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM campaign WHERE campaign.id = 24100030790 AND segments.date BETWEEN '{S}' AND '{E}'
"""
for r in run_query(CID, q):
    m = r.get("metrics", {})
    print(f"  {r['segments']['day_of_week']:10s} cost=${f(m,'cost_micros',int)/1e6:7.2f} clk={f(m,'clicks',int):3.0f} conv={f(m,'conversions'):3.1f}")

hdr("B5) USER LOCATION (city-level, clean window)")
q = f"""
SELECT campaign.id, segments.geo_target_city, segments.geo_target_most_specific_location,
       metrics.cost_micros, metrics.clicks, metrics.conversions
FROM user_location_view
WHERE campaign.id IN {CAMPS} AND segments.date BETWEEN '{S}' AND '{E}'
"""
geo = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    m = r.get("metrics", {})
    k = ("BR" if r["campaign"]["id"] == BR else "NB", r["segments"].get("geo_target_city", "?"))
    geo[k]["cost"] += f(m, "cost_micros", int) / 1e6
    geo[k]["clk"] += f(m, "clicks", int)
    geo[k]["conv"] += f(m, "conversions")
cities = [k[1] for k in geo]
names = {}
ids = sorted({c.split("/")[-1] for c in cities if c and c != "?"})
if ids:
    q = f"SELECT geo_target_constant.id, geo_target_constant.canonical_name FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"
    for r in run_query(CID, q):
        g = r["geo_target_constant"]
        names[g["id"]] = g["canonical_name"]
for k, v in sorted(geo.items(), key=lambda x: -x[1]["cost"])[:30]:
    nm = names.get(k[1].split("/")[-1], k[1])
    print(f"  {k[0]} {nm[:50]:50s} cost=${v['cost']:7.2f} clk={v['clk']:3.0f} conv={v['conv']:3.1f}")

hdr("B6) LOCATION CRITERIA + AD SCHEDULE on enabled campaigns")
q = f"""
SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative,
       campaign_criterion.location.geo_target_constant,
       campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units,
       campaign_criterion.proximity.address.city_name, campaign_criterion.proximity.geo_point.latitude_in_micro_degrees,
       campaign_criterion.proximity.geo_point.longitude_in_micro_degrees,
       campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour,
       campaign_criterion.ad_schedule.end_hour, campaign_criterion.bid_modifier
FROM campaign_criterion
WHERE campaign.id IN {CAMPS} AND campaign_criterion.type IN ('LOCATION','PROXIMITY','AD_SCHEDULE','LOCATION_GROUP')
"""
for r in run_query(CID, q):
    cc = r["campaign_criterion"]
    print(f"  {'BR' if r['campaign']['id']==BR else 'NB'} {cc.get('type', cc.get('type_')):12s} neg={cc.get('negative')} loc={cc.get('location')} prox={cc.get('proximity')} sched={cc.get('ad_schedule')} mod={cc.get('bid_modifier')}")
q = f"""
SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative
FROM campaign_criterion WHERE campaign.id IN {CAMPS}
"""
cnt = defaultdict(int)
for r in run_query(CID, q):
    cc = r["campaign_criterion"]
    cnt[("BR" if r["campaign"]["id"] == BR else "NB", cc.get("type", cc.get("type_")), cc.get("negative"))] += 1
print("  criterion counts:", dict(cnt))

hdr("B7) LANDING PAGES, pre vs post 09-15")
for lab, a, b in (("PRE ", S, "2026-09-14"), ("POST", LP, E)):
    q = f"""
    SELECT campaign.id, landing_page_view.unexpanded_final_url, metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM landing_page_view WHERE campaign.id IN {CAMPS} AND segments.date BETWEEN '{a}' AND '{b}'
    """
    for r in run_query(CID, q):
        m = r.get("metrics", {})
        print(f"  {lab} {'BR' if r['campaign']['id']==BR else 'NB'} {r['landing_page_view']['unexpanded_final_url'][:80]:80s} ${f(m,'cost_micros',int)/1e6:7.2f} clk={f(m,'clicks',int):3.0f} conv={f(m,'conversions'):3.1f}")

hdr("B8) ADS on enabled campaigns")
q = f"""
SELECT campaign.id, ad_group.name, ad_group.status, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.type,
       ad_group_ad.ad.final_urls, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status,
       ad_group_ad.ad.responsive_search_ad.headlines
FROM ad_group_ad WHERE campaign.id IN {CAMPS} AND ad_group_ad.status != 'REMOVED'
"""
for r in run_query(CID, q):
    a = r["ad_group_ad"]
    hl = [h.get("text") for h in a["ad"].get("responsive_search_ad", {}).get("headlines", [])][:6]
    print(f"  {'BR' if r['campaign']['id']==BR else 'NB'} ag={r['ad_group']['name'][:28]:28s}({r['ad_group']['status'][:3]}) ad={a['status'][:3]} str={a.get('ad_strength')} appr={a.get('policy_summary',{}).get('approval_status')} url={a['ad'].get('final_urls')}")
    print(f"       headlines: {hl}")

hdr("B9) CALLS (call_view, last 30d)")
q = """
SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds,
       call_view.call_status, call_view.type, call_view.call_tracking_display_location
FROM call_view WHERE call_view.start_call_date_time >= '2026-08-30 00:00:00'
ORDER BY call_view.start_call_date_time
"""
for r in run_query(CID, q):
    c = r["call_view"]
    print(f"  {c.get('start_call_date_time')} dur={c.get('call_duration_seconds',0):>4}s {c.get('call_status','')[:10]:10s} {c.get('type','')[:14]:14s} {c.get('call_tracking_display_location','')[:10]:10s} {r['campaign']['name'][:40]}")

hdr("B10) DAILY conversions by action, since 09-10 (to see Click-to-call vs Calls-from-ads overlap)")
q = """
SELECT segments.date, segments.conversion_action_name, metrics.all_conversions
FROM customer WHERE segments.date BETWEEN '2026-09-10' AND '2026-09-29' AND metrics.all_conversions > 0
"""
for r in sorted(run_query(CID, q), key=lambda x: x["segments"]["date"]):
    print(f"  {r['segments']['date']} {r['segments']['conversion_action_name'][:45]:45s} {r['metrics']['all_conversions']}")

hdr("B11) CHANGE EVENTS last 30d (both campaigns + account)")
q = """
SELECT change_event.change_date_time, change_event.user_email, change_event.client_type,
       change_event.change_resource_type, change_event.resource_change_operation,
       change_event.changed_fields, campaign.name
FROM change_event
WHERE change_event.change_date_time >= '2026-09-01' AND change_event.change_date_time <= '2026-09-30'
ORDER BY change_event.change_date_time DESC
LIMIT 300
"""
for r in run_query(CID, q):
    ce = r["change_event"]
    print(f"  {ce['change_date_time'][:16]} {ce.get('user_email','')[:28]:28s} {ce.get('client_type','')[:18]:18s} {ce.get('change_resource_type','')[:20]:20s} {ce.get('resource_change_operation','')[:7]:7s} {str(ce.get('changed_fields',''))[:70]:70s} {r.get('campaign',{}).get('name','')[:30]}")
