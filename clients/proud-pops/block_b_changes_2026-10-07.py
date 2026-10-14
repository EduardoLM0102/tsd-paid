#!/usr/bin/env python3
"""
Proud Pops — checklist Block B account changes (2026-10-07). Account 1051843378.
See clients/proud-pops/internal-checklist-2026-10.md.

DEFAULT IS VALIDATE-ONLY (Google checks the request, nothing is written). Add --apply to write.
Every --apply run reads back from the API afterwards; tick the checklist on the read-back, not the mutate response.

  b3          Add PHRASE negatives "beyer", "bryco" to CSMS_Competitors (11334178042) and attach that list to
              Search Plumbing 23853484024.
  b4          Create call asset (210) 225-5767 -> Calls from ads (6569241485); link at account level + on the
              6 lead campaigns. Old disapproved 210-794-7570 links stay until b4-cleanup.
  b4-cleanup  Remove the old 210-794-7570 links (campaign asset 360709032917 on 6 campaigns + account asset
              185848871539). Refuses unless the new asset is APPROVED / not disapproved.
  b4-revert   Undo b4: remove the new (210) 225-5767 links (account + 6 campaigns). Old links untouched.
  b5          Calls from ads (6569241485): minimum call duration 15s -> 60s.
  b7          Swap final URLs on 6 Search ads (Electrical + Plumbing) to the service pages.

Run from the skill scripts dir:
  ./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b5            (validate)
  ./tsd.sh ~/Documents/GitHub/topserv-workspace/clients/proud-pops/block_b_changes_2026-10-07.py b5 --apply    (write)
"""
import sys, os, argparse

SKILL = os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
sys.path.insert(0, SKILL)
from lib import init_client, run_query

CID = "1051843378"
C = f"customers/{CID}"
LEAD_CAMPAIGNS = {
    "23848895678": "Search HVAC", "23853361615": "Branded", "23853484024": "Search Plumbing",
    "23853595615": "PMax HVAC", "23866982084": "PMax Electrical", "23866999121": "Search Electrical",
}
CALLS_FROM_ADS = f"{C}/conversionActions/6569241485"
NEW_NUMBER = "(210) 225-5767"
OLD_CAMPAIGN_ASSET = "360709032917"
OLD_ACCOUNT_ASSET = "185848871539"
CSMS_COMPETITORS = f"{C}/sharedSets/11334178042"
SEARCH_PLUMBING = "23853484024"
B7_URLS = {  # ad_id: new final URL
    "809528123698": "https://proudpops.com/services/electrical",               # AG1_Electrician_NearMe
    "809490621054": "https://proudpops.com/services/electrical",               # AG2_Electrical_Services
    "809490671193": "https://proudpops.com/services/electrical",               # AG3_Electrical_Repair
    "808814916930": "https://proudpops.com/services/plumbing",                 # AG1_Plumbing_LeakDetection (generic plumber terms)
    "808929407402": "https://proudpops.com/services/plumbing",                 # AG2_Plumbing_Emergency
    "808929711767": "https://proudpops.com/services/plumbing/water-heaters",   # AG3_Plumbing_WaterHeaters
}

client = init_client()
E = client.enums


def mutate(ops, validate):
    svc = client.get_service("GoogleAdsService")
    req = client.get_type("MutateGoogleAdsRequest")
    req.customer_id = CID
    req.mutate_operations.extend(ops)
    req.validate_only = validate
    resp = svc.mutate(request=req)
    if validate:
        print(f"VALIDATE-ONLY OK: {len(ops)} operation(s) accepted by Google. Nothing written. Re-run with --apply.")
    else:
        print(f"APPLIED: {len(ops)} operation(s).")
        for r in resp.mutate_operation_responses:
            print("   ", str(r).strip().replace("\n", " ")[:160])
    return resp


def op():
    return client.get_type("MutateOperation")


def b3(validate):
    ops = []
    for word in ("beyer", "bryco"):
        o = op(); sc = o.shared_criterion_operation.create
        sc.shared_set = CSMS_COMPETITORS
        sc.keyword.text = word
        sc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
        ops.append(o)
    o = op(); css = o.campaign_shared_set_operation.create
    css.campaign = f"{C}/campaigns/{SEARCH_PLUMBING}"
    css.shared_set = CSMS_COMPETITORS
    ops.append(o)
    mutate(ops, validate)
    if not validate:
        print("READ-BACK:")
        for r in run_query(CID, "SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.id = 11334178042"):
            if r["shared_criterion"]["keyword"]["text"] in ("beyer", "bryco"):
                print("   in list:", r["shared_criterion"]["keyword"])
        for r in run_query(CID, "SELECT campaign.id, campaign.status, shared_set.name, campaign_shared_set.status FROM campaign_shared_set WHERE shared_set.id = 11334178042"):
            print("   attached:", r["campaign"]["id"], r["shared_set"]["name"], r["campaign_shared_set"]["status"])


