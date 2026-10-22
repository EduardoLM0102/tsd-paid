# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), 2026-10-22, Edu chose "Google native, 60s": 'Calls From Ads (BCJ)' 6959959574 (the account's
call reporting action, counts call-asset calls via Google forwarding numbers) -> renamed '[TSD] Calls from ads (60s)', threshold
10s -> 60s, stays primary. Website calls will come from Edu's CallRail integration (needs the swap script on the go. pages)."""
import sys
sys.path.insert(0, ".")
from google.protobuf.field_mask_pb2 import FieldMask
from lib import init_client

CID, AID, NEW = "9215192296", "6959959574", "[TSD] Calls from ads (60s)"
APPLY = "--apply" in sys.argv
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
a = q(f"SELECT conversion_action.name, conversion_action.phone_call_duration_seconds, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.id = {AID}")[0].conversion_action
print(f"now: {a.name} {a.phone_call_duration_seconds}s primary={a.primary_for_goal}")
if a.name != "Calls From Ads (BCJ)": sys.exit("ABORT: unexpected name")
op = client.get_type("ConversionActionOperation")
op.update.resource_name = ga.conversion_action_path(CID, AID); op.update.name = NEW; op.update.phone_call_duration_seconds = 60
client.copy_from(op.update_mask, FieldMask(paths=["name", "phone_call_duration_seconds"]))
client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("OK", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    a = q(f"SELECT conversion_action.name, conversion_action.phone_call_duration_seconds, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.id = {AID}")[0].conversion_action
    print(f"   after: {a.name} {a.phone_call_duration_seconds}s primary={a.primary_for_goal}")
    s = q("SELECT customer.call_reporting_setting.call_conversion_action FROM customer")[0].customer.call_reporting_setting.call_conversion_action
    print(f"   account call reporting action: {s}")
