"""Neon Monkey 7953905280, 2026-10-26. Approved by Edu in chat ("Yes, apply 1 to 3"), from the 10-26 recheck (fu-094).
1. NB Trimming 23825900343: pause PHRASE 'remove tree stump from yard' (ad group 198813877160, criterion 2475088199212; the EXACT stays);
   campaign negatives PHRASE rental, rent, how to, diy, chemical, jack, vs, remover + EXACT stump grinder.
2. Branded ad group 193951349406: max CPC $5 -> $6.
3. PMax 21225221220: copy NB's 36 West FW locations, exclude Arlington/Dallas/Grand Prairie/Irving TX, then remove Fort Worth city
   1026411 + the 5 radius circles. One atomic request, adds before removes. Budgets unchanged.
Validate-only unless --apply. Run: ./tsd.sh neon_monkey_apply_1026.py [--apply]
"""
import sys
from lib import init_client
from google.protobuf import field_mask_pb2
CID = "7953905280"; NB = "23825900343"; PMAX = "21225221220"
APPLY = "--apply" in sys.argv
client = init_client(); vo = not APPLY
NB_LOCS = [1026175, 1026204, 9027192, 9027244, 9027248, 9027250, 9027253, 9027254, 9027255, 9027256, 9027259, 9027260, 9027261,
           9027266, 9027268, 9027269, 9027271, 9027272, 9027273, 9027275, 9027278, 9027283, 9027284, 9051585, 9052790, 9053169,
           9190074, 9190457, 9190910, 9194620, 9194931, 9195005, 9195476, 9211681, 9215592, 9219741]
EXCL = [1026194, 1026339, 1026439, 1026497]  # Arlington, Dallas, Grand Prairie, Irving (all Texas)
PMAX_OLD = ["1026411", "2298949617968", "2326917008110", "2326917008150", "2326917008310", "2326917008350"]
assert len(NB_LOCS) == 36
gtc = client.get_service("GeoTargetConstantService")
ccs = client.get_service("CampaignCriterionService"); camp = client.get_service("CampaignService").campaign_path

# 1a. pause the phrase keyword
agcs = client.get_service("AdGroupCriterionService")
op = client.get_type("AdGroupCriterionOperation")
op.update.resource_name = agcs.ad_group_criterion_path(CID, "198813877160", "2475088199212")
op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))
agcs.mutate_ad_group_criteria(request={"customer_id": CID, "operations": [op], "validate_only": vo})

# 1b. NB negatives
ops = []
for text, mt in [(t, "PHRASE") for t in ["rental", "rent", "how to", "diy", "chemical", "jack", "vs", "remover"]] + [("stump grinder", "EXACT")]:
    o = client.get_type("CampaignCriterionOperation"); c = o.create
    c.campaign = camp(CID, NB); c.negative = True
    c.keyword.text = text; c.keyword.match_type = client.enums.KeywordMatchTypeEnum[mt]; ops.append(o)
ccs.mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})

# 2. Branded ad group bid
ags = client.get_service("AdGroupService")
o = client.get_type("AdGroupOperation"); o.update.resource_name = ags.ad_group_path(CID, "193951349406")
o.update.cpc_bid_micros = 6_000_000
o.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["cpc_bid_micros"]))
ags.mutate_ad_groups(request={"customer_id": CID, "operations": [o], "validate_only": vo})

# 3. PMax geo: adds, then removes, one atomic request
ops = []
for gid, neg in [(g, False) for g in NB_LOCS] + [(g, True) for g in EXCL]:
    o = client.get_type("CampaignCriterionOperation"); c = o.create
    c.campaign = camp(CID, PMAX); c.location.geo_target_constant = gtc.geo_target_constant_path(gid)
    if neg: c.negative = True
    ops.append(o)
for crit in PMAX_OLD:
    o = client.get_type("CampaignCriterionOperation"); o.remove = ccs.campaign_criterion_path(CID, PMAX, crit); ops.append(o)
ccs.mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("OK", "APPLIED" if APPLY else "(validate_only)")
