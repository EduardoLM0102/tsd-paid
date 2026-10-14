import sys
sys.path.insert(0, ".")
from collections import defaultdict
from lib import run_query

CID = "7953905280"
NB, BR, PMAX = "23825900343", "23739724064", "21225221220"
LIVE = f"{NB}, {BR}, {PMAX}"
TAG = {NB: "NB", BR: "BR", PMAX: "PMAX"}
HOLIDAY, LEAF = "18787352551", "19146431184"


def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)


def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


def safe(label, fn):
    try:
        fn()
    except Exception as e:
        print(f"  !! {label} failed: {str(e)[:500]}")


def conv_actions():
    hdr("1) CONVERSION ACTIONS (enabled)")
    q = """
    SELECT conversion_action.id, conversion_action.name, conversion_action.status, conversion_action.type,
           conversion_action.category, conversion_action.primary_for_goal, conversion_action.counting_type,
           conversion_action.include_in_conversions_metric, conversion_action.phone_call_duration_seconds,
           conversion_action.origin
    FROM conversion_action WHERE conversion_action.status = 'ENABLED'
    """
    for r in run_query(CID, q):
        c = r["conversion_action"]
        print(f"  {c['id']:>12} {c['name'][:52]:52s} {c['type']:28s} {c['category']:20s} primary={c.get('primary_for_goal')} "
              f"incl={c.get('include_in_conversions_metric')} count={c.get('counting_type')} dur={c.get('phone_call_duration_seconds','-')} origin={c.get('origin')}")
    hdr("1b) CAMPAIGN CONVERSION GOALS (biddable)")
    q = f"""
    SELECT campaign.id, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
    FROM campaign_conversion_goal WHERE campaign.id IN ({LIVE})
    """
    for r in run_query(CID, q):
        g = r["campaign_conversion_goal"]
        if g.get("biddable"):
            print(f"  {TAG[r['campaign']['id']]:5s} {g['category']:22s} {g['origin']:10s} biddable")


def assets():
    hdr("2) CAMPAIGN + ACCOUNT ASSETS (call, sitelink, callout, etc.)")
    q = f"""
    SELECT campaign.id, campaign_asset.field_type, campaign_asset.status, asset.call_asset.phone_number,
           asset.sitelink_asset.link_text, asset.callout_asset.callout_text, asset.type,
           campaign_asset.primary_status
    FROM campaign_asset WHERE campaign.id IN ({LIVE}) AND campaign_asset.status = 'ENABLED'
    """
    agg = defaultdict(list)
    for r in run_query(CID, q):
        a, ca = r["asset"], r["campaign_asset"]
        val = (a.get("call_asset", {}).get("phone_number") or a.get("sitelink_asset", {}).get("link_text")
               or a.get("callout_asset", {}).get("callout_text") or a.get("type"))
        agg[(TAG[r["campaign"]["id"]], ca["field_type"])].append(f"{val}[{ca.get('primary_status','')}]")
    for k, v in sorted(agg.items()):
        print(f"  {k[0]:5s} {k[1]:20s} {len(v)}: {', '.join(v)[:300]}")
    q = """
    SELECT customer_asset.field_type, customer_asset.status, asset.call_asset.phone_number, asset.type,
           asset.sitelink_asset.link_text, asset.callout_asset.callout_text, customer_asset.primary_status
    FROM customer_asset WHERE customer_asset.status = 'ENABLED'
    """
    agg = defaultdict(list)
    for r in run_query(CID, q):
        a, ca = r["asset"], r["customer_asset"]
        val = (a.get("call_asset", {}).get("phone_number") or a.get("sitelink_asset", {}).get("link_text")
               or a.get("callout_asset", {}).get("callout_text") or a.get("type"))
        agg[ca["field_type"]].append(f"{val}[{ca.get('primary_status','')}]")
    for k, v in sorted(agg.items()):
        print(f"  ACCOUNT {k:20s} {len(v)}: {', '.join(v)[:300]}")


