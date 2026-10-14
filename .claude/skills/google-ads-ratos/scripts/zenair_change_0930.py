"""Zen Air 2026-09-30 — approved by Edu in chat:
  A) NB ad group 205687909824: competitor / supply-house / tech-support / manufacturer negatives,
     plus Zen Air brand negatives so brand searches route to the branded campaign.
  B) BR ad group 193305460463: pause all 8 BROAD brand keywords (only source of non-brand traffic in 90d).
  C) BR campaign 23675783172: campaign-level safety-net negatives (competitors, supply, support, jobs, manufacturers).
  D) NB campaign 24100030790: Maximize Conversions (uncapped) -> Maximize Clicks with $18 max CPC.
Branded Target IS ceiling stays at $8 (exact brand kws avg CPC $4.23-5.26, still 12-16% rank-lost at $8).

Usage: ./tsd.sh zenair_change_0930.py            # validate_only dry run (nothing changes)
       ./tsd.sh zenair_change_0930.py --apply    # mutate for real
Pre-change snapshot: clients/zen-air/snapshot-2026-09-30-pre-negatives-bidcap.json
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "4360840956"
NB_CAMP, NB_AG = "24100030790", "205687909824"
BR_CAMP, BR_AG = "23675783172", "193305460463"
APPLY = "--apply" in sys.argv
NB_MAX_CPC = 18_000_000

COMPETITORS_PHRASE = """
shumate|coolray|cool ray|bardi|casteel|estes|e dennis|zerorez|holtkamp|lawson|sayler|neese jones|rs andrews|r s andrews
reliance heating|reliance hvac|reliable heating and air|reliable ac and heating|triad mechanical|cool air mechanical
coolair mechanical|cool air mechanics|climate heroes|climate masters|hvh mechanical|aire serv|air serv|all weather heating
absolute heating|anytime heating|anytime hvac|cheeky|zone heating and air|zone hvac|varsity zone|allgood|all good services
all good home services|gee heating|gee hvac|gee air|pv heating|poe's|poes|edwards heating|peppers heating|economy heating
pruitt|a team services|kennon|spencer|one hour heating|anchor heating|coleman's heating|te certified|techmazing
mitchell mechanical|mitchell heating|henson|gagne|hero heating|hometown heating|blue tech mechanical|ace and a|ace & a
comfort masters|hammock's|protech heating|kim's hvac|my aire|piedmont mechanical|b mays|capital city mechanical
clark heating|clark's heating|four seasons|4 seasons|service first hvac|southern comfort heating|wilbanks|zack hammonds
air design|american comfort|comfort guardians|hansard|legacy hvac|moncrief|r&r heating|rr heating|seasons comforts
seasons choice|total comfort heating|alpha heating|bolton heating|coolmasters|denson|green heating and air|lee company
mckinney|mckinneys|superior aire|tejada|united maintenance|vital air|ac doctors|air heat america|airtron|arctic blast
boiling point heating|castle heating|champion heating|cool tech hvac|coolmax|davis heating|dunwoody's choice|erhvacr
extreme heating and air|facility controls|flowtech|fox pros|ful bro|georgia air control|grayland mechanical|holt hudson
honor hvac|indoor comfort solutions|innovative mechanical|j r hobbs|jermaine grant|jones heating|mjones|jordan air
keep smiling|lane heating|mcgee heating|mckeon|metro air services|may heating and air|mr cool|perfection air
premier comfort|robillard|self brothers|slam heating|staton|sterling heating|stuart hvac|stuart mechanical|thermal tech
tri county hvac|united air temp|wyrick|gainesville mechanical|martin mechanical|ambient heating|any seasons
arcadia heating|all american services|hvac direct|cochran|ferguson|mingledorff
"""
COMPETITORS_EXACT = """
reliable air|reliable heating|cool air|your ac company|your hvac guys|premier hvac|premier ac|superior air conditioning
metro atlanta heating and cooling|zone air conditioning|ace hvac|precision hvac
"""
SUPPLY_SUPPORT_PHRASE = """
ed's supply|eds supply|sun air supply|sunair supply|trane supply|hvac supply|supply house|supply store|hvac store
r e michel|tech support|technical support|help line
"""
MANUFACTURER_EXACT = """
carrier|goodman|lennox|daikin|rheem|trane|carrier hvac|lennox hvac|goodman hvac|goodman ac unit|lennox air conditioner
carrier near me
"""
BRAND_PHRASE = "zen air|zenair|callzenair"
JOBS_PHRASE = "jobs|job|careers|career|hiring|salary|employment"

BR_BROAD_KW_IDS = ["298692941016", "1231717749522", "2406992335904", "2423116135356",
                   "2493656191363", "2493656191403", "2493656191843", "2493656191883"]


def terms(block):
    out = []
    for t in block.replace("\n", "|").split("|"):
        t = t.strip()
        if t and t not in out:
            out.append(t)
    return out


client = init_client()
ga = client.get_service("GoogleAdsService")
MT = client.enums.KeywordMatchTypeEnum


def report(label, resp, ops):
    pf = getattr(resp, "partial_failure_error", None)
    failed = set()
    if pf and pf.code:
        for d in pf.details:
            fail = client.get_type("GoogleAdsFailure").deserialize(d.value)
            for e in fail.errors:
                idx = e.location.field_path_elements[0].index
                failed.add(idx)
                print(f"   ! {label} op#{idx} '{ops[idx][0]}' [{ops[idx][1]}]: {e.message}")
    print(f"{label}: {len(ops) - len(failed)}/{len(ops)} ok{' (validate_only)' if not APPLY else ''}")


# --- A) NB ad-group negatives -------------------------------------------------------------
nb_neg = ([(t, "PHRASE") for t in terms(COMPETITORS_PHRASE)] + [(t, "EXACT") for t in terms(COMPETITORS_EXACT)]
          + [(t, "PHRASE") for t in terms(SUPPLY_SUPPORT_PHRASE)] + [(t, "EXACT") for t in terms(MANUFACTURER_EXACT)]
          + [(t, "PHRASE") for t in terms(BRAND_PHRASE)])
ops = []
for text, mt in nb_neg:
    op = client.get_type("AdGroupCriterionOperation")
    c = op.create
    c.ad_group = ga.ad_group_path(CID, NB_AG)
    c.negative = True
    c.keyword.text = text
    c.keyword.match_type = getattr(MT, mt)
    ops.append(op)
resp = client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
    request={"customer_id": CID, "operations": ops, "partial_failure": True, "validate_only": not APPLY})
report("A) NB ad-group negatives", resp, nb_neg)

# --- B) pause BR broad keywords -----------------------------------------------------------
ops = []
for kid in BR_BROAD_KW_IDS:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = ga.ad_group_criterion_path(CID, BR_AG, kid)
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    op.update_mask.paths.append("status")
    ops.append(op)
resp = client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
    request={"customer_id": CID, "operations": ops, "partial_failure": True, "validate_only": not APPLY})
report("B) BR broad keywords paused", resp, [(k, "BROAD") for k in BR_BROAD_KW_IDS])

# --- C) BR campaign negatives --------------------------------------------------------------
br_neg = ([(t, "PHRASE") for t in terms(COMPETITORS_PHRASE)] + [(t, "EXACT") for t in terms(COMPETITORS_EXACT)]
          + [(t, "PHRASE") for t in terms(SUPPLY_SUPPORT_PHRASE)] + [(t, "EXACT") for t in terms(MANUFACTURER_EXACT)]
          + [(t, "PHRASE") for t in terms(JOBS_PHRASE)])
ops = []
for text, mt in br_neg:
    op = client.get_type("CampaignCriterionOperation")
    c = op.create
    c.campaign = ga.campaign_path(CID, BR_CAMP)
    c.negative = True
    c.keyword.text = text
    c.keyword.match_type = getattr(MT, mt)
    ops.append(op)
resp = client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "partial_failure": True, "validate_only": not APPLY})
report("C) BR campaign negatives", resp, br_neg)

# --- D) NB bid strategy -> Maximize Clicks, $18 cap ----------------------------------------
op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB_CAMP)
op.update.target_spend.cpc_bid_ceiling_micros = NB_MAX_CPC
op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
client.get_service("CampaignService").mutate_campaigns(
    request={"customer_id": CID, "operations": [op], "validate_only": not APPLY})
print(f"D) NB -> Maximize Clicks, max CPC ${NB_MAX_CPC/1e6:.0f}: ok{' (validate_only)' if not APPLY else ''}")
print(f"\ncounts: NB negatives={len(nb_neg)}, BR negatives={len(br_neg)}, BR broads={len(BR_BROAD_KW_IDS)}")
