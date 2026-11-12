# APPLIED LIVE 2026-11-06, read-back confirmed (26 negs, none missing). Do NOT re-run with --apply.
# Edu's go 2026-11-06 ("apply those negatives you proposed"), from the fu-129 day-2 check; includes the 5 EV negs pending since fu-117.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Watt's Right (3651667805), staged in the 11-06 fu-129 check. Budgets + tCPA unchanged.
Nonbranded 23832838033: PHRASE negatives = job/trade, public EV charging, competitor names, EV research. Replays them against 30d search terms + live keywords first, aborts on a conflict.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "3651667805", "23832838033"
NEG = ["electrical technician",
       "charging station near me", "charging stations near me", "chargepoint charging station", "charge point app", "charge point charging station", "tesla com", "power electronics",
       "wright way electric", "buxton electric", "edison electric", "lighthouse electric", "marrs electric", "oil capital electric",
       "setter electric", "vintage electric", "hypower", "coleman electric", "coleman electrician", "owen electric", "emc tulsa",
       "tesla in tulsa", "ev connect", "ford charging station", "if i buy a tesla", "how long does it take"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

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

# --- mutation
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
    got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]}")
