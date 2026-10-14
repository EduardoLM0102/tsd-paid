#!/usr/bin/env python3
"""Pause the legacy Problem Solvers ROOFING LSA campaign (account 3477779749, campaign 20805107400). Edu asked 2026-10-08.
Default validate-only; --apply writes; read-back after."""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID, CAMP = "3477779749", "20805107400"
client = init_client()
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
o = client.get_type("MutateOperation"); c = o.campaign_operation.update
c.resource_name = f"customers/{CID}/campaigns/{CAMP}"
c.status = client.enums.CampaignStatusEnum.PAUSED
o.campaign_operation.update_mask.paths.append("status")
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.append(o); req.validate_only = not a.apply
client.get_service("GoogleAdsService").mutate(request=req)
print("APPLIED" if a.apply else "VALIDATE-ONLY OK (nothing written)")
if a.apply:
    for r in run_query(CID, f"SELECT campaign.name, campaign.status, campaign.serving_status, campaign.primary_status FROM campaign WHERE campaign.id = {CAMP}"):
        print("READ-BACK:", r["campaign"])
