"""Zen Air 2026-09-30: branded search terms by matching keyword match type (read-only)."""
import sys
from collections import defaultdict
sys.path.insert(0, ".")
from lib import run_query
CID = "4360840956"
q = """
SELECT search_term_view.search_term, segments.keyword.info.text, segments.keyword.info.match_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view WHERE campaign.id = 23675783172 AND segments.date BETWEEN '2026-07-01' AND '2026-09-29'
"""
agg = defaultdict(lambda: [0.0, 0, 0, 0.0])
for r in run_query(CID, q):
    k = r["segments"]["keyword"]["info"]
    m = r.get("metrics", {})
    a = agg[(k.get("match_type"), k.get("text"), r["search_term_view"]["search_term"])]
    a[0] += int(m.get("cost_micros", 0)) / 1e6; a[1] += int(m.get("clicks", 0))
    a[2] += int(m.get("impressions", 0)); a[3] += float(m.get("conversions", 0))
tot = defaultdict(lambda: [0.0, 0, 0, 0.0])
for (mt, kw, st), a in agg.items():
    brand = "zen" in st.lower()
    for i in range(4):
        tot[(mt, brand)][i] += a[i]
for k, a in sorted(tot.items()):
    print(f"{k[0]:8s} brand_query={k[1]!s:5s} cost=${a[0]:8.2f} clk={a[1]:4d} imp={a[2]:5d} conv={a[3]:.0f}")
print("\nNON-BROAD keywords matching queries WITHOUT 'zen' (the leaks that survive pausing broads):")
for (mt, kw, st), a in sorted(agg.items(), key=lambda x: -x[1][2]):
    if mt != "BROAD" and "zen" not in st.lower():
        print(f"  [{mt}] kw='{kw}' -> '{st}' ${a[0]:.2f} clk={a[1]} imp={a[2]} conv={a[3]:.0f}")
print("\nBrand-containing queries that look off (not the HVAC company):")
for (mt, kw, st), a in sorted(agg.items(), key=lambda x: -x[1][2]):
    s = st.lower()
    if "zen" in s and not any(w in s for w in ["heat", "cool", "air cond", "hvac", "ac ", " ac", "repair", "duluth", "suwanee", "phone", "number", "review", "near", "service", "furnace", "georgia", " ga", "callzenair", "company", "llc", "inc"]) and s.strip() not in ("zen air", "zenair", "zen-air", "zen airs", "zen air'"):
        print(f"  [{mt}] kw='{kw}' -> '{st}' ${a[0]:.2f} clk={a[1]} imp={a[2]}")
