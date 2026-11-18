# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""Nick's (1854100356), 2026-11-18 read (Command Center fu-152): week 1 of the Heating Repair ad group + Branded cleanup (applied 11-11 07:21 CT).
POST = 11-11..11-17 (7d) vs PRE = 11-04..11-10 (7d), conversions by CONVERSION date (ad calls count on the click date otherwise).
Split Google's Pay-per-lead PMax 24425921001 (ex-LSA) from TSD PMax 23586346547. Also pulls what the heating LP brief needs."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "1854100356"
PM, BR, NB, LSA_OLD, PPL = "23586346547", "23675600637", "23821497590", "23344968885", "24425921001"
NAMES = {PM: "TSD PMax", BR: "Branded", NB: "NB AC", LSA_OLD: "LSA old", PPL: "PPL PMax (LSA)"}
POST = ("segments.date BETWEEN '2026-11-11' AND '2026-11-17'", 7)
PRE = ("segments.date BETWEEN '2026-11-04' AND '2026-11-10'", 7)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
pct = lambda x: f"{F(x)*100:.0f}%"
q = lambda s: run_query(CID, s)

for label, (win, days) in (("POST 11-11..11-17", POST), ("PRE 11-04..11-10", PRE)):
    print(f"\n===== A. campaigns {label}")
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros,
        metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions_by_conversion_date, metrics.all_conversions,
        metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE {win} AND metrics.impressions > 0"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
        print(f"  {NAMES.get(c['id'], c['name'][:18]):16s} {c['status'][:7]} {c.get('advertising_channel_type','')[:12]:12s} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | ${sp:7.2f} ({sp/days:.0f}/d) impr {m.get('impressions',0):>5} clk {cl:>4}"
              f" CPC ${sp/cl if cl else 0:.2f} conv(cd) {F(m.get('conversions_by_conversion_date')):.1f} all {F(m.get('all_conversions')):.1f} | IS {pct(m.get('search_impression_share'))} budL {pct(m.get('search_budget_lost_impression_share'))} rankL {pct(m.get('search_rank_lost_impression_share'))}")
    print(f"  -- conversions by action ({label}, by conversion date)")
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions_by_conversion_date, metrics.all_conversions_by_conversion_date
        FROM campaign WHERE {win} AND metrics.all_conversions_by_conversion_date > 0"""):
        print(f"     {NAMES.get(r['campaign']['id'], r['campaign']['id']):16s} {r['segments']['conversion_action_name'][:40]:40s} conv {F(r['metrics'].get('conversions_by_conversion_date')):.1f} all {F(r['metrics'].get('all_conversions_by_conversion_date')):.1f}")

print("\n===== B. TSD PMax network split")
for label, (win, d) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE {win} AND campaign.id = {PM}"):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):7.2f} clk {m.get('clicks',0):>4} conv {F(m.get('conversions')):.1f}")

print("\n===== C. TSD PMax search categories POST")
for r in q(f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.impressions, metrics.conversions
        FROM campaign_search_term_insight WHERE campaign_search_term_insight.campaign_id = {PM} AND {POST[0]} ORDER BY metrics.clicks DESC LIMIT 20"""):
    i = r["campaign_search_term_insight"]; m = r["metrics"]
    print(f"  {i['category_label'][:50]:50s} impr {m.get('impressions',0):>4} clk {m.get('clicks',0):>3} conv {F(m.get('conversions')):.1f}")

print("\n===== D. calls from ads 11-11..11-17 (call_view)")
for r in q("""SELECT campaign.id, ad_group.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
        FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-11-11 00:00:00' AND '2026-11-17 23:59:59' ORDER BY call_view.start_call_date_time"""):
    c = r["call_view"]; print(f"  {NAMES.get(r['campaign']['id'], r['campaign']['id']):16s} {(r.get('ad_group') or {}).get('name','')[:16]:16s} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== E. LSA / PPL PMax: daily delivery 11-04..11-17 + leads since 11-04")
for r in q(f"SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE campaign.id = {PPL} AND segments.date BETWEEN '2026-11-04' AND '2026-11-17' ORDER BY segments.date"):
    m = r["metrics"]; print(f"  PPL {r['segments']['date']} impr {m.get('impressions',0):>3} clk {m.get('clicks',0):>2} ${M(m.get('cost_micros')):.2f}")
leads = q("""SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged,
        local_services_lead.creation_date_time, local_services_lead.category_id FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-04 00:00:00'""")
for l in sorted(leads, key=lambda l: l["local_services_lead"]["creation_date_time"]):
    x = l["local_services_lead"]; print(f"  lead {x['id']} {x['creation_date_time'][:16]} {x['lead_type']:12s} {x['lead_status']:16s} charged={x.get('lead_charged', False)}")
