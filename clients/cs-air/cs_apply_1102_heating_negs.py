# APPLIED LIVE 2026-11-02 on Edu's go. Do NOT re-run with --apply (skips existing negatives anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), heating Search week-1 check (fu-095), Edu 11-02: "Apply the negatives and keep the cap where it is".
TSD_10.23_Search_Nonbranded_Heating 24383234148: $226 / 24 clicks / 0 leads 10-26..11-02; Replacement side buys product
research, competitors showing. Adds campaign negatives:
- PHRASE: research, not-our-job, product brands, competitors.
- EXACT: bare product lookups (keeps "furnace repair", "new furnace", "heat pump replacement" etc. open).
Cap $12 + budget $30 unchanged. Aborts on unexpected state or a negative hitting a live keyword.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, H = "5563867754", "24383234148"
PHRASE = ["what is", "best", "reviews", "brands", "error codes", "window", "mobile home", "floor heating", "empire", "infinity",
          "ao smith", "prime time", "bock", "service champs", "silver spur", "burke", "christmas", "encore", "hat plumbing"]
EXACT = ["heat pump", "gas furnace", "furnace", "a c furnace", "electric furnace", "central heater", "gas heating unit"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

c = q(f"""SELECT campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
    FROM campaign WHERE campaign.id = {H}""")[0]
cap, bud = c.campaign.target_spend.cpc_bid_ceiling_micros / 1e6, c.campaign_budget.amount_micros / 1e6
print(f"Heating: {c.campaign.status.name} {c.campaign.bidding_strategy_type.name} cap=${cap:.2f} budget=${bud:.2f}")
if c.campaign.status.name != "ENABLED" or c.campaign.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 12) > 0.01 or abs(bud - 30) > 0.01:
    sys.exit("ABORT: heating campaign not in the expected state")

live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {H} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
hit = [(n, k) for n in PHRASE for k in live if f" {n} " in f" {k} "] + [(n, k) for n in EXACT for k in live if n == k]
print(f"live keywords: {len(live)}")
if hit: sys.exit(f"ABORT: negative matches a live keyword {hit}")

for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.impressions, metrics.conversions FROM search_term_view
    WHERE campaign.id = {H} AND segments.date DURING LAST_14_DAYS"""):
    t = r.search_term_view.search_term.lower()
    m = [n for n in PHRASE if f" {n} " in f" {t} "] or [n for n in EXACT if n == t]
    if m: print(f"   replay blocks '{t}' ${r.metrics.cost_micros/1e6:.2f} {r.metrics.impressions}i conv {r.metrics.conversions} ({m[0]})")

existing = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
    SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
    WHERE campaign.id = {H} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
todo = [(t, "PHRASE") for t in PHRASE] + [(t, "EXACT") for t in EXACT]
new = [x for x in todo if x not in existing]
print(f"new negatives {len(new)} (already there: {[x for x in todo if x in existing]}; existing total {len(existing)})")

ops = []
for t, mt in new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, H); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = getattr(MT, mt); ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    now = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
        SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
        WHERE campaign.id = {H} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    c = q(f"SELECT campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {H}")[0]
    print("missing:", [x for x in todo if x not in now], f"total {len(now)}",
          f"cap=${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} budget=${c.campaign_budget.amount_micros/1e6:.2f}")
