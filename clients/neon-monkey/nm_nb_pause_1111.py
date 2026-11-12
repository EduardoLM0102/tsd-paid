# STAGED 2026-11-11, NOT applied. Waits for Edu's go (fu-122 kill-or-keep).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Neon Monkey (7953905280): PAUSE NB Trimming 23825900343.
Why: 3 weeks with 0 real leads. 10-19..11-01 $858 / 0 real; 11-04..11-10 $306 / 16 clicks / 0 calls / 0 forms / 0 all_conversions,
no CallRail gclid matching an NB click. Budget $150 and $20 cap left as they are, so re-enabling = status back to ENABLED.
Total spend goes DOWN (~$44/day), so no client approval needed."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "7953905280", "23825900343"
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
