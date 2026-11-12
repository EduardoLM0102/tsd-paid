# APPLIED LIVE 2026-11-02 on Edu's go. Do NOT re-run with --apply (aborts: budget no longer $23.26).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754) LSA budget $23.26 -> $55.00/day, Edu 11-02 "It passed, can you do the budget increase?".
Insurance re-verified 11-02 (reach had collapsed 09-11 on a failed insurance check). Money comes from the spare budget
(PMax $110 + Cooling $25 paused 10-23); account stays inside the $238/day approved total, so no client approval needed.
Aborts unless insurance shows PASSED and the budget is still $23.26 and not shared."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, LSA, NEW = "5563867754", "15794404030", 55.00
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

ins = q("SELECT customer.local_services_settings.granular_insurance_statuses FROM customer")[0].customer.local_services_settings.granular_insurance_statuses
print("insurance:", [(s.category_id, s.verification_status.name) for s in ins])
for r in sorted(q("""SELECT local_services_verification_artifact.creation_date_time, local_services_verification_artifact.status,
    local_services_verification_artifact.artifact_type FROM local_services_verification_artifact"""), key=lambda r: r.local_services_verification_artifact.creation_date_time)[-2:]:
    a = r.local_services_verification_artifact; print("  artifact", a.creation_date_time[:16], a.artifact_type.name, a.status.name)
if not ins or any(s.verification_status.name != "PASSED" for s in ins): sys.exit("ABORT: insurance not PASSED in the API yet")

b = q(f"""SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.period
    FROM campaign WHERE campaign.id = {LSA}""")[0].campaign_budget
print(f"budget now ${b.amount_micros/1e6:.2f} {b.period.name} shared={b.explicitly_shared}")
if b.explicitly_shared or abs(b.amount_micros/1e6 - 23.26) > 0.01: sys.exit("ABORT: budget not $23.26 or shared")

op = client.get_type("CampaignBudgetOperation")
op.update.resource_name = b.resource_name; op.update.amount_micros = int(NEW * 1e6); op.update_mask.paths.append("amount_micros")
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"budget -> ${NEW:.2f}", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    print("read-back:", q(f"SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = {LSA}")[0].campaign_budget.amount_micros / 1e6)
