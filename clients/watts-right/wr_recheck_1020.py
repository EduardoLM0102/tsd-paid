# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-10-20 recheck (Command Center fu-034): RSA A/B, Nonbranded CPC/CPL, Branded IS,
PMax real CPL, Panel ad group. Window = 10-09 -> 10-19 (11 days); RSA A/B uses the full 10-01 -> 10-19 run."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PM = "23690645223", "23832838033", "23833205176"
NAMES = {BR: "Branded", NB: "Nonbranded", PM: "PMax"}
WIN = "segments.date BETWEEN '2026-10-09' AND '2026-10-19'"
AB = "segments.date BETWEEN '2026-10-01' AND '2026-10-19'"
NEW_ADS = {"826560998576", "826560998579", "826560998582"}
REAL = {"Calls from ads", "Website calls", "Contact Form", "Form Submit", "Book Now", "Phone Call"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. campaigns 10-09..10-19")
for r in q(f"""SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
    campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.search_impression_share,
    metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
    FROM campaign WHERE {WIN} AND campaign.id IN ({BR},{NB},{PM})"""):
    c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); cv = F(m.get("conversions"))
    print(f"{NAMES[c['id']]:<11} {c['status']} {c.get('bidding_strategy_type')} tCPA={M(c.get('maximize_conversions',{}).get('target_cpa_micros'))} "
          f"budget ${M(r['campaign_budget'].get('amount_micros')):.0f}/d | ${sp:,.2f} ({sp/11:.0f}/d) clk {cl} conv {cv:.1f} "
          f"CPL ${sp/cv if cv else 0:,.2f} CPC ${sp/cl if cl else 0:.2f} | IS {F(m.get('search_impression_share'))*100:.1f} "
          f"budget-lost {F(m.get('search_budget_lost_impression_share'))*100:.1f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.1f}")

print("\n===== B. conversions by action 10-09..10-19 (primary conversions column)")
for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
    WHERE {WIN} AND campaign.id IN ({BR},{NB},{PM}) AND metrics.all_conversions > 0"""):
    print(f"  {NAMES[r['campaign']['id']]:<11} {r['segments']['conversion_action_name']:<40} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== C. RSA A/B 10-01..10-19 (Nonbranded)")
for r in q(f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, metrics.impressions, metrics.clicks,
    metrics.conversions, metrics.cost_micros FROM ad_group_ad WHERE {AB} AND campaign.id = {NB} AND metrics.impressions > 0"""):
    a, m = r["ad_group_ad"], r["metrics"]; im = int(m.get("impressions", 0)); cl = int(m.get("clicks", 0)); cv = F(m.get("conversions"))
    tag = "NEW" if a["ad"]["id"] in NEW_ADS else "old"
    print(f"  {r['ad_group']['name']:<28} {tag} {a['ad']['id']} {a['status']} {a.get('ad_strength')} impr {im} clk {cl} CTR {cl/im*100 if im else 0:.2f}% "
          f"conv {cv:.1f} CVR {cv/cl*100 if cl else 0:.1f}% ${M(m.get('cost_micros')):.2f}")

print("\n===== D. ad group 10-09..10-19 (Nonbranded) + 10-01..10-08 for impressions/day")
for win, days in ((WIN, 11), ("segments.date BETWEEN '2026-10-01' AND '2026-10-08'", 8)):
    for r in q(f"""SELECT ad_group.name, metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros FROM ad_group
        WHERE {win} AND campaign.id = {NB}"""):
        m = r["metrics"]; print(f"  [{days}d] {r['ad_group']['name']:<28} impr/d {int(m.get('impressions',0))/days:.1f} clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f} ${M(m.get('cost_micros')):.2f}")

print("\n===== E. keyword QS (Nonbranded, enabled)")
for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score,
    ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.creative_quality_score,
    metrics.clicks, metrics.cost_micros FROM keyword_view WHERE {WIN} AND campaign.id = {NB} AND ad_group_criterion.status = 'ENABLED' AND metrics.impressions > 0"""):
    k = r["ad_group_criterion"]; qi = k.get("quality_info", {})
    print(f"  {r['ad_group']['name']:<24} {k['keyword']['text']:<34} {k['keyword']['match_type']:<7} QS {qi.get('quality_score','-')} "
          f"ctr {qi.get('search_predicted_ctr','-')} lp {qi.get('post_click_quality_score','-')} ad {qi.get('creative_quality_score','-')} clk {r['metrics'].get('clicks',0)} ${M(r['metrics'].get('cost_micros')):.2f}")

print("\n===== F. changes since 10-09")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
    change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-09' AND '2026-10-21'
    ORDER BY change_event.change_date_time LIMIT 200"""):
    e = r["change_event"]; print(" ", e["change_date_time"], e.get("user_email"), e["change_resource_type"], e["resource_change_operation"], e.get("changed_fields"), e.get("campaign"))
