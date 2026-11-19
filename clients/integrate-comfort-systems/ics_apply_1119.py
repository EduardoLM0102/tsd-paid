# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]
"""Integrate Comfort (4571881760): NonBranded 24047025253, 2026-11-19 (Edu: "apply 1 and 2").
1. Campaign PHRASE negatives: competitor names seen in search terms 11-17..11-19 + AC terms (campaign is heating-only).
2. Pause the 2 old AC RSAs 817245367824 (/ac-repairs/) and 817245367830 (/ac-installations/); heating RSA 831383124121 stays.
Note: AC Repair (197798871825) + AC Installation (197798872025) ad groups are PAUSED; their AC ads never served since. 'ac repair' / 'a c repair' negatives WILL block AC Repair's keywords if it is re-enabled in spring: remove them first.
Rollback: remove the negative criteria (resource names printed on apply); set the 2 ads back to ENABLED.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "4571881760", "24047025253"
AC_ADS = ["817245367824", "817245367830"]
KEEP_AD = "831383124121"
APPLY = "--apply" in sys.argv
VO = not APPLY
NEG_PHRASE = [
    "arctic ac", "arctic air", "delta heating", "dennis terhune", "terhune", "efficient air", "kays affordable", "l&f hvac",
    "ludlow heating", "poust", "rpoust", "sam's air control", "sams air control", "verona heating and cooling", "bi state heating",
    "dj wagner", "dwyer heating", "energy solutions", "hart and iliff",
    "ac repair", "a c repair",
]
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
E = client.enums

existing = {r.campaign_criterion.keyword.text.lower() for r in q(
    f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
negs = [n for n in NEG_PHRASE if n.lower() not in existing]
print(f"existing negs {len(existing)}, adding {len(negs)}: {negs}")
# safety: no new negative may block the live positive keywords
pos = [r.ad_group_criterion.keyword.text.lower() for r in q(
    f"SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'")]
for n in negs:
    hit = [p for p in pos if f" {n} " in f" {p} "]
    if hit: sys.exit(f"ABORT: negative '{n}' would block live keyword(s) {hit}")
ads = {r.ad_group_ad.ad.id: (r.ad_group_ad.resource_name, r.ad_group_ad.status.name, r.ad_group.id) for r in q(
    f"SELECT ad_group_ad.ad.id, ad_group_ad.resource_name, ad_group_ad.status, ad_group.id FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.status != 'REMOVED'")}
print("ads:", {k: v[1:] for k, v in ads.items()})
if ads.get(int(KEEP_AD), (None, None))[1] != "ENABLED": sys.exit("ABORT: heating RSA not ENABLED, pausing AC ads would leave nothing serving")

ops = []
for n in negs:
    op = client.get_type("CampaignCriterionOperation")
    c = op.create; c.campaign = ga.campaign_path(CID, NB); c.negative = True
    c.keyword.text = n; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
    ops.append(op)
if ops:
    r = client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
    print(f"  ok  {len(ops)} negatives", "APPLIED" if APPLY else "(validate_only)", [x.resource_name for x in r.results] if APPLY else "")

aops = []
for a in AC_ADS:
    rn, st, ag = ads[int(a)]
    if st == "PAUSED": continue
    op = client.get_type("AdGroupAdOperation")
    op.update.resource_name = rn; op.update.status = E.AdGroupAdStatusEnum.PAUSED
    op.update_mask.paths.append("status")
    aops.append(op)
if aops:
    client.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CID, "operations": aops, "validate_only": VO})
    print(f"  ok  pause {len(aops)} AC ads", "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    n2 = len([1 for r in q(f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")])
    print("read-back: negatives now", n2)
    for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.status != 'REMOVED'"):
        print("  ad", r.ad_group_ad.ad.id, r.ad_group_ad.status.name)
