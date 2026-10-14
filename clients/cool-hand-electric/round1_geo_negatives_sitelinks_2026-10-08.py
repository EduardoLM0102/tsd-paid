#!/usr/bin/env python3
"""
Cool Hand round 1 (Edu: "work on topics 1, 2, 3, 4, 5", 2026-10-08). Budgets unchanged. Account 9865206319.

  1  Geo: location option PRESENCE (people in / regularly in the area) on TSD_Search_HVAC, _Electrical, _Branded.
  2  Negatives (campaign-level, from the Aug 25 - Oct 7 search terms). Own-brand: add 4 "cool hand ..." PHRASE keywords
     to Branded FIRST, then negate "cool hand" in HVAC + Electrical (Proud Pops H2 lesson: never leave brand searches
     with no ad). Competitor names only where they had 0 conversions; Dallas and other city terms left alone (they convert).
  4  Sitelinks: the electrical ad-group-level sitelinks on Furnace-Heating, HVAC-General-Broad and Brand-Terms come off.
     Several point to /electrical/... URLs that redirect and DROP the gclid (one lands on the homepage). Replaced by
     campaign-level sets with direct URLs: HVAC = AC/heating pages, Electrical = electrical pages (it was showing the
     account's HVAC sitelinks), Branded = a mix. Every URL checked 200 with no redirect, gclid kept (2026-10-08).
     Sitelink descriptions use only claims on the linked page (checked 2026-10-08). The account-level HVAC sitelinks are
     Google auto-created ("text customization") and can't be linked by advertisers, so all sitelinks here are new assets.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, re, argparse, collections
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query

CID = "9865206319"; C = f"customers/{CID}"
HVAC, ELEC, BRAND = "24118511502", "24123995882", "24123995948"
BRAND_AG = "194393028410"
STRIP_AGS = {"196336894302": "Furnace-Heating", "199432346123": "HVAC-General-Broad", BRAND_AG: "Brand-Terms"}
S, U = "2026-08-25", "2026-10-07"

BRAND_KW = ["cool hand hvac", "cool hand heating", "cool hand air", "cool hand ac"]
NEG_BOTH = [("cool hand", "PHRASE"), ("commercial", "PHRASE"), ("industrial", "PHRASE"), ("home depot", "PHRASE"),
            ("lowes", "PHRASE"), ("lowe's", "PHRASE"), ("ferguson", "PHRASE"), ("for sale", "PHRASE"), ("supply", "PHRASE"),
            ("apprentice", "PHRASE"), ("apprenticeship", "PHRASE"), ("solar", "PHRASE"), ("appliance", "PHRASE")]
NEG_HVAC = [("window unit", "PHRASE"), ("team enoch", "PHRASE"), ("burke mechanical", "PHRASE"), ("daffan", "PHRASE"),
            ("jamar air", "PHRASE")]
NEG_ELEC = [("encore electricity", "PHRASE"), ("fancher electric", "PHRASE"), ("motor repair", "PHRASE")]
NEGS = {HVAC: NEG_BOTH + NEG_HVAC, ELEC: NEG_BOTH + NEG_ELEC}

# (tmp id, link text, url, desc1, desc2); None = reuse an existing asset found by link text + url
NEW_SL = {
    "ac_install": ("AC Installation", "https://coolhandelectric.com/ac-installation-replacement/", "New AC sized for your home", "Payment plans available"),
    "emerg_hvac": ("Emergency HVAC Repair", "https://coolhandelectric.com/emergency-hvac/", "Emergency service available", "Heating and cooling repair"),
    "panel": ("Panel Upgrades", "https://coolhandelectric.com/electrical-panel-repair-replacement/", "Panel repair and replacement", "Upfront pricing before work"),
    "surge": ("Surge Protection", "https://coolhandelectric.com/whole-house-surge-protector-installation/", "Whole-home surge protectors", "Protect your appliances"),
    "generator": ("Generator Installation", "https://coolhandelectric.com/emergency-generator-installation/", "Whole-house backup generators", "We guarantee our electrical work"),
    "fan": ("Ceiling Fan Installation", "https://coolhandelectric.com/ceiling-fan-installation/", "Indoor and outdoor fans", "Upfront pricing before work"),
    "inspection": ("$37 Safety Inspection", "https://coolhandelectric.com/electrical-safety-inspection/", "Check your home's wiring", "Recommended every 3 to 5 years"),
    "ev": ("EV Charger Installation", "https://coolhandelectric.com/ev-charger-installation/", "Home EV charger installs", "Permitted and inspected"),
    "electrician": ("Electrician Services", "https://coolhandelectric.com/electrician-mansfield-tx/", "Licensed residential electricians", "Free quotes, upfront pricing"),
    "ac_repair": ("Air Conditioning Repair", "https://coolhandelectric.com/ac-repair/", "We find the cause and fix it", "Emergency service available"),
    "ac_maint": ("AC Maintenance", "https://coolhandelectric.com/ac-maintenance/", "Helps protect your warranty", "Fewer emergency calls"),
    "furnace_repair": ("Furnace Repair", "https://coolhandelectric.com/furnace-repair/", "Many repairs done same day", "We give you a clear timeline"),
    "heat_pump": ("Heat Pump Repair", "https://coolhandelectric.com/heat-pump/", "Repair and maintenance", "Hands-on heat pump experience"),
    "contact": ("Contact Us", "https://coolhandelectric.com/contact-us/", "Offices in Mansfield and Red Oak", "Book online or give us a call"),
}
SETS = {
    HVAC: ["ac_repair", "ac_install", "ac_maint", "furnace_repair", "heat_pump", "emerg_hvac", "contact"],
    ELEC: ["electrician", "panel", "surge", "generator", "fan", "inspection", "ev", "contact"],
    BRAND: ["electrician", "ac_repair", "panel", "furnace_repair", "inspection", "contact"],
}
client = init_client(); E = client.enums
f = lambda x: float(x or 0)
toks = lambda s: re.findall(r"[a-z0-9'&$]+", s.lower())


def blocks(neg, mt, q):
    n, w = toks(neg), toks(q)
    if mt == "EXACT": return n == w
    if mt == "PHRASE": return any(w[i:i + len(n)] == n for i in range(len(w) - len(n) + 1))
    return set(n) <= set(w)


def check_copy():
    for k, (t, u, d1, d2) in NEW_SL.items():
        assert len(t) <= 25 and len(d1) <= 35 and len(d2) <= 35, (k, len(t), len(d1), len(d2))
        assert not any(x in t + d1 + d2 for x in ("—", "–")), k
    print(f"copy check OK: {len(NEW_SL)} new sitelinks within 25/35/35 chars, no dashes")


def negatives_report():
    terms = collections.defaultdict(lambda: [0.0, 0.0])
    for r in run_query(CID, f"""SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.all_conversions FROM search_term_view
