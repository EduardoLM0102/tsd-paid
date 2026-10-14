# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Napps (9509605037), 2026-10-05 weekly optimization. Approved by Edu in chat ("napps now").
  A) Pause keyword 'new air conditioner' (PHRASE, AC Replacement ad group, AC Summer): QS 1, $224 / 14 clicks / 0 conv 30d.
  B) PHRASE negatives: AC Summer (24049055193) 'store', 'scratch and dent'; Plumbing (23819717682) 'store'.
Budgets untouched (client's equal HVAC / plumbing split stays $50 / $50).
Then reads back totals for 09-28..10-04 for the KPI entry.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9509605037"
AG, KW = "198093421826", "941382736"
NEG = {"24049055193": ["store", "scratch and dent"], "23819717682": ["store"]}
APPLY = "--apply" in sys.argv
tag = "" if APPLY else " (validate_only)"

client = init_client()
ga = client.get_service("GoogleAdsService")

op = client.get_type("AdGroupCriterionOperation")
op.update.resource_name = ga.ad_group_criterion_path(CID, AG, KW)
op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
    request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"A) keyword 'new air conditioner' PAUSED{tag}")

ops = []
for camp, terms in NEG.items():
    for t in terms:
        o = client.get_type("CampaignCriterionOperation")
        c = o.create
        c.campaign = ga.campaign_path(CID, camp)
        c.negative = True
        c.keyword.text = t
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(o)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"B) negatives: {len(ops)} ok{tag}")

print("--- read-back")
for r in ga.search(customer_id=CID, query=f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion
        WHERE ad_group_criterion.criterion_id = {KW} AND ad_group.id = {AG}"""):
    print(f"   keyword '{r.ad_group_criterion.keyword.text}': {r.ad_group_criterion.status.name}")
for camp, terms in NEG.items():
    got = {r.campaign_criterion.keyword.text for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.keyword.text
            FROM campaign_criterion WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   {camp}: {sorted(set(terms) & got)} present, missing {sorted(set(terms) - got)}")

print("--- PPC totals 09-28..10-04 + budgets")
for r in ga.search(customer_id=CID, query="""SELECT campaign.name, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM campaign WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04' AND metrics.impressions > 0"""):
    print(f"   {r.campaign.name}: ${r.metrics.cost_micros/1e6:.2f} clk={r.metrics.clicks} conv={r.metrics.conversions:.1f} budget=${r.campaign_budget.amount_micros/1e6:.0f}/d")
for r in ga.search(customer_id=CID, query="""SELECT metrics.search_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share FROM customer WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04'"""):
    print(f"   account search IS={r.metrics.search_impression_share:.4f} rank_lost={r.metrics.search_rank_lost_impression_share:.4f} budget_lost={r.metrics.search_budget_lost_impression_share:.4f}")
