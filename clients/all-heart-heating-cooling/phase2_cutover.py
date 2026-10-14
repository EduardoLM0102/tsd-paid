"""All Heart — Phase 2 CUTOVER (run at flip time, ~48h after the 2026-07-10 tCPA ramp reads clean).

Flips the staged (PAUSED) themed ad groups + brand campaign live, retires the old mega ad group,
and routes brand queries to the new brand campaign. Reversible (see REVERT at bottom of the log entry).

Run:  ./tsd.sh ../../../clients/all-heart-heating-cooling/phase2_cutover.py     (or via GADS_ENV_PATH)
Dry run first:  set DRY_RUN=True
"""
import os
import sys, json
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client, run_query

DRY_RUN = False   # executed 2026-07-13 (after phase2_kw_patch.py)

CID="9205826499"
NONBRAND_CAMP="23685938569"
OLD_ADGROUP="193307267686"           # "All Hearth Plumbing - NonBranded" (mega, mixed) -> PAUSE
BRAND_CAMP="24016694610"
BRAND_ADGROUP="198469690939"
NEW_ADGROUPS=["199017381820","203964394691","196979638774","198469621179","198469621619"]  # AC Repair/Heating/AC Install/HVAC Svc/Plumbing

# brand terms to negate in the NonBranded campaign so they route to the brand campaign
BRAND_NEGATIVES=["all heart heating and cooling","all heart heating","all heart heating & cooling",
 "all heart heating cooling & plumbing","all heart plumbing","all heart hvac","all heart cooling",
 "all heart ac & heating","all heart ac and heating","all heart ac repair","all heart ac installation",
 "all heart air conditioning","all heart palmdale","all heart lancaster","all heart santa clarita",
 "callallheart.com","all heart"]

client=init_client()
agc=client.get_service("AdGroupService")
adsvc=client.get_service("AdGroupAdService")
campsvc=client.get_service("CampaignService")
ccsvc=client.get_service("CampaignCriterionService")
ga=client.get_service("GoogleAdsService")

def set_adgroup(agid, status):
    op=client.get_type("AdGroupOperation"); u=op.update
    u.resource_name=ga.ad_group_path(CID,agid)
    u.status=getattr(client.enums.AdGroupStatusEnum,status)
    op.update_mask.paths.append("status")
    if not DRY_RUN: agc.mutate_ad_groups(customer_id=CID,operations=[op])
    print(f"  ad_group {agid} -> {status}")

def enable_ads_in(agid):
    ads=run_query(CID,f"SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.id={agid}")
    for a in ads:
        aid=a["ad_group_ad"]["ad"]["id"]
        op=client.get_type("AdGroupAdOperation"); u=op.update
        u.resource_name=f"customers/{CID}/adGroupAds/{agid}~{aid}"
        u.status=client.enums.AdGroupAdStatusEnum.ENABLED
        op.update_mask.paths.append("status")
        if not DRY_RUN: adsvc.mutate_ad_group_ads(customer_id=CID,operations=[op])
        print(f"    ad {aid} -> ENABLED")

def set_campaign(cid,status):
    op=client.get_type("CampaignOperation"); u=op.update
    u.resource_name=ga.campaign_path(CID,cid)
    u.status=getattr(client.enums.CampaignStatusEnum,status)
    op.update_mask.paths.append("status")
    if not DRY_RUN: campsvc.mutate_campaigns(customer_id=CID,operations=[op])
    print(f"  campaign {cid} -> {status}")

print(("DRY RUN — " if DRY_RUN else "EXECUTING — ")+"Phase 2 cutover")
print("1) Activate 5 themed ad groups + their RSAs:")
for agid in NEW_ADGROUPS:
    set_adgroup(agid,"ENABLED"); enable_ads_in(agid)
print("2) Pause old mega ad group:")
set_adgroup(OLD_ADGROUP,"PAUSED")
print("3) Activate brand campaign + ad group + RSA:")
set_campaign(BRAND_CAMP,"ENABLED"); set_adgroup(BRAND_ADGROUP,"ENABLED"); enable_ads_in(BRAND_ADGROUP)
print("4) Add brand EXACT negatives to NonBranded campaign (route brand -> brand campaign):")
ops=[]
for t in BRAND_NEGATIVES:
    op=client.get_type("CampaignCriterionOperation"); c=op.create
    c.campaign=ga.campaign_path(CID,NONBRAND_CAMP)
    c.negative=True
    c.keyword.text=t
    c.keyword.match_type=client.enums.KeywordMatchTypeEnum.EXACT
    ops.append(op)
if not DRY_RUN: ccsvc.mutate_campaign_criteria(customer_id=CID,operations=ops)
print(f"  {len(ops)} brand negatives added to {NONBRAND_CAMP}")
print("DONE." + ("  (dry run — nothing changed)" if DRY_RUN else ""))
