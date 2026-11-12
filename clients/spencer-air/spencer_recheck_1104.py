# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Spencer Air (2524618054), 2026-11-04: fu-111 Branded recheck after the 10-28 cap $8 -> $10 (Target IS 95% abs-top) and the Spencer half
of fu-031 (do CallRail uploads land as First Time / Repeat since the 10-20 fix?). POST = 10-29 -> 11-03 (6d) vs PRE = 10-21 -> 10-27 (7d on $8)."""
import sys
sys.path.insert(0, ".")
from lib import run_query

CID, BR = "2524618054", "23822436393"
POST = ("segments.date BETWEEN '2026-10-29' AND '2026-11-03'", 6)
PRE = ("segments.date BETWEEN '2026-10-21' AND '2026-10-27'", 7)
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. enabled campaigns now")
for r in q("""SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.bidding_strategy_type,
    campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.status = 'ENABLED'"""):
    c = r["campaign"]
    print(f"  {c['name'][:45]:<45} {c.get('advertising_channel_type')} {c.get('bidding_strategy_type')} cap ${M((c.get('target_impression_share') or {}).get('cpc_bid_ceiling_micros')):.0f} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} {c.get('primary_status')}")

for label, (win, days) in (("POST 10-29..11-03", POST), ("PRE 10-21..10-27", PRE)):
    print(f"\n===== B. Branded {label}")
    for r in q(f"""SELECT metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions_by_conversion_date, metrics.all_conversions_by_conversion_date,
        metrics.search_impression_share, metrics.search_absolute_top_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share FROM campaign WHERE {win} AND campaign.id = {BR}"""):
        m = r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
        print(f"  ${sp:.2f} ({sp/days:.1f}/d) clk {cl} impr {m.get('impressions',0)} CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions_by_conversion_date')):.1f} "
              f"all {F(m.get('all_conversions_by_conversion_date')):.1f} | IS {F(m.get('search_impression_share'))*100:.0f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f} "
              f"rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f}")
    for r in q(f"""SELECT segments.conversion_action_name, metrics.conversions_by_conversion_date, metrics.all_conversions_by_conversion_date
        FROM campaign WHERE {win} AND campaign.id = {BR} AND metrics.all_conversions_by_conversion_date > 0"""):
        m = r["metrics"]; print(f"     {r['segments']['conversion_action_name'][:40]:<40} conv {F(m.get('conversions_by_conversion_date')):.1f} all {F(m.get('all_conversions_by_conversion_date')):.1f}")

print("\n===== C. Branded daily 10-21..11-03")
for r in q(f"""SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share,
    metrics.search_absolute_top_impression_share FROM campaign WHERE segments.date BETWEEN '2026-10-21' AND '2026-11-03' AND campaign.id = {BR} ORDER BY segments.date"""):
    m = r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
    print(f"  {r['segments']['date']} ${sp:6.2f} clk {cl} impr {m.get('impressions',0):>3} CPC ${sp/cl if cl else 0:5.2f} IS {F(m.get('search_impression_share'))*100:.0f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f}")

print("\n===== D. call_view since 10-21 (ad call button)")
for r in q("""SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-21 00:00:00' AND '2026-11-03 23:59:59'"""):
    c = r["call_view"]; print(f"  {r['campaign']['name'][:30]} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== E. account conversions by action + date since 10-20 (CallRail uploads?)")
for r in q("""SELECT segments.date, segments.conversion_action_name, metrics.all_conversions_by_conversion_date FROM customer
    WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-03' AND metrics.all_conversions_by_conversion_date > 0 ORDER BY segments.date"""):
    print(f"  {r['segments']['date']} {r['segments']['conversion_action_name'][:45]:<45} {F(r['metrics'].get('all_conversions_by_conversion_date')):.1f}")

print("\n===== F. Branded search terms POST")
for r in q(f"""SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {BR} AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 12"""):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term'][:45]:<45} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== G. changes since 10-28")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
    FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-28' AND '2026-11-05' ORDER BY change_event.change_date_time LIMIT 50"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:70], (e.get("campaign") or "")[-11:])
