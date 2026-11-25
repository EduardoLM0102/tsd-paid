# APPLIED LIVE 2026-11-20 23:27 UTC (Gui via Claude, Edu's go). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file> [--apply]   (validate-only without --apply)
"""Proud Pops (1051843378), 2026-11-20, Edu's go on the 11-20 AT read ("pode trocar o sitelink / pode pausar mas coloca isso no log").
1. 'See Our Pricing' sitelink 360873861063 (/pricing) OFF Electrical 23866999121 + Plumbing 23853484024
   (14d: Elec $4,045 / 155 clk / 13 conv, Plumbing $1,466 / 97 / 0). Kept on Branded (9 conv / $511) and HVAC.
   Replaced by 2 NEW advertiser sitelinks (the account's service sitelinks are all AUTOMATICALLY_CREATED, can't be linked;
   both URLs are in sitemap-services.xml; description claims copied from the approved RSAs in these campaigns):
     Electrical -> 'Electrical Repair' (/services/electrical/repair)
     Plumbing   -> 'Drain Cleaning'    (/services/plumbing/drain-cleaning)
2. PAUSE Elec AG2_Electrical_Services RSA 827482059113 (14d $549 / 0 conv); 809490621054 ($785 / 5) stays ENABLED.
NOT done: EXACT [electrician] neg (not confirmed), Plumbing schedule/pause (Edu: hold).
Rollback: remove the 2 new campaign_assets (asset ids printed on apply), re-link 360873861063 on both campaigns, set 827482059113 ENABLED.
At the new-site DNS switch: 200-check these sitelink URLs (fu-178)."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "1051843378"
ELEC, PLUMB = "23866999121", "23853484024"
PRICING = "360873861063"
NEW_SL = {ELEC: ("Electrical Repair", "Breakers, wiring and outlets", "Written price before any work", "https://proudpops.com/services/electrical/repair"),
          PLUMB: ("Drain Cleaning", "Clogs, slow drains and backups", "Written price before any work", "https://proudpops.com/services/plumbing/drain-cleaning")}
PAUSE_AD, KEEP_AD = "827482059113", "809490621054"
APPLY = "--apply" in sys.argv; VO = not APPLY
client = init_client(); ga = client.get_service("GoogleAdsService"); E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))

def links(camp):
    return {r.asset.id: (r.campaign_asset.resource_name, r.campaign_asset.status.name) for r in q(
        f"SELECT campaign.id, campaign.status, asset.id, campaign_asset.resource_name, campaign_asset.status FROM campaign_asset "
        f"WHERE campaign.id = {camp} AND campaign_asset.field_type = 'SITELINK' AND campaign_asset.status != 'REMOVED'")}

ops, tmp = [], -1
for camp, (lt, d1, d2, url) in NEW_SL.items():
    assert len(lt) <= 25 and len(d1) <= 35 and len(d2) <= 35, (lt, d1, d2)
    cur = links(camp)
    print(camp, "current sitelinks:", {k: v[1] for k, v in cur.items()})
    if int(PRICING) in cur:
        m = client.get_type("MutateOperation"); m.campaign_asset_operation.remove = cur[int(PRICING)][0]; ops.append(m)
    arn = ga.asset_path(CID, tmp); tmp -= 1
    m = client.get_type("MutateOperation"); a = m.asset_operation.create
    a.resource_name = arn; a.sitelink_asset.link_text = lt; a.sitelink_asset.description1 = d1; a.sitelink_asset.description2 = d2
    a.final_urls.append(url); ops.append(m)
    m = client.get_type("MutateOperation"); c = m.campaign_asset_operation.create
    c.campaign = ga.campaign_path(CID, camp); c.asset = arn; c.field_type = E.AssetFieldTypeEnum.SITELINK; ops.append(m)
if ops:
    r = ga.mutate(request={"customer_id": CID, "mutate_operations": ops, "validate_only": VO})
    print(f"  ok  {len(ops)} sitelink ops", "APPLIED" if APPLY else "(validate_only)")
    if APPLY:
        for x in r.mutate_operation_responses:
            if x.asset_result.resource_name: print("   new asset", x.asset_result.resource_name)

ads = {r.ad_group_ad.ad.id: (r.ad_group_ad.resource_name, r.ad_group_ad.status.name) for r in q(
    f"SELECT ad_group_ad.ad.id, ad_group_ad.resource_name, ad_group_ad.status FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({PAUSE_AD},{KEEP_AD})")}
print("ads:", {k: v[1] for k, v in ads.items()})
if ads.get(int(KEEP_AD), (None, None))[1] != "ENABLED": sys.exit("ABORT: 809490621054 not ENABLED, pausing would leave AG2 thin")
if ads[int(PAUSE_AD)][1] == "ENABLED":
    op = client.get_type("AdGroupAdOperation"); op.update.resource_name = ads[int(PAUSE_AD)][0]
    op.update.status = E.AdGroupAdStatusEnum.PAUSED; op.update_mask.paths.append("status")
    client.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CID, "operations": [op], "validate_only": VO})
    print("  ok  pause RSA", PAUSE_AD, "APPLIED" if APPLY else "(validate_only)")

if APPLY:
    for camp in NEW_SL: print("read-back", camp, {k: v[1] for k, v in links(camp).items()})
    for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({PAUSE_AD},{KEEP_AD})"):
        print("  ad", r.ad_group_ad.ad.id, r.ad_group_ad.status.name)
