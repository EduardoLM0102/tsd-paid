# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), first TSD Search build, 2026-10-22. Edu: "if its creating the campaigns, go for it and leave paused".
Per Ryan's Paid Media Packet: small Google Search capture, branded + high-intent unbranded, Oxford MS only,
exact/phrase only, no AI expansion, no offers or discounts.
- TSD_10.22_Search_Branded_Oxford     $5/day, Maximize Clicks, $4 max CPC
- TSD_10.22_Search_Nonbranded_Oxford  $10/day, Maximize Clicks, $10 max CPC (old MS Search averaged ~$10.70/click)
Both PAUSED. Google Search only (no partners, no Display), presence-only geo = Oxford city + ZIP 38655, English,
AI Max text + final URL expansion opted out. Campaign-level sitelinks/callouts/snippet override the old agency's
account-level ones ('5-Year Warranty', 'Head-Resistant', 'Get Your Free Quote'). Shared negative list from the packet.
No call asset on purpose: waiting for the CallRail number. Ad groups/keywords/ads ENABLED inside the paused campaigns,
so ads go through review now and launch = enabling the 2 campaigns.
One atomic GoogleAdsService.mutate with temp ids. Aborts if TSD_10.22 campaigns or the list already exist.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9215192296"
APPLY = "--apply" in sys.argv
SITE = "https://www.concrete-adventures.com/"
GEO = [1020795, 9013748]  # Oxford, MS (city) + 38655
LIST_NAME = "TSD Negatives - Oxford (10.22)"

NEGATIVES = ["aggregate", "millings", "asphalt", "supply", "supplies", "wholesale", "diy", "do it yourself", "how to",
             "kit", "kits", "jobs", "job", "hiring", "salary", "career", "careers", "employment", "home depot", "lowes",
             "lowe's", "rustoleum", "paint", "ready mix", "concrete truck", "gravel", "pavers", "cheap", "rental", "rent",
             "grinder", "training", "class", "classes", "certification", "youtube", "pressure washing", "soft washing",
             "pool plaster", "replaster", "memphis", "tupelo", "southaven"]

