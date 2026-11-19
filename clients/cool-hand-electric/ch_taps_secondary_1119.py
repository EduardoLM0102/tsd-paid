# Run from google-ads-ratos/scripts: ./tsd.sh <abs path> [--apply]
"""Cool Hand 9865206319 (Edu 11-19: "Move the taps to secondary"). 'Click to call' 7716560298 (CLICK_TO_CALL = taps on the ad call
button, PHONE_CALL_LEAD / CALL_FROM_ADS, same goal as 'Calls from ads') -> Secondary (primary_for_goal False), account-wide.
The goal itself stays biddable (it also holds 'Calls from ads'). Other taps ('Clicks to call' CONTACT, 'Phone Call' DEFAULT, Local actions)
sit in goals that are NOT biddable on the Search campaigns, so they don't steer bidding; left as is.
Rollback: primary_for_goal True on 7716560298."""
import sys; sys.path.insert(0, ".")
from lib import init_client
from google.protobuf import field_mask_pb2
CID, AID = "9865206319", "7716560298"
APPLY = "--apply" in sys.argv
c = init_client(); ga = c.get_service("GoogleAdsService")
SEL = f"SELECT conversion_action.name, conversion_action.type, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.id = {AID}"
a = list(ga.search(customer_id=CID, query=SEL))[0].conversion_action
print(f"before: {a.name} {a.type_.name} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
if a.type_.name != "CLICK_TO_CALL": sys.exit("ABORT: not the tap action")
if a.primary_for_goal:
    op = c.get_type("ConversionActionOperation")
    op.update.resource_name = f"customers/{CID}/conversionActions/{AID}"; op.update.primary_for_goal = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))
    c.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
    print("APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    a = list(ga.search(customer_id=CID, query=SEL))[0].conversion_action
    print(f"after: primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
