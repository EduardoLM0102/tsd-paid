#!/usr/bin/env python3
"""
Stop PMax taking Proud Pops brand searches (Edu: "execute on 2", 2026-10-08), so they go to Branded instead.
  - BRANDS shared set "TSD - Proud Pops brand (PMax exclusion)" with Google brand entities /g/11zy333b8y "Proud Pops" and
    /g/11zbnljsnq "Proud Pops Plumbing, Air & Electric" (both proudpops.com, from BrandSuggestionService), linked to
    PMax Electrical 23866982084 + PMax HVAC 23853595615.
  - Campaign-level PHRASE negatives on both PMax campaigns: proud pops, problem solvers, pops electric, pops electrical
    ("The Problem Solvers" brand entity in Google's database is an unrelated UK company, so the old name is covered by keyword).
Branded Search is untouched. Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"; C = f"customers/{CID}"
PMAX = ["23866982084", "23853595615"]
BRANDS = ["/g/11zy333b8y", "/g/11zbnljsnq"]
NEGS = ["proud pops", "problem solvers", "pops electric", "pops electrical"]
client = init_client(); E = client.enums


def run(validate):
    ops = []
    tmp = f"{C}/sharedSets/-1"
    o = client.get_type("MutateOperation"); ss = o.shared_set_operation.create
    ss.resource_name = tmp; ss.name = "TSD - Proud Pops brand (PMax exclusion)"; ss.type_ = E.SharedSetTypeEnum.BRANDS; ops.append(o)
    for b in BRANDS:
        o = client.get_type("MutateOperation"); sc = o.shared_criterion_operation.create
        sc.shared_set = tmp; sc.brand.entity_id = b; ops.append(o)
    for camp in PMAX:
        # PMax brand exclusions: a negative campaign criterion of type BRAND_LIST (campaign_shared_set links are
        # OPERATION_NOT_PERMITTED_FOR_CONTEXT for BRANDS sets on PMax).
        o = client.get_type("MutateOperation"); bl = o.campaign_criterion_operation.create
        bl.campaign = f"{C}/campaigns/{camp}"; bl.negative = True; bl.brand_list.shared_set = tmp; ops.append(o)
        for kw in NEGS:
            o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
            cc.campaign = f"{C}/campaigns/{camp}"; cc.negative = True
            cc.keyword.text = kw; cc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE; ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK" if validate else "APPLIED") + f": {len(ops)} ops")
    if not validate:
        for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign_criterion.negative, campaign_criterion.brand_list.shared_set, campaign_criterion.status
FROM campaign_criterion WHERE campaign.id IN ({','.join(PMAX)}) AND campaign_criterion.type = 'BRAND_LIST'"""):
            print("READ-BACK brand list exclusion:", r["campaign"]["name"], r["campaign_criterion"])
        for r in run_query(CID, """SELECT shared_set.name, shared_criterion.brand.entity_id FROM shared_criterion WHERE shared_set.type = 'BRANDS'"""):
            print("   member:", r["shared_criterion"].get("brand"))
        for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign_criterion.keyword.text FROM campaign_criterion
WHERE campaign.id IN ({','.join(PMAX)}) AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"""):
            print("READ-BACK PMax negative:", r["campaign"]["name"], r["campaign_criterion"]["keyword"]["text"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    run(validate=not a.apply)
