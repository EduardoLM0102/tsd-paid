import sys
sys.path.insert(0, ".")
from lib import run_query, micros_to_currency

CID = "8634274092"
D = "segments.date BETWEEN '2026-04-15' AND '2026-07-13'"

def pct(v):
    try:
        return f"{float(v)*100:.1f}%"
    except (TypeError, ValueError):
        return "  n/a"

print("=" * 130)
print("ACCOUNT TOTALS — last 90 days (2026-04-15 .. 2026-07-13)")
print("=" * 130)
for r in run_query(CID, f"""
    SELECT metrics.cost_micros, metrics.impressions, metrics.clicks,
           metrics.ctr, metrics.average_cpc, metrics.conversions,
           metrics.conversions_value, metrics.all_conversions
    FROM customer WHERE {D}
"""):
    m = r["metrics"]
    cost = micros_to_currency(m.get("cost_micros"))
    conv = float(m.get("conversions") or 0)
    clicks = float(m.get("clicks") or 0)
    print(f"  spend        : ${cost:,.2f}")
    print(f"  impressions  : {int(m.get('impressions') or 0):,}")
    print(f"  clicks       : {int(clicks):,}   CTR {pct(m.get('ctr'))}   avgCPC ${micros_to_currency(m.get('average_cpc')):.2f}")
    print(f"  conversions  : {conv:.1f}  (COUNTED — inflated ~32% by call dedup issue)")
    print(f"  conv value   : ${float(m.get('conversions_value') or 0):,.2f}")
    print(f"  CPA          : ${cost/conv if conv else 0:,.2f}   (true CPA ~${cost/(conv/1.32) if conv else 0:,.2f} after dedup)")
    print(f"  conv rate    : {conv/clicks*100 if clicks else 0:.1f}%")

print("\n" + "=" * 130)
print("CAMPAIGNS — 90 days (ALL statuses, so we see what's live vs paused)")
print("=" * 130)
hdr = f"{'CAMPAIGN':<42} {'STATUS':<8} {'TYPE':<12} {'spend':>9} {'impr':>8} {'clicks':>7} {'CTR':>6} {'CPC':>7} {'conv':>6} {'CPA':>8}"
print(hdr)
print("-" * 130)
rows = run_query(CID, f"""
    SELECT campaign.id, campaign.name, campaign.status,
           campaign.advertising_channel_type, campaign.bidding_strategy_type,
           metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.ctr,
           metrics.average_cpc, metrics.conversions, metrics.conversions_value
    FROM campaign WHERE {D} AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
""")
live = []
for r in rows:
    c, m = r["campaign"], r["metrics"]
    cost = micros_to_currency(m.get("cost_micros"))
    conv = float(m.get("conversions") or 0)
    if c.get("status") == "ENABLED":
        live.append((c.get("id"), c.get("name"), c.get("bidding_strategy_type"), c.get("advertising_channel_type")))
    print(f"{str(c.get('name'))[:41]:<42} {str(c.get('status'))[:7]:<8} "
          f"{str(c.get('advertising_channel_type'))[:11]:<12} "
          f"${cost:>8,.0f} {int(m.get('impressions') or 0):>8,} {int(m.get('clicks') or 0):>7,} "
          f"{pct(m.get('ctr')):>6} ${micros_to_currency(m.get('average_cpc')):>6.2f} "
          f"{conv:>6.1f} ${cost/conv if conv else 0:>7,.0f}")

print("\n  LIVE (ENABLED) campaigns + bidding strategy:")
for cid_, name, bid, ch in live:
    print(f"    - [{ch}] {name} (id {cid_})  bidding={bid}")

print("\n" + "=" * 130)
print("IMPRESSION SHARE / COMPETITION — 90 days, ENABLED campaigns")
print("=" * 130)
print(f"{'CAMPAIGN':<40} {'SearchIS':>9} {'LostBudget':>11} {'LostRank':>9} {'AbsTopIS':>9} {'TopIS':>8} {'AbsTop%':>8}")
print("-" * 130)
for r in run_query(CID, f"""
    SELECT campaign.name, campaign.status,
           metrics.search_impression_share,
           metrics.search_budget_lost_impression_share,
           metrics.search_rank_lost_impression_share,
           metrics.search_absolute_top_impression_share,
           metrics.search_top_impression_share,
           metrics.absolute_top_impression_percentage
    FROM campaign WHERE {D} AND campaign.status = 'ENABLED' AND metrics.impressions > 0
"""):
    c, m = r["campaign"], r["metrics"]
    print(f"{str(c.get('name'))[:39]:<40} "
          f"{pct(m.get('search_impression_share')):>9} "
          f"{pct(m.get('search_budget_lost_impression_share')):>11} "
          f"{pct(m.get('search_rank_lost_impression_share')):>9} "
          f"{pct(m.get('search_absolute_top_impression_share')):>9} "
          f"{pct(m.get('search_top_impression_share')):>8} "
          f"{pct(m.get('absolute_top_impression_percentage')):>8}")
