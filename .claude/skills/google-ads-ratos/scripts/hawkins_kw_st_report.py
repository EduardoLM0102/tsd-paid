import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query, print_json

CUSTOMER_ID = "2198608170"
CAMPAIGN_ID = 23805382277
SINCE = "2026-04-29"
UNTIL = "2026-09-13"

kw_query = f"""
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.average_cpc,
        metrics.cost_micros,
        metrics.conversions,
        metrics.cost_per_conversion
    FROM keyword_view
    WHERE campaign.id = {CAMPAIGN_ID}
        AND ad_group_criterion.status = 'ENABLED'
        AND segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
    ORDER BY metrics.conversions DESC
"""

st_query = f"""
    SELECT
        ad_group.name,
        search_term_view.search_term,
        segments.keyword.info.text,
        segments.keyword.info.match_type,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.ctr,
        metrics.conversions
    FROM search_term_view
    WHERE campaign.id = {CAMPAIGN_ID}
        AND segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
        AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
"""

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "keywords"
    if mode == "keywords":
        print_json(run_query(CUSTOMER_ID, kw_query))
    else:
        print_json(run_query(CUSTOMER_ID, st_query))
