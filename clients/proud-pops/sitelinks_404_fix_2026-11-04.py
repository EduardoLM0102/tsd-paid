# APPLIED LIVE 2026-11-04, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Fix the sitelinks, yes").
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Proud Pops (1051843378), 2026-11-04: 2 sitelinks on Search Electrical point to the dead old domain (404).
   'Our Story'  120042497724  txproblemsolvers.com/about/our-story/     → https://proudpops.com/about   ("Pop's Promise" page)
   'Contact Us' 185822702561  txproblemsolvers.com/contact/contact-us/  → https://proudpops.com/contact
Updates the asset final_urls in place (every link using these assets gets the fix). Aborts if the current URL isn't the old domain."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "1051843378"
FIX = {"120042497724": ("Our Story", "https://proudpops.com/about"), "185822702561": ("Contact Us", "https://proudpops.com/contact")}
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = f"SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls FROM asset WHERE asset.id IN ({','.join(FIX)})"

ops = []
for r in q(SEL):
    aid, txt, urls = str(r.asset.id), r.asset.sitelink_asset.link_text, list(r.asset.final_urls)
    print(f"before: {aid} '{txt}' {urls}")
    if txt != FIX[aid][0] or not urls or "txproblemsolvers.com" not in urls[0]: sys.exit(f"ABORT: {aid} not as expected")
    op = client.get_type("AssetOperation"); op.update.resource_name = ga.asset_path(CID, aid)
    op.update.final_urls.append(FIX[aid][1]); op.update_mask.paths.append("final_urls"); ops.append(op)
if len(ops) != 2: sys.exit("ABORT: expected 2 assets")
client.get_service("AssetService").mutate_assets(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print("2 sitelinks", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")
if APPLY:
    for r in q(SEL): print(f"read-back: {r.asset.id} '{r.asset.sitelink_asset.link_text}' {list(r.asset.final_urls)}")
