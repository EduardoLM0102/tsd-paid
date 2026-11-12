# APPLIED LIVE 2026-10-20 on Edu's go, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-10-20 ("For Watt's Right - you have my ok to execute"), Command Center fu-070.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Watt's Right (3651667805), staged in the 10-09 and 10-20 rechecks. Constant $235/d total:
1. Budgets: Branded 23690645223 $20 -> $35/d, Nonbranded 23832838033 $120 -> $105/d (PMax $95 unchanged).
2. Branded: remove the Mon-Fri 06:00-22:00 ad schedule (no schedule = all days/hours).
3. Nonbranded: target CPA $80 on Maximize Conversions.
4. Nonbranded: 11 competitor PHRASE negatives.
5. Pause old Emergency RSA 808052449185 (new 826560998576 keeps serving).
Aborts on shared budgets / unexpected current values; replays negatives against 30d search terms + live keywords first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, NB, PM = "3651667805", "23690645223", "23832838033", "23833205176"
BUDGETS = {BR: (20.0, 35.0), NB: (120.0, 105.0)}
TCPA = 80.0
OLD_AD, NEW_AD = "808052449185", "826560998576"
NEG = ["quality electric", "fox electric", "let there be light", "forehand electric", "b&b electric", "miller electric",
       "reeves electric", "bennett electric", "pride electric", "shanks electric", "a plus electric"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
bud = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy,
    campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
    FROM campaign WHERE campaign.id IN ({BR},{NB},{PM})""")}
for cid, r in bud.items():
    print(f"{r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} "
          f"shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
for cid, (old, new) in BUDGETS.items():
    r = bud[cid]; cur = r.campaign_budget.amount_micros / 1e6
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")
if bud[NB].campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS" or bud[NB].campaign.bidding_strategy:
    sys.exit("ABORT: Nonbranded is not standard Maximize Conversions")
total = sum(bud[c].campaign_budget.amount_micros / 1e6 for c in (BR, NB, PM))
print(f"total now ${total:.2f}/d -> ${total - 20 - 120 + 35 + 105:.2f}/d")

sched = q(f"""SELECT campaign_criterion.resource_name, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour,
    campaign_criterion.ad_schedule.end_hour FROM campaign_criterion WHERE campaign.id = {BR} AND campaign_criterion.type = 'AD_SCHEDULE'""")
print("Branded schedule:", [(s.campaign_criterion.ad_schedule.day_of_week.name, s.campaign_criterion.ad_schedule.start_hour,
                             s.campaign_criterion.ad_schedule.end_hour) for s in sched])

ads = {str(r.ad_group_ad.ad.id): r for r in q(f"""SELECT ad_group.name, ad_group_ad.resource_name, ad_group_ad.ad.id, ad_group_ad.status,
    ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.ad.id IN ({OLD_AD},{NEW_AD})""")}
for a in (OLD_AD, NEW_AD):
    r = ads[a]; print(f"ad {a} ({r.ad_group.name}): {r.ad_group_ad.status.name} {r.ad_group_ad.policy_summary.approval_status.name}")
if ads[NEW_AD].ad_group_ad.status.name != "ENABLED" or ads[NEW_AD].ad_group_ad.policy_summary.approval_status.name not in ("APPROVED", "APPROVED_LIMITED"):
    sys.exit("ABORT: new Emergency ad not enabled+approved")

# --- safety replay of negatives (30d)
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg = [n for n in NEG if n not in existing]
for n in NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    print(f"neg '{n}': {'ALREADY THERE' if n in existing else ''} blocks {len(hit)} terms {[h.search_term_view.search_term for h in hit][:4]}, "
          f"${sum(r.metrics.cost_micros for r in hit)/1e6:.2f}, conv {sum(r.metrics.conversions for r in hit):.1f}; "
          f"kw conflicts: {[k for k in kws if f' {n} ' in f' {k} ']}")

# --- mutations
ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = bud[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.maximize_conversions.target_cpa_micros = int(TCPA * 1e6)
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("NB tCPA ok", "(validate_only)" if vo else "APPLIED")

cc = client.get_service("CampaignCriterionService")
MT = client.enums.KeywordMatchTypeEnum
ops = []
for s in sched:
    op = client.get_type("CampaignCriterionOperation"); op.remove = s.campaign_criterion.resource_name; ops.append(op)
for t in neg:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    cc.mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"schedule removal ({len(sched)}) + negatives ({len(neg)}) ok", "(validate_only)" if vo else "APPLIED")

op = client.get_type("AdGroupAdOperation")
op.update.resource_name = ads[OLD_AD].ad_group_ad.resource_name
op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("old Emergency ad pause ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    for r in q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros,
            campaign.primary_status FROM campaign WHERE campaign.id IN ({BR},{NB},{PM})"""):
        print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} "
              f"tCPA ${r.campaign.maximize_conversions.target_cpa_micros/1e6:.2f} {r.campaign.primary_status.name}")
    left = q(f"SELECT campaign_criterion.resource_name FROM campaign_criterion WHERE campaign.id = {BR} AND campaign_criterion.type = 'AD_SCHEDULE'")
    print(f"   Branded schedule rows left: {len(left)}")
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]}")
    for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.ad.id IN ({OLD_AD},{NEW_AD})"):
        print(f"   ad {r.ad_group_ad.ad.id}: {r.ad_group_ad.status.name}")
