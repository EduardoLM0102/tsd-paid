import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import defaultdict
CID = "1051843378"
for camp in ("TSD_05.14_Leads_Pmax_HVAC", "TSD_05.20_PMax_Electrical"):
    print("==", camp, "weekly network split: cost (share) / Website lead all_conv")
    cost = defaultdict(lambda: defaultdict(float)); forms = defaultdict(lambda: defaultdict(float))
    for r in run_query(CID, f"""
SELECT campaign.name, segments.week, segments.ad_network_type, metrics.cost_micros
FROM campaign WHERE campaign.name = '{camp}' AND segments.date BETWEEN '2026-07-20' AND '2026-10-06'"""):
        cost[r['segments']['week']][str(r['segments']['ad_network_type'])] += float(r['metrics'].get('cost_micros', 0) or 0)/1e6
    for r in run_query(CID, f"""
SELECT campaign.name, segments.week, segments.ad_network_type, segments.conversion_action_name, metrics.all_conversions
FROM campaign WHERE campaign.name = '{camp}' AND segments.date BETWEEN '2026-07-20' AND '2026-10-06'"""):
        if r['segments'].get('conversion_action_name') == 'Website lead':
            forms[r['segments']['week']][str(r['segments']['ad_network_type'])] += float(r['metrics'].get('all_conversions', 0) or 0)
    for w in sorted(cost):
        tot = sum(cost[w].values()) or 1
        parts = "  ".join(f"{n[:7]} ${c:,.0f}({c/tot*100:.0f}%)/{forms[w].get(n,0):.0f}f" for n, c in sorted(cost[w].items(), key=lambda x: -x[1]) if c > 1)
        print(f"  {w}  {parts}")
print("== bidding")
for r in run_query(CID, """
SELECT campaign.name, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign.status
FROM campaign WHERE campaign.status = 'ENABLED'"""):
    c = r['campaign']; print("  ", c['name'], c.get('bidding_strategy_type'), float(c.get('maximize_conversions', {}).get('target_cpa_micros', 0) or 0)/1e6)