def b4(validate):
    tmp = f"{C}/assets/-1"
    o = op(); a = o.asset_operation.create
    a.resource_name = tmp
    a.call_asset.country_code = "US"
    a.call_asset.phone_number = NEW_NUMBER
    a.call_asset.call_conversion_reporting_state = E.CallConversionReportingStateEnum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION
    a.call_asset.call_conversion_action = CALLS_FROM_ADS
    ops = [o]
    o = op(); ca = o.customer_asset_operation.create
    ca.asset = tmp; ca.field_type = E.AssetFieldTypeEnum.CALL
    ops.append(o)
    for cid in LEAD_CAMPAIGNS:
        o = op(); cpa = o.campaign_asset_operation.create
        cpa.campaign = f"{C}/campaigns/{cid}"; cpa.asset = tmp; cpa.field_type = E.AssetFieldTypeEnum.CALL
        ops.append(o)
    mutate(ops, validate)
    if not validate:
        readback_calls()


def readback_calls():
    print("READ-BACK call assets:")
    for r in run_query(CID, "SELECT asset.id, asset.call_asset.phone_number, asset.policy_summary.approval_status, asset.policy_summary.review_status FROM asset WHERE asset.type = 'CALL'"):
        print("   asset", r["asset"].get("id"), r["asset"].get("call_asset", {}).get("phone_number"), r["asset"].get("policy_summary"))
    for r in run_query(CID, "SELECT campaign.id, campaign.status, asset.id, asset.call_asset.phone_number, campaign_asset.status, campaign_asset.primary_status FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' AND campaign.status = 'ENABLED'"):
        print("   campaign", r["campaign"]["id"], r["asset"]["call_asset"].get("phone_number"), r["campaign_asset"].get("status"), r["campaign_asset"].get("primary_status"))
    for r in run_query(CID, "SELECT asset.id, asset.call_asset.phone_number, customer_asset.status, customer_asset.primary_status FROM customer_asset WHERE customer_asset.field_type = 'CALL'"):
        print("   account", r["asset"]["call_asset"].get("phone_number"), r["customer_asset"].get("status"), r["customer_asset"].get("primary_status"))


def b4_cleanup(validate):
    new = [r for r in run_query(CID, "SELECT asset.id, asset.call_asset.phone_number, asset.policy_summary.approval_status FROM asset WHERE asset.type = 'CALL'")
           if r["asset"].get("call_asset", {}).get("phone_number", "").replace(" ", "") in ("(210)225-5767", "210-225-5767", "2102255767")]
    if not new:
        sys.exit("REFUSED: new 210-225-5767 call asset not found. Run b4 --apply first.")
    status = str(new[0]["asset"].get("policy_summary", {}).get("approval_status"))
    print("new asset", new[0]["asset"]["id"], "approval_status =", status)
    if status not in ("APPROVED", "APPROVED_LIMITED"):
        sys.exit(f"REFUSED: new call asset is {status}, not approved yet. Old links stay until it is.")
    ops = []
    for cid in LEAD_CAMPAIGNS:
        o = op(); o.campaign_asset_operation.remove = f"{C}/campaignAssets/{cid}~{OLD_CAMPAIGN_ASSET}~CALL"; ops.append(o)
    o = op(); o.customer_asset_operation.remove = f"{C}/customerAssets/{OLD_ACCOUNT_ASSET}~CALL"; ops.append(o)
    mutate(ops, validate)
    if not validate:
        readback_calls()


NEW_ASSET = "428601259336"   # (210) 225-5767, created by b4 --apply on 2026-10-08


def b4_revert(validate):
    """Undo b4: remove the new (210) 225-5767 links (account + 6 campaigns). Old 794-7570 links are untouched."""
    ops = []
    for cid in LEAD_CAMPAIGNS:
        o = op(); o.campaign_asset_operation.remove = f"{C}/campaignAssets/{cid}~{NEW_ASSET}~CALL"; ops.append(o)
    o = op(); o.customer_asset_operation.remove = f"{C}/customerAssets/{NEW_ASSET}~CALL"; ops.append(o)
    mutate(ops, validate)
    if not validate:
        readback_calls()


def b5(validate):
    o = op(); ca = o.conversion_action_operation.update
    ca.resource_name = CALLS_FROM_ADS
    ca.phone_call_duration_seconds = 60
    o.conversion_action_operation.update_mask.paths.append("phone_call_duration_seconds")
    mutate([o], validate)
    if not validate:
        for r in run_query(CID, "SELECT conversion_action.name, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = 6569241485"):
            print("READ-BACK:", r["conversion_action"])


def b7(validate):
    ops = []
    for ad_id, url in B7_URLS.items():
        o = op(); ad = o.ad_operation.update
        ad.resource_name = f"{C}/ads/{ad_id}"
        ad.final_urls.append(url)
        o.ad_operation.update_mask.paths.append("final_urls")
        ops.append(o)
    mutate(ops, validate)
    if not validate:
        ids = ",".join(B7_URLS)
        for r in run_query(CID, f"SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({ids})"):
            print("READ-BACK:", r["ad_group"]["name"], r["ad_group_ad"]["ad"]["id"], r["ad_group_ad"]["ad"].get("final_urls"), r["ad_group_ad"].get("policy_summary", {}).get("approval_status"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["b3", "b4", "b4-cleanup", "b4-revert", "b5", "b7"])
    ap.add_argument("--apply", action="store_true", help="write for real (default: validate-only)")
    a = ap.parse_args()
    {"b3": b3, "b4": b4, "b4-cleanup": b4_cleanup, "b4-revert": b4_revert, "b5": b5, "b7": b7}[a.step](validate=not a.apply)