FAMILY = "Family owned decorative concrete company. We take a limited number of projects each month."
CAMPAIGNS = [
    {"name": "TSD_10.22_Search_Branded_Oxford", "budget": 5.0, "cap": 4.0, "groups": [
        {"name": "Branded", "url": SITE, "path": ("Oxford-MS", ""),
         "kw": [("concrete adventures", "EXACT"), ("concrete adventures", "PHRASE")],
         "h": ["Concrete Adventures", "Concrete Adventures Oxford", "Official Site", "Decorative Concrete Coatings",
               "Pool Decks and Garage Floors", "Patios, Driveways and More", "Family Owned and Operated",
               "Nearly 10 Years in Concrete", "Request an Estimate Today", "Serving Oxford, MS", "Quality Over Quantity",
               "Limited Projects Each Month"],
         "d": ["Decorative concrete coatings for pool decks, garage floors, patios and driveways.", FAMILY,
               "See our work and request an estimate for your project in Oxford, MS.",
               "Concrete artisans focused on craftsmanship, durability and style on every project."]}]},
    {"name": "TSD_10.22_Search_Nonbranded_Oxford", "budget": 10.0, "cap": 10.0, "groups": [
        {"name": "Garage Floor Coatings", "url": SITE + "garage-floor-coatings/", "path": ("Garage-Floors", "Oxford-MS"),
         "kw": [(k, "PHRASE") for k in ["garage floor coating", "garage floor coatings", "garage floor epoxy",
                                        "epoxy garage floor", "garage floor resurfacing", "polyaspartic garage floor"]],
         "h": ["Garage Floor Coatings", "Oxford Garage Floor Coatings", "Concrete Adventures", "Coatings That Hold Up",
               "Durable, Easy-Clean Finish", "Resinous Garage Floor Systems", "Built for Daily Use",
               "A Floor You'll Want to Show", "Family Owned and Operated", "Nearly 10 Years in Concrete",
               "Limited Projects Each Month", "Quality Over Quantity", "Request an Estimate Today", "Serving Oxford, MS",
               "See Our Garage Floor Work"],
         "d": ["We turn worn garage floors into durable, good-looking surfaces built for everyday use.", FAMILY,
               "Tell us about your garage and we will give you a clear estimate for your floor.",
               "Easy to clean and made to last. See our garage floor gallery and request an estimate."]},
        {"name": "Pool Deck Resurfacing", "url": SITE + "pool-deck-resurfacing/", "path": ("Pool-Decks", "Oxford-MS"),
         "kw": [(k, "PHRASE") for k in ["pool deck resurfacing", "pool deck coating", "pool deck refinishing",
                                        "resurface pool deck", "pool deck repair"]],
         "h": ["Pool Deck Resurfacing", "Oxford Pool Deck Resurfacing", "Slip-Resistant Pool Decks", "UV-Stable Coatings",
               "A Safer Deck for Wet Feet", "Easy to Clean Pool Decks", "Upgrade Your Backyard", "Concrete Adventures",
               "Family Owned and Operated", "Nearly 10 Years in Concrete", "Limited Projects Each Month",
               "Quality Over Quantity", "Request an Estimate Today", "Serving Oxford, MS", "See Our Pool Deck Work"],
         "d": ["Slip-resistant, UV-stable coatings that make your pool deck safer and better looking.",
               "Tired of a rough, dated pool deck? We coat over it for a smooth, attractive finish.", FAMILY,
               "Easy to clean and built for the Mississippi sun. Request an estimate for your pool deck."]},
        {"name": "Concrete Coatings", "url": SITE + "concrete-overlays/", "path": ("Concrete", "Oxford-MS"),
         "kw": [(k, "PHRASE") for k in ["concrete resurfacing", "concrete coating", "concrete overlay",
                                        "decorative concrete", "driveway resurfacing", "patio resurfacing",
                                        "concrete staining"]],
         "h": ["Decorative Concrete Coatings", "Concrete Resurfacing", "Patio and Driveway Coatings",
               "Oxford Concrete Coatings", "Concrete Overlays and Stains", "Transform Old Concrete",
               "Custom Stains and Finishes", "Made to Last", "Concrete Adventures", "Family Owned and Operated",
               "Nearly 10 Years in Concrete", "Limited Projects Each Month", "Quality Over Quantity",
               "Request an Estimate Today", "Serving Oxford, MS"],
         "d": ["We resurface driveways, patios and walkways with decorative coatings made to last.",
               "From stains to overlays, we turn plain concrete into something you will be proud of.", FAMILY,
               "Tell us about your project and we will give you a clear estimate. Serving Oxford, MS."]}]},
]
SITELINKS = [("Garage Floor Coatings", "garage-floor-coatings/", "Durable, easy-clean garage floors", "See finished garage projects"),
             ("Pool Deck Resurfacing", "pool-deck-resurfacing/", "Slip-resistant, UV-stable decks", "Cover a rough, dated pool deck"),
             ("Concrete Overlays", "concrete-overlays/", "Resurface worn concrete", "Driveways, patios and walkways"),
             ("Project Gallery", "gallery/", "See our recent concrete work", "Garage floors, decks and more"),
             ("About Us", "about-us/", "Family owned and operated", "Nearly 10 years in concrete")]
CALLOUTS = ["Family Owned & Operated", "Slip-Resistant Pool Decks", "UV-Stable Coatings", "Easy to Clean",
            "Residential & Commercial", "Limited Projects Monthly"]
SNIPPET = ("Services", ["Garage Floor Coatings", "Pool Deck Resurfacing", "Concrete Overlays", "Concrete Staining", "Polished Concrete"])

# --- static checks
for c in CAMPAIGNS:
    for g in c["groups"]:
        assert 3 <= len(g["h"]) <= 15 and 2 <= len(g["d"]) <= 4, g["name"]
        for h in g["h"]: assert len(h) <= 30, f"headline too long ({len(h)}): {h}"
        for d in g["d"]: assert len(d) <= 90, f"description too long ({len(d)}): {d}"
        assert len(set(g["h"])) == len(g["h"]), f"dupe headline in {g['name']}"
        assert all(len(p) <= 15 for p in g["path"])
        for k, _ in g["kw"]:
            hit = [n for n in NEGATIVES if f" {n} " in f" {k} "]
            assert not hit, f"negative {hit} blocks keyword '{k}'"
        for t in g["h"] + g["d"]:
            assert not any(w in t.lower() for w in ["free", "discount", "% off", "sale", "deal", "warranty", "—", "–"]), t
