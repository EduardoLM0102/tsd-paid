import sys
sys.path.insert(0, "scripts")
from lib import run_query, print_json

q = """
    SELECT
        ad_group.name,
        search_term_view.search_term,
        segments.keyword.info.text,
        segments.keyword.info.match_type,
        metrics.clicks,
        metrics.cost_micros,
        metrics.ctr,
        metrics.conversions
    FROM search_term_view
    WHERE campaign.id = 23848895678
        AND segments.date BETWEEN '2026-07-12' AND '2026-08-10'
    ORDER BY metrics.cost_micros DESC
"""
print_json(run_query("1051843378", q))
