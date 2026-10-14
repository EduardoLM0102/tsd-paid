# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), 2026-10-05 weekly optimization. Approved by Edu in chat ("next one now").
Campaign-level negatives on TSD_04.29_Leads_Nonbranded_Evergreen (23805382277): handyman / Angi / grant and
senior-aid searches, DIY and where-to-buy, suppliers, generic construction. Competitor names kept open (several
converted in 30d: bee builders, hometown building center, homeland vinyl), 'sherwin williams' kept (converted once).
Then reads back totals for 09-28..10-04 (LSA excluded) for the KPI entry.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, CAMP = "2198608170", "23805382277"
PHRASE = ["handyman", "angi", "angies list", "grants", "senior citizens", "how to", "where to purchase", "where to buy",
          "norandex", "qxo", "building a house"]
EXACT = ["construction company", "construction companies"]
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

want = set(PHRASE + EXACT)
got = {r.campaign_criterion.keyword.text for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.keyword.text
        FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
print(f"--- read-back: {len(want & got)}/{len(want)} present; missing: {sorted(want - got)}")

print("--- PPC totals 09-28..10-04 (LSA excluded)")
for r in ga.search(customer_id=CID, query="""SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM campaign WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04' AND campaign.advertising_channel_type != 'LOCAL_SERVICES'
        AND metrics.impressions > 0"""):
    print(f"   {r.campaign.name}: ${r.metrics.cost_micros/1e6:.2f} clk={r.metrics.clicks} conv={r.metrics.conversions:.1f}")
for r in ga.search(customer_id=CID, query="""SELECT segments.conversion_action_name, metrics.conversions FROM campaign
        WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04' AND campaign.advertising_channel_type != 'LOCAL_SERVICES'
        AND metrics.conversions > 0"""):
    print(f"   action {r.segments.conversion_action_name}: {r.metrics.conversions:.1f}")
for r in ga.search(customer_id=CID, query="""SELECT metrics.search_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share FROM customer WHERE segments.date BETWEEN '2026-09-28' AND '2026-10-04'"""):
    print(f"   account search IS={r.metrics.search_impression_share:.4f} rank_lost={r.metrics.search_rank_lost_impression_share:.4f} budget_lost={r.metrics.search_budget_lost_impression_share:.4f}")
