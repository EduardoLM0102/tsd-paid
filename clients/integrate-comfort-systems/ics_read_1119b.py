# READ-ONLY follow-up to ics_read_1119.py
import sys; sys.path.insert(0, ".")
from lib import run_query
CID, NB = "4571881760", "24047025253"
M = lambda x: int(x or 0) / 1e6
q = lambda s: run_query(CID, s)
print("== clicked NB search terms 11-12..11-19")
for r in q(f"SELECT segments.date, search_term_view.search_term, metrics.clicks, metrics.cost_micros FROM search_term_view WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-19' AND metrics.clicks > 0 ORDER BY segments.date"):
    print(f"  {r['segments']['date']} {r['search_term_view']['search_term'][:55]:<55} clk {r['metrics'].get('clicks')} ${M(r['metrics'].get('cost_micros')):.2f}")
print("== NB geo 11-12..11-19 clicked")
for r in q(f"SELECT campaign.id, segments.geo_target_city, metrics.cost_micros, metrics.clicks FROM user_location_view WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-12' AND '2026-11-19' AND metrics.clicks > 0"):
    print("  ", r["segments"].get("geo_target_city"), f"${M(r['metrics'].get('cost_micros')):.2f}", r["metrics"].get("clicks"))
print("== NB device 11-17..11-19")
for r in q(f"SELECT segments.device, metrics.cost_micros, metrics.clicks, metrics.impressions FROM campaign WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-11-17' AND '2026-11-19'"):
    print("  ", r["segments"]["device"], f"${M(r['metrics'].get('cost_micros')):.2f}", r["metrics"].get("clicks"), r["metrics"].get("impressions"))
print("== NB bidding now")
for r in q(f"SELECT campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros, campaign.primary_status, campaign.primary_status_reasons FROM campaign WHERE campaign.id = {NB}"):
    print("  ", r["campaign"], M(r["campaign_budget"]["amount_micros"]))
