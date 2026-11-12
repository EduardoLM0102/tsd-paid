# APPLIED LIVE 2026-11-04, read-back confirmed (list 43 → 48). Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("apply the 5 negatives"), Command Center fu-083.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), 2026-11-04: 5 PHRASE negatives on the shared list 'TSD Negatives - Oxford (10.22)' 12280924077
(attached to both TSD_10.22 Search campaigns): yasen, dabin, stonhard, stontec, ideas (DIY epoxy product brands + research).
Replays them against all search terms since launch + live keywords first; aborts on a keyword conflict."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, SET = "9215192296", "12280924077"
CAMPS = "24379794681,24379794684"
NEG = ["yasen", "dabin", "stonhard", "stontec", "ideas"]
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

existing = {r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {SET}")}
print(f"list {SET}: {len(existing)} negatives today")
terms = q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view
    WHERE campaign.id IN ({CAMPS}) AND segments.date BETWEEN '2026-10-22' AND '2026-11-04' AND metrics.impressions > 0""")
kws = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id IN ({CAMPS}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
neg = [n for n in NEG if n not in existing]
conflict = False
for n in NEG:
    hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
    kc = [k for k in kws if f" {n} " in f" {k} "]
    conflict |= bool(kc)
    print(f"neg '{n}': {'ALREADY THERE ' if n in existing else ''}blocks {len(hit)} terms {[h.search_term_view.search_term for h in hit][:5]}, "
          f"${sum(t.metrics.cost_micros for t in hit)/1e6:.2f}; kw conflicts: {kc}")
if conflict: sys.exit("ABORT: a negative blocks a live keyword")

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg:
    op = client.get_type("SharedCriterionOperation"); c = op.create
    c.shared_set = ga.shared_set_path(CID, SET); c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("SharedCriterionService").mutate_shared_criteria(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"{len(ops)} negatives", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    got = {r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {SET}")}
    print(f"read-back: list now {len(got)} negatives, missing: {[n for n in NEG if n not in got]}")
