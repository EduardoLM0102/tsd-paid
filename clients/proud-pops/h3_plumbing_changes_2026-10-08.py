#!/usr/bin/env python3
"""
Checklist H3a/H3b/H3c (Edu: "Execute H3a, H3b, H3c", 2026-10-08). Account 1051843378, Search Plumbing 23853484024.
  h3a  Pause keyword "leak detection near me" PHRASE in AG1_Plumbing_LeakDetection (196726297659)
  h3b  Bidding: Maximize Conversions (no target) -> Maximize Clicks (TARGET_SPEND) with a $45.00 max CPC ceiling
  h3c  Add PHRASE "aramendia" to CSMS_Competitors (11334178042, attached to Plumbing only)
Default validate-only; --apply writes; read-back after each.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID, CAMP, AG = "1051843378", "23853484024", "196726297659"
CEILING = 45_000_000  # micros = $45.00 (plain micros, NOT the update.py centavos convention)
client = init_client(); E = client.enums
C = f"customers/{CID}"


def mutate(ops, validate, label):
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(f"[{label}] " + ("VALIDATE-ONLY OK" if validate else "APPLIED"))


def h3a(validate):
    rows = run_query(CID, f"""SELECT ad_group_criterion.criterion_id, ad_group_criterion.status, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
FROM ad_group_criterion WHERE ad_group.id = {AG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.keyword.text = 'leak detection near me'""")
    rows = [r for r in rows if str(r["ad_group_criterion"]["keyword"]["match_type"]) == "PHRASE"]
    assert len(rows) == 1, f"expected 1 PHRASE 'leak detection near me', got {rows}"
    kid = rows[0]["ad_group_criterion"]["criterion_id"]; print("[h3a] before:", rows[0]["ad_group_criterion"]["status"], "criterion", kid)
    o = client.get_type("MutateOperation"); u = o.ad_group_criterion_operation.update
    u.resource_name = f"{C}/adGroupCriteria/{AG}~{kid}"; u.status = E.AdGroupCriterionStatusEnum.PAUSED
    o.ad_group_criterion_operation.update_mask.paths.append("status")
    mutate([o], validate, "h3a")
    if not validate:
        r = run_query(CID, f"SELECT ad_group_criterion.status, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.id = {AG} AND ad_group_criterion.criterion_id = {kid}")[0]
        print("[h3a] READ-BACK:", r["ad_group_criterion"])


def h3b(validate):
    before = run_query(CID, f"SELECT campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros FROM campaign WHERE campaign.id = {CAMP}")[0]["campaign"]
    print("[h3b] before:", before)
    o = client.get_type("MutateOperation"); u = o.campaign_operation.update
    u.resource_name = f"{C}/campaigns/{CAMP}"
    u.target_spend.cpc_bid_ceiling_micros = CEILING
    o.campaign_operation.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
    mutate([o], validate, "h3b")
    if not validate:
        r = run_query(CID, f"SELECT campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign.status FROM campaign WHERE campaign.id = {CAMP}")[0]["campaign"]
        print("[h3b] READ-BACK:", r.get("bidding_strategy_type"), "| ceiling $", int(r.get("target_spend", {}).get("cpc_bid_ceiling_micros", 0)) / 1e6, "| status", r.get("status"))


def h3c(validate):
    o = client.get_type("MutateOperation"); sc = o.shared_criterion_operation.create
    sc.shared_set = f"{C}/sharedSets/11334178042"; sc.keyword.text = "aramendia"; sc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
    mutate([o], validate, "h3c")
    if not validate:
        rows = [r["shared_criterion"]["keyword"] for r in run_query(CID, "SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.id = 11334178042")
                if r["shared_criterion"]["keyword"]["text"] == "aramendia"]
        print("[h3c] READ-BACK:", rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("step", choices=["h3a", "h3b", "h3c", "all"]); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    for step in (["h3a", "h3b", "h3c"] if a.step == "all" else [a.step]):
        {"h3a": h3a, "h3b": h3b, "h3c": h3c}[step](validate=not a.apply)
