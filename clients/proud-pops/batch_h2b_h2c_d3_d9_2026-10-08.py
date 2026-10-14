#!/usr/bin/env python3
"""
Proud Pops, Google Ads batch (Edu OK 2026-10-08): H2b, H2c, D-3, D-9. Account 1051843378.
  h2b  Branded: add EXACT "pops electric" + "pops electrical" to Brand_Electrical (193744394062);
       then EXACT negatives for both on Search Electrical 23866999121 (mirrors Branded's EXACT, so nothing goes dark).
  h2c  Search Electrical: AI Max OFF (campaign.ai_max_setting.enable_ai_max = false).
  d3   Budget-neutral: Branded 23853361615 $70 -> $100/day; PMax HVAC 23853595615 $325 -> $295/day (total unchanged).
       Asserts both budgets are non-shared (reference_count == 1). Plain micros.
  d9   Remove EXACT "electricians for hire" (customer intent) from CSMS_Negatives 11330296375.
Default validate-only; --apply writes; read-back after each.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"; C = f"customers/{CID}"
ELEC, BRANDED, PMAX_HVAC, BRAND_ELEC_AG, CSMS_NEG = "23866999121", "23853361615", "23853595615", "193744394062", "11330296375"
BRAND_TERMS = ["pops electric", "pops electrical"]
BUDGETS = {BRANDED: 100_000_000, PMAX_HVAC: 295_000_000}   # micros/day
client = init_client(); E = client.enums


def run(ops, validate, label):
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(f"[{label}] " + ("VALIDATE-ONLY OK" if validate else "APPLIED") + f" ({len(ops)} op)")


def h2b(validate):
    ops = []
    for t in BRAND_TERMS:
        o = client.get_type("MutateOperation"); k = o.ad_group_criterion_operation.create
        k.ad_group = f"{C}/adGroups/{BRAND_ELEC_AG}"; k.status = E.AdGroupCriterionStatusEnum.ENABLED
        k.keyword.text = t; k.keyword.match_type = E.KeywordMatchTypeEnum.EXACT; ops.append(o)
    for t in BRAND_TERMS:
        o = client.get_type("MutateOperation"); n = o.campaign_criterion_operation.create
        n.campaign = f"{C}/campaigns/{ELEC}"; n.negative = True
        n.keyword.text = t; n.keyword.match_type = E.KeywordMatchTypeEnum.EXACT; ops.append(o)
    run(ops, validate, "h2b")
    if not validate:
        print("   Branded:", [(r["ad_group_criterion"]["keyword"], r["ad_group_criterion"]["status"]) for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
FROM ad_group_criterion WHERE ad_group.id = {BRAND_ELEC_AG} AND ad_group_criterion.type = 'KEYWORD'""") if r["ad_group_criterion"]["keyword"]["text"] in BRAND_TERMS])
        print("   Electrical negatives:", [r["campaign_criterion"]["keyword"] for r in run_query(CID, f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion WHERE campaign.id = {ELEC} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""") if r["campaign_criterion"]["keyword"]["text"] in BRAND_TERMS])


def h2c(validate):
    o = client.get_type("MutateOperation"); u = o.campaign_operation.update
    u.resource_name = f"{C}/campaigns/{ELEC}"; u.ai_max_setting.enable_ai_max = False
    # Google rejects AI Max off while text customization (an AI Max feature) is OPTED_IN -> AI_MAX_MUST_BE_ENABLED.
    # So switch both AI Max text features off in the same op (URL expansion was already OPTED_OUT by H1).
    for t in ("TEXT_ASSET_AUTOMATION", "FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION"):
        st = client.get_type("Campaign").AssetAutomationSetting()
        st.asset_automation_type = getattr(E.AssetAutomationTypeEnum, t)
        st.asset_automation_status = E.AssetAutomationStatusEnum.OPTED_OUT
        u.asset_automation_settings.append(st)
    o.campaign_operation.update_mask.paths.extend(["ai_max_setting.enable_ai_max", "asset_automation_settings"])
    run([o], validate, "h2c")
    if not validate:
        r = run_query(CID, f"SELECT campaign.ai_max_setting.enable_ai_max, campaign.asset_automation_settings FROM campaign WHERE campaign.id = {ELEC}")[0]["campaign"]
        print("   READ-BACK ai_max:", r.get("ai_max_setting", {}).get("enable_ai_max", False), "| automation:",
              {x["asset_automation_type"]: x["asset_automation_status"] for x in r.get("asset_automation_settings", [])})


def d3(validate):
    rows = run_query(CID, f"""SELECT campaign.id, campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros,
campaign_budget.reference_count, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id IN ({BRANDED}, {PMAX_HVAC})""")
    before = {r["campaign"]["id"]: r for r in rows}
    total_before = sum(int(r["campaign_budget"]["amount_micros"]) for r in rows)
    total_after = sum(BUDGETS.values())
    for cid, r in before.items():
        b = r["campaign_budget"]
        print(f"   {r['campaign']['name'][:40]:40s} ${int(b['amount_micros']) / 1e6:.0f} -> ${BUDGETS[cid] / 1e6:.0f}  refs={b.get('reference_count')} shared={b.get('explicitly_shared', False)}")
        assert int(b.get("reference_count", 0)) == 1 and not b.get("explicitly_shared", False), "budget is shared, STOP"
    assert total_before == total_after, f"not budget-neutral: {total_before} vs {total_after}"
    print(f"   total ${total_before / 1e6:.0f} -> ${total_after / 1e6:.0f} (neutral)")
    ops = []
    for cid, r in before.items():
        o = client.get_type("MutateOperation"); u = o.campaign_budget_operation.update
        u.resource_name = r["campaign_budget"]["resource_name"]; u.amount_micros = BUDGETS[cid]
        o.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(o)
    run(ops, validate, "d3")
    if not validate:
        for r in run_query(CID, f"SELECT campaign.name, campaign_budget.amount_micros FROM campaign WHERE campaign.id IN ({BRANDED}, {PMAX_HVAC})"):
            print(f"   READ-BACK {r['campaign']['name'][:40]:40s} ${int(r['campaign_budget']['amount_micros']) / 1e6:.2f}/day")


def d9(validate):
    rows = [r for r in run_query(CID, f"""SELECT shared_criterion.criterion_id, shared_criterion.keyword.text, shared_criterion.keyword.match_type
FROM shared_criterion WHERE shared_set.id = {CSMS_NEG}""") if r["shared_criterion"]["keyword"]["text"] == "electricians for hire"]
    assert len(rows) == 1, rows
    o = client.get_type("MutateOperation"); o.shared_criterion_operation.remove = f"{C}/sharedCriteria/{CSMS_NEG}~{rows[0]['shared_criterion']['criterion_id']}"
    run([o], validate, "d9")
    if not validate:
        left = [r for r in run_query(CID, f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {CSMS_NEG}") if r["shared_criterion"]["keyword"]["text"] == "electricians for hire"]
        print("   READ-BACK still present:", bool(left))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("steps", nargs="+", choices=["h2b", "h2c", "d3", "d9"]); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    for s in a.steps:
        {"h2b": h2b, "h2c": h2c, "d3": d3, "d9": d9}[s](validate=not a.apply)
