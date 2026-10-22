# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), 2026-10-22, Edu: "Make it not count the BCJ stuff. Let's keep the Click to call we created as secondary".
Sets primary_for_goal = False (secondary: still recorded under All conversions, not in Conversions) on the old agency's
website/form/chat actions + '[TSD] Click to call'. '[TSD} Submit lead form' stays primary. 'Calls From Ads (BCJ)' 6959959574
(the account's call reporting action for call assets) is NOT touched here: decided separately.
"""
import sys
sys.path.insert(0, ".")
from google.protobuf.field_mask_pb2 import FieldMask
from lib import init_client

CID = "9215192296"
APPLY = "--apply" in sys.argv
SECONDARY = {"6959959571": "Calls From Website - SC (BCJ)", "6960158572": "Calls From Website - MS (BCJ)",
             "7404522862": "Calls From Website - GA (BCJ)", "6959959577": "Lead Form Submission (BCJ)",
             "6960159274": "Chat Lead (BCJ)", "7861943916": "[TSD] Click to call"}
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
cur = {str(r.conversion_action.id): r.conversion_action for r in q(f"""SELECT conversion_action.id, conversion_action.name,
    conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.id IN ({",".join(SECONDARY)})""")}
for i, n in SECONDARY.items():
    if i not in cur or cur[i].name != n: sys.exit(f"ABORT: {i} is not '{n}'")
ops = []
for i in SECONDARY:
    if not cur[i].primary_for_goal: continue
    op = client.get_type("ConversionActionOperation")
    op.update.resource_name = ga.conversion_action_path(CID, i); op.update.primary_for_goal = False
    client.copy_from(op.update_mask, FieldMask(paths=["primary_for_goal"])); ops.append(op)
print(f"{len(ops)} to secondary, {'APPLYING' if APPLY else 'validate_only'}")
if ops: client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print("OK")
if APPLY:
    for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.primary_for_goal, conversion_action.phone_call_duration_seconds
            FROM conversion_action WHERE conversion_action.status = 'ENABLED' AND conversion_action.primary_for_goal = TRUE"""):
        a = r.conversion_action; print(f"   still primary: {a.id} {a.name}")
