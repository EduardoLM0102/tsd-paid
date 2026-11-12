# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-11-04: can Google Search absorb the Meta budget (~$7,850/mo) for Angela's revised
budget proposal (Meta removed, TSD doesn't manage it)? Pulls Branded + Nonbranded IS / budget-lost / rank-lost / CPC over
30d and 7d, Nonbranded keywords, and campaign geo targets (for the Keyword Planner run)."""
import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB = "23690645223", "23832838033"
NAMES = {BR: "Branded", NB: "Nonbranded"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

for label, win, days in (("30d 10-05..11-03", "segments.date BETWEEN '2026-10-05' AND '2026-11-03'", 30),
                         ("7d 10-28..11-03", "segments.date BETWEEN '2026-10-28' AND '2026-11-03'", 7)):
    print(f"===== {label}")
    for r in q(f"""SELECT campaign.id, campaign_budget.amount_micros, campaign.maximize_conversions.target_cpa_micros,
        metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_top_impression_share FROM campaign WHERE {win} AND campaign.id IN ({BR},{NB})"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); im = int(m.get("impressions", 0))
        IS = F(m.get("search_impression_share"))
        print(f"{NAMES[c['id']]:<11} budget ${M(r['campaign_budget'].get('amount_micros')):.0f}/d tCPA {M(c.get('maximize_conversions',{}).get('target_cpa_micros'))} | "
              f"${sp:,.0f} (${sp/days:.0f}/d) clk {cl} impr {im} CPC ${sp/cl if cl else 0:.2f} | IS {IS*100:.1f} top {F(m.get('search_top_impression_share'))*100:.1f} "
              f"budget-lost {F(m.get('search_budget_lost_impression_share'))*100:.1f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.1f} "
              f"| eligible impr ~{im/IS if IS else 0:,.0f}")

print("\n===== Nonbranded keywords (enabled)")
for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM keyword_view WHERE campaign.id = {NB} AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'
    AND segments.date DURING LAST_30_DAYS"""):
    print(f"  {r['ad_group']['name']:<25} {r['ad_group_criterion']['keyword']['match_type']:<7} {r['ad_group_criterion']['keyword']['text']}")

print("\n===== geo targets Nonbranded")
for r in q(f"""SELECT campaign_criterion.location.geo_target_constant, campaign_criterion.negative, campaign_criterion.proximity.radius
    FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"""):
    print(" ", r["campaign_criterion"])
