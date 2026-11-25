# APPLIED LIVE 2026-11-20 23:27 UTC (Gui via Claude, Edu's go). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]   (validate-only without --apply)
"""Watt's Right (3651667805) NB 'Electrician (General)' RSA 830598421847, 2026-11-20 (Edu: "pode trocar sim").
WR charges extra after hours (AT 76e1df4a, 11-19), so the 2 'no extra fee' lines come out:
  H 'No Extra Fees on Weekends'  -> 'Call Now for Fast Service'
  D 'Nights, weekends and holidays at no extra fee. Call now or request service online.'
    -> 'Available nights, weekends and holidays. Call now or request service online.'
Everything else (pins on the 3 HEADLINE_1 lines, paths, final URL) kept as is. Aborts if the ad text changed.
Rollback: re-run with OLD/NEW swapped."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, AD = "3651667805", "830598421847"
SWAP_H = {"No Extra Fees on Weekends": "Call Now for Fast Service"}
SWAP_D = {"Nights, weekends and holidays at no extra fee. Call now or request service online.":
          "Available nights, weekends and holidays. Call now or request service online."}
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

r = q(f"""SELECT ad_group_ad.ad.resource_name, ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.responsive_search_ad.descriptions FROM ad_group_ad WHERE ad_group_ad.ad.id = {AD}""")[0].ad_group_ad
H = [(h.text, h.pinned_field) for h in r.ad.responsive_search_ad.headlines]
D = [(d.text, d.pinned_field) for d in r.ad.responsive_search_ad.descriptions]
if not all(any(t == o for t, _ in H) for o in SWAP_H) or not all(any(t == o for t, _ in D) for o in SWAP_D):
    sys.exit("ABORT: expected lines not found, ad changed since 11-20")
newH = [(SWAP_H.get(t, t), p) for t, p in H]
newD = [(SWAP_D.get(t, t), p) for t, p in D]
for t, _ in newH: assert len(t) <= 30, t
for t, _ in newD: assert len(t) <= 90, t
if len({t for t, _ in newH}) != len(newH): sys.exit("ABORT: duplicate headline")

op = client.get_type("AdOperation")
op.update.resource_name = r.ad.resource_name
for lst, field in ((newH, op.update.responsive_search_ad.headlines), (newD, op.update.responsive_search_ad.descriptions)):
    for t, p in lst:
        a = client.get_type("AdTextAsset"); a.text = t
        if p: a.pinned_field = p
        field.append(a)
op.update_mask.paths.extend(["responsive_search_ad.headlines", "responsive_search_ad.descriptions"])
client.get_service("AdService").mutate_ads(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print("RSA text", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    a = q(f"""SELECT ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status FROM ad_group_ad WHERE ad_group_ad.ad.id = {AD}""")[0].ad_group_ad
    print("read-back H:", [(h.text, h.pinned_field.name) for h in a.ad.responsive_search_ad.headlines])
    print("read-back D:", [d.text for d in a.ad.responsive_search_ad.descriptions])
    print("status:", a.status.name, a.policy_summary.approval_status.name, a.policy_summary.review_status.name)
