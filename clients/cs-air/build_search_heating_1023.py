# APPLIED LIVE 2026-10-23 (built PAUSED, campaign 24383234148). Do NOT re-run with --apply.
# APPLIED LIVE 2026-10-23 (built PAUSED). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), heating Search build, 2026-10-23. Edu: "Build it for me" (after pausing PMax + Cooling NB the
same day, ~$135/d freed; plan: one heating campaign ~$30/d, phrase + exact, Max Clicks with a CPC cap).
- TSD_10.23_Search_Nonbranded_Heating  $30/day, Maximize Clicks, $12 max CPC (Cooling NB averaged ~$8.66/click)
  Ad groups: Heating Repair -> /heating-repair/, Heating Replacement -> /heating-replacement/. No maintenance group
  (the Cooling tune-up keywords drew price research and never converted).
Built PAUSED. Google Search only, presence-only geo = the same 10 locations as Branded/Cooling, English, AI Max text
+ final URL expansion opted out. Call asset 343525874146 (CallRail Google Ads tracker 817-442-6949), reused callouts /
sitelinks / business name + logo, 3 new heating sitelinks + 3 new callouts. 'Competitos May' list attached + curated
campaign negatives. The Cooling campaign's 708 negatives are NOT copied: they include furnace, heat, replacement,
burner, not working. Ad copy uses only claims on the heating pages (checked 10-23): same-day service, licensed &
insured, background-checked techs, all makes/models, 20+ years, upfront price, 5-star Google rating, financing
(replacement page). No '24/7' and no 'Since 1958' (not on the heating pages).
One atomic GoogleAdsService.mutate with temp ids. Aborts if the campaign already exists.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "5563867754"
APPLY = "--apply" in sys.argv
SITE = "https://www.candsair.com/"
HEAT = SITE + "services/residential/heating/"
NAME = "TSD_10.23_Search_Nonbranded_Heating"
BUDGET, CAP = 30.0, 12.0
GEO = [1026194, 1026257, 1026411, 1026439, 1026523, 1026591, 1026623, 9051585, 9191716, 9219741]  # same as Branded
COMPETITOR_LIST = "9228503611"  # 'Competitos May'
CALL_ASSET = "343525874146"
REUSE = {  # existing assets, linked at campaign level
    "SITELINK": ["339652160216", "340444969557", "340446011643", "339652160213"],  # Schedule Service, Reviews, Financing, About
    "CALLOUT": ["339651537935", "339651537941", "339651537944", "340297835693"],   # Family Owned, Licensed & Insured, 20+ yrs, Same Day
    "BUSINESS_NAME": ["335345533462"], "BUSINESS_LOGO": ["333622193251"],
}
NEW_SITELINKS = [("Heating Repair", HEAT + "heating-repair/", "Furnace and heat pump repair", "Same-day service available"),
                 ("Heating Replacement", HEAT + "heating-replacement/", "Honest evaluation first", "Financing is available"),
                 ("Heating Maintenance", HEAT + "heating-maintenance/", "Keep your system running", "Catch problems early")]
NEW_CALLOUTS = ["Upfront Pricing", "All Makes & Models", "Background-Checked Techs"]

NEGATIVES = ["water heater", "water heaters", "hot water", "tankless", "pool heater", "space heater", "space heaters",
             "portable", "electric heater", "car", "truck", "rv", "auto", "vehicle", "how to", "how do", "diy", "youtube",
             "reddit", "manual", "parts", "jobs", "job", "hiring", "salary", "career", "careers", "training", "school",
             "certification", "home depot", "lowes", "amazon", "walmart", "wood stove", "fireplace", "cost", "price",
             "prices", "cheap", "used", "for sale",
             # competitors seen in the Cooling search terms (Competitos May list is attached too)
             "anderson air", "texas air", "christmas air", "milestone", "a 1 air", "comfort masters", "compass air",
             "airplex", "american heating and air", "copeland air", "anthony air", "michael and sons", "chill brothers",
             "always there air", "family first comfort", "tk mechanical", "minuteman heating", "walker hvac", "lex hvac",
             "casa mechanical", "barnett", "the ac lady", "enoch hvac", "o daniel", "markl", "derden", "klund", "trutex",
             "houk", "honest abe", "texas best"]

