# ALREADY APPLIED LIVE 2026-10-09. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-09. Edu: "make whatever is needed to keep the same ad spend, reallocate, pause -
whatever. Of course, in a clever way." Restores this morning's $238/d budget total (Smart $80 + NB $55 + Branded $80 +
LSA $23) after the Smart pause, putting the Smart's $80 into the new PMax:
  1) new PMax 24336822932 budget $30 -> $110/d   (new total: PMax 110 + NB 25 + Branded 80 + LSA 23 = $238)
  2) new PMax geo: + the 9 other service-area locations Branded/Nonbranded already target (was Mansfield only), PRESENCE
  3) Branded 23653583753 target-IS CPC ceiling $10 -> $15 (14d: IS 77%, 23% lost to rank, avg CPC $6.92)
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, PMAX, NB, BR = "5563867754", "24336822932", "23828098448", "23653583753"
APPLY = "--apply" in sys.argv
client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums

budget = next(iter(ga.search(customer_id=CID, query=f"SELECT campaign_budget.resource_name FROM campaign WHERE campaign.id = {PMAX}"))).campaign_budget.resource_name
have = {r.campaign_criterion.location.geo_target_constant for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.location.geo_target_constant
        FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.type = 'LOCATION'""")}
want = [r.campaign_criterion.location.geo_target_constant for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.location.geo_target_constant
        FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE""")]
add = [g for g in want if g not in have]
print(f"PMax budget {budget}; locations to add: {len(add)}")

ops = []
m = client.get_type("MutateOperation")
m.campaign_budget_operation.update.resource_name = budget
m.campaign_budget_operation.update.amount_micros = 110_000_000
m.campaign_budget_operation.update_mask.paths.append("amount_micros")
ops.append(m)
for g in add:
    m = client.get_type("MutateOperation")
    m.campaign_criterion_operation.create.campaign = ga.campaign_path(CID, PMAX)
    m.campaign_criterion_operation.create.location.geo_target_constant = g
    ops.append(m)
m = client.get_type("MutateOperation")
m.campaign_operation.update.resource_name = ga.campaign_path(CID, BR)
m.campaign_operation.update.target_impression_share.cpc_bid_ceiling_micros = 15_000_000
m.campaign_operation.update_mask.paths.append("target_impression_share.cpc_bid_ceiling_micros")
ops.append(m)

ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"batch of {len(ops)} ops: {'APPLIED' if APPLY else 'validate_only OK'}")
if APPLY:
    tot = 0
    for r in ga.search(customer_id=CID, query="""SELECT campaign.name, campaign.status, campaign.primary_status, campaign_budget.amount_micros,
            campaign.target_impression_share.cpc_bid_ceiling_micros FROM campaign WHERE campaign.status = 'ENABLED'"""):
        b = r.campaign_budget.amount_micros / 1e6
        if r.campaign.primary_status.name != "ENDED": tot += b
        print(f"   {r.campaign.name[:42]:42s} {r.campaign.primary_status.name:10s} ${b:.0f}/d"
              + (f" cpc ceiling ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.0f}" if r.campaign.target_impression_share.cpc_bid_ceiling_micros else ""))
    print(f"   serving budget total: ${tot:.0f}/d")
    n = [r.campaign_criterion.location.geo_target_constant for r in ga.search(customer_id=CID, query=f"""SELECT campaign_criterion.location.geo_target_constant
         FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.type = 'LOCATION'""")]
    print(f"   PMax locations: {len(n)}")
