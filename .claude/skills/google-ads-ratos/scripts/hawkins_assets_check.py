import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "2198608170"
CAMPAIGN_ID = "23805382277"

print("=== Assets linked at CAMPAIGN level ===")
q1 = f"""
SELECT campaign.id, asset.type, asset.id, campaign_asset.status, campaign_asset.field_type
FROM campaign_asset
WHERE campaign.id = {CAMPAIGN_ID}
"""
for r in run_query(CID, q1):
    a = r.get("asset", {})
    ca = r.get("campaign_asset", {})
    print(f"  type={a.get('type')}  status={ca.get('status')}  field_type={ca.get('field_type')}  id={a.get('id')}")

print("\n=== Assets linked at ACCOUNT (customer) level ===")
q2 = """
SELECT asset.type, asset.id, customer_asset.status, customer_asset.field_type
FROM customer_asset
"""
for r in run_query(CID, q2):
    a = r.get("asset", {})
    ca = r.get("customer_asset", {})
    print(f"  type={a.get('type')}  status={ca.get('status')}  field_type={ca.get('field_type')}  id={a.get('id')}")

print("\n=== Assets linked at AD GROUP level (Siding ad group) ===")
q3 = """
SELECT ad_group.id, asset.type, asset.id, ad_group_asset.status, ad_group_asset.field_type
FROM ad_group_asset
WHERE ad_group.id = 196112304677
"""
for r in run_query(CID, q3):
    a = r.get("asset", {})
    aa = r.get("ad_group_asset", {})
    print(f"  type={a.get('type')}  status={aa.get('status')}  field_type={aa.get('field_type')}  id={a.get('id')}")
