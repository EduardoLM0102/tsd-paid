# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-05 weekly optimization. Approved by Edu in chat ("go to C&S").
  A) Campaign-level PHRASE negatives on TSD_07.05_Leads_Search_Nonbranded_Cooling (23828098448):
     local competitors (Edu blocks competitors here since 08-12), DIY/informational, RV AC.
  B) Pause keyword 'ac not cooling fix' (PHRASE, AC Repair ad group): $216.77 / 31 clicks / 0 conv in 30d, DIY intent.
Then reads back totals for 09-28..10-04 (LSA excluded) for the KPI entry.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, CAMP = "5563867754", "23828098448"
AG, KW = "197197281278", "1571435633198"
PHRASE = ["michael and sons", "lex hvac", "trutex", "always there air", "a 1 air", "comfort masters", "family first comfort",
          "matco", "airplex", "barnett ac", "burnside", "enoch hvac", "klund", "minuteman heating", "how often", "what does",
          "dometic"]
APPLY = "--apply" in sys.argv
tag = "" if APPLY else " (validate_only)"

client = init_client()
ga = client.get_service("GoogleAdsService")
ops = []
for t in PHRASE:
    op = client.get_type("CampaignCriterionOperation")
    c = op.create
    c.campaign = ga.campaign_path(CID, CAMP)
    c.negative = True
    c.keyword.text = t
    c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"A) negatives: {len(ops)} ok{tag}")

op = client.get_type("AdGroupCriterionOperation")
op.update.resource_name = ga.ad_group_criterion_path(CID, AG, KW)
op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
    request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"B) keyword 'ac not cooling fix' PAUSED{tag}")

print("--- read-back")
want = set(PHRASE)
got = [r.campaign_criterion.keyword.text for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.keyword.text
        FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")
       if r.campaign_criterion.keyword.text in want]
print(f"   negatives {len(set(got))}/{len(want)} present; missing: {sorted(want - set(got))}")
for r in ga.search(customer_id=CID, query=f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion
        WHERE ad_group_criterion.criterion_id = {KW} AND ad_group.id = {AG}"""):
    print(f"   keyword '{r.ad_group_criterion.keyword.text}': {r.ad_group_criterion.status.name}")

print("--- PPC totals 09-28..10-04 (LSA excluded)")
for r in ga.search(customer_id=CID, query="""SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM campaign WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04' AND campaign.advertising_channel_type != 'LOCAL_SERVICES'
        AND metrics.impressions > 0"""):
    print(f"   {r.campaign.name} [{r.campaign.advertising_channel_type.name}]: ${r.metrics.cost_micros/1e6:.2f} clk={r.metrics.clicks} conv={r.metrics.conversions:.1f}")
for r in ga.search(customer_id=CID, query="""SELECT metrics.search_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share FROM customer WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04'"""):
    print(f"   account search IS={r.metrics.search_impression_share:.4f} rank_lost={r.metrics.search_rank_lost_impression_share:.4f} budget_lost={r.metrics.search_budget_lost_impression_share:.4f}")
