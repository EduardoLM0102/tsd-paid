# APPLIED LIVE 2026-11-04, read-back confirmed (Target IS 95% abs-top, $10 cap, budget $130; both ads PAUSED). Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Apply 2 and 3, yes"). Staged by Gui's 10-31 7-day pass.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
"""Proud Pops (1051843378) Branded 23853361615:
2. Maximize Conversions (no target) -> Target Impression Share, absolute top of page 95%, max CPC ceiling $10 (same setup as Spencer / Napps).
   Budget $130/d unchanged. Brand CPC was $11-15 on QS 10 terms; with taps out of bidding Branded had almost no conversion signal.
3. Pause the 2 POOR Branded RSAs: Brand_OldName 808846497511, Brand_HVAC 808844736361 (only if their ad groups keep another enabled ad).
Rollback = back to Maximize Conversions / re-enable the ads."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR = "1051843378", "23853361615"
ADS = ["808846497511", "808844736361"]
APPLY = "--apply" in sys.argv
c = init_client(); ga = c.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

r = q(f"SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {BR}")[0]
print(r.campaign.name, r.campaign.status.name, r.campaign.bidding_strategy_type.name, f"portfolio='{r.campaign.bidding_strategy}'", r.campaign_budget.amount_micros / 1e6)
if r.campaign.bidding_strategy: sys.exit("ABORT: portfolio strategy")
if r.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: unexpected current strategy")

ads = q(f"""SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength FROM ad_group_ad
    WHERE campaign.id = {BR} AND ad_group_ad.status != 'REMOVED' AND ad_group.status = 'ENABLED'""")
by_ag = {}
for a in ads: by_ag.setdefault(a.ad_group.id, []).append(a)
ad_ops = []
for aid in ADS:
    hit = [a for a in ads if str(a.ad_group_ad.ad.id) == aid]
    if not hit: sys.exit(f"ABORT: ad {aid} not found in Branded")
    a = hit[0]
    others = [x for x in by_ag[a.ad_group.id] if str(x.ad_group_ad.ad.id) not in ADS and x.ad_group_ad.status.name == "ENABLED"]
    print(f"ad {aid} in '{a.ad_group.name}' {a.ad_group_ad.status.name} strength={a.ad_group_ad.ad_strength.name}, other enabled ads in group: {len(others)}")
    if a.ad_group_ad.status.name != "ENABLED": continue
    if not others: sys.exit(f"ABORT: pausing {aid} would leave '{a.ad_group.name}' with no enabled ad")
    op = c.get_type("AdGroupAdOperation"); op.update.resource_name = ga.ad_group_ad_path(CID, str(a.ad_group.id), aid)
    op.update.status = c.enums.AdGroupAdStatusEnum.PAUSED; op.update_mask.paths.append("status"); ad_ops.append(op)

op = c.get_type("CampaignOperation"); u = op.update
u.resource_name = ga.campaign_path(CID, BR)
u.target_impression_share.location = c.enums.TargetImpressionShareLocationEnum.ABSOLUTE_TOP_OF_PAGE
u.target_impression_share.location_fraction_micros = 950000
u.target_impression_share.cpc_bid_ceiling_micros = 10_000_000
op.update_mask.paths.extend(["target_impression_share.location", "target_impression_share.location_fraction_micros",
                             "target_impression_share.cpc_bid_ceiling_micros"])
c.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
if ad_ops:
    c.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CID, "operations": ad_ops, "validate_only": not APPLY})
print(f"Target IS + {len(ad_ops)} ad pause(s)", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    r = q(f"""SELECT campaign.bidding_strategy_type, campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros,
        campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id = {BR}""")[0]
    t = r.campaign.target_impression_share
    print("read-back:", r.campaign.bidding_strategy_type.name, t.location.name, t.location_fraction_micros / 1e4, "%", "ceiling $", t.cpc_bid_ceiling_micros / 1e6,
          "budget $", r.campaign_budget.amount_micros / 1e6, r.campaign.primary_status.name)
    for a in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({','.join(ADS)})"):
        print("read-back ad:", a.ad_group_ad.ad.id, a.ad_group_ad.status.name)
