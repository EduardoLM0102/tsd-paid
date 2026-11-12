# APPLIED LIVE 2026-11-04, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("change the asset to the right number and get rid of the old disapproved one"), Command Center fu-052.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Proud Pops (1051843378), 2026-11-04: call asset swap.
P-5 answered 11-04 (CallRail via Cowork): (210) 225-5767 = CallRail tracker '210 - CALL POP' (the website swap target); main line 210-997-7190.
1. Link the EXISTING approved asset 428601259336 ((210) 225-5767, created 10-08 by block_b b4, unlinked by b4-revert) at account level
   + on the 6 lead campaigns from block_b_changes_2026-10-07.py (links that already exist are skipped).
2. Remove the old disapproved (210) 794-7570 links: campaign asset 360709032917 on the same 6 campaigns + account asset 185848871539 (if still linked).
Refuses if the new asset isn't APPROVED / APPROVED_LIMITED. One atomic request."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "1051843378"
C = f"customers/{CID}"
LEAD_CAMPAIGNS = {
    "23848895678": "Search HVAC", "23853361615": "Branded", "23853484024": "Search Plumbing",
    "23853595615": "PMax HVAC", "23866982084": "PMax Electrical", "23866999121": "Search Electrical",
}
NEW_ASSET, OLD_CAMPAIGN_ASSET, OLD_ACCOUNT_ASSET = "428601259336", "360709032917", "185848871539"
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))

a = q(f"SELECT asset.id, asset.call_asset.phone_number, asset.policy_summary.approval_status FROM asset WHERE asset.id = {NEW_ASSET}")
if not a: sys.exit("ABORT: new asset not found")
num, st = a[0].asset.call_asset.phone_number, a[0].asset.policy_summary.approval_status.name
print(f"new asset {NEW_ASSET} {num} {st}")
if "225" not in num or "5767" not in num: sys.exit("ABORT: asset number is not (210) 225-5767")
if st not in ("APPROVED", "APPROVED_LIMITED"): sys.exit(f"ABORT: new asset is {st}")

camp_links = {(str(r.campaign.id), str(r.asset.id)): r.campaign_asset.status.name for r in q(
    "SELECT campaign.id, asset.id, campaign_asset.status FROM campaign_asset WHERE campaign_asset.field_type = 'CALL'")}
acct_links = {str(r.asset.id): r.customer_asset.status.name for r in q(
    "SELECT asset.id, customer_asset.status FROM customer_asset WHERE customer_asset.field_type = 'CALL'")}
print("before: account CALL links", acct_links)
print("before: campaign CALL links", {k: v for k, v in camp_links.items() if k[0] in LEAD_CAMPAIGNS})

ops = []
def op(): return client.get_type("MutateOperation")
if acct_links.get(NEW_ASSET) != "ENABLED":
    o = op(); ca = o.customer_asset_operation.create; ca.asset = f"{C}/assets/{NEW_ASSET}"; ca.field_type = E.AssetFieldTypeEnum.CALL; ops.append(o)
for cid in LEAD_CAMPAIGNS:
    if camp_links.get((cid, NEW_ASSET)) != "ENABLED":
        o = op(); cpa = o.campaign_asset_operation.create
        cpa.campaign = f"{C}/campaigns/{cid}"; cpa.asset = f"{C}/assets/{NEW_ASSET}"; cpa.field_type = E.AssetFieldTypeEnum.CALL; ops.append(o)
    if camp_links.get((cid, OLD_CAMPAIGN_ASSET)) == "ENABLED":
        o = op(); o.campaign_asset_operation.remove = f"{C}/campaignAssets/{cid}~{OLD_CAMPAIGN_ASSET}~CALL"; ops.append(o)
if acct_links.get(OLD_ACCOUNT_ASSET) == "ENABLED":
    o = op(); o.customer_asset_operation.remove = f"{C}/customerAssets/{OLD_ACCOUNT_ASSET}~CALL"; ops.append(o)

if ops:
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not APPLY
    ga.mutate(request=req)
print(f"{len(ops)} op(s)", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")
if APPLY:
    for r in q("SELECT asset.id, asset.call_asset.phone_number, customer_asset.status FROM customer_asset WHERE customer_asset.field_type = 'CALL'"):
        print(f"read-back account: {r.asset.id} {r.asset.call_asset.phone_number} {r.customer_asset.status.name}")
    for r in q("SELECT campaign.id, asset.id, asset.call_asset.phone_number, campaign_asset.status FROM campaign_asset WHERE campaign_asset.field_type = 'CALL'"):
        if str(r.campaign.id) in LEAD_CAMPAIGNS:
            print(f"read-back {LEAD_CAMPAIGNS[str(r.campaign.id)]:<17} {r.asset.call_asset.phone_number} {r.campaign_asset.status.name}")
