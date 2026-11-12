# APPLIED LIVE 2026-10-28 on Edu's go ("Execute 1 and 2"). Do NOT re-run with --apply (pause guard aborts anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), from the 10-28 fu-080 read, Edu: "Execute 1 and 2".
1. Nonbranded 23805382277: pause PHRASE 'home improvement siding' (Siding Replacement) and 'home siding' (Siding - General).
   75% of NB spend 10-23..10-27, all research/product terms (hardie board, types of siding, calculator, sheds), 0 leads.
2. NB campaign PHRASE negatives for DIY/material research terms (singular/plural twins, since negatives don't match close variants).
Aborts on unexpected state (bidding, cap, budget, keywords not found exactly once, negative hitting a live keyword).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "2198608170", "23805382277"
PAUSE = {("Siding Replacement", "home improvement siding"), ("Siding - General", "home siding")}
NEG = ["calculator", "soffit", "cdx", "log siding", "shed", "sheds", "precios", "precio", "types of",
       "picture", "pictures", "material", "materials", "panels"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum

# --- guards
c = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
    FROM campaign WHERE campaign.id = {NB}""")[0]
cap, bud = c.campaign.target_spend.cpc_bid_ceiling_micros / 1e6, c.campaign_budget.amount_micros / 1e6
print(f"NB: {c.campaign.bidding_strategy_type.name} cap=${cap:.2f} budget=${bud:.2f}")
if c.campaign.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 12) > 0.01: sys.exit("ABORT: NB not on Max Clicks $12")
if abs(bud - 67) > 0.01: sys.exit("ABORT: NB budget not $67")

kws = q(f"""SELECT ad_group.name, ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED'
    AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")
targets = [r for r in kws if (r.ad_group.name, r.ad_group_criterion.keyword.text.lower()) in PAUSE
           and r.ad_group_criterion.keyword.match_type.name == "PHRASE"]
print(f"to pause: {[(r.ad_group.name, r.ad_group_criterion.keyword.text) for r in targets]}")
if len(targets) != len(PAUSE): sys.exit("ABORT: pause targets not found exactly once each")
live = [r.ad_group_criterion.keyword.text.lower() for r in kws if r not in targets]
print(f"stay live ({len(live)}): {live}")
hit = [(n, k) for n in NEG for k in live if f" {n} " in f" {k} "]
if hit: sys.exit(f"ABORT: negative matches a live keyword {hit}")

# negatives: 30d replay on NB terms
blocked = 0
for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS"""):
    t = r.search_term_view.search_term.lower()
    m = [n for n in NEG if f" {n} " in f" {t} "]
    if m and r.metrics.cost_micros:
        blocked += r.metrics.cost_micros
        print(f"   replay blocks '{t}' ${r.metrics.cost_micros/1e6:.2f} conv {r.metrics.conversions} ({m[0]})")
print(f"   replay total ${blocked/1e6:.2f}")
existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg_new = [n for n in NEG if n not in existing]
print(f"new negatives: {neg_new} (existing total {len(existing)})")

# --- 1. pause
ops = []
for r in targets:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = r.ad_group_criterion.resource_name; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} pauses ok", "(validate_only)" if vo else "APPLIED")

# --- 2. negatives
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, NB); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE; ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- read-back
if APPLY:
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion
            WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
            AND ad_group_criterion.status = 'ENABLED'"""):
        print(f"   live kw: {r.ad_group.name} | {r.ad_group_criterion.keyword.text} {r.ad_group_criterion.keyword.match_type.name}")
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]} (total {len(got)})")
