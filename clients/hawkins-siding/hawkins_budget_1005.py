# ALREADY APPLIED LIVE 2026-10-05. Kept for the record. Do NOT re-run with --apply (it would try to repeat the change).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), 2026-10-05: small budget-neutral shift, approved by Edu in chat
("do that budget shift you recommended, but a small one"). Account daily total unchanged ($93/d).
  TSD_04.29_Leads_Nonbranded_Evergreen (23805382277): $80 -> $75/day  (averaged ~$65/d spend last 7d)
  TSD_Pmax_Siding (21291552209):                      $13 -> $18/day  (capped, $29 CPL vs $76 on Nonbranded)
Aborts if either budget is shared or the current amounts are not what we expect.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "2198608170"
PLAN = {"23805382277": (80.0, 75.0), "21291552209": (13.0, 18.0)}
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")


def read():
    out = {}
    for r in ga.search(customer_id=CID, query=f"""SELECT campaign.id, campaign.name, campaign.status, campaign_budget.resource_name,
            campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
            FROM campaign WHERE campaign.id IN ({','.join(PLAN)})"""):
        out[str(r.campaign.id)] = r
    return out


before = read()
ops = []
for cid, (old, new) in PLAN.items():
    r = before[cid]
    cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name} [{r.campaign.status.name}]: ${cur:.2f}/d shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1:
        sys.exit(f"ABORT: budget for {cid} is shared")
    if abs(cur - old) > 0.01:
        sys.exit(f"ABORT: {cid} budget is ${cur:.2f}, expected ${old:.2f}")
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = r.campaign_budget.resource_name
    op.update.amount_micros = int(new * 1_000_000)
    op.update_mask.paths.append("amount_micros")
    ops.append(op)

client.get_service("CampaignBudgetService").mutate_campaign_budgets(
    request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"mutate ok{'' if APPLY else ' (validate_only)'}")

if APPLY:
    print("--- read-back")
    after = read()
    total = 0
    for cid, (old, new) in PLAN.items():
        cur = after[cid].campaign_budget.amount_micros / 1e6
        total += cur
        print(f"   {after[cid].campaign.name}: ${cur:.2f}/d (target ${new:.2f}) {'OK' if abs(cur - new) < 0.01 else 'MISMATCH'}")
    print(f"   total of the two: ${total:.2f}/d (was $93.00)")
