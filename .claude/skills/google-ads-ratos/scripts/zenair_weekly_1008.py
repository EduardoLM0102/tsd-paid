import sys
sys.path.insert(0, ".")
from collections import defaultdict
from lib import run_query

CID = "4360840956"
NB, BR = "24100030790", "23675783172"
S, E = "2026-09-17", "2026-10-07"

def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)

def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

hdr(f"A) DAILY BY CAMPAIGN {S}..{E} (enabled search campaigns)")
q = f"""
SELECT segments.date, campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions,
       metrics.conversions, metrics.all_conversions, metrics.search_impression_share,
       metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share
FROM campaign WHERE campaign.id IN ({NB}, {BR}) AND segments.date BETWEEN '{S}' AND '{E}'
"""
rows = sorted(run_query(CID, q), key=lambda r: (r["segments"]["date"], r["campaign"]["id"]))
for r in rows:
    m = r.get("metrics", {})
    tag = "NB" if r["campaign"]["id"] == NB else "BR"
    print(f"  {r['segments']['date']} {tag} cost=${f(m,'cost_micros',int)/1e6:8.2f} clk={f(m,'clicks',int):3d} imp={f(m,'impressions',int):5d} "
          f"conv={f(m,'conversions'):4.1f} allc={f(m,'all_conversions'):4.1f} IS={f(m,'search_impression_share'):.2f} "
          f"rankLost={f(m,'search_rank_lost_impression_share'):.2f} budLost={f(m,'search_budget_lost_impression_share'):.2f}")

hdr("B) CONVERSIONS BY ACTION BY DAY (all_conversions > 0)")
q = f"""
SELECT segments.date, campaign.name, segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '{S}' AND '{E}' AND metrics.all_conversions > 0
"""
for r in sorted(run_query(CID, q), key=lambda x: x["segments"]["date"]):
    s, m = r["segments"], r.get("metrics", {})
    print(f"  {s['date']} {r['campaign']['name'][:38]:38s} {s.get('conversion_action_name','')[:32]:32s} {s.get('conversion_action_category','')[:18]:18s} conv={f(m,'conversions'):.1f} all={f(m,'all_conversions'):.1f}")

hdr(f"C) CALLS (call_view since {S})")
q = f"""
SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds,
       call_view.call_status, call_view.type, call_view.caller_area_code
FROM call_view WHERE call_view.start_call_date_time >= '{S} 00:00:00'
ORDER BY call_view.start_call_date_time
"""
for r in run_query(CID, q):
    c = r["call_view"]
    print(f"  {c.get('start_call_date_time')} dur={c.get('call_duration_seconds',0):>4}s {c.get('call_status','')[:10]:10s} {c.get('type','')[:14]:14s} area={c.get('caller_area_code','')} {r['campaign']['name'][:40]}")

hdr("D) KEYWORDS SERVED 10-01..10-07")
q = f"""
SELECT campaign.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       ad_group_criterion.quality_info.quality_score,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM keyword_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date BETWEEN '2026-10-01' AND '{E}' AND metrics.impressions > 0
"""
kw = sorted(run_query(CID, q), key=lambda r: -f(r.get("metrics", {}), "cost_micros", int))
for r in kw:
    m, k = r.get("metrics", {}), r["ad_group_criterion"]
    clk = f(m, "clicks", int); cost = f(m, "cost_micros", int) / 1e6
    tag = "NB" if r["campaign"]["id"] == NB else "BR"
    print(f"  {tag} {k['keyword']['text'][:40]:40s} {k['keyword']['match_type'][:6]:6s} QS={k.get('quality_info',{}).get('quality_score','-')} "
          f"cost=${cost:7.2f} clk={clk:3d} imp={f(m,'impressions',int):5d} cpc=${(cost/clk if clk else 0):5.2f} conv={f(m,'conversions'):.1f}")

hdr("E) SEARCH TERMS 10-05..10-07 (after 10-05 negatives), by cost")
q = f"""
SELECT campaign.id, search_term_view.search_term, segments.search_term_match_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date BETWEEN '2026-10-05' AND '{E}'
"""
st = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    m = r.get("metrics", {})
    k = ("NB" if r["campaign"]["id"] == NB else "BR", r["search_term_view"]["search_term"])
    st[k]["cost"] += f(m, "cost_micros", int) / 1e6
    st[k]["clk"] += f(m, "clicks", int)
    st[k]["conv"] += f(m, "conversions")
tot = sum(v["cost"] for v in st.values())
print(f"  rows={len(st)} cost covered=${tot:,.2f}")
for k, v in sorted(st.items(), key=lambda x: -x[1]["cost"])[:45]:
    if v["cost"] > 0:
        print(f"  {k[0]} {k[1][:55]:55s} ${v['cost']:7.2f} clk={int(v['clk']):3d} conv={v['conv']:.1f}")

hdr("F) CURRENT SETTINGS")
q = f"""
SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type,
       campaign.maximize_clicks.cpc_bid_ceiling_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
       campaign.target_impression_share.location_fraction_micros,
       campaign_budget.amount_micros, campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network
FROM campaign WHERE campaign.id IN ({NB}, {BR})
"""
for r in run_query(CID, q):
    print("  ", r["campaign"], r.get("campaign_budget"))
