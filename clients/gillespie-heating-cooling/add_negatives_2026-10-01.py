#!/usr/bin/env python3
"""Gillespie 2026-10-01: campaign-level negatives on TSD_09.26_Search_NonBranded_Evergreen.

Edu asked to fix the competitor-name and junk searches found in the 10-01 check-in. Lists built from
every Non-Branded search term since launch (08-18 to 10-01, old + new campaign, 764 terms).

Kept open on purpose (client offers these, or they are inside the service area):
  - commercial, boiler, gas fireplace (09-29 form lead came from "gas fireplace service florence ky")
  - financing / bad-credit searches (ads say "Financing Available")
  - brand + install/dealer/near me searches (e.g. "carrier dealers near me", "mrcool installers")
  - towns in the client's area: union (41091), georgetown OH (45121), fayetteville OH (45118),
    winchester OH (45697), dayton KY (next to Newport), mason county, butler (41006), burlington,
    hillsboro/goshen (next to Brown/Clermont), cincinnati (open client question since 09-26)

Usage (from the google-ads-ratos scripts dir):
  ./tsd.sh ../../../../clients/gillespie-heating-cooling/add_negatives_2026-10-01.py          # validate_only
  ./tsd.sh ../../../../clients/gillespie-heating-cooling/add_negatives_2026-10-01.py --apply  # live
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                ".claude", "skills", "google-ads-ratos", "scripts"))
from lib import init_client, run_query  # noqa: E402

CID = "7410489772"
NB_CAMP = "24297839425"
APPLY = "--apply" in sys.argv

COMPETITORS_PHRASE = """
geiler|knock knock|rusk heating|doc rusk|accurate heating|333help|333 help|help heating|help air conditioning
gerard hvac|jefferson heating|premier heating|raisor|johnson heating|zimmer heating|gozimmer|bachman
hubbard mechanical|logan heating|logan hvac|logan a c|reinhart|victory air|watkins heating|aces of air
adam heating|adams heating and cooling|airbenders|airtron|anderson heating|arc electric|carlos dye
chuck's heating|chucks heating|davis heating|ed brun|gc home service|honesty mechanical|howard heating
jones heating|miller heating|morris heating|perfect climate|peters heating|reliant heating|schaefer heating
shafer heating|smiths heating|smith's heating|steve's heating|steves heating|thomas and galbraith
thomas & galbraith|rechtin|valentino hvac|wingate mechanical|workman hvac|folk and sons|all good home
ambient hvac|ams hvac|apex hvac|armor heating|bello hvac|blue collar heating|butler heating and air|call dad
carr electric|certified service inc|chad love|chad simpson|comfort control|comfort man heating
comfort systems usa|comfy club|corcoran|custom air|dns heating|dons ac|duck air|eddie green|elite hvac
fast response heating|fenix|forever vent|four quarters|fresh air hvac|golden rule|greater comfort|hauck
j m mechanical|kw mechanical|mike's hvac|mikes hvac|miley heating|nextech|nicely heating|peak heating
perfection group|pinnacle hvac|pro source heating|r & w heating|redwood hvac|refcon|reupert|schneller
sealtite|teamwork heating|teasdale|teegarden|tr miller|tri county heating|tribble refrigeration
turner on electric|valor heating|titan heating|any weather|p3 mechanical|acco air|air plus heating
monarch hvac|reading heating|stycove|taylor heating|rescue hvac|smart heating and cooling|blue hvac
climate control solutions|mars hvac|cinfab
"""
SUPPLY_DIY_PHRASE = """
johnstone|ferguson|habegger|re michel|r e michel|re michaels|supply|supplier|distributor|distributors
distribution|parts|store|outlet|costco|lowe's|sells to public|for sale|where to buy|can i buy|hvac direct
repair clinic|rep locator|btu|aciq|brands|brand|manufacturers|manufacturer|list of|sheet metal|fabrication
assistance|industry|businesses
"""
CAR_WINDOW_PHRASE = """
car|cars|auto|automotive|vehicle|window ac|window air conditioner|window unit|portable ac
portable air conditioner|through the wall
"""
# Plurals/variants of Edu's own 09-22 negatives (cheap/quote/price/cost); negatives don't match close variants.
PRICE_VARIANTS_PHRASE = "prices|pricing|costs|quotes|cheapest"
OUT_OF_AREA_PHRASE = """
lexington|louisville|london ky|danville|somerset|harlan|elizabethtown|richmond ky|mt sterling|mount sterling
morehead|georgetown ky|dayton ohio|dayton oh|columbus|springfield|wichita|dallas|cadiz|ashland|lebanon
new jersey|nj
"""
MANUFACTURER_EXACT = """
carrier|goodman|lennox|daikin|rheem|trane|bryant|ruud|tempstar|amana|york
carrier hvac|carrier hvac system|carrier hvac systems|carrier furnace|carrier furnaces|trane hvac
trane hvac systems|train hvac systems|trane heating system|goodman hvac systems|goodman furnace|goodman ac unit
goodman gas furnace|goodman electric furnace|goodman company air conditioner|goodman daikin|daikin hvac
daikin furnace|daikin comfort|daikin electric furnace|bryant hvac|payne furnace|amana hvac|american standard hvac
american standard heating and air conditioning|ameristar hvac|ruud hvac|ruud furnace|ruud heat pumps
rheem furnace|rheem hvac systems|rheem weather king furnace|toshiba hvac|mitsubishi hvac|york air conditioning
lennox furnaces|lennox air furnace|lennox elite|lennox heating and air conditioning systems|tempstar hvac
tempstar furnace|tempstar gas furnace|tempstar heating and cooling|coleman furnace|coleman home furnace
ducane hvac|ducane furnace|luxaire furnace|evcon hvac|evcon ac unit|comfort maker furnace|thermopride furnace
gibson hvac|ge hvac|ge furnace|icp hvac|spacepak hvac|magicpack hvac|melco hvac|mrcool hvac system
armstrong air furnace|armstrong air conditioning|bard ac units
best hvac system for home|best hvac systems|best hvac systems 2026|best furnaces|highest rated hvac systems
best replacement hvac system|most affordable hvac system|hvac people|major hvac companies
"""


def terms(block):
    out = []
    for t in block.replace("\n", "|").split("|"):
        t = t.strip()
        if t and t not in out:
            out.append(t)
    return out


wanted = ([(t, "PHRASE") for t in terms(COMPETITORS_PHRASE)] + [(t, "PHRASE") for t in terms(SUPPLY_DIY_PHRASE)]
          + [(t, "PHRASE") for t in terms(CAR_WINDOW_PHRASE)] + [(t, "PHRASE") for t in terms(PRICE_VARIANTS_PHRASE)]
          + [(t, "PHRASE") for t in terms(OUT_OF_AREA_PHRASE)] + [(t, "EXACT") for t in terms(MANUFACTURER_EXACT)])

# --- safety checks against the live account -------------------------------------------------
existing = {(r["campaign_criterion"]["keyword"]["text"].lower(), r["campaign_criterion"]["keyword"]["match_type"])
            for r in run_query(CID, f"SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type "
                                    f"FROM campaign_criterion WHERE campaign.id = {NB_CAMP} "
                                    f"AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
keywords = [r["ad_group_criterion"]["keyword"]["text"].lower()
            for r in run_query(CID, f"SELECT ad_group_criterion.keyword.text FROM keyword_view "
                                    f"WHERE campaign.id = {NB_CAMP} AND ad_group_criterion.status = 'ENABLED' "
                                    f"AND ad_group_criterion.negative = FALSE")]
converted = sorted({r["search_term_view"]["search_term"].lower()
                    for r in run_query(CID, "SELECT search_term_view.search_term, metrics.conversions FROM search_term_view "
                                            "WHERE segments.date BETWEEN '2026-08-18' AND '2026-10-01' "
                                            "AND metrics.conversions > 0")})


def blocks(neg, mt, query):
    q, n = query.split(), neg.split()
    if mt == "EXACT":
        return q == n
    return any(q[i:i + len(n)] == n for i in range(len(q) - len(n) + 1))


problems = []
for text, mt in wanted:
    for kw in keywords:
        if blocks(text, mt, kw):
            problems.append(f"'{text}' [{mt}] would block active keyword '{kw}'")
    for st in converted:
        if blocks(text, mt, st):
            problems.append(f"'{text}' [{mt}] would block converting search term '{st}'")
    if "gillespie" in text:
        problems.append(f"'{text}' contains the client's brand")
if problems:
    print("STOP, conflicts found:")
    print("\n".join("  " + p for p in problems))
    sys.exit(1)
print(f"Checked {len(wanted)} negatives against {len(keywords)} active keywords and "
      f"{len(converted)} converting search terms: no conflicts. Converting terms: {converted}")

new = [(t, mt) for t, mt in wanted if (t.lower(), mt) not in existing]
print(f"{len(wanted) - len(new)} already on the campaign, {len(new)} to add.")

# --- mutate ----------------------------------------------------------------------------------
client = init_client()
ga = client.get_service("GoogleAdsService")
MT = client.enums.KeywordMatchTypeEnum
ops = []
for text, mt in new:
    op = client.get_type("CampaignCriterionOperation")
    c = op.create
    c.campaign = ga.campaign_path(CID, NB_CAMP)
    c.negative = True
    c.keyword.text = text
    c.keyword.match_type = getattr(MT, mt)
    ops.append(op)
resp = client.get_service("CampaignCriterionService").mutate_campaign_criteria(
    request={"customer_id": CID, "operations": ops, "partial_failure": True, "validate_only": not APPLY})
failed = set()
pf = getattr(resp, "partial_failure_error", None)
if pf and pf.code:
    for d in pf.details:
        fail = client.get_type("GoogleAdsFailure").deserialize(d.value)
        for e in fail.errors:
            idx = e.location.field_path_elements[0].index
            failed.add(idx)
            print(f"   ! op#{idx} '{new[idx][0]}' [{new[idx][1]}]: {e.message}")
print(f"NB campaign negatives: {len(new) - len(failed)}/{len(new)} ok{' (validate_only)' if not APPLY else ' (LIVE)'}")
