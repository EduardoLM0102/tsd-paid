#!/usr/bin/env python3
"""Cool Hand round 2 cutover (same pattern as Proud Pops G2b): for each ad group that got a new RSA from
round2_rsa_drafts_2026-10-08.py, pause the OLD ad(s) ONLY once the new RSA is APPROVED / APPROVED_LIMITED.
Ad groups whose new ad is still under review are skipped, so nothing goes dark. Safe to re-run.
Default validate-only; --apply writes."""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "9865206319"
IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".round2_new_ads.txt")
if not os.path.exists(IDS_FILE): sys.exit("STOP: round 2 RSAs not built yet (no .round2_new_ads.txt)")
NEW = {ag: ad for ag, ad, _ in (l.split() for l in open(IDS_FILE) if l.strip())}
client = init_client(); E = client.enums
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
ops, report = [], []
for ag, new_ad in NEW.items():
    ads = run_query(CID, f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status,
ad_group_ad.policy_summary.review_status FROM ad_group_ad WHERE ad_group.id = {ag} AND ad_group_ad.status != 'REMOVED'""")
    new = [x for x in ads if x["ad_group_ad"]["ad"]["id"] == new_ad]
    if not new: report.append((ag, "NEW AD NOT FOUND")); continue
    ps = new[0]["ad_group_ad"].get("policy_summary", {}); st = str(ps.get("approval_status")); name = new[0]["ad_group"]["name"]
    olds = [x for x in ads if x["ad_group_ad"]["ad"]["id"] != new_ad and str(x["ad_group_ad"]["status"]) == "ENABLED"]
    if st not in ("APPROVED", "APPROVED_LIMITED"):
        report.append((name, f"new ad {new_ad} is {st} / {ps.get('review_status')}: wait, old ad keeps serving")); continue
    for x in olds:
        o = client.get_type("MutateOperation"); u = o.ad_group_ad_operation.update
        u.resource_name = f"customers/{CID}/adGroupAds/{ag}~{x['ad_group_ad']['ad']['id']}"; u.status = E.AdGroupAdStatusEnum.PAUSED
        o.ad_group_ad_operation.update_mask.paths.append("status"); ops.append(o)
    report.append((name, f"new ad APPROVED: pause old {[x['ad_group_ad']['ad']['id'] for x in olds] or 'none left'}"))
for r in report: print("  ", r)
if ops:
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f": pause {len(ops)} old ad(s)")
else:
    print("nothing to pause yet")
