#!/usr/bin/env python3
"""Cool Hand callout fix (Edu: "execute on 1", 2026-10-08). Site check 2026-10-08:
  - "Family-Owned Since 2015" is not on coolhandelectric.com anymore → replaced by "Family Owned and Local" on HVAC,
    Electrical and Branded (site: "Family Owned", "family-owned business").
  - "$37 Safety Inspection" is an electrical offer but ran on HVAC → removed from HVAC only (stays on Electrical/Branded),
    replaced by "Easy Payment Plans" (site nav + AC install FAQ: "easy payment plans").
Default validate-only; --apply writes; read-back after."""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "9865206319"; C = f"customers/{CID}"
HVAC, ELEC, BRAND = "24118511502", "24123995882", "24123995948"
client = init_client(); E = client.enums


def links():
    return run_query(CID, f"""SELECT campaign.id, campaign.name, asset.callout_asset.callout_text, campaign_asset.resource_name FROM campaign_asset
WHERE campaign.id IN ({HVAC}, {ELEC}, {BRAND}) AND campaign_asset.field_type = 'CALLOUT' AND campaign_asset.status = 'ENABLED'""")


def run(validate):
    rows = links()
    remove = [r for r in rows if r["asset"]["callout_asset"]["callout_text"] == "Family-Owned Since 2015"]
    remove += [r for r in rows if r["asset"]["callout_asset"]["callout_text"] == "$37 Safety Inspection" and r["campaign"]["id"] == HVAC]
    print("removing:", [(r["campaign"]["name"], r["asset"]["callout_asset"]["callout_text"]) for r in remove])
    assert len(remove) == 4, len(remove)
    ops = []
    def op(): o = client.get_type("MutateOperation"); ops.append(o); return o
    new = {"-1": ("Family Owned and Local", [HVAC, ELEC, BRAND]), "-2": ("Easy Payment Plans", [HVAC])}
    for tmp, (text, camps) in new.items():
        assert len(text) <= 25
        o = op(); a = o.asset_operation.create; a.resource_name = f"{C}/assets/{tmp}"; a.callout_asset.callout_text = text
        for camp in camps:
            o = op(); ca = o.campaign_asset_operation.create; ca.campaign = f"{C}/campaigns/{camp}"
            ca.asset = f"{C}/assets/{tmp}"; ca.field_type = E.AssetFieldTypeEnum.CALLOUT
    for r in remove:
        o = op(); o.campaign_asset_operation.remove = r["campaign_asset"]["resource_name"]
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK (nothing written)" if validate else "APPLIED") + f": {len(ops)} ops")
    if not validate:
        by = {}
        for r in links(): by.setdefault(r["campaign"]["name"], []).append(r["asset"]["callout_asset"]["callout_text"])
        for k, v in by.items(): print("READ-BACK", k, sorted(v))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    run(validate=not a.apply)
