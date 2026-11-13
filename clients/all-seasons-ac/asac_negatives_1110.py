# APPLIED LIVE 2026-11-10 (22 negatives, all created). Do NOT re-run with --live.
"""2026-11-10 (Gui's go on the 11-09 staged list): competitor/junk PHRASE negatives on All Seasons AC (4467722415).
LeadGen 11803942938 + MiniSplit 24050402045. Skips any text already a campaign negative there.
Not copied: the whole LeadGen list (8,751) -> it holds 'mitsubishi', 'mini split', 'air conditioning', 'ac' etc.
that would kill MiniSplit; Edu's curated 10-16/10-22 lists are already on MiniSplit. Only competitor names that
actually bought clicks on MiniSplit in the last 90d are copied.
'lennox' only on MiniSplit (Mitsubishi co-op): on LeadGen it would block Lennox repair searches; 'lennox farmingdale'
is already a LeadGen negative.
Run from the skill scripts dir:  ./tsd.sh /abs/path/asac_negatives_1110.py          (validate only)
                                 ./tsd.sh /abs/path/asac_negatives_1110.py --live   (apply)
"""
import sys
sys.path.insert(0, ".")
from lib import run_query, init_client

CID = "4467722415"
LG, MS = "11803942938", "24050402045"
LIVE = "--live" in sys.argv

BOTH = ["hart home", "kool point", "dole fuel", "app support", "residential insulation", "flynnaire"]
MS_ONLY = ["lennox", "universe home services", "flynn aire", "mac heating", "dix hills air conditioning",
           "quality air care", "innovation air conditioning", "hardy plumbing", "pc richards", "all service heating"]
PLAN = {LG: BOTH, MS: BOTH + MS_ONLY}

existing = {LG: set(), MS: set()}
for r in run_query(CID, f"""SELECT campaign.id, campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD' AND campaign.id IN ({LG}, {MS})"""):
    existing[str(r["campaign"]["id"])].add(r["campaign_criterion"]["keyword"]["text"].lower())

client = init_client()
svc = client.get_service("CampaignCriterionService")
ga = client.get_service("GoogleAdsService")
ops, labels = [], []
for camp, words in PLAN.items():
    for w in words:
        if w in existing[camp]:
            print(f"skip (exists) {camp} '{w}'")
            continue
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = ga.campaign_path(CID, camp)
        c.negative = True
        c.keyword.text = w
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
        labels.append((camp, w))

print(f"{len(ops)} negatives to add, live={LIVE}")
req = client.get_type("MutateCampaignCriteriaRequest")
req.customer_id = CID
req.operations.extend(ops)
req.validate_only = not LIVE
resp = svc.mutate_campaign_criteria(request=req)
if LIVE:
    for (camp, w), res in zip(labels, resp.results):
        print("added", camp, w, res.resource_name)
else:
    print("validate_only OK")
