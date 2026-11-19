# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path>. ICS NB first read after relaunch 11-12 + plan C 11-16 (fu-159).
import sys; sys.path.insert(0, ".")
from lib import run_query
CID, NB = "4571881760", "24047025253"
M = lambda x: int(x or 0) / 1e6; F = lambda x: float(x or 0)
q = lambda s: run_query(CID, s)
print("== NB daily 11-12..11-19")
for r in q(f"""SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.search_impression_share,
  metrics.search_top_impression_share, metrics.search_absolute_top_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share
  FROM campaign WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-19' ORDER BY segments.date"""):
    m = r["metrics"]; s = M(m.get("cost_micros")); c = int(m.get("clicks", 0))
    print(f"  {r['segments']['date']} ${s:6.2f} clk {c:>2} impr {m.get('impressions',0):>4} CPC ${s/c if c else 0:5.2f} conv {F(m.get('conversions')):.1f} IS {F(m.get('search_impression_share'))*100:.0f} top {F(m.get('search_top_impression_share'))*100:.0f} abs {F(m.get('search_absolute_top_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f}")
print("== all campaigns spend 11-12..11-18")
for r in q("SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-11-12' AND '2026-11-18' AND metrics.impressions > 0"):
    print(f"  {r['campaign']['name'][:45]:<45} {r['campaign']['status']} {r['campaign'].get('bidding_strategy_type')} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} ${M(r['metrics'].get('cost_micros')):.2f} clk {r['metrics'].get('clicks',0)} conv {F(r['metrics'].get('conversions')):.1f}")
print("== NB conv by action since 11-12")
for r in q(f"SELECT segments.date, segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM campaign WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-19' AND metrics.all_conversions > 0"):
    print(f"  {r['segments']['date']} {r['segments']['conversion_action_name']:<35} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")
print("== call_view since 11-12 (all campaigns)")
for r in q("SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.type, call_view.caller_area_code, campaign.name FROM call_view WHERE call_view.start_call_date_time >= '2026-11-12 00:00:00'"):
    v = r.get("call_view") or r.get("callView")
    print("  ", {k: v.get(k) for k in v if k != 'resource_name'}, r["campaign"]["name"][:35])
print("== NB search terms 11-17..11-19")
for r in q(f"SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-17' AND '2026-11-19' ORDER BY metrics.impressions DESC LIMIT 40"):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term'][:50]:<50} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")
print("== NB keywords QS + LP experience")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, metrics.impressions
  FROM keyword_view WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-19' AND metrics.impressions > 0"""):
    k = r["ad_group_criterion"]; qi = k.get("quality_info", {})
    print(f"  {k['keyword']['text'][:30]:<30} {k['keyword']['match_type']:<7} QS {qi.get('quality_score','-')} LP {qi.get('post_click_quality_score','-')} ad {qi.get('creative_quality_score','-')} ctr {qi.get('search_predicted_ctr','-')} impr {r['metrics'].get('impressions')}")
print("== NB ads approval")
for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.status = 'ENABLED'"):
    a = r["ad_group_ad"]; print("  ", a["ad"]["id"], a["policy_summary"].get("approval_status"), a["policy_summary"].get("review_status"), a["ad"].get("final_urls"))
print("== NB geo 11-16..11-19 (user location city)")
for r in q(f"SELECT segments.geo_target_city, metrics.cost_micros, metrics.clicks FROM user_location_view WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-17' AND '2026-11-19' AND metrics.clicks > 0"):
    print("  ", r["segments"].get("geo_target_city"), f"${M(r['metrics'].get('cost_micros')):.2f}", r["metrics"].get("clicks"))
