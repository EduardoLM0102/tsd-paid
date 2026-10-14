import sys
sys.path.insert(0, ".")
from lib import run_query, micros_to_currency

CID = "8634274092"
START = "2025-01-01"
END = "2026-07-13"

print("=" * 110)
print(f"WHEN DID EACH CONVERSION ACTION START FIRING?  (monthly, {START} .. {END})")
print("=" * 110)
first_seen = {}
by_action_month = {}
for r in run_query(CID, f"""
    SELECT segments.month, segments.conversion_action_name,
           metrics.conversions, metrics.all_conversions
    FROM customer
    WHERE segments.date BETWEEN '{START}' AND '{END}'
"""):
    s = r["segments"]; m = r["metrics"]
    name = s.get("conversion_action_name")
    mo = s.get("month")
    cv = float(m.get("conversions") or 0)
    av = float(m.get("all_conversions") or 0)
    if av > 0 or cv > 0:
        if name not in first_seen or mo < first_seen[name]:
            first_seen[name] = mo
    by_action_month.setdefault(name, {})[mo] = (cv, av)

for name, mo in sorted(first_seen.items(), key=lambda x: x[1]):
    tot_c = sum(v[0] for v in by_action_month[name].values())
    tot_a = sum(v[1] for v in by_action_month[name].values())
    months = len(by_action_month[name])
    print(f"  first fired {mo}   {str(name)[:52]:<54} months_active={months:>2}  "
          f"counted={tot_c:>7.1f}  all={tot_a:>7.1f}")

print("\n" + "=" * 110)
print("MONTHLY ACCOUNT HISTORY — spend, counted conversions, CPA")
print("=" * 110)
print(f"{'month':<10} {'spend':>11} {'clicks':>8} {'COUNTED conv':>13} {'CPA':>9} {'convValue':>11}")
print("-" * 110)
mo_agg = {}
for r in run_query(CID, f"""
    SELECT segments.month, metrics.cost_micros, metrics.clicks,
           metrics.conversions, metrics.conversions_value
    FROM customer
    WHERE segments.date BETWEEN '{START}' AND '{END}'
"""):
    mo = r["segments"]["month"]; m = r["metrics"]
    d = mo_agg.setdefault(mo, {"c": 0.0, "k": 0, "v": 0.0, "val": 0.0})
    d["c"] += micros_to_currency(m.get("cost_micros"))
    d["k"] += int(m.get("clicks") or 0)
    d["v"] += float(m.get("conversions") or 0)
    d["val"] += float(m.get("conversions_value") or 0)

tot_spend = tot_conv = 0.0
for mo, d in sorted(mo_agg.items()):
    if d["c"] == 0 and d["v"] == 0:
        continue
    tot_spend += d["c"]; tot_conv += d["v"]
    cpa = d["c"] / d["v"] if d["v"] else 0
    print(f"{mo:<10} ${d['c']:>10,.0f} {d['k']:>8,} {d['v']:>13.1f} ${cpa:>8,.0f} ${d['val']:>10,.0f}")
print("-" * 110)
print(f"{'TOTAL':<10} ${tot_spend:>10,.0f} {'':>8} {tot_conv:>13.1f}")

print("\n" + "=" * 110)
print("BIDDING STRATEGY per campaign (any status) + first/last spend date")
print("=" * 110)
for r in run_query(CID, """
    SELECT campaign.id, campaign.name, campaign.status,
           campaign.advertising_channel_type,
           campaign.bidding_strategy_type,
           campaign.maximize_conversions.target_cpa_micros,
           campaign.target_cpa.target_cpa_micros
    FROM campaign
    WHERE campaign.status != 'REMOVED'
"""):
    c = r["campaign"]
    mc = (c.get("maximize_conversions") or {}).get("target_cpa_micros")
    tc = (c.get("target_cpa") or {}).get("target_cpa_micros")
    t = mc or tc
    tstr = f"  tCPA=${micros_to_currency(t):,.0f}" if t else ""
    print(f"  [{str(c.get('status')):<8}] {str(c.get('name'))[:42]:<44} "
          f"{str(c.get('advertising_channel_type'))[:11]:<12} "
          f"BID={c.get('bidding_strategy_type')}{tstr}")

print("\n" + "=" * 110)
print("FIRST + LAST SPEND DATE per campaign (how long each has been learning)")
print("=" * 110)
camp_dates = {}
for r in run_query(CID, f"""
    SELECT campaign.name, segments.date, metrics.cost_micros
    FROM campaign
    WHERE segments.date BETWEEN '{START}' AND '{END}' AND metrics.cost_micros > 0
"""):
    n = r["campaign"]["name"]; d = r["segments"]["date"]
    c = micros_to_currency(r["metrics"].get("cost_micros"))
    e = camp_dates.setdefault(n, {"first": d, "last": d, "spend": 0.0, "days": 0})
    e["first"] = min(e["first"], d)
    e["last"] = max(e["last"], d)
    e["spend"] += c
    e["days"] += 1
for n, e in sorted(camp_dates.items(), key=lambda x: -x[1]["spend"]):
    print(f"  {str(n)[:44]:<46} {e['first']} -> {e['last']}  "
          f"days={e['days']:>3}  spend=${e['spend']:>9,.0f}")
