#!/usr/bin/env python3
"""G2b (Edu: execute, 2026-10-08): for each ad group that got a new site-verified RSA (G2a, and later G2c), pause the OLD ad(s)
ONLY once the new RSA is APPROVED / APPROVED_LIMITED. Ad groups whose new ad is still under review are skipped (no downtime).
Safe to re-run any time. Default validate-only; --apply writes; read-back after."""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
NEW = {  # ad_group_id: new RSA ad id (G2a 2026-10-08). G2c adds more below.
    "199431304209": "827482059110", "196768586637": "827482059113", "195955611119": "827482059116",
    "195220521334": "827482059119", "202213821731": "827482059242",
}
G2C_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".g2c_new_ads.txt")
if os.path.exists(G2C_FILE):
    for line in open(G2C_FILE):
        if line.strip(): ag, ad = line.split(); NEW[ag] = ad
client = init_client(); E = client.enums
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
ops, report = [], []
for ag, new_ad in NEW.items():
    ads = run_query(CID, f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status
FROM ad_group_ad WHERE ad_group.id = {ag} AND ad_group_ad.status != 'REMOVED'""")
    new = [x for x in ads if x["ad_group_ad"]["ad"]["id"] == new_ad]
    if not new: report.append((ag, "NEW AD NOT FOUND")); continue
    st = str(new[0]["ad_group_ad"].get("policy_summary", {}).get("approval_status"))
    olds = [x for x in ads if x["ad_group_ad"]["ad"]["id"] != new_ad and str(x["ad_group_ad"]["status"]) == "ENABLED"]
    name = new[0]["ad_group"]["name"]
    if st not in ("APPROVED", "APPROVED_LIMITED"):
        report.append((name, f"new ad {new_ad} is {st} / {new[0]['ad_group_ad'].get('policy_summary', {}).get('review_status')} → wait, old ad(s) keep serving")); continue
    for x in olds:
        o = client.get_type("MutateOperation"); u = o.ad_group_ad_operation.update
        u.resource_name = f"customers/{CID}/adGroupAds/{ag}~{x['ad_group_ad']['ad']['id']}"; u.status = E.AdGroupAdStatusEnum.PAUSED
        o.ad_group_ad_operation.update_mask.paths.append("status"); ops.append(o)
    report.append((name, f"new ad APPROVED → pause old {[x['ad_group_ad']['ad']['id'] for x in olds] or 'none left'}"))
for r in report: print("  ", r)
if ops:
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f": pause {len(ops)} old ad(s)")
else:
    print("nothing to pause yet")
