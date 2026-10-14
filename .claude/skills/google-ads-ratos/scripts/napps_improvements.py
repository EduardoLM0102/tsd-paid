import sys, time
sys.path.insert(0, ".")
from lib import init_client, run_query

CID = "9509605037"
AC_SUMMER_CAMPAIGN = "24049055193"
BRANDED_CAMPAIGN = "23685615826"
OLD_AG = "198093421826"  # "AC Replace Install"

client = init_client()
ga = client.get_service("GoogleAdsService")


def add_campaign_negatives(campaign_id, terms, match="PHRASE"):
    service = client.get_service("CampaignCriterionService")
    match_type = getattr(client.enums.KeywordMatchTypeEnum, match)
    ops = []
    for text in terms:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = ga.campaign_path(CID, campaign_id)
        c.negative = True
        c.keyword.text = text
        c.keyword.match_type = match_type
        ops.append(op)
    resp = service.mutate_campaign_criteria(customer_id=CID, operations=ops)
    return [r.resource_name for r in resp.results]


print("=" * 100)
print("(2) NEGATIVES — TSD_07.21_Search_Nonbranded_AC_Summer (brand/manufacturer shopping queries)")
print("=" * 100)
ac_summer_negatives = [
    "goodman", "lennox", "carrier", "daikin", "amana", "bryant", "american standard",
    "comfortmaker", "friedrich", "ducane", "heil", "bard", "ruud", "mirage",
    "cooper and hunter", "della", "hessaire", "pioneer", "mr cool", "comfort aire",
    "guardian", "evcon", "nfm", "premaire", "aaron's", "lowe's", "midea",
]
res = add_campaign_negatives(AC_SUMMER_CAMPAIGN, ac_summer_negatives)
print(f"Created {len(res)} negatives:")
for r in res:
    print(" ", r)
time.sleep(1)

print("\n" + "=" * 100)
print("(4) NEGATIVES — TSD_03.22_Search_Branded_Evergreen (local competitor names seen in search terms)")
print("=" * 100)
branded_negatives = [
    "all seasons professionals", "a us air conditioning of texas",
    "ben maines air conditioning", "mack and hansen",
]
res2 = add_campaign_negatives(BRANDED_CAMPAIGN, branded_negatives)
print(f"Created {len(res2)} negatives:")
for r in res2:
    print(" ", r)
time.sleep(1)

print("\n" + "=" * 100)
print("(3) SPLIT AC Replace Install -> AC Replacement (existing) + AC Installation (new)")
print("=" * 100)

# a. create new ad group, PAUSED (script convention)
ag_service = client.get_service("AdGroupService")
op = client.get_type("AdGroupOperation")
ad_group = op.create
ad_group.name = "AC Installation"
ad_group.campaign = ga.campaign_path(CID, AC_SUMMER_CAMPAIGN)
ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
resp = ag_service.mutate_ad_groups(customer_id=CID, operations=[op])
new_ag_resource = resp.results[0].resource_name
new_ag_id = new_ag_resource.split("/")[-1]
print(f"Created ad group: {new_ag_resource} (PAUSED)")
time.sleep(1)

# b. add keywords to new ad group
crit_service = client.get_service("AdGroupCriterionService")
kw_specs = [
    ("hvac installation", "EXACT"),
    ("ac installation", "EXACT"),
    ("ac installation near me", "PHRASE"),
]
kw_ops = []
for text, mt in kw_specs:
    op = client.get_type("AdGroupCriterionOperation")
    c = op.create
    c.ad_group = new_ag_resource
    c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    c.keyword.text = text
    c.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, mt)
    kw_ops.append(op)
resp = crit_service.mutate_ad_group_criteria(customer_id=CID, operations=kw_ops)
print(f"Added {len(resp.results)} keywords to new ad group:")
for (text, mt), r in zip(kw_specs, resp.results):
    print(f"   '{text}' [{mt}] -> {r.resource_name}")
time.sleep(1)

# c. create RSA, PAUSED
ad_service = client.get_service("AdGroupAdService")
op = client.get_type("AdGroupAdOperation")
ad_group_ad = op.create
ad_group_ad.ad_group = new_ag_resource
ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
ad = ad_group_ad.ad
ad.final_urls.append("https://nappsac.com/")

headlines = [
    "New AC Installation", "Professional AC Install", "HVAC Installation Experts",
    "New System, Expert Install", "Get an AC Installed Fast", "Expert AC Install Team",
    "Same-Day AC Service", "Licensed & Insured Techs", "Financing Available",
    "Free Estimates Available", "Serving Longview & East TX", "Call Napps AC Experts",
    "TACLA Licensed HVAC Pros", "Fast, Reliable AC Service", "Trusted East Texas HVAC",
]
descriptions = [
    "Professional AC installation in Longview & East TX. Licensed techs, free estimates.",
    "Installing a new AC system? Get expert install from TACLA-licensed pros. Call today.",
    "Fast, reliable AC installation. Financing available. Serving Longview & East Texas.",
    "New AC install done right the first time. Free estimates, honest pricing. Call Napps.",
]
assert all(len(h) <= 30 for h in headlines), "headline over 30 chars"
assert all(len(d) <= 90 for d in descriptions), "description over 90 chars"

for text in headlines:
    h = client.get_type("AdTextAsset")
    h.text = text
    ad.responsive_search_ad.headlines.append(h)
for text in descriptions:
    d = client.get_type("AdTextAsset")
    d.text = text
    ad.responsive_search_ad.descriptions.append(d)

resp = ad_service.mutate_ad_group_ads(customer_id=CID, operations=[op])
print(f"Created RSA: {resp.results[0].resource_name} (PAUSED, {len(headlines)} headlines / {len(descriptions)} descriptions)")
time.sleep(1)

# d. rename old ad group
op = client.get_type("AdGroupOperation")
op.update.resource_name = ga.ad_group_path(CID, OLD_AG)
op.update.name = "AC Replacement"
op.update_mask.paths.append("name")
resp = ag_service.mutate_ad_groups(customer_id=CID, operations=[op])
print(f"Renamed old ad group {OLD_AG}: 'AC Replace Install' -> 'AC Replacement'")
time.sleep(1)

# e. remove the install-intent keywords from the old (now "AC Replacement") ad group
old_ag_resource = ga.ad_group_path(CID, OLD_AG)
move_out = {
    "60153946": "hvac installation",
    "218175154": "ac installation",
    "300376704652": "ac installation near me",
}
rm_ops = []
for kw_id in move_out:
    op = client.get_type("AdGroupCriterionOperation")
    op.remove = ga.ad_group_criterion_path(CID, OLD_AG, kw_id)
    rm_ops.append(op)
resp = crit_service.mutate_ad_group_criteria(customer_id=CID, operations=rm_ops)
print(f"Removed {len(resp.results)} install-intent keywords from old ad group:")
for kw_id, text in move_out.items():
    print(f"   '{text}' (criterion {kw_id})")

print("\n" + "=" * 100)
print(f"NEW AD GROUP ID (for follow-up activation): {new_ag_id}")
print("=" * 100)
