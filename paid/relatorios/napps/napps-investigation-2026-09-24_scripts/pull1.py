from h import *
q = """
SELECT segments.month, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM customer
WHERE segments.date BETWEEN '2024-01-01' AND '2026-09-23'
ORDER BY segments.month
"""
rows = list(run_query(CID, q))
json.dump(rows, open(OUT+"acct_monthly.json","w"), default=str)
print("month      cost     clk    imp   conv allconv  IS  lostBudget lostRank")
for r in rows:
    m=r["metrics"]
    print(r["segments"]["month"], f"{f(m.get('cost_micros'))/1e6:9.2f} {f(m.get('clicks')):6.0f} {f(m.get('impressions')):7.0f} {f(m.get('conversions')):6.1f} {f(m.get('all_conversions')):6.1f}  IS={m.get('search_impression_share')} B={m.get('search_budget_lost_impression_share')} R={m.get('search_rank_lost_impression_share')}")
