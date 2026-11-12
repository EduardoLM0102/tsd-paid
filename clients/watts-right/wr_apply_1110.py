# APPLIED LIVE 2026-11-10 09:13 -03, read-back confirmed. Do NOT re-run with --apply.
# Watt's Right (3651667805), 2026-11-10. Edu's go in-session: "Kill pmax / Move the $95 from pmax to branded / Add(ed) the phrase negatives".
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""1. PMax 23833205176 -> PAUSED (fu-119: 4 ad calls transcribed = 0 new customers, 11-04..11-09).
2. Branded 23690645223 budget $50 -> $95/d (PMax's $95; Branded $22 CPL, budget-lost 57%). PPC total unchanged.
3. Nonbranded 23832838033 campaign PHRASE negatives (skips any already present): rocky electric, catale electric, arnold electric,
   oklahoma generator, magnum electric, generator supercenter. Replay 11-10: $135/30d, 0 conv, no live-kw conflicts.
Aborts on shared budget / unexpected current values."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, NB, PM = "3651667805", "23690645223", "23832838033", "23833205176"
OLD, NEW = 50.0, 95.0
NEGS = ["rocky electric", "catale electric", "arnold electric", "oklahoma generator", "magnum electric", "generator supercenter"]
APPLY = "--apply" in sys.argv; vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

pm = q(f"SELECT campaign.name, campaign.status, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {PM}")[0]
print(f"PMax {pm.campaign.name}: {pm.campaign.status.name} ${pm.campaign_budget.amount_micros/1e6:.2f}/d")
br = q(f"""SELECT campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared,
    campaign_budget.reference_count FROM campaign WHERE campaign.id = {BR}""")[0]
cur = br.campaign_budget.amount_micros / 1e6
print(f"Branded {br.campaign.name}: ${cur:.2f}/d -> ${NEW:.2f}/d shared={br.campaign_budget.explicitly_shared} refs={br.campaign_budget.reference_count}")
if br.campaign_budget.explicitly_shared or br.campaign_budget.reference_count > 1: sys.exit("ABORT: Branded budget shared")
if abs(cur - OLD) > 0.01: sys.exit(f"ABORT: Branded budget ${cur:.2f}, expected ${OLD:.2f}")
have = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
todo = [n for n in NEGS if n not in have]
print("negatives already present:", [n for n in NEGS if n in have], "| to add:", todo)

op = client.get_type("CampaignOperation"); op.update.resource_name = ga.campaign_path(CID, PM)
op.update.status = client.enums.CampaignStatusEnum.PAUSED; op.update_mask.paths.append("status")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("PMax pause ok", "(validate_only)" if vo else "APPLIED")
op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = br.campaign_budget.resource_name
op.update.amount_micros = int(NEW * 1e6); op.update_mask.paths.append("amount_micros")
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("Branded budget ok", "(validate_only)" if vo else "APPLIED")
if todo:
    MT = client.enums.KeywordMatchTypeEnum; ops = []
    for t in todo:
        o = client.get_type("CampaignCriterionOperation"); c = o.create
        c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(o)
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
    print(f"negatives ({len(ops)}) ok", "(validate_only)" if vo else "APPLIED")
if APPLY:
    print("READ-BACK:")
    for r in q(f"""SELECT campaign.name, campaign.status, campaign_budget.amount_micros FROM campaign WHERE campaign.id IN ({BR},{NB},{PM})"""):
        print(f"   {r.campaign.name}: {r.campaign.status.name} ${r.campaign_budget.amount_micros/1e6:.2f}/d")
    have = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("   negatives missing:", [n for n in NEGS if n not in have])
