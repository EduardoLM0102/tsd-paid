#!/usr/bin/env python3
"""
Proud Pops, Google Ads (Edu OK 2026-10-14 ~22:50 CT): client cut the budget to $25k/month. Account 1051843378.
  October had already spent $28,105 through Oct 14 (3 accts), so Oct can't land at $25k. Edu chose the lowest
  overshoot that keeps brand demand: BRANDED ONLY for Oct 15-31 -> Oct lands ~$30k.
  Pause (status only, budgets untouched so the Nov 1 restore starts from known values):
    Search Electrical 23866999121, Search HVAC 23848895678, Search Plumbing 23853484024,
    PMax HVAC 23853595615, PMax Electrical 23866982084,
    YouTube San Antonio 24120440530, YouTube New Braunfels 24120482524 (VIDEO: --youtube, may be API-blocked -> UI)
  Stays on: Branded 23853361615 ($100/d) + the 3 LSA surfaces (demand-limited, ~$20/d combined).
  Nov 1 restore to the $25k pace = nov_restore_25k_2026-11-01.py (Command Center follow-up).
Asserts each campaign is still ENABLED. Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
SEARCH_PMAX = {
    "23866999121": "Search Electrical",
    "23848895678": "Search HVAC",
    "23853484024": "Search Plumbing",
    "23853595615": "PMax HVAC",
    "23866982084": "PMax Electrical",
}
YOUTUBE = {
    "24120440530": "YouTube San Antonio",
    "24120482524": "YouTube New Braunfels",
}
client = init_client()


def status(ids):
    q = f"SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status FROM campaign WHERE campaign.id IN ({', '.join(ids)})"
    return {r["campaign"]["id"]: r["campaign"] for r in run_query(CID, q)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--youtube", action="store_true", help="pause the 2 YouTube campaigns too (separate request)")
    a = ap.parse_args()
    targets = YOUTUBE if a.youtube else SEARCH_PMAX
    before = status(targets)
    assert set(before) == set(targets), f"missing campaigns: {set(targets) - set(before)}"
    ops = []
    for cid, label in targets.items():
        c = before[cid]
        print(f"   {label:22s} {c['name'][:50]:50s} {c['status']} -> PAUSED")
        assert c["status"] == "ENABLED", f"{label} is {c['status']}, not ENABLED, STOP"
        o = client.get_type("MutateOperation"); u = o.campaign_operation.update
        u.resource_name = f"customers/{CID}/campaigns/{cid}"
        u.status = client.enums.CampaignStatusEnum.PAUSED
        o.campaign_operation.update_mask.paths.append("status"); ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID
    req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f" ({len(ops)} ops)")
    if a.apply:
        after = status(targets)
        for cid, label in targets.items():
            s = after[cid]["status"]
            print(f"   READ-BACK {label:22s} {s} " + ("OK" if s == "PAUSED" else "MISMATCH"))


if __name__ == "__main__":
    main()
