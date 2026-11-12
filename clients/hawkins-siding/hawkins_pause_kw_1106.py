# APPLIED LIVE 2026-11-06, read-back confirmed (8 NB keywords live, house exterior siding paused). Do NOT re-run with --apply.
# Edu's go 2026-11-06 ("Apply the recommendations"), from the fu-103 watch.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins (2198608170) Nonbranded: pause PHRASE 'house exterior siding' (Siding Replacement). 11-03..11-06 it took $198 of $266 NB keyword spend,
34 clicks, 0 leads, on research/product terms. NB keeps running on service keywords only. Budget $67 / Max Clicks $12 unchanged."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "2198608170"
KW = "house exterior siding"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
def live():
    return q("""SELECT campaign.id, campaign.name, ad_group.name, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
        FROM ad_group_criterion WHERE campaign.name LIKE '%Nonbranded%' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
        AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND campaign.status = 'ENABLED'""")
rows = live()
for r in rows: print(" live:", r.ad_group.name, "|", r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name)
hit = [r for r in rows if r.ad_group_criterion.keyword.text.lower() == KW and r.ad_group_criterion.keyword.match_type.name == "PHRASE"]
if len(hit) != 1: sys.exit(f"ABORT: expected 1 live PHRASE '{KW}', found {len(hit)}")
if len(rows) < 2: sys.exit("ABORT: pausing it would leave NB with no live keyword")
r = hit[0]
op = client.get_type("AdGroupCriterionOperation")
op.update.resource_name = r.ad_group_criterion.resource_name
op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"pause '{KW}' in {r.ad_group.name}", "APPLIED" if APPLY else "ok (validate_only)")
if APPLY:
    after = live()
    print("read-back: live NB keywords now", len(after), [x.ad_group_criterion.keyword.text for x in after])
    print("still live?", any(x.ad_group_criterion.keyword.text.lower() == KW for x in after))
