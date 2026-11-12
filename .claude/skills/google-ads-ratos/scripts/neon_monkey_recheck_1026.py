"""Read-only: Neon Monkey 7953905280 recheck of the 10-19 changes (fu-063, 2026-10-26)."""
from collections import defaultdict
from lib import run_query
cid = "7953905280"
W = {"A_prior30 (09-19..10-18)": ("2026-09-19", "2026-10-18"),
     "B_pre_tagback (10-13..10-18)": ("2026-10-13", "2026-10-18"),
     "C_post (10-20..10-25)": ("2026-10-20", "2026-10-25")}
print("== campaigns now")
for r in run_query(cid, """SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
  campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.status='ENABLED'"""):
    c = r["campaign"]; print(" ", c["id"], c["name"], c.get("bidding_strategy_type"), c.get("primary_status"),
      "budget=$%.0f" % (int(r["campaign_budget"]["amount_micros"])/1e6), "cap=$%.0f" % (int(c.get("target_spend", {}).get("cpc_bid_ceiling_micros", 0))/1e6))
for label, (a, b) in W.items():
    print(f"\n== {label}: campaign stats")
    for r in run_query(cid, f"""SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
      metrics.search_impression_share, metrics.search_absolute_top_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
      FROM campaign WHERE segments.date BETWEEN '{a}' AND '{b}' AND metrics.cost_micros > 0"""):
        m = r["metrics"]; cost = int(m["cost_micros"])/1e6; cl = int(m["clicks"])
        print(f"  {r['campaign']['name'][:40]:<40} cost=${cost:,.0f} clk={cl} cpc=${cost/max(cl,1):.2f} conv={float(m['conversions']):.1f} all={float(m['all_conversions']):.1f} "
              f"IS={m.get('search_impression_share')} absTop={m.get('search_absolute_top_impression_share')} lostBud={m.get('search_budget_lost_impression_share')} lostRank={m.get('search_rank_lost_impression_share')}")
    print(f"  -- by conversion action x campaign (all_conversions)")
    for r in sorted(run_query(cid, f"""SELECT campaign.name, segments.conversion_action_name, segments.conversion_action_category, metrics.all_conversions, metrics.conversions
      FROM campaign WHERE segments.date BETWEEN '{a}' AND '{b}'"""), key=lambda r: (r["campaign"]["name"], r["segments"]["conversion_action_name"])):
        m = r["metrics"]
        if float(m.get("all_conversions", 0)):
            print(f"     {r['campaign']['name'][:28]:<28} {r['segments']['conversion_action_name'][:38]:<38} {r['segments'].get('conversion_action_category',''):<18} all={float(m['all_conversions']):.1f} bid={float(m['conversions']):.1f}")
print("\n== Branded daily 10-13..10-25")
for r in sorted(run_query(cid, """SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share, metrics.search_absolute_top_impression_share,
  metrics.search_rank_lost_impression_share FROM campaign WHERE campaign.id = 23739724064 AND segments.date BETWEEN '2026-10-13' AND '2026-10-25'"""), key=lambda r: r["segments"]["date"]):
    m = r["metrics"]; cost = int(m["cost_micros"])/1e6; cl = int(m["clicks"])
    print(f"  {r['segments']['date']} cost=${cost:.2f} clk={cl} impr={m['impressions']} cpc=${cost/max(cl,1):.2f} IS={m.get('search_impression_share')} absTop={m.get('search_absolute_top_impression_share')} lostRank={m.get('search_rank_lost_impression_share')}")
print("\n== NB daily 10-13..10-25")
for r in sorted(run_query(cid, """SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.all_conversions, metrics.search_impression_share
  FROM campaign WHERE campaign.id = 23825900343 AND segments.date BETWEEN '2026-10-13' AND '2026-10-25'"""), key=lambda r: r["segments"]["date"]):
    m = r["metrics"]; cost = int(m["cost_micros"])/1e6; cl = int(m["clicks"])
    print(f"  {r['segments']['date']} cost=${cost:.2f} clk={cl} impr={m['impressions']} cpc=${cost/max(cl,1):.2f} all={float(m['all_conversions']):.1f} IS={m.get('search_impression_share')}")