def geo():
    hdr("3) LOCATION + PROXIMITY TARGETS")
    q = f"""
    SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative,
           campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius,
           campaign_criterion.proximity.radius_units, campaign_criterion.proximity.geo_point.latitude_in_micro_degrees,
           campaign_criterion.proximity.geo_point.longitude_in_micro_degrees
    FROM campaign_criterion WHERE campaign.id IN ({LIVE}) AND campaign_criterion.type IN ('LOCATION', 'PROXIMITY')
    """
    rows = run_query(CID, q)
    gtcs = set()
    for r in rows:
        cc = r["campaign_criterion"]
        if cc.get("location"):
            gtcs.add(cc["location"]["geo_target_constant"])
    names = {}
    if gtcs:
        ids = ",".join(f"'{g}'" for g in gtcs)
        for r in run_query(CID, f"SELECT geo_target_constant.resource_name, geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.resource_name IN ({ids})"):
            g = r["geo_target_constant"]
            names[g["resource_name"]] = f"{g['name']} ({g.get('target_type')})"
    for r in sorted(rows, key=lambda r: r["campaign"]["id"]):
        cc = r["campaign_criterion"]
        neg = "NEG " if cc.get("negative") else ""
        if cc.get("location"):
            print(f"  {TAG[r['campaign']['id']]:5s} {neg}LOC {names.get(cc['location']['geo_target_constant'], cc['location']['geo_target_constant'])}")
        else:
            p = cc["proximity"]
            gp = p.get("geo_point", {})
            print(f"  {TAG[r['campaign']['id']]:5s} {neg}RADIUS {p.get('radius')} {p.get('radius_units')} @ "
                  f"{int(gp.get('latitude_in_micro_degrees',0))/1e6:.3f},{int(gp.get('longitude_in_micro_degrees',0))/1e6:.3f}")


def geo_perf():
    hdr("4) WHERE SPEND LANDS, LAST_30_DAYS (user physical location, city)")
    q = f"""
    SELECT campaign.id, segments.geo_target_city, user_location_view.targeting_location,
           metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM user_location_view WHERE campaign.id IN ({LIVE}) AND segments.date DURING LAST_30_DAYS
    """
    rows = run_query(CID, q)
    city = defaultdict(lambda: [0, 0, 0.0, 0])
    gtcs = set()
    for r in rows:
        c = r.get("segments", {}).get("geo_target_city", "unknown")
        gtcs.add(c)
        m = r["metrics"]
        city[c][0] += f(m, "cost_micros", int)
        city[c][1] += f(m, "clicks", int)
        city[c][2] += f(m, "conversions")
        if not r["user_location_view"].get("targeting_location"):
            city[c][3] += f(m, "cost_micros", int)
    names = {}
    real = [g for g in gtcs if g and g.startswith("geoTargetConstants/")]
    if real:
        ids = ",".join(f"'{g}'" for g in real)
        for r in run_query(CID, f"SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.resource_name IN ({ids})"):
            names[r["geo_target_constant"]["resource_name"]] = r["geo_target_constant"]["name"]
    tot = sum(v[0] for v in city.values())
    print(f"  total ${tot/1e6:.2f}")
    for c, v in sorted(city.items(), key=lambda kv: -kv[1][0])[:30]:
        print(f"  {names.get(c, c)[:28]:28s} ${v[0]/1e6:8.2f} ({v[0]/tot*100:4.1f}%) clk={v[1]:4d} conv={v[2]:4.1f} "
              f"outside-targets=${v[3]/1e6:.2f}")


def ads():
    hdr("5) ADS (enabled) — final URLs, strength, approval")
    q = f"""
    SELECT campaign.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.ad.final_urls,
           ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status, ad_group_ad.primary_status,
           metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM ad_group_ad WHERE campaign.id IN ({NB}, {BR}) AND ad_group_ad.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
    """
    for r in run_query(CID, q):
        a, m = r["ad_group_ad"], r["metrics"]
        print(f"  {TAG[r['campaign']['id']]:3s} {r['ad_group']['name'][:20]:20s} {a['ad']['type']:22s} {a.get('ad_strength'):10s} "
              f"{a.get('policy_summary',{}).get('approval_status'):18s} {a.get('primary_status')} ${f(m,'cost_micros',int)/1e6:7.2f} "
              f"conv={f(m,'conversions'):3.1f} {a['ad'].get('final_urls')}")
    hdr("5b) PMAX ASSET GROUPS")
    q = f"""
    SELECT asset_group.name, asset_group.status, asset_group.final_urls, asset_group.ad_strength, asset_group.primary_status,
           metrics.cost_micros, metrics.conversions
    FROM asset_group WHERE campaign.id = {PMAX} AND segments.date DURING LAST_30_DAYS
    """
    for r in run_query(CID, q):
        g, m = r["asset_group"], r["metrics"]
        print(f"  {g['name'][:30]:30s} {g['status']:8s} {g.get('ad_strength')} {g.get('primary_status')} "
              f"${f(m,'cost_micros',int)/1e6:8.2f} conv={f(m,'conversions'):4.1f} {g.get('final_urls')}")
    q = f"""
    SELECT campaign.asset_automation_settings, campaign.url_expansion_opt_out, campaign.brand_guidelines_enabled
    FROM campaign WHERE campaign.id = {PMAX}
    """
    for r in run_query(CID, q):
        print("  PMAX settings:", r["campaign"])


