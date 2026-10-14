"""Cool Hand 2026-10-09 (Edu's rule): NOTHING goes to coolhandelectric.com, only go.coolhandelectric.com.
ALREADY APPLIED 2026-10-09, don't re-run.
1) Every non-removed ad still on a main-site URL (paused old ads + ads in paused ad groups) -> go. page by trade:
   Electrical -> /electrician/, AC groups -> /ac-repair/, other HVAC groups -> /hvac-repair/.
2) Unlinks every main-site sitelink (campaign + ad group + account level). Assets stay, links go.
3) New "Schedule Service" sitelink -> go./ . Sitelinks never point at the ad's own page:
   Electrical campaign: Schedule Service + AC Repair + Heating & HVAC Repair
   HVAC campaign (fallback): Schedule Service + Electrician Services
   HVAC ad groups: AC groups get + Heating & HVAC Repair, other HVAC groups get + AC Repair (plus the 2 fallback ones)
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys, time
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client
from google.api_core import protobuf_helpers

CID = "9865206319"
GO = "https://go.coolhandelectric.com/"
AC_GROUPS = {"AC-Repair", "AC-Installation"}
# existing go. sitelink assets (created earlier 10-09)
ELECTRICIAN, AC, HEATING = "428923086331", "428923079863", "428923086340"

c = init_client(); ga = c.get_service("GoogleAdsService")
def q(s): return list(ga.search(customer_id=CID, query=s))
def is_main(urls): return any("coolhandelectric.com" in u and "go.coolhandelectric.com" not in u for u in urls)
def arn(aid): return ga.asset_path(CID, aid)

# 1) ads
ad_ops = []
for r in q("""SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_mobile_urls
  FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' AND campaign.status != 'REMOVED' AND ad_group.status != 'REMOVED'"""):
    ad = r.ad_group_ad.ad
    if not is_main(list(ad.final_urls) + list(ad.final_mobile_urls)): continue
    if r.campaign.name == "TSD_Search_Electrical": url = GO + "electrician/"
    elif r.campaign.name == "TSD_Search_HVAC": url = GO + ("ac-repair/" if r.ad_group.name in AC_GROUPS else "hvac-repair/")
    elif r.campaign.name == "TSD_Search_Branded": url = GO
    else: raise SystemExit(f"unmapped ad {ad.id} in {r.campaign.name}")
    op = c.get_type("AdOperation"); u = op.update
    u.resource_name = c.get_service("AdService").ad_path(CID, ad.id)
    u.final_urls.append(url)
    paths = ["final_urls"] + (["final_mobile_urls"] if list(ad.final_mobile_urls) else [])
    op.update_mask.paths.extend(paths)
    ad_ops.append(op); print(f"ad {ad.id} {r.ad_group.name} -> {url}")
res = c.get_service("AdService").mutate_ads(customer_id=CID, operations=ad_ops)
print("ads updated:", len(res.results))

# 2) unlink main-site sitelinks at every level
rm_c = [r.campaign_asset.resource_name for r in q("""SELECT campaign_asset.resource_name, asset.final_urls FROM campaign_asset
  WHERE campaign_asset.field_type='SITELINK' AND campaign_asset.status != 'REMOVED'""") if is_main(list(r.asset.final_urls))]
rm_ag = [r.ad_group_asset.resource_name for r in q("""SELECT ad_group_asset.resource_name, asset.final_urls FROM ad_group_asset
  WHERE ad_group_asset.field_type='SITELINK' AND ad_group_asset.status != 'REMOVED'""") if is_main(list(r.asset.final_urls))]
rm_cu = [r.customer_asset.resource_name for r in q("""SELECT customer_asset.resource_name, asset.final_urls FROM customer_asset
  WHERE customer_asset.field_type='SITELINK' AND customer_asset.status != 'REMOVED'""") if is_main(list(r.asset.final_urls))]
cas, agas, cuas = c.get_service("CampaignAssetService"), c.get_service("AdGroupAssetService"), c.get_service("CustomerAssetService")
def remove(svc, typ, fn, rns):
    ops = []
    for rn in rns:
        op = c.get_type(typ); op.remove = rn; ops.append(op)
    return len(getattr(svc, fn)(customer_id=CID, operations=ops).results) if ops else 0
print("unlinked campaign:", remove(cas, "CampaignAssetOperation", "mutate_campaign_assets", rm_c))
print("unlinked ad group:", remove(agas, "AdGroupAssetOperation", "mutate_ad_group_assets", rm_ag))
try:
    print("unlinked account:", remove(cuas, "CustomerAssetOperation", "mutate_customer_assets", rm_cu))
except Exception as e:
    print("account remove failed, pausing instead:", str(e)[:300])
    ops = []
    for rn in rm_cu:
        op = c.get_type("CustomerAssetOperation"); op.update.resource_name = rn
        op.update.status = c.enums.AssetLinkStatusEnum.PAUSED
        op.update_mask.paths.append("status"); ops.append(op)
    print("paused account:", len(cuas.mutate_customer_assets(customer_id=CID, operations=ops).results))
time.sleep(2)

# 3) new Schedule Service asset + go. links
op = c.get_type("AssetOperation"); a = op.create
a.sitelink_asset.link_text = "Schedule Service"
a.sitelink_asset.description1 = "Request service online"
a.sitelink_asset.description2 = "Serving Mansfield & Red Oak"
a.final_urls.append(GO)
SCHED = c.get_service("AssetService").mutate_assets(customer_id=CID, operations=[op]).results[0].resource_name.split("/")[-1]
print("created Schedule Service asset:", SCHED)

camp = {r.campaign.name: r.campaign.id for r in q("SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name IN ('TSD_Search_Electrical','TSD_Search_HVAC')")}
ops = []
for cname, aids in (("TSD_Search_Electrical", [SCHED, AC, HEATING]), ("TSD_Search_HVAC", [SCHED, ELECTRICIAN])):
    for aid in aids:
        op = c.get_type("CampaignAssetOperation"); l = op.create
        l.campaign = ga.campaign_path(CID, camp[cname]); l.asset = arn(aid)
        l.field_type = c.enums.AssetFieldTypeEnum.SITELINK; ops.append(op)
print("campaign links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))

ops = []
for r in q("SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.name = 'TSD_Search_HVAC' AND ad_group.status != 'REMOVED'"):
    cross = HEATING if r.ad_group.name in AC_GROUPS else AC
    for aid in (SCHED, cross, ELECTRICIAN):
        op = c.get_type("AdGroupAssetOperation"); l = op.create
        l.ad_group = ga.ad_group_path(CID, r.ad_group.id); l.asset = arn(aid)
        l.field_type = c.enums.AssetFieldTypeEnum.SITELINK; ops.append(op)
    print(f"  {r.ad_group.name}: Schedule Service + {'Heating & HVAC Repair' if cross == HEATING else 'AC Repair'} + Electrician Services")
print("ad group links:", len(agas.mutate_ad_group_assets(customer_id=CID, operations=ops).results))
