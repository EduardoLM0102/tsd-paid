# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Concrete Adventures (9215192296), 2026-11-04: first check (Command Center fu-083, due 10-27) on the Oxford Search campaigns live since 10-22:
Branded 24379794681 ($5/d, Max Clicks $4 cap) + Nonbranded 24379794684 ($10/d, $10 cap). Window 10-22 -> 11-03."""
import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "9215192296"
BR, NB = "24379794681", "24379794684"
N = {BR: "Branded", NB: "Nonbranded"}
WIN = "segments.date BETWEEN '2026-10-22' AND '2026-11-03'"
IDS = f"campaign.id IN ({BR},{NB})"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. campaigns 10-22..11-03")
for r in q(f"""SELECT campaign.id, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign_budget.amount_micros,
    campaign.target_spend.cpc_bid_ceiling_micros, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
    metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share FROM campaign WHERE {WIN} AND {IDS}"""):
    c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
    print(f"  {N[c['id']]:<10} {c['status']}/{c.get('primary_status')} {c.get('primary_status_reasons','')} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} cap ${M((c.get('target_spend') or {}).get('cpc_bid_ceiling_micros')):.0f} | "
          f"${sp:.2f} clk {cl} impr {m.get('impressions',0)} CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} | "
          f"IS {F(m.get('search_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f}")

print("\n===== B. daily")
for r in q(f"SELECT campaign.id, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions FROM campaign WHERE {WIN} AND {IDS} AND metrics.impressions > 0 ORDER BY segments.date"):
    m = r["metrics"]; print(f"  {r['segments']['date']} {N[r['campaign']['id']]:<10} ${M(m.get('cost_micros')):5.2f} clk {m.get('clicks',0)} impr {m.get('impressions',0)}")

print("\n===== C. conversions by action")
for r in q(f"SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign WHERE {WIN} AND {IDS} AND metrics.all_conversions > 0"):
    print(f"  {N[r['campaign']['id']]:<10} {r['segments']['conversion_action_name'][:40]:<40} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== D. ads: approval + final URL")
for r in q(f"""SELECT campaign.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status,
    ad_group_ad.policy_summary.review_status FROM ad_group_ad WHERE {IDS} AND ad_group_ad.status != 'REMOVED'"""):
    a = r["ad_group_ad"]; print(f"  {N[r['campaign']['id']]:<10} {r['ad_group']['name'][:24]:<24} {a['status']} {a['policy_summary'].get('approval_status')}/{a['policy_summary'].get('review_status')} {a['ad'].get('final_urls')}")

print("\n===== E. campaign assets (call, sitelinks, callouts): approval")
for r in q(f"""SELECT campaign.id, campaign_asset.field_type, campaign_asset.status, campaign_asset.primary_status, asset.id, asset.call_asset.phone_number,
    asset.sitelink_asset.link_text, asset.final_urls, asset.policy_summary.approval_status FROM campaign_asset WHERE {IDS} AND campaign_asset.status = 'ENABLED'"""):
    a = r["asset"]; ca = r["campaign_asset"]
    label = a.get("call_asset", {}).get("phone_number") or a.get("sitelink_asset", {}).get("link_text") or a["id"]
    print(f"  {N[r['campaign']['id']]:<10} {ca['field_type']:<16} {ca.get('primary_status')} {a.get('policy_summary',{}).get('approval_status')} {label} {a.get('final_urls','')}")

print("\n===== F. search terms (all, by impressions)")
for r in q(f"""SELECT campaign.id, search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros FROM search_term_view
    WHERE {WIN} AND {IDS} AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 40"""):
    m = r["metrics"]; print(f"  {N[r['campaign']['id']]:<10} {r['search_term_view']['search_term'][:45]:<45} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== G. call_view since 10-22")
for r in q("SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-22 00:00:00' AND '2026-11-04 23:59:59'"):
    c = r["call_view"]; print(f"  {N.get(r['campaign']['id'], r['campaign']['id'])} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== H. keyword volume signal (impressions by keyword)")
for r in q(f"""SELECT campaign.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, metrics.impressions, metrics.clicks
    FROM keyword_view WHERE {WIN} AND {IDS} AND ad_group_criterion.status = 'ENABLED' ORDER BY metrics.impressions DESC LIMIT 25"""):
    k = r["ad_group_criterion"]; m = r["metrics"]
    print(f"  {N[r['campaign']['id']]:<10} {k['keyword']['text'][:35]:<35} {k['keyword']['match_type'][:6]} QS {k.get('quality_info',{}).get('quality_score','-')} impr {m.get('impressions',0)} clk {m.get('clicks',0)}")
