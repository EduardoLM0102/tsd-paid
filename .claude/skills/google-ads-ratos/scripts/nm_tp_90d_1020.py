import sys; sys.path.insert(0, ".")
from lib import init_client
ga=init_client().get_service("GoogleAdsService")
for b in ga.search_stream(customer_id="7953905280", query="SELECT campaign.name, search_term_view.search_term, metrics.clicks, metrics.cost_micros FROM search_term_view WHERE segments.date BETWEEN '2026-07-20' AND '2026-10-20'"):
    for r in b.results:
        t=r.search_term_view.search_term.lower()
        if 'tree place' in t or 'treeplace' in t: print(r.campaign.name,'|',t,r.metrics.clicks,round(r.metrics.cost_micros/1e6,2))
for b in ga.search_stream(customer_id="7953905280", query="SELECT campaign_search_term_insight.category_label, metrics.clicks FROM campaign_search_term_insight WHERE segments.date BETWEEN '2026-07-20' AND '2026-10-20' AND campaign_search_term_insight.campaign_id = 0"):
    pass
