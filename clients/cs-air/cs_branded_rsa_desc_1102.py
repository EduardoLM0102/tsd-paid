# APPLIED LIVE 2026-11-02 on Edu's go. Do NOT re-run with --apply (aborts: descriptions already changed).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""C&S Air (5563867754) Branded RSA 800192030388 (TSD_03.13_Search_Branded_Evergreen): replace 3 weak descriptions.
Edu 11-02: "Yes, go for it". Headlines untouched; 'Call our HVAC experts to set an appointment' kept.
Claims only from C&S's heating pages / the other Branded ad (all makes and models, upfront pricing, family-owned, 20+ years,
licensed and insured). Aborts if the current descriptions aren't the expected ones."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, AD = "5563867754", "800192030388"
KEEP = "Call our HVAC experts to set an appointment"
OLD = {"1 Trusted Heating and AC Experts Mansfield, TX | C&S Air",
       "Reliable HVAC services in Mansfield, TX. Expert AC repair and maintenance. Call us today!",
       "Trust the experts at C&S Air Inc. for all your heating and cooling needs. 20+ years of exp"}
NEW = ["Heating and AC repair, maintenance and installs in Mansfield and DFW. Call C&S Air.",
       "Furnace acting up? Our techs fix all makes and models. Upfront pricing, no surprises.",
       "Family-owned and serving Mansfield for over 20 years. Licensed and insured HVAC team.",
       KEEP]
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

r = q(f"""SELECT ad_group_ad.ad.resource_name, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.status
    FROM ad_group_ad WHERE ad_group_ad.ad.id = {AD}""")[0].ad_group_ad
cur = [d.text.strip() for d in r.ad.responsive_search_ad.descriptions]
print("current:", cur)
if set(cur) != OLD | {KEEP} or any(d.pinned_field for d in r.ad.responsive_search_ad.descriptions):
    sys.exit("ABORT: descriptions changed or pinned, check first")
for t in NEW: assert len(t) <= 90, t

op = client.get_type("AdOperation")
op.update.resource_name = r.ad.resource_name
for t in NEW:
    a = client.get_type("AdTextAsset"); a.text = t; op.update.responsive_search_ad.descriptions.append(a)
op.update_mask.paths.append("responsive_search_ad.descriptions")
client.get_service("AdService").mutate_ads(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("descriptions", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    a = q(f"""SELECT ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status FROM ad_group_ad WHERE ad_group_ad.ad.id = {AD}""")[0].ad_group_ad
    print("read-back:", [d.text for d in a.ad.responsive_search_ad.descriptions], "| headlines", len(a.ad.responsive_search_ad.headlines),
          "|", a.status.name, a.policy_summary.approval_status.name, a.policy_summary.review_status.name)
