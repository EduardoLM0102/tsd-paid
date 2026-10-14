"""Checklist B3 (read-only): what would CSMS_Competitors (+ beyer, bryco) block on Plumbing Search 23853484024?
Uses Google negative-match semantics: BROAD = all words present (any order, no close variants), PHRASE = word sequence,
EXACT = whole query. Shows 90-day search terms that would be blocked, plus collisions with our own keywords."""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, CAMP = "1051843378", "23853484024"
f = lambda x: float(x or 0)
toks = lambda s: re.findall(r"[a-z0-9']+", s.lower())
def blocks(neg, mt, q):
    n, w = toks(neg), toks(q)
    if mt == "EXACT": return n == w
    if mt == "PHRASE": return any(w[i:i + len(n)] == n for i in range(len(w) - len(n) + 1))
    return set(n) <= set(w)
negs = [(r["shared_criterion"]["keyword"]["text"], str(r["shared_criterion"]["keyword"]["match_type"]))
        for r in run_query(CID, "SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.id = 11334178042")]
negs += [("beyer", "PHRASE"), ("bryco", "PHRASE")]
print("CSMS_Competitors members (+2 proposed):")
for t, m in sorted(negs): print(f"   {m:7s} {t}")
terms = defaultdict(lambda: [0.0, 0.0, 0.0])
for r in run_query(CID, f"""SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE campaign.id = {CAMP} AND segments.date BETWEEN '2026-07-09' AND '2026-10-06'"""):
    t = terms[r["search_term_view"]["search_term"]]; m = r["metrics"]
    t[0] += f(m.get("clicks")); t[1] += f(m.get("cost_micros")) / 1e6; t[2] += f(m.get("all_conversions"))
print(f"\n90-day Plumbing search terms that WOULD be blocked ({len(terms)} distinct terms checked):")
hit = defaultdict(list)
for q, (c, cost, conv) in terms.items():
    for t, m in negs:
        if blocks(t, m, q): hit[(t, m)].append((q, c, cost, conv))
tc = tcost = tconv = 0
for (t, m), qs in sorted(hit.items()):
    for q, c, cost, conv in sorted(qs, key=lambda x: -x[2]):
        print(f"   [{m} {t}] '{q}'  clk {c:.0f}  ${cost:,.2f}  allconv {conv:.1f}"); tc += c; tcost += cost; tconv += conv
print(f"   TOTAL blocked: {tc:.0f} clicks, ${tcost:,.2f}, {tconv:.1f} all_conversions")
own = [r["ad_group_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE campaign.id = {CAMP} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
coll = [(k, t, m) for k in own for t, m in negs if blocks(t, m, k)]
print(f"\nCollisions with our own {len(own)} Plumbing keywords: {coll or 'none'}")
