# READ-ONLY. 2026-11-16 deep dive, main PPC account 4571881760.
import sys, collections
sys.path.insert(0, ".")
from lib import run_query
PPC="4571881760"; NB="24047025253"; BR="23675636592"; PM="22890783804"
M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0); pct=lambda x:f"{F(x)*100:.0f}%"
def q(s):
    try: return run_query(PPC,s)
    except BaseException as e: print("  ERR", str(e).splitlines()[0][:220]); return []

print("\n===== 5. NB keyword metrics 11-12..11-16")
for r in q(f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.average_cpc, metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_top_impression_share FROM keyword_view WHERE campaign.id={NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-16' AND metrics.impressions>0 ORDER BY metrics.impressions DESC"):
    k=r['ad_group_criterion']; m=r['metrics']
    print(f"  {k['keyword']['text'][:34]:34s} [{k['keyword']['match_type'][:5]}] impr {m.get('impressions',0):>4} clk {m.get('clicks',0):>2} ${M(m.get('cost_micros')):6.2f} cpc ${M(m.get('average_cpc')):.2f} IS {pct(m.get('search_impression_share'))} lost-rank {pct(m.get('search_rank_lost_impression_share'))} top {pct(m.get('search_top_impression_share'))}")

print("\n===== 6. NB search terms 11-12..11-16 (all)")
for r in q(f"SELECT search_term_view.search_term, search_term_view.status, segments.keyword.info.text, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE campaign.id={NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-16' ORDER BY metrics.impressions DESC"):
    s=r['search_term_view']; m=r['metrics']
    print(f"  {s['search_term'][:44]:44s} <- {r['segments'].get('keyword',{}).get('info',{}).get('text','')[:24]:24s} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} {s.get('status','')}")

print("\n===== 7. NB by hour / day / device 11-12..11-16")
for seg in ('hour','day_of_week','device'):
    agg=collections.defaultdict(lambda:[0,0,0.0])
    for r in q(f"SELECT segments.{seg}, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE campaign.id={NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-16'"):
        a=agg[r['segments'][seg]]; a[0]+=int(r['metrics'].get('impressions',0)); a[1]+=int(r['metrics'].get('clicks',0)); a[2]+=M(r['metrics'].get('cost_micros'))
    print(f"  {seg}: " + " | ".join(f"{k}:{v[0]}i/{v[1]}c/${v[2]:.0f}" for k,v in sorted(agg.items(), key=lambda kv: str(kv[0]))))

print("\n===== 8. NB geo (city) 11-12..11-16")
geo=collections.defaultdict(lambda:[0,0,0.0]); ids=set()
for r in q(f"SELECT segments.geo_target_city, geographic_view.location_type, metrics.impressions, metrics.clicks, metrics.cost_micros FROM geographic_view WHERE campaign.id={NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-16'"):
    cid=str(r['segments'].get('geo_target_city','?')).split('/')[-1]; ids.add(cid); a=geo[(cid,r['geographic_view']['location_type'][:3])]
    a[0]+=int(r['metrics'].get('impressions',0)); a[1]+=int(r['metrics'].get('clicks',0)); a[2]+=M(r['metrics'].get('cost_micros'))
names={}
ids={i for i in ids if i.isdigit()}
if ids:
    for r in q(f"SELECT geo_target_constant.id, geo_target_constant.name, geo_target_constant.canonical_name FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"):
        g=r['geo_target_constant']; names[str(g['id'])]=g.get('canonical_name',g['name'])[:40]
for k,v in sorted(geo.items(), key=lambda kv:-kv[1][0])[:25]:
    print(f"  {names.get(k[0],k[0])[:40]:40s} {k[1]} impr {v[0]:>3} clk {v[1]} ${v[2]:.2f}")

print("\n===== 9. Branded 11-01..11-16 daily IS")
tot=[0.0,0,0]
for r in q(f"SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share, metrics.search_absolute_top_impression_share, metrics.conversions FROM campaign WHERE campaign.id={BR} AND segments.date BETWEEN '2026-11-01' AND '2026-11-16'"):
    m=r['metrics']; tot[0]+=M(m.get('cost_micros')); tot[1]+=int(m.get('impressions',0)); tot[2]+=int(m.get('clicks',0))
    print(f"  {r['segments']['date']} ${M(m.get('cost_micros')):5.2f} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} cpc ${M(m.get('average_cpc')):.2f} IS {pct(m.get('search_impression_share'))} lost-bud {pct(m.get('search_budget_lost_impression_share'))} lost-rank {pct(m.get('search_rank_lost_impression_share'))} abs-top {pct(m.get('search_absolute_top_impression_share'))} conv {F(m.get('conversions')):.0f}")
print(f"  TOTAL ${tot[0]:.2f} impr {tot[1]} clk {tot[2]}")
for r in q(f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros FROM keyword_view WHERE campaign.id={BR} AND segments.date BETWEEN '2026-11-01' AND '2026-11-16' AND metrics.impressions>0 ORDER BY metrics.impressions DESC"):
    k=r['ad_group_criterion']; m=r['metrics']; print(f"    kw {k['keyword']['text'][:30]:30s} [{k['keyword']['match_type'][:5]}] impr {m.get('impressions',0)} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== 10. Ad calls (call_view) since 11-01")
for r in q("SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.type, call_view.caller_area_code, call_view.call_tracking_display_location, campaign.name FROM call_view WHERE segments.date BETWEEN '2026-11-01' AND '2026-11-16'"):
    c=r['call_view']; print(f"  {c.get('start_call_date_time','')[:16]} {c.get('call_duration_seconds',0):>4}s {c.get('call_status','')[:8]:8s} {c.get('type','')[:14]:14s} {c.get('call_tracking_display_location','')[:12]:12s} area {c.get('caller_area_code','')} {r['campaign']['name'][:30]}")

print("\n===== 11. Conversion actions (status, primary, 30d all_conv)")
rows=q("SELECT conversion_action.id, conversion_action.name, conversion_action.status, conversion_action.type, conversion_action.category, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.counting_type, metrics.all_conversions FROM conversion_action WHERE segments.date BETWEEN '2026-10-17' AND '2026-11-16'")
if not rows: rows=q("SELECT conversion_action.id, conversion_action.name, conversion_action.status, conversion_action.type, conversion_action.category, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.counting_type FROM conversion_action")
for r in rows:
    c=r['conversion_action']; 
    if c['status']!='ENABLED': continue
    print(f"  {c['id']} {c['name'][:42]:42s} {c['type'][:22]:22s} {c['category'][:16]:16s} primary={c.get('primary_for_goal')} inConv={c.get('include_in_conversions_metric')} {c.get('counting_type','')[:8]} 30d={F(r.get('metrics',{}).get('all_conversions')):.0f}")

print("\n===== 12. Last heating season (2025-11..2026-03) monthly by campaign, cost>0")
for r in q("SELECT campaign.name, campaign.advertising_channel_type, segments.month, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2025-11-01' AND '2026-03-31' AND metrics.cost_micros>0 ORDER BY segments.month"):
    m=r['metrics']; print(f"  {r['segments']['month']} {r['campaign']['name'][:40]:40s} {r['campaign']['advertising_channel_type'][:8]:8s} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>5} conv {F(m.get('conversions')):.0f} all {F(m.get('all_conversions')):.0f}")
print("  -- conversions by action (excl page_view), last season")
agg=collections.defaultdict(float)
for r in q("SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2025-11-01' AND '2026-03-31' AND metrics.all_conversions>0"):
    n=r['segments']['conversion_action_name']
    if 'page_view' in n: continue
    agg[(r['campaign']['name'][:34], n[:40])]+=F(r['metrics'].get('all_conversions'))
for k,v in sorted(agg.items(), key=lambda kv:-kv[1])[:30]: print(f"    {k[0]:34s} {k[1]:40s} {v:.0f}")

print("\n===== 13. Assets on NB/BR + account level (call, sitelink, callout)")
for r in q(f"SELECT campaign.id, campaign_asset.field_type, campaign_asset.status, asset.call_asset.phone_number, asset.sitelink_asset.link_text, asset.callout_asset.callout_text, asset.structured_snippet_asset.header FROM campaign_asset WHERE campaign.id IN ({NB},{BR}) AND campaign_asset.status!='REMOVED'"):
    a=r['asset']; print(f"  camp {r['campaign']['id']} {r['campaign_asset']['field_type']:18s} {a.get('call_asset',{}).get('phone_number','')} {a.get('sitelink_asset',{}).get('link_text','')} {a.get('callout_asset',{}).get('callout_text','')} {a.get('structured_snippet_asset',{}).get('header','')}")
for r in q("SELECT customer_asset.field_type, customer_asset.status, asset.call_asset.phone_number, asset.sitelink_asset.link_text, asset.callout_asset.callout_text FROM customer_asset WHERE customer_asset.status!='REMOVED'"):
    a=r['asset']; print(f"  acct {r['customer_asset']['field_type']:18s} {a.get('call_asset',{}).get('phone_number','')} {a.get('sitelink_asset',{}).get('link_text','')} {a.get('callout_asset',{}).get('callout_text','')}")
for r in q(f"SELECT ad_group.id, ad_group_asset.field_type, ad_group_asset.status, asset.call_asset.phone_number, asset.sitelink_asset.link_text, asset.callout_asset.callout_text FROM ad_group_asset WHERE campaign.id IN ({NB},{BR}) AND ad_group_asset.status!='REMOVED'"):
    a=r['asset']; print(f"  adg {r['ad_group']['id']} {r['ad_group_asset']['field_type']:18s} {a.get('call_asset',{}).get('phone_number','')} {a.get('sitelink_asset',{}).get('link_text','')} {a.get('callout_asset',{}).get('callout_text','')}")

print("\n===== 14. NB RSA headlines/descriptions + strength")
for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions FROM ad_group_ad WHERE campaign.id={NB} AND ad_group_ad.status='ENABLED'"):
    a=r['ad_group_ad']; rsa=a['ad'].get('responsive_search_ad',{})
    print(f"  ad {a['ad']['id']} {a.get('ad_strength')} {a['policy_summary']['approval_status']} {a['ad'].get('final_urls')}")
    print("   H:", " | ".join(h['text'] for h in rsa.get('headlines',[])))
    print("   D:", " | ".join(d['text'] for d in rsa.get('descriptions',[])))

print("\n===== 15. Change events 11-11..11-16")
for r in q("SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-11 00:00:00' AND '2026-11-16 23:59:59' ORDER BY change_event.change_date_time LIMIT 60"):
    c=r['change_event']; print(f"  {c['change_date_time'][:16]} {c.get('user_email','')[:28]:28s} {c['change_resource_type'][:20]:20s} {c['resource_change_operation'][:6]} {str(c.get('changed_fields',''))[:70]} {str(c.get('campaign','')).split('/')[-1]}")
