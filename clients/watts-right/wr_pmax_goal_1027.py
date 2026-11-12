# APPLIED LIVE 2026-10-27, goal 6459658990, read-back confirmed. Re-running is safe (reuses goal by name, aborts if PMax already on a custom goal).
# Edu's go 2026-10-27 ("Ok, apply #1"), Command Center fu-096. Re-running is safe: it reuses the goal by name.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Watt's Right (3651667805), 2026-10-27. Take [TSD] Click to call (CLICK_TO_CALL = taps on the ad's call button) out of PMax bidding.
It shares PHONE_CALL_LEAD / CALL_FROM_ADS with Calls from ads, so campaign_conversion_goal can't split them: use a custom goal.

 1. Create custom conversion goal "TSD | Calls + Forms (no taps)" = everything PMax bids on today minus the taps:
      Calls from ads (978295624)                 AD_CALL, 60s+          (PHONE_CALL_LEAD / CALL_FROM_ADS)
      Phone Call (7131022071)                    CallRail upload, 60s+  (DEFAULT / WEBSITE)
      Submit lead form - web (7550516373)        GTM form               (SUBMIT_LEAD_FORM / WEBSITE)
      Form Submission [Landing Page] (7520838635) upload                (QUALIFIED_LEAD / WEBSITE)
 2. PMax 23833205176: account-default goals -> the new goal. Nonbranded + Branded untouched. Old goals CSMS / CSMS Pmax untouched.
validate_only checks the assignment against the existing CSMS Pmax goal (custom goals have no temp ids).
"""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, PM = "3651667805", "23833205176"
ACTIONS = ["978295624", "7131022071", "7550516373", "7520838635"]
GOAL_NAME = "TSD | Calls + Forms (no taps)"
CHECK_GOAL = "6454664763"  # CSMS Pmax, only used for validate_only
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))
CFG = f"customers/{CID}/conversionGoalCampaignConfigs/{PM}"

print("--- before")
for r in q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal, "
           f"campaign.bidding_strategy_type FROM conversion_goal_campaign_config WHERE campaign.id = {PM}"):
    c = r.conversion_goal_campaign_config
    print(f"   PMax {c.goal_config_level.name} custom={c.custom_conversion_goal or '-'} bidding={r.campaign.bidding_strategy_type.name}")
    if c.custom_conversion_goal: sys.exit("ABORT: PMax already on a custom goal, re-check before changing")

existing = q(f"SELECT custom_conversion_goal.resource_name FROM custom_conversion_goal WHERE custom_conversion_goal.name = '{GOAL_NAME}'")
if existing:
    goal_rn = existing[0].custom_conversion_goal.resource_name; print(f"goal already exists: {goal_rn}")
else:
    op = client.get_type("CustomConversionGoalOperation"); g = op.create
    g.name = GOAL_NAME; g.status = E.CustomConversionGoalStatusEnum.ENABLED
    for a in ACTIONS: g.conversion_actions.append(f"customers/{CID}/conversionActions/{a}")
    resp = client.get_service("CustomConversionGoalService").mutate_custom_conversion_goals(
        request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
    goal_rn = resp.results[0].resource_name if APPLY else None
    print(f"custom goal create ok{'' if APPLY else ' (validate_only)'}: {goal_rn or '-'}")

op = client.get_type("ConversionGoalCampaignConfigOperation"); c = op.update
c.resource_name = CFG
c.goal_config_level = E.GoalConfigLevelEnum.CAMPAIGN
c.custom_conversion_goal = goal_rn if APPLY else f"customers/{CID}/customConversionGoals/{CHECK_GOAL}"
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["goal_config_level", "custom_conversion_goal"]))
client.get_service("ConversionGoalCampaignConfigService").mutate_conversion_goal_campaign_configs(
    request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"PMax goal assignment ok{'' if APPLY else ' (validate_only, nothing changed)'}")
if not APPLY: sys.exit(0)

print("--- read-back")
names = {r.conversion_action.resource_name: r.conversion_action.name for r in q("SELECT conversion_action.resource_name, conversion_action.name FROM conversion_action")}
for r in q(f"SELECT custom_conversion_goal.name, custom_conversion_goal.status, custom_conversion_goal.conversion_actions FROM custom_conversion_goal "
           f"WHERE custom_conversion_goal.resource_name = '{goal_rn}'"):
    g = r.custom_conversion_goal; print(f"   goal '{g.name}' {g.status.name}: {[names.get(a, a) for a in g.conversion_actions]}")
for r in q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal, campaign.name, "
           f"campaign.bidding_strategy_type FROM conversion_goal_campaign_config WHERE campaign.id = {PM}"):
    c = r.conversion_goal_campaign_config
    print(f"   {r.campaign.name}: {c.goal_config_level.name} {c.custom_conversion_goal} bidding={r.campaign.bidding_strategy_type.name}")
