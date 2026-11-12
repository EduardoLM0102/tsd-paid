# APPLIED LIVE 2026-11-09 on Edu's go (read-back OK: HVAC negatives 55 -> 64). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]   (validate-only without --apply)
"""Cool Hand (9865206319), Edu 11-09: "Work on the cleanup please".
TSD_Search_HVAC 24118511502 (Max Clicks $8 cap, $36/d): 0 leads since 10-30, $323 / 43 clicks 10-31..11-09.
Campaign PHRASE negatives for price research (people pricing a replacement, not a broken AC) + 1 competitor seen 3x.
Left out on purpose: 'afford' / 'financing' / 'quote' / 'estimate' (each converted at least once),
'mini split' (open question to the client: do they install them?), 'hvac near me' (core intent, just expensive).
Aborts on unexpected state, a negative hitting a live keyword, or a negative blocking any term that ever converted."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, H = "9865206319", "24118511502"
PHRASE = ["cost", "costs", "price", "prices", "pricing", "average", "how much", "4 ton", "temperaturepro"]
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

c = q(f"SELECT campaign.name, campaign.status, campaign.bidding_strategy_type FROM campaign WHERE campaign.id = {H}")[0]
print(f"{c.campaign.name} {c.campaign.status.name} {c.campaign.bidding_strategy_type.name}")
if c.campaign.name != "TSD_Search_HVAC" or c.campaign.status.name != "ENABLED":
    sys.exit("ABORT: campaign not in the expected state")

negs = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""
    SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
    WHERE campaign.id = {H} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {H} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
    AND ad_group_criterion.status = 'ENABLED'""")]
hit = [(n, k) for n in PHRASE for k in live if f" {n} " in f" {k} "]
if hit: sys.exit(f"ABORT: negative matches a live keyword {hit}")

agg = {}
for r in q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.all_conversions
    FROM search_term_view WHERE campaign.id = {H} AND segments.date BETWEEN '2026-08-10' AND '2026-11-09'"""):
    a = agg.setdefault(r.search_term_view.search_term.lower(), [0, 0, 0])
    a[0] += r.metrics.cost_micros / 1e6; a[1] += r.metrics.clicks; a[2] += r.metrics.all_conversions
n = cost = 0
for t, (co, cl, cv) in sorted(agg.items(), key=lambda x: -x[1][0]):
    m = [w for w in PHRASE if f" {w} " in f" {t} "]
    if not m: continue
    if cv > 0: sys.exit(f"ABORT: '{m[0]}' would block a term that converted: {t}")
    n += 1; cost += co
    if cl: print(f"   blocks '{t}' ${co:.2f} {cl}clk ({m[0]})")
print(f"replay since 08-10: {n} terms, ${cost:.2f}, none converted")

new = [t for t in PHRASE if (t, "PHRASE") not in negs]
ops = []
for t in new:
    op = client.get_type("CampaignCriterionOperation"); cc = op.create
    cc.campaign = ga.campaign_path(CID, H); cc.negative = True
    cc.keyword.text = t; cc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append(op)
svc = client.get_service("CampaignCriterionService")
req = client.get_type("MutateCampaignCriteriaRequest")
req.customer_id = CID; req.operations.extend(ops); req.validate_only = not APPLY
svc.mutate_campaign_criteria(request=req)
print(f"{len(ops)} negatives ok", "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    after = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {H} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"read-back: negatives {len(negs)} -> {len(after)}, missing {[t for t in PHRASE if t not in after]}")
