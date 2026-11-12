# APPLIED LIVE 2026-11-04, read-back confirmed (2 negs, none missing). Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Let's add the negatives and wait another week"), Command Center fu-029.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Neon Monkey (7953905280), 2026-11-04: NB Trimming 23825900343, 2 PHRASE competitor negatives (four seasons, wright tree).
NB gets one more week (10-19..11-01: $858, 0 real leads; competitor clicks 'four seasons arbor service', 'wright tree service fort worth').
Replays the negatives against 30d search terms + live keywords first, aborts on a conflict. Budget and $20 cap unchanged."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "7953905280", "23825900343"
NEG = ["four seasons", "wright tree"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

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

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"negatives ({len(neg)}) ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"read-back: NB negatives missing: {[n for n in NEG if n not in got]}")
