# APPLIED LIVE 2026-11-11 10:37 BRT (Edu: "build 2"), read-back OK: 17 brand kws paused in LeadGen, 4 negatives, Branded 24202454875 ENABLED Target IS 90% $5 cap $5/d, LeadGen $17. Do NOT re-run with --apply (aborts: LeadGen not $22).
"""All Seasons AC (4467722415): give brand searches a cheap home. Total Google budget stays $46/day.
1. LeadGen 11803942938: PAUSE the live brand keywords sitting in non-brand ad groups ('all seasons …' in residential hvac / heating repair /
   air conditioning repair; 17 found 11-11). They are why brand clicks cost $11-18 inside Max Conversions.
2. LeadGen + MiniSplit 24050402045: PHRASE negatives 'all seasons', 'all season' (after step 1 there is no live conflict; aborts if one remains).
3. Branded 24202454875 (TSD_08.31_Search_Branded_Evergreen, paused 10-15, 12 brand keywords, approved RSA -> seasonsair.com):
   bidding -> Target Impression Share TOP_OF_PAGE 90% with a $5.00 CPC ceiling, budget $13 -> $5.00/day, status ENABLED.
4. LeadGen budget $22 -> $17 (funds step 3; total $46 unchanged).
Rollback: re-enable the printed keywords, remove the 2 negatives per campaign, Branded -> PAUSED (bidding can stay), LeadGen $22."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, LG, MS, BR = "4467722415", "11803942938", "24050402045", "24202454875"
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

# 1. brand keywords live inside LeadGen non-brand ad groups
rows = q(f"""SELECT ad_group.name, ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM ad_group_criterion WHERE campaign.id = {LG} AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED'
    AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.keyword.text LIKE '%season%'""")
print(f"1. LeadGen live brand keywords to PAUSE: {len(rows)}")
for r in rows: print(f"   {r.ad_group.name[:24]:24s} {r.ad_group_criterion.keyword.text} [{r.ad_group_criterion.keyword.match_type.name[:1]}]")
kw_ops = []
for r in rows:
    op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = r.ad_group_criterion.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status"); kw_ops.append(op)

# 2. negatives, conflict check against live keywords that are NOT in the pause list
pause_rn = {r.ad_group_criterion.resource_name for r in rows}
neg_ops = []
for camp, name in ((LG, "LeadGen"), (MS, "MiniSplit")):
    live = [k for k in q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {camp}
        AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE""")
        if k.ad_group_criterion.resource_name not in pause_rn]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    for n in ("all seasons", "all season"):
        kc = [k.ad_group_criterion.keyword.text for k in live if f" {n} " in f" {k.ad_group_criterion.keyword.text.lower()} "]
        if kc: sys.exit(f"ABORT: '{n}' would block live keywords in {name}: {kc}")
        if n in existing: print(f"2. {name}: '{n}' already a negative"); continue
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, camp); c.negative = True; c.keyword.text = n; c.keyword.match_type = MT.PHRASE; neg_ops.append(op)
    print(f"2. {name}: negatives staged, {len(live)} live keywords checked, no conflict")

# 3. Branded: bidding + budget + status
br = q(f"""SELECT campaign.status, campaign.bidding_strategy_type, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared
    FROM campaign WHERE campaign.id = {BR}""")[0]
print(f"3. Branded now: {br.campaign.status.name} {br.campaign.bidding_strategy_type.name} budget ${br.campaign_budget.amount_micros/1e6:.2f} shared={br.campaign_budget.explicitly_shared}")
if br.campaign_budget.explicitly_shared: sys.exit("ABORT: Branded budget is shared")
c_op = client.get_type("CampaignOperation"); cu = c_op.update
cu.resource_name = ga.campaign_path(CID, BR)
cu.target_impression_share.location = client.enums.TargetImpressionShareLocationEnum.TOP_OF_PAGE
cu.target_impression_share.location_fraction_micros = 900_000
cu.target_impression_share.cpc_bid_ceiling_micros = 5_000_000
cu.status = client.enums.CampaignStatusEnum.ENABLED
c_op.update_mask.paths.extend(["target_impression_share.location", "target_impression_share.location_fraction_micros", "target_impression_share.cpc_bid_ceiling_micros", "status"])
b_ops = []
for rn, new in ((br.campaign_budget.resource_name, 5.00),):
    op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = rn; op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); b_ops.append(op)
# 4. LeadGen budget
lg = q(f"SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id = {LG}")[0].campaign_budget
print(f"4. LeadGen budget now ${lg.amount_micros/1e6:.2f} shared={lg.explicitly_shared} -> $17.00")
if lg.explicitly_shared or abs(lg.amount_micros/1e6 - 22.00) > 0.01: sys.exit("ABORT: LeadGen budget is not $22 or is shared")
op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = lg.resource_name; op.update.amount_micros = 17_000_000; op.update_mask.paths.append("amount_micros"); b_ops.append(op)

req = {"customer_id": CID, "validate_only": vo}
if kw_ops: client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={**req, "operations": kw_ops}); print(f"   keyword pauses ok ({len(kw_ops)})", "(validate_only)" if vo else "APPLIED")
if neg_ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={**req, "operations": neg_ops}); print(f"   negatives ok ({len(neg_ops)})", "(validate_only)" if vo else "APPLIED")
client.get_service("CampaignService").mutate_campaigns(request={**req, "operations": [c_op]}); print("   Branded Target IS 90% top-of-page, $5 cap, ENABLED ok", "(validate_only)" if vo else "APPLIED")
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={**req, "operations": b_ops}); print("   budgets Branded $5 / LeadGen $17 ok", "(validate_only)" if vo else "APPLIED")
if APPLY:
    r = q(f"""SELECT campaign.status, campaign.bidding_strategy_type, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location_fraction_micros, campaign_budget.amount_micros
        FROM campaign WHERE campaign.id = {BR}""")[0]
    print(f"read-back Branded: {r.campaign.status.name} {r.campaign.bidding_strategy_type.name} {r.campaign.target_impression_share.location_fraction_micros/1e4:.0f}% ceil ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.2f} budget ${r.campaign_budget.amount_micros/1e6:.2f}")
    print(f"read-back LeadGen budget: ${q(f'SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = {LG}')[0].campaign_budget.amount_micros/1e6:.2f}")
    left = q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {LG} AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED'
        AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.keyword.text LIKE '%season%'""")
    print(f"read-back LeadGen live brand keywords left: {len(left)}")
    for camp, name in ((LG, "LeadGen"), (MS, "MiniSplit")):
        got = {k.campaign_criterion.keyword.text.lower() for k in q(f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
        print(f"read-back {name} negatives: all seasons={'all seasons' in got} all season={'all season' in got}")
