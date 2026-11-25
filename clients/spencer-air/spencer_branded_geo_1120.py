# APPLIED LIVE 2026-11-20 23:27 UTC (Gui via Claude, Edu's go). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]   (validate-only without --apply)
"""Spencer Air (2524618054) Branded 23822436393, 2026-11-20 (Edu: "da um ajuste nas cidades da campanha branded").
Add the 7 AT service-area cities missing from Branded (alignment 5a7202d9): Allen, Addison, Bedford, Lewisville,
The Colony, Farmers Branch, Highland Village. Existing 10 cities untouched (Arlington stays; not on the AT list but
Edu didn't ask to remove it). Geo type stays PRESENCE. Budget unchanged ($50/d, Target IS $10 ceiling).
Rollback: remove the 7 criteria (resource names printed on apply)."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR = "2524618054", "23822436393"
ADD = {"Allen": 1026178, "Addison": 1026171, "Bedford": 1026215, "Lewisville": 1026556,
       "The Colony": 1026836, "Farmers Branch": 9051933, "Highland Village": 9052132}
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
cur_q = f"SELECT campaign_criterion.location.geo_target_constant, campaign_criterion.negative FROM campaign_criterion WHERE campaign.id = {BR} AND campaign_criterion.type = 'LOCATION'"
cur = {r.campaign_criterion.location.geo_target_constant for r in q(cur_q)}
print("current locations:", len(cur))
ops = []
for name, gid in ADD.items():
    rn = f"geoTargetConstants/{gid}"
    if rn in cur: print("  already there:", name); continue
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, BR); c.location.geo_target_constant = rn
    ops.append(op)
if ops:
    r = client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
    print(f"  ok  {len(ops)} cities", "APPLIED" if APPLY else "(validate_only)", [x.resource_name for x in r.results] if APPLY else "")
if APPLY:
    print("read-back locations:", len(q(cur_q)))
