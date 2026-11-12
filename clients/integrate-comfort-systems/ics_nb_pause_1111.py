# APPLIED LIVE 2026-11-11 09:5x BRT (Edu: "Execute A"), read-back PAUSED. Do NOT re-run with --apply (aborts: not ENABLED).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Integrate Comfort (4571881760): PAUSE NonBranded heating 24047025253.
Why: fails the <= $200 per real lead rule twice. 10-28 checkpoint $287 / 1; since heating-only (10-29..11-10) $281 / 25+18 clicks / 0 real leads, 0 ad calls.
0 CallRail calls with a gclid. Budget $22 and $15 cap left as they are, so re-enabling = status back to ENABLED.
Total spend goes DOWN (~$22/day), so no client approval needed."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "4571881760", "24047025253"
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

before = q(f"SELECT campaign.name, campaign.status FROM campaign WHERE campaign.id = {NB}")[0].campaign
print(f"before: {before.name} {before.status.name}")
if before.status.name != "ENABLED":
    sys.exit("ABORT: NB is not ENABLED, nothing to pause")

op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.status = client.enums.CampaignStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("pause ok", "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    after = q(f"SELECT campaign.status FROM campaign WHERE campaign.id = {NB}")[0].campaign
    print(f"read-back: {after.status.name}")
