# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""All Seasons AC (4467722415), 2026-11-04 (Command Center fu-089, due 10-29): first full read after the 10-22 cleanup (520 phrase negatives,
898 keywords paused, LeadGen 979 -> 83 live) and the 10-23 NB pause ($8 -> LeadGen). POST 10-23 -> 11-03 (12d) vs PRE 10-11 -> 10-21 (11d)."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"
POST = ("segments.date BETWEEN '2026-10-23' AND '2026-11-03'", 12)
PRE = ("segments.date BETWEEN '2026-10-11' AND '2026-10-21'", 11)
REAL = {"Calls from ads", "Call ext LEAD", "[TSD] Lead Form", "Submit lead form"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. conversion actions in Conversions (+ taps)")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.origin,
    conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.phone_call_duration_seconds FROM conversion_action
    WHERE conversion_action.status = 'ENABLED'"""):
    a = r["conversion_action"]
    if a.get("include_in_conversions_metric") or a.get("type_") == "CLICK_TO_CALL":
        print(f"  {a['id']} {a['name'][:40]:<40} {a.get('type_')} {a.get('category')} {a.get('origin')} {'primary' if a.get('primary_for_goal') else 'secondary'} in_conv={a.get('include_in_conversions_metric')} {a.get('phone_call_duration_seconds')}s")

for label, (win, days) in (("POST 10-23..11-03", POST), ("PRE 10-11..10-21", PRE)):
    print(f"\n===== B. campaigns with spend {label}")
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros,
        metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions, metrics.search_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND metrics.impressions > 0"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
        print(f"  {c['id']} {c['name'][:34]:<34} {c['status'][:7]:<7} {c.get('advertising_channel_type','')[:6]} {c.get('bidding_strategy_type','')[:18]:<18} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | "
              f"${sp:7.2f} ({sp/days:.0f}/d) clk {cl:>3} impr {m.get('impressions',0):>5} CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} | IS {F(m.get('search_impression_share'))*100:.0f} "
              f"bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
    for r in q(f"""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND metrics.all_conversions > 0 AND campaign.advertising_channel_type != 'LOCAL_SERVICES'"""):
        print(f"     {r['campaign']['name'][:30]:<30} {r['segments']['conversion_action_name'][:36]:<36} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== C. search terms POST (by cost, non-LSA)")
for r in q(f"""SELECT campaign.name, search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 40"""):
    m = r["metrics"]; print(f"  {r['campaign']['name'][:18]:<18} {r['search_term_view']['search_term'][:46]:<46} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== D. call_view POST")
for r in q("""SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-23 00:00:00' AND '2026-11-03 23:59:59'"""):
    c = r["call_view"]; print(f"  {r['campaign']['name'][:24]:<24} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== E. MiniSplit keywords POST (broad still converting?)")
for r in q(f"""SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM keyword_view WHERE {POST[0]} AND campaign.name LIKE '%ini%' AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 15"""):
    k = r["ad_group_criterion"]["keyword"]; m = r["metrics"]
    print(f"  {k['text'][:36]:<36} {k['match_type'][:6]} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== F. changes since 10-23")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
    FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-23' AND '2026-11-05' ORDER BY change_event.change_date_time LIMIT 40"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:60], (e.get("campaign") or "")[-11:])
