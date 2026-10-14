#!/usr/bin/env python3
"""
H4a/H4b/H4c (Edu: execute, 2026-10-08). Account 1051843378 sitelinks.
  H4a  New account-level sitelink "Contact Us" → https://proudpops.com/contact; remove the old account link to the
       txproblemsolvers.com "Contact Us" asset (its redirect drops the click ID and lands on the homepage).
  H4b  Remove the account links of the 3 dead old-domain sitelinks (Air Conditioning Services, Bathroom Plumbing, Heat Pumps).
  H4c  New sitelink "Book a Free Pop-In" → https://proudpops.com/schedule, linked to all 4 Search campaigns.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"; C = f"customers/{CID}"
SEARCH = ["23866999121", "23848895678", "23853484024", "23853361615"]
OLD_DOMAIN = "txproblemsolvers.com"
client = init_client(); E = client.enums


def account_sitelinks():
    return run_query(CID, """SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls, customer_asset.status, customer_asset.resource_name
FROM customer_asset WHERE customer_asset.field_type = 'SITELINK'""")


def plan():
    rows = account_sitelinks()
    old = [r for r in rows if OLD_DOMAIN in ((r["asset"].get("final_urls") or [""])[0]) and str(r["customer_asset"]["status"]) == "ENABLED"]
    print("old-domain ENABLED account sitelinks:", [(r["asset"]["sitelink_asset"]["link_text"], r["asset"]["final_urls"][0]) for r in old])
    contact = [r for r in old if r["asset"]["sitelink_asset"]["link_text"] == "Contact Us"]
    dead = [r for r in old if r["asset"]["sitelink_asset"]["link_text"] in ("Air Conditioning Services", "Bathroom Plumbing", "Heat Pumps")]
    assert len(contact) == 1 and len(dead) == 3, (contact, dead)
    return contact[0], dead


def sitelink(tmp_id, text, url, d1, d2):
    o = client.get_type("MutateOperation"); a = o.asset_operation.create
    a.resource_name = f"{C}/assets/{tmp_id}"; a.final_urls.append(url)
    a.sitelink_asset.link_text = text; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    return o


def run(validate):
    contact, dead = plan()
    ops = []
    # H4a
    ops.append(sitelink(-1, "Contact Us", "https://proudpops.com/contact", "Check we serve your area", "A real person picks up"))
    o = client.get_type("MutateOperation"); ca = o.customer_asset_operation.create
    ca.asset = f"{C}/assets/-1"; ca.field_type = E.AssetFieldTypeEnum.SITELINK; ops.append(o)
    o = client.get_type("MutateOperation"); o.customer_asset_operation.remove = contact["customer_asset"]["resource_name"]; ops.append(o)
    # H4b
    for r in dead:
        o = client.get_type("MutateOperation"); o.customer_asset_operation.remove = r["customer_asset"]["resource_name"]; ops.append(o)
    # H4c
    ops.append(sitelink(-2, "Book a Free Pop-In", "https://proudpops.com/schedule", "Free visit, no obligation", "Written price before any work"))
    for camp in SEARCH:
        o = client.get_type("MutateOperation"); cpa = o.campaign_asset_operation.create
        cpa.campaign = f"{C}/campaigns/{camp}"; cpa.asset = f"{C}/assets/-2"; cpa.field_type = E.AssetFieldTypeEnum.SITELINK; ops.append(o)
    for d in ("Check we serve your area", "A real person picks up", "Free visit, no obligation", "Written price before any work"):
        assert len(d) <= 35, d
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK" if validate else "APPLIED") + f": {len(ops)} ops (H4a 3, H4b 3, H4c 5)")
    if not validate:
        print("READ-BACK account sitelinks (ENABLED):")
        for r in account_sitelinks():
            if str(r["customer_asset"]["status"]) == "ENABLED":
                print("   ", r["asset"]["sitelink_asset"]["link_text"], "->", (r["asset"].get("final_urls") or ["?"])[0])
        print("READ-BACK 'Book a Free Pop-In' campaign links:")
        for r in run_query(CID, """SELECT campaign.id, campaign.name, campaign.status, asset.sitelink_asset.link_text, campaign_asset.status FROM campaign_asset
WHERE campaign_asset.field_type = 'SITELINK' AND campaign.status = 'ENABLED'"""):
            if r["asset"]["sitelink_asset"]["link_text"] == "Book a Free Pop-In":
                print("   ", r["campaign"]["name"], r["campaign_asset"]["status"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    run(validate=not a.apply)
