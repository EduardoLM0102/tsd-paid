# READ-ONLY 7-day pass on Nick's Heating & Air, Google Ads 1854100356
import os
import sys, json, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID = "1854100356"
def q(label, gaql):
    try:
        return run_query(CID, gaql)
    except SystemExit:
        print(f"   !! query failed: {label}"); return []
    except Exception as e:
        print(f"   !! {label}: {str(e)[:200]}"); return []
M = lambda x: int(x or 0)/1e6
def H(t): print("\n" + "="*100 + f"\n{t}\n" + "="*100)

H("ACCOUNT")
for r in q("acct", "SELECT customer.descriptive_name, customer.currency_code, customer.time_zone, customer.auto_tagging_enabled, customer.status FROM customer"):
    print(r["customer"])

H("CAMPAIGNS (non-removed): settings")
camps = q("camps", """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
  campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
  campaign.target_cpa.target_cpa_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
  campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign.geo_target_type_setting.positive_geo_target_type, campaign_budget.amount_micros, campaign_budget.period
  FROM campaign WHERE campaign.status != 'REMOVED'""")
for r in camps:
    c = r["campaign"]; b = r.get("campaign_budget", {})
    ns = c.get("network_settings", {})
    mc = (c.get("maximize_conversions") or {}).get("target_cpa_micros")
    print(f"- {c['name']} [{c['id']}] {c['status']} / {c.get('primary_status')} {c.get('primary_status_reasons','')}")
    print(f"    {c['advertising_channel_type']} bid={c.get('bidding_strategy_type')} tCPA={M(mc) if mc else '-'} budget=${M(b.get('amount_micros')):.2f}/{b.get('period')} "
          f"search={ns.get('target_search_network')} partners={ns.get('target_partner_search_network')} display={ns.get('target_content_network')} geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')}")

H("CAMPAIGN METRICS: 7d (10-01..10-07) vs 30d")
for rng in ("LAST_7_DAYS", "LAST_30_DAYS"):
    print(f"-- {rng}")
    tot = collections.Counter()
    for r in q(rng, f"""SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.impressions,
      metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share FROM campaign WHERE segments.date DURING {rng} AND metrics.impressions > 0"""):
        c = r["campaign"]; m = r["metrics"]
        cost = M(m.get("cost_micros")); cl = int(m.get("clicks") or 0); cv = float(m.get("conversions") or 0)
        tot["cost"] += cost; tot["clicks"] += cl; tot["conv"] += cv
        print(f"   {c['name'][:45]:<45} {c['advertising_channel_type'][:10]:<10} ${cost:>8,.0f} clk {cl:>4} conv {cv:>5.1f} all {float(m.get('all_conversions') or 0):>5.1f} "
              f"CPL {('$%.0f' % (cost/cv)) if cv else '-':>6} CPC ${cost/cl if cl else 0:.2f} IS {m.get('search_impression_share','-')} rankLost {m.get('search_rank_lost_impression_share','-')} budLost {m.get('search_budget_lost_impression_share','-')}")
    print(f"   TOTAL ${tot['cost']:,.0f} clicks {tot['clicks']} conv {tot['conv']:.1f}")

H("MONTHLY TREND (Apr..Oct)")
mo = collections.defaultdict(lambda: collections.Counter())
for r in q("monthly", """SELECT segments.month, campaign.advertising_channel_type, metrics.cost_micros, metrics.conversions, metrics.clicks
  FROM campaign WHERE segments.date BETWEEN '2026-04-01' AND '2026-10-07'"""):
    k = r["segments"]["month"]; ch = r["campaign"]["advertising_channel_type"]
    mo[k][ch+"_cost"] += M(r["metrics"].get("cost_micros")); mo[k][ch+"_conv"] += float(r["metrics"].get("conversions") or 0)
for k in sorted(mo):
    print(" ", k, {kk: round(v,1) for kk, v in sorted(mo[k].items()) if v})

H("CONVERSIONS BY ACTION (30d and 7d)")
for rng in ("LAST_30_DAYS", "LAST_7_DAYS"):
    print(f"-- {rng}")
    for r in q("conv "+rng, f"""SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.conversions, metrics.all_conversions
      FROM customer WHERE segments.date DURING {rng} AND metrics.all_conversions > 0"""):
        s = r["segments"]; m = r["metrics"]
        print(f"   {s['conversion_action_name'][:55]:<55} {s.get('conversion_action_category'):<22} conv {float(m.get('conversions') or 0):>6.1f} all {float(m.get('all_conversions') or 0):>6.1f}")
print("-- by campaign x action, 30d (counted conv only)")
for r in q("conv camp", """SELECT campaign.name, segments.conversion_action_name, metrics.conversions FROM campaign
   WHERE segments.date DURING LAST_30_DAYS AND metrics.conversions > 0"""):
    print(f"   {r['campaign']['name'][:40]:<40} {r['segments']['conversion_action_name'][:50]:<50} {float(r['metrics']['conversions']):.1f}")

