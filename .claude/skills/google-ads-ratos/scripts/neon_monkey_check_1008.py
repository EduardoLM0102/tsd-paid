import sys
sys.path.insert(0, ".")
from collections import defaultdict
from lib import run_query

CID = "7953905280"
NB, BR, PMAX = "23825900343", "23739724064", "21225221220"
LIVE = f"{NB}, {BR}, {PMAX}"
TAG = {NB: "NB", BR: "BR", PMAX: "PMAX"}
S30, E = "2026-09-08", "2026-10-07"


def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)


def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


def safe(label, fn):
    try:
        fn()
    except Exception as e:
        print(f"  !! {label} failed: {str(e)[:400]}")


def a():
    hdr("A) LIVE CAMPAIGN SETTINGS")
    q = f"""
    SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, campaign.primary_status,
           campaign.primary_status_reasons, campaign.network_settings.target_search_network,
           campaign.network_settings.target_content_network,
           campaign.geo_target_type_setting.positive_geo_target_type,
           campaign.maximize_conversions.target_cpa_micros, campaign.target_cpa.target_cpa_micros,
           campaign.maximize_conversion_value.target_roas,
           campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros,
           campaign.target_impression_share.cpc_bid_ceiling_micros,
           campaign.target_spend.cpc_bid_ceiling_micros, campaign.bidding_strategy
    FROM campaign WHERE campaign.id IN ({LIVE})
    """
    for r in run_query(CID, q):
        print(" ", TAG[r["campaign"]["id"]], r["campaign"])


def b():
    for rng in ("LAST_7_DAYS", "LAST_30_DAYS"):
        hdr(f"B) CONVERSIONS BY ACTION {rng} (account)")
        q = f"""
        SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.conversions,
               metrics.all_conversions
        FROM customer WHERE segments.date DURING {rng} AND metrics.all_conversions > 0
        """
        for r in run_query(CID, q):
            s, m = r["segments"], r["metrics"]
            print(f"  {s['conversion_action_name'][:60]:60s} {s['conversion_action_category']:22s} "
                  f"conv={f(m,'conversions'):5.1f} all={f(m,'all_conversions'):5.1f}")


def b2():
    hdr("B2) CONVERSIONS BY ACTION x CAMPAIGN, LAST_30_DAYS")
    q = f"""
    SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
    FROM campaign WHERE campaign.id IN ({LIVE}) AND segments.date DURING LAST_30_DAYS AND metrics.all_conversions > 0
    """
    for r in run_query(CID, q):
        m = r["metrics"]
        print(f"  {TAG[r['campaign']['id']]:5s} {r['segments']['conversion_action_name'][:60]:60s} "
              f"conv={f(m,'conversions'):5.1f} all={f(m,'all_conversions'):5.1f}")


def c():
    hdr(f"C) WEEKLY BY CAMPAIGN {S30}..{E}")
    q = f"""
    SELECT segments.week, campaign.id, metrics.cost_micros, metrics.clicks, metrics.impressions,
           metrics.conversions, metrics.all_conversions
    FROM campaign WHERE campaign.id IN ({LIVE}) AND segments.date BETWEEN '2026-08-17' AND '{E}'
    """
    rows = sorted(run_query(CID, q), key=lambda r: (r["segments"]["week"], r["campaign"]["id"]))
    for r in rows:
        m = r["metrics"]
        cost, clk = f(m, "cost_micros", int) / 1e6, f(m, "clicks", int)
        print(f"  wk {r['segments']['week']} {TAG[r['campaign']['id']]:5s} cost=${cost:8.2f} clk={clk:4d} "
              f"cpc=${(cost/clk if clk else 0):6.2f} imp={f(m,'impressions',int):6d} conv={f(m,'conversions'):4.1f} "
              f"all={f(m,'all_conversions'):5.1f}")


def c2():
    hdr("C2) DAILY SEARCH CAMPAIGNS, LAST 30 DAYS (IS / rank lost / budget lost)")
    q = f"""
    SELECT segments.date, campaign.id, metrics.cost_micros, metrics.clicks, metrics.impressions,
           metrics.conversions, metrics.search_impression_share, metrics.search_rank_lost_impression_share,
           metrics.search_budget_lost_impression_share, metrics.search_top_impression_share,
           metrics.search_absolute_top_impression_share
    FROM campaign WHERE campaign.id IN ({NB}, {BR}) AND segments.date BETWEEN '{S30}' AND '{E}'
    """
    rows = sorted(run_query(CID, q), key=lambda r: (r["segments"]["date"], r["campaign"]["id"]))
    for r in rows:
        m = r["metrics"]
        cost, clk = f(m, "cost_micros", int) / 1e6, f(m, "clicks", int)
        print(f"  {r['segments']['date']} {TAG[r['campaign']['id']]:3s} cost=${cost:7.2f} clk={clk:3d} "
              f"cpc=${(cost/clk if clk else 0):6.2f} imp={f(m,'impressions',int):4d} conv={f(m,'conversions'):3.1f} "
              f"IS={f(m,'search_impression_share'):.2f} rank={f(m,'search_rank_lost_impression_share'):.2f} "
              f"bud={f(m,'search_budget_lost_impression_share'):.2f} absTop={f(m,'search_absolute_top_impression_share'):.2f}")


