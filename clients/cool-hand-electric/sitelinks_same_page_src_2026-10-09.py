"""Cool Hand 2026-10-09 (Edu's rule): every sitelink goes to the SAME go. page as its ad, made distinct with ?src=1, ?src=2...
ALREADY APPLIED 2026-10-09, don't re-run.
  Electrical campaign            -> go./electrician/?src=N
  HVAC campaign (HVAC groups)    -> go./hvac-repair/?src=N
  AC-Repair + AC-Installation    -> go./ac-repair/?src=N   (ad-group level, overrides the campaign set)
  Branded + YouTube campaigns    -> go./?src=N
Replaces the cross-trade sitelinks (Electrical ads showing AC/HVAC links etc). Old links are unlinked, assets kept.
Link text + descriptions use only what the live page says (checked 10-09).
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys, time
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client

CID = "9865206319"
GO = "https://go.coolhandelectric.com/"
SETS = {
    "electrician/": [
        ("Get Your Electrical Quote", "Short form, we call you back", "Easy payment plans available"),
        ("$37 Safety Inspection", "Ask about it when you book", "Licensed TECL #31768"),
        ("Panel Upgrades", "Licensed, local electricians", "Every job done to code"),
        ("Surge Protection", "Licensed, local electricians", "Options in writing up front"),
        ("EV Charger Installation", "New circuits done to code", "Family-owned and local"),
        ("Generator Installation", "New circuits done to code", "Voted Best in Ellis County"),
    ],
    "ac-repair/": [
        ("Request AC Repair", "Short form, we call you back", "Easy payment plans available"),
        ("AC Blowing Warm Air?", "We fix it right the first time", "Family-owned and local"),
        ("AC Installation", "We install and replace AC systems", "Repair or replace, you choose"),
        ("Repair or Replace?", "We lay out both options", "Voted Best in Ellis County"),
    ],
    "hvac-repair/": [
        ("Request HVAC Service", "Short form, we call you back", "Easy payment plans available"),
        ("Furnace Repair", "Furnace repair and replacement", "Family-owned and local"),
        ("Heat Pump Repair", "Heat pumps, AC and furnaces", "Voted Best in Ellis County"),
        ("AC Repair & Replacement", "From AC to furnace, we handle it", "BBB A+ Rating"),
        ("Thermostats & Air Quality", "Thermostats and duct cleaning", "Plus indoor air quality"),
    ],
    "": [
        ("Electrical Services", "Award-winning electrical work", "Family owned and local"),
        ("AC Repair", "AC repair in Mansfield, TX", "Licensed, trained professionals"),
        ("Furnace Repair", "Furnace repair in Mansfield, TX", "Clean, organized workmanship"),
        ("Book Online", "Schedule your service today", "Reliable, responsive service"),
    ],
}
for page, rows in SETS.items():
    for t, d1, d2 in rows:
        assert len(t) <= 25 and len(d1) <= 35 and len(d2) <= 35, (t, len(t), d1, len(d1), d2, len(d2))
AC_GROUPS = {"AC-Repair", "AC-Installation"}
CAMPAIGN_SET = {"TSD_Search_Electrical": "electrician/", "TSD_Search_HVAC": "hvac-repair/",
                "TSD_Search_Branded": "", "TSD_YouTube": ""}

c = init_client(); ga = c.get_service("GoogleAdsService")
def q(s): return list(ga.search(customer_id=CID, query=s))
cas, agas = c.get_service("CampaignAssetService"), c.get_service("AdGroupAssetService")
names = "','".join(CAMPAIGN_SET)

# 1) unlink every current sitelink on these 4 campaigns + all their ad groups
old_c = [r.campaign_asset.resource_name for r in q(f"""SELECT campaign_asset.resource_name, campaign.name FROM campaign_asset
  WHERE campaign_asset.field_type='SITELINK' AND campaign_asset.status != 'REMOVED' AND campaign.name IN ('{names}')""")]
old_ag = [r.ad_group_asset.resource_name for r in q(f"""SELECT ad_group_asset.resource_name, campaign.name FROM ad_group_asset
  WHERE ad_group_asset.field_type='SITELINK' AND ad_group_asset.status != 'REMOVED' AND campaign.name IN ('{names}')""")]
for svc, typ, fn, rns, label in ((cas, "CampaignAssetOperation", "mutate_campaign_assets", old_c, "campaign"),
                                 (agas, "AdGroupAssetOperation", "mutate_ad_group_assets", old_ag, "ad group")):
    ops = []
    for rn in rns:
        op = c.get_type(typ); op.remove = rn; ops.append(op)
    if ops: print(f"unlinked {label}:", len(getattr(svc, fn)(customer_id=CID, operations=ops).results))
time.sleep(2)

# 2) create the assets, ?src=1..N per page
asvc = c.get_service("AssetService"); created = {}
for page, rows in SETS.items():
    ops = []
    for i, (t, d1, d2) in enumerate(rows, 1):
        op = c.get_type("AssetOperation"); a = op.create
        a.sitelink_asset.link_text = t; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
        a.final_urls.append(f"{GO}{page}?src={i}"); ops.append(op)
    created[page] = [r.resource_name for r in asvc.mutate_assets(customer_id=CID, operations=ops).results]
    print(f"go./{page}: created {len(created[page])}")

# 3) link
camp = {r.campaign.name: r.campaign.id for r in q(f"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name IN ('{names}')")}
ops = []
for cname, page in CAMPAIGN_SET.items():
    for arn in created[page]:
        op = c.get_type("CampaignAssetOperation"); l = op.create
        l.campaign = ga.campaign_path(CID, camp[cname]); l.asset = arn
        l.field_type = c.enums.AssetFieldTypeEnum.SITELINK; ops.append(op)
print("campaign links:", len(cas.mutate_campaign_assets(customer_id=CID, operations=ops).results))
ops = []
for r in q("SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.name = 'TSD_Search_HVAC' AND ad_group.status != 'REMOVED'"):
    if r.ad_group.name not in AC_GROUPS: continue
    for arn in created["ac-repair/"]:
        op = c.get_type("AdGroupAssetOperation"); l = op.create
        l.ad_group = ga.ad_group_path(CID, r.ad_group.id); l.asset = arn
        l.field_type = c.enums.AssetFieldTypeEnum.SITELINK; ops.append(op)
print("AC ad group links:", len(agas.mutate_ad_group_assets(customer_id=CID, operations=ops).results))
