# READ-ONLY. ./tsd.sh <abs path>. Spencer post-review alignment (AT 5a7202d9): review 7a4093a1 (call 11-16) presented ~$2,700/mo thru Dec,
# Google = LSA + Branded only (no Nonbranded, Q1 plan), Meta = brand video awareness. TMS = installs, residential/commercial repair + replacement.
# Offer on file: free 1-yr maintenance agreement with a new full system replacement.
import sys; sys.path.insert(0, ".")
from lib import run_query
C = "2524618054"; M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0)
def q(label, gaql):
    try: return run_query(C, gaql)
    except BaseException as e: print("  ERR", label, str(e)[:200]); return []
print("== campaigns: status, budget, bidding, geo type + spend Nov 1-19 / Nov 16-19")
spend={}
for w,(a,b) in {"mtd":("2026-11-01","2026-11-19"),"post":("2026-11-16","2026-11-19")}.items():
    for r in q("spend","SELECT campaign.id, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '%s' AND '%s'"%(a,b)):
        spend.setdefault(r["campaign"]["id"],{})[w]=(M(r["metrics"].get("cost_micros")),r["metrics"].get("clicks",0),F(r["metrics"].get("conversions")))
for r in q("camps","SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type, campaign.target_impression_share.cpc_bid_ceiling_micros FROM campaign WHERE campaign.status != 'REMOVED'"):
    c=r["campaign"]; s=spend.get(c["id"],{})
    if c["status"]!="ENABLED" and not s: continue
    print(f"  {c['id']} {c['name'][:52]:<52} {c['status'][:7]} {c['advertising_channel_type'][:12]} {c.get('bidding_strategy_type','')[:22]} bud ${M(r['campaign_budget']['amount_micros']):.2f}/d ceil ${M(c.get('target_impression_share',{}).get('cpc_bid_ceiling_micros')):.2f} geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')} | mtd {s.get('mtd')} | 11-16..19 {s.get('post')}")
print("== daily spend 11-01..11-19 by channel type")
d={}
for r in q("daily","SELECT segments.date, campaign.name, metrics.cost_micros FROM campaign WHERE segments.date BETWEEN '2026-11-01' AND '2026-11-19' AND metrics.cost_micros > 0"):
    d.setdefault(r["segments"]["date"],[]).append(f"{r['campaign']['name'][:14]} ${M(r['metrics']['cost_micros']):.2f}")
for k in sorted(d): print("  ",k,"; ".join(d[k]))
print("== location criteria (enabled campaigns)")
for r in q("geo","SELECT campaign.name, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius, campaign_criterion.proximity.address.city_name FROM campaign_criterion WHERE campaign.status = 'ENABLED' AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"):
    cc=r["campaign_criterion"]; print("  ",r["campaign"]["name"][:30],cc.get("type"),"NEG" if cc.get("negative") else "",cc.get("location",{}).get("geo_target_constant") or cc.get("proximity"))
print("== Branded geo names")
ids=[]
for r in q("geoB","SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = 23822436393 AND campaign_criterion.type = 'LOCATION'"):
    ids.append(r["campaign_criterion"]["location"]["geo_target_constant"])
if ids:
    for r in q("gtc","SELECT geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.resource_name IN (%s)"%",".join("'%s'"%i for i in ids)):
        print("  ",r["geo_target_constant"]["name"],r["geo_target_constant"].get("target_type"))
print("== ad schedule (enabled campaigns)")
for r in q("sched","SELECT campaign.name, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour, campaign_criterion.ad_schedule.end_hour FROM campaign_criterion WHERE campaign.status = 'ENABLED' AND campaign_criterion.type = 'AD_SCHEDULE'"):
    a=r["campaign_criterion"]["ad_schedule"]; print("  ",r["campaign"]["name"][:30],a.get("day_of_week"),a.get("start_hour"),a.get("end_hour"))
print("== enabled ad groups + RSAs (text + final URLs)")
for r in q("ads","SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad_strength FROM ad_group_ad WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'"):
    a=r["ad_group_ad"]; rsa=a["ad"].get("responsive_search_ad",{})
    print(f"  {r['campaign']['name'][:30]} / {r['ad_group']['name'][:30]} ad {a['ad']['id']} {a['policy_summary'].get('approval_status')} {a.get('ad_strength')} {a['ad'].get('final_urls')}")
    print("     H:", " | ".join(h.get("text","") for h in rsa.get("headlines",[])))
    print("     D:", " | ".join(h.get("text","") for h in rsa.get("descriptions",[])))
print("== enabled keywords")
for r in q("kw","SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM keyword_view WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE"):
    print("  ",r["campaign"]["name"][:30],r["ad_group_criterion"]["keyword"]["text"],r["ad_group_criterion"]["keyword"]["match_type"])
print("== text assets linked (sitelinks / callouts / snippets / promotions), account + campaign level")
for lvl,res in (("customer","customer_asset"),("campaign","campaign_asset")):
    extra = ", campaign.name, campaign.status" if lvl=="campaign" else ""
    where = " AND campaign.status = 'ENABLED'" if lvl=="campaign" else ""
    for r in q(lvl,f"SELECT {res}.field_type, {res}.status, asset.sitelink_asset.link_text, asset.sitelink_asset.description1, asset.callout_asset.callout_text, asset.structured_snippet_asset.values, asset.promotion_asset.promotion_target, asset.final_urls{extra} FROM {res} WHERE {res}.status = 'ENABLED'{where}"):
        a=r["asset"]; ft=r[res]["field_type"]
        txt=(a.get("sitelink_asset",{}).get("link_text") or a.get("callout_asset",{}).get("callout_text") or a.get("structured_snippet_asset",{}).get("values") or a.get("promotion_asset",{}).get("promotion_target") or "")
        if ft in ("SITELINK","CALLOUT","STRUCTURED_SNIPPET","PROMOTION"): print(f"  {lvl:<8} {r.get('campaign',{}).get('name','')[:22]:<22} {ft:<18} {txt} {a.get('sitelink_asset',{}).get('description1','')} {a.get('final_urls','')}")
print("== conversion actions (enabled) primary/secondary + all_conv/conv 11-06..11-19")
conv={}
for r in q("convseg","SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-11-06' AND '2026-11-19'"):
    conv[r["segments"]["conversion_action_name"]]=(round(F(r["metrics"].get("all_conversions")),1),round(F(r["metrics"].get("conversions")),1))
for r in q("ca","SELECT conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.primary_for_goal, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.status = 'ENABLED'"):
    a=r["conversion_action"]; print(f"  {a['name'][:46]:<46} {str(a.get('type_') or a.get('type'))[:24]:<24} {str(a.get('category'))[:20]:<20} {'PRIMARY' if a.get('primary_for_goal') else 'secondary'} | 14d all/conv {conv.get(a['name'],(0,0))}")
print("== campaign conversion goals (biddable) on enabled campaigns")
for r in q("ccg","SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.status = 'ENABLED'"):
    g=r["campaign_conversion_goal"]
    if g.get("biddable"): print("  ",r["campaign"]["name"][:30],g.get("category"),g.get("origin"))
print("== LSA (pay-per-lead) leads 11-01..11-19")
for r in q("lsa","SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.service_id, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-01 00:00:00'"):
    l=r["local_services_lead"]; print("  ",l["creation_date_time"][:16],l["lead_type"][:7],l.get("service_id"),l["lead_status"],"charged" if l.get("lead_charged") else "-")
