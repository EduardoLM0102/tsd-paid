#!/usr/bin/env python3
"""Strip 23 wrong location targets from TSD_Search_LeadGen, leaving only the
same 3 locations every other correctly-targeted campaign in the account uses.

Found 2026-08-31: LeadGen was targeting the account's real service area
(Suffolk County, West Babylon, Nassau County — Long Island NY) PLUS 22
Spanish-speaking-country targets (Argentina, Mexico, Colombia, Peru,
Venezuela, Puerto Rico, Guatemala, Honduras, Nicaragua, Panama, Paraguay,
Uruguay, Bolivia, Chile, Costa Rica, Dominican Republic, Ecuador, El Salvador,
Andorra, Gibraltar, Equatorial Guinea) PLUS Queens — none of which appear on
any other campaign in the account (PMax, Mitsubishi-Brand, and
MiniSplit-General all target exactly Suffolk County + West Babylon + Nassau
County). Likely explains LeadGen's outlier 62.4% rank-lost IS and its
disproportionately expensive Click-to-call CPL.

Removes the 23 wrong criteria, leaves the 3 correct ones (1023413, 1023474,
9058760) untouched.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query

CUSTOMER_ID = "4467722415"
CAMPAIGN_ID = "11803942938"  # TSD_Search_LeadGen

# geo_target_constant id -> name, for the criteria being removed
REMOVE_IDS = {
    2020: "Andorra", 2032: "Argentina", 2068: "Bolivia", 2084: "Belize",
    2152: "Chile", 2170: "Colombia", 2188: "Costa Rica",
    2214: "Dominican Republic", 2218: "Ecuador", 2222: "El Salvador",
    2226: "Equatorial Guinea", 2292: "Gibraltar", 2320: "Guatemala",
    2340: "Honduras", 2484: "Mexico", 2558: "Nicaragua", 2591: "Panama",
    2600: "Paraguay", 2604: "Peru", 2630: "Puerto Rico", 2858: "Uruguay",
    2862: "Venezuela", 9067608: "Queens",
}
KEEP_IDS = {1023413: "Suffolk County", 1023474: "West Babylon", 9058760: "Nassau County"}

client = init_client()
gads_service = client.get_service("GoogleAdsService")
criterion_service = client.get_service("CampaignCriterionService")

ops = []
for geo_id in REMOVE_IDS:
    op = client.get_type("CampaignCriterionOperation")
    op.remove = gads_service.campaign_criterion_path(CUSTOMER_ID, CAMPAIGN_ID, geo_id)
    ops.append(op)

response = criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
print(f"Removed {len(response.results)} location criteria from LeadGen:")
for r in response.results:
    print(" ", r.resource_name)

# Read-back verification.
q = f"""
SELECT campaign.name, campaign_criterion.location.geo_target_constant
FROM campaign_criterion
WHERE campaign_criterion.type = 'LOCATION' AND campaign.id = {CAMPAIGN_ID}
"""
rows = list(run_query(CUSTOMER_ID, q))
print(f"\nVerified: {len(rows)} location criteria remain on LeadGen:")
for r in rows:
    geo = r["campaign_criterion"]["location"]["geo_target_constant"]
    geo_id = int(geo.split("/")[-1])
    label = KEEP_IDS.get(geo_id, f"UNEXPECTED id {geo_id}")
    print(f"  {geo} ({label})")
