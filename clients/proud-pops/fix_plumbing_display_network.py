#!/usr/bin/env python3
"""Turn off Display network (target_content_network) on Search Nonbranded Plumbing.

Gate-1 fix from budget-allocation-2026-08.md, staged since 2026-07-30, never executed.
Campaign 23853484024 was still serving on Display as of 2026-08-13 (confirmed via
campaign.network_settings.target_content_network = True).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "1051843378"
CAMPAIGN_ID = "23853484024"

client = init_client()
gads_service = client.get_service("GoogleAdsService")
campaign_service = client.get_service("CampaignService")

op = client.get_type("CampaignOperation")
campaign = op.update
campaign.resource_name = gads_service.campaign_path(CUSTOMER_ID, CAMPAIGN_ID)
campaign.network_settings.target_content_network = False
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["network_settings.target_content_network"]))

response = campaign_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
print("Mutated:", response.results[0].resource_name)

# Read-back verification — never trust the mutation's own success JSON.
q = f"""
SELECT campaign.id, campaign.name, campaign.network_settings.target_content_network
FROM campaign
WHERE campaign.id = {CAMPAIGN_ID}
"""
rows = run_query(CUSTOMER_ID, q)
for r in rows:
    ns = r["campaign"].get("network_settings", {})
    print("Verified:", r["campaign"]["name"], "target_content_network =", ns.get("target_content_network", False))
