# APPLIED LIVE 2026-10-22 on Edu's go ("Yes, execute 1, 2, 3 and 4"). Do NOT re-run with --apply (BROAD-count guard aborts anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), from the 10-22 post-change read, Edu: "Yes, execute 1, 2, 3 and 4".
1. Nonbranded 23805382277: portfolio Max Conversions w/ $15 ceiling (12283201754, set 10-21) -> standard Maximize Clicks,
   $12 max CPC (Nick's pattern). Max Conv was learning from wrong-number calls on ~1 real lead a week.
2. 'Calls from ads' goal (PHONE_CALL_LEAD / CALL_FROM_ADS, incl. '[TSD] Click to call' taps) -> NOT biddable on NB and PMax.
   Calls keep reporting under All conversions. PMax keeps bidding on Google lead forms. Branded left as is: it is Manual CPC
   and the call goal is its only goal (API: EMPTY_CONVERSION_GOALS).
3. NB phrase-only: PHRASE twins for the BROAD keywords that spent in 30d (home siding contractors, siding repair contractors,
   home improvement siding, siding contractors near me), then pause all 23 enabled BROAD keywords in enabled ad groups.
4. NB campaign PHRASE negatives: vivax, quint pro, cat exteriors.
Aborts on unexpected state (bidding, budget, BROAD count, goals, existing twins).
"""
import sys
sys.path.insert(0, ".")
from google.protobuf.field_mask_pb2 import FieldMask
from lib import init_client

CID, NB, PMAX, BR = "2198608170", "23805382277", "21291552209", "23233882685"
PORTFOLIO = "12283201754"
NB_CPC_CAP = 12.0
TWINS = {"home siding contractors", "siding repair contractors", "home improvement siding", "siding contractors near me"}
NEG = ["vivax", "quint pro", "cat exteriors"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum
CAT, ORI = client.enums.ConversionActionCategoryEnum, client.enums.ConversionOriginEnum

# --- guards
c = q(f"""SELECT campaign.bidding_strategy, campaign.bidding_strategy_type, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {NB}""")[0]
print(f"NB: {c.campaign.bidding_strategy_type.name} portfolio={c.campaign.bidding_strategy} budget=${c.campaign_budget.amount_micros/1e6:.2f}")
if not c.campaign.bidding_strategy.endswith(PORTFOLIO): sys.exit("ABORT: NB not on the 10-21 portfolio")
if abs(c.campaign_budget.amount_micros / 1e6 - 67.0) > 0.01: sys.exit("ABORT: NB budget not $67")

kws = q(f"""SELECT ad_group.id, ad_group.name, ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'""")
broad = [r for r in kws if r.ad_group_criterion.keyword.match_type.name == "BROAD" and r.ad_group_criterion.status.name == "ENABLED"]
print(f"enabled BROAD in enabled ad groups: {len(broad)}")
if len(broad) != 23: sys.exit("ABORT: expected 23 enabled BROAD keywords")
twin_src = [r for r in broad if r.ad_group_criterion.keyword.text.lower() in TWINS]
print(f"twin sources: {[(r.ad_group.name, r.ad_group_criterion.keyword.text) for r in twin_src]}")
if len(twin_src) != len(TWINS): sys.exit("ABORT: twin source keywords not found exactly once each")
have_phrase = {(r.ad_group.id, r.ad_group_criterion.keyword.text.lower()) for r in kws if r.ad_group_criterion.keyword.match_type.name == "PHRASE"}
if any((r.ad_group.id, r.ad_group_criterion.keyword.text.lower()) in have_phrase for r in twin_src): sys.exit("ABORT: a PHRASE twin already exists")

goals = [r for r in q(f"""SELECT campaign.id, campaign_conversion_goal.resource_name, campaign_conversion_goal.category, campaign_conversion_goal.origin,
    campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id IN ({NB},{PMAX})""")
    if r.campaign_conversion_goal.category == CAT.PHONE_CALL_LEAD and r.campaign_conversion_goal.origin == ORI.CALL_FROM_ADS]
print(f"call goals: {[(r.campaign.id, r.campaign_conversion_goal.biddable) for r in goals]}")
if len(goals) != 2 or not all(r.campaign_conversion_goal.biddable for r in goals): sys.exit("ABORT: call goals not biddable on NB + PMax")

# negatives: replay on 30d NB terms + conflicts with live keywords / existing negatives
for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE campaign.id = {NB}
    AND segments.date DURING LAST_30_DAYS"""):
    t = r.search_term_view.search_term.lower()
    if any(n in t for n in NEG): print(f"   replay blocks '{t}' ${r.metrics.cost_micros/1e6:.2f} conv {r.metrics.conversions}")
live = [r.ad_group_criterion.keyword.text.lower() for r in kws if r.ad_group_criterion.status.name == "ENABLED"]
if any(n in k for n in NEG for k in live): sys.exit("ABORT: a negative matches a live keyword")
existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg_new = [n for n in NEG if n not in existing]

# --- 3. phrase twins, then pause all enabled BROAD
agc = client.get_service("AdGroupCriterionService")
ops = []
for r in twin_src:
    op = client.get_type("AdGroupCriterionOperation"); k = op.create
    k.ad_group = ga.ad_group_path(CID, r.ad_group.id); k.status = ST.ENABLED
    k.keyword.text = r.ad_group_criterion.keyword.text; k.keyword.match_type = MT.PHRASE; ops.append(op)
agc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} phrase twins ok", "(validate_only)" if vo else "APPLIED")
ops = []
for r in broad:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = r.ad_group_criterion.resource_name; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
agc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} BROAD pauses ok", "(validate_only)" if vo else "APPLIED")

# --- 4. negatives
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, NB); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE; ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- 1. NB -> Maximize Clicks $12 cap (replaces the portfolio)
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.target_spend.cpc_bid_ceiling_micros = int(NB_CPC_CAP * 1e6)
op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("NB Max Clicks ok", "(validate_only)" if vo else "APPLIED")

# --- 2. call goal not biddable (explicit mask: the helper drops falsy values)
ops = []
for r in goals:
    op = client.get_type("CampaignConversionGoalOperation")
    op.update.resource_name = r.campaign_conversion_goal.resource_name; op.update.biddable = False
    client.copy_from(op.update_mask, FieldMask(paths=["biddable"])); ops.append(op)
client.get_service("CampaignConversionGoalService").mutate_campaign_conversion_goals(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("call goals ok", "(validate_only)" if vo else "APPLIED")

# --- read-back
if APPLY:
    c = q(f"""SELECT campaign.bidding_strategy, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros FROM campaign WHERE campaign.id = {NB}""")[0]
    print(f"   NB: {c.campaign.bidding_strategy_type.name} cap ${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} portfolio='{c.campaign.bidding_strategy}'")
    for r in q(f"""SELECT campaign.id, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
            FROM campaign_conversion_goal WHERE campaign.id IN ({NB},{PMAX},{BR})"""):
        g = r.campaign_conversion_goal
        if g.biddable or g.category == CAT.PHONE_CALL_LEAD: print(f"   {r.campaign.id} cat={int(g.category)} origin={int(g.origin)} biddable={g.biddable}")
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion
            WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
            AND ad_group_criterion.status = 'ENABLED'"""):
        print(f"   live kw: {r.ad_group.name} | {r.ad_group_criterion.keyword.text} {r.ad_group_criterion.keyword.match_type.name}")
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]} (total {len(got)})")
