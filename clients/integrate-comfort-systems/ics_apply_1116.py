# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]
"""Integrate Comfort (4571881760): NonBranded 24047025253, plan C of the 2026-11-16 deep dive (Edu: approved).

Why: since the 11-12 relaunch the campaign loses 43-77% of impressions to rank (Max Clicks buys bottom of page, top IS 13%),
22% of spend went to competitor-name searches and 17% to Newark/Elizabeth (cities the client excludes in its own LSA geo).

Changes (heating ad group 197798871985; budget stays $25/day):
 1. Bidding: Max Clicks ($20 cap) -> Target Impression Share, TOP_OF_PAGE, 65%, CPC ceiling $18.
 2. Campaign PHRASE negatives: ~40 competitor names seen in search terms since 10-07, plumbing/plumber, why/how to/can a/what's wrong.
 3. Negative locations: Newark 1022300, Paterson 1022331, Elizabeth 1022108, Irvington 1022190 (same 4 the client excludes in LSA Belleville).
 4. Keywords (heating ad group): hvac repair [EXACT], hvac repair near me [EXACT], hvac repair nj [PHRASE].
Rollback: bidding back to Max Clicks cap $20 (target_spend); remove the criteria created (ids printed on apply).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client
from google.api_core import protobuf_helpers

CID, NB, AG = "4571881760", "24047025253", "197798871985"
APPLY = "--apply" in sys.argv
VO = not APPLY
TIS_FRACTION, TIS_CAP = 650_000, 18_000_000
NEG_LOCS = {"1022300": "Newark", "1022331": "Paterson", "1022108": "Elizabeth", "1022190": "Irvington"}
NEG_PHRASE = [
    # competitor names (search terms 10-07 .. 11-16)
    "total comfort", "1 800 heaters", "800 heaters", "bogush", "smith heating", "ixim", "iceman", "oneill", "o neill", "o'neill",
    "scotty and son", "good tidings", "comfort pro", "princeton air", "revere plumbing", "schaible", "splash plumbing", "pete manley",
    "platinum hvac", "nj hvac and plumbing", "air group", "atlantic heating", "colella", "merring", "climate care", "dave's heating",
    "daves heating", "ductmate", "gold medal", "ideal air", "jack dong", "keil", "perfection contracting", "russo brothers",
    "edison heating", "sunrise heating", "tanous", "trinity air", "warren heating", "your ultimate comfort", "harmony hvac", "ck control temp",
    # services ICS does not sell
    "plumbing", "plumber", "plumbers",
    # informational / DIY
    "why", "how to", "can a", "what's wrong", "whats wrong", "if the",
]
KW = [("hvac repair", "EXACT"), ("hvac repair near me", "EXACT"), ("hvac repair nj", "PHRASE")]

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums

# ---- pre-checks
row = q(f"SELECT campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {NB}")[0]
print(f"before: {row.campaign.status.name}, {row.campaign.bidding_strategy_type.name}, maxclicks cap ${row.campaign.target_spend.cpc_bid_ceiling_micros/1e6}, budget ${row.campaign_budget.amount_micros/1e6}")
if row.campaign.status.name != "ENABLED" or row.campaign.bidding_strategy_type.name != "TARGET_SPEND":
    sys.exit("ABORT: campaign is not ENABLED on Max Clicks (someone changed it), re-read first")
existing_negs = {r.campaign_criterion.keyword.text.lower() for r in q(
    f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
negs = [n for n in NEG_PHRASE if n.lower() not in existing_negs]
existing_locs = {str(r.campaign_criterion.location.geo_target_constant).split("/")[-1] for r in q(
    f"SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type = 'LOCATION'")}
locs = {k: v for k, v in NEG_LOCS.items() if k not in existing_locs}
existing_kws = {(r.ad_group_criterion.keyword.text.lower(), r.ad_group_criterion.keyword.match_type.name) for r in q(
    f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.id = {AG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'")}
kws = [(t, m) for t, m in KW if (t.lower(), m) not in existing_kws]

def run(label, fn):
    res = fn()
    print(f"  ok  {label}", "APPLIED" if APPLY else "(validate_only)", res or "")

# 1. bidding -> Target Impression Share
def bidding():
    op = client.get_type("CampaignOperation")
    c = op.update
    c.resource_name = ga.campaign_path(CID, NB)
    c.target_impression_share.location = E.TargetImpressionShareLocationEnum.TOP_OF_PAGE
    c.target_impression_share.location_fraction_micros = TIS_FRACTION
    c.target_impression_share.cpc_bid_ceiling_micros = TIS_CAP
    op.update_mask.CopyFrom(protobuf_helpers.field_mask(None, c._pb))
    client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": VO})
run("bidding -> Target IS top-of-page 65%, cap $18", bidding)

# 2. negatives
def negatives():
    ops = []
    for n in negs:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create; c.campaign = ga.campaign_path(CID, NB); c.negative = True
        c.keyword.text = n; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    if ops:
        r = client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
        return [x.resource_name.split("~")[-1] for x in r.results] if APPLY else None
run(f"{len(negs)} campaign PHRASE negatives (skipped {len(NEG_PHRASE)-len(negs)} existing)", negatives)

# 3. negative locations
def locations():
    ops = []
    for gid in locs:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create; c.campaign = ga.campaign_path(CID, NB); c.negative = True
        c.location.geo_target_constant = client.get_service("GeoTargetConstantService").geo_target_constant_path(gid)
        ops.append(op)
    if ops:
        r = client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
        return [x.resource_name.split("~")[-1] for x in r.results] if APPLY else None
run(f"negative locations {list(locs.values())}", locations)

# 4. keywords
def keywords():
    ops = []
    for t, m in kws:
        op = client.get_type("AdGroupCriterionOperation")
        c = op.create; c.ad_group = ga.ad_group_path(CID, AG); c.status = E.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = t; c.keyword.match_type = getattr(E.KeywordMatchTypeEnum, m)
        ops.append(op)
    if ops:
        r = client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
        return [x.resource_name.split("~")[-1] for x in r.results] if APPLY else None
run(f"keywords {kws}", keywords)

if APPLY:
    r = q(f"SELECT campaign.status, campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {NB}")[0]
    t = r.campaign.target_impression_share
    print(f"read-back: {r.campaign.status.name}, {r.campaign.bidding_strategy_type.name}, {t.location.name} {t.location_fraction_micros/1e4:.0f}% cap ${t.cpc_bid_ceiling_micros/1e6}, budget ${r.campaign_budget.amount_micros/1e6}")
    n = q(f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")
    l = q(f"SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = TRUE")
    k = q(f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.id = {AG} AND ad_group_criterion.type='KEYWORD' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE")
    print(f"read-back: {len(n)} campaign negatives, {len(l)} negative locations {[str(x.campaign_criterion.location.geo_target_constant).split('/')[-1] for x in l]}, {len(k)} enabled keywords in heating AG")
else:
    print("validate-only run finished. Re-run with --apply to make the changes.")
