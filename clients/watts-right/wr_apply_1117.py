# APPLIED LIVE 2026-11-17 09:09 -03, read-back confirmed (Branded $60, NB $405 tCPA $110, 3 negs present). Do NOT re-run with --apply.
# Watt's Right (3651667805), 2026-11-17. Edu's go in-session: "Apply 1 and 2" (fu-175 revised proposals).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""1. Branded 23690645223 budget $145 -> $60/d (spends ~$40/d at IS 96%; cap keeps headroom for busy brand days).
2. Nonbranded 23832838033 budget $320 -> $405/d (brand's unspent $105 minus the $20 kept on Branded; tCPA $110 UNCHANGED).
   PPC total $465/d unchanged (same constant-total rule as 11-10). Stop rule: real CPL > $200 at 11-24 -> back to $320.
3. Nonbranded campaign PHRASE negatives (skips any already present): fireplace, commercial, parking lot. 90d: 0 real leads, no live-kw conflicts.
Aborts on shared budgets / unexpected current values."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, NB = "3651667805", "23690645223", "23832838033"
BR_OLD, BR_NEW, NB_OLD, NB_NEW = 145.0, 60.0, 320.0, 405.0
NEGS = ["fireplace", "commercial", "parking lot"]
APPLY = "--apply" in sys.argv; vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

rows = {r.campaign.id: r for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type,
    campaign.maximize_conversions.target_cpa_micros, campaign_budget.resource_name, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared, campaign_budget.reference_count FROM campaign WHERE campaign.id IN ({BR},{NB})""")}
ops = []
for cid, old, new in ((int(BR), BR_OLD, BR_NEW), (int(NB), NB_OLD, NB_NEW)):
    r = rows[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: {r.campaign.status.name} {r.campaign.bidding_strategy_type.name} tCPA ${r.campaign.maximize_conversions.target_cpa_micros/1e6:.0f} "
          f"| ${cur:.2f}/d -> ${new:.2f}/d shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit("ABORT: shared budget")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: budget ${cur:.2f}, expected ${old:.2f}")
    if r.campaign.status.name != "ENABLED": sys.exit("ABORT: campaign not ENABLED")
    op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = r.campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
nb = rows[int(NB)]
if abs(nb.campaign.maximize_conversions.target_cpa_micros / 1e6 - 110.0) > 0.01: sys.exit("ABORT: NB tCPA is not $110")
print(f"PPC total ${BR_NEW + NB_NEW:.0f}/d (was ${BR_OLD + NB_OLD:.0f}/d)")

have = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
live = {r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")}
conflict = [n for n in NEGS if any(n in k for k in live)]
if conflict: sys.exit(f"ABORT: negative inside a live keyword: {conflict}")
todo = [n for n in NEGS if n not in have]
print("negatives already present:", [n for n in NEGS if n in have], "| to add:", todo, "| live-kw conflicts: none")

client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")
if todo:
    MT = client.enums.KeywordMatchTypeEnum; cops = []
    for t in todo:
        o = client.get_type("CampaignCriterionOperation"); c = o.create
        c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; cops.append(o)
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": cops, "validate_only": vo})
    print(f"negatives ({len(cops)}) ok", "(validate_only)" if vo else "APPLIED")
if APPLY:
    print("READ-BACK:")
    for r in q(f"""SELECT campaign.name, campaign.status, campaign_budget.amount_micros, campaign.maximize_conversions.target_cpa_micros FROM campaign WHERE campaign.id IN ({BR},{NB})"""):
        print(f"   {r.campaign.name}: {r.campaign.status.name} ${r.campaign_budget.amount_micros/1e6:.2f}/d tCPA ${r.campaign.maximize_conversions.target_cpa_micros/1e6:.0f}")
    have = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
        FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("   negatives missing:", [n for n in NEGS if (n, "PHRASE") not in have])
