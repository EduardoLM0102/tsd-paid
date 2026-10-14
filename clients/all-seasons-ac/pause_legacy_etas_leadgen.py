#!/usr/bin/env python3
"""Pause the 59 legacy Expanded Text Ads still ENABLED in TSD_Search_LeadGen.

Found 2026-08-31 while diagnosing LeadGen's rank-lost IS (62.4%): the campaign
has 59 EXPANDED_TEXT_AD (legacy format, Google stopped allowing new
creation/edits of these in mid-2022) sitting alongside 42
RESPONSIVE_SEARCH_AD in the same ad groups. Every ad group with an ETA also
has at least one EXCELLENT/GOOD-rated RSA already serving, so pausing the ETAs
leaves every ad group with live ads — traffic just shifts fully to the RSAs,
which is the standard Google-recommended move away from ETAs anyway.

NOT touching the 1 EXPANDED_DYNAMIC_SEARCH_AD (ad_id 515097715153,
"HVAC (Lead Gen) - dynamic ad group") — different ad format, not part of this
finding, and it's actually driving real traffic (1022 impr / 30 clicks /
$243.57 over 30 days).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query

CUSTOMER_ID = "4467722415"
CAMPAIGN_ID = "11803942938"  # TSD_Search_LeadGen

AD_GROUP_AD_RESOURCE_NAMES = [
    "customers/4467722415/adGroupAds/121605420144~485103415081",
    "customers/4467722415/adGroupAds/121605420144~485103415084",
    "customers/4467722415/adGroupAds/121605420144~485103415087",
    "customers/4467722415/adGroupAds/115563973635~485160490541",
    "customers/4467722415/adGroupAds/115563973635~485160490544",
    "customers/4467722415/adGroupAds/115563973635~485160490547",
    "customers/4467722415/adGroupAds/115563973675~485160490553",
    "customers/4467722415/adGroupAds/115563973675~485160490556",
    "customers/4467722415/adGroupAds/115563973835~485160490559",
    "customers/4467722415/adGroupAds/115563973835~485160490682",
    "customers/4467722415/adGroupAds/115563973835~485160490685",
    "customers/4467722415/adGroupAds/115563973875~485160490688",
    "customers/4467722415/adGroupAds/115563973875~485160490691",
    "customers/4467722415/adGroupAds/115563973875~485160490694",
    "customers/4467722415/adGroupAds/115563973915~485160490697",
    "customers/4467722415/adGroupAds/115563973915~485160490700",
    "customers/4467722415/adGroupAds/115563973915~485160490703",
    "customers/4467722415/adGroupAds/115563974075~485160490706",
    "customers/4467722415/adGroupAds/115563974075~485160490709",
    "customers/4467722415/adGroupAds/115563974115~485160490715",
    "customers/4467722415/adGroupAds/115563974115~485160490718",
    "customers/4467722415/adGroupAds/115563974115~485160490721",
    "customers/4467722415/adGroupAds/115563974155~485160490724",
    "customers/4467722415/adGroupAds/115563974155~485160490727",
    "customers/4467722415/adGroupAds/115563974155~485160490730",
    "customers/4467722415/adGroupAds/115563974315~485160490733",
    "customers/4467722415/adGroupAds/115563974315~485160490736",
    "customers/4467722415/adGroupAds/115563974315~485160490739",
    "customers/4467722415/adGroupAds/115563974355~485160490742",
    "customers/4467722415/adGroupAds/115563974355~485160490745",
    "customers/4467722415/adGroupAds/115563974355~485160490748",
    "customers/4467722415/adGroupAds/115563974395~485160490754",
    "customers/4467722415/adGroupAds/115563974395~485160490757",
    "customers/4467722415/adGroupAds/115563974395~485160490760",
    "customers/4467722415/adGroupAds/115563974395~485160490763",
    "customers/4467722415/adGroupAds/115563974395~485160490766",
    "customers/4467722415/adGroupAds/115563974555~485160490772",
    "customers/4467722415/adGroupAds/115563974555~485160490778",
    "customers/4467722415/adGroupAds/115563974595~485160490781",
    "customers/4467722415/adGroupAds/115563974595~485160490784",
    "customers/4467722415/adGroupAds/115563974595~485160490787",
    "customers/4467722415/adGroupAds/115563974635~485160490790",
    "customers/4467722415/adGroupAds/115563974635~485160490793",
    "customers/4467722415/adGroupAds/115563974635~485160490796",
    "customers/4467722415/adGroupAds/115563974795~485160490922",
    "customers/4467722415/adGroupAds/115563974795~485160490931",
    "customers/4467722415/adGroupAds/115563974835~485160490934",
    "customers/4467722415/adGroupAds/115563974835~485160490937",
    "customers/4467722415/adGroupAds/115563974835~485160490940",
    "customers/4467722415/adGroupAds/115563974875~485160490943",
    "customers/4467722415/adGroupAds/115563974875~485160490946",
    "customers/4467722415/adGroupAds/115563974875~485160490949",
    "customers/4467722415/adGroupAds/115563975035~485160490952",
    "customers/4467722415/adGroupAds/115563975035~485160490955",
    "customers/4467722415/adGroupAds/115563975035~485160490958",
    "customers/4467722415/adGroupAds/112010777222~485171758259",
    "customers/4467722415/adGroupAds/112010777222~485171758265",
    "customers/4467722415/adGroupAds/115563973915~526761211644",
    "customers/4467722415/adGroupAds/130559857567~545237138328",
]

assert len(AD_GROUP_AD_RESOURCE_NAMES) == 59, f"expected 59, got {len(AD_GROUP_AD_RESOURCE_NAMES)}"

client = init_client()
service = client.get_service("AdGroupAdService")

ops = []
for rn in AD_GROUP_AD_RESOURCE_NAMES:
    op = client.get_type("AdGroupAdOperation")
    aga = op.update
    aga.resource_name = rn
    aga.status = client.enums.AdGroupAdStatusEnum.PAUSED
    op.update_mask.CopyFrom(__import__("google.protobuf.field_mask_pb2", fromlist=["FieldMask"]).FieldMask(paths=["status"]))
    ops.append(op)

response = service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=ops)
print(f"Paused {len(response.results)} ads.")

# Read-back verification.
q = f"""
SELECT ad_group_ad.ad.type, ad_group_ad.status
FROM ad_group_ad
WHERE campaign.id = {CAMPAIGN_ID}
"""
rows = list(run_query(CUSTOMER_ID, q))
counts = {}
for r in rows:
    t = r["ad_group_ad"]["ad"].get("type_", r["ad_group_ad"]["ad"].get("type"))
    s = r["ad_group_ad"]["status"]
    key = (t, s)
    counts[key] = counts.get(key, 0) + 1

print("\nVerified ad type x status counts in LeadGen:")
for (t, s), n in sorted(counts.items()):
    print(f"  {t:30s} {s:10s} {n}")
