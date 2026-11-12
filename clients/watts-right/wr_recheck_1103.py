# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-11-03 recheck (Command Center fu-097) of the 10-27 Nonbranded changes: tCPA $80 -> $95 + 7 phrase
negatives. POST = 10-28 -> 11-02 (6d, first full days on $95), PRE = 10-20 -> 10-26 (7d on $80). Also EV + Panel RSA A/B since 10-20
and a short PMax network split (fu-098 is the full PMax read)."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PM = "23690645223", "23832838033", "23833205176"
NAMES = {BR: "Branded", NB: "Nonbranded", PM: "PMax"}
POST = ("segments.date BETWEEN '2026-10-28' AND '2026-11-02'", 6)
PRE = ("segments.date BETWEEN '2026-10-20' AND '2026-10-26'", 7)
REAL = {"Calls from ads", "Phone Call", "Submit lead form - web", "Form Submission [Landing Page]"}  # same basis as the 10-27 log: ad calls + CallRail upload + forms, no taps/ghl_*
NEGS = ["genesis 1 3", "aa electric", "tesla tulsa", "xeal", "j1772", "nissan leaf", "cost to charge"]
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
IDS = f"campaign.id IN ({BR},{NB},{PM})"

for label, (win, days) in (("POST 10-28..11-02", POST), ("PRE 10-20..10-26", PRE)):
    print(f"===== A. campaigns {label}")
    for r in q(f"""SELECT campaign.id, campaign.status, campaign.primary_status, campaign.bidding_strategy_type,
        campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.impressions,
        metrics.conversions, metrics.search_impression_share, metrics.search_absolute_top_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE {win} AND {IDS}"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); cv = F(m.get("conversions"))
        print(f"{NAMES[c['id']]:<11} {c['status']}/{c.get('primary_status')} {c.get('bidding_strategy_type')} "
              f"tCPA={M(c.get('maximize_conversions',{}).get('target_cpa_micros'))} budget ${M(r['campaign_budget'].get('amount_micros')):.0f}/d | "
              f"${sp:,.2f} ({sp/days:.0f}/d) clk {cl} ({cl/days:.1f}/d) impr {int(m.get('impressions',0))/days:.0f}/d conv {cv:.1f} "
              f"CPC ${sp/cl if cl else 0:.2f} | IS {F(m.get('search_impression_share'))*100:.1f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.1f} "
              f"budget-lost {F(m.get('search_budget_lost_impression_share'))*100:.1f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.1f}")

    print(f"\n===== B. conversions by action {label}")
    real = collections.defaultdict(float); spend = {}
    for r in q(f"SELECT campaign.id, metrics.cost_micros FROM campaign WHERE {win} AND {IDS}"):
        spend[r["campaign"]["id"]] = M(r["metrics"].get("cost_micros"))
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND {IDS} AND metrics.all_conversions > 0"""):
        n = r["segments"]["conversion_action_name"]; cv = F(r["metrics"].get("conversions")); al = F(r["metrics"].get("all_conversions"))
        if n in REAL: real[r["campaign"]["id"]] += al
        print(f"  {NAMES[r['campaign']['id']]:<11} {n:<40} conv {cv:.1f} all {al:.1f}")
    for k, v in real.items():
        print(f"  REAL {NAMES[k]:<11} {v:.1f} leads (all_conversions, no taps/views) -> CPL ${spend.get(k,0)/v if v else 0:,.2f}")
    print()

print("===== C. Nonbranded daily 10-20..11-02")
for r in q(f"""SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.search_impression_share,
    metrics.search_rank_lost_impression_share FROM campaign WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-02' AND campaign.id = {NB}
    ORDER BY segments.date"""):
    m = r["metrics"]
    print(f"  {r['segments']['date']} ${M(m.get('cost_micros')):6.2f} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>4} conv {F(m.get('conversions')):.1f} "
          f"IS {F(m.get('search_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")

print("\n===== D. Nonbranded ad groups PRE vs POST")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT ad_group.name, ad_group.status, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions,
        metrics.cost_micros, metrics.search_rank_lost_impression_share FROM ad_group WHERE {win} AND campaign.id = {NB}"""):
        m = r["metrics"]
        print(f"  {label} {r['ad_group']['name']:<28} {r['ad_group']['status']:<8} impr/d {int(m.get('impressions',0))/days:5.1f} clk {m.get('clicks',0):>3} "
              f"conv {F(m.get('conversions')):.1f} ${M(m.get('cost_micros')):7.2f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")

print("\n===== E. Nonbranded real leads by ad group + action POST")
for r in q(f"""SELECT ad_group.name, segments.conversion_action_name, metrics.all_conversions FROM ad_group
    WHERE {POST[0]} AND campaign.id = {NB} AND metrics.all_conversions > 0"""):
    print(f"  {r['ad_group']['name']:<28} {r['segments']['conversion_action_name']:<40} {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== F. Nonbranded search terms POST (by cost)")
leak = []
for r in q(f"""SELECT search_term_view.search_term, ad_group.name, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {NB} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 50"""):
    t = r["search_term_view"]["search_term"]; m = r["metrics"]
    if any(n in t for n in NEGS): leak.append(t)
    print(f"  {t:<45} {r['ad_group']['name'][:18]:<18} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")
print("  terms still matching the 10-27 negatives:", leak or "none")

print("\n===== G. Nonbranded call_view POST (ad call button)")
for r in q(f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-10-28 00:00:00' AND '2026-11-02 23:59:59' AND campaign.id = {NB}"""):
    c = r["call_view"]; print(f"  {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== H. Nonbranded RSAs since 10-20 (A/B)")
for r in q(f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls, metrics.impressions, metrics.clicks, metrics.ctr,
    metrics.conversions, metrics.all_conversions, metrics.cost_micros FROM ad_group_ad
    WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-02' AND campaign.id = {NB} AND metrics.impressions > 0"""):
    a, m = r["ad_group_ad"], r["metrics"]
    print(f"  {r['ad_group']['name'][:22]:<22} ad {a['ad']['id']} {a['status']:<7} impr {m.get('impressions',0):>5} clk {m.get('clicks',0):>3} "
          f"CTR {F(m.get('ctr'))*100:.1f}% conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} ${M(m.get('cost_micros')):.2f}")

print("\n===== I. PMax network split POST vs PRE (full read = fu-098)")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE {win} AND campaign.id = {PM}"""):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>5} "
                                f"conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f}")

print("\n===== J. changes since 10-27")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
    change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-27' AND '2026-11-04'
    ORDER BY change_event.change_date_time LIMIT 200"""):
    e = r["change_event"]; print(" ", e["change_date_time"], e.get("user_email"), e["change_resource_type"], e["resource_change_operation"], e.get("changed_fields"), e.get("campaign"))
