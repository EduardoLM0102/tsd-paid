# APPLIED LIVE 2026-10-28 on Edu's go (brand list sharedSets/12290621628). Do NOT re-run with --apply (aborts: brand list exists).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Nick's Heating (1854100356), 2026-10-28. fu-108 items 2 + 3, Edu: "Execute 2 and 3".
2. PMax 23586346547: brand exclusion for Nick's (brand list w/ entity /g/11shhfxyk8 = nicksac.com) + campaign-level PHRASE
   competitor negatives (0 conv in PMax search categories, 60d). Budget stays $50/d.
   'keefe's ac' is NOT blocked: 4 clicks / 2 conv in PMax over 60d (same rule as 'tropical air kare' on 10-21).
3. Branded: broad 'hvac contractors near me' stays paused (no change, checked below).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, PMAX = "1854100356", "23675600637", "23586346547"
BRAND_ID, BRAND_URL = "/g/11shhfxyk8", "https://nicksac.com/"
LIST_NAME = "TSD | Nick's own brand (PMax exclusion)"
NEG = ["theriot", "theriots", "theriot's", "nash heating", "burkhardt", "hagerman", "wilkins heating",
       "southern air", "accutemp", "enviro mechanical"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
r = q(f"""SELECT campaign.advertising_channel_type, campaign.status, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {PMAX}""")[0]
print(f"PMax {r.campaign.advertising_channel_type.name} {r.campaign.status.name} ${r.campaign_budget.amount_micros/1e6:.2f}/d")
if r.campaign.advertising_channel_type.name != "PERFORMANCE_MAX" or abs(r.campaign_budget.amount_micros/1e6 - 50) > 0.01:
    sys.exit("ABORT: PMax not as expected")
br = [x for x in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id = {BR}
    AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE""") if x.ad_group_criterion.keyword.text.lower() == "hvac contractors near me"]
print("Branded 'hvac contractors near me':", [x.ad_group_criterion.status.name for x in br])
if any(x.ad_group_criterion.status.name == "ENABLED" for x in br): sys.exit("ABORT: broad keyword is enabled again")

res = client.get_service("BrandSuggestionService").suggest_brands(customer_id=CID, brand_prefix="nick's heating")
b = [x for x in res.brands if x.id == BRAND_ID]
if not b or BRAND_URL not in list(b[0].urls): sys.exit("ABORT: brand entity not confirmed")
print(f"brand ok: {b[0].name} {list(b[0].urls)}")

existing = q(f"""SELECT campaign_criterion.type, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {PMAX}
    AND campaign_criterion.negative = TRUE""")
has_brand_list = any(x.campaign_criterion.type_.name == "BRAND_LIST" for x in existing)
ex_kw = {x.campaign_criterion.keyword.text.lower() for x in existing if x.campaign_criterion.type_.name == "KEYWORD"}
if has_brand_list: sys.exit("ABORT: PMax already has a brand list exclusion")

# replay negatives on PMax search categories (60d): abort if one hits a converting category
cats = q(f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.conversions FROM campaign_search_term_insight
    WHERE campaign_search_term_insight.campaign_id = '{PMAX}' AND segments.date BETWEEN '2026-08-29' AND '2026-10-27'""")
bad = False
for n in NEG:
    hit = [c for c in cats if f" {n} " in f" {c.campaign_search_term_insight.category_label.lower()} "]
    conv = sum(c.metrics.conversions for c in hit)
    print(f"neg '{n}': {len(hit)} categories, clicks {sum(c.metrics.clicks for c in hit)}, conv {conv:.1f}")
    if conv > 0: bad = True
if bad: sys.exit("ABORT: a negative hits a converting category")
neg_new = [n for n in NEG if n not in ex_kw]

# --- brand list (shared set + member). Created only on --apply (validate-only can't reference a new set).
if APPLY:
    ss_op = client.get_type("SharedSetOperation")
    ss_op.create.name = LIST_NAME
    ss_op.create.type_ = client.enums.SharedSetTypeEnum.BRANDS
    ss = client.get_service("SharedSetService").mutate_shared_sets(customer_id=CID, operations=[ss_op]).results[0].resource_name
    sc_op = client.get_type("SharedCriterionOperation")
    sc_op.create.shared_set = ss; sc_op.create.brand.entity_id = BRAND_ID
    client.get_service("SharedCriterionService").mutate_shared_criteria(customer_id=CID, operations=[sc_op])
    print("brand list created:", ss)
else:
    ss = None
    print("brand list: skipped in validate-only")

MT = client.enums.KeywordMatchTypeEnum
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, PMAX); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ss:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, PMAX); c.negative = True; c.brand_list.shared_set = ss; ops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(neg_new)} negatives{' + brand exclusion' if ss else ''} ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    for x in q(f"""SELECT campaign_criterion.type, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type, campaign_criterion.brand_list.shared_set
            FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.negative = TRUE"""):
        c = x.campaign_criterion
        print(f"   {c.type_.name} {c.keyword.text} {c.keyword.match_type.name if c.keyword.text else ''} {c.brand_list.shared_set}")
    for x in q(f"SELECT shared_criterion.brand.entity_id FROM shared_criterion WHERE shared_set.resource_name = '{ss}'"):
        print("   brand list member:", x.shared_criterion.brand.entity_id)
    r = q(f"SELECT campaign.primary_status, campaign_budget.amount_micros FROM campaign WHERE campaign.id = {PMAX}")[0]
    print(f"   PMax {r.campaign.primary_status.name} ${r.campaign_budget.amount_micros/1e6:.2f}/d")
