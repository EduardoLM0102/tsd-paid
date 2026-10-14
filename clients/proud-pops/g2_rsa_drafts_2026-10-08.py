#!/usr/bin/env python3
"""
Checklist G2: new RSA drafts for the 5 highest-spend ad groups with expected CTR "below average" (2026-10-08).
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
  "AG1_Electrician_NearMe": dict(ad_group="199431304209", url="https://proudpops.com/services/electrical", p1="Electrician", p2="San-Antonio",
    h=["Electrician in San Antonio", "San Antonio Electricians", "Local Electrician Near You", "Need an Electrician? Call Pops",
       "TECL Licensed Electricians", "Free Pop-In Visit", "Written Price Before We Start", "Photos of Everything We Find",
       "No Surprises, No Pressure", "Rated 4.8 on Google", "Panels, Outlets, Lights, Fans", "Breaker Keeps Tripping?",
       "A Real Person Picks Up", "Family Owned and Local", "Book Your Free Pop-In"],
    d=["Breaker tripping or lights flickering? A licensed electrician comes out free to look.",
       "TECL-licensed electricians in San Antonio and New Braunfels. Price in writing first.",
       "Panel upgrades, EV chargers, surge protection, outlets and lighting. Book your Pop-In.",
       "Family owned and local. Photos of what we find and a written warranty on repairs."]),
  "AG2_Electrical_Services": dict(ad_group="196768586637", url="https://proudpops.com/services/electrical", p1="Electrical", p2="Services",
    h=["Electrical Services in SA", "Home Electrical Services", "Electrical Contractor Near You", "San Antonio Electrical Work",
       "TECL Licensed Electricians", "Free Pop-In Visit", "Written Price Before We Start", "Panel Upgrades and EV Chargers",
       "Whole-Home Surge Protection", "Lighting, Fans and Outlets", "Safety Inspection With Report", "Photos of Everything We Find",
       "Rated 4.8 on Google", "No Surprises, No Pressure", "Family Owned and Local"],
    d=["From a flickering light to a full panel upgrade. Licensed electricians, written pricing.",
       "Free Pop-In Visit. We show you photos of what we find and the price before any work.",
       "Serving San Antonio and New Braunfels. EV chargers, surge protection, wiring repair.",
       "Family owned and local. A real person picks up when you call. Book your free Pop-In."]),
  "AG3_Electrical_Repair": dict(ad_group="195955611119", url="https://proudpops.com/services/electrical/repair", p1="Electrical", p2="Repair",
    h=["Electrical Repair San Antonio", "Electrical Repair Near You", "Home Electrical Repair", "Breaker Won't Reset?",
       "Flickering Lights? We Fix It", "Burning Smell at an Outlet?", "Free Pop-In Diagnostic", "Written Price Before We Start",
       "TECL Licensed Electricians", "We Bring a Thermal Camera", "Written Repair Warranty", "Photos of Everything We Find",
       "Rated 4.8 on Google", "Family Owned and Local", "Book Your Free Pop-In"],
    d=["Breaker won't reset or lights flickering? A licensed electrician finds the real cause.",
       "Free Pop-In diagnostic, photos of what we find, and a written price before any work.",
       "Every repair comes with a written workmanship warranty. Family owned and local.",
       "Serving San Antonio and New Braunfels. Book your free Pop-In online or give us a call."]),
  "AG3_HVAC_Maintenance": dict(ad_group="195220521334", url="https://proudpops.com/proud-pops-hvac-services", p1="AC-Service", p2="San-Antonio",
    h=["AC Service in San Antonio", "AC Maintenance San Antonio", "HVAC Service Near You", "AC Tune-Up in San Antonio",
       "Free HVAC Pop-In Visit", "Same-Day HVAC Appointments", "Spring and Fall Tune-Ups", "Pop's Perks: 2 Tune-Ups a Year",
       "Don't Wait for a Breakdown", "Rated 4.8 on Google", "Background-Checked Techs", "Written Price Before We Start",
       "Family Owned and Local", "0% Financing, Approved Credit", "Book Your Free Pop-In"],
    d=["Don't wait for a breakdown. A licensed tech checks your whole system for free.",
       "Spring and fall Clean and Check tune-ups. Pop's Perks members get two a year plus savings.",
       "Rated 4.8 on 1,100+ Google reviews in San Antonio. Family owned, background-checked techs.",
       "Written price before any work starts. No surprises, no pressure. Book your free Pop-In."]),
  "AG1_HVAC_ACRepair": dict(ad_group="202213821731", url="https://proudpops.com/proud-pops-hvac-services", p1="AC-Repair", p2="San-Antonio",
    h=["AC Repair in San Antonio", "AC Repair Near You", "Air Conditioner Repair SA", "AC Quit? Same-Day Repair",
       "Same-Day AC Repair", "Free Pop-In Diagnostic", "Flat-Rate Price Before Work", "Photos of What We Find",
       "We Fix Any Brand of AC", "Rated 4.8 on Google", "Licensed, Background-Checked", "Emergency AC Service",
       "Fix First, Replace if Needed", "Family Owned and Local", "0% Financing, Approved Credit"],
    d=["AC quit? Same-day repair with a free Pop-In diagnostic and photos of what we find.",
       "You get a written, flat-rate price before any work begins. No surprises, no pressure.",
       "Licensed, background-checked techs. Rated 4.8 on 1,100+ Google reviews in San Antonio.",
       "We fix first and only replace when it makes sense. 0% financing with approved credit."]),
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
        for r in resp.mutate_operation_responses:
            print("   ", r.ad_group_ad_result.resource_name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("step", nargs="?", default="validate", choices=["validate", "build"]); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not local_checks():
        sys.exit("fix copy first")
    google(validate=not (a.step == "build" and a.apply))
