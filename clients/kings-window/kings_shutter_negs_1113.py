# APPLIED LIVE 2026-11-13 (Edu: "let's work on the negatives"), 4 negatives, read-back OK on both campaigns. Re-running adds nothing new.
"""King's Window Services (6769493219): PHRASE negatives 'shutter' + 'shutters' on the live Search campaigns (Nonbranded 28.04 + Branded 03.16),
per Lee's request (AT Client Request cf56717b, 2026-11-12). Safety check 2026-05-01..11-12: 6 shutter search terms, 1 click, $0.09, 0 conv;
no live keyword contains 'shutter'; none of the 120 converting terms do. Replays each negative against 180d search terms + live keywords and
ABORTS on a keyword conflict. Budgets untouched. Run: ./tsd.sh <abs path> [--apply]"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "6769493219"
NEG = ["shutter", "shutters"]
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

camps = {str(r.campaign.id): r.campaign.name for r in q("""SELECT campaign.id, campaign.name FROM campaign
    WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'""")}
print("live Search campaigns:", camps)
assert len(camps) == 2, "expected exactly Nonbranded + Branded live"
ops = []
for camp, name in camps.items():
    terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = {camp} AND segments.date BETWEEN '2026-05-17' AND '2026-11-12' AND metrics.impressions > 0""")
    kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {camp} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"== {name}: {len(kws)} live keywords, {len(existing)} campaign negatives")
    for n in NEG:
        if n in existing: print(f"   '{n}': already there"); continue
        hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
        kc = [k for k in kws if f" {n} " in f" {k} "]
        print(f"   '{n}': blocks {len(hit)} terms ${sum(t.metrics.cost_micros for t in hit)/1e6:.2f} conv {sum(t.metrics.conversions for t in hit):.1f} {[h.search_term_view.search_term for h in hit][:6]}; kw conflicts: {kc}")
        if kc: sys.exit(f"ABORT: '{n}' blocks a live keyword in {name}: {kc}")
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, camp); c.negative = True; c.keyword.text = n; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"negatives ({len(ops)}) ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    for camp, name in camps.items():
        got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"  read-back {name}: missing {[n for n in NEG if n not in got]}")
