# APPLIED LIVE 2026-10-22 on Edu's go. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC PPC (4467722415), 2026-10-22, Edu: "apply the negatives".
Post-10-16 search terms (10-17..10-21) still showed ~38% of spend on other companies (pretro, cool solutions bethpage,
airborne, senville...) plus ~200 zero-cost competitor impressions, all via BROAD keywords. Adds PHRASE negatives on the
3 enabled Search campaigns, skipping ones already present. Town names and generic phrases left out on purpose.
Guards: aborts if a negative conflicts with an active keyword; prints 30d terms/conv each negative would have blocked.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "4467722415"
CAMPS = ["11803942938", "23813282398", "24050402045"]  # LeadGen, Nonbranded, MiniSplit-General
NEG = [
 # misspellings of Petro + the paid hits
 "pretro", "peteo", "petrooil", "cool solutions", "airborne heating", "mr mechanical", "alure", "senville",
 # other Long Island / NY companies
 "4 seasons", "a1 heating", "a1 hvac", "a1 cooling", "aaron air", "abbey air", "able air", "able heating", "above all air",
 "absolute air", "absolute hvac", "accool", "accu temp", "accutemp", "accurate cooling", "action air", "air design",
 "air max", "air tech heating", "airtech", "aire tech", "all about air", "all island plumbing", "all points plumbing",
 "all season climate", "all weather", "alpha omega", "alpine plumbing", "always on energy", "american cool air", "amran",
 "apple air", "apple heating", "arc heating", "arista", "arrow heating", "atlantic air", "atlantic a c", "b&s heating",
 "baker air", "baker cooling", "bbo construction", "ben dinkin", "blaka", "bosch brothers", "bowman's", "bowmans",
 "brighton installation", "c & a mechanical", "c&h heating", "cam energy", "carefree", "chivalry", "christensen",
 "christian brothers", "cms heating", "comfy air", "cool bros", "cool pro", "cool temp", "cooper hvac", "ct morley",
 "cunningham", "danisi", "day and night air", "domino", "donlon", "dynaire", "econo air", "efficient mechanical",
 "elm air", "energy mechanical", "energy wise", "energywise", "enviroduct", "ferguson", "ferrara", "five star aircond",
 "flanders", "flynn air", "galetta", "galletti", "gillette", "grace mechanical", "grant heating", "green home hvac",
 "greenteamli", "groner", "haas hvac", "hafner", "hardy heating", "hardy hvac", "harthomecomfort", "haugen",
 "heart home comfort", "home hart", "herrera", "highpoint mechanical", "homeserve", "innovation hvac", "innovative air",
 "island aire", "jay's heating", "jbs mechanical", "jm heating", "joe's custom", "joes custom", "junior's elite",
 "juniors climate", "keston", "kintech", "li boilers", "limitless hvac", "lm mechanical", "lvv hvac", "mainduct",
 "maple mechanical", "matz", "mcavoy", "mcintosh hvac", "mustang heating", "napolitano", "nuway", "one hour heating",
 "osi oceanside", "paul's way", "perfect temp", "phoenix air", "polar bear", "precision heating", "premier heating",
 "prestige heating", "quality ac and heating", "rellytech", "romanelli", "ryan anthony", "safehaven", "sam hvac",
 "scarpelli", "scheblein", "service experts hampton", "smith brothers", "solo plumbing", "soundview heating",
 "southern comfort", "stan gelber", "sullivan heating", "summit home", "sun ray", "sunset mechanical",
 "sunshine heating", "swezey", "sweezy", "systematic great neck", "tempco", "total air comfort", "tragar",
 "true mechanical", "twin air", "universal heating", "universal home", "universe heating", "universe hvac",
 "universe plumbing", "us air conditioning port", "us heating and air", "varsity", "wales darby", "weber and grahn",
 "arctic air", "burner king", "galletti hvac",
 # non-lead intent
 "tech support", "technical support", "manual", "troubleshooting", "distributor", "remote", "stores",
]
APPLY = "--apply" in sys.argv
vo = not APPLY
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
NEG = list(dict.fromkeys(n.lower() for n in NEG))

kws = q(f"""SELECT ad_group_criterion.keyword.text, campaign.id FROM ad_group_criterion
    WHERE campaign.id IN ({','.join(CAMPS)}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
    AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")
active = {}
for k in kws: active.setdefault(str(k.campaign.id), []).append(k.ad_group_criterion.keyword.text.lower())

plan = {}
for cid in CAMPS:
    existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    plan[cid] = [n for n in NEG if n not in existing]
    print(f"campaign {cid}: {len(plan[cid])} new (already there: {len(NEG) - len(plan[cid])})")

# A negative that would block a live keyword in the same campaign is skipped THERE only (listed for Edu's decision:
# those keywords are $0/30d competitor or manual terms, pausing them is a separate call).
skipped = {}
for cid in CAMPS:
    for n in list(plan[cid]):
        hits = [k for k in active.get(cid, []) if f" {n} " in f" {k} "]
        if hits: plan[cid].remove(n); skipped.setdefault(cid, []).append((n, hits))
print("skipped (would block live keywords):", skipped)
conflicts = []
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id IN ({','.join(CAMPS)}) AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
tot_cost = tot_conv = 0
conv_hits = []
for n in NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    c = sum(r.metrics.cost_micros for r in hit)/1e6; cv = sum(r.metrics.conversions for r in hit)
    tot_cost += c; tot_conv += cv
    if cv: conv_hits.append((n, cv, sorted({r.search_term_view.search_term for r in hit if r.metrics.conversions})))
print(f"30d replay: blocks ${tot_cost:.2f}, conv {tot_conv:.1f}; negatives hitting converting terms: {conv_hits}")
if conflicts: sys.exit(f"ABORT: conflicts with active keywords: {conflicts}")

ops = []
for cid, items in plan.items():
    for t in items:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, cid); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE
        ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives", "(validate_only OK)" if vo else "APPLIED")
if APPLY:
    for cid in CAMPS:
        got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"   read-back {cid}: missing {[n for n in plan[cid] if n not in got]}")
