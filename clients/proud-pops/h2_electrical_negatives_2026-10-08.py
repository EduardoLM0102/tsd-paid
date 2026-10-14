#!/usr/bin/env python3
"""
Checklist H2: campaign-level negatives on Search Electrical 23866999121, built from the Sep 8 – Oct 7 search terms.
Default validate-only; --apply writes; read-back after. Prints, before any write:
  - what each negative would have blocked (Google negative semantics: BROAD = all words, PHRASE = word sequence)
  - collisions with Electrical's own keywords and with Branded's keywords
  - candidates already covered by existing negatives (skipped)
  - AI Max vs keyword spend/all_conversions split
"""
import sys, os, re, argparse
from collections import defaultdict
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query

CID, CAMP, BRANDED = "1051843378", "23866999121", "23853361615"
S, U = "2026-09-08", "2026-10-07"
CANDIDATES = {
    "competitor": [(t, "PHRASE") for t in (
        "q electric", "mission city electric", "wattsmith", "snyder electric", "elevate electrical", "genesis electric",
        "genesis electrician", "d & g electrical", "hays electrical", "advanced electrical contractors", "finlee",
        "turney electric", "m & r electrical", "chain electric", "cfa electric", "bates electric", "sa classic electric",
        "goettl", "wrangler", "service experts", "jaydylan", "willfixit", "american home shield", "goodman", "trane")],
    "off-service": [("plumbers", "BROAD"), ("plumer", "BROAD"), ("climas", "BROAD"), ("a c repair", "PHRASE"),
                    ("ac service", "PHRASE"), ("ac technician", "PHRASE"), ("boerne ac", "PHRASE"),
                    ("leak detection", "PHRASE"), ("appliance installer", "PHRASE"), ("customer service", "PHRASE")],
    # "pops electric"/"pops electrical" HELD 2026-10-08: Branded only has "proud pops ..." keywords, so negating them here would
    # leave those brand searches with no ad. Add them to Branded first (H2b), then negate. "pops ac" is AC = off-service here.
    "own brand / off-service": [("pops ac", "PHRASE")],
}
f = lambda x: float(x or 0)
toks = lambda s: re.findall(r"[a-z0-9'&]+", s.lower())


def blocks(neg, mt, q):
    n, w = toks(neg), toks(q)
    if mt == "EXACT": return n == w
    if mt == "PHRASE": return any(w[i:i + len(n)] == n for i in range(len(w) - len(n) + 1))
    return set(n) <= set(w)


# search terms (with match source)
terms = defaultdict(lambda: [0.0, 0.0, 0.0]); src = defaultdict(lambda: [0.0, 0.0, 0.0])
for r in run_query(CID, f"""SELECT search_term_view.search_term, segments.search_term_match_source, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S}' AND '{U}'"""):
    m = r["metrics"]; t = terms[r["search_term_view"]["search_term"]]; s_ = src[str(r["segments"].get("search_term_match_source"))]
    for x in (t, s_):
        x[0] += f(m.get("clicks")); x[1] += f(m.get("cost_micros")) / 1e6; x[2] += f(m.get("all_conversions"))
print("AI MAX vs KEYWORDS (30d, visible terms): " + " | ".join(f"{k}: ${v[1]:,.0f}, {v[0]:.0f} clk, {v[2]:.1f} all_conv, ${v[1] / v[2] if v[2] else 0:,.0f}/all_conv" for k, v in src.items()))

# existing negatives that already apply to Electrical
existing = [(r["campaign_criterion"]["keyword"]["text"], str(r["campaign_criterion"]["keyword"]["match_type"])) for r in run_query(CID, f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")]
for sid in ("11330296375", "12263521315"):  # CSMS_Negatives (attached), account-level list
    existing += [(r["shared_criterion"]["keyword"]["text"], str(r["shared_criterion"]["keyword"]["match_type"])) for r in run_query(CID, f"SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.id = {sid}")]
own_kw = [r["ad_group_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE campaign.id = {CAMP} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
brand_kw = [(r["ad_group_criterion"]["keyword"]["text"], str(r["ad_group_criterion"]["keyword"]["match_type"])) for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion
WHERE campaign.id = {BRANDED} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
print(f"\nBranded keywords mentioning 'pops' ({len(brand_kw)} total):", sorted(f"{m}:{t}" for t, m in brand_kw if "pops" in t))

final, total_saved = [], 0.0
for group, cands in CANDIDATES.items():
    print(f"\n== {group}")
    for neg, mt in cands:
        if any(blocks(e, em, neg) for e, em in existing):
            print(f"   SKIP (already covered)  {mt:6s} {neg}"); continue
        coll = [k for k in own_kw if blocks(neg, mt, k)]
        hit = {q: v for q, v in terms.items() if blocks(neg, mt, q)}
        cost = sum(v[1] for v in hit.values()); total_saved += cost
        flag = f"  !! COLLIDES with own keyword(s) {coll}" if coll else ""
        print(f"   {mt:6s} {neg:32s} blocks {len(hit):2d} terms, ${cost:7,.2f}  e.g. {list(hit)[:3]}{flag}")
        if not coll:
            final.append((neg, mt))
print(f"\nPROPOSED: {len(final)} negatives; 30-day spend on the terms they block: ${total_saved:,.2f}")
# safety: any blocked term that looks like core customer intent?
CORE = re.compile(r"\b(electrician|electricians|electrical|electric)\b.*\b(near me|san antonio|boerne|new braunfels|repair|install|service)\b")
risky = sorted({q for q in terms for n, m in final if blocks(n, m, q) and CORE.search(q) and not re.search(r"q electric|mission city|snyder|elevate|genesis|d & g|hays|advanced electrical|turney|m & r|chain electric|cfa|bates|classic|pops|trane|wattsmith|finlee", q)})
print("Blocked terms that look like core customer intent (review):", risky or "none")

ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
client = init_client(); E = client.enums
ops = []
for neg, mt in final:
    o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
    cc.campaign = f"customers/{CID}/campaigns/{CAMP}"; cc.negative = True
    cc.keyword.text = neg; cc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
    ops.append(o)
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
client.get_service("GoogleAdsService").mutate(request=req)
print(("APPLIED " if a.apply else "VALIDATE-ONLY OK (nothing written): ") + f"{len(ops)} campaign-level negatives on Search Electrical")
if a.apply:
    now = {(r["campaign_criterion"]["keyword"]["text"], str(r["campaign_criterion"]["keyword"]["match_type"])) for r in run_query(CID, f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print("READ-BACK: present", sum((n, m) in now for n, m in final), "of", len(final))
