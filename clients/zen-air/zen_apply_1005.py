# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Zen Air (4360840956), 2026-10-05 weekly optimization. Approved by Edu in chat ("move to the next one").
Campaign-level negatives on TSD_08.03_Search_NonBranded_Evergreen (24100030790), built from search terms since the
09-30 changes. Duct cleaning kept open (site lists Ventilation & Duct Cleaning). Price/cost searches kept open.
Then reads back the account totals for 09-28..10-04 for the KPI entry.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, CAMP = "4360840956", "24100030790"
PHRASE = ["metus", "jc lane", "omega heating", "res air", "johnson controls", "stand for"]
EXACT = ["top notch buford", "what is hvac", "ttb024c100a2", "fb4cnp042", "carrier fj5a"]
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
MT = client.enums.KeywordMatchTypeEnum
ops = []
for t, mt in [(t, MT.PHRASE) for t in PHRASE] + [(t, MT.EXACT) for t in EXACT]:
    op = client.get_type("CampaignCriterionOperation")
    c = op.create
    c.campaign = ga.campaign_path(CID, CAMP)
    c.negative = True
    c.keyword.text = t
    c.keyword.match_type = mt
    ops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"negatives: {len(ops)} ok{'' if APPLY else ' (validate_only)'}")

print("--- read-back")
want = set(PHRASE + EXACT)
got = []
for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
        FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"""):
    if r.campaign_criterion.keyword.text in want:
        got.append(f"{r.campaign_criterion.keyword.text} [{r.campaign_criterion.keyword.match_type.name}]")
print(f"   {len(got)}/{len(want)} present:", ", ".join(sorted(got)))

print("--- PPC totals 09-28..10-04")
for r in ga.search(customer_id=CID, query="""SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM campaign WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04' AND metrics.impressions > 0"""):
    print(f"   {r.campaign.name}: ${r.metrics.cost_micros/1e6:.2f} clk={r.metrics.clicks} conv={r.metrics.conversions:.1f}")
for r in ga.search(customer_id=CID, query="""SELECT metrics.search_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share FROM customer WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04'"""):
    print(f"   account search IS={r.metrics.search_impression_share:.4f} rank_lost={r.metrics.search_rank_lost_impression_share:.4f} budget_lost={r.metrics.search_budget_lost_impression_share:.4f}")
