# APPLIED LIVE 2026-10-21 on Edu's go. Do NOT re-run with --apply (budget guards abort anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Nick's Heating (1854100356), 2026-10-21. The 10-08 checklist (tarefas.md, Command Center fu-005), Edu: "do both the ones you can please".
Fresh read 10-08..10-20: Nonbranded AC $470 / 13 clicks / 0 conv ($36 CPC); PMax $424 / 7 conv ($61 CPL, 32% budget-lost).
1. Nonbranded AC 23821497590: pause PHRASE 'air conditioner repair Louisiana' ($208 / 7 clicks / 0 conv since 10-08);
   PHRASE negatives (competitors that never converted, supply houses / dealers, car AC, out of area, price research);
   bidding from Max Conversions (no target, ~0 conv) to Max Clicks with a $15 max CPC.
2. Branded 23675600637: pause the BROAD non-brand 'hvac contractors near me' (matches competitor names, inflates branded).
3. PMax 23586346547: geo PRESENCE_OR_INTEREST -> PRESENCE.
4. Constant total ($75/d): Nonbranded $40 -> $25/d, PMax $35 -> $50/d.
Competitor 'tropical air kare' converted once in 60d, so it is NOT blocked. Aborts on unexpected state; replays negatives first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, BR, PMAX = "1854100356", "23821497590", "23675600637", "23586346547"
BUDGETS = {NB: (40.0, 25.0), PMAX: (35.0, 50.0)}
NB_CPC_CAP = 15.0
PAUSE = {NB: ("air conditioner repair louisiana", "PHRASE"), BR: ("hvac contractors near me", "BROAD")}
NEG = [
    # competitors (none converted)
    "professional heating", "surgis", "southern air", "drinkard", "one hour", "accutemp", "all in heating", "berthelot",
    "majano", "bruzeau", "precision air", "total maintenance", "benfatti", "peffer",
    # supply houses / dealers / manufacturers
    "ferguson", "supply", "dealer", "dealers", "distributor", "manufacturing",
    # car AC
    "auto", "car",
    # out of area
    "metairie", "new orleans", "nola", "baton rouge", "gonzales", "houma", "zachary", "lockport",
    # research / DIY
    "how much", "price", "why is my", "handyman",
]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
bud = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign.bidding_strategy, campaign.bidding_strategy_type,
    campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count,
    campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id IN ({NB},{PMAX})""")}
for cid, (old, new) in BUDGETS.items():
    r = bud[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: ${cur:.2f}/d shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count} "
          f"bid={r.campaign.bidding_strategy_type.name} geo={r.campaign.geo_target_type_setting.positive_geo_target_type.name}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")
if bud[NB].campaign.bidding_strategy or bud[NB].campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: NB bidding changed")

kw_rows = {}
for cid, (text, mt) in PAUSE.items():
    rows = [r for r in q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
        ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")
        if r.ad_group_criterion.keyword.text.lower() == text and r.ad_group_criterion.keyword.match_type.name == mt]
    print(f"pause '{text}' {mt} in {cid}: {len(rows)} found")
    if len(rows) != 1: sys.exit("ABORT: keyword to pause not found exactly once")
    kw_rows[cid] = rows[0]

# --- safety replay of negatives on NB (60d terms) + conflicts with live NB keywords
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date BETWEEN '2026-08-22' AND '2026-10-20' AND metrics.impressions > 0""")
kws = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
bad = False
for n in NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    conv = sum(r.metrics.conversions for r in hit)
    conflict = [k for k in kws if f" {n} " in f" {k} "]
    print(f"neg '{n}': blocks {len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {conv:.1f} | kw conflicts {conflict}")
    if conv > 0 or conflict: bad = True
if bad: sys.exit("ABORT: a negative blocks a converting term or a live keyword")
neg_new = [n for n in NEG if n not in existing]

# --- mutations
ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = bud[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

ops = []
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.target_spend.cpc_bid_ceiling_micros = int(NB_CPC_CAP * 1e6)
op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros"); ops.append(op)
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, PMAX)
op.update.geo_target_type_setting.positive_geo_target_type = client.enums.PositiveGeoTargetTypeEnum.PRESENCE
op.update_mask.paths.append("geo_target_type_setting.positive_geo_target_type"); ops.append(op)
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("NB Max Clicks $15 + PMax presence ok", "(validate_only)" if vo else "APPLIED")

ops = []
for cid, r in kw_rows.items():
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = r.ad_group_criterion.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("keyword pauses ok", "(validate_only)" if vo else "APPLIED")

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(neg_new)} negatives ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    for r in q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros,
            campaign.geo_target_type_setting.positive_geo_target_type, campaign.primary_status FROM campaign WHERE campaign.id IN ({NB},{BR},{PMAX})"""):
        c = r.campaign
        print(f"   {c.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {c.bidding_strategy_type.name} cap ${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
              f"geo {c.geo_target_type_setting.positive_geo_target_type.name} {c.primary_status.name}")
    for cid, r in kw_rows.items():
        s = q(f"SELECT ad_group_criterion.status FROM ad_group_criterion WHERE ad_group_criterion.resource_name = '{r.ad_group_criterion.resource_name}'")
        print(f"   '{r.ad_group_criterion.keyword.text}': {s[0].ad_group_criterion.status.name}")
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]} (total negatives on NB: {len(got)})")
