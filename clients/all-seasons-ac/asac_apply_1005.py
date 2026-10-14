# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC (4467722415), 2026-10-05 weekly optimization. Approved by Edu in chat.
  A) Campaign-level PHRASE negatives "customer service", "phone number" on Nonbranded Evergreen,
     MiniSplit-General, Mitsubishi-Brand (manufacturer help-line searches).
  B) Display network OFF on MiniSplit-General, Branded Evergreen, Mitsubishi-Brand.
  C) Auto-apply subscription DISPLAY_EXPANSION_OPT_IN -> PAUSED (it keeps switching Display back on).
Usage: ./tsd.sh asac_apply_1005.py           # validate_only
       ./tsd.sh asac_apply_1005.py --apply   # live, then read-back
"""
import sys
sys.path.insert(0, ".")
from lib import init_client
from google.protobuf.json_format import MessageToDict

CID = "4467722415"
NEG_CAMPS = ["23813282398", "24050402045", "24050401592"]
NEG_TERMS = ["customer service", "phone number"]
DISPLAY_CAMPS = ["24050402045", "24202454875", "24050401592"]
APPLY = "--apply" in sys.argv
VO = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
tag = "" if APPLY else " (validate_only)"

# A) negatives
ops = []
for camp in NEG_CAMPS:
    for t in NEG_TERMS:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = ga.campaign_path(CID, camp)
        c.negative = True
        c.keyword.text = t
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
resp = client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "validate_only": VO})
print(f"A) negatives: {len(ops)} ok{tag}", [r.resource_name for r in resp.results] if APPLY else "")

# B) Display off
ops = []
for camp in DISPLAY_CAMPS:
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, camp)
    op.update.network_settings.target_content_network = False
    op.update_mask.paths.append("network_settings.target_content_network")
    ops.append(op)
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": VO})
print(f"B) Display OFF on {len(ops)} campaigns{tag}")

# C) auto-apply Display expansion paused
op = client.get_type("RecommendationSubscriptionOperation")
op.update.resource_name = f"customers/{CID}/recommendationSubscriptions/DISPLAY_EXPANSION_OPT_IN"
op.update.status = client.enums.RecommendationSubscriptionStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("RecommendationSubscriptionService").mutate_recommendation_subscription(
    request={"customer_id": CID, "operations": [op], "validate_only": VO})
print(f"C) auto-apply DISPLAY_EXPANSION_OPT_IN PAUSED{tag}")

if APPLY:
    print("\n--- read-back")
    q = lambda s: [MessageToDict(r._pb, preserving_proto_field_name=True) for r in ga.search(customer_id=CID, query=s)]
    ids = ",".join(sorted(set(NEG_CAMPS + DISPLAY_CAMPS)))
    for r in q(f"SELECT campaign.id, campaign.name, campaign.status, campaign.network_settings.target_content_network, campaign.network_settings.target_search_network, campaign.network_settings.target_partner_search_network FROM campaign WHERE campaign.id IN ({ids})"):
        c = r["campaign"]
        print(f"   {c['name']}: status={c['status']} display={c['network_settings'].get('target_content_network', False)} partners={c['network_settings'].get('target_partner_search_network', False)}")
    for r in q(f"SELECT campaign.id, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign.id IN ({','.join(NEG_CAMPS)}) AND campaign_criterion.negative = TRUE AND campaign_criterion.keyword.text IN ('customer service','phone number')"):
        print(f"   neg {r['campaign']['id']}: {r['campaign_criterion']['keyword']['text']} {r['campaign_criterion']['keyword']['match_type']}")
    for r in q("SELECT recommendation_subscription.type, recommendation_subscription.status, recommendation_subscription.modify_date_time FROM recommendation_subscription"):
        rs = r["recommendation_subscription"]
        if (rs.get("type_") or rs.get("type")) == "DISPLAY_EXPANSION_OPT_IN":
            print(f"   auto-apply DISPLAY_EXPANSION_OPT_IN: {rs['status']} (modified {rs.get('modify_date_time')})")
