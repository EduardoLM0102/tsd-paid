# APPLIED LIVE 2026-10-20, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-10-20 ("the staged changes, they are ALL approved - make them go live"), Command Center fu-045.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>   (validate-only without --apply)
"""Staged in the 10-05 / 10-13 weekly passes, all at constant account totals:
LILYPAD (3797438623): Branded 24153698844 $5 -> $8/d, Nonbranded 24164203087 $41 -> $38/d.
NAPPS (9509605037):
  - Branded 23685615826: Maximize Conversions -> Target Impression Share, 95% absolute top, $10 CPC cap.
  - Plumbing 23819717682: PHRASE negatives 'the mink', 'detector'.
  - AC Summer 24049055193 -> heating, budget $50/d unchanged: 3 new heating ad groups (Furnace Repair, Furnace Replacement,
    Heating Maintenance) with PHRASE/EXACT keywords + 1 RSA each on the real heating pages; AC Tune-Up, AC Replacement,
    AC Installation ad groups PAUSED; 'ac repair' PHRASE ($914 / 1 conv in 30d) PAUSED; AC Repair ad group stays on.
    Campaign renamed TSD_07.21_Search_Nonbranded_HVAC_Heating.
C&S (5563867754): Branded 23653583753 PHRASE negatives 'airlines', 'airline', 'southern'; Nonbranded 23828098448 PHRASE 'car'.
Copy uses only claims from nappsac.com (checked 2026-10-20): 24/7 emergency heating, TACLA 72668C, family owned since 1957,
Bryant factory authorized dealer, upfront flat-rate pricing, financing on furnace/heat pump replacement.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

APPLY = "--apply" in sys.argv
VO = not APPLY
c = init_client(); ga = c.get_service("GoogleAdsService")
E = c.enums
def q(cid, s): return list(ga.search(customer_id=cid, query=s))
def budget_rn(cid, camp, expect):
    r = q(cid, f"""SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
        FROM campaign WHERE campaign.id = {camp}""")[0].campaign_budget
    if r.explicitly_shared or r.reference_count > 1: sys.exit(f"ABORT: {camp} budget shared")
    if abs(r.amount_micros / 1e6 - expect) > 0.01: sys.exit(f"ABORT: {camp} budget ${r.amount_micros/1e6:.2f}, expected ${expect:.2f}")
    return r.resource_name
def replay(cid, camp, negs):
    terms = q(cid, f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = {camp} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
    kws = [r.ad_group_criterion.keyword.text.lower() for r in q(cid, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {camp} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    have = {r.campaign_criterion.keyword.text.lower() for r in q(cid, f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    out = []
    for n in negs:
        hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
        conf = [k for k in kws if f" {n} " in f" {k} "]
        print(f"   neg '{n}' on {camp}: {'ALREADY THERE ' if n in have else ''}blocks {len(hit)} terms {[h.search_term_view.search_term for h in hit][:4]} "
              f"${sum(h.metrics.cost_micros for h in hit)/1e6:.2f} conv {sum(h.metrics.conversions for h in hit):.1f}; kw conflicts {conf}")
        if conf: sys.exit("ABORT: negative conflicts with a live keyword")
        if n not in have: out.append(n)
    return out
def neg_ops(cid, camp, negs):
    ops = []
    for t in negs:
        op = c.get_type("CampaignCriterionOperation"); x = op.create
        x.campaign = ga.campaign_path(cid, camp); x.negative = True; x.keyword.text = t; x.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    return ops
def budget_op(rn, new):
    op = c.get_type("CampaignBudgetOperation"); op.update.resource_name = rn
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); return op
tag = "(validate_only)" if VO else "APPLIED"

# ---------------- LILYPAD
L, L_BR, L_NB = "3797438623", "24153698844", "24164203087"
print("== Lilypad")
ops = [budget_op(budget_rn(L, L_BR, 5.0), 8.0), budget_op(budget_rn(L, L_NB, 41.0), 38.0)]
c.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": L, "operations": ops, "validate_only": VO})
print("  budgets Branded $5->$8, NB $41->$38", tag)

# ---------------- C&S
CS, CS_BR, CS_NB = "5563867754", "23653583753", "23828098448"
print("== C&S")
ops = neg_ops(CS, CS_BR, replay(CS, CS_BR, ["airlines", "airline", "southern"])) + neg_ops(CS, CS_NB, replay(CS, CS_NB, ["car"]))
if ops: c.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CS, "operations": ops, "validate_only": VO})
print(f"  {len(ops)} negatives", tag)

# ---------------- NAPPS
N, N_BR, N_PL, N_AC = "9509605037", "23685615826", "23819717682", "24049055193"
print("== Napps")
r = q(N, f"SELECT campaign.bidding_strategy_type, campaign.bidding_strategy FROM campaign WHERE campaign.id = {N_BR}")[0].campaign
if r.bidding_strategy or r.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: Napps Branded strategy unexpected")
op = c.get_type("CampaignOperation"); u = op.update; u.resource_name = ga.campaign_path(N, N_BR)
u.target_impression_share.location = E.TargetImpressionShareLocationEnum.ABSOLUTE_TOP_OF_PAGE
u.target_impression_share.location_fraction_micros = 950000
u.target_impression_share.cpc_bid_ceiling_micros = 10_000_000
op.update_mask.paths.extend(["target_impression_share.location", "target_impression_share.location_fraction_micros", "target_impression_share.cpc_bid_ceiling_micros"])
c.get_service("CampaignService").mutate_campaigns(request={"customer_id": N, "operations": [op], "validate_only": VO})
print("  Branded -> Target IS 95% abs top, $10 cap", tag)

ops = neg_ops(N, N_PL, replay(N, N_PL, ["the mink", "detector"]))
if ops: c.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": N, "operations": ops, "validate_only": VO})
print(f"  Plumbing {len(ops)} negatives", tag)

budget_rn(N, N_AC, 50.0)  # guard only, budget unchanged
HEAT = {
  "Furnace Repair": {
    "url": "https://nappsac.com/heating/furnaces/",
    "kw": [("furnace repair", "PHRASE"), ("furnace repair", "EXACT"), ("heater repair", "PHRASE"), ("heating repair", "PHRASE"),
           ("heat pump repair", "PHRASE"), ("furnace not working", "PHRASE"), ("heater not working", "PHRASE"),
           ("emergency heating repair", "PHRASE"), ("furnace repair near me", "PHRASE")],
    "h": ["Furnace Repair in Longview TX", "Heater Not Working? Call Now", "24/7 Emergency Heating Repair", "Heat Pump Repair Experts",
          "Upfront Flat-Rate Pricing", "Family Owned Since 1957", "TACLA Licensed & Insured", "Bryant Factory Authorized",
          "Serving Longview & East TX", "Fast Furnace & Heater Repair", "Call Napps Heating Today", "No Heat? We Can Help 24/7"],
    "d": ["No heat? Napps repairs furnaces and heat pumps 24/7 across Longview and East Texas.",
          "Upfront flat-rate pricing from TACLA-licensed techs. Family owned since 1957.",
          "Bryant factory authorized dealer. Call or schedule your heating repair online today.",
          "Furnace acting up before a cold night? Call Napps for fast, local heating repair."]},
  "Furnace Replacement": {
    "url": "https://nappsac.com/heating/furnaces/replacement/",
    "kw": [("furnace replacement", "PHRASE"), ("new furnace", "PHRASE"), ("furnace installation", "PHRASE"),
           ("heat pump installation", "PHRASE"), ("heat pump replacement", "PHRASE"), ("heating system replacement", "PHRASE")],
    "h": ["Furnace Replacement Longview", "New Furnace Installation", "Heat Pump Installation", "Financing on New Systems",
          "Bryant Factory Authorized", "Upfront Flat-Rate Pricing", "Family Owned Since 1957", "TACLA Licensed & Insured",
          "Serving Longview & East TX", "Replace Your Old Furnace", "Efficient Heating Systems", "Call Napps Heating Today"],
    "d": ["New furnace or heat pump installed by TACLA-licensed techs. Financing available.",
          "Bryant factory authorized dealer serving Longview and East Texas since 1957.",
          "Old furnace costing you? Get upfront, flat-rate pricing on a new heating system.",
          "Family owned and local. Call Napps or schedule your heating visit online today."]},
  "Heating Maintenance": {
    "url": "https://nappsac.com/heating/maintenance/",
    "kw": [("furnace tune up", "PHRASE"), ("furnace maintenance", "PHRASE"), ("heating maintenance", "PHRASE"),
           ("heater maintenance", "PHRASE"), ("heat pump maintenance", "PHRASE"), ("furnace inspection", "PHRASE")],
    "h": ["Furnace Tune-Up Longview TX", "Heating Maintenance Service", "Pre-Season Safety Check", "Get Ready for Winter",
          "Keep Your Furnace Safe", "Heat Pump Maintenance", "Upfront Flat-Rate Pricing", "Family Owned Since 1957",
          "TACLA Licensed & Insured", "Serving Longview & East TX", "Bryant Factory Authorized", "Book Your Tune-Up Today"],
    "d": ["Pre-season furnace and heat pump safety checks from TACLA-licensed Napps techs.",
          "Avoid a no-heat night. Book heating maintenance in Longview and East Texas.",
          "Family owned since 1957. Upfront flat-rate pricing. Call or schedule online.",
          "Keep your system running safely all winter with a heating tune-up from Napps."]},
}
for name, g in HEAT.items():
    for h in g["h"]: assert len(h) <= 30, (name, h, len(h))
    for d in g["d"]: assert len(d) <= 90, (name, d, len(d))
    assert "—" not in "".join(g["h"] + g["d"])
existing = {r.ad_group.name for r in q(N, f"SELECT ad_group.name FROM ad_group WHERE campaign.id = {N_AC} AND ad_group.status != 'REMOVED'")}
if existing & set(HEAT): sys.exit(f"ABORT: heating ad groups already exist: {existing & set(HEAT)}")

mops = []; tmp = -1
for name, g in HEAT.items():
    ag_rn = f"customers/{N}/adGroups/{tmp}"; tmp -= 1
    m = c.get_type("MutateOperation"); a = m.ad_group_operation.create
    a.resource_name = ag_rn; a.name = name; a.campaign = ga.campaign_path(N, N_AC)
    a.status = E.AdGroupStatusEnum.ENABLED; a.type_ = E.AdGroupTypeEnum.SEARCH_STANDARD; mops.append(m)
    for text, mt in g["kw"]:
        m = c.get_type("MutateOperation"); k = m.ad_group_criterion_operation.create
        k.ad_group = ag_rn; k.status = E.AdGroupCriterionStatusEnum.ENABLED
        k.keyword.text = text; k.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt); mops.append(m)
    m = c.get_type("MutateOperation"); ad = m.ad_group_ad_operation.create
    ad.ad_group = ag_rn; ad.status = E.AdGroupAdStatusEnum.ENABLED; ad.ad.final_urls.append(g["url"])
    for h in g["h"]:
        x = c.get_type("AdTextAsset"); x.text = h; ad.ad.responsive_search_ad.headlines.append(x)
    for d in g["d"]:
        x = c.get_type("AdTextAsset"); x.text = d; ad.ad.responsive_search_ad.descriptions.append(x)
    mops.append(m)

# pause AC ad groups + 'ac repair' PHRASE, rename campaign
ags = {r.ad_group.name: r.ad_group.resource_name for r in q(N, f"SELECT ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.id = {N_AC} AND ad_group.status = 'ENABLED'")}
for name in ("AC Tune-Up", "AC Replacement", "AC Installation"):
    if name not in ags: print(f"  (skip: {name} not enabled)"); continue
    m = c.get_type("MutateOperation"); u = m.ad_group_operation.update; u.resource_name = ags[name]
    u.status = E.AdGroupStatusEnum.PAUSED; m.ad_group_operation.update_mask.paths.append("status"); mops.append(m)
kw = q(N, f"""SELECT ad_group_criterion.resource_name FROM ad_group_criterion WHERE campaign.id = {N_AC} AND ad_group.name = 'AC Repair'
    AND ad_group_criterion.keyword.text = 'ac repair' AND ad_group_criterion.keyword.match_type = 'PHRASE' AND ad_group_criterion.status = 'ENABLED'""")
for r in kw:
    m = c.get_type("MutateOperation"); u = m.ad_group_criterion_operation.update; u.resource_name = r.ad_group_criterion.resource_name
    u.status = E.AdGroupCriterionStatusEnum.PAUSED; m.ad_group_criterion_operation.update_mask.paths.append("status"); mops.append(m)
m = c.get_type("MutateOperation"); u = m.campaign_operation.update; u.resource_name = ga.campaign_path(N, N_AC)
u.name = "TSD_07.21_Search_Nonbranded_HVAC_Heating"; m.campaign_operation.update_mask.paths.append("name"); mops.append(m)

res = ga.mutate(request={"customer_id": N, "mutate_operations": mops, "validate_only": VO})
print(f"  AC Summer -> heating: {len(mops)} ops", tag)

if APPLY:
    print("--- read-back")
    for cid, ids in ((L, (L_BR, L_NB)), (N, (N_BR, N_PL, N_AC)), (CS, (CS_BR, CS_NB))):
        for r in q(cid, f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign_budget.amount_micros
                FROM campaign WHERE campaign.id IN ({','.join(ids)})"""):
            print(f"   {cid} {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.bidding_strategy_type.name} "
                  f"ceiling ${r.campaign.target_impression_share.cpc_bid_ceiling_micros/1e6:.2f}")
    for r in q(N, f"SELECT ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {N_AC} AND ad_group.status != 'REMOVED'"):
        print(f"   Napps AG {r.ad_group.name}: {r.ad_group.status.name}")
    for r in q(N, f"SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = {N_AC} AND ad_group_ad.status = 'ENABLED'"):
        print(f"   Napps ad {r.ad_group.name} {r.ad_group_ad.ad.id}: {r.ad_group_ad.policy_summary.approval_status.name}")
    for cid, camp in ((CS, CS_BR), (CS, CS_NB), (N, N_PL)):
        got = [r.campaign_criterion.keyword.text for r in q(cid, f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")]
        print(f"   {camp} negatives incl: {[t for t in got if t in ('airlines','airline','southern','car','the mink','detector')]}")
