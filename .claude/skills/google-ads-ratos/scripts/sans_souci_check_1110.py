from lib import run_query
C="1723283029"
def q(s): return run_query(C,s)
print("== Campaign config")
for r in q("SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.status='ENABLED'"):
    c=r['campaign']; print(c['name'],c['status'],c.get('bidding_strategy_type'),int(c.get('maximize_conversions',{}).get('target_cpa_micros',0))/1e6, int(r['campaign_budget']['amount_micros'])/1e6)
print("== Weekly (Mon-Sun)")
rows=q("SELECT segments.week, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share FROM campaign WHERE segments.date BETWEEN '2026-09-29' AND '2026-11-09' AND campaign.status='ENABLED'")
for r in sorted(rows,key=lambda x:x['segments']['week']):
    m=r['metrics']; cost=int(m.get('cost_micros',0))/1e6; cv=float(m.get('conversions',0))
    print(r['segments']['week'], f"${cost:.0f}", m.get('clicks'), m.get('impressions'), f"conv {cv:.1f}", f"CPL ${cost/cv if cv else 0:.2f}", f"allconv {float(m.get('all_conversions',0)):.1f}", "IS",m.get('search_impression_share'),"lostRank",m.get('search_rank_lost_impression_share'),"lostBud",m.get('search_budget_lost_impression_share'))
print("== Weekly by conversion action")
rows=q("SELECT segments.week, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2026-09-29' AND '2026-11-09' AND campaign.status='ENABLED'")
for r in sorted(rows,key=lambda x:(x['segments']['week'],x['segments']['conversion_action_name'])):
    m=r['metrics']; print(r['segments']['week'], r['segments']['conversion_action_name'], f"conv {float(m.get('conversions',0)):.1f} all {float(m.get('all_conversions',0)):.1f}")
print("== Daily last 14")
rows=q("SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-10-27' AND '2026-11-09' AND campaign.status='ENABLED'")
for r in sorted(rows,key=lambda x:x['segments']['date']):
    m=r['metrics']; print(r['segments']['date'], f"${int(m.get('cost_micros',0))/1e6:.2f}", m.get('clicks'), f"{float(m.get('conversions',0)):.1f}")
print("== Change events since 10-27")
try:
  for r in q("SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields FROM change_event WHERE change_event.change_date_time >= '2026-10-27' ORDER BY change_event.change_date_time DESC LIMIT 50"):
    e=r['change_event']; print(e.get('change_date_time'),e.get('user_email'),e.get('change_resource_type'),e.get('resource_change_operation'),e.get('changed_fields'))
except Exception as ex: print("change_event err",ex)
