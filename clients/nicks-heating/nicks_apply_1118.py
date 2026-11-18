# APPLIED LIVE 2026-11-18 13:16 BRT (Edu: "proceed"). 12 negs added, AC Installation + AC Emergency PAUSED, Branded -> Target IS top 90% $8 cap (read-back OK). Re-run with --apply = no-op for negs, re-pauses, re-sets Target IS.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path> [--apply]. Validate-only unless --apply.
"""Nick's (1854100356), 2026-11-18 (Command Center fu-181, Edu: "proceed"). Three changes from the 11-18 read:
1. Heating Repair ad group 205669629001: +12 ad-group PHRASE negatives (fireplace, camper, rv, bathroom, error code, code, goodman,
   american standard, draft inducer, blown fuse, hauck, accurate electric). Week-1 impression-only terms were DIY / off-service / competitors.
2. NB 23821497590: PAUSE ad groups AC Installation 194012881577 + AC Emergency 195469149119 (0 leads in November, $30 + $0). AC Repair stays
   (228s call 11-16). NB budget stays $40, heating gets the room.
3. Branded 23675600637: Max Conversions (tCPA $25) -> Target Impression Share top-of-page 90%, CPC ceiling $8 (All Seasons pattern).
   Week 1 after the cleanup: CPC $4.59 -> $13.24, 'nicks ac hammond' phrase $111 / 4 clicks = $28 CPC. Budget $85 untouched.
Rollback: remove the 12 negatives; ENABLE the 2 ad groups; Branded back to maximize_conversions target_cpa_micros 25_000_000."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB, BR, HG = "1854100356", "23821497590", "23675600637", "205669629001"
PAUSE_AG = {"194012881577": "AC Installation", "195469149119": "AC Emergency"}
NEG = ["fireplace", "camper", "rv", "bathroom", "error code", "code", "goodman", "american standard", "draft inducer", "blown fuse", "hauck", "accurate electric"]
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
req = {"customer_id": CID, "validate_only": vo}

# 1. heating negatives (skip any already there)
have = {r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE ad_group.id = {HG} AND ad_group_criterion.negative = TRUE AND ad_group_criterion.status != 'REMOVED'""")}
kws = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE ad_group.id = {HG} AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
add = [n for n in NEG if n not in have]
block = [(n, k) for n in add for k in kws if f" {n} " in f" {k} "]
if block: sys.exit(f"ABORT: negative would block a live heating keyword: {block}")
print(f"1. heating negatives: {len(have)} existing, adding {len(add)}: {add}")
neg_ops = []
for n in add:
    op = client.get_type("AdGroupCriterionOperation"); c = op.create
    c.ad_group = ga.ad_group_path(CID, HG); c.negative = True
    c.keyword.text = n; c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE; neg_ops.append(op)

# 2. pause the 2 AC ad groups
ags = {r.ad_group.id: r.ad_group for r in q(f"SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'")}
for i, name in PAUSE_AG.items():
    g = ags.get(int(i))
    if not g or g.name != name: sys.exit(f"ABORT: ad group {i} is not '{name}' (got {g.name if g else None})")
keep = [g.name for g in ags.values() if str(g.id) not in PAUSE_AG and g.status.name == "ENABLED"]
if "AC Repair" not in keep or "Heating Repair" not in keep: sys.exit(f"ABORT: AC Repair / Heating Repair not enabled: {keep}")
print(f"2. pause {list(PAUSE_AG.values())} (now {[ags[int(i)].status.name for i in PAUSE_AG]}); stays enabled: {keep}")
ag_ops = []
for i in PAUSE_AG:
    op = client.get_type("AdGroupOperation"); op.update.resource_name = ga.ad_group_path(CID, i)
    op.update.status = client.enums.AdGroupStatusEnum.PAUSED; op.update_mask.paths.append("status"); ag_ops.append(op)

# 3. Branded -> Target IS
br = q(f"""SELECT campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign.bidding_strategy, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared FROM campaign WHERE campaign.id = {BR}""")[0]
print(f"3. Branded now {br.campaign.bidding_strategy_type.name} tCPA ${br.campaign.maximize_conversions.target_cpa_micros/1e6:.2f} budget ${br.campaign_budget.amount_micros/1e6:.2f} shared={br.campaign_budget.explicitly_shared} portfolio='{br.campaign.bidding_strategy}'")
if br.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS" or br.campaign.bidding_strategy: sys.exit("ABORT: Branded bidding is not the expected standard Max Conversions")
c_op = client.get_type("CampaignOperation"); cu = c_op.update
cu.resource_name = ga.campaign_path(CID, BR)
cu.target_impression_share.location = client.enums.TargetImpressionShareLocationEnum.TOP_OF_PAGE
cu.target_impression_share.location_fraction_micros = 900_000
cu.target_impression_share.cpc_bid_ceiling_micros = 8_000_000
c_op.update_mask.paths.extend(["target_impression_share.location", "target_impression_share.location_fraction_micros", "target_impression_share.cpc_bid_ceiling_micros"])

tag = "(validate_only)" if vo else "APPLIED"
if neg_ops: client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={**req, "operations": neg_ops}); print(f"   negatives ok ({len(neg_ops)})", tag)
client.get_service("AdGroupService").mutate_ad_groups(request={**req, "operations": ag_ops}); print(f"   ad group pauses ok ({len(ag_ops)})", tag)
client.get_service("CampaignService").mutate_campaigns(request={**req, "operations": [c_op]}); print("   Branded Target IS top 90% / $8 cap ok", tag)
if APPLY:
    got = {r.ad_group_criterion.keyword.text.lower() for r in q(f"SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.id = {HG} AND ad_group_criterion.negative = TRUE AND ad_group_criterion.status != 'REMOVED'")}
    print(f"read-back heating negatives: {len(got)}, all new present={all(n in got for n in NEG)}")
    for r in q(f"SELECT ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'"): print(f"read-back AG {r.ad_group.name}: {r.ad_group.status.name}")
    r = q(f"SELECT campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {BR}")[0]
    print(f"read-back Branded: {r.campaign.bidding_strategy_type.name} {r.campaign.target_impression_share.location.name} {r.campaign.target_impression_share.location_fraction_micros/1e4:.0f}% ceil ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.2f} budget ${r.campaign_budget.amount_micros/1e6:.2f}")
