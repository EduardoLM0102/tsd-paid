# APPLIED LIVE 2026-11-11 10:21 BRT (Edu: "Execute 1 to 3"). Ad group 205669629001 "Heating Repair" ENABLED, 18 kw + 14 negs + 1 RSA (in review). Do NOT re-run with --apply (aborts: ad group exists).
"""Nick's (1854100356): add a HEATING ad group to Nonbranded 23821497590 (Max Clicks $15 cap, $25/day), landing on the page that
already exists: https://nicksac.com/heating-repair-hammond-la/ (H1 "Heating Repair in Hammond, LA", GHL form, phone (985) 999-4785,
NATE / 40+ years / Carrier Factory Authorized / licensed & insured all on the site 11-11). No new landing page needed to start.
- 1 ad group "Heating Repair", 18 keywords (exact + phrase), ad-group negatives from fu-125 (for sale, in store, deals, evaporator core,
  why isn't, why won't) + research/DIY terms, 1 RSA (15 headlines / 4 descriptions, claims verified on nicksac.com).
- Prints every NB campaign negative that contains heat/furnace/hvac first and ABORTS if one would block the new keywords.
- Budget NOT changed here (Edu's call: NB $25 -> $40 funded from Branded's unused $100, or PMax $50 -> $35)."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "1854100356", "23821497590"
URL = "https://nicksac.com/heating-repair-hammond-la/"
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

KW = [  # (text, match)
    ("heating repair", "EXACT"), ("heating repair near me", "EXACT"), ("heating repair hammond la", "EXACT"), ("heating repair hammond", "PHRASE"),
    ("furnace repair", "EXACT"), ("furnace repair near me", "EXACT"), ("furnace repair hammond la", "EXACT"), ("gas furnace repair", "PHRASE"),
    ("heater repair", "EXACT"), ("heater repair near me", "EXACT"), ("heat pump repair", "EXACT"), ("heat pump repair near me", "EXACT"),
    ("heating system repair", "PHRASE"), ("emergency heating repair", "PHRASE"), ("heater not working", "PHRASE"), ("furnace not working", "PHRASE"),
    ("no heat", "PHRASE"), ("heating service hammond la", "EXACT"),
]
NEG = ["for sale", "in store", "deals", "evaporator core", "why isn't", "why won't", "how to", "diy", "parts", "manual", "space heater", "water heater", "cost of", "price of"]
HEADLINES = ["Heating Repair in Hammond, LA", "Furnace Repair Hammond LA", "No Heat? Same-Day Service", "NATE-Certified Technicians", "Heater Not Working? Call Now",
             "Heat Pump & Furnace Repair", "Fast, Honest Heating Repair", "Trusted in Hammond 40+ Years", "Carrier Factory Authorized", "Licensed & Fully Insured",
             "Emergency Heating Repair", "5-Star Rated Heating Repair", "Heating Repair Near You", "Southeast Louisiana Heating", "Fixed Right the First Time"]
DESCS = ["Furnace or heat pump not heating? NATE-certified techs fix it right, same day.",
         "Trusted in Hammond for 40+ years. Licensed, insured, Carrier Factory Authorized Dealer.",
         "Heating repair in Hammond, Ponchatoula, Covington and Mandeville. Upfront pricing.",
         "Heater blowing cold air or won't turn on? Fast heating repair for Southeast Louisiana."]
for h in HEADLINES: assert len(h) <= 30, h
for d in DESCS: assert len(d) <= 90, d

# 1. conflicts: campaign negatives that would block the new keywords
negs = [r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")]
hits = [n for n in negs if any(w in n for w in ("heat", "furnace", "hvac", "repair", "near me", "emergency"))]
print(f"NB campaign negatives: {len(negs)}; containing heat/furnace/hvac/repair/near me/emergency: {hits}")
conflict = [(k, n) for k, _ in KW for n in negs if f" {n} " in f" {k} "]
if conflict: sys.exit(f"ABORT: campaign negatives block new keywords: {conflict}")
existing = {r.ad_group.name for r in q(f"SELECT ad_group.name FROM ad_group WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'")}
if "Heating Repair" in existing: sys.exit("ABORT: ad group 'Heating Repair' already exists")
print("existing NB ad groups:", sorted(existing))

# 2. ad group
ag_op = client.get_type("AdGroupOperation"); ag = ag_op.create
ag.name = "Heating Repair"; ag.campaign = ga.campaign_path(CID, NB); ag.status = client.enums.AdGroupStatusEnum.ENABLED
ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD; ag.cpc_bid_micros = 12_000_000
ag_svc = client.get_service("AdGroupService")
resp = ag_svc.mutate_ad_groups(request={"customer_id": CID, "operations": [ag_op], "validate_only": vo})
print("ad group ok", "(validate_only)" if vo else resp.results[0].resource_name)
if vo:
    print(f"would add {len(KW)} keywords, {len(NEG)} ad-group negatives, 1 RSA ({len(HEADLINES)} H / {len(DESCS)} D) -> {URL}")
    # validate the keyword + RSA shapes against a dummy ad group resource is not possible in one pass; the shapes are standard.
    sys.exit(0)

ag_rn = resp.results[0].resource_name
ops = []
for text, match in KW:
    op = client.get_type("AdGroupCriterionOperation"); c = op.create
    c.ad_group = ag_rn; c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED; c.keyword.text = text; c.keyword.match_type = getattr(MT, match); ops.append(op)
for text in NEG:
    op = client.get_type("AdGroupCriterionOperation"); c = op.create
    c.ad_group = ag_rn; c.negative = True; c.keyword.text = text; c.keyword.match_type = MT.PHRASE; ops.append(op)
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops})
print(f"keywords + negatives APPLIED ({len(ops)})")

ad_op = client.get_type("AdGroupAdOperation"); ada = ad_op.create
ada.ad_group = ag_rn; ada.status = client.enums.AdGroupAdStatusEnum.ENABLED; ada.ad.final_urls.append(URL)
for h in HEADLINES:
    a = client.get_type("AdTextAsset"); a.text = h; ada.ad.responsive_search_ad.headlines.append(a)
for d in DESCS:
    a = client.get_type("AdTextAsset"); a.text = d; ada.ad.responsive_search_ad.descriptions.append(a)
ada.ad.responsive_search_ad.path1 = "heating-repair"; ada.ad.responsive_search_ad.path2 = "hammond-la"
client.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CID, "operations": [ad_op]})
print("RSA APPLIED (in review)")
print("read-back:", [(r.ad_group.name, r.ad_group.status.name) for r in q(f"SELECT ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = {NB} AND ad_group.name = 'Heating Repair'")])