def qs():
    hdr("6) QUALITY SCORE COMPONENTS (keywords with impressions, 30d)")
    q = f"""
    SELECT campaign.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
           ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score,
           ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr,
           metrics.impressions
    FROM keyword_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0
    """
    for r in sorted(run_query(CID, q), key=lambda r: -f(r["metrics"], "impressions", int)):
        k = r["ad_group_criterion"]
        qi = k.get("quality_info", {})
        print(f"  {TAG[r['campaign']['id']]:3s} {k['keyword']['text'][:36]:36s} {k['keyword']['match_type']:7s} QS={qi.get('quality_score','-')!s:2s} "
              f"ad={qi.get('creative_quality_score','-'):14s} lp={qi.get('post_click_quality_score','-'):14s} ctr={qi.get('search_predicted_ctr','-'):14s} imp={r['metrics']['impressions']}")


def negs():
    hdr("7) NEGATIVE KEYWORDS (campaign + shared lists)")
    q = f"""
    SELECT campaign.id, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
    FROM campaign_criterion WHERE campaign.id IN ({LIVE}) AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE
    """
    agg = defaultdict(list)
    for r in run_query(CID, q):
        k = r["campaign_criterion"]["keyword"]
        agg[TAG[r["campaign"]["id"]]].append(f"{k['text']}({k['match_type'][0]})")
    for k, v in agg.items():
        print(f"  {k:5s} {len(v)}: {', '.join(v)[:600]}")
    q = """SELECT campaign.id, shared_set.name, shared_set.type, shared_set.member_count FROM campaign_shared_set
           WHERE campaign_shared_set.status = 'ENABLED'"""
    for r in run_query(CID, q):
        print(f"  shared: camp={r['campaign']['id']} {r['shared_set']}")
    q = f"""SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative FROM campaign_criterion
            WHERE campaign.id = {PMAX} AND campaign_criterion.negative = TRUE"""
    c = defaultdict(int)
    for r in run_query(CID, q):
        c[r["campaign_criterion"]["type"]] += 1
    print("  PMAX negative criteria by type:", dict(c))


def st_themes():
    hdr("8) SEARCH TERMS 30d BY THEME (NB + BR)")
    q = f"""
    SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM search_term_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date DURING LAST_30_DAYS
    """
    themes = {
        "out_of_area": ["dallas", "arlington", "grand prairie", "irving", "mansfield", "keller", "north richland",
                        "denton", "plano", "frisco", "mckinney", "garland", "southlake", "grapevine", "euless",
                        "bedford", "hurst", "burleson", "cleburne", "duncanville", "mesquite", "lewisville"],
        "competitor": ["trugreen", "mercer", "jc tree", "blue ox", "davey", "bartlett", "monster tree", "arbor masters",
                       "arbormasters", "preservation tree", "tree amigos", "integrity tree"],
        "landscaping": ["landscap", "lawn", "yard", "mow", "sod", "irrigation", "sprinkler"],
        "other_service": ["planting", "plant", "fence", "gutter", "pest", "firewood", "mulch", "nursery"],
        "diy_jobs_price": ["job", "hiring", "salary", "rent", "rental", "diy", "how to", "free", "cheap", "cost", "price"],
    }
    agg = defaultdict(lambda: [0, 0, 0.0, set()])
    tot = [0, 0, 0.0]
    for r in run_query(CID, q):
        t, m = r["search_term_view"]["search_term"], r["metrics"]
        cost, clk, conv = f(m, "cost_micros", int), f(m, "clicks", int), f(m, "conversions")
        tot[0] += cost; tot[1] += clk; tot[2] += conv
        hit = None
        if "neon monkey" in t:
            hit = "brand"
        else:
            for th, words in themes.items():
                if any(w in t for w in words):
                    hit = th
                    break
        hit = hit or "core_tree"
        agg[hit][0] += cost; agg[hit][1] += clk; agg[hit][2] += conv
        if cost > 0:
            agg[hit][3].add(t)
    print(f"  TOTAL ${tot[0]/1e6:.2f} clk={tot[1]} conv={tot[2]:.1f}")
    for th, v in sorted(agg.items(), key=lambda kv: -kv[1][0]):
        top = sorted(v[3])[:18]
        print(f"  {th:15s} ${v[0]/1e6:8.2f} ({v[0]/tot[0]*100:4.1f}%) clk={v[1]:4d} conv={v[2]:4.1f}  e.g. {top}")


