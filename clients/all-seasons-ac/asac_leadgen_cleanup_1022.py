# APPLIED LIVE 2026-10-22 on Edu's OK. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC PPC (4467722415), 2026-10-22, Edu's OK ("you have my ok for 1 and 2").
1. LeadGen (11803942938) cleanup: of 979 enabled keywords, 880 had 0 impressions 07-24..10-21 (snapshot in
   leadgen_keywords_90d_2026-10-22.json). PAUSE every 0-impression keyword except own-brand ('all season'), plus
   impression-only competitor / junk names. Every keyword with a click in 90d stays.
2. Nonbranded (23813282398): PAUSE '4 seasons heating and air', 'one hour heating and air conditioning' ($0, competitors).
3. Add the 9 PHRASE negatives skipped on 10-22 because those keywords were live.
Pause only (reversible). Guards: never pauses a keyword with clicks; aborts if a negative still hits a live keyword.
"""
import sys, json, os
sys.path.insert(0, ".")
from lib import init_client

CID, LEADGEN, NB = "4467722415", "11803942938", "23813282398"
SNAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leadgen_keywords_90d_2026-10-22.json")
JUNK = {"cousins air", "ads air conditioning", "jc plumbing and heating", "prestigeair", "reliance air", "twin air holtsville",
        "american cool air", "tosot usa", "a c plus", "nyc free air conditioner", "proactive ac", "s w anderson hvac",
        "jaco mechanical", "galletair", "s w anderson farmingdale", "intercounty mechanical", "dls mechanical corp",
        "ade freeport", "shore mechanical corp", "ac repair fl", "hampton air", "air filter unit",
        "ac compressor air compressor", "air compressor hvac"}
NB_PAUSE = {"4 seasons heating and air", "one hour heating and air conditioning"}
NEG = {LEADGEN: ["american cool air", "apple air", "arista", "twin air", "manual", "troubleshooting", "remote"],
       NB: ["4 seasons", "one hour heating"]}
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
ST = client.enums.AdGroupCriterionStatusEnum
MT = client.enums.KeywordMatchTypeEnum

snap = json.load(open(SNAP))
pause = set()
for o in snap:
    t = o["text"].lower()
    if o["clk"] > 0: continue
    if o["impr"] == 0 and "all season" not in t: pause.add(o["rn"])
    elif t in JUNK: pause.add(o["rn"])
live = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, campaign.id FROM ad_group_criterion
    WHERE campaign.id IN ({LEADGEN},{NB}) AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'
    AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE""")
live_rn = {r.ad_group_criterion.resource_name for r in live}
pause &= live_rn  # only still-enabled ones
for r in live:
    if str(r.campaign.id) == NB and r.ad_group_criterion.keyword.text.lower() in NB_PAUSE: pause.add(r.ad_group_criterion.resource_name)
clicked = {o["rn"] for o in snap if o["clk"] > 0}
assert not (pause & clicked), "ABORT: would pause a clicked keyword"
remaining = {}
for r in live:
    if r.ad_group_criterion.resource_name not in pause:
        remaining.setdefault(str(r.campaign.id), []).append(r.ad_group_criterion.keyword.text.lower())
print(f"pausing {len(pause)} keywords; LeadGen keeps {len(remaining.get(LEADGEN, []))}, NB keeps {len(remaining.get(NB, []))}")
conf = [(n, k) for cid, ns in NEG.items() for n in ns for k in remaining.get(cid, []) if f" {n} " in f" {k} "]
if conf: sys.exit(f"ABORT: negatives still hit live keywords: {conf}")

ops = []
for rn in sorted(pause):
    op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = rn; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
svc = client.get_service("AdGroupCriterionService")
for i in range(0, len(ops), 1000):
    svc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops[i:i+1000], "validate_only": vo})
print(f"{len(ops)} keyword pauses", "(validate_only OK)" if vo else "APPLIED")
nops = []
for cid, ns in NEG.items():
    for t in ns:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, cid); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; nops.append(op)
client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": nops, "validate_only": vo})
print(f"{len(nops)} negatives", "(validate_only OK)" if vo else "APPLIED")
if APPLY:
    st = {r.ad_group_criterion.resource_name: r.ad_group_criterion.status.name for r in q(f"""SELECT ad_group_criterion.resource_name,
        ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id IN ({LEADGEN},{NB}) AND ad_group_criterion.type = 'KEYWORD'""")}
    print("   read-back paused:", sum(1 for rn in pause if st.get(rn) == "PAUSED"), "of", len(pause))
    for cid, ns in NEG.items():
        got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"   read-back negatives {cid}: missing {[n for n in ns if n not in got]}")
    for r in q(f"SELECT campaign.name, campaign.primary_status FROM campaign WHERE campaign.id IN ({LEADGEN},{NB})"):
        print(f"   {r.campaign.name}: {r.campaign.primary_status.name}")
