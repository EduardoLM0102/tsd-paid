#!/usr/bin/env python3
"""Turn off Display network on all 4 enabled Search campaigns.

Same create.py hardcoding bug already found and fixed on Zen Air, Cool Hand
Electric, and Gillespie's (2026-08-24) — Search campaigns built with
target_content_network=True. Search Partners (target_search_network) is
already False on all 4 here, so this only needs to flip target_content_network,
but both fields are set explicitly for parity with the other fixes.

Confirmed leak via 7-day network breakdown (2026-08-31):
- Nonbranded Evergreen: $131.93 of $399 spend (33%) on Display vs $267.11 on
  real Search, muddying the campaign's true CPL.
- Mitsubishi-Brand: $68.68 of $104.45 spend (66%) on Display with ZERO
  conversions, vs $35.77 on real Search that produced the campaign's 1 lead.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "4467722415"
CAMPAIGN_IDS = {
    "11803942938": "TSD_Search_LeadGen",
    "23813282398": "TSD_04.29_Search_Nonbranded_Evergreen",
    "24050402045": "TSD_07.01_Lead_Search_MiniSplit-General",
    "24050401592": "TSD_07.01_Lead_Search_Mitsubishi-Brand",
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
WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
"""
rows = run_query(CUSTOMER_ID, q)
for r in rows:
    ns = r["campaign"].get("network_settings", {})
    print(
        "Verified:", r["campaign"]["name"],
        "| target_search_network =", ns.get("target_search_network", False),
        "| target_content_network =", ns.get("target_content_network", False),
    )
