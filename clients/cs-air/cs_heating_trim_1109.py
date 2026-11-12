# APPLIED LIVE 2026-11-09 ~11:25 CT on Edu's go (read-back OK: Replacement PAUSED, budget $15, negatives 99 -> 125).
# Do NOT re-run with --apply (aborts anyway: budget is no longer $30 and Replacement is no longer ENABLED).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), fu-091, Edu 11-09: "for Heating Search, do what you think is better".
TSD_10.23_Search_Nonbranded_Heating 24383234148 since launch (10-27..11-09): $458 / 51 clicks / 0 leads.
One atomic mutate:
- PAUSE ad group Heating Replacement 198402775381 ($284 / 32 clicks / 0 leads, research traffic, QS 0 on the spenders).
- Budget $30 -> $15/day: Heating Repair alone for one last week ($174 / 19 clicks / 0 leads so far, too few clicks to call).
- Campaign negatives from the visible impression-only terms (troubleshooting, equipment C&S doesn't service, research, competitors).
$12 CPC cap unchanged. Decide on 11-16: pause the campaign if Repair still has 0 leads.
Aborts on unexpected state, on a negative hitting a live Repair keyword, or on a negative blocking a term that converted."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, H = "5563867754", "24383234148"
AG_REPLACE, AG_REPAIR = "198402775381", "196718543930"
NEW_BUDGET = 15.00
PHRASE = [
    # troubleshooting / DIY ('why' and 'thermostat' left out on purpose: "why is my heater not working" and
    # "thermostat on but no heat" are people with a broken heater, which is what Repair is there to catch)
    "code", "codes", "pilot light", "blinking",
    # equipment C&S does not service
    "boiler", "boilers", "geothermal", "radiant", "gas log", "gas logs", "navien", "dometic", "heat and glo",
    # research
    "ratings", "rating", "brand", "how much", "largest", "biggest",
    # competitors seen 2+ times
    "service champions", "varsity zone", "bacon hvac", "matco", "reliant", "southern air", "willard",
]
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum


def state():
    c = q(f"""SELECT campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
        campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
        FROM campaign WHERE campaign.id = {H}""")[0]
    ags = {str(r.ad_group.id): (r.ad_group.name, r.ad_group.status.name) for r in q(f"SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {H}")}
    negs = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
        SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
        WHERE campaign.id = {H} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    return c, ags, negs


c, ags, negs = state()
cap, bud = c.campaign.target_spend.cpc_bid_ceiling_micros / 1e6, c.campaign_budget.amount_micros / 1e6
print(f"Heating: {c.campaign.status.name} {c.campaign.bidding_strategy_type.name} cap=${cap:.2f} budget=${bud:.2f} "
      f"shared={c.campaign_budget.explicitly_shared} refs={c.campaign_budget.reference_count} | ad groups {ags} | negatives {len(negs)}")
if (c.campaign.status.name != "ENABLED" or c.campaign.bidding_strategy_type.name != "TARGET_SPEND" or abs(cap - 12) > 0.01
        or abs(bud - 30) > 0.01 or c.campaign_budget.explicitly_shared or c.campaign_budget.reference_count != 1):
    sys.exit("ABORT: heating campaign or its budget not in the expected state")
if ags.get(AG_REPLACE) != ("Heating Replacement", "ENABLED") or ags.get(AG_REPAIR) != ("Heating Repair", "ENABLED"):
    sys.exit("ABORT: ad groups not in the expected state")

live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE ad_group.id = {AG_REPAIR} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
    AND ad_group_criterion.status = 'ENABLED'""")]
hit = [(n, k) for n in PHRASE for k in live if f" {n} " in f" {k} "]
print(f"live Repair keywords: {len(live)}")
if hit: sys.exit(f"ABORT: negative matches a live Repair keyword {hit}")

blocked_cost = blocked_n = 0
for r in q(f"""SELECT ad_group.name, search_term_view.search_term, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.all_conversions
    FROM search_term_view WHERE campaign.id = {H} AND segments.date BETWEEN '2026-10-27' AND '2026-11-09'"""):
    t = r.search_term_view.search_term.lower()
    m = [n for n in PHRASE if f" {n} " in f" {t} "]
    if not m: continue
    blocked_n += 1; blocked_cost += r.metrics.cost_micros / 1e6
    if r.metrics.all_conversions > 0: sys.exit(f"ABORT: negative '{m[0]}' would block a term that converted: {t}")
    if r.metrics.clicks or r.metrics.impressions > 1:
        print(f"   replay blocks [{r.ad_group.name[8:]}] '{t}' ${r.metrics.cost_micros/1e6:.2f} {r.metrics.impressions}i ({m[0]})")
print(f"replay: {blocked_n} visible terms blocked, ${blocked_cost:.2f}, none converted")

todo = [(t, "PHRASE") for t in PHRASE]
new = [x for x in todo if x not in negs]
print(f"new negatives {len(new)} (already there: {[x[0] for x in todo if x in negs]})")

ops = []
op = client.get_type("MutateOperation")
op.ad_group_operation.update.resource_name = ga.ad_group_path(CID, AG_REPLACE)
op.ad_group_operation.update.status = client.enums.AdGroupStatusEnum.PAUSED
op.ad_group_operation.update_mask.paths.append("status"); ops.append(op)
op = client.get_type("MutateOperation")
op.campaign_budget_operation.update.resource_name = c.campaign_budget.resource_name
op.campaign_budget_operation.update.amount_micros = int(NEW_BUDGET * 1e6)
op.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(op)
for t, mt in new:
    op = client.get_type("MutateOperation"); cc = op.campaign_criterion_operation.create
    cc.campaign = ga.campaign_path(CID, H); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = getattr(MT, mt); ops.append(op)

req = client.get_type("MutateGoogleAdsRequest")
req.customer_id = CID; req.validate_only = not APPLY; req.mutate_operations.extend(ops)
ga.mutate(request=req)
print(f"{len(ops)} operations ok: pause Heating Replacement, budget -> ${NEW_BUDGET:.2f}, {len(new)} negatives", "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    c, ags, negs = state()
    print(f"read-back: budget=${c.campaign_budget.amount_micros/1e6:.2f} cap=${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
          f"campaign={c.campaign.status.name} ad groups={ags} negatives={len(negs)} missing={[x[0] for x in todo if x not in negs]}")