WHERE campaign.id IN ({HVAC}, {ELEC}) AND segments.date BETWEEN '{S}' AND '{U}'"""):
        t = terms[(r["campaign"]["id"], r["search_term_view"]["search_term"])]
        t[0] += f(r["metrics"].get("cost_micros")) / 1e6; t[1] += f(r["metrics"].get("all_conversions"))
    own = collections.defaultdict(list)
    for r in run_query(CID, f"""SELECT campaign.id, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id IN ({HVAC}, {ELEC})
AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'"""):
        own[r["campaign"]["id"]].append(r["ad_group_criterion"]["keyword"]["text"])
    existing = collections.defaultdict(set)
    for r in run_query(CID, f"""SELECT campaign.id, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
WHERE campaign.id IN ({HVAC}, {ELEC}) AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"""):
        existing[r["campaign"]["id"]].add((r["campaign_criterion"]["keyword"]["text"], str(r["campaign_criterion"]["keyword"]["match_type"])))
    final = {}
    for camp, negs in NEGS.items():
        print(f"\n== negatives for {'HVAC' if camp == HVAC else 'Electrical'}")
        keep = []
        for neg, mt in negs:
            if any(blocks(e, em, neg) for e, em in existing[camp]):
                print(f"   SKIP already covered  {neg}"); continue
            coll = [k for k in own[camp] if blocks(neg, mt, k)]
            hit = {q: v for (c, q), v in terms.items() if c == camp and blocks(neg, mt, q)}
            cost = sum(v[0] for v in hit.values()); conv = sum(v[1] for v in hit.values())
            print(f"   {mt:6s} {neg:20s} blocks {len(hit):3d} terms ${cost:7.2f} {conv:.1f} conv  e.g. {list(hit)[:2]}" + (f"  !! COLLIDES {coll}" if coll else ""))
            assert not coll, (neg, coll)
            keep.append((neg, mt))
        final[camp] = keep
    return final


def find_assets():
    rows = run_query(CID, "SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls FROM asset WHERE asset.type = 'SITELINK'")
    out = {}
    for key, (text, url) in EXISTING_SL.items():
        m = [r["asset"]["id"] for r in rows if r["asset"]["sitelink_asset"]["link_text"] == text and url in (r["asset"].get("final_urls") or [])]
        assert m, f"existing sitelink not found: {text} {url}"
        out[key] = f"{C}/assets/{m[0]}"
    return out