def devices():
    hdr("9) DEVICE + DAY-OF-WEEK, NB 30d")
    q = f"""SELECT segments.device, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign
            WHERE campaign.id IN ({NB}, {PMAX}) AND segments.date DURING LAST_30_DAYS"""
    agg = defaultdict(lambda: [0, 0, 0.0])
    for r in run_query(CID, q):
        m = r["metrics"]
        a = agg[r["segments"]["device"]]
        a[0] += f(m, "cost_micros", int); a[1] += f(m, "clicks", int); a[2] += f(m, "conversions")
    for d, v in agg.items():
        print(f"  {d:10s} ${v[0]/1e6:8.2f} clk={v[1]:4d} conv={v[2]:4.1f}")
    q = f"""SELECT campaign.ad_schedule_criterion FROM campaign WHERE campaign.id = {NB}"""
    q = f"""SELECT campaign.id, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour,
            campaign_criterion.ad_schedule.end_hour, campaign_criterion.bid_modifier FROM campaign_criterion
            WHERE campaign.id IN ({LIVE}) AND campaign_criterion.type = 'AD_SCHEDULE'"""
    rows = run_query(CID, q)
    print(f"  ad schedule rows: {len(rows)}")
    for r in rows[:14]:
        print("   ", TAG[r["campaign"]["id"]], r["campaign_criterion"])


def seasonal():
    hdr("10) SEASONAL CAMPAIGNS (Holiday Lighting, Leaf Cleanup) + PMax/all, monthly Aug 2025 - Jan 2026")
    q = f"""
    SELECT segments.month, campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions,
           metrics.conversions
    FROM campaign WHERE segments.date BETWEEN '2025-08-01' AND '2026-01-31' AND metrics.impressions > 0
    """
    for r in sorted(run_query(CID, q), key=lambda r: (r["segments"]["month"], r["campaign"]["name"])):
        m = r["metrics"]
        print(f"  {r['segments']['month']} {r['campaign']['name'][:40]:40s} ${f(m,'cost_micros',int)/1e6:8.2f} "
              f"clk={f(m,'clicks',int):4d} imp={f(m,'impressions',int):6d} conv={f(m,'conversions'):5.1f}")
    hdr("10b) HOLIDAY + LEAF keywords/ads state")
    q = f"""
    SELECT campaign.id, ad_group.name, ad_group.status, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM ad_group_criterion WHERE campaign.id IN ({HOLIDAY}, {LEAF}) AND ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'
    """
    agg = defaultdict(list)
    for r in run_query(CID, q):
        k = r["ad_group_criterion"]["keyword"]
        agg[(r["campaign"]["id"], r["ad_group"]["name"])].append(f"{k['text']}({k['match_type'][0]})")
    for k, v in agg.items():
        print(f"  {k}: {len(v)} kws: {', '.join(v)[:400]}")
    q = f"""SELECT campaign.id, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.responsive_search_ad.headlines
            FROM ad_group_ad WHERE campaign.id IN ({HOLIDAY}, {LEAF}) AND ad_group_ad.status = 'ENABLED'"""
    for r in run_query(CID, q):
        a = r["ad_group_ad"]
        hl = [h.get("text") for h in a["ad"].get("responsive_search_ad", {}).get("headlines", [])][:6]
        print(f"  {r['campaign']['id']} {a['ad'].get('final_urls')} {a.get('policy_summary',{}).get('approval_status')} {hl}")


def billing():
    hdr("11) ACCOUNT BUDGET (billing)")
    q = """SELECT account_budget.status, account_budget.approved_spending_limit_micros, account_budget.approved_start_date_time,
           account_budget.approved_end_date_time, account_budget.amount_served_micros, account_budget.name
           FROM account_budget"""
    for r in run_query(CID, q):
        print("  ", r["account_budget"])


for label, fn in [("1", conv_actions), ("2", assets), ("3", geo), ("4", geo_perf), ("5", ads), ("6", qs), ("7", negs),
                  ("8", st_themes), ("9", devices), ("10", seasonal), ("11", billing)]:
    safe(label, fn)
