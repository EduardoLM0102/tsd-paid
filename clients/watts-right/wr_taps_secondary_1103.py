# APPLIED LIVE 2026-11-03 on Edu's go ("Taps to secondary"), read-back: primary=False in_conversions=False. Undo = same script with primary_for_goal True.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Watt's Right (3651667805), 2026-11-03 (fu-098). Take `[TSD] Click to call` (7835456094, CLICK_TO_CALL = taps on the ad's call button)
out of bidding for good, account-wide: primary_for_goal True -> False (Secondary). It keeps reporting under All conversions (Command Center
funnel reads all_conversions). The 10-27 custom goal didn't do it: a goal with `Calls from ads` pulls in the whole PHONE_CALL_LEAD /
CALL_FROM_ADS bucket. ⚠ tsd-google-conversion-goals-mechanics says primary_for_goal writes once did nothing on GC, so the read-back checks
include_in_conversions_metric too, and the real proof is conversions vs all_conversions on the next days.
"""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, TAP = "3651667805", "7835456094"
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = f"""SELECT conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.primary_for_goal,
    conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.id = {TAP}"""

a = q(SEL)[0].conversion_action
print(f"before: {a.name} {a.type_.name} {a.status.name} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
if a.type_.name != "CLICK_TO_CALL" or a.status.name != "ENABLED": sys.exit("ABORT: unexpected action")
if not a.primary_for_goal: sys.exit("already Secondary, nothing to do")

op = client.get_type("ConversionActionOperation")
op.update.resource_name = ga.conversion_action_path(CID, TAP)
op.update.primary_for_goal = False
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))  # explicit mask: the helper drops falsy values
client.get_service("ConversionActionService").mutate_conversion_actions(
    request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("primary_for_goal -> False", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")

if APPLY:
    a = q(SEL)[0].conversion_action
    print(f"read-back: primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
