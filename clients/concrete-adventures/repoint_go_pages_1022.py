# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), 2026-10-22, after Edu: tracking = TSD GTM-53FXJRN4, which lives on the go. pages
(https://go.concrete-adventures.com and /decorative-concrete/), not on www (old agency GTM-KV5TR7CK).
1. Final URLs: Branded RSA -> go. homepage; the 3 Nonbranded RSAs -> /decorative-concrete/ (form on page).
2. Sitelinks: unlink the 5 www sitelinks from both TSD_10.22 campaigns, add 6 go. sitelinks (distinct ?src=N, Cool Hand pattern).
3. Call asset (662) 498-5409 on both campaigns: Johnny's Ads number in the client's own CallRail (source 'Google Ads Assets',
   forwards to 662-291-7755), per his Slack DM 2026-10-21. Same number shown on both go. pages.
Campaigns stay PAUSED. Aborts if either campaign is not PAUSED or the ads/links differ from the 10-22 build.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9215192296"
APPLY = "--apply" in sys.argv
CAMPS = {"24379794681": "Branded", "24379794684": "Nonbranded"}
GO = "https://go.concrete-adventures.com/"
LP = GO + "decorative-concrete/"
ADS = {"829340074238": GO, "829340074529": LP, "829340074541": LP, "829340074556": LP}
PHONE = "(662) 498-5409"
SITELINKS = [("Garage Floor Coatings", GO + "?src=1", "Tough, chemical-resistant finish", "For homes and businesses"),
             ("Pool Deck Resurfacing", GO + "?src=2", "Cooler underfoot, slip-resistant", "Patios and walkways too"),
             ("Concrete Overlays", GO + "?src=3", "Refresh worn concrete", "No need to tear out the slab"),
             ("Concrete Staining", GO + "?src=4", "Rich, lasting color", "Patios, driveways and floors"),
             ("Request an Estimate", LP + "?src=5", "Tell us about your project", "We'll be in touch"),
             ("Customer Reviews", GO + "?src=6", "See what customers say", "Projects across Mississippi")]
for s in SITELINKS: assert len(s[0]) <= 25 and len(s[2]) <= 35 and len(s[3]) <= 35, s

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums
ids = ",".join(CAMPS)

# --- guards
for r in q(f"SELECT campaign.id, campaign.status FROM campaign WHERE campaign.id IN ({ids})"):
    if r.campaign.status.name != "PAUSED": sys.exit(f"ABORT: campaign {r.campaign.id} is {r.campaign.status.name}")
ads = {str(r.ad_group_ad.ad.id): list(r.ad_group_ad.ad.final_urls) for r in q(f"""SELECT campaign.id, ad_group_ad.ad.id, ad_group_ad.ad.final_urls
    FROM ad_group_ad WHERE campaign.id IN ({ids}) AND ad_group_ad.status != 'REMOVED'""")}
if set(ads) != set(ADS): sys.exit(f"ABORT: ads differ from build: {ads}")
print("current final URLs:", ads)
links = q(f"""SELECT campaign.id, campaign_asset.resource_name, campaign_asset.field_type, asset.final_urls, asset.call_asset.phone_number
    FROM campaign_asset WHERE campaign.id IN ({ids}) AND campaign_asset.status != 'REMOVED'""")
sl = [r for r in links if r.campaign_asset.field_type.name == "SITELINK"]
if len(sl) != 10 or not all("www.concrete-adventures.com" in r.asset.final_urls[0] for r in sl): sys.exit(f"ABORT: expected 10 www sitelink links, got {len(sl)}")
if [r for r in links if r.campaign_asset.field_type.name == "CALL"]: sys.exit("ABORT: a call asset is already linked")

ops, tmp = [], [0]
def tid():
    tmp[0] -= 1
    return tmp[0]
def mop():
    o = client.get_type("MutateOperation"); ops.append(o); return o

# 1. final URLs
for ad_id, url in ADS.items():
    o = mop(); a = o.ad_operation.update
    a.resource_name = ga.ad_path(CID, ad_id); a.final_urls.append(url)
    o.ad_operation.update_mask.paths.append("final_urls")
# 2. sitelinks: unlink www, create + link go.
for r in sl:
    mop().campaign_asset_operation.remove = r.campaign_asset.resource_name
new_assets = []
for text, url, d1, d2 in SITELINKS:
    a_id = tid(); a = mop().asset_operation.create; a.resource_name = ga.asset_path(CID, a_id)
    a.final_urls.append(url); a.sitelink_asset.link_text = text; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    new_assets.append((a_id, E.AssetFieldTypeEnum.SITELINK))
# 3. call asset
a_id = tid(); a = mop().asset_operation.create; a.resource_name = ga.asset_path(CID, a_id)
a.call_asset.country_code = "US"; a.call_asset.phone_number = PHONE
a.call_asset.call_conversion_reporting_state = E.CallConversionReportingStateEnum.USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION
new_assets.append((a_id, E.AssetFieldTypeEnum.CALL))
for c_id in CAMPS:
    for a_id, ft in new_assets:
        ca = mop().campaign_asset_operation.create
        ca.campaign = ga.campaign_path(CID, c_id); ca.asset = ga.asset_path(CID, a_id); ca.field_type = ft

print(f"{len(ops)} operations, {'APPLYING' if APPLY else 'validate_only'}")
ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": not APPLY})
if not APPLY:
    print("VALIDATE OK"); sys.exit()

print("APPLIED")
for r in q(f"""SELECT campaign.id, campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad WHERE campaign.id IN ({ids}) AND ad_group_ad.status != 'REMOVED'"""):
    print(f"   ad {r.ad_group_ad.ad.id} {r.ad_group.name}: {list(r.ad_group_ad.ad.final_urls)} {r.ad_group_ad.policy_summary.approval_status.name}")
for r in q(f"""SELECT campaign.id, campaign.name, campaign_asset.field_type, asset.final_urls, asset.sitelink_asset.link_text, asset.call_asset.phone_number
        FROM campaign_asset WHERE campaign.id IN ({ids}) AND campaign_asset.status != 'REMOVED' AND campaign_asset.field_type IN ('SITELINK','CALL')"""):
    print(f"   {r.campaign.name} {r.campaign_asset.field_type.name}: {r.asset.sitelink_asset.link_text or r.asset.call_asset.phone_number} {list(r.asset.final_urls)}")
