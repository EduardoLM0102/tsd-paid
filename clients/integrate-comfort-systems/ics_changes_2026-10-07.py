"""ICS (4571881760) changes 2026-10-07, plan steps 4, 5 (rebate only, approved by Edu), 6, 7, 8. One atomic request.
Run from google-ads-ratos/scripts with GADS_ENV_PATH=.env.topserv. Default = validate only; pass --live to apply."""
import sys
sys.path.insert(0, ".")
from lib import init_client, run_query
from google.api_core import protobuf_helpers

LIVE = "--live" in sys.argv
CID = "4571881760"
PMAX, NB, BRANDED = "22890783804", "24047025253", "23675636592"
NB_NEGATIVES = [  # campaign-level PHRASE
    "greensboro", "cleveland", "brooklyn", "nyc", "san antonio", "mattituck",          # out of area
    "lowe's", "lowes", "home depot", "window ac", "window air conditioner", "window unit",
    "for sale", "without outdoor unit", "frigidaire", "windmill",                       # DIY / retail
]
NEW_BUDGETS = {PMAX: 50_000_000, NB: 15_000_000}   # $50/day, $15/day
BRANDED_CEILING = 7_000_000                         # $7

client = init_client()
ga = client.get_service("GoogleAdsService")
ops = []

# --- lookups ---
ac_neg = [r for r in run_query(CID, f"""SELECT campaign_criterion.criterion_id, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
  FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE""")
  if r["campaign_criterion"]["keyword"]["text"].strip().lower() in ("air conditioning", "rebate")]
print("PMax negatives to remove:", [(r["campaign_criterion"]["criterion_id"], r["campaign_criterion"]["keyword"]["text"], r["campaign_criterion"]["keyword"]["match_type"]) for r in ac_neg])
existing_pmax = {r["campaign_criterion"]["keyword"]["text"].lower() for r in run_query(CID, f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.type = 'KEYWORD'")}
acr = run_query(CID, f"SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB} AND ad_group.name = 'AC Repair'")
print("AC Repair ad group:", acr)
budgets = run_query(CID, f"""SELECT campaign.id, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
  FROM campaign WHERE campaign.id IN ({PMAX}, {NB})""")
for b in budgets: print("budget:", b["campaign"]["id"], b["campaign_budget"])
tis = run_query(CID, f"SELECT campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros FROM campaign WHERE campaign.id = {BRANDED}")
print("Branded target IS before:", tis[0]["campaign"].get("target_impression_share"))

# --- step 4: PMax negatives ---
for r in ac_neg:
    op = client.get_type("MutateOperation")
    op.campaign_criterion_operation.remove = ga.campaign_criterion_path(CID, PMAX, r["campaign_criterion"]["criterion_id"])
    ops.append((f"PMax: remove negative '{r['campaign_criterion']['keyword']['text']}' " + r["campaign_criterion"]["keyword"]["match_type"], op))
if "tech support" not in existing_pmax:
    op = client.get_type("MutateOperation")
    c = op.campaign_criterion_operation.create
    c.campaign = ga.campaign_path(CID, PMAX); c.negative = True
    c.keyword.text = "tech support"; c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append(("PMax: add negative 'tech support' PHRASE", op))

# --- step 6: NonBranded negatives + pause AC Repair ---
for t in NB_NEGATIVES:
    op = client.get_type("MutateOperation")
    c = op.campaign_criterion_operation.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True
    c.keyword.text = t; c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append((f"NB: add negative '{t}' PHRASE", op))
assert len(acr) == 1, "AC Repair ad group not found uniquely"
op = client.get_type("MutateOperation")
ag = op.ad_group_operation.update
ag.resource_name = ga.ad_group_path(CID, acr[0]["ad_group"]["id"])
ag.status = client.enums.AdGroupStatusEnum.PAUSED
op.ad_group_operation.update_mask.CopyFrom(protobuf_helpers.field_mask(None, ag._pb))
ops.append(("NB: pause ad group 'AC Repair'", op))

# --- step 7: Branded CPC ceiling ---
op = client.get_type("MutateOperation")
camp = op.campaign_operation.update
camp.resource_name = ga.campaign_path(CID, BRANDED)
camp.target_impression_share.cpc_bid_ceiling_micros = BRANDED_CEILING
op.campaign_operation.update_mask.CopyFrom(protobuf_helpers.field_mask(None, camp._pb))
ops.append(("Branded: target IS CPC ceiling -> $7", op))

# --- step 8: budgets ---
for b in budgets:
    cid = str(b["campaign"]["id"])
    assert not b["campaign_budget"].get("explicitly_shared"), f"budget for {cid} is shared, stop"
    op = client.get_type("MutateOperation")
    bu = op.campaign_budget_operation.update
    bu.resource_name = b["campaign_budget"]["resource_name"]
    bu.amount_micros = NEW_BUDGETS[cid]
    op.campaign_budget_operation.update_mask.CopyFrom(protobuf_helpers.field_mask(None, bu._pb))
    ops.append((f"Budget {cid}: ${int(float(b['campaign_budget']['amount_micros']))} -> ${NEW_BUDGETS[cid]/1e6:.0f}/day (raw before={b['campaign_budget']['amount_micros']})", op))

print(f"\n{len(ops)} operations, mode = {'LIVE' if LIVE else 'VALIDATE ONLY'}")
for d, _ in ops: print("  -", d)
req = client.get_type("MutateGoogleAdsRequest")
req.customer_id = CID
req.mutate_operations.extend([o for _, o in ops])
req.validate_only = not LIVE
resp = ga.mutate(request=req)
print("\nOK." if not LIVE else f"\nAPPLIED: {len(resp.mutate_operation_responses)} responses")
