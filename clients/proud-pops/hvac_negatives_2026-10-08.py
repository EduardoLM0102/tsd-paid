#!/usr/bin/env python3
"""HVAC search-term sweep (Edu: "execute on 1", 2026-10-08): campaign-level negatives on Search HVAC 23848895678.
Competitor names with zero conversions + RV AC. Deliberately NOT blocked:
  - commercial HVAC (the site says "Residential & Commercial")
  - "cheapest ac repair" (customer intent)
  - equipment brands (Ruud, Pioneer = owners of that equipment)
  - "alamo air conditioning" (competitor, but 2 conversions)
  - "sa specialist" (ambiguous)
Collision check vs own keywords; prints what each would have blocked (30d). Default validate-only; --apply writes."""
import sys, os, re, argparse
from collections import defaultdict
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID, CAMP = "1051843378", "23848895678"
NEGS = [(t, "PHRASE") for t in ("airco", "cowboys ac", "beluga air", "sa specialties", "atlas ac", "ems home services", "one hour air",
                                 "statewide ac")] + [("rv", "BROAD")]
toks = lambda s: re.findall(r"[a-z0-9'&]+", s.lower()); f = lambda x: float(x or 0)
def blocks(n, mt, q):
    n, w = toks(n), toks(q)
    return any(w[i:i + len(n)] == n for i in range(len(w) - len(n) + 1)) if mt == "PHRASE" else set(n) <= set(w)
terms = defaultdict(lambda: [0.0, 0.0])
for r in run_query(CID, f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.all_conversions FROM search_term_view
WHERE campaign.id = {CAMP} AND segments.date BETWEEN '2026-09-08' AND '2026-10-07'"""):
    t = terms[r["search_term_view"]["search_term"]]; t[0] += f(r["metrics"].get("cost_micros")) / 1e6; t[1] += f(r["metrics"].get("all_conversions"))
own = [r["ad_group_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {CAMP}
AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
total = 0.0
for n, mt in NEGS:
    hit = {q: v for q, v in terms.items() if blocks(n, mt, q)}; c = sum(v[0] for v in hit.values()); total += c
    coll = [k for k in own if blocks(n, mt, k)]
    print(f"   {mt:6s} {n:18s} blocks {list(hit)[:3]} ${c:,.2f} conv {sum(v[1] for v in hit.values()):.1f}" + (f"  !! COLLIDES {coll}" if coll else ""))
    assert not coll
print(f"30-day spend on blocked terms: ${total:,.2f}")
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
client = init_client(); E = client.enums; ops = []
for n, mt in NEGS:
    o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
    cc.campaign = f"customers/{CID}/campaigns/{CAMP}"; cc.negative = True; cc.keyword.text = n; cc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt); ops.append(o)
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
client.get_service("GoogleAdsService").mutate(request=req)
print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f": {len(ops)} negatives on Search HVAC")
if a.apply:
    now = {r["campaign_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("READ-BACK present:", sum(n in now for n, _ in NEGS), "of", len(NEGS))
