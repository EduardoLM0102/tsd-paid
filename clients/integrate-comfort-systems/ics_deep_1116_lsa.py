# READ-ONLY. 2026-11-16 deep dive, ICS LSA accounts + Mitsubishi YouTube.
import sys, collections
sys.path.insert(0, ".")
from lib import run_query
LSA={"2175964343":"Carlstadt","8323145223":"Englewood"}
M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0)
def q(cid,s):
    try: return run_query(cid,s)
    except BaseException as e: print("  ERR", str(e).splitlines()[0][:220]); return []

for cid,name in LSA.items():
    print(f"\n######## {name} {cid}")
    for r in q(cid,"SELECT customer.descriptive_name, customer.status, customer.currency_code, customer.time_zone FROM customer"):
        print("  customer:", r['customer'])
    print("  -- LSA campaign settings")
    for r in q(cid,"SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign_budget.period, campaign.local_services_campaign_settings.category_bids FROM campaign WHERE campaign.advertising_channel_type='LOCAL_SERVICES'"):
        c=r['campaign']; print(f"    {c['id']} {c['status']} {c.get('primary_status')} {c.get('primary_status_reasons')} bid={c['bidding_strategy_type']} budget=${M(r['campaign_budget']['amount_micros']):.2f} period={r['campaign_budget'].get('period')}")
        for cb in c.get('local_services_campaign_settings',{}).get('category_bids',[]):
            print(f"      cat {cb.get('category_id','').replace('xcat:service_area_business_','')} manual_cpa=${M(cb.get('manual_cpa_bid_micros')):.2f} target_cpa=${M(cb.get('target_cpa_bid_micros')):.2f} enum={cb.get('enum_bid')}")
    print("  -- geo criteria")
    locs=[]
    for r in q(cid,"SELECT campaign_criterion.negative, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.advertising_channel_type='LOCAL_SERVICES' AND campaign_criterion.type='LOCATION'"):
        cc=r['campaign_criterion']; locs.append(("-" if cc.get('negative') else "+")+str(cc['location']['geo_target_constant']).split('/')[-1])
    ids=[l[1:] for l in locs]
    names={}
    if ids:
        for r in q(cid,f"SELECT geo_target_constant.id, geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"):
            g=r['geo_target_constant']; names[str(g['id'])]=f"{g['name']}({g['target_type'][:4]})"
    print("    "+", ".join(l[0]+names.get(l[1:],l[1:]) for l in locs)[:900])
    print("  -- verification artifacts")
    for r in q(cid,"SELECT local_services_verification_artifact.id, local_services_verification_artifact.artifact_type, local_services_verification_artifact.status, local_services_verification_artifact.creation_date_time, local_services_verification_artifact.license_verification_artifact.license_type, local_services_verification_artifact.license_verification_artifact.license_number, local_services_verification_artifact.insurance_verification_artifact.amount_micros, local_services_verification_artifact.license_verification_artifact.rejection_reason, local_services_verification_artifact.insurance_verification_artifact.rejection_reason FROM local_services_verification_artifact"):
        v=r['local_services_verification_artifact']; print(f"    {v.get('creation_date_time','')[:10]} {v.get('artifact_type','')[:10]:10s} {v.get('status','?')[:12]:12s} {v.get('license_verification_artifact',{}).get('license_type','')} {v.get('license_verification_artifact',{}).get('license_number','')} ins=${M(v.get('insurance_verification_artifact',{}).get('amount_micros')):.0f} rej={v.get('license_verification_artifact',{}).get('rejection_reason','') or v.get('insurance_verification_artifact',{}).get('rejection_reason','')}")
    print("  -- employees")
    for r in q(cid,"SELECT local_services_employee.id, local_services_employee.status, local_services_employee.job_title, local_services_employee.creation_date_time FROM local_services_employee"):
        e=r['local_services_employee']; print(f"    {e.get('id')} {e.get('status')} {e.get('job_title','')} {e.get('creation_date_time','')[:10]}")
    print("  -- daily 11-01..11-16 (LSA campaign only)")
    for r in q(cid,"SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions FROM campaign WHERE campaign.advertising_channel_type='LOCAL_SERVICES' AND segments.date BETWEEN '2026-11-01' AND '2026-11-16' AND metrics.impressions>0"):
        m=r['metrics']; print(f"    {r['segments']['date']} impr {m.get('impressions',0):>4} clk {m.get('clicks',0):>3} ${M(m.get('cost_micros')):.2f} allconv {F(m.get('all_conversions')):.0f}")
    print("  -- monthly 2025-10..2026-11 (LSA campaign)")
    for r in q(cid,"SELECT segments.month, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE campaign.advertising_channel_type='LOCAL_SERVICES' AND segments.date BETWEEN '2025-10-01' AND '2026-11-16' ORDER BY segments.month"):
        m=r['metrics']; print(f"    {r['segments']['month']} impr {m.get('impressions',0):>5} clk {m.get('clicks',0):>4} ${M(m.get('cost_micros')):8.2f}")
    print("  -- leads by month since 2025-10 (type/charged)")
    leads=q(cid,"SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time, local_services_lead.locale FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2025-10-01 00:00:00'")
    bym=collections.defaultdict(lambda:[0,0,collections.Counter()])
    for l in leads:
        x=l['local_services_lead']; mth=x['creation_date_time'][:7]; bym[mth][0]+=1; bym[mth][1]+= 1 if x.get('lead_charged') else 0; bym[mth][2][x['lead_type']]+=1
    for mth in sorted(bym): print(f"    {mth} leads {bym[mth][0]} charged {bym[mth][1]} {dict(bym[mth][2])}")
    print("  -- leads since 11-01 detail")
    for l in sorted(leads, key=lambda l:l['local_services_lead']['creation_date_time']):
        x=l['local_services_lead']
        if x['creation_date_time']>='2026-11-01': print(f"    {x['creation_date_time'][:16]} {x['lead_type']:12s} {x['category_id'].replace('xcat:service_area_business_','')[:12]:12s} {x['lead_status']:16s} charged={x.get('lead_charged',False)}")
    print("  -- change events 11-01..11-16")
    for r in q(cid,"SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-01 00:00:00' AND '2026-11-16 23:59:59' ORDER BY change_event.change_date_time LIMIT 40"):
        c=r['change_event']; print(f"    {c['change_date_time'][:16]} {c.get('user_email','')[:28]:28s} {c['change_resource_type'][:20]:20s} {c['resource_change_operation'][:6]} {str(c.get('changed_fields',''))[:80]} {str(c.get('campaign','')).split('/')[-1]}")

