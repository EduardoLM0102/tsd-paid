# READ-ONLY. ./tsd.sh <abs path>. All Seasons post-review alignment (AT b1e7e485): what was agreed 11-10 = LSA top service, LSA $350/wk, PPC unchanged ($46/d), $2,500 cap.
import sys; sys.path.insert(0, ".")
from lib import run_query
PPC, LSA = "4467722415", "8655979348"; M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0)
print("== PPC campaigns (enabled + spend 11-10..11-18)")
for r in run_query(PPC,"SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-11-10' AND '2026-11-18' AND campaign.status = 'ENABLED'"):
    c,m=r["campaign"],r["metrics"]; print(f"  {c['id']} {c['name'][:42]:<42} {c['advertising_channel_type'][:6]} {c.get('bidding_strategy_type','')[:14]} bud ${M(r['campaign_budget']['amount_micros']):.0f}/d geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')} | ${M(m.get('cost_micros')):.2f} clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f}")
print("== enabled campaigns with no spend this window")
for r in run_query(PPC,"SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign_budget.amount_micros FROM campaign WHERE campaign.status = 'ENABLED'"):
    print("  ", r["campaign"]["id"], r["campaign"]["name"][:45], r["campaign"]["advertising_channel_type"], M(r["campaign_budget"]["amount_micros"]))
print("== PPC location targets (enabled campaigns)")
for r in run_query(PPC,"SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius, campaign_criterion.proximity.address.city_name, campaign_criterion.negative, campaign_criterion.type FROM campaign_criterion WHERE campaign.status = 'ENABLED' AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"):
    cc=r["campaign_criterion"]; print("  ", r["campaign"]["name"][:30], cc.get("type"), "NEG" if cc.get("negative") else "", cc.get("location",{}).get("geo_target_constant") or cc.get("proximity"))
print("== PPC ad final URLs + headline sample (enabled RSAs)")
for r in run_query(PPC,"SELECT campaign.name, ad_group.name, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'"):
    a=r["ad_group_ad"]; hl=[h.get("text") for h in a["ad"].get("responsive_search_ad",{}).get("headlines",[])]
    print(f"  {r['campaign']['name'][:24]:<24} {r['ad_group']['name'][:22]:<22} {a['policy_summary'].get('approval_status')} {a['ad'].get('final_urls')} | {', '.join(hl[:15])[:300]}")
print("== PPC conversion actions (enabled) + 14d all_conv")
conv={}
for r in run_query(PPC,"SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-11-05' AND '2026-11-18'"):
    conv[r["segments"]["conversion_action_name"]]=(F(r["metrics"].get("all_conversions")),F(r["metrics"].get("conversions")))
for r in run_query(PPC,"SELECT conversion_action.name, conversion_action.type, conversion_action.primary_for_goal, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.status = 'ENABLED'"):
    a=r["conversion_action"]; print(f"  {a['name'][:40]:<40} {str(a.get('type_') or a.get('type'))[:22]:<22} {'PRIMARY' if a.get('primary_for_goal') else 'secondary'} min {a.get('phone_call_duration_seconds','-')}s | 14d all/conv {conv.get(a['name'],(0,0))}")
print("== LSA budget + weekly spend")
for r in run_query(LSA,"SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, campaign_budget.period FROM campaign WHERE campaign.status = 'ENABLED'"):
    print("  ", r["campaign"]["id"], r["campaign"]["name"][:40], r["campaign"]["status"], f"${M(r['campaign_budget']['amount_micros']):.2f}", r["campaign_budget"].get("period"))
for r in run_query(LSA,"SELECT segments.week, metrics.cost_micros, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2026-10-27' AND '2026-11-18' ORDER BY segments.week"):
    print("   week", r["segments"]["week"], f"${M(r['metrics'].get('cost_micros')):.2f}", "impr", r["metrics"].get("impressions"))
print("== LSA leads 11-10..11-18")
for r in run_query(LSA,"SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-10 00:00:00'"):
    l=r["local_services_lead"]; print("  ", l["creation_date_time"][:16], l["lead_type"][:5], l["lead_status"], "charged" if l.get("lead_charged") else "-")
print("== LSA hourly impressions 11-01..11-18 (schedule check)")
h={}
for r in run_query(LSA,"SELECT segments.day_of_week, segments.hour, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2026-11-01' AND '2026-11-18'"):
    k=(r["segments"]["day_of_week"][:3]); h.setdefault(k,set()).add(int(r["segments"]["hour"])) if int(r["metrics"].get("impressions",0)) else None
print("  ", {k:(min(v),max(v)) for k,v in h.items()})