for s in SITELINKS: assert len(s[0]) <= 25 and len(s[2]) <= 35 and len(s[3]) <= 35, s
for c in CALLOUTS: assert len(c) <= 25, c
assert all(len(v) <= 25 for v in SNIPPET[1])

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums

# --- guards
names = [c["name"] for c in CAMPAIGNS]
existing = [r.campaign.name for r in q("SELECT campaign.name FROM campaign WHERE campaign.status != 'REMOVED'")]
if any(n in existing for n in names): sys.exit(f"ABORT: already built: {[n for n in names if n in existing]}")
if [r for r in q("SELECT shared_set.name FROM shared_set WHERE shared_set.status = 'ENABLED'") if r.shared_set.name == LIST_NAME]:
    sys.exit("ABORT: negative list already exists")
if q("SELECT customer_asset.resource_name FROM customer_asset WHERE customer_asset.field_type = 'CALL' AND customer_asset.status = 'ENABLED'"):
    sys.exit("ABORT: an account-level call asset exists (old agency number would attach)")
print(f"guards ok. existing campaigns: {len(existing)}")

ops, tmp = [], [0]
def tid():
    tmp[0] -= 1
    return tmp[0]
def op(kind):
    o = client.get_type("MutateOperation")
    ops.append(o)
    return getattr(o, kind).create

# shared negative list
ss_id = tid()
ss = op("shared_set_operation")
ss.resource_name = ga.shared_set_path(CID, ss_id); ss.name = LIST_NAME; ss.type_ = E.SharedSetTypeEnum.NEGATIVE_KEYWORDS
for n in NEGATIVES:
    sc = op("shared_criterion_operation")
    sc.shared_set = ga.shared_set_path(CID, ss_id); sc.keyword.text = n; sc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE

# assets (shared by both campaigns)
asset_links = []
for text, path, d1, d2 in SITELINKS:
    a_id = tid(); a = op("asset_operation"); a.resource_name = ga.asset_path(CID, a_id)
    a.final_urls.append(SITE + path); a.sitelink_asset.link_text = text
    a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    asset_links.append((a_id, E.AssetFieldTypeEnum.SITELINK))
for text in CALLOUTS:
    a_id = tid(); a = op("asset_operation"); a.resource_name = ga.asset_path(CID, a_id); a.callout_asset.callout_text = text
    asset_links.append((a_id, E.AssetFieldTypeEnum.CALLOUT))
a_id = tid(); a = op("asset_operation"); a.resource_name = ga.asset_path(CID, a_id)
a.structured_snippet_asset.header = SNIPPET[0]; a.structured_snippet_asset.values.extend(SNIPPET[1])
asset_links.append((a_id, E.AssetFieldTypeEnum.STRUCTURED_SNIPPET))

