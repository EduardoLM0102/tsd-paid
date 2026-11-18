# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-11-17: fu-145. First week with PMax paused + Branded $145 (Target IS 95% top, $8 ceiling) + 6 negs on NB
(applied 11-10 09:13-09:14 -03). POST = 11-10 -> 11-16 (7d), PRE = 11-04 -> 11-09 (6d, Branded $50, PMax on)."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PM, PPL = "23690645223", "23832838033", "23833205176", "24425981973"
NAMES = {BR: "Branded", NB: "Nonbranded", PM: "PMax", PPL: "LSA-PPL"}
POST = ("segments.date BETWEEN '2026-11-10' AND '2026-11-16'", 7)
PRE = ("segments.date BETWEEN '2026-11-04' AND '2026-11-09'", 6)
REAL = {"Calls from ads", "Phone Call", "Submit lead form - web", "Form Submission [Landing Page]", "Phone calls (Pay-per-lead goals)"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
IDS = f"campaign.id IN ({BR},{NB},{PM},{PPL})"

import os
PART = os.environ.get("PART")
for label, (win, days) in (() if PART else (("POST 11-10..11-16", POST), ("PRE 11-04..11-09", PRE))):
    print(f"===== A. campaigns {label}")
    spend = {}
    for r in q(f"""SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
        campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions,
        metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE {win} AND {IDS}"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); spend[c["id"]] = sp
        print(f"{NAMES[c['id']]:<10} {c['status']} {c.get('bidding_strategy_type')} tCPA={M(c.get('maximize_conversions',{}).get('target_cpa_micros'))} "
              f"bud ${M(r['campaign_budget'].get('amount_micros')):.0f}/d | ${sp:,.2f} (${sp/days:.0f}/d) clk {cl} CPC ${sp/cl if cl else 0:.2f} "
              f"conv {F(m.get('conversions')):.1f} | IS {F(m.get('search_impression_share'))*100:.0f} budlost {F(m.get('search_budget_lost_impression_share'))*100:.0f} "
              f"ranklost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
    print(f"--- B. conversions by action {label}")
    real = collections.defaultdict(float)
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND {IDS} AND metrics.all_conversions > 0"""):
        n = r["segments"]["conversion_action_name"]; al = F(r["metrics"].get("all_conversions"))
        if n in REAL: real[r["campaign"]["id"]] += al
        print(f"  {NAMES[r['campaign']['id']]:<10} {n:<38} conv {F(r['metrics'].get('conversions')):.1f} all {al:.1f}")
    for k in (BR, NB, PM, PPL):
        v = real.get(k, 0); print(f"  REAL {NAMES[k]:<10} {v:.1f} leads, spend ${spend.get(k,0):,.2f} -> CPL ${spend.get(k,0)/v if v else 0:,.2f}")
    print()

print("===== C. Branded + NB + PMax daily 11-04..11-16")
for r in q(f"""SELECT segments.date, campaign.id, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions
    FROM campaign WHERE segments.date BETWEEN '2026-11-04' AND '2026-11-16' AND campaign.id IN ({BR},{NB},{PM}) ORDER BY segments.date"""):
    m = r["metrics"]
    print(f"  {r['segments']['date']} {NAMES[r['campaign']['id']]:<10} ${M(m.get('cost_micros')):7.2f} clk {m.get('clicks',0):>4} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f}")

print("\n===== D. NB ad groups POST (real leads by action)")
ag = {}
for r in q(f"""SELECT ad_group.id, ad_group.name, ad_group.status, metrics.impressions, metrics.clicks, metrics.cost_micros
    FROM ad_group WHERE {POST[0]} AND campaign.id = {NB}"""):
    a, m = r["ad_group"], r["metrics"]; ag[a["id"]] = [a["name"], a["status"], int(m.get("impressions",0)), int(m.get("clicks",0)), M(m.get("cost_micros")), 0.0]
for r in q(f"""SELECT ad_group.id, segments.conversion_action_name, metrics.all_conversions FROM ad_group
    WHERE {POST[0]} AND campaign.id = {NB} AND metrics.all_conversions > 0"""):
    if r["segments"]["conversion_action_name"] in REAL and r["ad_group"]["id"] in ag: ag[r["ad_group"]["id"]][5] += F(r["metrics"].get("all_conversions"))
for v in sorted(ag.values(), key=lambda x: -x[4]):
    print(f"  {v[0]:<28} {v[1]:<7} impr {v[2]:>5} clk {v[3]:>4} ${v[4]:8.2f} real {v[5]:.1f} CPL ${v[4]/v[5] if v[5] else 0:,.0f}")

print("\n===== E. PMax network split POST vs PRE (POST should be ~0)")
for label, (win, _) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.all_conversions FROM campaign
        WHERE campaign.id = {PM} AND {win}"""):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>4} all-conv {F(m.get('all_conversions')):.1f}")

print("\n===== F. call_view 11-10..11-16 (Branded / NB / PMax)")
for r in q(f"""SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-11-10 00:00:00' AND '2026-11-16 23:59:59' AND campaign.id IN ({BR},{NB},{PM})"""):
    c = r["call_view"]; print(f"  {NAMES[r['campaign']['id']]:<10} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== G. NB search terms POST, top 40 by cost")
rows = q(f"""SELECT search_term_view.search_term, ad_group.name, metrics.cost_micros, metrics.clicks, metrics.all_conversions
    FROM search_term_view WHERE {POST[0]} AND campaign.id = {NB} AND metrics.cost_micros > 0""")
rows.sort(key=lambda r: -int(r["metrics"].get("cost_micros", 0)))
tot = sum(M(r["metrics"].get("cost_micros")) for r in rows); print(f"  visible term spend ${tot:,.2f}")
for r in rows[:40]:
    m = r["metrics"]; print(f"  ${M(m.get('cost_micros')):7.2f} clk {m.get('clicks',0):>3} all {F(m.get('all_conversions')):.1f}  {r['search_term_view']['search_term']}  [{r['ad_group']['name']}]")

print("\n===== H. NB RSAs POST")
for r in q(f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, metrics.impressions, metrics.clicks, metrics.ctr, metrics.all_conversions
    FROM ad_group_ad WHERE {POST[0]} AND campaign.id = {NB} AND metrics.impressions > 0"""):
    m = r["metrics"]; a = r["ad_group_ad"]
    print(f"  {r['ad_group']['name']:<28} {a['ad']['id']} {a['status']:<7} {a.get('ad_strength')} impr {m.get('impressions')} CTR {F(m.get('ctr'))*100:.1f}% all {F(m.get('all_conversions')):.1f}")

print("\n===== I. change_event since 11-10")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
    change_event.changed_fields, campaign.name FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-10 00:00:00' AND '2026-11-17 23:59:59'
    ORDER BY change_event.change_date_time LIMIT 200"""):
    c = r["change_event"]; print(f"  {c['change_date_time']} {c.get('user_email')} {c.get('change_resource_type')} {c.get('resource_change_operation')} {r.get('campaign',{}).get('name','')} {c.get('changed_fields','')}")

print("\n===== J. Branded search terms POST, top 25 by cost + abs-top")
rows = q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.all_conversions
    FROM search_term_view WHERE {POST[0]} AND campaign.id = {BR} AND metrics.cost_micros > 0""")
rows.sort(key=lambda r: -int(r["metrics"].get("cost_micros", 0)))
for r in rows[:25]:
    m = r["metrics"]; print(f"  ${M(m.get('cost_micros')):7.2f} clk {m.get('clicks',0):>3} all {F(m.get('all_conversions')):.1f}  {r['search_term_view']['search_term']}")
for label, (win, _) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT metrics.search_absolute_top_impression_share, metrics.search_top_impression_share, metrics.average_cpc
        FROM campaign WHERE {win} AND campaign.id = {BR}"""):
        m = r["metrics"]; print(f"  {label} Branded abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f}% top {F(m.get('search_top_impression_share'))*100:.0f}% avgCPC ${M(m.get('average_cpc')):.2f}")

print("\n===== K. NB terms POST matching the 11-10 negatives / job seekers")
NEG = ("rocky", "catale", "arnold", "magnum", "oklahoma generator", "generator supercenter", "job", "apprentice", "hiring", "career", "salary")
for r in q(f"""SELECT search_term_view.search_term, campaign.id, metrics.cost_micros, metrics.clicks FROM search_term_view
    WHERE {POST[0]} AND campaign.id IN ({BR},{NB}) AND metrics.impressions > 0"""):
    t = r["search_term_view"]["search_term"]
    if any(n in t for n in NEG): print(f"  {NAMES[r['campaign']['id']]} {t} ${M(r['metrics'].get('cost_micros')):.2f} clk {r['metrics'].get('clicks',0)}")
