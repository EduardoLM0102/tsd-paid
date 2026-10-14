# ALREADY APPLIED LIVE 2026-10-09 (keyword pauses). Re-running --apply is harmless (sets PAUSED again) but unnecessary.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-09. Approved by Edu in chat: revive the Feb PMax within the current budget,
trim Nonbranded as suggested. Taps ([TSD] Click to call) keep counting (Edu: they might generate calls).

APPLIED: Nonbranded 23828098448, pause 'licensed ac repair', 'air conditioning repair service', 'annual ac maintenance'
($963 / 30d, 0 conv).

BLOCKED by Google (validate_only), so the Feb PMax 23584282933 can't be revived in place:
  - its budget is a $3,000 CUSTOM_PERIOD total; swapping in a DAILY budget -> CANNOT_CHANGE_BUDGET_PERIOD + IMMUTABLE_FIELD
  - keeping it and moving the end date (2026-03-31 -> 2026-11-13) -> "Duration too long for total budget"
    (duration counts from the original 2026-02-18 start)
  Path instead: copy the campaign in the UI with a $30/d daily budget; then NB budget $55 -> $25 (constant total).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, PMAX = "5563867754", "23828098448", "23584282933"
NB_BUDGET = "15562672299"
KWS = [("197197281278", "326155282700", "licensed ac repair"),
       ("197197281278", "1425607556", "air conditioning repair service"),
       ("194069608017", "297465191423", "annual ac maintenance")]
CALL_ASSET = "343525874146"
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
ops = []

for ag, crit, _ in KWS:
    mo = client.get_type("MutateOperation")
    u = mo.ad_group_criterion_operation.update
    u.resource_name = ga.ad_group_criterion_path(CID, ag, crit)
    u.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    mo.ad_group_criterion_operation.update_mask.paths.append("status")
    ops.append(mo)

resp = ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"batch of {len(ops)} ops: {'APPLIED' if APPLY else 'validate_only OK'}")
if not APPLY:
    sys.exit(0)

print("--- read-back")
for r in ga.search(customer_id=CID, query=f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion
        WHERE campaign.id = {NB} AND ad_group_criterion.criterion_id IN ({','.join(k[1] for k in KWS)})"""):
    print(f"   kw '{r.ad_group_criterion.keyword.text}': {r.ad_group_criterion.status.name}")
