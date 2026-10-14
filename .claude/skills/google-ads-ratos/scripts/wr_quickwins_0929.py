"""Watt's Right quick wins, 2026-09-29. Authorized by Edu in-session (plan approved).

1. PMax: job-seeker + brand negatives (campaign level)
2. Nonbranded + EV Charger: brand negatives; Branded: add brand-misspelling keywords
3. Branded: Target IS max CPC ceiling $5 -> $8

Usage: ./tsd.sh wr_quickwins_0929.py [--validate]
"""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client, run_query

CID = "3651667805"
PMAX, NONBRANDED, EV, BRANDED = "23833205176", "23832838033", "24094882200", "23690645223"
VALIDATE = "--validate" in sys.argv
MODE = "validated" if VALIDATE else "written"

JOB_NEGS = ["apprentice", "apprenticeship", "hiring", "electrician jobs", "electrical jobs",
            "electrician job", "electrical job", "helper jobs", "careers", "career",
            "employment", "salary"]
BRAND_NEGS = ["watts right", "watt's right", "wattsright", "callwattsright",
              "what's right electric", "whats right electric", "watts electric tulsa"]
BRANDED_NEW_KWS = [("what's right electric", "PHRASE"), ("watts electric tulsa", "EXACT")]
BRANDED_CEILING_MICROS = 8_000_000

client = init_client()
ga = client.get_service("GoogleAdsService")
PHRASE = client.enums.KeywordMatchTypeEnum.PHRASE
EXACT = client.enums.KeywordMatchTypeEnum.EXACT


def existing_campaign_negs(cid):
    q = f"""SELECT campaign.status, campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {cid} AND campaign_criterion.negative = true AND campaign_criterion.type = 'KEYWORD'"""
    return {r["campaign_criterion"]["keyword"]["text"].lower() for r in run_query(CID, q)}


# --- 1 + 2a: campaign-level negatives
plan = {PMAX: JOB_NEGS + BRAND_NEGS, NONBRANDED: BRAND_NEGS, EV: BRAND_NEGS}
ops = []
for cid, words in plan.items():
    have = existing_campaign_negs(cid)
    for w in words:
        if w.lower() in have:
            print(f"skip (exists) {cid} {w}")
            continue
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = ga.campaign_path(CID, cid)
        c.negative = True
        c.keyword.text = w
        c.keyword.match_type = PHRASE
        ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(
        request={"customer_id": CID, "operations": ops, "validate_only": VALIDATE})
print(f"campaign negatives: {len(ops)} ops {MODE}")

# --- 2b: Branded keywords
q = f"""SELECT campaign.status, ad_group.id, ad_group.name FROM ad_group
WHERE campaign.id = {BRANDED} AND ad_group.status = 'ENABLED'"""
ag = run_query(CID, q)[0]["ad_group"]
q = f"""SELECT campaign.status, ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE ad_group.id = {ag['id']} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = false"""
have = {r["ad_group_criterion"]["keyword"]["text"].lower() for r in run_query(CID, q)}
kops = []
for text, mt in BRANDED_NEW_KWS:
    if text in have:
        print(f"skip (exists) branded kw {text}")
        continue
    op = client.get_type("AdGroupCriterionOperation")
    c = op.create
    c.ad_group = ga.ad_group_path(CID, ag["id"])
    c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    c.keyword.text = text
    c.keyword.match_type = PHRASE if mt == "PHRASE" else EXACT
    kops.append(op)
if kops:
    client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
        request={"customer_id": CID, "operations": kops, "validate_only": VALIDATE})
print(f"branded keywords in '{ag['name']}': {len(kops)} ops {MODE}")

# --- 3: Branded tIS ceiling
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = ga.campaign_path(CID, BRANDED)
camp.target_impression_share.cpc_bid_ceiling_micros = BRANDED_CEILING_MICROS
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["target_impression_share.cpc_bid_ceiling_micros"]))
client.get_service("CampaignService").mutate_campaigns(
    request={"customer_id": CID, "operations": [op], "validate_only": VALIDATE})
print(f"branded ceiling -> ${BRANDED_CEILING_MICROS/1e6:.2f} {MODE}")