print("\n== NB search terms 10-20..10-25 (by cost)")
agg = defaultdict(lambda: [0, 0, 0.0, set()])
for r in run_query(cid, """SELECT search_term_view.search_term, segments.search_term_match_type, segments.keyword.info.text, metrics.cost_micros, metrics.clicks, metrics.all_conversions
  FROM search_term_view WHERE campaign.id = 23825900343 AND segments.date BETWEEN '2026-10-20' AND '2026-10-25'"""):
    m = r["metrics"]; k = r["search_term_view"]["search_term"]
    a = agg[k]; a[0] += int(m["cost_micros"]); a[1] += int(m["clicks"]); a[2] += float(m.get("all_conversions", 0))
    a[3].add(f"{r['segments'].get('search_term_match_type','')}:{r['segments'].get('keyword',{}).get('info',{}).get('text','')}")
tot = sum(v[0] for v in agg.values())/1e6
print(f"  total ${tot:,.0f} across {len(agg)} terms")
for k, v in sorted(agg.items(), key=lambda kv: -kv[1][0])[:40]:
    print(f"  ${v[0]/1e6:6.2f} clk={v[1]:>2} conv={v[2]:.1f}  {k[:48]:<48} {', '.join(sorted(v[3]))[:70]}")
print("\n== PMax by user location type (geographic_view) 10-20..10-25 vs 10-12..10-18")
for a, b in [("2026-10-12", "2026-10-18"), ("2026-10-20", "2026-10-25")]:
    agg2 = defaultdict(lambda: [0, 0.0])
    for r in run_query(cid, f"""SELECT campaign.id, geographic_view.location_type, segments.geo_target_city, metrics.cost_micros, metrics.all_conversions
      FROM geographic_view WHERE campaign.id = 21225221220 AND segments.date BETWEEN '{a}' AND '{b}'"""):
        k = (r["geographic_view"]["location_type"], r["segments"].get("geo_target_city", "?"))
        agg2[k][0] += int(r["metrics"]["cost_micros"]); agg2[k][1] += float(r["metrics"].get("all_conversions", 0))
    names = {}
    ids = sorted({k[1] for k in agg2 if k[1] != "?"})
    if ids:
        for r in run_query(cid, "SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.resource_name IN (%s)" % ",".join(f"'{i}'" for i in ids)):
            names[r["geo_target_constant"]["resource_name"]] = r["geo_target_constant"]["name"]
    print(f"  {a}..{b}")
    for k, v in sorted(agg2.items(), key=lambda kv: -kv[1][0])[:15]:
        print(f"    {k[0]:<22} {names.get(k[1], k[1])[:28]:<28} ${v[0]/1e6:7.2f} conv={v[1]:.1f}")
print("\n== PMax location criteria + negatives count")
for r in run_query(cid, """SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius,
  campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = 21225221220 AND campaign_criterion.type IN ('LOCATION','PROXIMITY','KEYWORD')"""):
    cc = r["campaign_criterion"]; cc["type"] = cc.get("type", cc.get("type_"))
    if cc["type"] != "KEYWORD": print("  ", cc["type"], "neg" if cc.get("negative") else "pos", cc.get("location", {}).get("geo_target_constant", ""), cc.get("proximity", {}).get("radius", ""))
print("  PMax neg keywords:", sum(1 for r in run_query(cid, "SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.id = 21225221220 AND campaign_criterion.type='KEYWORD' AND campaign_criterion.negative = TRUE")))
print("  NB neg keywords:", sum(1 for r in run_query(cid, "SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.id = 23825900343 AND campaign_criterion.type='KEYWORD' AND campaign_criterion.negative = TRUE")))
print("\n== ad calls (call_view) 10-13..10-25")
for r in sorted(run_query(cid, """SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, campaign.name FROM call_view
  WHERE call_view.start_call_date_time >= '2026-10-13 00:00:00' """), key=lambda r: r["call_view"]["start_call_date_time"]):
    c = r["call_view"]; print(f"  {c['start_call_date_time']} {c.get('call_duration_seconds',0):>4}s {c.get('call_status','')} {r.get('campaign',{}).get('name','')[:30]}")
