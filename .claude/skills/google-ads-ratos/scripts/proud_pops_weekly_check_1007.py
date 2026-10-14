import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import defaultdict

CID = "1051843378"
WINDOWS = {
    "prev7 (Sep 23-29)": ("2026-09-23", "2026-09-29"),
    "last7 (Sep 30-Oct 6)": ("2026-09-30", "2026-10-06"),
    "Sep full": ("2026-09-01", "2026-09-30"),
    "Oct 1-6": ("2026-10-01", "2026-10-06"),
}

def f(x):
    try:
        return float(x or 0)
    except Exception:
        return 0.0

print("=== GATE 0: TSD - Website Call status ===")
for r in run_query(CID, """
SELECT conversion_action.name, conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.category, conversion_action.origin, conversion_action.type
FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    ca = r["conversion_action"]
    print(f"  {ca['name']:45s} {str(ca.get('category')):20s} {str(ca.get('origin')):15s} primary={ca.get('primary_for_goal')}")

print("\n=== campaign_conversion_goal (biddable) ===")
goals = defaultdict(list)
for r in run_query(CID, """
SELECT campaign.name, campaign.status, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
FROM campaign_conversion_goal WHERE campaign.status = 'ENABLED'"""):
    c = r["campaign"]["name"]; g = r["campaign_conversion_goal"]
    if g.get("biddable"):
        goals[c].append(f"{g['category']}/{g['origin']}")
for c, gs in goals.items():
    print(f"  {c}: {sorted(gs)}")

for label, (s, u) in WINDOWS.items():
    print(f"\n\n######## {label} ({s} .. {u}) ########")
    camp = {}
    for r in run_query(CID, f"""
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign WHERE segments.date BETWEEN '{s}' AND '{u}' AND metrics.cost_micros > 0"""):
        c = r["campaign"]; m = r["metrics"]
        camp[c["name"]] = dict(id=c["id"], status=c["status"], ch=c["advertising_channel_type"],
            budget=f(r.get("campaign_budget", {}).get("amount_micros"))/1e6,
            cost=f(m.get("cost_micros"))/1e6, clicks=f(m.get("clicks")), impr=f(m.get("impressions")),
            conv=f(m.get("conversions")), allc=f(m.get("all_conversions")),
            is_=m.get("search_impression_share"), bl=m.get("search_budget_lost_impression_share"),
            rl=m.get("search_rank_lost_impression_share"))
    # conv by action per campaign
    act = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    for r in run_query(CID, f"""
SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '{s}' AND '{u}'"""):
        a = r.get("segments", {}).get("conversion_action_name")
        if not a: continue
        m = r["metrics"]
        act[r["campaign"]["name"]][a][0] += f(m.get("conversions"))
        act[r["campaign"]["name"]][a][1] += f(m.get("all_conversions"))
    tot = defaultdict(float)
    for name, d in sorted(camp.items(), key=lambda x: -x[1]["cost"]):
        forms = act[name].get("Website lead", [0, 0])[1]
        calls = act[name].get("Calls from ads", [0, 0])[1]
        wcall = act[name].get("TSD - Website Call", [0, 0])[1]
        cpf = d["cost"]/forms if forms else 0
        isx = lambda v: f"{f(v)*100:.1f}" if v is not None else "-"
        print(f"{name[:52]:52s} {str(d['ch']):16s} {str(d['status']):8s} bud${d['budget']:.0f} cost${d['cost']:,.0f} clk{d['clicks']:.0f} "
              f"cpc${(d['cost']/d['clicks'] if d['clicks'] else 0):.2f} conv{d['conv']:.1f} forms{forms:.1f} callsAds{calls:.1f} phoneClk{wcall:.1f} $/form{cpf:,.0f} "
              f"IS{isx(d['is_'])} BL{isx(d['bl'])} RL{isx(d['rl'])}")
        for a, (cv, ac) in sorted(act[name].items(), key=lambda x: -x[1][1]):
            if ac > 0 and a not in ("Website lead", "Calls from ads", "TSD - Website Call"):
                print(f"      other: {a} conv={cv:.1f} all={ac:.1f}")
        bucket = "LSA" if d["ch"] == "LOCAL_SERVICES" else ("YT" if d["ch"] == "VIDEO" else ("BRAND" if "Branded" in name and "Nonbranded" not in name else "UNBR"))
        tot[bucket+"_cost"] += d["cost"]; tot[bucket+"_forms"] += forms; tot[bucket+"_conv"] += d["conv"]
        tot[bucket+"_clicks"] += d["clicks"]; tot[bucket+"_wcall"] += wcall; tot[bucket+"_calls"] += calls
    print("  TOTALS:", {k: round(v, 1) for k, v in sorted(tot.items())})
    # account search IS
    for r in run_query(CID, f"""
SELECT metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM customer WHERE segments.date BETWEEN '{s}' AND '{u}'"""):
        print("  ACCOUNT search IS:", r["metrics"])

print("\n\n=== Weekly Website lead (all_conv) by campaign, Aug 31 → Oct 6 ===")
wk = defaultdict(lambda: defaultdict(float))
wkcost = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, """
SELECT campaign.name, segments.week, segments.conversion_action_name, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2026-08-31' AND '2026-10-06'"""):
    if r.get("segments", {}).get("conversion_action_name") == "Website lead":
        wk[r["campaign"]["name"]][r["segments"]["week"]] += f(r["metrics"].get("all_conversions"))
for r in run_query(CID, """
SELECT campaign.name, segments.week, metrics.cost_micros
FROM campaign WHERE segments.date BETWEEN '2026-08-31' AND '2026-10-06' AND metrics.cost_micros > 0"""):
    wkcost[r["campaign"]["name"]][r["segments"]["week"]] += f(r["metrics"].get("cost_micros"))/1e6
weeks = sorted({w for d in wkcost.values() for w in d})
print(" " * 52 + "  ".join(w[5:] for w in weeks))
for name in sorted(wkcost, key=lambda n: -sum(wkcost[n].values())):
    print(f"{name[:52]:52s}" + "  ".join(f"{wk[name].get(w,0):3.0f}/${wkcost[name].get(w,0)/1000:.1f}k" for w in weeks))

print("\n\n=== change_event since 2026-09-23 ===")
for r in run_query(CID, """
SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
       change_event.resource_change_operation, change_event.changed_fields, campaign.name
FROM change_event
WHERE change_event.change_date_time >= '2026-09-23' AND change_event.change_date_time <= '2026-10-07 23:59:59'
ORDER BY change_event.change_date_time DESC LIMIT 200"""):
    ce = r["change_event"]
    print(f"  {ce['change_date_time'][:16]} {ce.get('user_email','?'):32s} {str(ce['change_resource_type']):22s} {str(ce['resource_change_operation']):7s} "
          f"{r.get('campaign',{}).get('name','')[:40]:40s} {str(ce.get('changed_fields',''))[:90]}")
