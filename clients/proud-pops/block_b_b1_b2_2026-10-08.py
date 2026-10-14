#!/usr/bin/env python3
"""
Proud Pops — checklist B1 + B2 via API (2026-10-08). Account 1051843378.
DEFAULT IS VALIDATE-ONLY. Add --apply to write. Every --apply run reads back.

  b1   PMax URL exclusion: negative WEBPAGE campaign criterion "URL contains /careers" on
       PMax Electrical 23866982084 and PMax HVAC 23853595615 (stops Final URL expansion sending traffic there).
  b2   Account-level negative keywords (cover PMax too): new ACCOUNT_LEVEL_NEGATIVE_KEYWORDS shared set,
       8 BROAD + 14 PHRASE terms (refined after collision check), attached to the account. Prints collisions with live keywords + 90-day search terms first.

Run: ./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_b1_b2_2026-10-08.py b1 [--apply]
"""
import sys, os, re, argparse
from collections import defaultdict
SKILL = os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
sys.path.insert(0, SKILL)
from lib import init_client, run_query

CID = "1051843378"
C = f"customers/{CID}"
PMAX = {"23866982084": "PMax Electrical", "23853595615": "PMax HVAC"}
# Refined 2026-10-08 after the collision check: bare "job"/"jobs"/"hiring" BROAD would block customer searches
# ("electrician near me for small jobs", "hiring electrician near me"). Single words only where unambiguous;
# job-seeker wording as PHRASE.
JOB_TERMS = [(w, "BROAD") for w in ("careers", "career", "apprentice", "apprenticeship", "salary",
                                     "employment", "indeed", "resume")] + \
            [(w, "PHRASE") for w in ("now hiring", "who's hiring", "hiring now", "near me hiring", "job openings",
                                     "jobs near me", "electrician jobs", "electrical jobs", "plumbing jobs",
                                     "plumber jobs", "hvac jobs", "hvac technician job", "hvac technician jobs",
                                     "hvac tech jobs")]
client = init_client()
E = client.enums
f = lambda x: float(x or 0)
toks = lambda s: re.findall(r"[a-z0-9']+", s.lower())


def blocks(neg, mt, q):
    n, w = toks(neg), toks(q)
    if mt == "PHRASE":
        return any(w[i:i + len(n)] == n for i in range(len(w) - len(n) + 1))
    return set(n) <= set(w)  # BROAD negative: all words present, no close variants


def mutate(ops, validate):
    req = client.get_type("MutateGoogleAdsRequest")
    req.customer_id = CID
    req.mutate_operations.extend(ops)
    req.validate_only = validate
    resp = client.get_service("GoogleAdsService").mutate(request=req)
    print(f"VALIDATE-ONLY OK: {len(ops)} op(s) accepted. Nothing written." if validate else f"APPLIED: {len(ops)} op(s).")
    if not validate:
        for r in resp.mutate_operation_responses:
            print("   ", str(r).strip().replace("\n", " ")[:150])


def b1(validate):
    existing = run_query(CID, f"""SELECT campaign.id, campaign_criterion.criterion_id, campaign_criterion.negative,
campaign_criterion.webpage.conditions FROM campaign_criterion
WHERE campaign_criterion.type = 'WEBPAGE' AND campaign.id IN ({','.join(PMAX)})""")
    print("existing WEBPAGE criteria on PMax:", [(r["campaign"]["id"], r["campaign_criterion"].get("webpage")) for r in existing] or "none")
    ops = []
    for cid in PMAX:
        o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
        cc.campaign = f"{C}/campaigns/{cid}"
        cc.negative = True
        cc.webpage.criterion_name = "Exclude careers (job applications)"
        cond = client.get_type("WebpageConditionInfo")
        cond.operand = E.WebpageConditionOperandEnum.URL
        cond.operator = E.WebpageConditionOperatorEnum.CONTAINS
        cond.argument = "/careers"
        cc.webpage.conditions.append(cond)
        ops.append(o)
    mutate(ops, validate)
    if not validate:
        for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign_criterion.negative, campaign_criterion.status,
campaign_criterion.webpage.criterion_name, campaign_criterion.webpage.conditions FROM campaign_criterion
WHERE campaign_criterion.type = 'WEBPAGE' AND campaign.id IN ({','.join(PMAX)})"""):
            print("READ-BACK:", r["campaign"]["name"], r["campaign_criterion"])


def b2(validate):
    # collision check: BROAD negative single word blocks any query containing that word
    kws = run_query(CID, """SELECT campaign.name, ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'
AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")
    coll = [(r["campaign"]["name"], r["ad_group_criterion"]["keyword"]["text"], t) for r in kws for t, m in JOB_TERMS
            if blocks(t, m, r["ad_group_criterion"]["keyword"]["text"])]
    print(f"collisions with {len(kws)} live keywords:", coll or "none")
    terms = defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in run_query(CID, """SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE segments.date BETWEEN '2026-07-10' AND '2026-10-07'"""):
        t = terms[r["search_term_view"]["search_term"]]; m = r["metrics"]
        t[0] += f(m.get("clicks")); t[1] += f(m.get("cost_micros")) / 1e6; t[2] += f(m.get("all_conversions"))
    hit = {q: v for q, v in terms.items() if any(blocks(t, m, q) for t, m in JOB_TERMS)}
    print(f"90-day search terms that would be blocked ({len(terms)} checked): {len(hit)}")
    for q, (c, cost, conv) in sorted(hit.items(), key=lambda x: -x[1][1])[:15]:
        print(f"   '{q}'  clk {c:.0f}  ${cost:,.2f}  allconv {conv:.1f}")
    existing = run_query(CID, "SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.status FROM shared_set WHERE shared_set.type = 'ACCOUNT_LEVEL_NEGATIVE_KEYWORDS'")
    print("existing account-level negative lists:", [r["shared_set"] for r in existing] or "none")
    if existing:
        sys.exit("STOP: an account-level list already exists; add terms to it instead of creating a second one.")
    tmp = f"{C}/sharedSets/-1"
    o = client.get_type("MutateOperation"); ss = o.shared_set_operation.create
    ss.resource_name = tmp; ss.name = "TSD - Account negatives (job seekers)"; ss.type_ = E.SharedSetTypeEnum.ACCOUNT_LEVEL_NEGATIVE_KEYWORDS
    ops = [o]
    for w, mt in JOB_TERMS:
        o = client.get_type("MutateOperation"); sc = o.shared_criterion_operation.create
        sc.shared_set = tmp; sc.keyword.text = w; sc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
        ops.append(o)
    o = client.get_type("MutateOperation"); cn = o.customer_negative_criterion_operation.create
    cn.negative_keyword_list.shared_set = tmp
    ops.append(o)
    mutate(ops, validate)
    if not validate:
        for r in run_query(CID, "SELECT shared_set.id, shared_set.name, shared_set.member_count, shared_set.status FROM shared_set WHERE shared_set.type = 'ACCOUNT_LEVEL_NEGATIVE_KEYWORDS'"):
            print("READ-BACK list:", r["shared_set"])
        for r in run_query(CID, "SELECT customer_negative_criterion.id, customer_negative_criterion.type, customer_negative_criterion.negative_keyword_list.shared_set FROM customer_negative_criterion WHERE customer_negative_criterion.type = 'NEGATIVE_KEYWORD_LIST'"):
            print("READ-BACK attached:", r["customer_negative_criterion"])


ACCOUNT_LIST = f"{C}/sharedSets/12263521315"   # TSD - Account negatives (job seekers), created by b2 on 2026-10-08
CSMS_NEGATIVES_ID = "11330296375"
SINGULAR_GAPS = ["electrician job", "plumber job", "hvac job", "hvac tech job"]


def b2b(validate):
    """Remove BROAD job/jobs from CSMS_Negatives (they block customer searches like 'small jobs');
    cover the singular job-seeker gap with PHRASE terms in the account-level list."""
    rows = run_query(CID, f"""SELECT shared_criterion.criterion_id, shared_criterion.keyword.text, shared_criterion.keyword.match_type
FROM shared_criterion WHERE shared_set.id = {CSMS_NEGATIVES_ID}""")
    target = [r for r in rows if r["shared_criterion"]["keyword"]["text"] in ("job", "jobs")
              and str(r["shared_criterion"]["keyword"]["match_type"]) == "BROAD"]
    print("to remove from CSMS_Negatives:", [(r["shared_criterion"]["keyword"]["text"], r["shared_criterion"]["criterion_id"]) for r in target])
    if len(target) != 2:
        sys.exit("STOP: expected exactly BROAD job + jobs in CSMS_Negatives")
    kws = run_query(CID, """SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD'
AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")
    coll = [(k["ad_group_criterion"]["keyword"]["text"], t) for k in kws for t in SINGULAR_GAPS if blocks(t, "PHRASE", k["ad_group_criterion"]["keyword"]["text"])]
    print("singular-gap PHRASE collisions with live keywords:", coll or "none")
    terms = {}
    for r in run_query(CID, """SELECT search_term_view.search_term, metrics.clicks FROM search_term_view
WHERE segments.date BETWEEN '2026-07-10' AND '2026-10-07'"""):
        terms[r["search_term_view"]["search_term"]] = 1
    newly_blocked = [q for q in terms if any(blocks(t, "PHRASE", q) for t in SINGULAR_GAPS)]
    unblocked = [q for q in terms if (set(toks(q)) & {"job", "jobs"}) and not any(blocks(t, m, q) for t, m in JOB_TERMS + [(g, "PHRASE") for g in SINGULAR_GAPS])]
    print("90-day terms newly blocked by the singular phrases:", newly_blocked or "none")
    print("90-day terms UNBLOCKED by removing BROAD job/jobs (should be customer intent):", unblocked or "none")
    ops = []
    for r in target:
        o = client.get_type("MutateOperation")
        o.shared_criterion_operation.remove = f"{C}/sharedCriteria/{CSMS_NEGATIVES_ID}~{r['shared_criterion']['criterion_id']}"
        ops.append(o)
    for t in SINGULAR_GAPS:
        o = client.get_type("MutateOperation"); sc = o.shared_criterion_operation.create
        sc.shared_set = ACCOUNT_LIST; sc.keyword.text = t; sc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
        ops.append(o)
    mutate(ops, validate)
    if not validate:
        left = [r["shared_criterion"]["keyword"]["text"] for r in run_query(CID, f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {CSMS_NEGATIVES_ID}")]
        print("READ-BACK CSMS_Negatives still has job/jobs:", [w for w in left if w in ("job", "jobs")] or "no", f"| members now {len(left)}")
        acct = [f"{r['shared_criterion']['keyword']['match_type']}:{r['shared_criterion']['keyword']['text']}" for r in run_query(CID, "SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.id = 12263521315")]
        print(f"READ-BACK account list ({len(acct)}):", [a for a in acct if any(g in a for g in SINGULAR_GAPS)])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["b1", "b2", "b2b"])
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    {"b1": b1, "b2": b2, "b2b": b2b}[a.step](validate=not a.apply)