by = collections.Counter((l["local_services_lead"]["creation_date_time"][:10] >= "2026-11-11", l["local_services_lead"].get("lead_charged", False)) for l in leads)
print("  leads POST(11-04..): charged", by[(True, True)], "not charged", by[(True, False)], "| 11-04..11-10: charged", by[(False, True)], "not charged", by[(False, False)])

HG = "205669629001"
print("\n===== F. NB ad groups POST")
for r in q(f"""SELECT ad_group.id, ad_group.name, ad_group.status, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions_by_conversion_date, metrics.all_conversions,
        metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_top_impression_share
        FROM ad_group WHERE campaign.id = {NB} AND {POST[0]}"""):
    g, m = r["ad_group"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
    print(f"  {g['name'][:24]:24s} {g['status'][:7]} ${sp:7.2f} impr {m.get('impressions',0):>4} clk {cl:>3} CPC ${sp/cl if cl else 0:.2f} conv(cd) {F(m.get('conversions_by_conversion_date')):.1f} all {F(m.get('all_conversions')):.1f} IS {pct(m.get('search_impression_share'))} rankL {pct(m.get('search_rank_lost_impression_share'))} top {pct(m.get('search_top_impression_share'))}")
print("  -- NB by day")
for r in q(f"SELECT segments.date, ad_group.name, metrics.cost_micros, metrics.clicks, metrics.impressions FROM ad_group WHERE campaign.id = {NB} AND {POST[0]} AND metrics.impressions > 0 ORDER BY segments.date"):
    m = r["metrics"]; print(f"   {r['segments']['date']} {r['ad_group']['name'][:20]:20s} ${M(m.get('cost_micros')):6.2f} clk {m.get('clicks',0):>2} impr {m.get('impressions',0):>3}")

print("\n===== G. heating RSA status + keywords POST")
for r in q(f"""SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status, ad_group_ad.ad_strength,
        ad_group_ad.policy_summary.policy_topic_entries FROM ad_group_ad WHERE ad_group.id = {HG}"""):
    a = r["ad_group_ad"]; print("  RSA", a["ad"]["id"], a["status"], a["policy_summary"].get("approval_status"), a["policy_summary"].get("review_status"), a.get("ad_strength"), a["policy_summary"].get("policy_topic_entries", ""))
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.system_serving_status,
        ad_group_criterion.quality_info.quality_score, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions_by_conversion_date
        FROM keyword_view WHERE ad_group.id = {HG} AND {POST[0]} ORDER BY metrics.impressions DESC"""):
    k, m = r["ad_group_criterion"], r["metrics"]
    print(f"  {k['keyword']['text'][:28]:28s} {k['keyword']['match_type'][:6]:6s} {k.get('system_serving_status','')[:12]:12s} QS {k.get('quality_info',{}).get('quality_score','-')} impr {m.get('impressions',0):>3} clk {m.get('clicks',0):>2} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions_by_conversion_date')):.1f}")
print("  -- heating keywords with 0 impressions (status)")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.system_serving_status, ad_group_criterion.quality_info.quality_score
        FROM ad_group_criterion WHERE ad_group.id = {HG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE"""):
    k = r["ad_group_criterion"]; print(f"   {k['keyword']['text'][:28]:28s} {k['keyword']['match_type'][:6]} {k.get('system_serving_status')} QS {k.get('quality_info',{}).get('quality_score','-')}")

print("\n===== H. search terms NB + Branded POST")
for r in q(f"""SELECT campaign.id, ad_group.name, search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM search_term_view WHERE campaign.id IN ({NB},{BR}) AND {POST[0]} ORDER BY metrics.cost_micros DESC LIMIT 80"""):
    m = r["metrics"]; print(f"  {NAMES[r['campaign']['id']]:8s} {r['ad_group']['name'][:16]:16s} {r['search_term_view']['search_term'][:42]:42s} impr {m.get('impressions',0):>3} clk {m.get('clicks',0):>2} ${M(m.get('cost_micros')):6.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== I. Branded keywords POST (enabled)")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.search_impression_share, metrics.search_rank_lost_impression_share FROM keyword_view WHERE campaign.id = {BR} AND ad_group_criterion.status = 'ENABLED' AND {POST[0]} ORDER BY metrics.impressions DESC"""):
    k, m = r["ad_group_criterion"], r["metrics"]
    print(f"  {k['keyword']['text'][:30]:30s} {k['keyword']['match_type'][:6]:6s} impr {m.get('impressions',0):>4} clk {m.get('clicks',0):>3} ${M(m.get('cost_micros')):6.2f} IS {pct(m.get('search_impression_share'))} rankL {pct(m.get('search_rank_lost_impression_share'))}")

print("\n===== J. changes since 11-11 07:30")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
        FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-11 07:30:00' AND '2026-11-18 23:59:59' ORDER BY change_event.change_date_time LIMIT 60"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:60], (e.get("campaign") or "")[-11:])
