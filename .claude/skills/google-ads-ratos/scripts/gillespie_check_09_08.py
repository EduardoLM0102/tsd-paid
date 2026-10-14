import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "7410489772"

print("=" * 100)
print("NETWORK SETTINGS (search campaigns) - confirm 08-24 fix held")
print("=" * 100)
q = """
SELECT campaign.id, campaign.name, campaign.status,
       campaign.network_settings.target_google_search,
       campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network,
       campaign.network_settings.target_partner_search_network
FROM campaign
WHERE campaign.advertising_channel_type = 'SEARCH'
AND campaign.status != 'REMOVED'
"""
for r in run_query(CID, q):
    c = r.get("campaign", {})
    ns = c.get("networkSettings", c.get("network_settings", {}))
    print(f"  {c.get('name','')[:45]:45s} status={c.get('status')} | search_partners={ns.get('targetSearchNetwork', ns.get('target_search_network'))} | "
          f"display/content_net={ns.get('targetContentNetwork', ns.get('target_content_network'))}")

print()
print("=" * 100)
print("CONVERSION ACTIONS - last 7 days (trust check)")
print("=" * 100)
q2 = """
SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS AND metrics.conversions > 0
"""
for r in run_query(CID, q2):
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    print(f"  {seg.get('conversionActionName', seg.get('conversion_action_name'))} | category={seg.get('conversionActionCategory', seg.get('conversion_action_category'))} | conversions={m.get('conversions')}")

print()
print("=" * 100)
print("BRANDED CAMPAIGN - check primary_status / eligibility (zero impressions issue)")
print("=" * 100)
q3 = """
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
       campaign_budget.amount_micros
FROM campaign
WHERE campaign.id = 24155673340
"""
for r in run_query(CID, q3):
    c = r.get("campaign", {})
    b = r.get("campaignBudget", r.get("campaign_budget", {}))
    print(f"  status={c.get('status')} | primary_status={c.get('primaryStatus', c.get('primary_status'))} | reasons={c.get('primaryStatusReasons', c.get('primary_status_reasons'))} | budget_micros={b.get('amountMicros', b.get('amount_micros'))}")

print()
print("=" * 100)
print("NETWORK SPLIT ON NON-BRANDED - last 7 days")
print("=" * 100)
q4 = """
SELECT segments.ad_network_type, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.id = 24155674204 AND segments.date DURING LAST_7_DAYS
"""
for r in run_query(CID, q4):
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    print(f"  network={seg.get('adNetworkType', seg.get('ad_network_type'))} | clicks={m.get('clicks')} | impressions={m.get('impressions')} | conversions={m.get('conversions')} | cost_micros={m.get('costMicros', m.get('cost_micros'))}")

print()
print("=" * 100)
print("NON-BRANDED CAMPAIGN BUDGET - raw check")
print("=" * 100)
q5 = """
SELECT campaign.id, campaign.name, campaign_budget.amount_micros
FROM campaign
WHERE campaign.id = 24155674204
"""
for r in run_query(CID, q5):
    c = r.get("campaign", {})
    b = r.get("campaignBudget", r.get("campaign_budget", {}))
    print(f"  {c.get('name')} | budget_micros={b.get('amountMicros', b.get('amount_micros'))}")
