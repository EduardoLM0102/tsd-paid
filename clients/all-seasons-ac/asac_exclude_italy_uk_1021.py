# APPLIED LIVE 2026-10-21 on Edu's go. Re-running is safe (skips campaigns that already exclude both).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC (4467722415), 2026-10-21, Edu: "Yes please, go ahead with that".
Angela (10-19, Slack DM): the client questioned the invoice's Italy + UK lines (Google regulatory fees, $0.03 each); Edu promised
to exclude both countries. Adds Italy (2380) and United Kingdom (2826) as NEGATIVE location criteria on every non-removed
Search / PMax campaign (paused ones too, so a re-enable doesn't bring them back). Skips campaigns that already exclude them.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "4467722415"
COUNTRIES = {"2380": "Italy", "2826": "United Kingdom"}
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

for gid, name in COUNTRIES.items():
    g = q(f"SELECT geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.resource_name = 'geoTargetConstants/{gid}'")
    print(f"{gid}: {g[0].geo_target_constant.name} ({g[0].geo_target_constant.target_type})")
    if g[0].geo_target_constant.name != name: sys.exit(f"ABORT: {gid} is not {name}")

camps = q("""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type FROM campaign
    WHERE campaign.status != 'REMOVED' AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')""")
have = {(str(r.campaign.id), r.campaign_criterion.location.geo_target_constant.split("/")[-1]) for r in q("""SELECT campaign.id,
    campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION'
    AND campaign_criterion.negative = TRUE AND campaign.status != 'REMOVED'""")}

ops = []
for c in camps:
    for gid in COUNTRIES:
        if (str(c.campaign.id), gid) in have: continue
        op = client.get_type("CampaignCriterionOperation"); cc = op.create
        cc.campaign = ga.campaign_path(CID, c.campaign.id); cc.negative = True
        cc.location.geo_target_constant = f"geoTargetConstants/{gid}"; ops.append(op)
    print(f"  {c.campaign.name} ({c.campaign.status.name}, {c.campaign.advertising_channel_type.name})")
print(f"{len(camps)} campaigns, {len(ops)} exclusions to add")
if not ops: sys.exit("nothing to do")

client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print("exclusions ok", "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    got = {(str(r.campaign.id), r.campaign_criterion.location.geo_target_constant.split("/")[-1]) for r in q("""SELECT campaign.id,
        campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION'
        AND campaign_criterion.negative = TRUE AND campaign.status != 'REMOVED'""")}
    missing = [(c.campaign.name, gid) for c in camps for gid in COUNTRIES if (str(c.campaign.id), gid) not in got]
    print(f"read-back: missing {missing}" if missing else f"read-back: Italy + UK excluded on all {len(camps)} campaigns")