print("\n######## Mitsubishi YouTube 23599485735 (Belleville acct)")
B="2895702982"; YT="23599485735"
for r in q(B,f"SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_cpm.target_frequency_goal.target_count, campaign_budget.amount_micros, campaign.start_date, campaign.end_date, campaign.video_campaign_settings.video_ad_sequence_control_settings, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id={YT}"):
    c=r['campaign']; print(f"  {c['status']} bid={c['bidding_strategy_type']} budget=${M(r['campaign_budget']['amount_micros']):.2f}/d start={c.get('start_date')} end={c.get('end_date')} geo={c['geo_target_type_setting'].get('positive_geo_target_type')}")
for r in q(B,f"SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.type FROM ad_group WHERE campaign.id={YT}"):
    print("  adgroup", r['ad_group'])
crit=collections.Counter()
for r in q(B,f"SELECT ad_group_criterion.type, ad_group_criterion.status, ad_group_criterion.negative FROM ad_group_criterion WHERE campaign.id={YT} AND ad_group_criterion.status!='REMOVED'"):
    c=r['ad_group_criterion']; crit[(c.get('type') or c.get('type_'), bool(c.get('negative')))]+=1
print("  adgroup criteria:", dict(crit))
crit=collections.Counter()
for r in q(B,f"SELECT campaign_criterion.type, campaign_criterion.negative FROM campaign_criterion WHERE campaign.id={YT}"):
    c=r['campaign_criterion']; crit[(c.get('type') or c.get('type_'), bool(c.get('negative')))]+=1
print("  campaign criteria:", dict(crit))
for r in q(B,f"SELECT ad_group_criterion.user_list.user_list, ad_group_criterion.user_interest.user_interest_category, ad_group_criterion.custom_audience.custom_audience, ad_group_criterion.keyword.text, ad_group_criterion.topic.path, ad_group_criterion.type FROM ad_group_criterion WHERE campaign.id={YT} AND ad_group_criterion.status!='REMOVED' AND ad_group_criterion.type IN ('USER_LIST','USER_INTEREST','CUSTOM_AUDIENCE','KEYWORD','TOPIC','PLACEMENT','YOUTUBE_VIDEO','YOUTUBE_CHANNEL')"):
    print("    tgt", {k:v for k,v in r['ad_group_criterion'].items() if k not in ('resource_name',)})
for r in q(B,f"SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.clicks, metrics.all_conversions FROM campaign WHERE campaign.id={YT} AND segments.date BETWEEN '2026-10-17' AND '2026-11-16'"):
    pass
tot=collections.defaultdict(float)
for r in q(B,f"SELECT segments.device, metrics.cost_micros, metrics.impressions, metrics.video_views, metrics.clicks FROM campaign WHERE campaign.id={YT} AND segments.date BETWEEN '2026-10-17' AND '2026-11-16'"):
    m=r['metrics']; d=r['segments']['device']; tot[d+'_cost']+=M(m.get('cost_micros')); tot[d+'_impr']+=int(m.get('impressions',0)); tot[d+'_views']+=int(m.get('video_views',0)); tot[d+'_clicks']+=int(m.get('clicks',0))
print("  30d by device:", {k:round(v,2) for k,v in tot.items()})
for r in q(B,f"SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.video_ad.video.asset, ad_group_ad.ad.final_urls, ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id={YT} AND ad_group_ad.status!='REMOVED'"):
    print("  ad", r['ad_group_ad']['ad'].get('name'), r['ad_group_ad']['status'], r['ad_group_ad']['ad'].get('final_urls'))
print("  -- other non-LSA campaigns in Belleville acct with spend since 2025-11")
for r in q(B,"SELECT campaign.name, campaign.status, campaign.advertising_channel_type, segments.month, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2025-11-01' AND '2026-11-16' AND metrics.cost_micros>0 AND campaign.advertising_channel_type!='LOCAL_SERVICES' AND campaign.advertising_channel_type!='VIDEO' ORDER BY segments.month"):
    m=r['metrics']; print(f"    {r['segments']['month']} {r['campaign']['name'][:36]:36s} {r['campaign']['status']} {r['campaign']['advertising_channel_type']} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.0f}")
