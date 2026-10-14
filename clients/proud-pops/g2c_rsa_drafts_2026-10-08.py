#!/usr/bin/env python3
"""
Checklist G2c: second batch of site-verified RSAs (Branded x5, Plumbing AG1/2/3, HVAC AG2) with expected CTR "below average" (2026-10-08).
Built as NEW ads next to the current ones (no downtime). Pause the old ad only after the new one is approved (lesson from B7).
Every claim verified on proudpops.com 2026-10-08:
  free Pop-In visit / diagnostic, written price before work, flat-rate (AC repair page), photos of what we find,
  no surprises / no pressure, TECL-licensed electricians, written repair warranty, thermal camera, panels / EV chargers /
  surge / lighting / fans / outlets, safety inspection with written report, family owned (Jacob & Brandon Rackler),
  4.8 on 1,152 Google reviews (San Antonio), background-checked techs, a real person picks up, same-day AC repair and
  same-day HVAC appointments (HVAC ONLY), seasonal Clean & Check tune-ups, Pop's Perks two tune-ups a year,
  0% financing with approved credit, fix first / replace when it makes sense.
NOT used: 5-star (it's 4.8), same-day for electrical or plumbing, upfront, trusted, affordable.
No phone numbers in ad text (call assets do that).

  validate  (default) checks lengths / dashes / dupes locally, then validate_only creates against Google (policy + format)
  build     --apply: create the 5 RSAs ENABLED in their ad groups (after Edu approves the copy)
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client
CID = "1051843378"

DRAFTS = {
  "Brand_Electrical": dict(ad_group="193744394062", url="https://proudpops.com/", p1="Proud-Pops", p2="Electrical",
    h=["Proud Pops Electrical", "Proud Pops Electricians", "Proud Pops Electric SA", "TECL Licensed Electricians", "Free Pop-In Visit",
       "Written Price Before We Start", "Panels, Outlets, Lights, Fans", "EV Chargers, Surge Protection", "Rated 4.8 on Google",
       "1,500+ Google Reviews", "Family Owned and Local", "Still Family. Still Local.", "A Real Person Picks Up", "Book Your Free Pop-In",
       "Serving SA and New Braunfels"],
    d=["Proud Pops electricians handle panels, wiring, lighting and EV chargers. Free Pop-In.",
       "TECL-licensed electricians in San Antonio and New Braunfels. Price in writing first.",
       "Family owned by Jacob and Brandon Rackler. Rated 4.8 on 1,100+ Google reviews.",
       "Every repair comes with a written workmanship warranty. Book your free Pop-In today."]),
  "Brand_OldName": dict(ad_group="195237569246", url="https://proudpops.com/", p1="Proud", p2="Pops",
    h=["Problem Solvers = Proud Pops", "Now We're Proud Pops", "Formerly The Problem Solvers", "Proud Pops San Antonio",
       "HVAC, Plumbing and Electrical", "Still Serving San Antonio", "Still Family. Still Local.", "Family Owned and Local",
       "Free Pop-In Visit", "Rated 4.8 on Google", "Licensed and Insured", "Written Price Before We Start", "A Real Person Picks Up",
       "Book Your Free Pop-In", "Serving SA and New Braunfels"],
    d=["The Problem Solvers is now Proud Pops. Book your free Pop-In visit today.",
       "Still serving San Antonio and New Braunfels with HVAC, plumbing and electrical.",
       "Family owned by Jacob and Brandon Rackler. Licensed, insured and rated 4.8 on Google.",
       "Written price before any work starts. No surprises, no pressure."]),
  "Brand_Plumbing": dict(ad_group="197098761552", url="https://proudpops.com/", p1="Proud-Pops", p2="Plumbing",
    h=["Proud Pops Plumbing", "Proud Pops Plumbers", "Proud Pops Plumbing SA", "Licensed and Insured Plumbers", "Free Pop-In Visit",
       "Written Price Before We Start", "Leaks, Drains, Water Heaters", "24/7 Emergency Plumbing", "Photos of Everything We Find",
       "Rated 4.8 on Google", "Still Family. Still Local.", "A Real Person Picks Up", "Book Your Free Pop-In",
       "Serving SA and New Braunfels", "Fix First, Replace if Needed"],
    d=["Proud Pops plumbers handle leaks, drains, water heaters and gas lines. Free Pop-In.",
       "Licensed, insured plumbers serving San Antonio and New Braunfels. 24/7 emergency response.",
       "Family owned by Jacob and Brandon Rackler. Rated 4.8 on 1,100+ Google reviews.",
       "No surprise charges. You see the price in writing before any work starts. Book a Pop-In."]),
  "Brand_HVAC": dict(ad_group="197278007500", url="https://proudpops.com/", p1="Proud-Pops", p2="HVAC",
    h=["Proud Pops HVAC", "Proud Pops AC Repair", "Proud Pops Heating and Air", "Same-Day HVAC Appointments", "Free HVAC Pop-In Visit",
       "Flat-Rate Price Before Work", "Background-Checked Techs", "Rated 4.8 on Google", "Pop's Perks: 2 Tune-Ups a Year",
       "0% Financing, Approved Credit", "We Fix Any Brand of AC", "Fix First, Replace if Needed", "Still Family. Still Local.",
       "Book Your Free Pop-In", "Serving SA and New Braunfels"],
    d=["Proud Pops handles AC repair, replacement and tune-ups. Same-day appointments available.",
       "Licensed, background-checked techs. Rated 4.8 on 1,100+ Google reviews in San Antonio.",
       "You get a written, flat-rate price before any work begins. No surprises, no pressure.",
       "Family owned by Jacob and Brandon Rackler. 0% financing with approved credit."]),
  "Brand ProudPops": dict(ad_group="203310611184", url="https://proudpops.com/", p1="Proud", p2="Pops",
    h=["Proud Pops San Antonio", "Proud Pops Home Services", "HVAC, Plumbing and Electrical", "Free Pop-In Visit", "Rated 4.8 on Google",
       "1,500+ Google Reviews", "Still Family. Still Local.", "Family Owned and Local", "Licensed and Insured",
       "Written Price Before We Start", "No Surprises, No Pressure", "A Real Person Picks Up", "24/7 Emergency Service",
       "Book Your Free Pop-In", "Serving SA and New Braunfels"],
    d=["HVAC, plumbing and electrical in San Antonio and New Braunfels. Book your free Pop-In.",
       "Family owned by Jacob and Brandon Rackler. Rated 4.8 on 1,100+ Google reviews.",
       "Written price before any work starts. Photos of everything we find. No surprises.",
       "Licensed and insured. A real person picks up, and we handle 24/7 emergencies."]),
  "AG2_HVAC_Installation": dict(ad_group="198057977242", url="https://proudpops.com/proud-pops-hvac-services", p1="AC-Install", p2="San-Antonio",
    h=["AC Installation San Antonio", "New AC Unit in San Antonio", "AC Replacement San Antonio", "Free Pop-In AC Estimate",
       "We Explain the Math First", "No Commission-Driven Pressure", "0% Financing, Approved Credit", "Written Price Before Work",
       "Rated 4.8 on Google", "Background-Checked Techs", "Family Owned and Local", "Fix First, Replace if Needed",
       "Same-Day HVAC Appointments", "Licensed and Insured", "Book Your Free Pop-In"],
    d=["Need a new AC? We explain savings, lifespan and warranty so you can choose. No pressure.",
       "Free Pop-In estimate and a written price before any work. 0% financing, approved credit.",
       "Family owned by Jacob and Brandon Rackler. Rated 4.8 on 1,100+ Google reviews.",
       "We fix first and only replace when it makes sense. Same-day HVAC appointments."]),
  "AG1_Plumbing_LeakDetection": dict(ad_group="196726297659", url="https://proudpops.com/services/plumbing/leak-detection", p1="Leak-Detection", p2="San-Antonio",
    h=["Leak Detection San Antonio", "Water Leak Repair San Antonio", "Slab Leak Detection", "Leak Under the Slab?", "SAWS Bill Jumped?",
       "No Smashed Tile Guesswork", "Hard Water Pinhole Leaks?", "Free Pop-In Visit", "Photos of Every Finding",
       "Written Price Before We Start", "Licensed and Insured Plumbers", "Rated 4.8 on Google", "Still Family. Still Local.",
       "Leak Detection Near You", "Book Your Free Pop-In"],
    d=["SAWS bill jumped with no visible leak? We find it without smashing tile or guessing.",
       "Free Pop-In Visit, photos of every finding and a written price before any work.",
       "Hard water wears out older copper lines. Licensed plumbers serving SA and New Braunfels.",
       "Family owned and local. Rated 4.8 on 1,100+ Google reviews. Book your free Pop-In."]),
  "AG2_Plumbing_Emergency": dict(ad_group="196726811459", url="https://proudpops.com/services/plumbing", p1="Emergency", p2="Plumber",
    h=["Emergency Plumber San Antonio", "24/7 Emergency Plumbing", "Emergency Plumber Near You", "Burst Pipe? Call Pops",
       "24 Hour Plumber San Antonio", "Plumbing Emergency? Call Pops", "A Real Person Picks Up", "Licensed and Insured Plumbers",
       "Written Price Before We Start", "Photos of Everything We Find", "Rated 4.8 on Google", "Still Family. Still Local.",
       "No Surprises, No Pressure", "Serving SA and New Braunfels", "Leaks, Drains, Water Heaters"],
    d=["Burst pipe or major leak? Licensed plumbers with 24/7 emergency response in San Antonio.",
       "A real person picks up. You get the price in writing before any work starts.",
       "Family owned and local. Rated 4.8 on 1,100+ Google reviews.",
       "Serving San Antonio and New Braunfels. Photos of what we find, no surprise charges."]),
  "AG3_Plumbing_WaterHeaters": dict(ad_group="196184241789", url="https://proudpops.com/services/plumbing/water-heaters", p1="Water-Heater", p2="San-Antonio",
    h=["Water Heater Repair SA", "Water Heater Replacement SA", "Tankless Water Heaters SA", "No Hot Water? Call Pops",
       "Tank and Tankless Service", "Free Pop-In Diagnostic", "Written Price Before We Start", "Photos of Everything We Find",
       "Annual Flush for Hard Water", "Licensed and Insured Plumbers", "Rated 4.8 on Google", "Fix First, Replace if Needed",
       "Still Family. Still Local.", "0% Financing, Approved Credit", "Book Your Free Pop-In"],
    d=["No hot water? We repair and replace tank and tankless water heaters in San Antonio.",
       "Free Pop-In diagnostic, photos of what we find and a written price before any work.",
       "Hard water is rough on water heaters. An annual flush is part of how we keep them going.",
       "Family owned and local. Rated 4.8 on 1,100+ Google reviews. 0% financing, approved credit."]),
}


def local_checks():
    ok = True
    for name, x in DRAFTS.items():
        over = [(t, len(t)) for t in x["h"] if len(t) > 30] + [(t, len(t)) for t in x["d"] if len(t) > 90]
        dashes = [t for t in x["h"] + x["d"] if "—" in t or "–" in t]
        banned = [t for t in x["h"] + x["d"] if any(b in t.lower() for b in ("5-star", "trusted", "affordable", "upfront", "!"))]
        sameday = [t for t in x["h"] + x["d"] if "same-day" in t.lower() and "HVAC" not in name]
        bad = over or dashes or banned or sameday or len(set(x["h"])) != 15 or len(x["d"]) != 4 or len(x["p1"]) > 15 or len(x["p2"]) > 15
        ok &= not bad
        print(f"{name:26s} {len(x['h'])} H (max {max(map(len, x['h']))}), {len(x['d'])} D (max {max(map(len, x['d']))})  "
              + ("OK" if not bad else f"PROBLEM over={over} dashes={dashes} banned={banned} sameday={sameday}"))
    return ok


def google(validate):
    client = init_client(); E = client.enums; ops = []
    for name, x in DRAFTS.items():
        o = client.get_type("MutateOperation"); aga = o.ad_group_ad_operation.create
        aga.ad_group = f"customers/{CID}/adGroups/{x['ad_group']}"; aga.status = E.AdGroupAdStatusEnum.ENABLED
        aga.ad.final_urls.append(x["url"]); rsa = aga.ad.responsive_search_ad; rsa.path1 = x["p1"]; rsa.path2 = x["p2"]
        for t in x["h"]:
            a = client.get_type("AdTextAsset"); a.text = t; rsa.headlines.append(a)
        for t in x["d"]:
            a = client.get_type("AdTextAsset"); a.text = t; rsa.descriptions.append(a)
        ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    resp = client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK (Google accepted all, nothing created)" if validate else "CREATED") + f": {len(ops)} RSAs")
    if not validate:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".g2c_new_ads.txt")
        with open(out, "w") as fh:
            for r in resp.mutate_operation_responses:
                rn = r.ad_group_ad_result.resource_name; print("   ", rn)
                ag, ad = rn.split("/")[-1].split("~"); fh.write(f"{ag} {ad}\n")
        print("   new ad ids saved for g2b_cutover:", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("step", nargs="?", default="validate", choices=["validate", "build"]); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not local_checks():
        sys.exit("fix copy first")
    google(validate=not (a.step == "build" and a.apply))
