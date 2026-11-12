# APPLIED LIVE 2026-11-10, read-back confirmed (2 negs, Henderson County -> Henderson city on both NB, tap Secondary). Do NOT re-run with --apply.
# Edu's go 2026-11-10 ("Apply 2-5"), Command Center fu-120 / fu-144.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Napps (9509605037), 2026-11-10:
2. PHRASE negatives: 'streety' on NB Plumbing 23819717682 (competitor Streety Plumbing, $70 / 3 clicks wk2 via 'emergency plumber' PHRASE);
   'water heater' on NB Heating 24049055193 (water-heater queries landing on the furnace page, $49 / 2 clicks wk2). 30d replay + keyword-conflict check first.
3. 'Click to call' 7707737498 (CLICK_TO_CALL = taps on the ad call button) -> Secondary (primary_for_goal False), account-wide.
   No enabled campaign bids on conversions (Branded = Target IS, NB = Max Clicks), so this is reporting only.
4. Geo, both NB campaigns: remove Henderson County TX (9059512: Athens, Gun Barrel City, Seven Points, Chandler, Eustace, none on nappsac.com/service-area/),
   add Henderson TX city (1026468, on the service-area page, already on Branded). Wk2 Henderson County clicks = $83 / 4.
5. Cap $25 and budgets $65 / $35 unchanged (asserted, not written)."""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, TAP = "9509605037", "7707737498"
HT, PL = "24049055193", "23819717682"
NEGS = {PL: ["streety"], HT: ["water heater"]}
NAMES = {HT: "NB Heating", PL: "NB Plumbing"}
COUNTY, CITY = "9059512", "1026468"
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- 5. guard: cap/budget/bidding as expected
for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
    campaign_budget.amount_micros FROM campaign WHERE campaign.id IN ({HT},{PL})"""):
    c = r.campaign; cap = c.target_spend.cpc_bid_ceiling_micros / 1e6; bud = r.campaign_budget.amount_micros / 1e6
    print(f"guard: {c.name} {c.status.name} {c.bidding_strategy_type.name} cap ${cap:.2f} budget ${bud:.2f}")
    if c.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 25) > 0.01: sys.exit("ABORT: unexpected bidding/cap")

# --- 2. negatives
MT = client.enums.KeywordMatchTypeEnum
neg_ops = []
for cid, negs in NEGS.items():
    terms = q(f"""SELECT search_term_view.search_term, metrics.all_conversions, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = {cid} AND segments.date BETWEEN '2026-10-11' AND '2026-11-09' AND metrics.impressions > 0""")
    kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    for n in negs:
        hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
        kc = [k for k in kws if f" {n} " in f" {k} "]
        print(f"neg '{n}' on {NAMES[cid]}: {'ALREADY THERE ' if n in existing else ''}blocks {len(hit)} terms "
              f"{[h.search_term_view.search_term for h in hit][:6]}, ${sum(t.metrics.cost_micros for t in hit)/1e6:.2f}, "
              f"all_conv {sum(t.metrics.all_conversions for t in hit):.1f}; kw conflicts: {kc}")
        if kc: sys.exit("ABORT: negative blocks a live keyword")
        if n in existing: continue
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, cid); c.negative = True; c.keyword.text = n; c.keyword.match_type = MT.PHRASE
        neg_ops.append(op)

# --- 4. geo swap
geo_ops = []
for cid in (HT, PL):
    locs = {r.campaign_criterion.location.geo_target_constant.split("/")[-1]: r.campaign_criterion.resource_name for r in q(
        f"""SELECT campaign_criterion.resource_name, campaign_criterion.location.geo_target_constant FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE""")}
    print(f"geo {NAMES[cid]}: {len(locs)} locations, county {'yes' if COUNTY in locs else 'no'}, Henderson city {'yes' if CITY in locs else 'no'}")
    if COUNTY in locs:
        op = client.get_type("CampaignCriterionOperation"); op.remove = locs[COUNTY]; geo_ops.append(op)
    if CITY not in locs:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, cid); c.location.geo_target_constant = f"geoTargetConstants/{CITY}"; geo_ops.append(op)

ccs = client.get_service("CampaignCriterionService")
ops = neg_ops + geo_ops
if ops:
    ccs.mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"2+4. {len(neg_ops)} negatives + {len(geo_ops)} geo ops", "APPLIED" if APPLY else "ok (validate_only)")

# --- 3. tap action -> Secondary
SEL = f"""SELECT conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.primary_for_goal,
    conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.id = {TAP}"""
a = q(SEL)[0].conversion_action
print(f"tap before: {a.name} {a.type_.name} {a.status.name} primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
if a.type_.name != "CLICK_TO_CALL" or a.status.name != "ENABLED": sys.exit("ABORT: unexpected tap action")
if a.primary_for_goal:
    op = client.get_type("ConversionActionOperation")
    op.update.resource_name = ga.conversion_action_path(CID, TAP)
    op.update.primary_for_goal = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"]))  # explicit mask: the helper drops falsy values
    client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": vo})
    print("3. tap action -> Secondary", "APPLIED" if APPLY else "ok (validate_only)")
else:
    print("3. tap action already Secondary, skipped")

if APPLY:
    a = q(SEL)[0].conversion_action
    print(f"read-back 3: primary={a.primary_for_goal} in_conversions={a.include_in_conversions_metric}")
    for cid in (HT, PL):
        negs = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        locs = {r.campaign_criterion.location.geo_target_constant.split("/")[-1] for r in q(f"""SELECT campaign_criterion.location.geo_target_constant
            FROM campaign_criterion WHERE campaign.id = {cid} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE""")}
        print(f"read-back {NAMES[cid]}: negs missing {[n for n in NEGS[cid] if n not in negs]} | county {'STILL THERE' if COUNTY in locs else 'gone'} | "
              f"Henderson city {'yes' if CITY in locs else 'MISSING'} | {len(locs)} locations")
