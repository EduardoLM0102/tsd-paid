# APPLIED LIVE 2026-11-11 09:5x BRT (Edu: "Execute A"), read-back PAUSED. Do NOT re-run with --apply (aborts: not ENABLED).
"""Integrate Comfort (4571881760): PAUSE PMax 22890783804 (TSD_03_22_Pmax_Evergreen).
Why: after taps left the goal (11-04) PMax has 0 conversions, 69% of spend on YouTube, Search side = competitor names;
11-05..11-10 $244 / 0 real leads; October $936 window / 1 real call. Budget $40 left as is (re-enable = status back to ENABLED).
Paired with the NB pause: $62/day of 0-lead spend stops; funds the LSA Belleville restore (ics_lsa_budgets_1111.py)."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, PM = "4571881760", "22890783804"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

before = q(f"SELECT campaign.name, campaign.status FROM campaign WHERE campaign.id = {PM}")[0].campaign
print(f"before: {before.name} {before.status.name}")
if before.status.name != "ENABLED":
    sys.exit("ABORT: PMax is not ENABLED, nothing to pause")
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, PM)
op.update.status = client.enums.CampaignStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("pause ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    print("read-back:", q(f"SELECT campaign.status FROM campaign WHERE campaign.id = {PM}")[0].campaign.status.name)
