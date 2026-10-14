#!/usr/bin/env python3
"""Turn off Search Partners (target_search_network) on the two live Search
campaigns still running it: Nonbranded Plumbing and Nonbranded Electrical.

Flagged in the 2026-08-24 book-wide network audit (see memory
tsd-weekly-ppc-snapshot) as 2 of the 9 accounts never corrected. Display
(target_content_network) was already confirmed False on both as of
2026-08-27 (Plumbing was fixed 2026-08-17 via fix_plumbing_display_network.py;
Electrical was already False) but both fields are set here anyway as a
defensive re-assert, matching the same pattern as that script.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "1051843378"
CAMPAIGN_IDS = {
    "23853484024": "TSD_05.14_Leads_Search_Nonbranded_Plumbing",
    "23866999121": "TSD_05.20_Leads_Search_Nonbranded_Electrical",
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

# Read-back verification -- never trust the mutation's own success JSON.
q = f"""
SELECT campaign.id, campaign.name, campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network
FROM campaign
WHERE campaign.id IN ({",".join(CAMPAIGN_IDS)})
"""
rows = run_query(CUSTOMER_ID, q)
for r in rows:
    ns = r["campaign"].get("network_settings", {})
    print(
        "Verified:", r["campaign"]["name"],
        "search_partners =", ns.get("target_search_network", False),
        "| display =", ns.get("target_content_network", False),
    )
