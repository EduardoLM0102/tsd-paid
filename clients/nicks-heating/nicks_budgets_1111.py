# APPLIED LIVE 2026-11-11 10:22 BRT (Edu: "Execute 1 to 3"), read-back NB $40.00, Branded $85.00. Do NOT re-run with --apply (aborts: budgets no longer $25 / $100).
"""Nick's (1854100356): fund the new Heating Repair ad group.
Nonbranded 23821497590 $25 -> $40/day; Branded 23675600637 $100 -> $85/day (Branded spends ~$5/day, so the account's total caps stay at
the same figure and no client approval is needed). PMax stays $50 (passes its rule, 48% lost to budget).
Aborts unless NB is at $25 and Branded at $100, both unshared."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "1854100356"
JOBS = [("Nonbranded", "23821497590", 25.00, 40.00), ("Branded", "23675600637", 100.00, 85.00)]
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

ops, plan = [], []
for name, camp, expect, new in JOBS:
    b = q(f"SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id = {camp}")[0].campaign_budget
    now = b.amount_micros / 1e6
    print(f"{name}: budget now ${now:.2f} shared={b.explicitly_shared} -> ${new:.2f}")
    if b.explicitly_shared or abs(now - expect) > 0.01:
        sys.exit(f"ABORT: {name} budget is not ${expect:.2f} or is shared")
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = b.resource_name; op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros")
    ops.append(op); plan.append((name, camp, new))
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print("budgets ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    for name, camp, new in plan:
        print(f"  read-back {name}: ${q(f'SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = {camp}')[0].campaign_budget.amount_micros / 1e6:.2f}")
