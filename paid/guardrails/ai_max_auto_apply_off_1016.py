# APPLIED LIVE 2026-10-16 on Edu's go ("deactivate AI Max in GENERAL and any autoapply"). Re-running is safe (only touches what is still ON).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""TSD guardrail, 2026-10-16, Edu: "can you deactivate AI Max in GENERAL and any autoapply shit we have?"
For every CURRENT client account under MCC 4155514468 (allow-list below):
1. Auto-apply: every ENABLED recommendation_subscription -> PAUSED. UNKNOWN-type subscriptions can't be changed via the API
   (seen on All Seasons 10-14), so they are listed for UI and skipped.
2. AI Max: campaign.ai_max_setting.enable_ai_max -> False on every non-removed Search campaign (paused ones too, so a later
   re-enable doesn't bring AI Max back), with AI Max's text customization (TEXT_ASSET_AUTOMATION) and final URL expansion
   opted out in the same operation (the API rejects AI Max off while they're on: AI_MAX_MUST_BE_ENABLED).
Left out on purpose (not current / not run by TSD): All Heart 9205826499, Strickland 9049508615 (On Purpose Media),
DFW _Unsuspended 1932181525, Gray Duct 6191956550, Bucksworth x3 (Concrete Adventures x2 added 2026-10-22, it IS current), and every account with nothing to change.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

ACCOUNTS = {
    "4467722415": "All Seasons AC", "8655979348": "All Seasons AC - LSA", "5563867754": "C&S Air", "9865206319": "Cool Hand Electric",
    "2198608170": "Hawkins Siding", "4571881760": "Integrate Comfort", "2175964343": "ICS LSA Carlsta", "8323145223": "ICS LSA Englewood",
    "2895702982": "ICS LSA Bellevue", "6769493219": "King's Window", "3797438623": "Lilypad Septic", "8634274092": "Mission Accomplished",
    "4904262993": "Mission Accomplished - LSA", "9509605037": "Napps", "9239407401": "Napps - LSA", "7953905280": "Neon Monkey",
    "1219885876": "Neon Monkey - LSA", "1854100356": "Nick's Heating", "1051843378": "Proud Pops", "7261668241": "Proud Pops LSA SA1",
    "6621969129": "Proud Pops LSA SA2", "2524618054": "Spencer Air", "3651667805": "Watt's Right Tulsa", "9261944882": "Watt's Right BA",
    "4360840956": "Zen Air", "3740502923": "Zen Air - LSA", "4193142570": "Golden Plumbing", "8513856629": "TopServ Digital (own)",
    "9215192296": "Concrete Adventures", "2898153501": "Concrete Adventures - LSA",  # added 2026-10-22: current client
}
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
RS = client.enums.RecommendationSubscriptionStatusEnum
rec_svc = client.get_service("RecommendationSubscriptionService")
camp_svc = client.get_service("CampaignService")
ui_only, totals = [], {"subs": 0, "ai": 0}

def scan(cid):
    subs = [r.recommendation_subscription for r in ga.search(customer_id=cid, query="""SELECT recommendation_subscription.resource_name,
        recommendation_subscription.type, recommendation_subscription.status FROM recommendation_subscription""")]
    ai = [r.campaign for r in ga.search(customer_id=cid, query="""SELECT campaign.resource_name, campaign.name, campaign.status,
        campaign.ai_max_setting.enable_ai_max FROM campaign WHERE campaign.status != 'REMOVED' AND campaign.advertising_channel_type = 'SEARCH'""")
          if r.campaign.ai_max_setting.enable_ai_max]
    return [s for s in subs if s.status.name == "ENABLED"], ai

for cid, name in ACCOUNTS.items():
    subs_on, ai_on = scan(cid)
    fixable = [s for s in subs_on if s.type.name != "UNKNOWN"]
    unknown = len(subs_on) - len(fixable)
    if unknown: ui_only.append((name, cid, unknown))
    if not fixable and not ai_on:
        continue
    print(f"{cid} {name}: auto-apply to pause {[s.type.name for s in fixable]}"
          f"{f' (+{unknown} UNKNOWN, UI only)' if unknown else ''} | AI Max off on {[(c.name, c.status.name) for c in ai_on]}")
    for s in fixable:
        op = client.get_type("RecommendationSubscriptionOperation")
        op.update.resource_name = s.resource_name; op.update.status = RS.PAUSED
        op.update_mask.paths.append("status")
        rec_svc.mutate_recommendation_subscription(request={"customer_id": cid, "operations": [op], "validate_only": vo})
        totals["subs"] += 1
    if ai_on:
        ops = []
        for c in ai_on:
            op = client.get_type("CampaignOperation")
            op.update.resource_name = c.resource_name; op.update.ai_max_setting.enable_ai_max = False
            # AI Max's text customization + final URL expansion only exist with AI Max on, so opt them out in the same op
            for t in ("TEXT_ASSET_AUTOMATION", "FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION"):
                a = client.get_type("Campaign").AssetAutomationSetting()
                a.asset_automation_type = client.enums.AssetAutomationTypeEnum[t]
                a.asset_automation_status = client.enums.AssetAutomationStatusEnum.OPTED_OUT
                op.update.asset_automation_settings.append(a)
            op.update_mask.paths.extend(["ai_max_setting.enable_ai_max", "asset_automation_settings"]); ops.append(op)
        camp_svc.mutate_campaigns(request={"customer_id": cid, "operations": ops, "validate_only": vo})
        totals["ai"] += len(ops)
    if APPLY:
        s2, a2 = scan(cid)
        left = [s.type.name for s in s2 if s.type.name != "UNKNOWN"]
        print(f"   read-back: auto-apply still ON (non-UNKNOWN) {left} | AI Max still ON {[c.name for c in a2]}")

print(f"\n{'APPLIED' if APPLY else 'validate_only OK'}: {totals['subs']} auto-apply subscriptions paused, AI Max off on {totals['ai']} campaigns")
print("UI-only (UNKNOWN auto-apply types):", ui_only)
