import sys
from lib import run_query
M='4571881760'
q=f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, segments.date,
metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2026-11-12' AND '2026-11-15' AND metrics.impressions > 0"""
print("== MAIN 4571881760 by day")
for r in run_query(M,q):
    c=r['campaign'];m=r['metrics'];d=r['segments']['date']
    print(d, c['name'][:40], c['status'], round(int(m.get('cost_micros',0))/1e6,2), m.get('impressions'), m.get('clicks'), m.get('conversions',0))
q2="""SELECT segments.conversion_action_name, campaign.name, segments.date, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2026-11-12' AND '2026-11-15' AND metrics.all_conversions > 0"""
print("== conv by action")
for r in run_query(M,q2):
    print(r['segments']['date'], r['campaign']['name'][:35], r['segments']['conversion_action_name'], r['metrics'].get('conversions',0), r['metrics'].get('all_conversions',0))
q3="""SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view
WHERE campaign.id = 24047025253 AND segments.date BETWEEN '2026-11-12' AND '2026-11-15' AND metrics.clicks > 0"""
print("== NB search terms w/ clicks")
for r in run_query(M,q3):
    print(r['search_term_view']['search_term'], r['metrics'].get('clicks'), round(int(r['metrics'].get('cost_micros',0))/1e6,2), r['metrics'].get('conversions',0))
for acct,name in [('2895702982','Belleville'),('8323145223','Englewood'),('2175964343','Carlstadt')]:
    print("== LSA",name)
    try:
        for r in run_query(acct,"""SELECT campaign.name, campaign.advertising_channel_type, segments.date, metrics.cost_micros, metrics.impressions, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-11-09' AND '2026-11-15' AND metrics.impressions > 0"""):
            print(r['segments']['date'], r['campaign']['name'][:30], round(int(r['metrics'].get('cost_micros',0))/1e6,2), r['metrics'].get('impressions'))
        for r in run_query(acct,"""SELECT local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time, local_services_lead.category_id FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-09 00:00:00'"""):
            l=r['local_services_lead']; print('  LEAD', l.get('creation_date_time'), l.get('lead_type'), l.get('lead_status'), 'charged' if l.get('lead_charged') else 'free', l.get('category_id'))
    except Exception as e: print('ERR', str(e)[:200])
