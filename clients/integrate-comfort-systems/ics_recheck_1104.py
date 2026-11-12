# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Integrate Comfort (4571881760), 2026-11-04 recheck (Command Center fu-109) of the 10-28 changes: PMax $40 on custom goal
'TSD | Calls + Forms (no taps)' 6459689709, NonBranded heating-only Max Clicks $15 cap $22/d, Branded $15/d.
POST = 10-29 -> 11-03 (6d) vs PRE = 10-09 -> 10-26 (18d, the 10-28 checkpoint window). First question: does PMax still count taps
(the same custom goal failed on Watt's Right, 2026-11-03)?"""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "4571881760"
PM, NB, BR = "22890783804", "24047025253", "23675636592"
NAMES = {PM: "PMax", NB: "NonBranded", BR: "Branded"}
POST = ("segments.date BETWEEN '2026-10-29' AND '2026-11-03'", 6)
PRE = ("segments.date BETWEEN '2026-10-09' AND '2026-10-26'", 18)
IDS = f"campaign.id IN ({PM},{NB},{BR})"
REAL = {"Calls from ads", "Landing Page Call", "Submit lead form - web", "Lead form - Submit"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. tap action + PMax goal config")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.origin,
    conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.phone_call_duration_seconds
    FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    a = r["conversion_action"]
    print(f"  {a['id']} {a['name'][:40]:<40} {a.get('type_')} {a.get('category')} {a.get('origin')} {'primary' if a.get('primary_for_goal') else 'secondary'} in_conv={a.get('include_in_conversions_metric')} {a.get('phone_call_duration_seconds')}s")
for r in q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id = {PM}"):
    print("  PMax goal cfg:", r["conversion_goal_campaign_config"])

for label, (win, days) in (("POST 10-29..11-03", POST), ("PRE 10-09..10-26", PRE)):
    print(f"\n===== B. campaigns {label}")
    spend = {}
    for r in q(f"""SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks,
        metrics.impressions, metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND {IDS}"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); spend[c["id"]] = sp
        print(f"  {NAMES[c['id']]:<11} {c.get('bidding_strategy_type')} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | ${sp:,.2f} ({sp/days:.0f}/d) clk {cl} "
              f"CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} | IS {F(m.get('search_impression_share'))*100:.0f} "
              f"bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
    real = collections.defaultdict(float)
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND {IDS} AND metrics.all_conversions > 0"""):
        n = r["segments"]["conversion_action_name"]; al = F(r["metrics"].get("all_conversions"))
        if n in REAL: real[r["campaign"]["id"]] += al
        print(f"     {NAMES[r['campaign']['id']]:<11} {n[:42]:<42} conv {F(r['metrics'].get('conversions')):.1f} all {al:.1f}")
    for k in (PM, NB, BR):
        v = real.get(k, 0); print(f"     REAL {NAMES[k]:<11} {v:.1f} -> ${spend.get(k,0)/v if v else 0:,.2f}/real lead")

print("\n===== C. PMax network split")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE {win} AND campaign.id = {PM}"):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>5} conv {F(m.get('conversions')):.1f}")

print("\n===== D. call_view 10-29..11-03 (ad call button, all campaigns)")
for r in q("""SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-29 00:00:00' AND '2026-11-03 23:59:59'"""):
    c = r["call_view"]; print(f"  {NAMES.get(r['campaign']['id'], r['campaign']['id'])[:11]:<11} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== E. NonBranded ad groups + search terms POST")
for r in q(f"""SELECT ad_group.name, ad_group.status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions,
    metrics.search_rank_lost_impression_share FROM ad_group WHERE {POST[0]} AND campaign.id = {NB}"""):
    m = r["metrics"]; print(f"  {r['ad_group']['name']:<34} {r['ad_group']['status']:<7} impr {m.get('impressions',0):>4} clk {m.get('clicks',0):>3} ${M(m.get('cost_micros')):7.2f} all {F(m.get('all_conversions')):.1f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
for r in q(f"""SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.all_conversions FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {NB} AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 25"""):
    m = r["metrics"]; print(f"    {r['search_term_view']['search_term'][:48]:<48} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} all {F(m.get('all_conversions')):.1f}")

print("\n===== F. changes since 10-28")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
    FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-28' AND '2026-11-05' ORDER BY change_event.change_date_time LIMIT 50"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:70], (e.get("campaign") or "")[-11:])
