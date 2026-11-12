# APPLIED LIVE 2026-11-11 10:35 BRT (Edu: "Apply 1"), 25 negatives, read-back OK on both campaigns. Re-running adds nothing new.
"""All Seasons AC (4467722415): PHRASE negatives on LeadGen 11803942938 + MiniSplit 24050402045 for the support / thermostat / research
terms that took ~$100 of $173 visible spend 11-04..11-10 (mitsubishi comfort app support $34.71 -> a wrong-company call Google counted
as a conversion; sensi copeland support $20.29; honeywell home thermostat $5.65; cooper hunter mini split reviews $4.47; mini split vs
central air electric bill $3.78). Gui added 'app support', 'hart home', 'lennox' etc. on 11-10 19:39; this adds what his list left out.
Replays each negative against 30d search terms + live keywords in both campaigns and ABORTS on a keyword conflict. Budgets untouched."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "4467722415"
CAMPS = {"11803942938": "LeadGen", "24050402045": "MiniSplit"}
NEG = ["support", "sensi", "copeland", "honeywell", "ecobee", "nest thermostat", "braeburn", "cooper hunter", "vs", "electric bill", "comfort app", "customer service", "phone number", "warranty"]
# Out: 'thermostat' (blocks the live LeadGen keyword 'thermostat air conditioner') and 'reviews' (blocks the brand keywords 'all seasons … reviews').
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

ops = []
for camp, name in CAMPS.items():
    terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = {camp} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
    kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {camp} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"== {name}: {len(kws)} live keywords, {len(existing)} campaign negatives")
    for n in NEG:
        if n in existing: print(f"   '{n}': already there"); continue
        hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
        kc = [k for k in kws if f" {n} " in f" {k} "]
        print(f"   '{n}': blocks {len(hit)} terms ${sum(t.metrics.cost_micros for t in hit)/1e6:.2f} conv {sum(t.metrics.conversions for t in hit):.1f} {[h.search_term_view.search_term for h in hit][:4]}; kw conflicts: {kc}")
        if kc: sys.exit(f"ABORT: '{n}' blocks a live keyword in {name}: {kc}")
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, camp); c.negative = True; c.keyword.text = n; c.keyword.match_type = MT.PHRASE; ops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"negatives ({len(ops)}) ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    for camp, name in CAMPS.items():
        got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"  read-back {name}: missing {[n for n in NEG if n not in got]}")
