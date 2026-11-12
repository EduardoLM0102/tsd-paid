# APPLIED LIVE 2026-10-27 on Edu's go, read-back confirmed (tCPA $95, 7 negs, NB LIMITED status). Do NOT re-run with --apply.
# Edu's go 2026-10-27 ("Number 2 and 3 are good to go"), Command Center fu-096. PMax taps (#1) NOT included, pending CallRail check.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Watt's Right (3651667805), staged in the 10-27 recheck. Budgets unchanged ($235/d):
1. Nonbranded 23832838033: target CPA $80 -> $95 on Maximize Conversions.
2. Nonbranded: 7 PHRASE negatives (2 competitors + 5 EV research).
Aborts on unexpected current values; replays negatives against 30d search terms + live keywords first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "3651667805", "23832838033"
TCPA_OLD, TCPA_NEW = 80.0, 95.0
NEG = ["genesis 1 3", "aa electric", "tesla tulsa", "xeal", "j1772", "nissan leaf", "cost to charge"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
r = q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.maximize_conversions.target_cpa_micros,
    campaign_budget.amount_micros FROM campaign WHERE campaign.id = {NB}""")[0]
cur = r.campaign.maximize_conversions.target_cpa_micros / 1e6
print(f"{r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} tCPA ${cur:.2f}")
if r.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS" or r.campaign.bidding_strategy:
    sys.exit("ABORT: Nonbranded is not standard Maximize Conversions")
if abs(cur - TCPA_OLD) > 0.01: sys.exit(f"ABORT: tCPA ${cur:.2f}, expected ${TCPA_OLD:.2f}")

# --- safety replay of negatives (30d)
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

# --- mutations
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.maximize_conversions.target_cpa_micros = int(TCPA_NEW * 1e6)
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("NB tCPA ok", "(validate_only)" if vo else "APPLIED")

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"negatives ({len(neg)}) ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    r = q(f"SELECT campaign.name, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id = {NB}")[0]
    print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d tCPA ${r.campaign.maximize_conversions.target_cpa_micros/1e6:.2f} {r.campaign.primary_status.name}")
    got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]}")
