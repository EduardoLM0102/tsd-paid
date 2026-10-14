"""Zen Air 2026-09-30: IDs + full search-term dumps to build the negative lists (read-only)."""
import sys
from collections import defaultdict
sys.path.insert(0, ".")
from lib import run_query
from zenair_st_classify_0930 import cls  # noqa: E402  (reuses the generic-vocabulary classifier)

CID = "4360840956"
BR, NB = "23675783172", "24100030790"

print("=== ad groups + positive keywords on enabled campaigns")
q = f"""
SELECT campaign.id, ad_group.id, ad_group.name, ad_group.status, ad_group_criterion.criterion_id,
       ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
FROM ad_group_criterion
WHERE campaign.id IN ({BR}, {NB}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
  AND ad_group_criterion.status != 'REMOVED'
"""
for r in run_query(CID, q):
    agc = r["ad_group_criterion"]
    print(f"  {'BR' if r['campaign']['id']==BR else 'NB'} ag={r['ad_group']['id']} ({r['ad_group']['name']}, {r['ad_group']['status']}) "
          f"kw={agc['criterion_id']} '{agc['keyword']['text']}' [{agc['keyword']['match_type']}] {agc['status']}")


def dump(label, camp, start, end):
    q = f"""
    SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
    FROM search_term_view WHERE campaign.id = {camp} AND segments.date BETWEEN '{start}' AND '{end}'
    """
    agg = defaultdict(lambda: [0.0, 0, 0, 0.0])
    for r in run_query(CID, q):
        m = r.get("metrics", {})
        a = agg[r["search_term_view"]["search_term"]]
        a[0] += int(m.get("cost_micros", 0)) / 1e6
        a[1] += int(m.get("clicks", 0))
        a[2] += int(m.get("impressions", 0))
        a[3] += float(m.get("conversions", 0))
    print(f"\n=== {label}: {len(agg)} terms")
    for t, a in sorted(agg.items(), key=lambda x: (-x[1][0], -x[1][2])):
        c = cls(t)
        if c == "generic_service":
            continue
        print(f"  [{c[:5]}] {t[:60]:60s} ${a[0]:7.2f} clk={a[1]:3d} imp={a[2]:4d} conv={a[3]:.0f}")


dump("NB clean window (non-generic only)", NB, "2026-08-27", "2026-09-29")
dump("BR last 90d (non-generic only)", BR, "2026-07-01", "2026-09-29")
