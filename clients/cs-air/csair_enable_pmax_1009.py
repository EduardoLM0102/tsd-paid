# ALREADY APPLIED LIVE 2026-10-09. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-09. Turns on the PMax copy and funds it within the current budget, one atomic batch:
  1) new PMax 24336822932: SIGNUP/WEBSITE goal non-biddable (GA4 "Sign Up", not a lead). Keeps PHONE_CALL_LEAD/CALL_FROM_ADS
     (taps stay counted, Edu), SUBMIT_LEAD_FORM/WEBSITE (forms) and DEFAULT/WEBSITE (CallRail calls) biddable.
  2) new PMax 24336822932: PAUSED -> ENABLED ($30/d)
  3) Nonbranded 23828098448 budget 15562672299: $55 -> $25/d  (net: account total unchanged)
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NEW, NB_BUDGET = "5563867754", "24336822932", "15562672299"
APPLY = "--apply" in sys.argv
client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
ops = []

m = client.get_type("MutateOperation")
g = m.campaign_conversion_goal_operation.update
g.resource_name = f"customers/{CID}/campaignConversionGoals/{NEW}~SIGNUP~WEBSITE"
g.biddable = False
m.campaign_conversion_goal_operation.update_mask.paths.append("biddable")
ops.append(m)

m = client.get_type("MutateOperation")
c = m.campaign_operation.update
c.resource_name = ga.campaign_path(CID, NEW)
c.status = E.CampaignStatusEnum.ENABLED
m.campaign_operation.update_mask.paths.append("status")
ops.append(m)

m = client.get_type("MutateOperation")
b = m.campaign_budget_operation.update
b.resource_name = ga.campaign_budget_path(CID, NB_BUDGET)
b.amount_micros = 25_000_000
m.campaign_budget_operation.update_mask.paths.append("amount_micros")
ops.append(m)

ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"batch of {len(ops)} ops: {'APPLIED' if APPLY else 'validate_only OK'}")
if APPLY:
    for r in ga.search(customer_id=CID, query=f"""SELECT campaign.name, campaign.status, campaign.primary_status, campaign_budget.amount_micros
            FROM campaign WHERE campaign.id IN ({NEW}, 23828098448)"""):
        print(f"   {r.campaign.name[:42]:42s} {r.campaign.status.name} {r.campaign.primary_status.name} ${r.campaign_budget.amount_micros/1e6:.0f}/d")
    print("   biddable goals new PMax:", sorted(f"{r.campaign_conversion_goal.category.name}/{r.campaign_conversion_goal.origin.name}"
          for r in ga.search(customer_id=CID, query=f"""SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin
          FROM campaign_conversion_goal WHERE campaign.id = {NEW} AND campaign_conversion_goal.biddable = TRUE""")))