FIRM = "C&S Air has repaired furnaces and heat pumps across Mansfield and DFW for over 20 years."
GROUPS = [
    {"name": "Heating Repair", "url": HEAT + "heating-repair/", "path": ("Heating-Repair", "Mansfield"),
     "kw": [(k, "PHRASE") for k in ["furnace repair", "heater repair", "heating repair", "heat pump repair",
                                     "furnace not working", "heater not working", "heat not working", "no heat",
                                     "furnace service", "heating service", "heater service"]]
           + [(k, "EXACT") for k in ["furnace repair near me", "heating repair near me", "heater repair near me",
                                      "heat pump repair near me", "furnace repair mansfield tx", "heater repair mansfield"]],
     "h": ["Heating Repair in Mansfield", "Furnace Repair Near You", "Heat Pump Repair", "Same-Day Heating Repair",
           "No Heat? Call C&S Air", "Upfront Price Before Work", "Licensed & Insured Techs", "Background-Checked Techs",
           "All Makes and Models", "Over 20 Years in DFW", "5-Star Google Rating", "C&S Air Heating Repair",
           "Serving Mansfield & DFW", "Furnace Not Working?", "Call for Same-Day Service"],
     "d": ["Furnace or heat pump not heating? Our licensed techs find the real problem and fix it.",
           "You get an upfront price before any work begins. No surprise charges on the invoice.",
           "Same-day heating repair across Mansfield, Arlington and Fort Worth. Call C&S Air today.",
           "We repair all makes and models, including Trane, Lennox, Carrier, Rheem and Goodman."]},
    {"name": "Heating Replacement", "url": HEAT + "heating-replacement/", "path": ("New-Furnace", "Mansfield"),
     "kw": [(k, "PHRASE") for k in ["furnace replacement", "replace furnace", "new furnace", "furnace installation",
                                     "install furnace", "heat pump replacement", "heat pump installation",
                                     "new heat pump", "heating system replacement", "new heating system",
                                     "heating installation"]]
           + [(k, "EXACT") for k in ["furnace replacement near me", "new furnace near me", "furnace installation near me",
                                      "heat pump installation near me"]],
     "h": ["Furnace Replacement", "New Furnace Installation", "Heat Pump Replacement", "Heating Replacement DFW",
           "Honest Evaluation First", "Financing Is Available", "Sized and Installed Right", "Upfront Quote, No Surprises",
           "Licensed & Insured Techs", "All Makes and Models", "Over 20 Years in DFW", "5-Star Google Rating",
           "C&S Air Heating", "Serving Mansfield & DFW", "Time for a New System?"],
     "d": ["Old furnace costing more to run than it's worth? Get an honest read from our techs.",
           "We size and install your new furnace or heat pump correctly. Financing is available.",
           "You'll know the full scope and price before we schedule. No pressure, no surprises.", FIRM]},
]

# --- static checks
for g in GROUPS:
    assert 3 <= len(g["h"]) <= 15 and 2 <= len(g["d"]) <= 4, g["name"]
    for h in g["h"]: assert len(h) <= 30, f"headline too long ({len(h)}): {h}"
    for d in g["d"]: assert len(d) <= 90, f"description too long ({len(d)}): {d}"
    assert len(set(g["h"])) == len(g["h"]), f"dupe headline in {g['name']}"
    assert all(len(p) <= 15 for p in g["path"]), g["path"]
    for k, _ in g["kw"]:
        hit = [n for n in NEGATIVES if f" {n} " in f" {k} "]
        assert not hit, f"negative {hit} blocks keyword '{k}'"
    for t in g["h"] + g["d"]:
        assert not any(w in t.lower() for w in ["free", "24/7", "1958", "—", "–", "discount", "% off"]), t
for s in NEW_SITELINKS: assert len(s[0]) <= 25 and len(s[2]) <= 35 and len(s[3]) <= 35, s
for c in NEW_CALLOUTS: assert len(c) <= 25, c

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums

# --- guards
if [r for r in q("SELECT campaign.name FROM campaign WHERE campaign.status != 'REMOVED'") if r.campaign.name == NAME]:
    sys.exit("ABORT: campaign already exists")
ids = [a for v in REUSE.values() for a in v] + [CALL_ASSET]
got = {str(r.asset.id) for r in q(f"SELECT asset.id FROM asset WHERE asset.id IN ({','.join(ids)})")}
if set(ids) - got: sys.exit(f"ABORT: assets missing: {set(ids) - got}")
if not q(f"SELECT shared_set.id FROM shared_set WHERE shared_set.id = {COMPETITOR_LIST} AND shared_set.status = 'ENABLED'"):
    sys.exit("ABORT: competitor list missing")
print("guards ok")

ops, tmp = [], [0]
def tid():
    tmp[0] -= 1
    return tmp[0]
def op(kind):
    o = client.get_type("MutateOperation"); ops.append(o)
    return getattr(o, kind).create

links = [(ga.asset_path(CID, a), getattr(E.AssetFieldTypeEnum, ft)) for ft, v in REUSE.items() for a in v]
links.append((ga.asset_path(CID, CALL_ASSET), E.AssetFieldTypeEnum.CALL))
for text, url, d1, d2 in NEW_SITELINKS:
    a_id = tid(); a = op("asset_operation"); a.resource_name = ga.asset_path(CID, a_id)
    a.final_urls.append(url); a.sitelink_asset.link_text = text; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    links.append((ga.asset_path(CID, a_id), E.AssetFieldTypeEnum.SITELINK))
