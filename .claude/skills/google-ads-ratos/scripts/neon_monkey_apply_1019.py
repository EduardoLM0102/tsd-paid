"""Neon Monkey 7953905280, 2026-10-19. Approved by Edu in chat ("You have my ok on Neon Monkey's 3 topics").
1. NB Trimming 23825900343: Maximize Conversions -> Maximize Clicks, max CPC $20 (budget $150 unchanged).
2. Branded 23739724064: -> Manual CPC; ad group 193951349406 default max CPC $0.01 -> $5 (no keyword overrides).
3. '[TSD] Click to call' 7835384828: category PHONE_CALL_LEAD -> CONTACT (not biddable on these campaigns; stays in All conversions).
4. PMax 21225221220: positive geo PRESENCE_OR_INTEREST -> PRESENCE (locations list unchanged).
Validate-only unless --apply. Run: ./tsd.sh neon_monkey_apply_1019.py [--apply]
"""
import sys
from lib import init_client
from google.protobuf import field_mask_pb2
CID = "7953905280"
APPLY = "--apply" in sys.argv
client = init_client()
vo = not APPLY

# 1 + 2 + 4: campaigns
cs = client.get_service("CampaignService"); ops = []
op = client.get_type("CampaignOperation"); c = op.update
c.resource_name = cs.campaign_path(CID, "23825900343")
c.target_spend.cpc_bid_ceiling_micros = 20_000_000
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["target_spend.cpc_bid_ceiling_micros"])); ops.append(op)
op = client.get_type("CampaignOperation"); c = op.update
c.resource_name = cs.campaign_path(CID, "23739724064")
c.manual_cpc.enhanced_cpc_enabled = False
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["manual_cpc.enhanced_cpc_enabled"])); ops.append(op)
op = client.get_type("CampaignOperation"); c = op.update
c.resource_name = cs.campaign_path(CID, "21225221220")
c.geo_target_type_setting.positive_geo_target_type = client.enums.PositiveGeoTargetTypeEnum.PRESENCE
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["geo_target_type_setting.positive_geo_target_type"])); ops.append(op)
# Branded ad group bid first (manual CPC would otherwise bid $0.01)
ags = client.get_service("AdGroupService")
op2 = client.get_type("AdGroupOperation"); a = op2.update
a.resource_name = ags.ad_group_path(CID, "193951349406"); a.cpc_bid_micros = 5_000_000
op2.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["cpc_bid_micros"]))
ags.mutate_ad_groups(request={'customer_id': CID, 'operations': [op2], 'validate_only': vo})
cs.mutate_campaigns(request={'customer_id': CID, 'operations': ops, 'validate_only': vo})

# 3: conversion action category
cas = client.get_service("ConversionActionService")
op3 = client.get_type("ConversionActionOperation"); ca = op3.update
ca.resource_name = cas.conversion_action_path(CID, "7835384828")
ca.category = client.enums.ConversionActionCategoryEnum.CONTACT
op3.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["category"]))
cas.mutate_conversion_actions(request={'customer_id': CID, 'operations': [op3], 'validate_only': vo})
print("OK", "APPLIED" if APPLY else "(validate_only)")
