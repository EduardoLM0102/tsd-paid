# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-11-03 (Command Center fu-098): first week of PMax 23833205176 on the custom goal
'TSD | Calls + Forms (no taps)' (6459658990, set 10-27). POST = 10-28 -> 11-02 (6d), PRE = 10-20 -> 10-26 (7d).
Why do [TSD] Click to call taps still show in PMax's Conversions column?"""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID, PM, TAP = "3651667805", "23833205176", "7835456094"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. tap action + its bucket-mates")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.origin,
    conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric, conversion_action.status,
    conversion_action.phone_call_duration_seconds, conversion_action.counting_type FROM conversion_action
    WHERE conversion_action.category = 'PHONE_CALL_LEAD'"""):
    a = r["conversion_action"]; print(" ", a)

print("\n===== B. PMax campaign_conversion_goal (category/origin biddable)")
for r in q(f"""SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
    FROM campaign_conversion_goal WHERE campaign.id = {PM}"""):
    g = r["campaign_conversion_goal"]; print(f"  {g['category']:<20} {g['origin']:<16} biddable={g.get('biddable')}")

print("\n===== C. PMax daily: spend by network + conv (goal column) vs all, taps vs real")
day = collections.defaultdict(lambda: collections.defaultdict(float))
for r in q(f"""SELECT segments.date, segments.ad_network_type, metrics.cost_micros, metrics.clicks FROM campaign
    WHERE campaign.id = {PM} AND segments.date BETWEEN '2026-10-20' AND '2026-11-02'"""):
    d = day[r["segments"]["date"]]; d[r["segments"]["ad_network_type"]] += M(r["metrics"].get("cost_micros")); d["clk"] += int(r["metrics"].get("clicks", 0))
for r in q(f"""SELECT segments.date, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
    WHERE campaign.id = {PM} AND segments.date BETWEEN '2026-10-20' AND '2026-11-02' AND metrics.all_conversions > 0"""):
    d = day[r["segments"]["date"]]; n = r["segments"]["conversion_action_name"]
    k = "tap" if n == "[TSD] Click to call" else ("yt" if "YouTube" in n else "real")
    d[k + "_conv"] += F(r["metrics"].get("conversions")); d[k + "_all"] += F(r["metrics"].get("all_conversions"))
for dt in sorted(day):
    d = day[dt]
    print(f"  {dt} Search ${d['SEARCH']:6.2f} Display ${d['CONTENT']:6.2f} YouTube ${d['YOUTUBE']:6.2f} | clk {int(d['clk']):>4} | "
          f"taps conv {d['tap_conv']:.0f}/all {d['tap_all']:.0f} | real conv {d['real_conv']:.0f}/all {d['real_all']:.0f}")

print("\n===== D. PMax call_view 10-20..11-02 (ad call button)")
for r in q(f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-20 00:00:00' AND '2026-11-02 23:59:59' AND campaign.id = {PM}"""):
    c = r["call_view"]; print(f"  {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== E. PMax asset groups POST")
for r in q(f"""SELECT asset_group.name, asset_group.status, metrics.cost_micros, metrics.clicks, metrics.conversions FROM asset_group
    WHERE campaign.id = {PM} AND segments.date BETWEEN '2026-10-28' AND '2026-11-02'"""):
    m = r["metrics"]; print(f"  {r['asset_group']['name']:<35} {r['asset_group']['status']} ${M(m.get('cost_micros')):.2f} clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f}")

print("\n===== F. PMax bidding + budget now")
for r in q(f"""SELECT campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros,
    campaign.primary_status, campaign.primary_status_reasons FROM campaign WHERE campaign.id = {PM}"""):
    print(" ", r["campaign"], "budget", M(r["campaign_budget"].get("amount_micros")))
