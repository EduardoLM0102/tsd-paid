# APPLIED LIVE 2026-11-02 on Edu's go. Do NOT re-run with --apply (skips existing negatives anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), 11-02 fu-103 recheck, Edu: "apply the negatives and let's watch - they'll offboard anyway".
Client terminated 11-02 (30-day countdown). 'house exterior siding' PHRASE stays live (Edu: don't pause), it took 74% of NB spend
10-29..11-02 on material/product research. Adds NB campaign negatives:
- PHRASE: research/DIY, board sizes, out of area, product brands, Spanish product searches.
- EXACT: bare product/material lookups (keeps "hardie siding installers near me" etc. open).
Cost searches ("how much is siding for a house") and metal/steel/faux/slate styles left alone on purpose.
Aborts on unexpected state (bidding, cap, budget, negative hitting a live keyword).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "2198608170", "23805382277"
PHRASE = ["types", "vs", "pros and cons", "installing", "installation process", "4x8", "4 x 8", "12 x 16", "seattle", "log cabin",
          "smartside", "smart siding", "smart board", "lp", "truwood", "everlog", "trek", "allura", "accoya", "masonite", "ogee",
          "hardboard", "de madera", "de plastico", "de cemento", "para casa"]
EXACT = ["hardie board siding", "hardie board", "hardie siding", "james hardie siding", "siding", "sidding", "house siding",
         "siding for houses", "siding for house", "siding house", "siding on a house", "exterior siding", "fiber cement siding",
         "board and batten siding", "metal siding", "wood siding", "vinyl siding for houses", "modern vinyl siding", "siding options",
         "house siding options", "home siding options"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

# --- guards
c = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
    FROM campaign WHERE campaign.id = {NB}""")[0]
cap, bud = c.campaign.target_spend.cpc_bid_ceiling_micros / 1e6, c.campaign_budget.amount_micros / 1e6
print(f"NB: {c.campaign.bidding_strategy_type.name} cap=${cap:.2f} budget=${bud:.2f}")
if c.campaign.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 12) > 0.01: sys.exit("ABORT: NB not on Max Clicks $12")
if abs(bud - 67) > 0.01: sys.exit("ABORT: NB budget not $67")

live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
print(f"live keywords ({len(live)}): {live}")
hit = [(n, k) for n in PHRASE for k in live if f" {n} " in f" {k} "] + [(n, k) for n in EXACT for k in live if n == k]
if hit: sys.exit(f"ABORT: negative matches a live keyword {hit}")

blocked = 0
for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS"""):
    t = r.search_term_view.search_term.lower()
    m = [n for n in PHRASE if f" {n} " in f" {t} "] or [n for n in EXACT if n == t]
    if m and (r.metrics.cost_micros or r.metrics.conversions):
        blocked += r.metrics.cost_micros
        print(f"   replay blocks '{t}' ${r.metrics.cost_micros/1e6:.2f} conv {r.metrics.conversions} ({m[0]})")
print(f"   replay total ${blocked/1e6:.2f}")

existing = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
    SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
todo = [(t, "PHRASE") for t in PHRASE] + [(t, "EXACT") for t in EXACT]
new = [x for x in todo if x not in existing]
print(f"new negatives {len(new)} (already there: {[x for x in todo if x in existing]}; existing total {len(existing)})")

ops = []
for t, mt in new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, NB); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = getattr(MT, mt); ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    now = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
        SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
        WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("missing:", [x for x in todo if x not in now], f"total {len(now)}")
