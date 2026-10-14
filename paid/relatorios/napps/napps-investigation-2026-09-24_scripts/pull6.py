from h import *
q = """
SELECT search_term_view.search_term, search_term_view.status, campaign.name, ad_group.name, segments.month,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions
FROM search_term_view
WHERE segments.date BETWEEN '2025-03-01' AND '2026-09-23'
"""
rows = list(run_query(CID, q))
json.dump(rows, open(OUT+"search_terms.json","w"), default=str)
print(len(rows))
