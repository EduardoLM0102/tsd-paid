"""Read-only weekly 7-day pull for the AT '7-Day Google Search Ads' tasks.

Run from the skill scripts dir via tsd.sh:
  ./tsd.sh /abs/path/weekly_pull.py <out_dir> <start> <end> <prev_start> <prev_end> <cid> [<cid> ...]
Writes <out_dir>/<cid>.json with campaigns (this + prior week), conversions by action,
search terms, keywords, networks, daily spend, call_view calls and recent change events.
Nothing is mutated.
"""
import json, os, sys
sys.path.insert(0, ".")
from lib import run_query

out_dir, start, end, pstart, pend = sys.argv[1:6]
cids = sys.argv[6:]
os.makedirs(out_dir, exist_ok=True)

def q(cid, query):
    try:
        return list(run_query(cid, query))
    except Exception as e:  # keep going, record the error
        return {"error": str(e)[:500]}

def rng(a, b):
    return f"segments.date BETWEEN '{a}' AND '{b}'"

CAMP = """
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status,
       campaign.advertising_channel_type, campaign.bidding_strategy_type,
       campaign_budget.amount_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
       campaign.maximize_conversions.target_cpa_micros, campaign.target_spend.cpc_bid_ceiling_micros,
       campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share, metrics.average_cpc
FROM campaign WHERE {r} AND campaign.status != 'REMOVED'
"""

for cid in cids:
    d = {"cid": cid, "window": [start, end], "prev": [pstart, pend]}
    d["campaigns"] = q(cid, CAMP.format(r=rng(start, end)))
    d["campaigns_prev"] = q(cid, CAMP.format(r=rng(pstart, pend)))
    d["campaigns_enabled"] = q(cid, """
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
       campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros
FROM campaign WHERE campaign.status = 'ENABLED'""")
    d["conv_by_action"] = q(cid, f"""
SELECT campaign.id, campaign.name, segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM campaign WHERE {rng(start, end)} AND metrics.all_conversions > 0""")
    d["conv_by_action_prev"] = q(cid, f"""
SELECT campaign.id, segments.conversion_action_name, metrics.conversions
FROM campaign WHERE {rng(pstart, pend)} AND metrics.conversions > 0""")
    d["search_terms"] = q(cid, f"""
SELECT campaign.id, campaign.name, ad_group.name, search_term_view.search_term, search_term_view.status,
       segments.keyword.info.text, segments.keyword.info.match_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view WHERE {rng(start, end)} AND metrics.impressions > 0""")
    d["keywords"] = q(cid, f"""
SELECT campaign.id, campaign.name, ad_group.name, ad_group_criterion.criterion_id,
       ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
       ad_group_criterion.quality_info.quality_score,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM keyword_view WHERE {rng(start, end)} AND metrics.impressions > 0""")
    d["networks"] = q(cid, f"""
SELECT campaign.id, campaign.name, segments.ad_network_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM campaign WHERE {rng(start, end)} AND metrics.impressions > 0""")
    d["daily"] = q(cid, f"""
SELECT campaign.id, campaign.name, segments.date, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM campaign WHERE {rng(start, end)} AND metrics.impressions > 0""")
    d["calls"] = q(cid, f"""
SELECT call_view.call_duration_seconds, call_view.start_call_date_time, call_view.call_status,
       call_view.type, campaign.id, campaign.name
FROM call_view WHERE call_view.start_call_date_time >= '{start} 00:00:00'
  AND call_view.start_call_date_time <= '{end} 23:59:59'""")
    d["changes"] = q(cid, f"""
SELECT change_event.change_date_time, change_event.user_email, change_event.client_type,
       change_event.change_resource_type, change_event.resource_change_operation,
       change_event.changed_fields, change_event.campaign
FROM change_event WHERE change_event.change_date_time >= '{pstart}'
  AND change_event.change_date_time <= '{end} 23:59:59'
ORDER BY change_event.change_date_time DESC LIMIT 200""")
    with open(os.path.join(out_dir, f"{cid}.json"), "w") as f:
        json.dump(d, f, indent=1, default=str)
    errs = [k for k, v in d.items() if isinstance(v, dict) and "error" in v]
    print(cid, "ok", "errors:", errs)
