# ALREADY APPLIED LIVE 2026-10-09 -> created campaign 24336822932 / asset group 6757854855 (PAUSED). Do NOT re-run with --apply (it would create a second copy).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754), 2026-10-09. Edu: "Revive the Feb PMax but keep within the current budget" + "can't you just
duplicate the campaign". The API has no copy endpoint and the old campaign's CUSTOM_PERIOD budget blocks reviving it, so
this rebuilds it 1:1 from the SAME asset IDs as a new campaign, created PAUSED:
  - budget $30/d DAILY (funded by Nonbranded $55 -> $25, done separately when this is enabled: constant total)
  - Max Conversions, tCPA $50 (as before); geo Mansfield (1026591) PRESENCE (old: presence or interest); English
  - brand guidelines on: BUSINESS_NAME + 2 LOGO + LANDSCAPE_LOGO as campaign assets; 6 sitelinks; + call asset 817-442-6949
  - asset automation as before: image extraction OPTED_OUT, final URL expansion OPTED_IN
  - 1 asset group, homepage, the old asset group's enabled assets + its 4 search themes, adjusted to what Google accepts now:
      * old group is over today's caps (17 headlines > 15, 8 long headlines > 5): dropped headlines "Get Your AC Ready"
        (summer) + "Call to set an appointment" (dup); long headlines "Call our HVAC experts to set an appointment" (dup),
        "Top-rated residential and commercial services" (generic), "1 Trusted Heating and AC Experts Mansfield, TX | C&S Air"
      * 2nd LOGO 333622193251 rejected (image dimensions not allowed) -> not attached
      * audience signal 339207432 is an AssetGroupPersona bound to the old asset group -> can't be reused
Old campaign 23584282933 is left untouched.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "5563867754"
OLD_AG = "6676624607"
APPLY = "--apply" in sys.argv
NAME = "TSD_10.09_PMax_Leads_Mansfield"

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums

old_assets = [(r.asset_group_asset.asset, r.asset_group_asset.field_type) for r in ga.search(customer_id=CID, query=f"""
    SELECT asset_group_asset.asset, asset_group_asset.field_type FROM asset_group_asset
    WHERE asset_group.id = {OLD_AG} AND asset_group_asset.status = 'ENABLED'""")]
old_signals = [(r.asset_group_signal.search_theme.text, r.asset_group_signal.audience.audience) for r in ga.search(customer_id=CID, query=f"""
    SELECT asset_group_signal.search_theme.text, asset_group_signal.audience.audience FROM asset_group_signal
    WHERE asset_group.id = {OLD_AG}""")]
DROP = {"332814404246", "138166563999", "81826777805", "138166563996", "112038933484"}
old_assets = [(a, ft) for a, ft in old_assets if a.split("/")[-1] not in DROP]
old_signals = [(t, a) for t, a in old_signals if t]
print(f"copying: {len(old_assets)} assets, {len(old_signals)} search themes")

BUDGET, CAMP, AGRP = ga.campaign_budget_path(CID, "-1"), ga.campaign_path(CID, "-2"), ga.asset_group_path(CID, "-3")
ops = []


def op():
    m = client.get_type("MutateOperation")
    ops.append(m)
    return m


b = op().campaign_budget_operation.create
b.resource_name = BUDGET
b.name = f"{NAME} daily"
b.amount_micros = 30_000_000
b.period = E.BudgetPeriodEnum.DAILY
b.delivery_method = E.BudgetDeliveryMethodEnum.STANDARD
b.explicitly_shared = False

c = op().campaign_operation.create
c.resource_name = CAMP
c.name = NAME
c.advertising_channel_type = E.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
c.status = E.CampaignStatusEnum.PAUSED
c.campaign_budget = BUDGET
c.maximize_conversions.target_cpa_micros = 50_000_000
c.geo_target_type_setting.positive_geo_target_type = E.PositiveGeoTargetTypeEnum.PRESENCE
c.brand_guidelines_enabled = True
c.contains_eu_political_advertising = E.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
for t, s in ((E.AssetAutomationTypeEnum.GENERATE_IMAGE_EXTRACTION, E.AssetAutomationStatusEnum.OPTED_OUT),
             (E.AssetAutomationTypeEnum.FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION, E.AssetAutomationStatusEnum.OPTED_IN)):
    st = client.get_type("Campaign").AssetAutomationSetting()
    st.asset_automation_type, st.asset_automation_status = t, s
    c.asset_automation_settings.append(st)

cc = op().campaign_criterion_operation.create
cc.campaign = CAMP
cc.location.geo_target_constant = "geoTargetConstants/1026591"
cc = op().campaign_criterion_operation.create
cc.campaign = CAMP
cc.language.language_constant = "languageConstants/1000"

CAMPAIGN_ASSETS = [("332942413848", "BUSINESS_NAME"), ("332941675083", "LOGO"),
                   ("332894617222", "LANDSCAPE_LOGO"), ("343525874146", "CALL")] + \
                  [(a, "SITELINK") for a in ("332814014195", "332814181355", "332814404285", "332814404288",
                                             "332942299128", "332942398329")]
for asset_id, ft in CAMPAIGN_ASSETS:
    ca = op().campaign_asset_operation.create
    ca.campaign = CAMP
    ca.asset = ga.asset_path(CID, asset_id)
    ca.field_type = getattr(E.AssetFieldTypeEnum, ft)

ag = op().asset_group_operation.create
ag.resource_name = AGRP
ag.campaign = CAMP
ag.name = "Asset Group 1"
ag.final_urls.append("https://www.candsair.com/")
ag.status = E.AssetGroupStatusEnum.ENABLED

for asset, ft in old_assets:
    aga = op().asset_group_asset_operation.create
    aga.asset_group = AGRP
    aga.asset = asset
    aga.field_type = ft

for theme, audience in old_signals:
    sg = op().asset_group_signal_operation.create
    sg.asset_group = AGRP
    if theme:
        sg.search_theme.text = theme
    else:
        sg.audience.audience = audience

resp = ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
print(f"batch of {len(ops)} ops: {'APPLIED (campaign PAUSED)' if APPLY else 'validate_only OK'}")
if APPLY:
    for r in resp.mutate_operation_responses:
        if r.campaign_result.resource_name:
            print("new campaign:", r.campaign_result.resource_name)
        if r.asset_group_result.resource_name:
            print("new asset group:", r.asset_group_result.resource_name)
