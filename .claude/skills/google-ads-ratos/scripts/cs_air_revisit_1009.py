import sys
sys.path.insert(0, ".")
from collections import defaultdict, Counter
from lib import run_query

# Read-only revisit of the 10-05 recommendations (tracking, Smart -> PMax, trim Nonbranded).
CID = "5563867754"
NB = "23828098448"


def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)


def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)




hdr("A) CHANGE HISTORY since 2026-10-05")
q = """SELECT change_event.change_date_time, change_event.user_email, change_event.client_type,
       change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields,
       change_event.campaign
       FROM change_event
       WHERE change_event.change_date_time >= '2026-10-05 00:00:00' AND change_event.change_date_time <= '2026-10-09 23:59:59'
       ORDER BY change_event.change_date_time LIMIT 200"""
rows = run_query(CID, q)
for r in rows:
    c = r["change_event"]
    print(f"  {c['change_date_time'][:16]} {str(c.get('user_email'))[:30]:30s} {str(c.get('client_type'))[:22]:22s} "
          f"{c.get('change_resource_type')} {c.get('resource_change_operation')} {str(c.get('changed_fields'))[:60]} "
          f"camp={str(c.get('campaign','')).split('/')[-1]}")
print(f"  total changes: {len(rows)}")

hdr("B) CAMPAIGNS: status, serving, budget, last 7d + 30d")
q = """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
       campaign.advertising_channel_type, campaign.advertising_channel_sub_type, campaign_budget.amount_micros
       FROM campaign WHERE campaign.status != 'REMOVED'"""
camps = {}
for r in run_query(CID, q):
    c = r["campaign"]
    camps[c["id"]] = c["name"]
    print(f"  {c['id']} {c['name'][:42]:42s} {c['status']:8s} {c.get('primary_status')} "
          f"{c.get('primary_status_reasons')} {c.get('advertising_channel_type')}/{c.get('advertising_channel_sub_type')} "
          f"${f(r.get('campaign_budget', {}), 'amount_micros') / 1e6:.0f}/d")
for rng in ("LAST_7_DAYS", "LAST_30_DAYS"):
    print(f"\n  -- {rng} --")
    q = f"""SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions
           FROM campaign WHERE segments.date DURING {rng} AND metrics.impressions > 0"""
    for r in run_query(CID, q):
        m = r["metrics"]
        print(f"  {r['campaign']['name'][:42]:42s} ${f(m,'cost_micros')/1e6:8.2f} clicks={f(m,'clicks',int):5d} "
              f"conv={f(m,'conversions'):5.1f} all={f(m,'all_conversions'):5.1f}")

hdr("C) NETWORK SPLIT last 7 days (non-LSA)")
q = """SELECT campaign.name, segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions
       FROM campaign WHERE segments.date DURING LAST_7_DAYS AND metrics.impressions > 0"""
for r in run_query(CID, q):
    m = r["metrics"]
    print(f"  {r['campaign']['name'][:42]:42s} {r['segments']['ad_network_type']:16s} ${f(m,'cost_micros')/1e6:8.2f} "
          f"clicks={f(m,'clicks',int):5d} conv={f(m,'conversions'):4.1f}")

hdr("D) CONVERSIONS BY ACTION, by conversion date, 2026-09-15 -> 2026-10-08")
q = """SELECT segments.conversion_action_name, campaign.name, metrics.conversions_by_conversion_date,
       metrics.all_conversions_by_conversion_date
       FROM campaign WHERE segments.date BETWEEN '2026-09-15' AND '2026-10-08' AND metrics.all_conversions_by_conversion_date > 0"""
agg = defaultdict(lambda: [0.0, 0.0])
for r in run_query(CID, q):
    m = r["metrics"]
    k = (r["segments"]["conversion_action_name"], r["campaign"]["name"])
    agg[k][0] += f(m, "conversions_by_conversion_date")
    agg[k][1] += f(m, "all_conversions_by_conversion_date")
for (a, c), (v, va) in sorted(agg.items()):
    print(f"  {a[:38]:38s} {c[:40]:40s} conv={v:5.1f} all={va:5.1f}")

hdr("E) CONVERSION ACTIONS config")
q = """SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.origin, conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.phone_call_duration_seconds
       FROM conversion_action WHERE conversion_action.status != 'REMOVED'"""
for r in run_query(CID, q):
    a = r["conversion_action"]
    print(f"  {a['name'][:38]:38s} {str(a.get('type', a.get('type_')))[:28]:28s} {str(a.get('category'))[:18]:18s} {a.get('origin')} "
          f"{a.get('status')} primary={a.get('primary_for_goal')} dur={a.get('phone_call_duration_seconds')}")

hdr("F) CALLS FROM ADS (call_view) since 2026-09-15")
q = """SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status
       FROM call_view WHERE call_view.start_call_date_time >= '2026-09-15 00:00:00'"""
rows = run_query(CID, q)
by = Counter()
for r in rows:
    c = r["call_view"]
    d = int(c.get("call_duration_seconds", 0) or 0)
    by[(r["campaign"]["name"][:40], "60s+" if d >= 60 else ("1-59s" if d > 0 else "0s"))] += 1
for k, v in sorted(by.items()):
    print(f"  {k[0]:40s} {k[1]:6s} {v}")
print(f"  total calls: {len(rows)}")

hdr("G) NONBRANDED: ad groups + keywords, last 30 days")
q = f"""SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'"""
for r in run_query(CID, q):
    g = r["ad_group"]
    print(f"  ad group {g['id']} {g['name']} {g['status']}")
q = f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       ad_group_criterion.status, ad_group_criterion.quality_info.quality_score,
       metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions
       FROM keyword_view WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS
       AND ad_group_criterion.status != 'REMOVED'"""
rows = sorted(run_query(CID, q), key=lambda r: -f(r["metrics"], "cost_micros"))
for r in rows:
    k, m = r["ad_group_criterion"], r["metrics"]
    print(f"  {r['ad_group']['name'][:18]:18s} {k['keyword']['text'][:34]:34s} {k['keyword']['match_type'][:6]:6s} "
          f"{k['status']:7s} QS={k.get('quality_info', {}).get('quality_score')} ${f(m,'cost_micros')/1e6:7.2f} "
          f"clicks={f(m,'clicks',int):3d} conv={f(m,'conversions'):3.1f} all={f(m,'all_conversions'):3.1f}")
