#!/usr/bin/env python3
"""Turn off Search Partners + Display network on both Search campaigns.

Same fix as Zen Air (24100030790) and Cool Hand Electric (9865206319) on
2026-08-24: create.py hardcoded target_search_network=True with no opt-out,
and both of these campaigns also have target_content_network=True. Confirmed
via network breakdown on the Non-Branded campaign (last 7 days): real Search
12 clicks/1 lead/$190.25, Search Partners 11 clicks/0 leads/$25.05 wasted,
Display 1 click/1 "lead"/$1.12 (converted on the first click — junk pattern,
not a real lead).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "7410489772"
CAMPAIGN_IDS = {
    "24155673340": "TSD_08.18_Search_Branded_Evergreen",
    "24155674204": "TSD_08.18_Search_NonBranded_Evergreen",
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
