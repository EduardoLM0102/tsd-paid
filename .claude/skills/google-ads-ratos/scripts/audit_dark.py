import sys
sys.path.insert(0, ".")
from lib import run_query, micros_to_currency

CID = "8634274092"

print("=" * 96)
print("DAILY SPEND — when did the account go dark?  (last 90d, only days with spend)")
print("=" * 96)
rows = run_query(CID, """
    SELECT segments.date, metrics.cost_micros, metrics.impressions,
           metrics.clicks, metrics.conversions
    FROM customer
    WHERE segments.date BETWEEN '2026-04-15' AND '2026-07-13'
    ORDER BY segments.date DESC
""")
active = [r for r in rows if float(r["metrics"].get("cost_micros") or 0) > 0]
print(f"  days with spend: {len(active)} of {len(rows)} days in range")
if active:
    print(f"\n  MOST RECENT 20 DAYS WITH SPEND:")
    print(f"  {'date':<12} {'spend':>9} {'impr':>8} {'clicks':>7} {'conv':>6}")
    for r in active[:20]:
        s, m = r["segments"], r["metrics"]
        print(f"  {s['date']:<12} ${micros_to_currency(m.get('cost_micros')):>8,.2f} "
              f"{int(m.get('impressions') or 0):>8,} {int(m.get('clicks') or 0):>7,} "
              f"{float(m.get('conversions') or 0):>6.1f}")
    last = active[0]["segments"]["date"]
    first = active[-1]["segments"]["date"]
    print(f"\n  >>> LAST DAY WITH ANY SPEND: {last}")
    print(f"  >>> (range started {first})")

print("\n" + "=" * 96)
print("ALL CAMPAIGNS — status, id, budget, bidding (regardless of impressions)")
print("=" * 96)
for r in run_query(CID, """
    SELECT campaign.id, campaign.name, campaign.status,
           campaign.advertising_channel_type,
           campaign.bidding_strategy_type,
           campaign.start_date, campaign.end_date,
           campaign_budget.amount_micros,
           campaign_budget.status
    FROM campaign
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.name
"""):
    c = r["campaign"]
    b = r.get("campaign_budget", {}) or {}
    print(f"  [{c.get('status'):<8}] {str(c.get('name'))[:44]:<45} id={c.get('id')}")
    print(f"             type={c.get('advertising_channel_type')}  bid={c.get('bidding_strategy_type')}  "
          f"budget=${micros_to_currency(b.get('amount_micros')):,.2f}/day  "
          f"start={c.get('start_date')} end={c.get('end_date')}")