def ag_sitelink_links():
    return run_query(CID, f"""SELECT ad_group.id, ad_group_asset.resource_name, asset.sitelink_asset.link_text FROM ad_group_asset
WHERE ad_group.id IN ({','.join(STRIP_AGS)}) AND ad_group_asset.field_type = 'SITELINK' AND ad_group_asset.status = 'ENABLED'""")


def campaign_sitelinks(camp):
    return run_query(CID, f"""SELECT campaign.id, asset.sitelink_asset.link_text, asset.final_urls, campaign_asset.status FROM campaign_asset
WHERE campaign.id = {camp} AND campaign_asset.field_type = 'SITELINK' AND campaign_asset.status = 'ENABLED'""")


def run(validate):
    check_copy()
    final_negs = negatives_report()
    have_brand = {r["ad_group_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE ad_group.id = {BRAND_AG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'""")}
    for camp in (HVAC, ELEC, BRAND):
        assert not campaign_sitelinks(camp), f"campaign {camp} already has campaign-level sitelinks; re-check before running"
    strip = ag_sitelink_links()
    print(f"\nad-group sitelink links to remove: {collections.Counter(STRIP_AGS[r['ad_group']['id']] for r in strip)}")

    ops = []
    def op(): o = client.get_type("MutateOperation"); ops.append(o); return o
    # 1 geo
    for camp in (HVAC, ELEC, BRAND):
        o = op(); u = o.campaign_operation.update; u.resource_name = f"{C}/campaigns/{camp}"
        u.geo_target_type_setting.positive_geo_target_type = E.PositiveGeoTargetTypeEnum.PRESENCE
        o.campaign_operation.update_mask.paths.append("geo_target_type_setting.positive_geo_target_type")
    # 2a brand keywords first
    for kw in BRAND_KW:
        if kw in have_brand: continue
        o = op(); k = o.ad_group_criterion_operation.create; k.ad_group = f"{C}/adGroups/{BRAND_AG}"
        k.status = E.AdGroupCriterionStatusEnum.ENABLED; k.keyword.text = kw; k.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE
    # 2b negatives
    for camp, negs in final_negs.items():
        for neg, mt in negs:
            o = op(); cc = o.campaign_criterion_operation.create; cc.campaign = f"{C}/campaigns/{camp}"; cc.negative = True
            cc.keyword.text = neg; cc.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
    # 4a new sitelink assets
    tmp = {}
    for i, (key, (text, url, d1, d2)) in enumerate(NEW_SL.items(), start=1):
        rn = f"{C}/assets/-{i}"; tmp[key] = rn
        o = op(); a = o.asset_operation.create; a.resource_name = rn; a.final_urls.append(url)
        a.sitelink_asset.link_text = text; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    # 4b campaign-level links
    for camp, keys in SETS.items():
        for key in keys:
            o = op(); ca = o.campaign_asset_operation.create; ca.campaign = f"{C}/campaigns/{camp}"
            ca.asset = tmp[key]; ca.field_type = E.AssetFieldTypeEnum.SITELINK
    # 4c remove ad-group-level sitelink links
    for r in strip:
        o = op(); o.ad_group_asset_operation.remove = r["ad_group_asset"]["resource_name"]

    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("\nVALIDATE-ONLY OK (nothing written)" if validate else "\nAPPLIED") + f": {len(ops)} ops")
    if not validate:
        readback()


def readback():
    for r in run_query(CID, f"SELECT campaign.name, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id IN ({HVAC}, {ELEC}, {BRAND})"):
        print("READ-BACK geo:", r["campaign"]["name"], r["campaign"].get("geo_target_type_setting", {}).get("positive_geo_target_type"))
    kws = [r["ad_group_criterion"]["keyword"]["text"] for r in run_query(CID, f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
WHERE ad_group.id = {BRAND_AG} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED'""")]
    print("READ-BACK Branded keywords:", sorted(kws))
    n = collections.Counter(r["campaign"]["name"] for r in run_query(CID, f"""SELECT campaign.name, campaign_criterion.keyword.text FROM campaign_criterion
WHERE campaign.id IN ({HVAC}, {ELEC}) AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"""))
    print("READ-BACK campaign negatives:", dict(n))
    for camp in (HVAC, ELEC, BRAND):
        print("READ-BACK sitelinks", camp, [r["asset"]["sitelink_asset"]["link_text"] for r in campaign_sitelinks(camp)])
    print("READ-BACK ad-group sitelink links left on stripped ad groups:", len(ag_sitelink_links()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); ap.add_argument("--readback", action="store_true")
    a = ap.parse_args()
    readback() if a.readback else run(validate=not a.apply)
