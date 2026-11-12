# APPLIED LIVE 2026-10-21 on Edu's go ("yes, apply 1 and 2"). Do NOT re-run with --apply (portfolio name guard aborts anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), from the 10-21 recheck of the 10-14 changes (Command Center fu-050), Edu: "yes, apply 1 and 2".
1. Branded 23233882685: ad group default max CPC $5 -> $6 (lost 37% of brand IS to rank) and budget $7 -> $10/d,
   funded by Nonbranded 23805382277 $70 -> $67/d (constant $100/d total incl. PMax $23).
2. Nonbranded bid ceiling: from standard Maximize Conversions (no cap; ~$20 CPC and single clicks of $30-40 after the
   10-19 phrase switch) to a portfolio Maximize Conversions with a $15 max CPC ceiling (avg CPC was $11.76 on 10-06..10-12).
Aborts on shared budgets, unexpected current values, keyword-level bid overrides on Branded, or a portfolio already on NB.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, BR = "2198608170", "23805382277", "23233882685"
BUDGETS = {NB: (70.0, 67.0), BR: (7.0, 10.0)}
BR_BID_OLD, BR_BID = 5.0, 6.0
NB_CEILING = 15.0
PORTFOLIO_NAME = "TSD_Hawkins_NB_MaxConv_CPC15"
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
bud = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared, campaign_budget.reference_count FROM campaign WHERE campaign.id IN ({NB},{BR})""")}
for cid, (old, new) in BUDGETS.items():
    r = bud[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: ${cur:.2f}/d shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")

ags = q(f"SELECT ad_group.resource_name, ad_group.name, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id = {BR} AND ad_group.status = 'ENABLED'")
print(f"Branded ad groups: {[(a.ad_group.name, a.ad_group.cpc_bid_micros/1e6) for a in ags]}")
if not ags or any(abs(a.ad_group.cpc_bid_micros/1e6 - BR_BID_OLD) > 0.01 for a in ags): sys.exit("ABORT: Branded ad group bid not at $5")
kw_over = [(r.ad_group_criterion.keyword.text, r.ad_group_criterion.cpc_bid_micros/1e6) for r in q(f"""SELECT ad_group_criterion.keyword.text,
    ad_group_criterion.cpc_bid_micros FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""") if r.ad_group_criterion.cpc_bid_micros]
print(f"Branded keyword-level bid overrides: {kw_over}")
if kw_over: sys.exit("ABORT: keyword-level bids would ignore the ad group bid")

nb = q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.maximize_conversions.target_cpa_micros
    FROM campaign WHERE campaign.id = {NB}""")[0]
print(f"NB: {nb.campaign.bidding_strategy_type.name} portfolio='{nb.campaign.bidding_strategy}' tCPA={nb.campaign.maximize_conversions.target_cpa_micros/1e6}")
if nb.campaign.bidding_strategy or nb.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: NB not on standard Max Conversions")
tcpa = nb.campaign.maximize_conversions.target_cpa_micros
dupe = q(f"SELECT bidding_strategy.resource_name FROM bidding_strategy WHERE bidding_strategy.name = '{PORTFOLIO_NAME}'")
if dupe: sys.exit(f"ABORT: portfolio {PORTFOLIO_NAME} already exists")

# --- 1. budgets + Branded bid
ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = bud[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

ops = []
for a in ags:
    op = client.get_type("AdGroupOperation")
    op.update.resource_name = a.ad_group.resource_name
    op.update.cpc_bid_micros = int(BR_BID * 1e6); op.update_mask.paths.append("cpc_bid_micros"); ops.append(op)
client.get_service("AdGroupService").mutate_ad_groups(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("branded bid ok", "(validate_only)" if vo else "APPLIED")

# --- 2. NB portfolio Max Conversions with CPC ceiling
op = client.get_type("BiddingStrategyOperation"); bs = op.create
bs.name = PORTFOLIO_NAME
bs.maximize_conversions.cpc_bid_ceiling_micros = int(NB_CEILING * 1e6)
if tcpa: bs.maximize_conversions.target_cpa_micros = tcpa
res = client.get_service("BiddingStrategyService").mutate_bidding_strategies(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("portfolio create ok", "(validate_only)" if vo else "APPLIED")
if APPLY:
    rn = res.results[0].resource_name
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, NB); op.update.bidding_strategy = rn
    op.update_mask.paths.append("bidding_strategy")
    client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op]})
    print("NB moved to portfolio APPLIED:", rn)

    print("--- read-back")
    for r in q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.primary_status, campaign_budget.amount_micros
            FROM campaign WHERE campaign.id IN ({NB},{BR},21291552209)"""):
        print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} "
              f"{r.campaign.bidding_strategy} {r.campaign.primary_status.name}")
    for r in q(f"SELECT ad_group.name, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id = {BR} AND ad_group.status = 'ENABLED'"):
        print(f"   Branded ad group {r.ad_group.name}: max CPC ${r.ad_group.cpc_bid_micros/1e6:.2f}")
    for r in q(f"""SELECT bidding_strategy.name, bidding_strategy.type, bidding_strategy.maximize_conversions.cpc_bid_ceiling_micros,
            bidding_strategy.maximize_conversions.target_cpa_micros, bidding_strategy.campaign_count FROM bidding_strategy WHERE bidding_strategy.name = '{PORTFOLIO_NAME}'"""):
        b = r.bidding_strategy
        print(f"   portfolio {b.name}: {b.type_.name} ceiling ${b.maximize_conversions.cpc_bid_ceiling_micros/1e6:.2f} "
              f"tCPA ${b.maximize_conversions.target_cpa_micros/1e6:.2f} campaigns={b.campaign_count}")
