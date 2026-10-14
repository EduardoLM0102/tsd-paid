# APPLIED LIVE 2026-10-14 on Edu's go ("For Hawkins, go as well - execute whatever we need to execute"). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), staged in the 10-13 weekly pass (AT task 133e8c07, Command Center fu-044):
1. Budget step, constant $93/d total: PMax 21291552209 $18 -> $23/d, Nonbranded 23805382277 $75 -> $70/d.
2. Brand fix (together): 'hawkins' PHRASE negative on Nonbranded + Branded 23233882685 from Max Conversions
   ($25 tCPA, 1 impression in 30d) to Manual CPC (no enhanced CPC), ad group default bid $5.
3. Nonbranded PHRASE negatives: 'charities', 'in stock'.
Aborts on shared budgets / unexpected current values; replays negatives against 30d converting search terms first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, PMAX, BR = "2198608170", "23805382277", "21291552209", "23233882685"
BUDGETS = {NB: (75.0, 70.0), PMAX: (18.0, 23.0)}
NEG = ["hawkins", "charities", "in stock"]
BR_BID = 5.0
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
bud = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared, campaign_budget.reference_count FROM campaign WHERE campaign.id IN ({NB},{PMAX})""")}
for cid, (old, new) in BUDGETS.items():
    r = bud[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: ${cur:.2f}/d shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")

br = q(f"SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy FROM campaign WHERE campaign.id = {BR}")[0]
print(f"Branded: {br.campaign.name} {br.campaign.bidding_strategy_type.name} portfolio='{br.campaign.bidding_strategy}'")
if br.campaign.bidding_strategy: sys.exit("ABORT: Branded uses a portfolio strategy")
ags = q(f"SELECT ad_group.resource_name, ad_group.name, ad_group.status, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id = {BR} AND ad_group.status = 'ENABLED'")
ads = q(f"SELECT ad_group_ad.status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = {BR} AND ad_group_ad.status = 'ENABLED'")
print(f"Branded enabled ad groups: {[(a.ad_group.name, a.ad_group.cpc_bid_micros/1e6) for a in ags]}; enabled ads: {[a.ad_group_ad.policy_summary.approval_status.name for a in ads]}")
if not ags or not ads: sys.exit("ABORT: Branded has no enabled ad group / ad")

# --- safety replay of negatives on Nonbranded (30d)
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
for n in NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    print(f"neg '{n}': blocks {len(hit)} terms, ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f}, conv {sum(r.metrics.conversions for r in hit):.1f}; "
          f"active kw conflicts: {[k for k in kws if f' {n} ' in f' {k} ']}")

# --- mutations
vo = not APPLY
ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = bud[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, BR)
op.update.manual_cpc.enhanced_cpc_enabled = False
op.update_mask.paths.append("manual_cpc.enhanced_cpc_enabled")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("branded bidding ok", "(validate_only)" if vo else "APPLIED")

if APPLY:  # ad group bid only valid once the campaign is on Manual CPC
    ops = []
    for a in ags:
        op = client.get_type("AdGroupOperation")
        op.update.resource_name = a.ad_group.resource_name
        op.update.cpc_bid_micros = int(BR_BID * 1e6); op.update_mask.paths.append("cpc_bid_micros"); ops.append(op)
    client.get_service("AdGroupService").mutate_ad_groups(request={"customer_id": CID, "operations": ops})
    print("branded ad group bid APPLIED")

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in NEG:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("negatives ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, campaign_budget.amount_micros
            FROM campaign WHERE campaign.id IN ({NB},{PMAX},{BR})"""):
        print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name}")
    for r in q(f"SELECT ad_group.name, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.id = {BR} AND ad_group.status = 'ENABLED'"):
        print(f"   Branded ad group {r.ad_group.name}: max CPC ${r.ad_group.cpc_bid_micros/1e6:.2f}")
    got = {r.campaign_criterion.keyword.text for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives present: {[n for n in NEG if n in got]} missing: {[n for n in NEG if n not in got]}")
