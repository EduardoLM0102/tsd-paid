# ALREADY APPLIED LIVE 2026-10-23. Kept for the record. Do NOT re-run with --apply (it would create duplicate ad groups).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Zen Air (4360840956), 2026-10-23. Non-branded rebuild onto the 2 new landing pages, then turn it back on.
Approved by Edu in chat ("implement them in the PPC campaigns and turn them back on", budget $100/day).

Campaign TSD_08.03_Search_NonBranded_Evergreen (24100030790), Max Clicks $18 ceiling kept:
 1. Copy the 202 ad-group negatives of the old ad group (205687909824) up to campaign level, + DIY/jobs/vehicle negatives.
 2. New ad group "Heating Repair & Replacement" -> /heating-repair-replacement-duluth-ga/ (phrase + exact, 1 RSA).
 3. New ad group "AC Repair & Replacement"      -> /ac-repair-replacement-duluth-ga/      (phrase + exact, 1 RSA).
 4. Pause the old broad ad group 205687909824.
 5. Budget $150 -> $100/day, campaign PAUSED -> ENABLED.
Everything goes in ONE atomic GoogleAdsService.mutate (temp ids), so validate_only checks the whole build.
"""
import sys, re
sys.path.insert(0, ".")
from lib import init_client

CID, CAMP, OLD_AG = "4360840956", "24100030790", "205687909824"
BUDGET_MICROS = 100_000_000
APPLY = "--apply" in sys.argv

HEAT_URL = "https://callzenair.com/heating-repair-replacement-duluth-ga/"
AC_URL = "https://callzenair.com/ac-repair-replacement-duluth-ga/"

AD_GROUPS = [
    {
        "name": "Heating Repair & Replacement", "url": HEAT_URL, "path1": "Heating-Repair", "path2": "Duluth-GA",
        "phrase": ["furnace repair", "heating repair", "heat pump repair", "furnace replacement", "heat pump replacement",
                   "furnace installation", "new furnace", "furnace tune up", "furnace service", "heating service",
                   "heater repair", "emergency furnace repair", "furnace not working"],
        "exact": ["furnace repair near me", "heating repair near me", "heat pump repair near me", "furnace repair",
                  "heating repair", "furnace repair duluth ga", "heating repair duluth ga"],
        "headlines": ["Heating Repair in Duluth, GA", "Furnace Repair & Replacement", "Same-Day Furnace Repair",
                      "24/7 Emergency Heating Repair", "Heat Pump Repair & Replacement", "Free Estimates on New Systems",
                      "Furnace Tune-Ups", "Stress Free HVAC", "Your Neighborhood HVAC", "Inhale Zen, Exhale Comfort",
                      "NATE-Certified Technicians", "Family-Owned Since 2016", "Financing Available", "BBB A+ Accredited",
                      "Clear Quote Before Any Work"],
        "descriptions": ["Same-day and 24/7 emergency furnace repair in Duluth. Call or book a free estimate today.",
                         "No heat? A NATE-certified tech finds the real cause and gives you a clear quote first.",
                         "Free estimates on new furnaces and heat pumps. Financing available. Stress Free HVAC.",
                         "Family-owned, licensed, BBB A+ Accredited. Serving Duluth, Suwanee, Johns Creek and more."],
    },
    {
        "name": "AC Repair & Replacement", "url": AC_URL, "path1": "AC-Repair", "path2": "Duluth-GA",
        "phrase": ["ac repair", "air conditioning repair", "air conditioner repair", "ac replacement", "ac installation",
                   "new ac unit", "ac tune up", "ac service", "emergency ac repair"],
        "exact": ["ac repair near me", "ac repair", "air conditioning repair near me", "ac repair duluth ga"],
        "headlines": ["AC Repair in Duluth, GA", "AC Repair & Replacement", "Same-Day AC Repair", "24/7 Emergency AC Repair",
                      "Free Estimates on New Systems", "AC Tune-Ups", "Air Conditioning Repair", "Your Neighborhood HVAC",
                      "Stress Free HVAC", "Inhale Zen, Exhale Comfort", "NATE-Certified Technicians",
                      "Family-Owned Since 2016", "Flexible Financing Available", "BBB A+ Accredited",
                      "Clear Quote Before Any Work"],
        "descriptions": ["Same-day and 24/7 emergency AC repair in Duluth. Call or book a free estimate today.",
                         "AC blowing warm air? A NATE-certified tech finds the real cause. Clear quote up front.",
                         "Free estimates on new AC systems. Flexible financing. Your Neighborhood HVAC since 2016.",
                         "Family-owned, licensed, BBB A+ Accredited. Serving Duluth, Suwanee, Johns Creek and more."],
    },
]
# New campaign-level PHRASE negatives (phrase/exact service kws open these doors: water heater, car AC, DIY, jobs)
EXTRA_NEG = ["water heater", "water heating", "hot water", "space heater", "pool", "car", "auto", "truck", "vehicle",
             "rv", "window unit", "portable", "diy", "how to", "yourself", "parts", "manual", "youtube", "reddit",
             "jobs", "job", "salary", "careers", "hiring", "school", "training", "certification", "course"]

for ag in AD_GROUPS:  # length guard
    for h in ag["headlines"]: assert len(h) <= 30, h
    for d in ag["descriptions"]: assert len(d) <= 90, d
    assert len(ag["path1"]) <= 15 and len(ag["path2"]) <= 15

client = init_client()
ga = client.get_service("GoogleAdsService")
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums

# --- existing negatives: old ad group (to copy) + campaign (to skip dupes)
old_negs = [(r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name) for r in ga.search(
    customer_id=CID, query=f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM ad_group_criterion WHERE ad_group.id = {OLD_AG} AND ad_group_criterion.negative = TRUE
    AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'""")]
