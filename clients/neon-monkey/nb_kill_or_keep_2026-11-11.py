# READ-ONLY. fu-122: NB Trimming kill-or-keep read, 11-04..11-10 (7 full days after the 11-04 negatives).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "7953905280", 23825900343
D0, D1 = "2026-11-04", "2026-11-10"
c = init_client(); ga = c.get_service("GoogleAdsService")
m = lambda x: x / 1e6
pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"
q = lambda s: list(ga.search(customer_id=CID, query=s))

print("=== Campaigns 11-04..11-10 ===")
for r in sorted(q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, metrics.cost_micros,
        metrics.impressions, metrics.clicks, metrics.average_cpc, metrics.conversions, metrics.all_conversions,
        metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share
        FROM campaign WHERE segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.impressions > 0"""), key=lambda r: -r.metrics.cost_micros):
    x = r.metrics
    print(f"  {r.campaign.id} {r.campaign.name[:40]:40s} {r.campaign.status.name:8s} bud ${m(r.campaign_budget.amount_micros):4.0f} | ${m(x.cost_micros):8.2f}"
          f" {x.impressions:5d} impr {x.clicks:4d} clk cpc ${m(x.average_cpc):5.2f} conv {x.conversions:4.1f} all {x.all_conversions:4.1f}"
          f" | IS {pct(x.search_impression_share)} lostR {pct(x.search_rank_lost_impression_share)} lostB {pct(x.search_budget_lost_impression_share)}")

print("\n=== NB daily ===")
for r in q(f"""SELECT segments.date, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE campaign.id = {NB} AND segments.date BETWEEN '{D0}' AND '{D1}' ORDER BY segments.date"""):
    x = r.metrics
    print(f"  {r.segments.date} ${m(x.cost_micros):7.2f} {x.clicks:3d} clk conv {x.conversions:3.1f} all {x.all_conversions:3.1f}")

print("\n=== NB conversions by action ===")
for r in q(f"""SELECT segments.conversion_action_name, segments.date, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE campaign.id = {NB} AND segments.date BETWEEN '{D0}' AND '{D1}'"""):
    if r.metrics.all_conversions:
        print(f"  {r.segments.date} {r.segments.conversion_action_name:40s} conv {r.metrics.conversions:3.1f} all {r.metrics.all_conversions:3.1f}")

print("\n=== NB search terms ===")
for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM search_term_view WHERE campaign.id = {NB} AND segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC LIMIT 25"""):
    x = r.metrics
    print(f"  ${m(x.cost_micros):6.2f} {x.clicks:2d} clk conv {x.conversions:3.1f} | {r.search_term_view.search_term}")

print("\n=== NB keywords ===")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
        metrics.cost_micros, metrics.clicks, metrics.impressions FROM keyword_view WHERE campaign.id = {NB}
        AND segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC"""):
    k = r.ad_group_criterion
    print(f"  ${m(r.metrics.cost_micros):6.2f} {r.metrics.clicks:2d} clk {r.metrics.impressions:4d} impr | {k.keyword.text} [{k.keyword.match_type.name}] {k.status.name}")

print("\n=== Calls from ads (call_view) 11-04.. ===")
for r in q(f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code,
        campaign.name FROM call_view WHERE call_view.start_call_date_time >= '{D0} 00:00:00' ORDER BY call_view.start_call_date_time"""):
    v = r.call_view
    print(f"  {v.start_call_date_time} {v.call_duration_seconds:4d}s {v.call_status.name:9s} area {v.caller_area_code} | {r.campaign.name}")

print("\n=== Click view gclids for NB (to match CallRail website-pool calls) ===")
for d in ["2026-11-04", "2026-11-05", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09", "2026-11-10"]:
    rows = q(f"""SELECT click_view.gclid, segments.date, campaign.id FROM click_view WHERE segments.date = '{d}' AND campaign.id = {NB}""")
    for r in rows:
        print(f"  {d} {r.click_view.gclid}")
