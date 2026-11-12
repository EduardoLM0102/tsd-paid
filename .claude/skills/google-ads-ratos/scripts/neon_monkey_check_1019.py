"""Read-only: Neon Monkey 7953905280 one-week check (fu-028, 2026-10-19): conv by action since 10-13, campaign stats, bidding, search-term hygiene."""
from lib import run_query
cid = "7953905280"
print("== conversions by action+day since 10-10 (nonzero)")
rows = run_query(cid, """SELECT segments.date, segments.conversion_action_name, metrics.all_conversions, metrics.conversions
  FROM customer WHERE segments.date BETWEEN '2026-10-10' AND '2026-10-19'""")
for r in sorted(rows, key=lambda r: (r["segments"]["date"], r["segments"]["conversion_action_name"])):
    m = r["metrics"]
    if float(m.get("all_conversions", 0)):
        print(f"  {r['segments']['date']}  {r['segments']['conversion_action_name'][:40]:<40} all={float(m['all_conversions']):.1f} biddable={float(m['conversions']):.1f}")
print("\n== campaigns: status/bidding/budget")
rows = run_query(cid, """SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.manual_cpc.enhanced_cpc_enabled,
  campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.status != 'REMOVED' AND campaign.status='ENABLED'""")
for r in rows:
    c = r["campaign"]; print(" ", c["id"], c["name"], c["status"], c.get("bidding_strategy_type"), "budget=$%.0f" % (int(r["campaign_budget"]["amount_micros"])/1e6))
for label, a, b in [("last 7d (10-12..10-18)", "2026-10-12", "2026-10-18"), ("since 10-13", "2026-10-13", "2026-10-18")]:
    print(f"\n== campaign stats {label}")
    rows = run_query(cid, f"""SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.average_cpc, metrics.conversions, metrics.all_conversions,
      metrics.search_impression_share FROM campaign WHERE segments.date BETWEEN '{a}' AND '{b}' AND campaign.status='ENABLED'""")
    for r in rows:
        m = r["metrics"]
        print(f"  {r['campaign']['name'][:34]:<34} cost=${int(m['cost_micros'])/1e6:,.0f} clicks={m['clicks']} cpc=${int(m.get('average_cpc',0))/1e6:.2f} conv={float(m['conversions']):.1f} all={float(m['all_conversions']):.1f} IS={m.get('search_impression_share')}")
print("\n== NB search terms since 10-13 (top 25 by cost)")
rows = run_query(cid, """SELECT search_term_view.search_term, campaign.name, metrics.cost_micros, metrics.clicks, metrics.all_conversions
  FROM search_term_view WHERE segments.date BETWEEN '2026-10-13' AND '2026-10-18' ORDER BY metrics.cost_micros DESC LIMIT 25""")
for r in rows:
    m = r["metrics"]; print(f"  ${int(m['cost_micros'])/1e6:6.0f} clk={m['clicks']:>3} conv={float(m['all_conversions']):.1f}  {r['search_term_view']['search_term'][:50]:<50} [{r['campaign']['name'][:18]}]")
