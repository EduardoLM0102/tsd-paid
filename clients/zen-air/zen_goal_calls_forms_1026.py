# ALREADY APPLIED LIVE 2026-10-26 (goal 6459645015). Kept for the record. Re-running is safe: it reuses the goal by name.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Zen Air (4360840956), 2026-10-26. Point Branded + Non-Branded at a custom goal of only taps, calls and forms.
Approved by Edu in chat ("fix the campaigns to make sure we're optimizing for tap to calls and forms";
picked: goals only, keep Max Clicks / Target IS bidding, leave Peach AI out).

 1. Create custom conversion goal "TSD | Calls + Forms":
      [TSD] Click to call (7769293652)   GTM tag "02 | Google Ads - Phone click", tel: taps on the site
      Calls from ads (1058843888)        60s+ calls from the call asset
      Submit lead form - web (7539810847) GTM "03 | Google Ads - Lead", gated on a real GHL form submit
      Lead form - Submit (7553021219)    Google-hosted lead form asset
    Left out: ghl_* GA4 imports (suspected page views), dead GA4 phone_link_click, Peach AI uploads (double count).
 2. Branded (23675783172): custom goal CMSA -> the new goal. CMSA itself is untouched (old paused campaigns use it).
 3. Non-Branded (24100030790): account-default goals -> the new goal.
Step 1 runs first (custom goals have no temp ids); step 2-3 in one mutate. validate_only covers both.
"""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID = "4360840956"
CAMPS = {"23675783172": "Branded", "24100030790": "Non-Branded"}
ACTIONS = ["7769293652", "1058843888", "7539810847", "7553021219"]
GOAL_NAME = "TSD | Calls + Forms"
APPLY = "--apply" in sys.argv
IN_CAMPS = ", ".join(f"'customers/{CID}/campaigns/{c}'" for c in CAMPS)

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums


def q(s):
    return list(ga.search(customer_id=CID, query=s))


print("--- before")
for r in q("SELECT conversion_goal_campaign_config.campaign, conversion_goal_campaign_config.goal_config_level, "
           "conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config "
           f"WHERE conversion_goal_campaign_config.campaign IN ({IN_CAMPS})"):
    c = r.conversion_goal_campaign_config
    print(f"   {CAMPS[c.campaign.split('/')[-1]]:12s} {c.goal_config_level.name} {c.custom_conversion_goal or '-'}")

existing = [r for r in q(f"SELECT custom_conversion_goal.resource_name, custom_conversion_goal.name FROM custom_conversion_goal "
                         f"WHERE custom_conversion_goal.name = '{GOAL_NAME}'")]
if existing:
    goal_rn = existing[0].custom_conversion_goal.resource_name
    print(f"goal already exists: {goal_rn}")
else:
    svc = client.get_service("CustomConversionGoalService")
    op = client.get_type("CustomConversionGoalOperation")
    g = op.create
    g.name = GOAL_NAME
    g.status = E.CustomConversionGoalStatusEnum.ENABLED
    for a in ACTIONS:
        g.conversion_actions.append(f"customers/{CID}/conversionActions/{a}")
    resp = svc.mutate_custom_conversion_goals(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
    goal_rn = resp.results[0].resource_name if APPLY else f"customers/{CID}/customConversionGoals/0"
    print(f"custom goal create ok{'' if APPLY else ' (validate_only)'}: {goal_rn}")

if not APPLY:
    # an assignment can't be validated against a goal that doesn't exist yet; validate it against CMSA instead
    goal_rn_check = f"customers/{CID}/customConversionGoals/6452365353"
else:
    goal_rn_check = goal_rn

svc = client.get_service("ConversionGoalCampaignConfigService")
ops = []
for camp in CAMPS:
    op = client.get_type("ConversionGoalCampaignConfigOperation")
    c = op.update
    c.resource_name = f"customers/{CID}/conversionGoalCampaignConfigs/{camp}"
    c.goal_config_level = E.GoalConfigLevelEnum.CAMPAIGN
    c.custom_conversion_goal = goal_rn_check
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["goal_config_level", "custom_conversion_goal"]))
    ops.append(op)
svc.mutate_conversion_goal_campaign_configs(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"campaign goal assignment ok{'' if APPLY else ' (validate_only, nothing changed)'}")
if not APPLY:
    sys.exit(0)

print("--- read-back")
for r in q(f"SELECT custom_conversion_goal.name, custom_conversion_goal.status, custom_conversion_goal.conversion_actions "
           f"FROM custom_conversion_goal WHERE custom_conversion_goal.resource_name = '{goal_rn}'"):
    g = r.custom_conversion_goal
    names = {x.conversion_action.resource_name: x.conversion_action.name for x in
             q("SELECT conversion_action.resource_name, conversion_action.name FROM conversion_action")}
    print(f"   goal '{g.name}' {g.status.name}: {[names.get(a, a) for a in g.conversion_actions]}")
for r in q("SELECT conversion_goal_campaign_config.campaign, conversion_goal_campaign_config.goal_config_level, "
           "conversion_goal_campaign_config.custom_conversion_goal, campaign.bidding_strategy_type FROM conversion_goal_campaign_config "
           f"WHERE conversion_goal_campaign_config.campaign IN ({IN_CAMPS})"):
    c = r.conversion_goal_campaign_config
    print(f"   {CAMPS[c.campaign.split('/')[-1]]:12s} {c.goal_config_level.name} {c.custom_conversion_goal} bidding={r.campaign.bidding_strategy_type.name}")
