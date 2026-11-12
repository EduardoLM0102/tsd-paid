# APPLIED LIVE 2026-11-04, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Make the campaigns bid only on real calls"), Command Center fu-126.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Proud Pops (1051843378), 2026-11-04: bidding on real leads only, now that CallRail uploads land in this account.
→ Secondary (primary_for_goal False; they keep reporting under All conversions):
   'TSD - Website Call' 7667749854  CLICK_TO_CALL = taps on the ad's call button (483 of ~517 conv in 30d)
   'Repeat Phone Call'  7889536740  CallRail upload, existing customers
   'Phone Call'         7238068273  leftover CallRail upload action from the old setup
Stays primary: 'First Time Phone Call' 7889536968 (CallRail, 60s), counting MANY_PER_CLICK → ONE_PER_CLICK;
   'Calls from ads' 6569241485 (60s); 'Website lead' 6562304397 (customer forms; careers excluded since GTM v43, 10-08)."""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID = "1051843378"
SECONDARY = {7667749854: "TSD - Website Call", 7889536740: "Repeat Phone Call", 7238068273: "Phone Call"}
FIRST_TIME = (7889536968, "First Time Phone Call")
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))
ids = list(SECONDARY) + [FIRST_TIME[0]]
SEL = f"""SELECT conversion_action.id, conversion_action.name, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
    conversion_action.counting_type, conversion_action.status FROM conversion_action WHERE conversion_action.id IN ({','.join(map(str, ids))})"""

rows = {r.conversion_action.id: r.conversion_action for r in q(SEL)}
for i, name in list(SECONDARY.items()) + [FIRST_TIME]:
    a = rows.get(i)
    if not a or a.name != name or a.status.name != "ENABLED": sys.exit(f"ABORT: {i} '{name}' not found as expected")
    print(f"before: {i} {a.name:<24} primary={a.primary_for_goal} in_conv={a.include_in_conversions_metric} counting={a.counting_type.name}")

ops = []
for i in SECONDARY:
    if rows[i].primary_for_goal:
        op = client.get_type("ConversionActionOperation"); op.update.resource_name = ga.conversion_action_path(CID, str(i))
        op.update.primary_for_goal = False
        op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))  # explicit mask: the helper drops falsy values
        ops.append(op)
ft = rows[FIRST_TIME[0]]
if ft.counting_type.name != "ONE_PER_CLICK" or not ft.primary_for_goal:
    op = client.get_type("ConversionActionOperation"); op.update.resource_name = ga.conversion_action_path(CID, str(FIRST_TIME[0]))
    op.update.counting_type = E.ConversionActionCountingTypeEnum.ONE_PER_CLICK
    op.update.primary_for_goal = True
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["counting_type", "primary_for_goal"]))
    ops.append(op)
if ops:
    client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"{len(ops)} op(s)", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")
if APPLY:
    for a in (r.conversion_action for r in q(SEL)):
        print(f"read-back: {a.id} {a.name:<24} primary={a.primary_for_goal} in_conv={a.include_in_conversions_metric} counting={a.counting_type.name}")
