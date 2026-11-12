# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""All Seasons AC (4467722415), 2026-11-11 read (Command Center fu-128): first week after the 11-04 leak fixes
(COMPETITORS list on MiniSplit + 11 names, 'insulation' neg, 'mini split heat pump' broad -> phrase, taps + GA4 CONTACT -> Secondary).
POST = 11-04..11-10 (7d) vs PRE = 10-23..11-03 (12d). LSA = separate CID 8655979348."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID, LSA = "4467722415", "8655979348"
POST = ("segments.date BETWEEN '2026-11-04' AND '2026-11-10'", 7)
PRE = ("segments.date BETWEEN '2026-10-23' AND '2026-11-03'", 12)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
pct = lambda x: f"{F(x)*100:.0f}%"
q = lambda s: run_query(CID, s)

for label, (win, days) in (("POST 11-04..11-10", POST), ("PRE 10-23..11-03", PRE)):
    print(f"\n===== A. campaigns {label}")
    tot = 0
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks,
        metrics.impressions, metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND metrics.cost_micros > 0"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); tot += sp
        print(f"  {c['id']} {c['name'][:34]:34s} {c['status'][:7]} {c.get('bidding_strategy_type','')[:14]:14s} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | ${sp:7.2f} ({sp/days:.0f}/d) impr {m.get('impressions',0):>5} clk {cl:>3}"
              f" CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} | IS {pct(m.get('search_impression_share'))} budL {pct(m.get('search_budget_lost_impression_share'))} rankL {pct(m.get('search_rank_lost_impression_share'))}")
    print(f"  TOTAL ${tot:,.2f} = ${tot/days:.2f}/day")
    print(f"  -- conversions by action ({label})")
    for r in q(f"""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign WHERE {win} AND metrics.all_conversions > 0"""):
        print(f"     {r['campaign']['name'][:30]:30s} {r['segments']['conversion_action_name'][:42]:42s} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== B. search terms POST (clicks > 0), brand vs competitor vs rest")
rows = q(f"""SELECT campaign.name, search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC""")
brand = sum(M(r["metrics"].get("cost_micros")) for r in rows if "all season" in r["search_term_view"]["search_term"].lower())
tot = sum(M(r["metrics"].get("cost_micros")) for r in rows)
print(f"  visible term spend ${tot:.2f}, brand ('all season') ${brand:.2f}")
for r in rows[:40]:
    m = r["metrics"]; print(f"  {r['campaign']['name'][:18]:18s} ${M(m.get('cost_micros')):6.2f} {m.get('clicks',0):>2} clk conv {F(m.get('conversions')):.1f} | {r['search_term_view']['search_term'][:60]}")

print("\n===== C. calls from ads POST (call_view)")
for r in q("""SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
        FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-11-04 00:00:00' AND '2026-11-10 23:59:59' ORDER BY call_view.start_call_date_time"""):
    c = r["call_view"]; print(f"  {r['campaign']['name'][:22]:22s} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== D. conversion actions: primary/secondary state (11-04 change held?)")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.category, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric
        FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    a = r["conversion_action"]
    print(f"  {a['id']} {a['name'][:44]:44s} {a.get('category','')[:16]:16s} {'primary' if a.get('primary_for_goal') else 'secondary'} in_conv={a.get('include_in_conversions_metric')}")

print("\n===== E. LSA 8655979348: delivery + leads since 11-01")
try:
    for r in run_query(LSA, """SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros, metrics.cost_micros, metrics.impressions
            FROM campaign WHERE segments.date BETWEEN '2026-11-01' AND '2026-11-10' AND campaign.status != 'REMOVED'"""):
        c = r["campaign"]; print(f"  {c['id']} {c['name'][:40]} {c.get('advertising_channel_type')} {c['status']} bud ${M(r['campaign_budget'].get('amount_micros')):.0f}/d spend ${M(r['metrics'].get('cost_micros')):.2f} impr {r['metrics'].get('impressions',0)}")
    leads = run_query(LSA, """SELECT local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time
            FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-01 00:00:00'""")
    for l in sorted(leads, key=lambda l: l["local_services_lead"]["creation_date_time"]):
        x = l["local_services_lead"]; print(f"  lead {x['creation_date_time'][:16]} {x['lead_type']:12s} {x['lead_status']:16s} charged={x.get('lead_charged', False)}")
    print(f"  {len(leads)} leads since 11-01, charged {sum(1 for l in leads if l['local_services_lead'].get('lead_charged'))}")
except Exception as e:
    print("  LSA ERROR", str(e).splitlines()[0][:160])

print("\n===== F. changes since 11-04")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.changed_fields, change_event.campaign
        FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-05' AND '2026-11-11' ORDER BY change_event.change_date_time LIMIT 40"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], (e.get("changed_fields") or "")[:60], (e.get("campaign") or "")[-11:])
