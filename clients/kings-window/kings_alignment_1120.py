# READ-ONLY. ./tsd.sh <abs path>. King's post-review alignment recheck (AT 9f657ee7, 2026-11-20). Review 2b381316 (call 11-10) rec $5,100/mo (+$500 NB);
# post-review direction = Growth Engine (AT 1496977c, 11-18), build waits on Angela's answers. Checks: budgets vs 11-12, NB raise applied?, enabled
# campaigns / ad groups / copy / offers, geo, conversion actions, LSA (pay-per-lead PMax 24431038949), any video/brand campaign built, change_event since 11-12.
import sys; sys.path.insert(0, ".")
from lib import run_query
C = "6769493219"; M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0)
def q(label, gaql):
    try: return run_query(C, gaql)
    except BaseException as e: print("  ERR", label, str(e)[:200]); return []
spend={}
for w,(a,b) in {"mtd":("2026-11-01","2026-11-19"),"7d":("2026-11-13","2026-11-19")}.items():
    for r in q("spend","SELECT campaign.id, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '%s' AND '%s'"%(a,b)):
        spend.setdefault(r["campaign"]["id"],{})[w]=(round(M(r["metrics"].get("cost_micros")),2),r["metrics"].get("clicks",0),round(F(r["metrics"].get("conversions")),1))
print("== campaigns (enabled or with Nov spend)")
for r in q("camps","SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.status != 'REMOVED'"):
    c=r["campaign"]; s=spend.get(c["id"],{})
    if c["status"]!="ENABLED" and not s.get("mtd",(0,))[0]: continue
    print(f"  {c['id']} {c['name'][:50]:<50} {c['status'][:7]} {c['advertising_channel_type'][:12]} {c.get('bidding_strategy_type','')[:20]} bud ${M(r['campaign_budget']['amount_micros']):.2f}/d geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')} | mtd {s.get('mtd')} | 7d {s.get('7d')}")
print("== change_event since 11-12 (user changes)")
for r in q("ce","SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields, campaign.name FROM change_event WHERE change_event.change_date_time >= '2026-11-12 00:00:00' AND change_event.change_date_time <= '2026-11-20 23:59:59' ORDER BY change_event.change_date_time DESC LIMIT 100"):
    e=r["change_event"]; print("  ",e["change_date_time"][:16],e.get("user_email"),e["change_resource_type"],e["resource_change_operation"],str(e.get("changed_fields"))[:80],r.get("campaign",{}).get("name","")[:30])
print("== enabled ad groups + RSAs")
for r in q("ads","SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad_strength FROM ad_group_ad WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'"):
    a=r["ad_group_ad"]; rsa=a["ad"].get("responsive_search_ad",{})
    print(f"  {r['campaign']['name'][:30]} / {r['ad_group']['name'][:28]} ad {a['ad']['id']} {a['policy_summary'].get('approval_status')} {a.get('ad_strength')} {a['ad'].get('final_urls')}")
    print("     H:", " | ".join(h.get("text","") for h in rsa.get("headlines",[])))
    print("     D:", " | ".join(h.get("text","") for h in rsa.get("descriptions",[])))
print("== ad group spend 11-13..11-19 (search)")
for r in q("ag","SELECT campaign.name, ad_group.name, ad_group.status, metrics.cost_micros, metrics.clicks, metrics.conversions FROM ad_group WHERE segments.date BETWEEN '2026-11-13' AND '2026-11-19' AND campaign.advertising_channel_type = 'SEARCH' AND metrics.impressions > 0"):
    m=r["metrics"]; print(f"  {r['campaign']['name'][:30]} / {r['ad_group']['name'][:28]} {r['ad_group']['status']} ${M(m.get('cost_micros')):.2f} clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f}")
print("== geo (enabled campaigns) with names")
crit=[]
for r in q("geo","SELECT campaign.name, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units, campaign_criterion.proximity.address.city_name FROM campaign_criterion WHERE campaign.status = 'ENABLED' AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"):
    cc=r["campaign_criterion"]; crit.append((r["campaign"]["name"][:30],cc))
ids=sorted({cc["location"]["geo_target_constant"] for _,cc in crit if cc.get("location")})
names={}
if ids:
    for r in q("gtc","SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.resource_name IN (%s)"%",".join("'%s'"%i for i in ids)):
        names[r["geo_target_constant"]["resource_name"]]=r["geo_target_constant"]["name"]
by={}
for n,cc in crit:
    v=("-" if cc.get("negative") else "")+(names.get(cc.get("location",{}).get("geo_target_constant"),"?") if cc.get("location") else f"radius {cc.get('proximity')}")
    by.setdefault(n,[]).append(v)
for n,v in by.items(): print("  ",n,len(v),":",", ".join(v)[:700])
print("== ad schedule (enabled)")
for r in q("sched","SELECT campaign.name, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour, campaign_criterion.ad_schedule.end_hour FROM campaign_criterion WHERE campaign.status = 'ENABLED' AND campaign_criterion.type = 'AD_SCHEDULE'"):
    a=r["campaign_criterion"]["ad_schedule"]; print("  ",r["campaign"]["name"][:30],a.get("day_of_week"),a.get("start_hour"),a.get("end_hour"))
print("== promotion / callout / sitelink assets (account + campaign)")
for lvl,res in (("customer","customer_asset"),("campaign","campaign_asset")):
    extra = ", campaign.name, campaign.status" if lvl=="campaign" else ""
    where = " AND campaign.status = 'ENABLED'" if lvl=="campaign" else ""
    for r in q(lvl,f"SELECT {res}.field_type, asset.sitelink_asset.link_text, asset.callout_asset.callout_text, asset.promotion_asset.promotion_target, asset.call_asset.phone_number, asset.final_urls{extra} FROM {res} WHERE {res}.status = 'ENABLED'{where}"):
        a=r["asset"]; ft=r[res]["field_type"]
        txt=(a.get("sitelink_asset",{}).get("link_text") or a.get("callout_asset",{}).get("callout_text") or a.get("promotion_asset",{}).get("promotion_target") or a.get("call_asset",{}).get("phone_number") or "")
        if ft in ("SITELINK","CALLOUT","PROMOTION","CALL"): print(f"  {lvl:<8} {r.get('campaign',{}).get('name','')[:26]:<26} {ft:<10} {txt} {a.get('final_urls','')}")
print("== conversion actions (enabled) + 14d 11-06..11-19")
conv={}
for r in q("convseg","SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-11-06' AND '2026-11-19'"):
    conv[r["segments"]["conversion_action_name"]]=(round(F(r["metrics"].get("all_conversions")),1),round(F(r["metrics"].get("conversions")),1))
for r in q("ca","SELECT conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.status = 'ENABLED'"):
    a=r["conversion_action"]; print(f"  {a['name'][:46]:<46} {str(a.get('type_') or a.get('type'))[:24]:<24} {str(a.get('category'))[:18]:<18} {'PRIMARY' if a.get('primary_for_goal') else 'secondary'} | 14d all/conv {conv.get(a['name'],(0,0))}")
print("== LSA (pay-per-lead) leads 11-10..11-19")
for r in q("lsa","SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.service_id, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-10 00:00:00'"):
    l=r["local_services_lead"]; print("  ",l["creation_date_time"][:16],l["lead_type"][:7],l.get("service_id"),l["lead_status"],"charged" if l.get("lead_charged") else "-")