H("CONVERSION ACTIONS (enabled)")
for r in q("ca", """SELECT conversion_action.name, conversion_action.status, conversion_action.category, conversion_action.type,
  conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.counting_type, conversion_action.origin
  FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    a = r["conversion_action"]
    print(f"   {a['name'][:50]:<50} {a.get('category'):<20} {a.get('type'):<28} primary={a.get('primary_for_goal')} inConv={a.get('include_in_conversions_metric')} {a.get('counting_type')} {a.get('origin')}")

H("CAMPAIGN CONVERSION GOALS (biddable)")
for r in q("ccg", "SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.status != 'REMOVED'"):
    g = r["campaign_conversion_goal"]
    if g.get("biddable"): print(f"   {r['campaign']['name'][:40]:<40} {g.get('category')}/{g.get('origin')}")

H("NETWORK SPLIT 30d")
for r in q("net", """SELECT campaign.name, segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign
   WHERE segments.date DURING LAST_30_DAYS AND metrics.impressions > 0"""):
    m = r["metrics"]
    print(f"   {r['campaign']['name'][:40]:<40} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):>7,.0f} clk {m.get('clicks')} conv {float(m.get('conversions') or 0):.1f}")

H("LOCATION TARGETING (campaign criteria)")
locs = q("loc", """SELECT campaign.name, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant,
  campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units, campaign_criterion.proximity.address.city_name
  FROM campaign_criterion WHERE campaign.status != 'REMOVED' AND campaign_criterion.type IN ('LOCATION','PROXIMITY')""")
gtc = set(r["campaign_criterion"].get("location",{}).get("geo_target_constant") for r in locs if r["campaign_criterion"].get("location"))
names = {}
if gtc:
    ids = ",".join("'"+g+"'" for g in gtc if g)
    for r in q("gtc", f"SELECT geo_target_constant.resource_name, geo_target_constant.canonical_name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.resource_name IN ({ids})"):
        names[r["geo_target_constant"]["resource_name"]] = r["geo_target_constant"]["canonical_name"]
bycamp = collections.defaultdict(list)
for r in locs:
    cc = r["campaign_criterion"]
    if cc.get("location"):
        bycamp[r["campaign"]["name"]].append(("NEG " if cc.get("negative") else "") + names.get(cc["location"]["geo_target_constant"], cc["location"]["geo_target_constant"]))
    else:
        p = cc.get("proximity", {}); bycamp[r["campaign"]["name"]].append(f"radius {p.get('radius')} {p.get('radius_units')} {p.get('address',{}).get('city_name')}")
for k, v in bycamp.items(): print(f"   {k[:40]}: {v}")
camp_names = [r["campaign"]["name"] for r in camps if r["campaign"]["status"] == "ENABLED"]
for n in camp_names:
    if n not in bycamp: print(f"   !! NO location criteria: {n}")

H("WHERE CLICKS CAME FROM 30d (user location, by country/region)")
geo = collections.Counter(); geoc = collections.Counter()
for r in q("geo", """SELECT segments.geo_target_region, user_location_view.country_criterion_id, metrics.clicks, metrics.cost_micros, metrics.conversions
   FROM user_location_view WHERE segments.date DURING LAST_30_DAYS AND metrics.clicks > 0"""):
    k = (r["user_location_view"].get("country_criterion_id"), r["segments"].get("geo_target_region"))
    geo[k] += M(r["metrics"].get("cost_micros")); geoc[k] += int(r["metrics"].get("clicks") or 0)
for k, v in geo.most_common(12): print(f"   country {k[0]} region {k[1]}  ${v:,.0f}  clicks {geoc[k]}")

H("SEARCH TERMS 30d, top 40 by cost")
st = q("st", """SELECT campaign.name, search_term_view.search_term, search_term_view.status, metrics.cost_micros, metrics.clicks, metrics.conversions
   FROM search_term_view WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0 ORDER BY metrics.cost_micros DESC LIMIT 40""")
for r in st:
    m = r["metrics"]
    print(f"   ${M(m.get('cost_micros')):>6.0f} clk {m.get('clicks'):>3} conv {float(m.get('conversions') or 0):>4.1f}  {r['search_term_view']['search_term'][:55]:<55} [{r['campaign']['name'][:25]}] {r['search_term_view'].get('status')}")
tot_st = q("st_tot", "SELECT metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0")
print(f"   (all search terms 30d: ${sum(M(r['metrics'].get('cost_micros')) for r in tot_st):,.0f}, {len(tot_st)} term rows)")

H("PMAX SEARCH CATEGORIES 30d (campaign_search_term_insight)")
for c in [r for r in camps if r["campaign"]["advertising_channel_type"] == "PERFORMANCE_MAX" and r["campaign"]["status"] == "ENABLED"]:
    cid = c["campaign"]["id"]
    rows = q("pmax insight", f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.conversions FROM campaign_search_term_insight
       WHERE segments.date DURING LAST_30_DAYS AND campaign_search_term_insight.campaign_id = '{cid}' ORDER BY metrics.clicks DESC LIMIT 15""")
    for r in rows: print(f"   {r['campaign_search_term_insight'].get('category_label')!s:<45} clk {r['metrics'].get('clicks')} conv {float(r['metrics'].get('conversions') or 0):.1f}")

