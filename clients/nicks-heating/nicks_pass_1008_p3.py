# READ-ONLY follow-ups on Nick's 1854100356
import os
import sys, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="1854100356"; M=lambda x:int(x or 0)/1e6
print("== keyword-level IS, 30d (branded + nonbranded)")
for r in run_query(CID, """SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions,
  metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.average_cpc FROM keyword_view
  WHERE segments.date DURING LAST_30_DAYS AND campaign.status='ENABLED' AND metrics.impressions > 0 ORDER BY metrics.impressions DESC"""):
    m=r["metrics"]; k=r["ad_group_criterion"]["keyword"]
    print(f"  {r['campaign']['name'][:28]:<28} {k['match_type']:<6} {k['text'][:38]:<38} impr {m.get('impressions'):>5} clk {m.get('clicks'):>3} ${M(m.get('cost_micros')):>5.0f} conv {float(m.get('conversions') or 0):.0f} IS {m.get('search_impression_share','-')} rankLost {m.get('search_rank_lost_impression_share','-')}")
print("== branded campaign search terms 30d, all rows")
for r in run_query(CID, """SELECT search_term_view.search_term, segments.keyword.info.text, metrics.cost_micros, metrics.clicks, metrics.conversions FROM search_term_view
  WHERE segments.date DURING LAST_30_DAYS AND campaign.id = 23675600637 AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC"""):
    m=r["metrics"]; print(f"  ${M(m.get('cost_micros')):>5.0f} clk {m.get('clicks')} conv {float(m.get('conversions') or 0):.0f}  {r['search_term_view']['search_term']}  <- kw '{r['segments'].get('keyword',{}).get('info',{}).get('text')}'")
print("== LSA charged leads: credit state 30d")
c=collections.Counter()
for r in run_query(CID, """SELECT local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.credit_details.credit_state, local_services_lead.creation_date_time
  FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-09-08 00:00:00'"""):
    l=r["local_services_lead"]; c[(l.get("lead_status"), l.get("lead_charged"), (l.get("credit_details") or {}).get("credit_state"))]+=1
for k,v in c.most_common(): print("  ",v,k)
print("== LSA leads by hour/day 30d (are any outside Mon-Fri 7-16?)")
h=collections.Counter()
import datetime
for r in run_query(CID, "SELECT local_services_lead.creation_date_time FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-09-08 00:00:00'"):
    t=datetime.datetime.strptime(r["local_services_lead"]["creation_date_time"][:19], "%Y-%m-%d %H:%M:%S")
    h[(t.strftime("%a"), t.hour)]+=1
print("  ", sorted(h.items()))
