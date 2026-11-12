"""Neon Monkey 2026-10-20 — Angela (Slack DM): "please add The Tree Place as a negative keyword".
90d: 'the tree place' / 'the tree place in fort worth' = 3 clicks, $80.56 on NB Trimming.
Adds PHRASE negatives 'tree place' + 'treeplace' at campaign level on the 3 ENABLED campaigns.
Usage: ./tsd.sh nm_neg_treeplace_1020.py  (validate_only)  |  --apply
"""
import sys; sys.path.insert(0, ".")
from lib import init_client
CID="7953905280"; APPLY="--apply" in sys.argv
CAMPS={"23825900343":"NB Trimming","21225221220":"PMax Evergreen","23739724064":"Branded Mix"}
c=init_client(); svc=c.get_service("CampaignCriterionService"); ops=[]
for camp in CAMPS:
    for kw in ["tree place","treeplace"]:
        op=c.get_type("CampaignCriterionOperation"); cr=op.create
        cr.campaign=c.get_service("CampaignService").campaign_path(CID,camp)
        cr.negative=True; cr.keyword.text=kw; cr.keyword.match_type=c.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
req=c.get_type("MutateCampaignCriteriaRequest"); req.customer_id=CID; req.operations.extend(ops)
req.validate_only=not APPLY; req.partial_failure=True
res=svc.mutate_campaign_criteria(request=req)
print("APPLIED" if APPLY else "VALIDATED", len(ops), "ops")
if res.partial_failure_error.message: print("partial failure:", res.partial_failure_error.message)
for r in res.results: print(r.resource_name)
