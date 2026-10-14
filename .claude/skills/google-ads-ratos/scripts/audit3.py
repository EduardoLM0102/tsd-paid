import sys
sys.path.insert(0, ".")
from lib import run_query, micros_to_currency

CID = "8634274092"
D = "segments.date BETWEEN '2026-04-15' AND '2026-07-07'"

print("=" * 128)
print("LANDING PAGES — CRO view (where clicks land, and do they convert)")
print("=" * 128)
print(f"{'URL':<66} {'clicks':>7} {'spend':>9} {'conv':>7} {'convRate':>9} {'CPA':>8}")
print("-" * 128)
try:
    lps = {}
    for r in run_query(CID, f"""
        SELECT landing_page_view.unexpanded_final_url,
               metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM landing_page_view WHERE {D} AND metrics.clicks > 0
    """):
        url = r["landing_page_view"].get("unexpanded_final_url")
        m = r["metrics"]
        d = lps.setdefault(url, {"k": 0, "c": 0.0, "v": 0.0})
        d["k"] += int(m.get("clicks") or 0)
        d["c"] += micros_to_currency(m.get("cost_micros"))
        d["v"] += float(m.get("conversions") or 0)
    for url, d in sorted(lps.items(), key=lambda x: -x[1]["k"])[:15]:
        cr = d["v"] / d["k"] * 100 if d["k"] else 0
        cpa = d["c"] / d["v"] if d["v"] else 0
        print(f"{str(url)[:65]:<66} {d['k']:>7,} ${d['c']:>8,.0f} {d['v']:>7.1f} {cr:>8.2f}% ${cpa:>7,.0f}")
    if not lps:
        print("  (no landing_page_view rows)")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 128)
print("TOP SEARCH TERMS — what we actually paid for (search campaigns)")
print("=" * 128)
print(f"{'SEARCH TERM':<52} {'campaign':<24} {'impr':>7} {'clicks':>7} {'spend':>8} {'conv':>6}")
print("-" * 128)
try:
    rows = run_query(CID, f"""
        SELECT search_term_view.search_term, campaign.name,
               metrics.impressions, metrics.clicks,
               metrics.cost_micros, metrics.conversions
        FROM search_term_view WHERE {D}
        ORDER BY metrics.cost_micros DESC
        LIMIT 30
    """)
    for r in rows:
        t = r["search_term_view"].get("search_term")
        c = r["campaign"].get("name")
        m = r["metrics"]
        print(f"{str(t)[:51]:<52} {str(c)[:23]:<24} "
              f"{int(m.get('impressions') or 0):>7,} {int(m.get('clicks') or 0):>7,} "
              f"${micros_to_currency(m.get('cost_micros')):>7,.0f} {float(m.get('conversions') or 0):>6.1f}")
    if not rows:
        print("  (none)")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 128)
print("PMAX — where the impressions actually served (asset group + channel if available)")
print("=" * 128)
try:
    for r in run_query(CID, f"""
        SELECT asset_group.name, asset_group.status,
               metrics.impressions, metrics.clicks,
               metrics.cost_micros, metrics.conversions
        FROM asset_group WHERE {D}
        ORDER BY metrics.cost_micros DESC
    """):
        a = r["asset_group"]; m = r["metrics"]
        k = int(m.get("clicks") or 0)
        v = float(m.get("conversions") or 0)
        print(f"  {str(a.get('name'))[:40]:<42} [{a.get('status')}] "
              f"impr={int(m.get('impressions') or 0):>8,} clicks={k:>6,} "
              f"spend=${micros_to_currency(m.get('cost_micros')):>7,.0f} conv={v:>5.1f} "
              f"CR={v/k*100 if k else 0:>5.2f}%")
except Exception as e:
    print(f"  ERROR: {e}")