for c in CAMPAIGNS:
    b_id, c_id = tid(), tid()
    b = op("campaign_budget_operation")
    b.resource_name = ga.campaign_budget_path(CID, b_id); b.name = f"{c['name']} budget"
    b.amount_micros = int(c["budget"] * 1e6); b.delivery_method = E.BudgetDeliveryMethodEnum.STANDARD; b.explicitly_shared = False
    k = op("campaign_operation")
    k.resource_name = ga.campaign_path(CID, c_id); k.name = c["name"]; k.status = E.CampaignStatusEnum.PAUSED
    k.advertising_channel_type = E.AdvertisingChannelTypeEnum.SEARCH
    k.campaign_budget = ga.campaign_budget_path(CID, b_id)
    k.target_spend.cpc_bid_ceiling_micros = int(c["cap"] * 1e6)
    k.network_settings.target_google_search = True; k.network_settings.target_search_network = False
    k.network_settings.target_content_network = False; k.network_settings.target_partner_search_network = False
    k.geo_target_type_setting.positive_geo_target_type = E.PositiveGeoTargetTypeEnum.PRESENCE
    k.contains_eu_political_advertising = E.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    for t in (E.AssetAutomationTypeEnum.TEXT_ASSET_AUTOMATION, E.AssetAutomationTypeEnum.FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION):
        s = client.get_type("Campaign").AssetAutomationSetting()
        s.asset_automation_type = t; s.asset_automation_status = E.AssetAutomationStatusEnum.OPTED_OUT
        k.asset_automation_settings.append(s)
    for g_id in GEO:
        cc = op("campaign_criterion_operation"); cc.campaign = ga.campaign_path(CID, c_id)
        cc.location.geo_target_constant = f"geoTargetConstants/{g_id}"
    cc = op("campaign_criterion_operation"); cc.campaign = ga.campaign_path(CID, c_id)
    cc.language.language_constant = "languageConstants/1000"
    css = op("campaign_shared_set_operation")
    css.campaign = ga.campaign_path(CID, c_id); css.shared_set = ga.shared_set_path(CID, ss_id)
    for a_id, ft in asset_links:
        ca = op("campaign_asset_operation"); ca.campaign = ga.campaign_path(CID, c_id)
        ca.asset = ga.asset_path(CID, a_id); ca.field_type = ft
    for g in c["groups"]:
        ag_id = tid()
        ag = op("ad_group_operation")
        ag.resource_name = ga.ad_group_path(CID, ag_id); ag.name = g["name"]; ag.campaign = ga.campaign_path(CID, c_id)
        ag.status = E.AdGroupStatusEnum.ENABLED; ag.type_ = E.AdGroupTypeEnum.SEARCH_STANDARD
        for text, mt in g["kw"]:
            kc = op("ad_group_criterion_operation"); kc.ad_group = ga.ad_group_path(CID, ag_id)
            kc.status = E.AdGroupCriterionStatusEnum.ENABLED; kc.keyword.text = text
            kc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
        ad = op("ad_group_ad_operation"); ad.ad_group = ga.ad_group_path(CID, ag_id); ad.status = E.AdGroupAdStatusEnum.ENABLED
        ad.ad.final_urls.append(g["url"])
        ad.ad.responsive_search_ad.path1 = g["path"][0]
        if g["path"][1]: ad.ad.responsive_search_ad.path2 = g["path"][1]
        for h in g["h"]:
            x = client.get_type("AdTextAsset"); x.text = h; ad.ad.responsive_search_ad.headlines.append(x)
        for d in g["d"]:
            x = client.get_type("AdTextAsset"); x.text = d; ad.ad.responsive_search_ad.descriptions.append(x)

print(f"{len(ops)} operations, {'APPLYING' if APPLY else 'validate_only'}")
resp = ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
if not APPLY:
    print("VALIDATE OK")
    sys.exit()

# --- read-back
print("APPLIED")
for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
        campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.name LIKE 'TSD_10.22_Search_%'"""):
    k = r.campaign
    print(f"   {k.id} {k.name} {k.status.name} {k.bidding_strategy_type.name} cap ${k.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
          f"budget ${r.campaign_budget.amount_micros/1e6:.2f} partners={k.network_settings.target_search_network} "
          f"display={k.network_settings.target_content_network} geo={k.geo_target_type_setting.positive_geo_target_type.name}")
for r in q("""SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad WHERE campaign.name LIKE 'TSD_10.22_Search_%'"""):
    print(f"   ad {r.ad_group_ad.ad.id} {r.campaign.name} / {r.ad_group.name}: {r.ad_group_ad.policy_summary.approval_status.name}")
n = q("""SELECT campaign.name, ad_group_criterion.keyword.text FROM keyword_view WHERE campaign.name LIKE 'TSD_10.22_Search_%'""")
print(f"   keywords: {len(n)}")
for r in q("""SELECT campaign.name, campaign_criterion.location.geo_target_constant FROM campaign_criterion
        WHERE campaign.name LIKE 'TSD_10.22_Search_%' AND campaign_criterion.type = 'LOCATION'"""):
    print(f"   geo {r.campaign.name}: {r.campaign_criterion.location.geo_target_constant}")
for r in q(f"""SELECT shared_set.id, shared_set.name, shared_set.member_count, shared_set.reference_count FROM shared_set WHERE shared_set.status = 'ENABLED'"""):
    if r.shared_set.name == LIST_NAME:
        print(f"   list {r.shared_set.id} members={r.shared_set.member_count} attached={r.shared_set.reference_count}")
