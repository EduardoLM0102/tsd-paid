# APPLIED LIVE 2026-10-30 on Edu's go ("Apply 1 to 4"). Do NOT re-run with --apply (bidding guard aborts anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Cool Hand Electric (9865206319), from the 10-30 QS recheck (fu-024), Edu: "Apply 1 to 4".
1. HVAC + Electrical Search: Maximize Conversions (uncapped) -> Maximize Clicks with a CPC cap (HVAC $8, Electrical $9).
   CPC went from $4-6 to $10-20 after the 10-08 changes. Budgets unchanged ($36 / $67).
2. Campaign PHRASE negatives for competitor names that took 28% of visible nonbranded spend 10-10..10-29.
3. Copy test: one new RSA next to the current one in the 4 biggest ad groups, leading with proof from the go. pages
   (4.9 / 420 Google reviews, BBB A+, Voted Best in Ellis County, $25,000 guarantee, $37 inspection on Electrical).
   No emergency / 24-7 claims (pages show Mon-Fri 8-5, Sat 8-12). Same go. URLs and paths as the current ads.
(4. LP-score recheck ~11-13 is a Command Center follow-up, not an API change.)
Aborts on unexpected state.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9865206319"
C = f"customers/{CID}"
HVAC, ELEC = "24118511502", "24123995882"
CAPS = {HVAC: 8.0, ELEC: 9.0}
BUDGETS = {HVAC: 36.0, ELEC: 67.0}
NEG = {HVAC: ["chill brothers", "hamill and harrison", "royal air", "toms mechanical", "tom's mechanical"],
       ELEC: ["mister sparky", "iec contractors"]}

PROOF_D = "Voted Best in Ellis County, BBB A+ rated and backed by a $25,000 guarantee."
AREA_D = "Serving Mansfield, Red Oak, Midlothian, Waxahachie, Burleson and South Arlington."
RSAS = {
    "Electrician-Broad": dict(ag="200481852420", url="https://go.coolhandelectric.com/electrician/", p1="Electrician", p2="Mansfield-TX",
        h=["Electrician in Mansfield, TX", "4.9 Stars, 420 Google Reviews", "$37 Electrical Inspection", "Voted Best in Ellis County",
           "BBB A+ Rated Electricians", "$25,000 Contractor Guarantee", "TECL License #31768", "Red Oak Electrician",
           "Local Electrician Near You", "Repairs, Installs, Upgrades", "Easy Payment Plans", "Family Owned and Local",
           "Open Monday to Saturday", "Offices in Mansfield & Red Oak", "Book Online or Call Today"],
        d=["Rated 4.9 from 420 Google reviews. Licensed electricians for repairs and upgrades.",
           "Ask about our $37 electrical safety inspection when you book online or by phone.", PROOF_D, AREA_D]),
    "Electrician-General": dict(ag="199867701540", url="https://go.coolhandelectric.com/electrician/", p1="Electrical", p2="Mansfield-TX",
        h=["Electrical Contractor Near You", "4.9 Stars, 420 Google Reviews", "$37 Electrical Inspection", "Voted Best in Ellis County",
           "BBB A+ Rated Electricians", "$25,000 Contractor Guarantee", "TECL License #31768", "Electrical Repair Mansfield TX",
           "Licensed Electrical Contractor", "Red Oak Electrical Repairs", "Easy Payment Plans", "Family Owned and Local",
           "Open Monday to Saturday", "Offices in Mansfield & Red Oak", "Book Online or Call Today"],
        d=["Rated 4.9 from 420 Google reviews. Licensed electrical contractor for homes.",
           "Ask about our $37 electrical safety inspection when you book online or by phone.", PROOF_D, AREA_D]),
    "HVAC-Repair": dict(ag="196336894302", url="https://go.coolhandelectric.com/hvac-repair/", p1="HVAC-Repair", p2="Mansfield-TX",
        h=["HVAC Repair in Mansfield, TX", "4.9 Stars, 420 Google Reviews", "Voted Best in Ellis County", "BBB A+ Rated Local Company",
           "$25,000 Contractor Guarantee", "Licensed HVAC Techs", "Heating and Cooling Repair", "AC, Furnace and Heat Pumps",
           "Red Oak HVAC Repair", "HVAC Repair Near You", "Easy Payment Plans", "Family Owned and Local",
           "Open Monday to Saturday", "Offices in Mansfield & Red Oak", "Book Online or Call Today"],
        d=["Rated 4.9 from 420 Google reviews. Licensed techs repair AC, furnaces and heat pumps.",
           PROOF_D, "Easy payment plans available. Book online or call for our first opening.", AREA_D]),
    "AC-Repair": dict(ag="197830573614", url="https://go.coolhandelectric.com/ac-repair/", p1="AC-Repair", p2="Mansfield-TX",
        h=["AC Repair in Mansfield, TX", "4.9 Stars, 420 Google Reviews", "AC Not Cooling? We Fix It", "Voted Best in Ellis County",
           "BBB A+ Rated Local Company", "$25,000 Contractor Guarantee", "Licensed HVAC Techs", "Red Oak AC Repair",
           "AC Repair Near You", "Air Conditioning Repair", "Fix It Right the First Time", "Easy Payment Plans",
           "Family Owned and Local", "Open Monday to Saturday", "Book Online or Call Today"],
        d=["Rated 4.9 from 420 Google reviews. We find the cause and fix it right the first time.",
           PROOF_D, "Easy payment plans available. Book online or call for our first opening.", AREA_D]),
}
APPLY = "--apply" in sys.argv
vo = not APPLY

