#!/usr/bin/env python3
"""
Checklist H7 (Edu: "Execute H7 now", 2026-10-08). Search Plumbing 23853484024 (Max Clicks, $45 CPC ceiling).
Give the generic "plumber" head terms their own ad group with a matching ad, instead of sitting in
AG1_Plumbing_LeakDetection (expected CTR below average → QS 4–5 → $45–120 clicks).

  build    Create AG4_Plumbing_General (ENABLED) + 3 keywords + 1 RSA → /services/plumbing.
           The AG1 originals stay ENABLED, so there's no downtime while the new ad is under review (lesson from B7).
  cutover  After the AG4 RSA is APPROVED: pause the 3 generic keywords in AG1 (refuses if the RSA isn't approved).

Copy: every claim verified on proudpops.com 2026-10-08 (Free Pop-In, written price before work, no surprises / no
pressure, photos of what we find, licensed & insured, 24/7 emergency response, "Still Family. Still Local.", fix first,
financing, leaks / drains / water heaters, San Antonio + New Braunfels). NOT used: same-day, 5-star, upfront, trusted.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query

CID, CAMP, OLD_AG = "1051843378", "23853484024", "196726297659"
C = f"customers/{CID}"
AG_NAME = "AG4_Plumbing_General"
URL, PATH1, PATH2 = "https://proudpops.com/services/plumbing", "Plumber", "San-Antonio"
KEYWORDS = [("plumber san antonio", "EXACT"), ("plumber near me", "EXACT"), ("plumber san antonio tx", "PHRASE")]
HEADLINES = [
    "Plumber in San Antonio", "San Antonio Plumbers", "Local San Antonio Plumber", "Need a Plumber? Call Pops",
    "Free Pop-In Visit", "Book Your Free Pop-In", "Written Price Before We Start", "No Surprises, No Pressure",
    "Licensed & Insured Plumbers", "24/7 Emergency Plumbing", "Leaks, Drains, Water Heaters", "Photos of Everything We Find",
    "Still Family. Still Local.", "Fix First, Replace if Needed", "Financing Available",
]
DESCRIPTIONS = [
    "Leak, clog or no hot water? We come out free, show you photos and give a written price.",
    "Licensed, insured plumbers serving San Antonio and New Braunfels. 24/7 emergency response.",
    "No surprise charges. You see the price in writing before any work starts. Book a Pop-In.",
    "Hard water is rough on SA pipes and water heaters. We fix first, replace only if needed.",
]


def check_copy():
    bad = [(h, len(h)) for h in HEADLINES if len(h) > 30] + [(d, len(d)) for d in DESCRIPTIONS if len(d) > 90]
    dashes = [x for x in HEADLINES + DESCRIPTIONS if "—" in x or "–" in x]
    dupes = len(set(HEADLINES)) != len(HEADLINES)
    print(f"copy check: {len(HEADLINES)} headlines (max {max(map(len, HEADLINES))} chars), {len(DESCRIPTIONS)} descriptions "
          f"(max {max(map(len, DESCRIPTIONS))} chars), over-limit={bad or 'none'}, dashes={dashes or 'none'}, duplicates={dupes}")
    assert not bad and not dashes and not dupes and len(PATH1) <= 15 and len(PATH2) <= 15


def build(validate):
    check_copy()
    if run_query(CID, f"SELECT ad_group.id FROM ad_group WHERE campaign.id = {CAMP} AND ad_group.name = '{AG_NAME}' AND ad_group.status != 'REMOVED'"):
        sys.exit(f"STOP: {AG_NAME} already exists")
    client = init_client(); E = client.enums; ops = []
    tmp_ag = f"{C}/adGroups/-1"
    o = client.get_type("MutateOperation"); ag = o.ad_group_operation.create
    ag.resource_name = tmp_ag; ag.name = AG_NAME; ag.campaign = f"{C}/campaigns/{CAMP}"
    ag.status = E.AdGroupStatusEnum.ENABLED; ag.type_ = E.AdGroupTypeEnum.SEARCH_STANDARD
    ops.append(o)
    for text, mt in KEYWORDS:
        o = client.get_type("MutateOperation"); k = o.ad_group_criterion_operation.create
        k.ad_group = tmp_ag; k.status = E.AdGroupCriterionStatusEnum.ENABLED
        k.keyword.text = text; k.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
        ops.append(o)
    o = client.get_type("MutateOperation"); aga = o.ad_group_ad_operation.create
    aga.ad_group = tmp_ag; aga.status = E.AdGroupAdStatusEnum.ENABLED
    aga.ad.final_urls.append(URL)
    rsa = aga.ad.responsive_search_ad; rsa.path1 = PATH1; rsa.path2 = PATH2
    for h in HEADLINES:
        a = client.get_type("AdTextAsset"); a.text = h; rsa.headlines.append(a)
    for d in DESCRIPTIONS:
        a = client.get_type("AdTextAsset"); a.text = d; rsa.descriptions.append(a)
    ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if not validate else "VALIDATE-ONLY OK (nothing written)") + f": ad group + {len(KEYWORDS)} keywords + 1 RSA")
    if not validate:
        readback()


def readback():
    for r in run_query(CID, f"SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {CAMP} AND ad_group.name = '{AG_NAME}'"):
        agid = r["ad_group"]["id"]; print("READ-BACK ad group:", r["ad_group"])
        for k in run_query(CID, f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id = {agid} AND ad_group_criterion.type = 'KEYWORD'"):
            print("   keyword:", k["ad_group_criterion"]["keyword"], k["ad_group_criterion"]["status"])
        for a in run_query(CID, f"""SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.review_status,
