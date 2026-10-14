import sys
sys.path.insert(0, ".")
from lib import run_query, micros_to_currency

CID = "8634274092"
D = "segments.date BETWEEN '2026-04-15' AND '2026-07-07'"   # live period only

def pct(v):
    try:
        return f"{float(v)*100:.1f}%"
    except (TypeError, ValueError):
        return "n/a"

print("=" * 132)
print("IMPRESSION SHARE — live period 2026-04-15 .. 2026-07-07 (all campaigns with impressions)")
print("=" * 132)
print(f"{'CAMPAIGN':<40} {'TYPE':<11} {'SearchIS':>9} {'LostBudget':>11} {'LostRank':>9} {'AbsTopIS':>9} {'TopIS':>7} {'AbsTop%':>8} {'Top%':>7}")
print("-" * 132)
for r in run_query(CID, f"""
    SELECT campaign.name, campaign.advertising_channel_type,
           metrics.search_impression_share,
           metrics.search_budget_lost_impression_share,
           metrics.search_rank_lost_impression_share,
           metrics.search_absolute_top_impression_share,
           metrics.search_top_impression_share,
           metrics.absolute_top_impression_percentage,
           metrics.top_impression_percentage,
           metrics.impressions
    FROM campaign WHERE {D} AND metrics.impressions > 0
    ORDER BY metrics.impressions DESC
"""):
    c, m = r["campaign"], r["metrics"]
    print(f"{str(c.get('name'))[:39]:<40} {str(c.get('advertising_channel_type'))[:10]:<11} "
          f"{pct(m.get('search_impression_share')):>9} "
          f"{pct(m.get('search_budget_lost_impression_share')):>11} "
          f"{pct(m.get('search_rank_lost_impression_share')):>9} "
          f"{pct(m.get('search_absolute_top_impression_share')):>9} "
          f"{pct(m.get('search_top_impression_share')):>7} "
          f"{pct(m.get('absolute_top_impression_percentage')):>8} "
          f"{pct(m.get('top_impression_percentage')):>7}")

print("\n" + "=" * 132)
print("CPC PRESSURE OVER TIME (monthly) — proxy for competitive heat")
print("=" * 132)
print(f"{'month':<10} {'spend':>10} {'impr':>9} {'clicks':>8} {'CTR':>7} {'avgCPC':>8} {'conv':>7} {'CPA':>9} {'convRate':>9}")
print("-" * 132)
agg = {}
for r in run_query(CID, f"""
    SELECT segments.month, metrics.cost_micros, metrics.impressions,
           metrics.clicks, metrics.conversions
    FROM customer WHERE {D}
"""):
    mo = r["segments"]["month"]
    m = r["metrics"]
    d = agg.setdefault(mo, {"c": 0.0, "i": 0, "k": 0, "v": 0.0})
    d["c"] += micros_to_currency(m.get("cost_micros"))
    d["i"] += int(m.get("impressions") or 0)
    d["k"] += int(m.get("clicks") or 0)
    d["v"] += float(m.get("conversions") or 0)
for mo, d in sorted(agg.items()):
    cpc = d["c"] / d["k"] if d["k"] else 0
    ctr = d["k"] / d["i"] * 100 if d["i"] else 0
    cpa = d["c"] / d["v"] if d["v"] else 0
    cr = d["v"] / d["k"] * 100 if d["k"] else 0
    print(f"{mo:<10} ${d['c']:>9,.0f} {d['i']:>9,} {d['k']:>8,} {ctr:>6.1f}% ${cpc:>7.2f} "
          f"{d['v']:>7.1f} ${cpa:>8,.0f} {cr:>8.2f}%")

print("\n" + "=" * 132)
print("DEVICE SPLIT — where the money and the leads are")
print("=" * 132)
print(f"{'device':<12} {'spend':>10} {'clicks':>8} {'conv':>7} {'CPA':>9} {'convRate':>9}")
print("-" * 132)
dev = {}
for r in run_query(CID, f"""
    SELECT segments.device, metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM customer WHERE {D}
"""):
    dv = r["segments"]["device"]
    m = r["metrics"]
    d = dev.setdefault(dv, {"c": 0.0, "k": 0, "v": 0.0})
    d["c"] += micros_to_currency(m.get("cost_micros"))
    d["k"] += int(m.get("clicks") or 0)
    d["v"] += float(m.get("conversions") or 0)
for dv, d in sorted(dev.items(), key=lambda x: -x[1]["c"]):
    cpa = d["c"] / d["v"] if d["v"] else 0
    cr = d["v"] / d["k"] * 100 if d["k"] else 0
    print(f"{dv:<12} ${d['c']:>9,.0f} {d['k']:>8,} {d['v']:>7.1f} ${cpa:>8,.0f} {cr:>8.2f}%")
