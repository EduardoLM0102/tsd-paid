#!/usr/bin/env python3
"""
Cool Hand items 3 + 5 (Edu: "work on topics 1, 2, 3, 4, 5", 2026-10-08). New RSAs for all 16 nonbranded ad groups,
built as NEW ads next to the current ones (no downtime). Old ads are paused only after the new one is approved
(round2_cutover_2026-10-08.py). Budgets unchanged.

Item 3: Furnace-Heating (196336894302) only holds "hvac repair" + "hvac repair near me", so instead of moving the keywords
(which resets their history) it is renamed HVAC-Repair and gets an HVAC-repair ad pointing to /emergency-hvac/
("Emergency HVAC Repair in Mansfield, TX", heating + cooling) instead of the homepage. Swap to the LP rollout's
HVAC Repair page when it exists.

Why: expected CTR is below average on every scored nonbranded keyword. The current ads share the same 6 generic
headlines, carry 8-10 headlines (standard is 15) and never name a city.

Every claim checked on coolhandelectric.com 2026-10-08: family owned, award winning, licensed and insured (company),
TECL License 31768 (electrical only), offices in Mansfield + Red Oak, service area (Burleson, Ennis, Fort Worth, Mansfield,
Midlothian, Pantego, Red Oak, South Arlington, Waxahachie), upfront pricing / no surprises, free quotes (electrical),
financing / easy or flexible payment plans, emergency service available, 100% satisfaction guarantee (electrical),
"we guarantee our work" (home), $37 electrical safety inspection, book online, plus each service page's own specifics.
NOT used: 24/7, 24 hour, after hours (hours question still open), since 2015 (not on the site), decades, 5-star,
top-rated, licensed HVAC (no HVAC license shown on the site), same-day (except ceiling fans, "when our schedule allows").
No phone numbers in ad text (call assets do that). No pinning (Proud Pops G2 precedent).

  (default)  local checks (lengths, dashes, duplicates) + validate_only against Google. Nothing written.
  --apply    rename Furnace-Heating -> HVAC-Repair, create the 16 RSAs ENABLED, save their IDs for the cutover.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query

CID = "9865206319"; C = f"customers/{CID}"
SITE = "https://coolhandelectric.com"
IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".round2_new_ads.txt")
RENAME = ("196336894302", "HVAC-Repair")

AREA = "Serving Mansfield, Red Oak, Midlothian, Waxahachie, Burleson and South Arlington."
E_PROOF = ["TECL Licensed Electricians", "Family Owned and Local", "Award-Winning Local Team", "100% Satisfaction Guarantee",
           "Book Online or Call Today"]
H_PROOF = ["Family Owned and Local", "Award-Winning Local Team", "Quality Work Guaranteed", "Book Online or Call Today"]

DRAFTS = {
  # ---------------- Electrical ----------------
  "Electrician-Broad": dict(ag="200481852420", url=f"{SITE}/electrician-mansfield-tx/", p1="Electrician", p2="Mansfield-TX",
    h=["Electrician in Mansfield, TX", "Red Oak Electrician", "Local Electrician Near You", "Licensed Local Electricians",
       "Repairs, Installs, Upgrades", "Emergency Electrical Repairs", "Free Quotes, Upfront Pricing", "$37 Safety Inspection",
       "Financing Available", "Offices in Mansfield & Red Oak"] + E_PROOF,
    d=["Licensed electricians for home repairs, installs and upgrades in Mansfield and Red Oak.",
       "Free quotes and upfront pricing, so you know the cost before any work begins.",
       "Family owned and award winning. Emergency electrical repairs available.", AREA]),
  "Electrician-General": dict(ag="199867701540", url=f"{SITE}/electrician-mansfield-tx/", p1="Electrical", p2="Mansfield-TX",
    h=["Electrical Contractor Near You", "Electrician Near You", "Electrical Repair Mansfield TX", "Local Electrical Contractor",
       "Red Oak Electrical Repairs", "Licensed and Insured", "Emergency Electrical Repairs", "Free Quotes, Upfront Pricing",
       "$37 Safety Inspection", "Financing Available"] + E_PROOF,
    d=["Licensed electrical contractor for homes in Mansfield, Red Oak and nearby towns.",
       "Troubleshooting, repairs and installs. Free quotes and upfront pricing before work starts.",
       "Family owned and award winning. Emergency electrical repairs available.", AREA]),
  "Ceiling-Fan-Installation": dict(ag="204820073891", url=f"{SITE}/ceiling-fan-installation/", p1="Ceiling-Fans", p2="Mansfield-TX",
    h=["Ceiling Fan Installation", "Ceiling Fan Install Mansfield", "Red Oak Ceiling Fan Install", "Fan Installation Near You",
       "Same-Day Installs Available", "Indoor and Outdoor Fans", "Fan Replacement and Repair", "Sloped Ceilings? No Problem",
       "Upfront Pricing, No Surprises", "Financing Available"] + E_PROOF,
    d=["Licensed electricians install, replace and repair ceiling fans, indoors and outdoors.",
       "Same-day installation when our schedule allows. Upfront pricing before work begins.",
       "We check the wiring, breaker, light kit and remote so your fan works right.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "Circuit-Breaker-Repair": dict(ag="202019894111", url=f"{SITE}/circuit-breaker-installation-repair/", p1="Breakers", p2="Mansfield-TX",
    h=["Circuit Breaker Repair", "Breaker Repair in Mansfield", "Red Oak Breaker Repair", "Breaker Won't Reset?",
       "Breaker Keeps Tripping?", "Scorch Marks on a Breaker?", "Breaker Replacement", "Emergency Service Available",
       "Upfront Pricing, No Surprises", "Free Quotes on Electrical Work"] + E_PROOF,
    d=["Breaker won't reset or keeps tripping? A licensed electrician finds and fixes the cause.",
       "Scorch marks or a breaker over 20 years old usually means it's time to replace it.",
       "Emergency service available. Upfront pricing before any work begins.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "Generator-Installation": dict(ag="201604402920", url=f"{SITE}/emergency-generator-installation/", p1="Generators", p2="Mansfield-TX",
    h=["Generator Installation", "Home Standby Generators", "Whole House Generator Install", "Generator Install Mansfield",
       "Keep Power On in an Outage", "We Size and Place It for You", "Home Inspection Before Install", "Electrical Work Guaranteed",
       "Free Quotes, Upfront Pricing", "Financing Available", "Offices in Mansfield & Red Oak",
       "TECL Licensed Electricians", "Family Owned and Local", "Award-Winning Local Team", "Book Online or Call Today"],
    d=["Whole-house standby generators that take over when the grid goes down.",
       "We inspect your electrical system, then plan the location, fuel lines and generator size.",
       "Licensed, family-owned electricians. We guarantee our work. Financing available.", AREA]),
  "Outlet-Installation": dict(ag="199194839716", url=f"{SITE}/electrical-outlet-installation-service/", p1="Outlets", p2="Mansfield-TX",
    h=["Outlet Installation", "Outlet Installation Mansfield", "GFCI Outlet Installation", "Red Oak Outlet Installation",
       "Smart Outlet Upgrades", "New Outlets and Replacements", "We Check for Hazards First", "Licensed and Insured",
       "Upfront Pricing, No Surprises", "$37 Safety Inspection"] + E_PROOF,
    d=["New outlets, GFCI and smart outlet installs from a licensed and insured electrician.",
       "We inspect your home for electrical hazards first, so the job is done safely.",
       "Upfront pricing before work begins. Family owned and award winning.", AREA]),
  "Panel-Upgrade": dict(ag="196336887022", url=f"{SITE}/electrical-panel-repair-replacement/", p1="Panel-Upgrade", p2="Mansfield-TX",
    h=["Electrical Panel Upgrade", "Panel Upgrade in Mansfield", "Panel Replacement Red Oak", "Electrical Panel Repair",
       "Breakers Tripping Often?", "Old Panel? Time to Upgrade", "Detailed Panel Inspection", "Free Quotes, Upfront Pricing",
       "Emergency Service Available", "Financing Available"] + E_PROOF,
    d=["Panel repair, replacement and upgrades by licensed electricians in Mansfield and Red Oak.",
       "Detailed inspection and upfront pricing, so you know your options before work begins.",
       "Free quotes. Financing available. Family owned and award winning.", AREA]),
  "Smoke-CO-Detector": dict(ag="199868113420", url=f"{SITE}/smoke-detector/", p1="Smoke-Alarms", p2="Mansfield-TX",
    h=["Smoke Detector Installation", "Smoke Detectors in Mansfield", "CO Detector Installation", "Carbon Monoxide Detectors",
       "Hardwired Smoke Alarms", "Older Home? Upgrade Alarms", "Red Oak Smoke Detector Install", "Upfront Pricing, No Surprises",
       "$37 Safety Inspection", "Financing Available"] + E_PROOF,
    d=["Smoke and carbon monoxide detector installs from licensed electricians.",
       "Battery or hardwired smoke alarms, installed and tested by an electrician.",
       "Upfront pricing before work begins. Family owned and award winning.", AREA]),
  "Surge-Protection": dict(ag="204820086211", url=f"{SITE}/whole-house-surge-protector-installation/", p1="Surge", p2="Mansfield-TX",
    h=["Whole House Surge Protector", "Surge Protection Mansfield", "Surge Protector Installation", "Red Oak Surge Protection",
       "Protect Your Appliances", "Small Surges Add Up Daily", "Whole-Home Surge Protection", "Upfront Pricing, No Surprises",
       "Financing Available", "$37 Safety Inspection"] + E_PROOF,
    d=["Small surges hit several times a day and wear down appliances. Protect the whole home.",
       "Licensed electricians install whole-house surge protection, done right.",
       "Upfront pricing and a 100% satisfaction guarantee. Family owned and award winning.", AREA]),
  # ---------------- HVAC ----------------
  "AC-Repair": dict(ag="197830573614", url=f"{SITE}/ac-repair/", p1="AC-Repair", p2="Mansfield-TX",
    h=["AC Repair in Mansfield, TX", "AC Repair Near You", "Red Oak AC Repair", "Air Conditioning Repair",
       "AC Not Cooling? We Fix It", "AC Unit Repair Service", "We Find It and Fix It Right", "Honest Repair Assessments",
       "Emergency AC Repair Available", "Upfront Pricing, No Surprises", "Flexible Payment Plans"] + H_PROOF,
    d=["AC not cooling? We listen first, find the cause and fix it right.",
       "Emergency AC repair available when it can't wait for a regular appointment.",
       "Honest repair-or-replace advice. Flexible payment plans for AC repairs.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "AC-Installation": dict(ag="199830399555", url=f"{SITE}/ac-installation-replacement/", p1="AC-Install", p2="Mansfield-TX",
    h=["AC Installation in Mansfield", "AC Replacement Near You", "Red Oak AC Replacement", "New AC System Install",
       "AC Sized for Your Home", "AC 10 to 15 Years Old?", "Emergency AC Replacement", "Easy Payment Plans",
       "We Help You Weigh Options", "Upfront Pricing, No Surprises", "Offices in Mansfield & Red Oak"] + H_PROOF,
    d=["New AC installs and replacements, sized for your home's square footage and layout.",
       "AC over 10 years old or needs frequent repairs? Replacing it often pays off.",
       "Easy payment plans available. We help you weigh repair versus replace honestly.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "HVAC-Repair": dict(ag="196336894302", url=f"{SITE}/emergency-hvac/", p1="HVAC-Repair", p2="Mansfield-TX",
    h=["HVAC Repair in Mansfield, TX", "HVAC Repair Near You", "Red Oak HVAC Repair", "Heating and Cooling Repair",
       "AC or Heat Not Working?", "Emergency HVAC Repair", "We Prioritize Emergency Calls", "Upfront Pricing, No Surprises",
       "AC, Furnace and Heat Pumps", "Financing Available", "Offices in Mansfield & Red Oak"] + H_PROOF,
    d=["Heating or cooling down? We repair AC, furnaces and heat pumps in Mansfield and Red Oak.",
       "We prioritize emergency calls and keep you informed until your system is running again.",
       "Upfront about costs before we begin any work, so there are no surprises.",
       "Family owned and award winning. Book online or give us a call."]),
  "Furnace-Repair": dict(ag="202019899871", url=f"{SITE}/furnace-repair/", p1="Furnace-Repair", p2="Mansfield-TX",
    h=["Furnace Repair in Mansfield", "Furnace Repair Near You", "Red Oak Furnace Repair", "Furnace Not Heating?",
       "Furnace Acting Up? Call Us", "Get Ready Before Cold Snaps", "Clear Repair Timeline", "Emergency Heating Repair",
       "Upfront Pricing, No Surprises", "Financing Available", "Offices in Mansfield & Red Oak"] + H_PROOF,
    d=["Furnace not heating? We diagnose and repair it with North Texas homes in mind.",
       "Many repairs are done the same day, depending on parts. We give you a clear timeline.",
       "Emergency heating repair available. Upfront about costs before any work begins.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "Furnace-Replacement": dict(ag="198474138425", url=f"{SITE}/furnace-installation-replacement/", p1="New-Furnace", p2="Mansfield-TX",
    h=["Furnace Replacement Mansfield", "Furnace Replacement Near You", "Red Oak Furnace Replacement", "New Furnace Installation",
       "Furnace Over 15 Years Old?", "Sized and Set Up for Your Home", "Efficiency Explained Clearly", "Wide Range of Furnace Brands",
       "Built to Local Code", "Easy Payment Plans", "Offices in Mansfield & Red Oak"] + H_PROOF,
    d=["Furnace over 15 years old or heating unevenly? A new one may be the better choice.",
       "We size each system for your home and explain efficiency ratings in plain terms.",
       "We install a wide range of brands to manufacturer guidelines and local codes.",
       "Family owned and award winning. Financing available. Book online or call."]),
  "Heat-Pump-Repair": dict(ag="199443926095", url=f"{SITE}/heat-pump/", p1="Heat-Pump", p2="Mansfield-TX",
    h=["Heat Pump Repair Mansfield", "Heat Pump Repair Near You", "Red Oak Heat Pump Repair", "Heat Pump Not Working?",
       "Older and Newer Systems", "Repair and Maintenance", "Hands-On Heat Pump Experience", "Emergency Service Available",
       "Upfront Pricing, No Surprises", "Financing Available", "Offices in Mansfield & Red Oak"] + H_PROOF,
    d=["Heat pump not heating or cooling right? We repair and maintain air-source heat pumps.",
       "Hands-on experience with the older and newer systems common in Mansfield homes.",
       "Upfront about costs before work begins. Emergency service available.",
       "Family owned and award winning. Serving Mansfield, Red Oak and nearby towns."]),
  "HVAC-General-Broad": dict(ag="199432346123", url=f"{SITE}/", p1="HVAC", p2="Mansfield-TX",
    h=["HVAC Company in Mansfield, TX", "HVAC Company Near You", "Red Oak HVAC Company", "Local Heating and Cooling",
       "AC, Furnace and Heat Pumps", "Repair, Install, Maintenance", "Emergency Service Available", "Upfront Pricing, No Surprises",
       "Financing Available", "Offices in Mansfield & Red Oak", "Electrical and HVAC Services"] + H_PROOF,
    d=["Family-owned HVAC company in Mansfield and Red Oak. AC, furnace and heat pump service.",
       "Repairs, new installs and maintenance. Emergency service available.",
       "Upfront about costs before work begins. Financing available.",
       "Award winning and local. Book online or give us a call."]),
}


def check():
    problems = []
    for name, d in DRAFTS.items():
        h, ds = d["h"], d["d"]
        if len(h) != 15: problems.append((name, f"{len(h)} headlines"))
        if len(ds) != 4: problems.append((name, f"{len(ds)} descriptions"))
        problems += [(name, f"H too long {len(x)}: {x}") for x in h if len(x) > 30]
        problems += [(name, f"D too long {len(x)}: {x}") for x in ds if len(x) > 90]
        problems += [(name, f"dash: {x}") for x in h + ds if "—" in x or "–" in x]
        if len(set(x.lower() for x in h)) != len(h): problems.append((name, "duplicate headline"))
        if len(d["p1"]) > 15 or len(d["p2"]) > 15: problems.append((name, "path too long"))
        banned = ("24/7", "24 hour", "after hours", "after-hours", "since 2015", "decades", "5-star", "top-rated", "licensed hvac")
        problems += [(name, f"banned phrase: {x}") for x in h + ds if any(b in x.lower() for b in banned)]
    print(f"local check: {len(DRAFTS)} RSAs, {'OK' if not problems else problems}")
    assert not problems


def ops_for(client, E):
    ops = []
    o = client.get_type("MutateOperation"); u = o.ad_group_operation.update
    u.resource_name = f"{C}/adGroups/{RENAME[0]}"; u.name = RENAME[1]; o.ad_group_operation.update_mask.paths.append("name"); ops.append(o)
    for name, d in DRAFTS.items():
        o = client.get_type("MutateOperation"); aga = o.ad_group_ad_operation.create
        aga.ad_group = f"{C}/adGroups/{d['ag']}"; aga.status = E.AdGroupAdStatusEnum.ENABLED
        aga.ad.final_urls.append(d["url"]); rsa = aga.ad.responsive_search_ad; rsa.path1 = d["p1"]; rsa.path2 = d["p2"]
        for t in d["h"]:
            a = client.get_type("AdTextAsset"); a.text = t; rsa.headlines.append(a)
        for t in d["d"]:
            a = client.get_type("AdTextAsset"); a.text = t; rsa.descriptions.append(a)
        ops.append(o)
    return ops


def run(apply):
    check()
    client = init_client(); E = client.enums
    ops = ops_for(client, E)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not apply
    resp = client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if apply else "VALIDATE-ONLY OK (nothing written)") + f": rename + {len(ops) - 1} RSAs")
    if apply:
        with open(IDS_FILE, "w") as fh:
            for name, r in zip(DRAFTS, list(resp.mutate_operation_responses)[1:]):
                rn = r.ad_group_ad_result.resource_name  # customers/X/adGroupAds/AG~AD
                ag, ad = rn.split("/")[-1].split("~"); fh.write(f"{ag} {ad} {name}\n")
        print(f"saved new ad IDs to {IDS_FILE}")
        for line in open(IDS_FILE):
            ag, ad, name = line.split()
            for r in run_query(CID, f"""SELECT ad_group.name, ad_group_ad.status, ad_group_ad.policy_summary.review_status,
ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group.id = {ag} AND ad_group_ad.ad.id = {ad}"""):
                x = r["ad_group_ad"]; print(f"   READ-BACK {r['ad_group']['name']:26s} ad {ad} {x.get('status')} {x.get('policy_summary')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    run(a.apply)
