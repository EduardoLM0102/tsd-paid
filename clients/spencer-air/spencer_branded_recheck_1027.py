# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Spencer Air (2524618054), 2026-10-27 recheck (Command Center fu-073). Branded 23822436393 moved 10-20 night from Max Conv to
Target IS 95% abs-top, $8 cap. POST = 10-21 -> 10-26 (6d), PRE = 10-07 -> 10-20 (14d). Also call_view, LSA spend (where unspent
Branded money could go), all campaigns with spend, changes since 10-20."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID, BR = "2524618054", "23822436393"
POST = ("segments.date BETWEEN '2026-10-21' AND '2026-10-26'", 6)
PRE = ("segments.date BETWEEN '2026-10-07' AND '2026-10-20'", 14)
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

for label, (win, days) in (("POST 10-21..10-26", POST), ("PRE 10-07..10-20", PRE)):
    print(f"===== A. campaigns with spend {label}")
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type,
        campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
        metrics.search_impression_share, metrics.search_absolute_top_impression_share, metrics.search_top_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND metrics.impressions > 0"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
        print(f"  {c['name'][:42]:<42} {c.get('advertising_channel_type','')[:8]:<8} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | ${sp:,.2f} ({sp/days:.0f}/d) "
              f"clk {cl} CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} | IS {F(m.get('search_impression_share'))*100:.0f} "
              f"top {F(m.get('search_top_impression_share'))*100:.0f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f} "
              f"bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
    print(f"  -- Branded conversions by action {label}")
    for r in q(f"""SELECT segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND campaign.id = {BR} AND metrics.all_conversions > 0"""):
        print(f"     {r['segments']['conversion_action_name']:<40} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")
    print()

print("===== B. Branded daily 10-14..10-26")
for r in q(f"""SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.search_impression_share,
    metrics.search_absolute_top_impression_share FROM campaign WHERE segments.date BETWEEN '2026-10-14' AND '2026-10-26' AND campaign.id = {BR}"""):
    m = r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
    print(f"  {r['segments']['date']} ${sp:6.2f} clk {cl:>2} CPC ${sp/cl if cl else 0:5.2f} impr {m.get('impressions',0):>3} conv {F(m.get('conversions')):.1f} "
          f"IS {F(m.get('search_impression_share'))*100:.0f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f}")

print("\n===== C. Branded settings + search terms POST")
for r in q(f"""SELECT campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros,
    campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.primary_status, campaign.primary_status_reasons FROM campaign WHERE campaign.id = {BR}"""):
    c = r["campaign"]; t = c.get("target_impression_share", {})
    print(f"  {c.get('bidding_strategy_type')} {t.get('location')} {int(t.get('location_fraction_micros',0))/1e4:.0f}% cap ${M(t.get('cpc_bid_ceiling_micros')):.2f} | "
          f"{c.get('primary_status')} {c.get('primary_status_reasons')}")
for r in q(f"""SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {BR} AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 25"""):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term']:<40} impr {m.get('impressions',0):>3} clk {m.get('clicks',0):>2} ${M(m.get('cost_micros')):6.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== D. Google ad calls (call_view) since 10-07")
for r in q("""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code,
    campaign.name FROM call_view WHERE call_view.start_call_date_time >= '2026-10-07 00:00:00' ORDER BY call_view.start_call_date_time"""):
    v = r["call_view"]; print(f"  {v['start_call_date_time'][:16]} {str(v.get('call_duration_seconds')):>4}s {v.get('call_status')} {v.get('caller_area_code')} {r['campaign']['name']}")

print("\n===== E. LSA daily spend 10-14..10-26")
for r in q("""SELECT segments.date, campaign.name, metrics.cost_micros, metrics.impressions FROM campaign
    WHERE segments.date BETWEEN '2026-10-14' AND '2026-10-26' AND campaign.advertising_channel_type = 'LOCAL_SERVICES'"""):
    print(f"  {r['segments']['date']} ${M(r['metrics'].get('cost_micros')):6.2f} impr {r['metrics'].get('impressions',0)}")

print("\n===== F. changes since 10-20")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.client_type, change_event.change_resource_type,
    change_event.resource_change_operation, change_event.changed_fields, change_event.campaign FROM change_event
    WHERE change_event.change_date_time BETWEEN '2026-10-20' AND '2026-10-28' ORDER BY change_event.change_date_time LIMIT 100"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e.get("client_type"), e["change_resource_type"], e["resource_change_operation"], e.get("changed_fields"), e.get("campaign"))
