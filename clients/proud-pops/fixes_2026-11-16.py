# Proud Pops fu-137 fixes, 2026-11-16 (Edu's go after the re-read). Run from google-ads-ratos/scripts:
#   ./tsd.sh <abs path>            validate-only
#   ./tsd.sh <abs path> --apply    apply + read-back
# One atomic mutate:
# - Electrical 23866999121 budget $455 -> $375 (undo the 11-09 raise: +$80/d bought looser matches, 0 extra leads)
# - Plumbing 23853484024 budget $145 -> $75 (Max Clicks on generic plumber terms, $1,661 / 2 leads since 11-04; LSA carries plumbing)
# - Campaign PHRASE negatives: Electrical mechanic / circuit board / gate opener / independent / cheap;
#   HVAC 23848895678 pops / corporation; Plumbing pops ('pops ac' served on HVAC: 'proud pops' PHRASE doesn't catch it)
# Aborts if budgets/status aren't as expected, if a negative would block a live keyword, or if it would have blocked a converting term.
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "1051843378"
ELEC, PLUMB, HVAC = "23866999121", "23853484024", "23848895678"
BUDGETS = {ELEC: (455.0, 375.0), PLUMB: (145.0, 75.0)}
NEGS = {ELEC: ["mechanic", "circuit board", "gate opener", "independent", "cheap"],
        HVAC: ["pops", "corporation"],
        PLUMB: ["pops"]}
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum


def state():
    camps = {}
    for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.campaign_budget, campaign_budget.amount_micros,
                   campaign_budget.explicitly_shared FROM campaign WHERE campaign.id IN ({ELEC}, {PLUMB}, {HVAC})"""):
        camps[str(r.campaign.id)] = (r.campaign.name, r.campaign.status.name, r.campaign.campaign_budget,
                                     r.campaign_budget.amount_micros / 1e6, r.campaign_budget.explicitly_shared)
    negs = {}
    for r in q(f"""SELECT campaign.id, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
                   WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD' AND campaign.id IN ({ELEC}, {PLUMB}, {HVAC})"""):
        negs.setdefault(str(r.campaign.id), set()).add((r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name))
    return camps, negs


camps, negs = state()
for cid, (name, status, bres, amt, shared) in camps.items():
    print(f"{cid} {name[20:48]:28s} {status} budget ${amt:.2f} shared={shared} negatives={len(negs.get(cid, ()))}")
for cid, (old, new) in BUDGETS.items():
    name, status, bres, amt, shared = camps[cid]
    if status != "ENABLED" or abs(amt - old) > 0.01 or shared:
        sys.exit(f"ABORT: {name} not in the expected state (ENABLED, ${old:.0f}, unshared)")

ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("MutateOperation")
    op.campaign_budget_operation.update.resource_name = camps[cid][2]
    op.campaign_budget_operation.update.amount_micros = int(new * 1e6)
    op.campaign_budget_operation.update_mask.paths.append("amount_micros")
    ops.append(op)

added = []
for cid, words in NEGS.items():
    live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
        AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")]
    hit = [(w, k) for w in words for k in live if f" {w} " in f" {k} "]
    if hit:
        sys.exit(f"ABORT: negative matches a live keyword in {camps[cid][0]}: {hit}")
    for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.all_conversions FROM search_term_view
                   WHERE campaign.id = {cid} AND segments.date BETWEEN '2026-11-02' AND '2026-11-15'"""):
        t = r.search_term_view.search_term.lower()
        m = [w for w in words if f" {w} " in f" {t} "]
        if m and r.metrics.all_conversions > 0:
            sys.exit(f"ABORT: '{m[0]}' would block a converting term in {camps[cid][0]}: {t}")
        if m and r.metrics.clicks:
            print(f"   replay blocks [{camps[cid][0][20:46]}] '{t}' ${r.metrics.cost_micros/1e6:.2f} / {r.metrics.clicks} clk ({m[0]})")
    for w in words:
        if (w, "PHRASE") in negs.get(cid, set()):
            print(f"   already there: {camps[cid][0][20:46]} '{w}'")
            continue
        op = client.get_type("MutateOperation")
        cc = op.campaign_criterion_operation.create
        cc.campaign = ga.campaign_path(CID, cid)
        cc.negative = True
        cc.keyword.text = w
        cc.keyword.match_type = MT.PHRASE
        ops.append(op)
        added.append((cid, w))

req = client.get_type("MutateGoogleAdsRequest")
req.customer_id = CID
req.validate_only = not APPLY
req.mutate_operations.extend(ops)
ga.mutate(request=req)
print(f"{len(ops)} operations ok: Electrical $455 -> $375, Plumbing $145 -> $75, {len(added)} negatives {added}",
      "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    camps, negs = state()
    for cid in (ELEC, PLUMB, HVAC):
        name, status, bres, amt, shared = camps[cid]
        missing = [w for w in NEGS.get(cid, []) if (w, "PHRASE") not in negs.get(cid, set())]
        print(f"read-back: {name[20:48]:28s} {status} budget ${amt:.2f} negatives={len(negs.get(cid, ()))} missing={missing}")