ad_group_ad.policy_summary.approval_status, ad_group_ad.ad_strength FROM ad_group_ad WHERE ad_group.id = {agid}"""):
            x = a["ad_group_ad"]; print("   RSA:", x["ad"]["id"], x.get("status"), x["ad"].get("final_urls"), x.get("policy_summary"), "strength:", x.get("ad_strength"))


def cutover(validate):
    rows = run_query(CID, f"SELECT ad_group.id FROM ad_group WHERE campaign.id = {CAMP} AND ad_group.name = '{AG_NAME}'")
    if not rows: sys.exit("STOP: AG4 not built yet")
    agid = rows[0]["ad_group"]["id"]
    ads = run_query(CID, f"SELECT ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group.id = {agid}")
    st = [str(a["ad_group_ad"].get("policy_summary", {}).get("approval_status")) for a in ads]
    print("AG4 RSA approval:", st)
    if not any(s in ("APPROVED", "APPROVED_LIMITED") for s in st):
        sys.exit("REFUSED: AG4's RSA isn't approved yet. The AG1 originals keep serving until it is.")
    olds = run_query(CID, f"""SELECT ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
FROM ad_group_criterion WHERE ad_group.id = {OLD_AG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED'""")
    target = [r for r in olds if (r["ad_group_criterion"]["keyword"]["text"], str(r["ad_group_criterion"]["keyword"]["match_type"])) in KEYWORDS]
    print("AG1 originals to pause:", [(r["ad_group_criterion"]["keyword"]["text"], r["ad_group_criterion"]["criterion_id"]) for r in target])
    client = init_client(); E = client.enums; ops = []
    for r in target:
        o = client.get_type("MutateOperation"); u = o.ad_group_criterion_operation.update
        u.resource_name = f"{C}/adGroupCriteria/{OLD_AG}~{r['ad_group_criterion']['criterion_id']}"; u.status = E.AdGroupCriterionStatusEnum.PAUSED
        o.ad_group_criterion_operation.update_mask.paths.append("status"); ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if not validate else "VALIDATE-ONLY OK") + f": pause {len(ops)} AG1 keywords")
    if not validate:
        for r in run_query(CID, f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id = {OLD_AG} AND ad_group_criterion.type = 'KEYWORD'"):
            print("   AG1:", r["ad_group_criterion"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("step", choices=["build", "cutover", "readback"]); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    {"build": build, "cutover": cutover, "readback": lambda validate: readback()}[a.step](validate=not a.apply)
