# APPLIED LIVE 2026-10-30 on Edu's go ("Cut Vinyl Siding and clean up siding repair"). Do NOT re-run with --apply (status guard aborts anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), from the 10-30 ad group side-by-side (fu-104), Edu: "Cut Vinyl Siding and clean up siding repair".
1. Nonbranded 23805382277: pause ad group Vinyl Siding (199267778626). Sep 1-Oct 29 $648 for 3 Sept forms, 0 in Oct,
   search terms = materials/supplier research.
2. NB campaign PHRASE negatives for the non-customer terms Siding Repair paid for in October (supplier brand, lead
   marketplaces, competitor, charity, handyman, suppliers), most already present since 10-16/10-22, plus 12
   other-company names Repair showed for since 10-22. "free" left out on purpose: it would block "free estimate".
Aborts on unexpected state (bidding, cap, budget, ad group status, negative hitting a live keyword).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, VINYL = "2198608170", "23805382277", "199267778626"
NEG = ["style crest", "angie", "angies", "angi", "vivax", "charities", "charity", "handyman", "supplier", "suppliers",
       # other companies Siding Repair showed for 10-22..10-29 (impressions, no clicks yet)
       "arcus construction", "certapro", "conservation construction", "dallas cedar", "handy jack", "house doctors",
       "level and square", "thumbtack", "true blue", "victory construction", "x team", "xteam"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
AGS = client.enums.AdGroupStatusEnum

# --- guards
c = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
    FROM campaign WHERE campaign.id = {NB}""")[0]
cap, bud = c.campaign.target_spend.cpc_bid_ceiling_micros / 1e6, c.campaign_budget.amount_micros / 1e6
print(f"NB: {c.campaign.bidding_strategy_type.name} cap=${cap:.2f} budget=${bud:.2f}")
if c.campaign.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 12) > 0.01: sys.exit("ABORT: NB not on Max Clicks $12")
if abs(bud - 67) > 0.01: sys.exit("ABORT: NB budget not $67")

ag = q(f"SELECT ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE ad_group.id = {VINYL}")[0].ad_group
print(f"ad group: {ag.name} {ag.status.name}")
if ag.name != "Vinyl Siding" or ag.status.name != "ENABLED": sys.exit("ABORT: Vinyl Siding not found ENABLED")

live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group.id != {VINYL} AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
print(f"live keywords after the pause ({len(live)}): {live}")
hit = [(n, k) for n in NEG for k in live if f" {n} " in f" {k} "]
if hit: sys.exit(f"ABORT: negative matches a live keyword {hit}")

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
print(f"new negatives: {neg_new} (already there: {[n for n in NEG if n in existing]}; existing total {len(existing)})")

# --- 1. pause Vinyl Siding
op = client.get_type("AdGroupOperation")
op.update.resource_name = ag.resource_name; op.update.status = AGS.PAUSED; op.update_mask.paths.append("status")
client.get_service("AdGroupService").mutate_ad_groups(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("Vinyl pause ok", "(validate_only)" if vo else "APPLIED")

# --- 2. negatives
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, NB); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE; ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- read-back
if APPLY:
    print("read-back:", q(f"SELECT ad_group.status FROM ad_group WHERE ad_group.id = {VINYL}")[0].ad_group.status.name)
    now = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("negatives present:", [n for n in NEG if n in now], "missing:", [n for n in NEG if n not in now], f"total {len(now)}")
