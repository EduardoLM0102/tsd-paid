# APPLIED LIVE 2026-11-02 on Edu's go. Do NOT re-run with --apply (aborts: brand list exists).
# Run: ./tsd.sh neon_monkey_apply_1102.py   (validate-only without --apply)
"""Neon Monkey 7953905280, PMax 2-week test (Edu 11-02: "work on those 3 to-dos"). Budgets unchanged (to-do 3).
Why: of 6 first-time 60s+ PMax ad calls Oct 19-Nov 1, only 2 were real leads (142s, 161s); 3 were wrong-company
calls (Davey Tree, Asplundh/Oncor, plant nursery, 63-73s) that 'Calls from ads' counted as conversions.
1. 'Calls from ads' 833426830 (AD_CALL): minimum call length 60s -> 90s (account-wide action, also NB/Branded).
2a. Phrase negatives davey, asplundh, oncor, utility, fertilizer on PMax 21225221220 + NB 23825900343.
2b. New brand list 'TSD | Utility tree companies' (Davey Tree Expert Company, Asplundh Tree Expert Company,
    Oncor Electric Delivery) attached to PMax as a brand exclusion.
Aborts on unexpected state.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, PMAX, NB, CALLS = "7953905280", "21225221220", "23825900343", "833426830"
NEG = ["davey", "asplundh", "oncor", "utility", "fertilizer"]
BRANDS = {"/g/11trq8nxps": "Davey Tree Expert Company", "/g/11shhfkh6r": "Asplundh Tree Expert Company",
          "/g/11shh9ty6t": "Oncor Electric Delivery"}
LIST_NAME = "TSD | Utility tree companies"
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

# --- guards
ca = q(f"SELECT conversion_action.resource_name, conversion_action.name, conversion_action.type, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALLS}")[0].conversion_action
print(f"conv: {ca.name} {ca.type_.name} dur={ca.phone_call_duration_seconds}s")
if ca.type_.name != "AD_CALL" or ca.phone_call_duration_seconds not in (60, 90): sys.exit("ABORT: unexpected Calls from ads state")
for cid_c, want in [(PMAX, "MAXIMIZE_CONVERSIONS"), (NB, "TARGET_SPEND")]:
    c = q(f"SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {cid_c}")[0]
    print(f"{c.campaign.name}: {c.campaign.status.name} {c.campaign.bidding_strategy_type.name} ${c.campaign_budget.amount_micros/1e6:.0f}/d")
    if c.campaign.status.name != "ENABLED" or c.campaign.bidding_strategy_type.name != want: sys.exit(f"ABORT: {cid_c} state changed")

live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
hit = [(n, k) for n in NEG for k in live if f" {n} " in f" {k} "]
if hit: sys.exit(f"ABORT: negative matches a live NB keyword {hit}")

for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS"""):
    t = r.search_term_view.search_term.lower()
    m = [n for n in NEG if f" {n} " in f" {t} "]
    if m: print(f"   NB replay blocks '{t}' ${r.metrics.cost_micros/1e6:.2f} conv {r.metrics.conversions}")

ops_neg = []
for cid_c in (PMAX, NB):
    have = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid_c} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    for t in NEG:
        if t in have: continue
        op = client.get_type("CampaignCriterionOperation"); cc = op.create
        cc.campaign = ga.campaign_path(CID, cid_c); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE
        ops_neg.append(op)
print(f"negatives to add: {len(ops_neg)}")

existing_list = q(f"SELECT shared_set.resource_name, shared_set.status FROM shared_set WHERE shared_set.type = 'BRANDS' AND shared_set.name = '{LIST_NAME}'")
if existing_list: sys.exit("ABORT: brand list already exists, check before re-running")

# --- 1. call length
op = client.get_type("ConversionActionOperation")
op.update.resource_name = ca.resource_name; op.update.phone_call_duration_seconds = 90
op.update_mask.paths.append("phone_call_duration_seconds")
client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("Calls from ads 90s ok", "(validate_only)" if vo else "APPLIED")

# --- 2a. negatives
if ops_neg:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops_neg, "validate_only": vo})
print(f"{len(ops_neg)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- 2b. brand list + exclusion on PMax (one atomic mutate with temp ids)
gas = client.get_service("GoogleAdsService")
ss_tmp = f"customers/{CID}/sharedSets/-1"
mops = []
m = client.get_type("MutateOperation"); ss = m.shared_set_operation.create
ss.resource_name = ss_tmp; ss.name = LIST_NAME; ss.type_ = client.enums.SharedSetTypeEnum.BRANDS; mops.append(m)
for eid in BRANDS:
    m = client.get_type("MutateOperation"); sc = m.shared_criterion_operation.create
    sc.shared_set = ss_tmp; sc.brand.entity_id = eid; mops.append(m)
m = client.get_type("MutateOperation"); cc = m.campaign_criterion_operation.create  # PMax: brand exclusion = negative BRAND_LIST criterion
cc.campaign = ga.campaign_path(CID, PMAX); cc.negative = True; cc.brand_list.shared_set = ss_tmp; mops.append(m)
gas.mutate(request={"customer_id": CID, "mutate_operations": mops, "validate_only": vo})
print("brand list + PMax exclusion ok", "(validate_only)" if vo else "APPLIED")

# --- read-back
if APPLY:
    print("calls dur:", q(f"SELECT conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALLS}")[0].conversion_action.phone_call_duration_seconds)
    for cid_c in (PMAX, NB):
        have = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid_c} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(cid_c, "missing negs:", [t for t in NEG if t not in have], "total", len(have))
    for r in q(f"""SELECT campaign_criterion.brand_list.shared_set, campaign_criterion.negative, campaign_criterion.status FROM campaign_criterion
        WHERE campaign.id = {PMAX} AND campaign_criterion.type = 'BRAND_LIST'"""):
        print("PMax brand exclusion:", r.campaign_criterion.brand_list.shared_set, "negative", r.campaign_criterion.negative, r.campaign_criterion.status.name)
    for r in q(f"SELECT shared_set.name, shared_set.member_count FROM shared_set WHERE shared_set.name = '{LIST_NAME}'"):
        print("brand list:", r.shared_set.name, "members", r.shared_set.member_count)
