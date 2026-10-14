import sys
sys.path.insert(0, ".")
from collections import defaultdict, Counter
from lib import run_query
CID = "7953905280"
TAG = {"23825900343": "NB", "23739724064": "BR", "21225221220": "PMAX"}
def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)
def hdr(t): print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

hdr("A) CONVERSIONS BY ACTION x CAMPAIGN x CONVERSION DATE, Aug 29 - Oct 8")
q = """SELECT segments.date, campaign.id, segments.conversion_action_name, metrics.conversions_by_conversion_date,
       metrics.all_conversions_by_conversion_date
       FROM campaign WHERE segments.date BETWEEN '2026-08-29' AND '2026-10-08' AND metrics.all_conversions_by_conversion_date > 0"""
for r in sorted(run_query(CID, q), key=lambda r: r["segments"]["date"]):
    m = r["metrics"]
    print(f"  {r['segments']['date']} {TAG.get(r['campaign']['id'], r['campaign']['id']):5s} {r['segments']['conversion_action_name'][:45]:45s} "
          f"conv={f(m,'conversions_by_conversion_date'):3.1f} all={f(m,'all_conversions_by_conversion_date'):3.1f}")

hdr("B) CALL DETAILS (call_view) Aug 29 - Oct 8")
q = """SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
       call_view.caller_area_code, call_view.call_tracking_display_location, call_view.type
       FROM call_view WHERE call_view.start_call_date_time >= '2026-08-29 00:00:00'"""
rows = run_query(CID, q)
st, ac, loc, dur = Counter(), Counter(), Counter(), Counter()
for r in sorted(rows, key=lambda r: r["call_view"]["start_call_date_time"]):
    c = r["call_view"]
    d = int(c.get("call_duration_seconds", 0) or 0)
    st[c.get("call_status")] += 1
    ac[c.get("caller_area_code")] += 1
    loc[(c.get("call_tracking_display_location"), c.get("type_", c.get("type")))] += 1
    dur["60s+" if d >= 60 else ("1-59s" if d > 0 else "0s")] += 1
    print(f"  {c['start_call_date_time'][:16]} {TAG.get(r['campaign']['id'], r['campaign']['id']):5s} {c.get('call_status'):9s} "
          f"{d:4d}s area={c.get('caller_area_code')} {c.get('call_tracking_display_location')}")
print(f"\n  total={len(rows)} status={dict(st)} duration={dict(dur)}\n  area codes={dict(ac)}\n  display/type={dict(loc)}")
