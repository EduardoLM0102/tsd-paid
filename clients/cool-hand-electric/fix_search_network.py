#!/usr/bin/env python3
"""Turn off Search Partners + Display network on all 3 Search campaigns.

Same fix as Zen Air (24100030790) on 2026-08-24: create.py hardcoded
target_search_network=True with no opt-out, and these 3 campaigns also have
target_content_network=True (built/edited in the UI wizard, which defaults
both networks checked). Confirmed via network breakdown that 78% of the
account's PPC spend/12% of "conversions" was going to Search Partners/Display,
not real Google Search demand.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "9865206319"
CAMPAIGN_IDS = {
    "24118511502": "TSD_Search_HVAC",
    "24123995882": "TSD_Search_Electrical",
    "24123995948": "TSD_Search_Branded",
}

client = init_client()
gads_service = client.get_service("GoogleAdsService")
campaign_service = client.get_service("CampaignService")

ops = []
for campaign_id in CAMPAIGN_IDS:
    op = client.get_type("CampaignOperation")
    campaign = op.update
    campaign.resource_name = gads_service.campaign_path(CUSTOMER_ID, campaign_id)
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(
        paths=["network_settings.target_search_network", "network_settings.target_content_network"]
    ))
    ops.append(op)

response = campaign_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=ops)
for r in response.results:
    print("Mutated:", r.resource_name)

# Read-back verification — never trust the mutation's own success JSON.
q = """
SELECT campaign.id, campaign.name, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network
FROM campaign
WHERE campaign.advertising_channel_type = 'SEARCH'
"""
rows = run_query(CUSTOMER_ID, q)
for r in rows:
    ns = r["campaign"].get("network_settings", {})
    print(
        "Verified:", r["campaign"]["name"],
        "| target_search_network =", ns.get("target_search_network", False),
        "| target_content_network =", ns.get("target_content_network", False),
    )
