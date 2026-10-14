#!/usr/bin/env python3
"""Checklist H1 (Edu OK 2026-10-08): turn OFF AI Max final URL expansion on Search Electrical 23866999121.
Only FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION changes (OPTED_IN -> OPTED_OUT). AI Max itself and text customization
(TEXT_ASSET_AUTOMATION) are left exactly as they are. Default validate-only; --apply writes; read-back after."""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID, CAMP = "1051843378", "23866999121"
client = init_client(); E = client.enums
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()

def current():
    r = run_query(CID, f"SELECT campaign.name, campaign.ai_max_setting.enable_ai_max, campaign.asset_automation_settings FROM campaign WHERE campaign.id = {CAMP}")[0]["campaign"]
    return r.get("ai_max_setting", {}).get("enable_ai_max"), {x["asset_automation_type"]: x["asset_automation_status"] for x in r.get("asset_automation_settings", [])}

ai_max, settings = current()
print("BEFORE: ai_max =", ai_max, "| automation =", settings)
target = dict(settings); target["FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION"] = "OPTED_OUT"
o = client.get_type("MutateOperation"); c = o.campaign_operation.update
c.resource_name = f"customers/{CID}/campaigns/{CAMP}"
for t, st in target.items():   # repeated field is replaced as a whole, so resend every entry
    s = client.get_type("Campaign").AssetAutomationSetting()
    s.asset_automation_type = getattr(E.AssetAutomationTypeEnum, t)
    s.asset_automation_status = getattr(E.AssetAutomationStatusEnum, st)
    c.asset_automation_settings.append(s)
o.campaign_operation.update_mask.paths.append("asset_automation_settings")
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.append(o); req.validate_only = not a.apply
client.get_service("GoogleAdsService").mutate(request=req)
print("APPLIED" if a.apply else "VALIDATE-ONLY OK (nothing written)", "-> target automation =", target)
if a.apply:
    ai_max2, settings2 = current()
    print("READ-BACK: ai_max =", ai_max2, "| automation =", settings2)
