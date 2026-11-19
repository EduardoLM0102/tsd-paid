# READ-ONLY budgets for Napps review
import sys; sys.path.insert(0, ".")
from lib import run_query
for cid in ("9509605037","9239407401"):
    for r in run_query(cid, "SELECT campaign.name, campaign.status, campaign_budget.amount_micros, campaign_budget.period, campaign_budget.type FROM campaign WHERE campaign.status = 'ENABLED'"):
        print(cid, r['campaign']['name'][:45], r['campaignBudget'] if 'campaignBudget' in r else r['campaign_budget'])
    for r in run_query(cid, "SELECT segments.date, metrics.cost_micros, metrics.search_budget_lost_impression_share FROM campaign WHERE segments.date BETWEEN '2026-11-11' AND '2026-11-17' AND campaign.advertising_channel_type = 'LOCAL_SERVICES'") if cid=="9239407401" else []:
        print('  ', r['segments']['date'], int(r['metrics'].get('cost_micros',0))/1e6)
