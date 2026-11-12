# APPLIED LIVE 2026-10-16 on Edu's go ("can you do that account-wide for me?"). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Proud Pops (1051843378), 2026-10-16, Edu: "can you do that account-wide for me?" (competitor / off-service negatives).
Adds PHRASE negatives to the existing ACCOUNT-LEVEL list 'TSD - Account negatives (job seekers)' (12263521315, attached at
customer level, so it covers Search + PMax). Terms come from the Oct 1-15 search-term check plus the 26 San Antonio
plumbing competitors in CSMS_Competitors (attached only to one paused campaign).
Deliberately NOT added: 'phone number' (would block 'proud pops phone number' on Branded), 'plumer' (a misspelling of
plumber = real intent), 'mobile home' (may be serviceable), and appliance words (stove/oven/washer/dryer/refrigerator):
the replay showed they block real electrician jobs ('4 prong dryer outlet', 'washer breaker keeps tripping').
Guards: aborts if the list isn't account-level/attached; replays against Aug 17-Oct 15 search terms + every non-removed keyword.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, LIST_ID = "1051843378", "12263521315"
NEG = ["elmer", "above all air", "gillette air", "sigma air", "service experts", "wattsmith", "goodman phone",
       "appliance repair", "roof leak", "roofing",
       "nest error", "error code", "how to", "diy"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

ss = q(f"SELECT shared_set.resource_name, shared_set.name, shared_set.type FROM shared_set WHERE shared_set.id = {LIST_ID}")[0].shared_set
attached = [r for r in q("SELECT customer_negative_criterion.negative_keyword_list.shared_set FROM customer_negative_criterion WHERE customer_negative_criterion.type = 'NEGATIVE_KEYWORD_LIST'")
            if r.customer_negative_criterion.negative_keyword_list.shared_set == ss.resource_name]
print(f"list '{ss.name}' type {ss.type.name} attached at account level: {bool(attached)}")
if not attached: sys.exit("ABORT: list not attached at account level")

comp = [r.shared_criterion.keyword.text.lower() for r in q("SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = 11334178042")]
present = {r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {LIST_ID}")}
ALL = list(dict.fromkeys(NEG + comp))
new = [t for t in ALL if t not in present]
print(f"{len(new)} new (incl. {len(comp)} from CSMS_Competitors); already present: {[t for t in ALL if t in present]}")

terms = q("""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE segments.date BETWEEN '2026-08-17' AND '2026-10-15' AND metrics.impressions > 0""")
kws = [r.ad_group_criterion.keyword.text.lower() for r in q("""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'
    AND campaign.status != 'REMOVED'""")]
bad = []
for t in new:
    hit = [r for r in terms if f" {t} " in f" {r.search_term_view.search_term.lower()} "]
    conf = sorted({k for k in kws if f" {t} " in f" {k} "})
    if hit or conf:
        print(f"  '{t}': blocks {len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {sum(r.metrics.conversions for r in hit):.1f}"
              f" e.g. {sorted({r.search_term_view.search_term for r in hit})[:3]}{' KW CONFLICT ' + str(conf[:5]) if conf else ''}")
    if conf: bad.append(t)
if bad: sys.exit(f"ABORT: conflicts with existing keywords: {bad}")

ops = []
for t in new:
    op = client.get_type("SharedCriterionOperation"); c = op.create
    c.shared_set = ss.resource_name; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("SharedCriterionService").mutate_shared_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} account-level negatives ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    got = {r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {LIST_ID}")}
    print(f"--- read-back: list now has {len(got)} terms; missing: {[t for t in ALL if t not in got]}")
