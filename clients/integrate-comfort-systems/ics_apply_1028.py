# APPLIED LIVE 2026-10-28 on Edu's go (goal customConversionGoals/6459689709). Do NOT re-run with --apply (budget guards abort).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Integrate Comfort (4571881760), 2026-10-28. fu-109 items 1-3, Edu: "Yes, apply 1, 2 and 3". Total stays $77/d.
1. PMax 22890783804: $50 -> $40/d, and bid on a custom goal "TSD | Calls + Forms (no taps)" instead of the campaign-level
   PHONE_CALL_LEAD goals, which include [TSD] Click to call (CLICK_TO_CALL = taps on the ad's call button; 7 of PMax's 8 conv
   10-09..10-26 vs 1 real 60s call). Goal = Calls from ads (60s) + Landing Page Call + Submit lead form - web (GTM) + Lead form - Submit.
   ghl_* GA4 imports stay out (they double-count the GTM form).
2. NonBranded 24047025253: pause AC Installation & Replacement (197798872025, $244 / 1 lead on DIY + cost terms), Heating &
   Furnace Repair stays the only live ad group; Max Conversions -> Max Clicks, $15 CPC cap; $15 -> $22/d.
3. Branded 23675636592: $12 -> $15/d (15% IS lost to budget).
"""
import sys
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, PMAX, NB, BR = "4571881760", "22890783804", "24047025253", "23675636592"
BUDGETS = {PMAX: (50.0, 40.0), NB: (15.0, 22.0), BR: (12.0, 15.0)}
NB_CAP = 15.0
AG_PAUSE, AG_KEEP = "197798872025", "197798871985"
ACTIONS = ["6657750145", "826596883", "7531889446", "7545300465"]
GOAL_NAME = "TSD | Calls + Forms (no taps)"
CHECK_GOAL = "6454453070"  # existing CSMS goal, only used for validate_only
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
rows = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign.bidding_strategy, campaign.bidding_strategy_type,
    campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
    FROM campaign WHERE campaign.id IN ({PMAX},{NB},{BR})""")}
tot_old = tot_new = 0
for cid, (old, new) in BUDGETS.items():
    r = rows[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: ${cur:.2f}/d -> ${new:.2f} shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count} bid={r.campaign.bidding_strategy_type.name}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")
    tot_old += old; tot_new += new
if abs(tot_old - tot_new) > 0.01: sys.exit("ABORT: total changes")
if rows[NB].campaign.bidding_strategy or rows[NB].campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: NB bidding changed")
ags = {str(r.ad_group.id): r.ad_group.status.name for r in q(f"SELECT ad_group.id, ad_group.status FROM ad_group WHERE campaign.id = {NB}")}
print("NB ad groups:", ags)
if ags.get(AG_PAUSE) != "ENABLED" or ags.get(AG_KEEP) != "ENABLED": sys.exit("ABORT: NB ad groups not as expected")
cfg = q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id = {PMAX}")[0].conversion_goal_campaign_config
print(f"PMax goal config {cfg.goal_config_level.name} custom={cfg.custom_conversion_goal or '-'}")
if cfg.custom_conversion_goal: sys.exit("ABORT: PMax already on a custom goal")
acts = {str(r.conversion_action.id): r.conversion_action.name for r in q("SELECT conversion_action.id, conversion_action.name FROM conversion_action WHERE conversion_action.status = 'ENABLED'")}
if any(a not in acts for a in ACTIONS): sys.exit("ABORT: a goal action is missing or not enabled")
print("goal actions:", [acts[a] for a in ACTIONS])

# --- 1. custom goal + PMax assignment
existing = q(f"SELECT custom_conversion_goal.resource_name FROM custom_conversion_goal WHERE custom_conversion_goal.name = '{GOAL_NAME}'")
if existing:
    goal_rn = existing[0].custom_conversion_goal.resource_name; print("goal already exists:", goal_rn)
else:
    op = client.get_type("CustomConversionGoalOperation"); g = op.create
    g.name = GOAL_NAME; g.status = E.CustomConversionGoalStatusEnum.ENABLED
    for a in ACTIONS: g.conversion_actions.append(f"customers/{CID}/conversionActions/{a}")
    resp = client.get_service("CustomConversionGoalService").mutate_custom_conversion_goals(request={"customer_id": CID, "operations": [op], "validate_only": vo})
    goal_rn = resp.results[0].resource_name if APPLY else None
    print("custom goal create ok", "(validate_only)" if vo else goal_rn)
op = client.get_type("ConversionGoalCampaignConfigOperation"); c = op.update
c.resource_name = f"customers/{CID}/conversionGoalCampaignConfigs/{PMAX}"
c.goal_config_level = E.GoalConfigLevelEnum.CAMPAIGN
c.custom_conversion_goal = goal_rn if APPLY else f"customers/{CID}/customConversionGoals/{CHECK_GOAL}"
op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["goal_config_level", "custom_conversion_goal"]))
client.get_service("ConversionGoalCampaignConfigService").mutate_conversion_goal_campaign_configs(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("PMax goal assignment ok", "(validate_only)" if vo else "APPLIED")

# --- budgets
ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = rows[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

# --- 2. NB Max Clicks + pause AC Installation
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.target_spend.cpc_bid_ceiling_micros = int(NB_CAP * 1e6)
op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("NB Max Clicks $15 ok", "(validate_only)" if vo else "APPLIED")
op = client.get_type("AdGroupOperation")
op.update.resource_name = ga.ad_group_path(CID, AG_PAUSE)
op.update.status = E.AdGroupStatusEnum.PAUSED; op.update_mask.paths.append("status")
client.get_service("AdGroupService").mutate_ad_groups(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("AC Installation pause ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    for r in q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros,
            campaign.primary_status FROM campaign WHERE campaign.id IN ({PMAX},{NB},{BR})"""):
        print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} "
              f"cap ${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} {r.campaign.primary_status.name}")
    print("   NB ad groups:", {r.ad_group.name: r.ad_group.status.name for r in q(f"SELECT ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB}")})
    names = {r.conversion_action.resource_name: r.conversion_action.name for r in q("SELECT conversion_action.resource_name, conversion_action.name FROM conversion_action")}
    for r in q(f"SELECT custom_conversion_goal.name, custom_conversion_goal.conversion_actions FROM custom_conversion_goal WHERE custom_conversion_goal.resource_name = '{goal_rn}'"):
        print(f"   goal '{r.custom_conversion_goal.name}': {[names.get(a, a) for a in r.custom_conversion_goal.conversion_actions]}")
    for r in q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id = {PMAX}"):
        print(f"   PMax goal: {r.conversion_goal_campaign_config.goal_config_level.name} {r.conversion_goal_campaign_config.custom_conversion_goal}")
