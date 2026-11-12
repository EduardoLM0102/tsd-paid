# APPLIED LIVE 2026-10-28 on Edu's go. Do NOT re-run with --apply (guards abort anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), Edu 10-28: "Would you apply the UTMs for me?" (Jared's 10-19 UTM ask, AT 3a267fb1 point 7).
1. Nonbranded 23805382277: had NO tracking template and NO final URL suffix -> set campaign final URL suffix with UTMs.
2. PMax 21291552209: tracking template '{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign=Pmax+Windows+Siding'
   (stale 'Windows' label, breaks if a final URL ever carries '?') -> clear template, same UTMs via final URL suffix.
Auto-tagging (gclid) stays on. Branded (paused) left as is. No budget/bidding change.
Aborts on unexpected state.
"""
import sys
sys.path.insert(0, ".")
from google.protobuf.field_mask_pb2 import FieldMask
from lib import init_client

CID, NB, PMAX = "2198608170", "23805382277", "21291552209"
OLD_PMAX_TPL = "{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign=Pmax+Windows+Siding"
SUFFIX = {
    NB: "utm_source=google&utm_medium=cpc&utm_campaign=search_nonbranded&utm_content={adgroupid}&utm_term={keyword}",
    PMAX: "utm_source=google&utm_medium=cpc&utm_campaign=pmax_siding",
}
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
svc = client.get_service("CampaignService")


def state():
    rows = ga.search(customer_id=CID, query=f"""SELECT campaign.id, campaign.name, campaign.tracking_url_template, campaign.final_url_suffix
        FROM campaign WHERE campaign.id IN ({NB}, {PMAX})""")
    return {str(r.campaign.id): (r.campaign.name, r.campaign.tracking_url_template, r.campaign.final_url_suffix) for r in rows}


s = state()
for cid, (n, tpl, suf) in s.items():
    print(f"BEFORE {cid} {n}: template={tpl!r} suffix={suf!r}")
if s[NB][1] or s[NB][2]:
    sys.exit("ABORT: Nonbranded already has a template or suffix")
if s[PMAX][1] != OLD_PMAX_TPL or s[PMAX][2]:
    sys.exit("ABORT: PMax template/suffix not as expected")

ops = []
for cid in (NB, PMAX):
    op = client.get_type("CampaignOperation")
    c = op.update
    c.resource_name = svc.campaign_path(CID, cid)
    c.final_url_suffix = SUFFIX[cid]
    paths = ["final_url_suffix"]
    if cid == PMAX:
        paths.append("tracking_url_template")  # in mask but unset = cleared (setting "" errors "Too short")
    op.update_mask.CopyFrom(FieldMask(paths=paths))
    ops.append(op)

req = client.get_type("MutateCampaignsRequest")
req.customer_id = CID
req.operations.extend(ops)
req.validate_only = not APPLY
svc.mutate_campaigns(request=req)
print("APPLIED" if APPLY else "VALIDATED (validate-only, nothing changed)")

if APPLY:
    for cid, (n, tpl, suf) in state().items():
        print(f"AFTER {cid} {n}: template={tpl!r} suffix={suf!r}")