camp_negs = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in ga.search(
    customer_id=CID, query=f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
    FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
to_add = []
for t, m in old_negs + [(t, "PHRASE") for t in EXTRA_NEG]:
    if (t.lower(), m) not in camp_negs and (t.lower(), m) not in {(x.lower(), y) for x, y in to_add}:
        to_add.append((t, m))
print(f"old ad-group negatives: {len(old_negs)} | campaign has {len(camp_negs)} | adding {len(to_add)} at campaign level")

# --- conflict check: would any negative block a new keyword?
toks = lambda s: re.findall(r"[a-z0-9+']+", s.lower())
def blocks(neg, m, kw):
    n, k = toks(neg), toks(kw)
    if m == "EXACT": return n == k
    if m == "PHRASE": return any(k[i:i + len(n)] == n for i in range(len(k) - len(n) + 1))
    return set(n) <= set(k)
all_negs = list(camp_negs) + [(t.lower(), m) for t, m in to_add]
conflicts = [(kw, n, m) for ag in AD_GROUPS for kw in ag["phrase"] + ag["exact"] for n, m in all_negs if blocks(n, m, kw)]
if conflicts:
    print("CONFLICTS, aborting:", conflicts); sys.exit(1)
print("conflict check: no negative blocks a new keyword")

# --- build one atomic mutate
budget_rn = next(iter(ga.search(customer_id=CID, query=f"SELECT campaign.campaign_budget, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id = {CAMP}")))
assert not budget_rn.campaign_budget.explicitly_shared, "budget is shared, stop"
camp_rn = ga.campaign_path(CID, CAMP)
ops = []
def mop(): return client.get_type("MutateOperation")

for t, m in to_add:
    op = mop(); c = op.campaign_criterion_operation.create
    c.campaign = camp_rn; c.negative = True; c.keyword.text = t; c.keyword.match_type = MT[m]
    ops.append(op)

for i, ag in enumerate(AD_GROUPS):
    ag_rn = ga.ad_group_path(CID, str(-(i + 1)))
    op = mop(); g = op.ad_group_operation.create
    g.resource_name = ag_rn; g.campaign = camp_rn; g.name = ag["name"]
    g.status = ST.AdGroupStatusEnum.ENABLED; g.type_ = ST.AdGroupTypeEnum.SEARCH_STANDARD
    ops.append(op)
    for t, m in [(t, "PHRASE") for t in ag["phrase"]] + [(t, "EXACT") for t in ag["exact"]]:
        op = mop(); k = op.ad_group_criterion_operation.create
        k.ad_group = ag_rn; k.status = ST.AdGroupCriterionStatusEnum.ENABLED
        k.keyword.text = t; k.keyword.match_type = MT[m]
        ops.append(op)
    op = mop(); a = op.ad_group_ad_operation.create
    a.ad_group = ag_rn; a.status = ST.AdGroupAdStatusEnum.ENABLED
    a.ad.final_urls.append(ag["url"])
    rsa = a.ad.responsive_search_ad; rsa.path1 = ag["path1"]; rsa.path2 = ag["path2"]
    for h in ag["headlines"]:
        x = client.get_type("AdTextAsset"); x.text = h; rsa.headlines.append(x)
    for d in ag["descriptions"]:
        x = client.get_type("AdTextAsset"); x.text = d; rsa.descriptions.append(x)
    ops.append(op)

op = mop(); g = op.ad_group_operation.update
g.resource_name = ga.ad_group_path(CID, OLD_AG); g.status = ST.AdGroupStatusEnum.PAUSED
op.ad_group_operation.update_mask.paths.append("status"); ops.append(op)

op = mop(); b = op.campaign_budget_operation.update
b.resource_name = budget_rn.campaign.campaign_budget; b.amount_micros = BUDGET_MICROS
op.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(op)

op = mop(); c = op.campaign_operation.update
c.resource_name = camp_rn; c.status = ST.CampaignStatusEnum.ENABLED
op.campaign_operation.update_mask.paths.append("status"); ops.append(op)

ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"mutate: {len(ops)} operations ok{'' if APPLY else ' (validate_only, nothing changed)'}")
if not APPLY: sys.exit(0)

print("--- read-back")
for r in ga.search(customer_id=CID, query=f"""SELECT campaign.status, campaign.bidding_strategy_type,
        campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {CAMP}"""):
    print(f"   campaign {r.campaign.status.name} {r.campaign.bidding_strategy_type.name} ceiling ${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} budget ${r.campaign_budget.amount_micros/1e6:.2f}")
for r in ga.search(customer_id=CID, query=f"SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {CAMP} AND ad_group.status != 'REMOVED'"):
    print(f"   ad group {r.ad_group.id} {r.ad_group.status.name} {r.ad_group.name}")
for r in ga.search(customer_id=CID, query=f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls,
        ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = {CAMP} AND ad_group.status = 'ENABLED' AND ad_group_ad.status != 'REMOVED'"""):
    print(f"   ad {r.ad_group_ad.ad.id} {r.ad_group_ad.status.name} {r.ad_group_ad.policy_summary.approval_status.name} {r.ad_group.name} -> {list(r.ad_group_ad.ad.final_urls)}")
n_kw = {}
for r in ga.search(customer_id=CID, query=f"""SELECT ad_group.name, ad_group_criterion.keyword.match_type FROM ad_group_criterion
        WHERE campaign.id = {CAMP} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'"""):
    key = (r.ad_group.name, r.ad_group_criterion.keyword.match_type.name); n_kw[key] = n_kw.get(key, 0) + 1
print("   keywords:", n_kw)
n = sum(1 for _ in ga.search(customer_id=CID, query=f"SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.id = {CAMP} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"))
print(f"   campaign negatives: {n}")