for text in NEW_CALLOUTS:
    a_id = tid(); a = op("asset_operation"); a.resource_name = ga.asset_path(CID, a_id); a.callout_asset.callout_text = text
    links.append((ga.asset_path(CID, a_id), E.AssetFieldTypeEnum.CALLOUT))

b_id, c_id = tid(), tid()
b = op("campaign_budget_operation")
b.resource_name = ga.campaign_budget_path(CID, b_id); b.name = f"{NAME} budget"
b.amount_micros = int(BUDGET * 1e6); b.delivery_method = E.BudgetDeliveryMethodEnum.STANDARD; b.explicitly_shared = False
k = op("campaign_operation")
k.resource_name = ga.campaign_path(CID, c_id); k.name = NAME; k.status = E.CampaignStatusEnum.PAUSED
k.advertising_channel_type = E.AdvertisingChannelTypeEnum.SEARCH; k.campaign_budget = ga.campaign_budget_path(CID, b_id)
k.target_spend.cpc_bid_ceiling_micros = int(CAP * 1e6)
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
cc = op("campaign_criterion_operation"); cc.campaign = ga.campaign_path(CID, c_id); cc.language.language_constant = "languageConstants/1000"
for n in NEGATIVES:
    cc = op("campaign_criterion_operation"); cc.campaign = ga.campaign_path(CID, c_id); cc.negative = True
    cc.keyword.text = n; cc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
css = op("campaign_shared_set_operation"); css.campaign = ga.campaign_path(CID, c_id); css.shared_set = ga.shared_set_path(CID, COMPETITOR_LIST)
for a_rn, ft in links:
    ca = op("campaign_asset_operation"); ca.campaign = ga.campaign_path(CID, c_id); ca.asset = a_rn; ca.field_type = ft
for g in GROUPS:
    ag_id = tid(); ag = op("ad_group_operation")
    ag.resource_name = ga.ad_group_path(CID, ag_id); ag.name = g["name"]; ag.campaign = ga.campaign_path(CID, c_id)
    ag.status = E.AdGroupStatusEnum.ENABLED; ag.type_ = E.AdGroupTypeEnum.SEARCH_STANDARD
    for text, mt in g["kw"]:
        kc = op("ad_group_criterion_operation"); kc.ad_group = ga.ad_group_path(CID, ag_id)
        kc.status = E.AdGroupCriterionStatusEnum.ENABLED; kc.keyword.text = text; kc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
    ad = op("ad_group_ad_operation"); ad.ad_group = ga.ad_group_path(CID, ag_id); ad.status = E.AdGroupAdStatusEnum.ENABLED
    ad.ad.final_urls.append(g["url"]); ad.ad.responsive_search_ad.path1 = g["path"][0]; ad.ad.responsive_search_ad.path2 = g["path"][1]
    for h in g["h"]:
        x = client.get_type("AdTextAsset"); x.text = h; ad.ad.responsive_search_ad.headlines.append(x)
    for d in g["d"]:
        x = client.get_type("AdTextAsset"); x.text = d; ad.ad.responsive_search_ad.descriptions.append(x)

print(f"{len(ops)} operations, {'APPLYING' if APPLY else 'validate_only'}")
ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
if not APPLY:
    print("VALIDATE OK"); sys.exit()

print("APPLIED")
for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network,
        campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.name = '{NAME}'"""):
    c = r.campaign
    print(f"   {c.id} {c.name} {c.status.name} {c.bidding_strategy_type.name} cap ${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
          f"budget ${r.campaign_budget.amount_micros/1e6:.2f} partners={c.network_settings.target_search_network} "
          f"display={c.network_settings.target_content_network} geo={c.geo_target_type_setting.positive_geo_target_type.name}")
for r in q(f"SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.name = '{NAME}'"):
    print(f"   ad {r.ad_group_ad.ad.id} / {r.ad_group.name} ({r.ad_group.id}): {r.ad_group_ad.policy_summary.approval_status.name}")
print("   keywords:", len(q(f"SELECT ad_group_criterion.criterion_id FROM ad_group_criterion WHERE campaign.name = '{NAME}' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE")))
print("   geo:", len(q(f"SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.name = '{NAME}' AND campaign_criterion.type = 'LOCATION'")),
      "| negatives:", len(q(f"SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.name = '{NAME}' AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE")),
      "| assets:", len(q(f"SELECT campaign.name, campaign_asset.resource_name FROM campaign_asset WHERE campaign.name = '{NAME}'")),
      "| shared lists:", len(q(f"SELECT campaign.name, campaign_shared_set.resource_name FROM campaign_shared_set WHERE campaign.name = '{NAME}'")))
