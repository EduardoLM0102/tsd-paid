# READ-ONLY. ./tsd.sh napps_review_1119.py  -- Napps Oct/Nov review cycle 10-19..11-17 spend (fu-170)
import sys; sys.path.insert(0, ".")
from lib import run_query
W = "segments.date BETWEEN '2026-10-19' AND '2026-11-17'"
M = lambda x: int(x or 0) / 1e6
for cid, lab in (("9509605037", "PPC"), ("9239407401", "LSA")):
    tot = 0
    print("=====", lab, cid)
    for r in run_query(cid, f"SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.status, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions FROM campaign WHERE {W} AND metrics.cost_micros > 0"):
        c, m = r["campaign"], r["metrics"]; s = M(m.get("cost_micros")); tot += s
        print(f"  {c['name'][:45]:<45} {c.get('advertising_channel_type')} {c['status']} ${s:,.2f} clk {m.get('clicks',0)} conv {float(m.get('conversions',0)):.1f}")
    print(f"  TOTAL ${tot:,.2f}")
print("===== PPC conv by action")
for r in run_query("9509605037", f"SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM campaign WHERE {W} AND metrics.all_conversions > 0"):
    print(f"  {r['campaign']['name'][:35]:<35} {r['segments']['conversion_action_name']:<35} conv {float(r['metrics'].get('conversions',0)):.1f} all {float(r['metrics'].get('all_conversions',0)):.1f}")
print("===== PPC call_view (ad call button)")
for r in run_query("9509605037", f"SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, campaign.name, call_view.caller_area_code FROM call_view WHERE call_view.start_call_date_time >= '2026-10-19 00:00:00' AND call_view.start_call_date_time <= '2026-11-17 23:59:59'"):
    v = r["callView"] if "callView" in r else r["call_view"]
    print(f"  {v.get('startCallDateTime') or v.get('start_call_date_time')} {v.get('callDurationSeconds') or v.get('call_duration_seconds')}s {v.get('callStatus') or v.get('call_status')} ({v.get('callerAreaCode') or v.get('caller_area_code')}) {r['campaign']['name']}")
