#!/usr/bin/env python3
"""Remove off-topic Plumbing/Electrical assets from the PMax HVAC asset group.

Gap found 2026-08-17: asset group "HVAC" (6712908741) inside TSD_05.14_Leads_Pmax_HVAC
(23853595615) rated AVERAGE ad strength, in part because its headline/description pool
included assets with nothing to do with HVAC (water heater, plumbers, electricians).
Removing the 10 unambiguous ones; 4 "HVAC, plumbing, and electrical" combined-messaging
assets are left in place since dropping those is a messaging call, not cleanup.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query

CUSTOMER_ID = "1051843378"
ASSET_GROUP_ID = "6712908741"

RESOURCE_NAMES_TO_REMOVE = [
    # Headlines
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~345699706684~HEADLINE",   # Proud Pops Electrical
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360740453357~HEADLINE",   # Trusted Water Heater Pros
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360809118202~HEADLINE",   # Licensed Plumbers SA TX
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360809118214~HEADLINE",   # Upfront Plumbing Pricing
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360828257188~HEADLINE",   # Leak Detection Experts SA
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360828257209~HEADLINE",   # Family-Owned Plumbing Co
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~369432606342~HEADLINE",   # Proud Pops Plumbing
    # Descriptions
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360828257212~DESCRIPTION",  # Leak or burst pipe...
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~360828257215~DESCRIPTION",  # Licensed plumbers serving...
    f"customers/{CUSTOMER_ID}/assetGroupAssets/{ASSET_GROUP_ID}~362781434102~DESCRIPTION",  # Family-owned electricians...
]

client = init_client()
service = client.get_service("AssetGroupAssetService")

operations = []
for rn in RESOURCE_NAMES_TO_REMOVE:
    op = client.get_type("AssetGroupAssetOperation")
    op.remove = rn
    operations.append(op)

response = service.mutate_asset_group_assets(customer_id=CUSTOMER_ID, operations=operations)
print(f"Removed {len(response.results)} asset_group_asset links")

# Read-back verification — never trust the mutation's own success JSON.
q = f"""
SELECT asset_group_asset.field_type, asset.type, asset.text_asset.text
FROM asset_group_asset
WHERE asset_group.id = {ASSET_GROUP_ID} AND asset_group_asset.field_type IN ('HEADLINE','DESCRIPTION')
"""
rows = run_query(CUSTOMER_ID, q)
headlines = [r for r in rows if r["asset_group_asset"]["field_type"] == "HEADLINE"]
descriptions = [r for r in rows if r["asset_group_asset"]["field_type"] == "DESCRIPTION"]
print(f"Verified: {len(headlines)} headlines, {len(descriptions)} descriptions remain")
remaining_texts = [r["asset"].get("text_asset", {}).get("text", "") for r in rows]
leftover_offtopic = [t for t in remaining_texts if any(w in t.lower() for w in ["plumb", "electric", "water heater"])]
print(f"Off-topic terms still present in remaining assets: {leftover_offtopic}")
