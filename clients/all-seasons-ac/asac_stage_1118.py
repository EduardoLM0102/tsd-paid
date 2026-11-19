# Run from google-ads-ratos/scripts: ./tsd.sh <abs path> [--apply]. Validate-only unless --apply. STAGED 2026-11-18 for Edu's go (fu-153).
"""All Seasons AC (4467722415), 2026-11-18 (fu-153 read). Week 11-11..11-17: 85% of visible LeadGen/MiniSplit click spend went to other companies
(nugent and potter $33, islandaire $31, burner man $25, hamptons air $21, airsync $14, strada $9, central air systems $9, b&r plumbing $9, hampton air $6,
seasons air conditioning $5, brian egan $5, midea $3). Branded's BROAD 'all seasons hvac' bought generic terms ($19 of $36: mitsubishi electric heating
and cooling, central air conditioning system, thermostat replacement cost) while the PHRASE brand keywords sit at 78-100% IS for ~$1 a click.
1. LeadGen 11803942938 + MiniSplit 24050402045: PHRASE negatives (other companies + impression-only leaks). 'hamptons air' as EXACT only (Gui 11-16: phrase
   would block 'hamptons' area searches); 'hampton air' PHRASE is safe (singular, a company name).
2. LeadGen: pause the BROAD keyword 'hvac & plumbing' (brought nugent and potter; open since 11-09).
3. Branded 24202454875: pause every BROAD keyword, keep PHRASE. Target IS / $5 cap / $5 budget untouched.
Rollback: remove the negatives; re-enable the printed keywords."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, LG, MS, BR = "4467722415", "11803942938", "24050402045", "24202454875"
NEG_PHRASE = ["nugent and potter", "islandaire", "burner man", "airsync", "seasons air conditioning", "strada hvac", "central air systems", "b&r plumbing",
              "hampton air", "brian egan", "midea", "hydronic supply", "systematic control", "airz", "blue sky hvac", "bem corp", "suburban gas", "petro home"]
NEG_EXACT = ["hamptons air"]
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
req = {"customer_id": CID, "validate_only": vo}

# 1. negatives, skipping ones already there
neg_ops = []
for camp, name in ((LG, "LeadGen"), (MS, "MiniSplit")):
    have = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""SELECT campaign_criterion.keyword.text,
        campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {camp}
        AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")]
    # brand keywords left ENABLED inside PAUSED ad groups are moot (and 'all seasons' PHRASE is already a negative here)
    todo = [(n, "PHRASE") for n in NEG_PHRASE if (n, "PHRASE") not in have] + [(n, "EXACT") for n in NEG_EXACT if (n, "EXACT") not in have]
    block = [(n, k) for n, _ in todo for k in live if f" {n} " in f" {k} "]
    if block: sys.exit(f"ABORT {name}: negative would block a live keyword: {block}")
    print(f"1. {name}: {len(have)} negatives now, adding {len(todo)}: {[n for n, _ in todo]}")
    for n, mt in todo:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, camp); c.negative = True; c.keyword.text = n; c.keyword.match_type = getattr(MT, mt); neg_ops.append(op)

# 2. LeadGen BROAD 'hvac & plumbing'
kw_ops = []
rows = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group.name FROM ad_group_criterion
    WHERE campaign.id = {LG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'
    AND ad_group_criterion.keyword.match_type = 'BROAD'""")
hp = [r for r in rows if "plumbing" in r.ad_group_criterion.keyword.text.lower()]
print(f"2. LeadGen BROAD keywords enabled: {len(rows)}; pausing: {[(r.ad_group_criterion.keyword.text, r.ad_group.name) for r in hp]}")
for r in hp:
    op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = r.ad_group_criterion.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status"); kw_ops.append(op)

# 3. Branded BROAD -> paused, PHRASE stays
rows = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion
    WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")
broad = [r for r in rows if r.ad_group_criterion.keyword.match_type.name == "BROAD"]
phrase = [r for r in rows if r.ad_group_criterion.keyword.match_type.name != "BROAD"]
if not phrase: sys.exit("ABORT: Branded would keep no keyword")
print(f"3. Branded: pause {len(broad)} BROAD {[r.ad_group_criterion.keyword.text for r in broad]}; keep {len(phrase)} {[r.ad_group_criterion.keyword.text + ' [' + r.ad_group_criterion.keyword.match_type.name[0] + ']' for r in phrase]}")
for r in broad:
    op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = r.ad_group_criterion.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status"); kw_ops.append(op)

tag = "(validate_only)" if vo else "APPLIED"
if neg_ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={**req, "operations": neg_ops}); print(f"   negatives ok ({len(neg_ops)})", tag)
if kw_ops: client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={**req, "operations": kw_ops}); print(f"   keyword pauses ok ({len(kw_ops)})", tag)
if APPLY:
    for camp, name in ((LG, "LeadGen"), (MS, "MiniSplit")):
        got = {r.campaign_criterion.keyword.text.lower() for r in q(f"SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {camp} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
        print(f"read-back {name}: all present={all(n in got for n in NEG_PHRASE + NEG_EXACT)}")
    left = q(f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'")
    print("read-back Branded enabled:", [f"{r.ad_group_criterion.keyword.text} [{r.ad_group_criterion.keyword.match_type.name[0]}]" for r in left])