# --- local checks
bad = []
for n, r in RSAS.items():
    if len(r["h"]) != 15 or len(r["d"]) != 4: bad.append((n, "count"))
    bad += [(n, h, len(h)) for h in r["h"] if len(h) > 30]
    bad += [(n, x, len(x)) for x in r["d"] if len(x) > 90]
    bad += [(n, "dup headline") for h in r["h"] if r["h"].count(h) > 1]
    bad += [(n, x) for x in r["h"] + r["d"] if any(b in x.lower() for b in ("24/7", "24 hour", "emergency", "after hours"))]
    if "coolhandelectric.com" in r["url"] and not r["url"].startswith("https://go."): bad.append((n, "not go."))
if bad: sys.exit(f"ABORT local check: {bad}")
print("local check OK: 4 RSAs, lengths within limits, go. URLs only")

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

# --- guards
for cid in (HVAC, ELEC):
    c = q(f"""SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign_budget.amount_micros
        FROM campaign WHERE campaign.id = {cid}""")[0]
    print(f"{c.campaign.name}: {c.campaign.bidding_strategy_type.name} budget ${c.campaign_budget.amount_micros/1e6:.2f} portfolio='{c.campaign.bidding_strategy}'")
    if c.campaign.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS" or c.campaign.bidding_strategy: sys.exit("ABORT: unexpected bidding")
    if abs(c.campaign_budget.amount_micros/1e6 - BUDGETS[cid]) > 0.01: sys.exit("ABORT: budget changed")
for n, r in RSAS.items():
    ag = q(f"SELECT ad_group.name, ad_group.status FROM ad_group WHERE ad_group.id = {r['ag']}")[0].ad_group
    if ag.name != n or ag.status.name != "ENABLED": sys.exit(f"ABORT: ad group {n} not found ENABLED")
live = {cid: [x.ad_group_criterion.keyword.text.lower() for x in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    for cid in (HVAC, ELEC)}
hit = [(cid, n, k) for cid in NEG for n in NEG[cid] for k in live[cid] if f" {n} " in f" {k} "]
if hit: sys.exit(f"ABORT: negative hits a live keyword {hit}")
existing = {cid: {x.campaign_criterion.keyword.text.lower() for x in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")} for cid in (HVAC, ELEC)}
neg_new = {cid: [n for n in NEG[cid] if n not in existing[cid]] for cid in NEG}
print("new negatives:", neg_new)

# --- one atomic request
ops = []
for cid, cap in CAPS.items():
    o = client.get_type("MutateOperation"); u = o.campaign_operation.update
    u.resource_name = f"{C}/campaigns/{cid}"; u.target_spend.cpc_bid_ceiling_micros = int(cap * 1e6)
    o.campaign_operation.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros"); ops.append(o)
for cid, lst in neg_new.items():
    for t in lst:
        o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
        cc.campaign = f"{C}/campaigns/{cid}"; cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE; ops.append(o)
for n, r in RSAS.items():
    o = client.get_type("MutateOperation"); aga = o.ad_group_ad_operation.create
    aga.ad_group = f"{C}/adGroups/{r['ag']}"; aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
    aga.ad.final_urls.append(r["url"]); rsa = aga.ad.responsive_search_ad; rsa.path1 = r["p1"]; rsa.path2 = r["p2"]
    for t in r["h"]:
        a = client.get_type("AdTextAsset"); a.text = t; rsa.headlines.append(a)
    for t in r["d"]:
        a = client.get_type("AdTextAsset"); a.text = t; rsa.descriptions.append(a)
    ops.append(o)
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = vo
resp = ga.mutate(request=req)
print(("APPLIED" if APPLY else "VALIDATE-ONLY OK (nothing written)") + f": 2 bid changes, {sum(len(v) for v in neg_new.values())} negatives, {len(RSAS)} RSAs")

# --- read-back
if APPLY:
    for cid in (HVAC, ELEC):
        c = q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
            FROM campaign WHERE campaign.id = {cid}""")[0]
        print(f"READ-BACK {c.campaign.name}: {c.campaign.bidding_strategy_type.name} cap ${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} budget ${c.campaign_budget.amount_micros/1e6:.2f}")
    for res in list(resp.mutate_operation_responses):
        rn = res.ad_group_ad_result.resource_name
        if rn:
            ag, ad = rn.split("/")[-1].split("~")
            x = q(f"""SELECT ad_group.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status
                FROM ad_group_ad WHERE ad_group.id = {ag} AND ad_group_ad.ad.id = {ad}""")[0]
            print(f"READ-BACK {x.ad_group.name}: ad {ad} {x.ad_group_ad.status.name} {x.ad_group_ad.policy_summary.review_status.name}")
