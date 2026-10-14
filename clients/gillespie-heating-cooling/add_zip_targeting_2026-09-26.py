#!/usr/bin/env python3
"""Add the client's service-area ZIP codes to the two new Gillespie Search campaigns.

2026-09-26. Client service area (14 KY + 23 OH ZIPs) vs the 11-city targeting found that
none of the Ohio area was covered and ~57% of past spend went to Cincinnati-area Ohio,
which is not in the client's list. This adds the ZIPs as Postal Code location criteria.

Skipped: 45105, 45115, 45119, 45618. Google's geo_target_constant table marks all four
REMOVAL_PLANNED (being retired), so they are not added.

Idempotent: skips any ZIP already targeted on the campaign. Removing Cincinnati OH
(geo 1023626) is a separate step, done with delete.py after this succeeds.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))
from lib import init_client, run_query  # noqa: E402

CID = "7410489772"
CAMPAIGNS = {"24297839425": "TSD_09.26_Search_NonBranded_Evergreen", "24297891262": "TSD_09.26_Search_Branded_Evergreen"}
ZIP_GEO_IDS = {
    # Kentucky (14)
    "41002": 9014388, "41004": 9014390, "41056": 9014419, "41001": 9014387, "41076": 9014427, "41091": 9014432, "41042": 9014409,
    "41007": 9014393, "41006": 9014392, "41040": 9014407, "41051": 9014416, "41075": 9014426, "41018": 9014401, "41017": 9014400,
    # Ohio (19 of the client's 23; 45105/45115/45119/45618 are REMOVAL_PLANNED in Google's table)
    "45101": 9015648, "45118": 9015657, "45121": 9015660, "45130": 9015663, "45131": 9015664, "45144": 9015671, "45154": 9015679,
    "45167": 9015688, "45168": 9015689, "45171": 9015691, "45176": 9015693, "45616": 9015863, "45650": 9015882, "45657": 9015888,
    "45660": 9015891, "45679": 9015901, "45684": 9015905, "45693": 9015911, "45697": 9015915,
}

client = init_client()
svc = client.get_service("CampaignCriterionService")
camp_svc = client.get_service("CampaignService")

for cid, name in CAMPAIGNS.items():
    existing = {
        r["campaign_criterion"]["location"]["geo_target_constant"].split("/")[-1]
        for r in run_query(CID, f"SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion "
                                f"WHERE campaign.id = {cid} AND campaign_criterion.type = 'LOCATION'")
    }
    ops = []
    for zip_code, gid in ZIP_GEO_IDS.items():
        if str(gid) in existing:
            continue
        op = client.get_type("CampaignCriterionOperation")
        op.create.campaign = camp_svc.campaign_path(CID, cid)
        op.create.location.geo_target_constant = f"geoTargetConstants/{gid}"
        ops.append(op)
    if ops:
        svc.mutate_campaign_criteria(customer_id=CID, operations=ops)
    print(f"{name} ({cid}): added {len(ops)} ZIP locations, {len(ZIP_GEO_IDS) - len(ops)} already present")
