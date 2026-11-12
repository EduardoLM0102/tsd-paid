# APPLIED LIVE 2026-11-12 (Edu: "Go"), read-back OK. Do NOT re-run with --apply (aborts: campaign not PAUSED).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]
"""Integrate Comfort (4571881760): relaunch NonBranded 24047025253 on the new heating landing page.

Why: the page Sha built (icshvac.com/furnace-heating-repair-northern-nj/, live 11-12, checked vs the brief) replaces the old
ad URL that redirected twice to a page with no form (QS 3, LP below average). The campaign was paused 11-11 at $281 / 0 real leads.

Changes (heating ad group 197798871985 only; AC ad groups stay paused):
 1. Campaign goal -> custom goal 6459689709 'TSD | Calls + Forms (no taps)' (same as PMax; clean conversions column).
 2. Budget $22 -> $25/day. Max Clicks CPC cap $15 -> $20.
 3. Campaign PHRASE negatives: price research, reviews, out-of-area, competitors seen in search terms.
 4. Keywords: pause the 8 old PHRASE keywords (they pulled competitor/research terms), add tight EXACT + a few PHRASE w/ "nj".
 5. New RSA -> the new page (15,000+ installs, no NYC, heating only). Old RSA 817245367827 paused.
 6. Campaign ENABLED (last, only if 1-5 succeeded).
Rollback: campaign PAUSED (everything else is inert while paused).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, AG, OLD_AD = "4571881760", "24047025253", "197798871985", "817245367827"
GOAL = "6459689709"
URL = "https://icshvac.com/furnace-heating-repair-northern-nj/"
APPLY = "--apply" in sys.argv
VO = not APPLY

NEW_BUDGET, NEW_CAP = 25_000_000, 20_000_000

NEG_PHRASE = ["cost", "price", "prices", "how much", "reviews", "reddit", "diy", "parts", "westchester", "new york",
              "lenny's", "lennys", "smiths heating", "a j perri", "aj perri", "reiner", "gadaleta", "petro", "jobs", "salary"]

KW_EXACT = ["furnace repair", "heating repair", "heater repair", "furnace repair near me", "heating repair near me",
            "boiler repair", "boiler repair near me", "emergency heating repair", "no heat repair", "heat pump repair",
            "oil burner repair", "furnace not working"]  # "no heat in house" dropped: Google flags it as Dating policy (11-12 validate)
KW_PHRASE = ["furnace repair nj", "heating repair nj", "boiler repair nj", "emergency furnace repair"]

HEADLINES = ["Furnace & Heating Repair NJ", "No Heat? Call ICS Today", "24/7 Emergency Heating Repair",
             "NATE-Certified Technicians", "Northern NJ Since 1990", "15,000+ Installs Since 1990",
             "Gas, Oil, Boiler & Heat Pumps", "Family-Owned HVAC Company", "Fast Furnace Repair",
             "Boiler Repair in Northern NJ", "Licensed & Insured in NJ", "Book a Heating Repair Today",
             "Request Heating Repair Online", "Heating Repair Experts in NJ", "Heating Repair Near You"]
DESCRIPTIONS = ["No heat? ICS repairs gas, oil, boiler and heat pump systems across Northern NJ.",
                "NATE-certified technicians and 24/7 emergency service. Family-owned since 1990.",
                "Call now or send the form. A tech diagnoses your system and you approve the repair.",
                "Licensed and insured in NJ. Serving Bergen, Essex, Hudson, Morris and Passaic."]
PATH1, PATH2 = "Heating-Repair", "Northern-NJ"

for h in HEADLINES: assert len(h) <= 30, h
for d in DESCRIPTIONS: assert len(d) <= 90, d
assert len(HEADLINES) == 15 and len(DESCRIPTIONS) == 4 and len(PATH1) <= 15 and len(PATH2) <= 15

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums

# ---- pre-checks
row = q(f"SELECT campaign.status, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.resource_name, campaign_budget.amount_micros "
        f"FROM campaign WHERE campaign.id = {NB}")[0]
print(f"before: status {row.campaign.status.name}, cap ${row.campaign.target_spend.cpc_bid_ceiling_micros/1e6}, budget ${row.campaign_budget.amount_micros/1e6}")
if row.campaign.status.name != "PAUSED":
    sys.exit("ABORT: campaign is not PAUSED (someone changed it), re-read before relaunching")
budget_rn = row.campaign_budget.resource_name
old_kws = q(f"SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.id = {AG} "
            f"AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' "
            f"AND ad_group_criterion.keyword.match_type = 'PHRASE'")
print(f"old PHRASE keywords to pause: {[r.ad_group_criterion.keyword.text for r in old_kws]}")
existing_negs = {r.campaign_criterion.keyword.text.lower() for r in q(
    f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
negs = [n for n in NEG_PHRASE if n not in existing_negs]

def run(label, fn):
    fn()
    print(f"  ok  {label}", "APPLIED" if APPLY else "(validate_only)")

# 1. goal
def goal():
    op = client.get_type("ConversionGoalCampaignConfigOperation")
    cfg = op.update
    cfg.resource_name = client.get_service("ConversionGoalCampaignConfigService").conversion_goal_campaign_config_path(CID, NB)
    cfg.goal_config_level = E.GoalConfigLevelEnum.CAMPAIGN
    cfg.custom_conversion_goal = f"customers/{CID}/customConversionGoals/{GOAL}"
    op.update_mask.paths.extend(["goal_config_level", "custom_conversion_goal"])
    client.get_service("ConversionGoalCampaignConfigService").mutate_conversion_goal_campaign_configs(
        request={"customer_id": CID, "operations": [op], "validate_only": VO})
run("goal -> TSD | Calls + Forms (no taps)", goal)

# 2. budget + cap
def budget():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = budget_rn; op.update.amount_micros = NEW_BUDGET; op.update_mask.paths.append("amount_micros")
    client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": [op], "validate_only": VO})
run("budget $22 -> $25", budget)

def cap():
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, NB)
    op.update.target_spend.cpc_bid_ceiling_micros = NEW_CAP
    op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
    client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": VO})
run("CPC cap $15 -> $20", cap)

# 3. negatives
def negatives():
    ops = []
    for t in negs:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create; c.campaign = ga.campaign_path(CID, NB); c.negative = True
        c.keyword.text = t; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    if ops:
        client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
run(f"{len(negs)} campaign PHRASE negatives: {negs}", negatives)

# 4. keywords
def keywords():
    svc = client.get_service("AdGroupCriterionService"); ops = []
    for r in old_kws:
        op = client.get_type("AdGroupCriterionOperation")
        op.update.resource_name = r.ad_group_criterion.resource_name
        op.update.status = E.AdGroupCriterionStatusEnum.PAUSED
        op.update_mask.paths.append("status"); ops.append(op)
    for text, mt in [(k, E.KeywordMatchTypeEnum.EXACT) for k in KW_EXACT] + [(k, E.KeywordMatchTypeEnum.PHRASE) for k in KW_PHRASE]:
        op = client.get_type("AdGroupCriterionOperation")
        c = op.create; c.ad_group = ga.ad_group_path(CID, AG); c.status = E.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = text; c.keyword.match_type = mt; ops.append(op)
    svc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
run(f"pause {len(old_kws)} old PHRASE kws, add {len(KW_EXACT)} EXACT + {len(KW_PHRASE)} PHRASE", keywords)

# 5. RSA
def rsa():
    svc = client.get_service("AdGroupAdService")
    new = client.get_type("AdGroupAdOperation")
    a = new.create; a.ad_group = ga.ad_group_path(CID, AG); a.status = E.AdGroupAdStatusEnum.ENABLED
    a.ad.final_urls.append(URL)
    r = a.ad.responsive_search_ad; r.path1 = PATH1; r.path2 = PATH2
    for h in HEADLINES:
        x = client.get_type("AdTextAsset"); x.text = h; r.headlines.append(x)
    for d in DESCRIPTIONS:
        x = client.get_type("AdTextAsset"); x.text = d; r.descriptions.append(x)
    old = client.get_type("AdGroupAdOperation")
    old.update.resource_name = svc.ad_group_ad_path(CID, AG, OLD_AD)
    old.update.status = E.AdGroupAdStatusEnum.PAUSED
    old.update_mask.paths.append("status")
    svc.mutate_ad_group_ads(request={"customer_id": CID, "operations": [new, old], "validate_only": VO})
run("new RSA -> new page, old RSA paused", rsa)

# 6. enable
def enable():
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, NB); op.update.status = E.CampaignStatusEnum.ENABLED
    op.update_mask.paths.append("status")
    client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": VO})
run("campaign ENABLED", enable)

if APPLY:
    r = q(f"SELECT campaign.status, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {NB}")[0]
    print(f"read-back: {r.campaign.status.name}, cap ${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6}, budget ${r.campaign_budget.amount_micros/1e6}")
    for x in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.review_status FROM ad_group_ad "
               f"WHERE ad_group.id = {AG} AND ad_group_ad.status != 'REMOVED'"):
        print(f"  ad {x.ad_group_ad.ad.id} {x.ad_group_ad.status.name} {list(x.ad_group_ad.ad.final_urls)} {x.ad_group_ad.policy_summary.review_status.name}")
    n = q(f"SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.id = {AG} AND ad_group_criterion.type='KEYWORD' "
          f"AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE")
    print(f"  enabled keywords: {len(n)}")
    g = q(f"SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id = {NB}")[0]
    print(f"  goal: {g.conversion_goal_campaign_config.goal_config_level.name} {g.conversion_goal_campaign_config.custom_conversion_goal}")
