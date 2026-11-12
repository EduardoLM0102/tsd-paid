# APPLIED LIVE 2026-11-04, read-back confirmed (both primary False, in_conversions False). Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Apply the clean up please"), Command Center fu-031 / fu-111.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Spencer Air (2524618054), 2026-11-04 reporting cleanup, both → Secondary (primary_for_goal False):
- 'Phone Call' 7849678789: leftover CallRail upload action, replaced by First Time / Repeat Phone Call (uploads proven 10-28, 11-02). No conv since 10-19.
- '[TSD] Click to call' (CLICK_TO_CALL = taps on the ad's call button): inflates Branded's Conversions; Branded is Target IS, so no bidding effect.
Both keep reporting under All conversions."""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID = "2524618054"
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = """SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.primary_for_goal,
    conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""

rows = [r.conversion_action for r in q(SEL)]
tn = lambda a: getattr(a.type_, "name", str(a.type_))  # LSA actions come back as bare ints
phone = [a for a in rows if a.id == 7849678789]
taps = [a for a in rows if tn(a) == "CLICK_TO_CALL" and a.name == "[TSD] Click to call"]
if len(phone) != 1 or phone[0].name != "Phone Call": sys.exit("ABORT: 'Phone Call' 7849678789 not found as expected")
if len(taps) != 1: sys.exit(f"ABORT: expected 1 '[TSD] Click to call' CLICK_TO_CALL action, found {len(taps)}")
targets = phone + taps
ops = []
for a in targets:
    print(f"before: {a.id} {a.name} {tn(a)} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
    if not a.primary_for_goal: continue
    op = client.get_type("ConversionActionOperation")
    op.update.resource_name = ga.conversion_action_path(CID, str(a.id))
    op.update.primary_for_goal = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))  # explicit mask: the helper drops falsy values
    ops.append(op)
if ops:
    client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"{len(ops)} action(s) → Secondary", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")
if APPLY:
    ids = {a.id for a in targets}
    for a in (r.conversion_action for r in q(SEL)):
        if a.id in ids: print(f"read-back: {a.id} {a.name} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
