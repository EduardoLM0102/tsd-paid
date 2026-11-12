# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Nick's Heating (1854100356), 2026-11-04 recheck (Command Center fu-108) of the 10-28 PMax brand exclusion + 10 competitor negatives.
POST = 10-29 -> 11-03 (6d) vs PRE = 10-22 -> 10-27 (6d, the 10-28 recheck window). Leads by conversion date. Also: tap action status
(the no-taps custom goal leaked on Watt's Right + ICS), Branded pickup, LSA leads + marking."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "1854100356"
NB, BR, PM, LSA = "23821497590", "23675600637", "23586346547", "23344968885"
NAMES = {NB: "NB AC", BR: "Branded", PM: "PMax", LSA: "LSA"}
POST = ("segments.date BETWEEN '2026-10-29' AND '2026-11-03'", 6)
PRE = ("segments.date BETWEEN '2026-10-22' AND '2026-10-27'", 6)
IDS = f"campaign.id IN ({NB},{BR},{PM},{LSA})"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. conversion actions (primary/in Conversions) + PMax goal config")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.origin,
    conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.phone_call_duration_seconds
    FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    a = r["conversion_action"]
    if a.get("include_in_conversions_metric") or a.get("type_") == "CLICK_TO_CALL":
        print(f"  {a['id']} {a['name'][:40]:<40} {a.get('type_')} {a.get('category')} {a.get('origin')} {'primary' if a.get('primary_for_goal') else 'secondary'} in_conv={a.get('include_in_conversions_metric')} {a.get('phone_call_duration_seconds')}s")
for r in q(f"SELECT campaign.id, conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id IN ({NB},{BR},{PM})"):
    print("  goal cfg", NAMES[r["campaign"]["id"]], r["conversion_goal_campaign_config"].get("goal_config_level"), r["conversion_goal_campaign_config"].get("custom_conversion_goal", "-"))
for r in q(f"SELECT campaign.id, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE {IDS.replace('segments','')}"):
    print("  ", NAMES[r["campaign"]["id"]], r["campaign"].get("bidding_strategy_type"), r["campaign"].get("primary_status"), f"${M(r['campaign_budget'].get('amount_micros')):.0f}/d")

for label, (win, days) in (("POST 10-29..11-03", POST), ("PRE 10-22..10-27", PRE)):
    print(f"\n===== B. campaigns {label} (conv = by conversion date)")
    for r in q(f"""SELECT campaign.id, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions_by_conversion_date,
        metrics.all_conversions_by_conversion_date, metrics.search_impression_share, metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND {IDS}"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); cv = F(m.get("conversions_by_conversion_date"))
        print(f"  {NAMES[c['id']]:<8} ${sp:7.2f} ({sp/days:.0f}/d) clk {cl:>3} impr {m.get('impressions',0):>5} CPC ${sp/cl if cl else 0:.2f} conv {cv:.1f} "
              f"all {F(m.get('all_conversions_by_conversion_date')):.1f} CPL ${sp/cv if cv else 0:,.2f} | IS {F(m.get('search_impression_share'))*100:.0f} "
              f"bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions_by_conversion_date, metrics.all_conversions_by_conversion_date
        FROM campaign WHERE {win} AND {IDS} AND metrics.all_conversions_by_conversion_date > 0"""):
        m = r["metrics"]; print(f"     {NAMES[r['campaign']['id']]:<8} {r['segments']['conversion_action_name'][:42]:<42} conv {F(m.get('conversions_by_conversion_date')):.1f} all {F(m.get('all_conversions_by_conversion_date')):.1f}")

print("\n===== C. PMax network split")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE {win} AND campaign.id = {PM}"):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>5} conv {F(m.get('conversions')):.1f}")

print("\n===== D. PMax daily POST")
for r in q(f"SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.conversions_by_conversion_date FROM campaign WHERE {POST[0]} AND campaign.id = {PM} ORDER BY segments.date"):
    m = r["metrics"]; print(f"  {r['segments']['date']} ${M(m.get('cost_micros')):6.2f} clk {m.get('clicks',0)} conv {F(m.get('conversions_by_conversion_date')):.1f}")

print("\n===== E. PMax search term categories POST (brand leak gone?)")
for r in q(f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.impressions, metrics.conversions
    FROM campaign_search_term_insight WHERE campaign_search_term_insight.campaign_id = '{PM}' AND {POST[0]} ORDER BY metrics.clicks DESC LIMIT 25"""):
    m = r["metrics"]; print(f"  {r['campaign_search_term_insight'].get('category_label','(blank)')[:50]:<50} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>5} conv {F(m.get('conversions')):.1f}")

print("\n===== F. Branded search terms POST")
for r in q(f"""SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {BR} AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 15"""):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term'][:45]:<45} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== G. call_view 10-29..11-03")
for r in q("""SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-29 00:00:00' AND '2026-11-03 23:59:59'"""):
    c = r["call_view"]; print(f"  {NAMES.get(r['campaign']['id'], r['campaign']['id'])[:8]:<8} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== H. LSA leads since 10-22 (marking)")
for r in q("""SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status,
    local_services_lead.lead_charged, local_services_lead.category_id FROM local_services_lead
    WHERE local_services_lead.creation_date_time >= '2026-10-22 00:00:00' ORDER BY local_services_lead.creation_date_time"""):
    l = r["local_services_lead"]; print(f"  {l['creation_date_time'][:16]} {l.get('lead_type'):<9} {l.get('lead_status'):<10} charged={l.get('lead_charged')} {l.get('category_id','')}")

print("\n===== I. changes since 10-28")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
    FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-28' AND '2026-11-05' ORDER BY change_event.change_date_time LIMIT 50"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:70], (e.get("campaign") or "")[-11:])
