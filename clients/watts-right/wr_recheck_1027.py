# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-10-27 recheck (Command Center fu-072) of the 10-20 changes: Nonbranded tCPA $80 spend + real CPL,
Branded $35 all hours (IS, nights/weekends), Emergency on one ad, PMax tap/network jump. POST = 10-20 -> 10-26 (7d), PRE = 10-09 -> 10-19 (11d)."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PM = "23690645223", "23832838033", "23833205176"
NAMES = {BR: "Branded", NB: "Nonbranded", PM: "PMax"}
POST = ("segments.date BETWEEN '2026-10-20' AND '2026-10-26'", 7)
PRE = ("segments.date BETWEEN '2026-10-09' AND '2026-10-19'", 11)
REAL = {"Calls from ads", "Website calls", "Contact Form", "Form Submit", "Book Now", "Phone Call", "First Time Caller", "Repeat Caller"}
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
IDS = f"campaign.id IN ({BR},{NB},{PM})"

for label, (win, days) in (("POST 10-20..10-26", POST), ("PRE 10-09..10-19", PRE)):
    print(f"===== A. campaigns {label}")
    for r in q(f"""SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
        campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.search_impression_share,
        metrics.search_absolute_top_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE {win} AND {IDS}"""):
        c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); cv = F(m.get("conversions"))
        print(f"{NAMES[c['id']]:<11} {c['status']} {c.get('bidding_strategy_type')} tCPA={M(c.get('maximize_conversions',{}).get('target_cpa_micros'))} "
              f"budget ${M(r['campaign_budget'].get('amount_micros')):.0f}/d | ${sp:,.2f} ({sp/days:.0f}/d) clk {cl} ({cl/days:.0f}/d) conv {cv:.1f} "
              f"CPL ${sp/cv if cv else 0:,.2f} CPC ${sp/cl if cl else 0:.2f} | IS {F(m.get('search_impression_share'))*100:.1f} "
              f"abs-top {F(m.get('search_absolute_top_impression_share'))*100:.1f} budget-lost {F(m.get('search_budget_lost_impression_share'))*100:.1f} "
              f"rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.1f}")

    print(f"\n===== B. conversions by action {label}")
    real = collections.defaultdict(float)
    for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE {win} AND {IDS} AND metrics.all_conversions > 0"""):
        n = r["segments"]["conversion_action_name"]; cv = F(r["metrics"].get("conversions"))
        if n in REAL: real[r["campaign"]["id"]] += cv
        print(f"  {NAMES[r['campaign']['id']]:<11} {n:<40} conv {cv:.1f} all {F(r['metrics'].get('all_conversions')):.1f}")
    print("  REAL (primary col, no taps/views):", {NAMES[k]: round(v, 1) for k, v in real.items()})
    print()

print("===== C. daily by campaign POST + 3 days before")
rows = collections.defaultdict(dict)
for r in q(f"""SELECT campaign.id, segments.date, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.search_impression_share
    FROM campaign WHERE segments.date BETWEEN '2026-10-17' AND '2026-10-26' AND {IDS}"""):
    m = r["metrics"]; rows[r["segments"]["date"]][NAMES[r["campaign"]["id"]]] = (M(m.get("cost_micros")), int(m.get("clicks", 0)), F(m.get("conversions")), F(m.get("search_impression_share")))
for d in sorted(rows):
    print(" ", d, " | ".join(f"{n[:4]} ${v[0]:.0f} clk {v[1]} cv {v[2]:.1f} IS {v[3]*100:.0f}" for n, v in sorted(rows[d].items())))

print("\n===== D. PMax network split PRE vs POST (conv = primary, by action)")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
        FROM campaign WHERE {win} AND campaign.id = {PM}"""):
        m = r["metrics"]; print(f"  {label} {r['segments']['ad_network_type']:<16} ${M(m.get('cost_micros')):8.2f} clk {m.get('clicks',0):>5} impr {m.get('impressions',0):>7} conv {F(m.get('conversions')):.1f}")
    for r in q(f"""SELECT segments.ad_network_type, segments.conversion_action_name, metrics.conversions FROM campaign
        WHERE {win} AND campaign.id = {PM} AND metrics.conversions > 0"""):
        print(f"     {label} {r['segments']['ad_network_type']:<16} {r['segments']['conversion_action_name']:<30} {F(r['metrics'].get('conversions')):.1f}")

print("\n===== E. Branded clicks by day-of-week x old-schedule window (old = Mon-Fri 06-22)")
old = collections.Counter(); new = collections.Counter()
for r in q(f"""SELECT segments.day_of_week, segments.hour, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
    FROM campaign WHERE {POST[0]} AND campaign.id = {BR}"""):
    s, m = r["segments"], r["metrics"]; h = int(s["hour"]); inside = s["day_of_week"] not in ("SATURDAY", "SUNDAY") and 6 <= h < 22
    b = old if inside else new
    b["clk"] += int(m.get("clicks", 0)); b["impr"] += int(m.get("impressions", 0)); b["conv"] += F(m.get("conversions")); b["cost"] += M(m.get("cost_micros"))
print("  inside old schedule :", dict(old)); print("  NEW hours (nights/wknd):", dict(new))

print("\n===== F. Nonbranded ad groups PRE vs POST (impr/day)")
for label, (win, days) in (("POST", POST), ("PRE", PRE)):
    for r in q(f"""SELECT ad_group.name, metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros FROM ad_group
        WHERE {win} AND campaign.id = {NB}"""):
        m = r["metrics"]; print(f"  {label} {r['ad_group']['name']:<28} impr/d {int(m.get('impressions',0))/days:.1f} clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f} ${M(m.get('cost_micros')):.2f}")

print("\n===== G. Nonbranded search terms POST (by cost)")
for r in q(f"""SELECT search_term_view.search_term, ad_group.name, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE {POST[0]} AND campaign.id = {NB} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 40"""):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term']:<45} {r['ad_group']['name'][:18]:<18} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} conv {F(m.get('conversions')):.1f}")

print("\n===== H. changes since 10-20")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
    change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-20' AND '2026-10-28'
    ORDER BY change_event.change_date_time LIMIT 200"""):
    e = r["change_event"]; print(" ", e["change_date_time"], e.get("user_email"), e["change_resource_type"], e["resource_change_operation"], e.get("changed_fields"), e.get("campaign"))