def d():
    hdr("D) NETWORK SPLIT, LAST_7_DAYS")
    q = f"""
    SELECT campaign.id, segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.impressions,
           metrics.conversions
    FROM campaign WHERE campaign.id IN ({LIVE}) AND segments.date DURING LAST_7_DAYS
    """
    for r in run_query(CID, q):
        m = r["metrics"]
        print(f"  {TAG[r['campaign']['id']]:5s} {r['segments']['ad_network_type']:16s} "
              f"cost=${f(m,'cost_micros',int)/1e6:8.2f} clk={f(m,'clicks',int):4d} imp={f(m,'impressions',int):6d} "
              f"conv={f(m,'conversions'):4.1f}")


def e():
    hdr("E) SEARCH TERMS LAST_7_DAYS (search campaigns), by cost")
    q = f"""
    SELECT campaign.id, search_term_view.search_term, segments.search_term_match_type, metrics.cost_micros,
           metrics.clicks, metrics.impressions, metrics.conversions
    FROM search_term_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date DURING LAST_7_DAYS
    """
    agg = defaultdict(lambda: [0, 0, 0, 0.0])
    for r in run_query(CID, q):
        m = r["metrics"]
        k = (TAG[r["campaign"]["id"]], r["search_term_view"]["search_term"])
        agg[k][0] += f(m, "cost_micros", int)
        agg[k][1] += f(m, "clicks", int)
        agg[k][2] += f(m, "impressions", int)
        agg[k][3] += f(m, "conversions")
    lawn = [k for k in agg if "lawn" in k[1]]
    print(f"  terms={len(agg)}  terms containing 'lawn'={len(lawn)} -> {lawn[:10]}")
    print(f"  lawn spend=${sum(agg[k][0] for k in lawn)/1e6:.2f}")
    for k, v in sorted(agg.items(), key=lambda kv: -kv[1][0])[:40]:
        print(f"  {k[0]:3s} ${v[0]/1e6:7.2f} clk={v[1]:3d} imp={v[2]:4d} conv={v[3]:3.1f}  {k[1]}")


def e2():
    hdr("E2) LAWN TERMS SINCE FIX (2026-09-29..2026-10-08), all campaigns incl PMax not available")
    q = f"""
    SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.impressions
    FROM search_term_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date BETWEEN '2026-09-29' AND '2026-10-08'
    """
    n = 0
    for r in run_query(CID, q):
        t = r["search_term_view"]["search_term"]
        if "lawn" in t:
            m = r["metrics"]
            n += 1
            print(f"  {TAG[r['campaign']['id']]} {t} ${f(m,'cost_micros',int)/1e6:.2f} clk={f(m,'clicks',int)} imp={f(m,'impressions',int)}")
    print(f"  lawn rows since fix: {n}")


def g():
    hdr("G) KEYWORDS (search campaigns), LAST_30_DAYS")
    q = f"""
    SELECT campaign.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
           ad_group_criterion.status, ad_group_criterion.quality_info.quality_score,
           ad_group_criterion.effective_cpc_bid_micros,
           metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
    FROM keyword_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date DURING LAST_30_DAYS
      AND ad_group_criterion.status != 'REMOVED'
    """
    rows = run_query(CID, q)
    for r in sorted(rows, key=lambda r: -f(r["metrics"], "cost_micros", int)):
        m, k = r["metrics"], r["ad_group_criterion"]
        cost, clk = f(m, "cost_micros", int) / 1e6, f(m, "clicks", int)
        qs = k.get("quality_info", {}).get("quality_score", "-")
        print(f"  {TAG[r['campaign']['id']]:3s} {r['ad_group']['name'][:22]:22s} {k['keyword']['text'][:34]:34s} "
              f"{k['keyword']['match_type']:7s} {k['status']:7s} QS={qs!s:2s} ${cost:7.2f} clk={clk:3d} "
              f"cpc=${(cost/clk if clk else 0):6.2f} conv={f(m,'conversions'):3.1f}")


def h():
    hdr("H) CHANGE HISTORY 2026-09-09..2026-10-08")
    q = """
    SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
           change_event.resource_change_operation, change_event.changed_fields, change_event.campaign,
           change_event.client_type, change_event.old_resource, change_event.new_resource
    FROM change_event
    WHERE change_event.change_date_time >= '2026-09-09' AND change_event.change_date_time <= '2026-10-08 23:59:59'
    ORDER BY change_event.change_date_time DESC
    LIMIT 200
    """
    for r in run_query(CID, q):
        ce = r["change_event"]
        print(f"  {ce['change_date_time']} {ce.get('user_email','?'):32s} {ce['change_resource_type']:22s} "
              f"{ce['resource_change_operation']:7s} {ce.get('client_type','')} camp={ce.get('campaign','').split('/')[-1]} "
              f"fields={ce.get('changed_fields','')}")
        if ce["change_resource_type"] in ("CAMPAIGN_BUDGET", "CAMPAIGN"):
            print(f"      old={str(ce.get('old_resource',''))[:300]}")
            print(f"      new={str(ce.get('new_resource',''))[:300]}")


def i():
    hdr("I) MONTHLY SPEND (all PPC)")
    q = """
    SELECT segments.month, metrics.cost_micros, metrics.conversions, metrics.all_conversions
    FROM customer WHERE segments.date BETWEEN '2026-07-01' AND '2026-10-08'
    """
    for r in sorted(run_query(CID, q), key=lambda r: r["segments"]["month"]):
        m = r["metrics"]
        print(f"  {r['segments']['month']} ${f(m,'cost_micros',int)/1e6:9.2f} conv={f(m,'conversions'):5.1f} all={f(m,'all_conversions'):5.1f}")


for label, fn in [("A", a), ("B", b), ("B2", b2), ("C", c), ("C2", c2), ("D", d), ("E", e), ("E2", e2),
                  ("G", g), ("H", h), ("I", i)]:
    safe(label, fn)
