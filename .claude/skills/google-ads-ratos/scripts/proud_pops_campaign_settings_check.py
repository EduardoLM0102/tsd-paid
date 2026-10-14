"""Proud Pops: Search campaign settings worth knowing before more campaign work (read-only)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID = "1051843378"
q = """SELECT campaign.id, campaign.name, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
campaign.network_settings.target_partner_search_network, campaign.asset_automation_settings, campaign.ai_max_setting.enable_ai_max
FROM campaign WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'"""
try:
    rows = run_query(CID, q)
except SystemExit:
    rows = run_query(CID, q.replace(", campaign.ai_max_setting.enable_ai_max", ""))
for r in rows:
    c = r["campaign"]; ns = c.get("network_settings", {})
    auto = {a["asset_automation_type"].replace("_ASSET_AUTOMATION", ""): a["asset_automation_status"] for a in c.get("asset_automation_settings", [])}
    print(f"{c['name'][:44]:44s} search={ns.get('target_search_network')} partners={ns.get('target_partner_search_network')} display={ns.get('target_content_network')} "
          f"ai_max={c.get('ai_max_setting', {}).get('enable_ai_max')} automation={auto}")
print("\nAG4_Plumbing_General (July 'Change 1') exists?",
      [(r["ad_group"]["id"], r["ad_group"]["status"]) for r in run_query(CID, "SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE ad_group.name = 'AG4_Plumbing_General'")] or "no")
print("\nSearch landing pages last 14 days (expanded), Search Electrical / HVAC / Plumbing:")
for r in run_query(CID, """SELECT campaign.name, expanded_landing_page_view.expanded_final_url, metrics.clicks, metrics.cost_micros
FROM expanded_landing_page_view WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date BETWEEN '2026-09-24' AND '2026-10-07' AND metrics.clicks > 0"""):
    u = r["expanded_landing_page_view"]["expanded_final_url"].split("?")[0]
    print(f"   {r['campaign']['name'][24:50]:26s} {u[:60]:60s} clk {r['metrics']['clicks']} ${int(r['metrics']['cost_micros'])/1e6:,.0f}")