H("KEYWORDS (enabled campaigns), 30d")
for r in q("kw", """SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
   ad_group_criterion.quality_info.quality_score, metrics.cost_micros, metrics.clicks, metrics.conversions FROM keyword_view
   WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED' AND ad_group_criterion.negative = FALSE ORDER BY metrics.cost_micros DESC LIMIT 40"""):
    k = r["ad_group_criterion"]; m = r["metrics"]
    print(f"   ${M(m.get('cost_micros')):>6.0f} clk {m.get('clicks'):>3} conv {float(m.get('conversions') or 0):>4.1f} QS {k.get('quality_info',{}).get('quality_score','-')!s:>2} {k['status']:<7} {k['keyword']['match_type']:<6} {k['keyword']['text'][:40]:<40} [{r['campaign']['name'][:22]}/{r['ad_group']['name'][:18]}]")

H("NEGATIVES per campaign + shared sets")
neg = collections.Counter()
for r in q("neg", "SELECT campaign.name FROM campaign_criterion WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD' AND campaign.status != 'REMOVED'"):
    neg[r["campaign"]["name"]] += 1
print("   campaign-level negative keywords:", dict(neg))
for r in q("ss", "SELECT campaign.name, shared_set.name, shared_set.type, shared_set.member_count FROM campaign_shared_set WHERE campaign.status != 'REMOVED'"):
    print("   shared set:", r["campaign"]["name"], r["shared_set"])

H("ADS: approval + strength (enabled)")
for r in q("ads", """SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status,
   ad_group_ad.policy_summary.review_status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.status = 'ENABLED' AND ad_group_ad.status != 'REMOVED'"""):
    a = r["ad_group_ad"]
    print(f"   {r['campaign']['name'][:30]:<30} {r['ad_group']['name'][:20]:<20} {a['status']:<7} {a.get('ad_strength')!s:<9} {a.get('policy_summary',{}).get('approval_status')} {a['ad'].get('final_urls')}")
print("-- asset groups (PMax)")
for r in q("ag", "SELECT campaign.name, asset_group.name, asset_group.status, asset_group.primary_status, asset_group.ad_strength, asset_group.final_urls FROM asset_group WHERE campaign.status = 'ENABLED'"):
    print("  ", r["campaign"]["name"], r["asset_group"])

H("AUTO-APPLY RECOMMENDATION SUBSCRIPTIONS")
for r in q("recsub", "SELECT recommendation_subscription.type, recommendation_subscription.status FROM recommendation_subscription"):
    print("  ", r["recommendation_subscription"])

H("AD SCHEDULE criteria")
for r in q("sched", "SELECT campaign.name, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour, campaign_criterion.ad_schedule.end_hour FROM campaign_criterion WHERE campaign_criterion.type = 'AD_SCHEDULE' AND campaign.status = 'ENABLED'"):
    print("  ", r["campaign"]["name"], r["campaign_criterion"]["ad_schedule"])

H("DAILY SPEND last 14 days (all campaigns)")
d = collections.defaultdict(lambda: collections.Counter())
for r in q("daily", "SELECT segments.date, campaign.advertising_channel_type, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING LAST_14_DAYS"):
    d[r["segments"]["date"]][r["campaign"]["advertising_channel_type"]] += M(r["metrics"].get("cost_micros"))
for k in sorted(d): print("  ", k, {kk: round(v) for kk, v in d[k].items() if v})

H("LSA LEADS 30d")
leads = q("lsa leads", """SELECT local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged,
  local_services_lead.category_id, local_services_lead.service_id, local_services_lead.creation_date_time,
  local_services_lead.credit_details.credit_state FROM local_services_lead
  WHERE local_services_lead.creation_date_time >= '2026-09-08 00:00:00'""")
c = collections.Counter((r["local_services_lead"].get("lead_type"), r["local_services_lead"].get("lead_status"), r["local_services_lead"].get("lead_charged")) for r in leads)
for k, v in c.most_common(): print("  ", v, k)
svc = collections.Counter(r["local_services_lead"].get("service_id") for r in leads); print("   services:", dict(svc))
wk = collections.Counter(r["local_services_lead"]["creation_date_time"][:10] >= "2026-10-01" for r in leads); print("   last 7d leads:", wk.get(True, 0), " prior:", wk.get(False, 0))

H("LSA VERIFICATION ARTIFACTS (insurance/license/background)")
for r in q("lsa verif", """SELECT local_services_verification_artifact.artifact_type, local_services_verification_artifact.status,
  local_services_verification_artifact.creation_date_time, local_services_verification_artifact.insurance_verification_artifact.amount_micros,
  local_services_verification_artifact.insurance_verification_artifact.rejection_reason,
  local_services_verification_artifact.license_verification_artifact.license_type,
  local_services_verification_artifact.license_verification_artifact.license_number,
  local_services_verification_artifact.license_verification_artifact.rejection_reason,
  local_services_verification_artifact.background_check_verification_artifact.final_adjudication_date_time
  FROM local_services_verification_artifact"""):
    print("  ", json.dumps(r["local_services_verification_artifact"], default=str))
