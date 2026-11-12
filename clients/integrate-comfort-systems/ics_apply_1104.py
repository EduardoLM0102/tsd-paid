# APPLIED LIVE 2026-11-04, read-back confirmed (tap primary False + in_conversions False; 2 negs, none missing). Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Apply 1 and 2"), Command Center fu-109.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Integrate Comfort (4571881760), 2026-11-04:
1. `[TSD] Click to call` (7835539864, CLICK_TO_CALL = taps on the ad's call button) → Secondary (primary_for_goal False), account-wide.
   The 10-28 custom goal 6459689709 lets taps through (same bucket as Calls from ads; same failure as Watt's Right 11-03).
   Only PMax bids on conversions here (Branded = Target IS, NonBranded = Max Clicks).
2. NonBranded 24047025253: PHRASE competitor negatives 'steve sirc', 'advanced heating'. Replayed against 30d terms + live keywords first.
Budgets unchanged ($40 / $22 / $15)."""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, TAP, NB = "4571881760", "7835539864", "24047025253"
NEG = ["steve sirc", "advanced heating"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = f"""SELECT conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.primary_for_goal,
    conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.id = {TAP}"""

# --- 1. tap action → Secondary
a = q(SEL)[0].conversion_action
print(f"before: {a.name} {a.type_.name} {a.status.name} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
if a.type_.name != "CLICK_TO_CALL" or a.status.name != "ENABLED": sys.exit("ABORT: unexpected tap action")
if a.primary_for_goal:
    op = client.get_type("ConversionActionOperation")
    op.update.resource_name = ga.conversion_action_path(CID, TAP)
    op.update.primary_for_goal = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))  # explicit mask: the helper drops falsy values
    client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": vo})
    print("1. tap action → Secondary", "APPLIED" if APPLY else "ok (validate_only)")
else:
    print("1. tap action already Secondary, skipped")

# --- 2. NB negatives (30d replay first)
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg = [n for n in NEG if n not in existing]
conflict = False
for n in NEG:
    hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
    kc = [k for k in kws if f" {n} " in f" {k} "]
    conflict |= bool(kc)
    print(f"neg '{n}': {'ALREADY THERE ' if n in existing else ''}blocks {len(hit)} terms {[h.search_term_view.search_term for h in hit][:5]}, "
          f"${sum(t.metrics.cost_micros for t in hit)/1e6:.2f}, conv {sum(t.metrics.conversions for t in hit):.1f}; kw conflicts: {kc}")
if conflict: sys.exit("ABORT: a negative blocks a live keyword")
MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"2. negatives ({len(neg)})", "APPLIED" if APPLY else "ok (validate_only)")

if APPLY:
    a = q(SEL)[0].conversion_action
    print(f"read-back 1: primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
    got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"read-back 2: NB negatives missing: {[n for n in NEG if n not in got]}")
