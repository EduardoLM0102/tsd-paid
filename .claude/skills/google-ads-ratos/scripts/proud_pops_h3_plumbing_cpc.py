"""
Checklist H3 (read-only): Search Plumbing 23853484024 cost-per-click control.
- daily trend (spend vs budget, clicks, avg CPC, IS)
- exact single-click prices from search-term-days with exactly 1 click -> CPC distribution + the priciest clicks
- keyword-level avg CPC, QS components, and where the expensive clicks come from
- today's $103 click: hour + term
"""
import sys, os, datetime
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, CAMP = "1051843378", "23853484024"
today = datetime.date.today()
S60, S30, U = (today - datetime.timedelta(days=60)).isoformat(), (today - datetime.timedelta(days=30)).isoformat(), today.isoformat()
f = lambda x: float(x or 0)

print("== bidding + budget")
for r in run_query(CID, f"""SELECT campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.maximize_conversions.target_cpa_micros,
campaign_budget.amount_micros FROM campaign WHERE campaign.id = {CAMP}"""):
    print("   ", r["campaign"].get("bidding_strategy_type"), "| portfolio:", r["campaign"].get("bidding_strategy", "none"),
          "| tCPA $", f(r["campaign"].get("maximize_conversions", {}).get("target_cpa_micros")) / 1e6, "| budget $", f(r["campaign_budget"]["amount_micros"]) / 1e6, "/day")

print(f"\n== daily, last 30 days")
tot = [0.0, 0.0, 0.0]
for r in sorted(run_query(CID, f"""SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions,
metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S30}' AND '{U}'"""), key=lambda r: r["segments"]["date"]):
    m = r["metrics"]; c = f(m.get("cost_micros")) / 1e6; k = f(m.get("clicks"))
    tot[0] += c; tot[1] += k; tot[2] += f(m.get("all_conversions"))
    p = lambda x: f"{f(m.get(x)) * 100:3.0f}%" if m.get(x) is not None else "  - "
    print(f"   {r['segments']['date']}  ${c:6.0f}  clk {k:3.0f}  cpc ${c / k if k else 0:6.2f}  impr {m.get('impressions', 0):>4}  IS {p('search_impression_share')} lostBud {p('search_budget_lost_impression_share')} lostRank {p('search_rank_lost_impression_share')}")
print(f"   30d: ${tot[0]:,.0f}, {tot[1]:.0f} clicks, avg CPC ${tot[0] / tot[1]:.2f}, all_conv {tot[2]:.1f}")

print(f"\n== exact single-click prices (search-term-days with exactly 1 click), last 60 days")
singles = []
for r in run_query(CID, f"""SELECT segments.date, search_term_view.search_term, segments.keyword.info.text, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S60}' AND '{U}' AND metrics.clicks = 1"""):
    singles.append((f(r["metrics"]["cost_micros"]) / 1e6, r["segments"]["date"], r["search_term_view"]["search_term"],
                    r["segments"].get("keyword", {}).get("info", {}).get("text", "?"), f(r["metrics"].get("all_conversions"))))
B = [(0, 20), (20, 40), (40, 60), (60, 100), (100, 10_000)]
n = len(singles); sc = sum(x[0] for x in singles)
print(f"   {n} single clicks, ${sc:,.0f}, median ${sorted(x[0] for x in singles)[n // 2] if n else 0:.2f}")
for lo, hi in B:
    xs = [x for x in singles if lo <= x[0] < hi]
    print(f"   ${lo:>3}-{hi if hi < 10000 else '+':<4}  {len(xs):3d} clicks ({len(xs) / n * 100:4.1f}%)  ${sum(x[0] for x in xs):7,.0f} ({sum(x[0] for x in xs) / sc * 100:4.1f}% of single-click spend)  all_conv {sum(x[4] for x in xs):.1f}")
print("   priciest single clicks:")
for x in sorted(singles, reverse=True)[:15]:
    print(f"     ${x[0]:7.2f}  {x[1]}  '{x[2]}'  <- keyword '{x[3]}'  all_conv {x[4]:.1f}")

print(f"\n== keywords, last 30 days (avg CPC, QS)")
for r in sorted(run_query(CID, f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.search_predicted_ctr,
ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.post_click_quality_score,
metrics.clicks, metrics.cost_micros, metrics.all_conversions FROM keyword_view
WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S30}' AND '{U}' AND metrics.clicks > 0"""), key=lambda r: -f(r["metrics"]["cost_micros"])):
    k = r["ad_group_criterion"]; q = k.get("quality_info", {}); m = r["metrics"]; c = f(m["cost_micros"]) / 1e6; cl = f(m["clicks"])
    print(f"   ${c:6.0f} clk {cl:3.0f} cpc ${c / cl:6.2f} conv {f(m.get('all_conversions')):4.1f}  QS {q.get('quality_score', '-')} "
          f"(ctr {str(q.get('search_predicted_ctr', '-'))[:5]}/ad {str(q.get('creative_quality_score', '-'))[:5]}/lp {str(q.get('post_click_quality_score', '-'))[:5]})  "
          f"{k['keyword']['match_type']:6s} {k['keyword']['text']}  [{r['ad_group']['name']}]")

print(f"\n== today ({U}) by hour")
for r in sorted(run_query(CID, f"""SELECT segments.hour, metrics.clicks, metrics.cost_micros, metrics.impressions FROM campaign
WHERE campaign.id = {CAMP} AND segments.date = '{U}'"""), key=lambda r: int(r["segments"]["hour"])):
    m = r["metrics"]
    if f(m.get("cost_micros")) or f(m.get("clicks")):
        print(f"   {int(r['segments']['hour']):02d}h CT  clicks {m.get('clicks', 0)}  ${f(m.get('cost_micros')) / 1e6:.2f}  impr {m.get('impressions', 0)}")
for r in run_query(CID, f"""SELECT search_term_view.search_term, segments.keyword.info.text, metrics.clicks, metrics.cost_micros FROM search_term_view
WHERE campaign.id = {CAMP} AND segments.date = '{U}' AND metrics.cost_micros > 0"""):
    print(f"   today term: '{r['search_term_view']['search_term']}' <- '{r['segments'].get('keyword', {}).get('info', {}).get('text', '?')}'  clk {r['metrics']['clicks']}  ${f(r['metrics']['cost_micros']) / 1e6:.2f}")
