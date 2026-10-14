#!/usr/bin/env python3
"""
G1a/G1b/G1c (Edu: execute, 2026-10-08). Budgets unchanged.
  G1a  Branded 23853361615 → all cities in the in-account LSA service area (client-declared, 47).
  G1b  Search HVAC 23848895678 + Search Plumbing 23853484024 → 20-city core metro (all from the client's LSA lists).
  G1c  Search HVAC + PMax Electrical 23866982084 → location option PRESENCE (people in / regularly in the area).
Geo constants are copied from the LSA campaigns' own criteria (exact match to the client's service area).
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"; C = f"customers/{CID}"
BRANDED, HVAC, PLUMB, PMAX_ELEC = "23853361615", "23848895678", "23853484024", "23866982084"
CORE = ["San Antonio", "Alamo Heights", "Castle Hills", "Leon Valley", "Kirby", "Windcrest", "Live Oak", "Universal City", "Converse",
        "Selma", "Schertz", "Cibolo", "Garden Ridge", "Timberwood Park", "New Braunfels", "Helotes", "Fair Oaks Ranch", "Boerne",
        "Bulverde", "Spring Branch"]
client = init_client(); E = client.enums


def lsa_geos(cid):
    rns = [r["campaign_criterion"]["location"]["geo_target_constant"] for r in run_query(cid, """SELECT campaign.id, campaign_criterion.location.geo_target_constant,
campaign_criterion.negative FROM campaign_criterion WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES' AND campaign.status = 'ENABLED'
AND campaign_criterion.type = 'LOCATION'""") if not r["campaign_criterion"].get("negative")]
    out = {}
    ids = [x.split("/")[-1] for x in rns]
    for r in run_query(CID, f"SELECT geo_target_constant.resource_name, geo_target_constant.name, geo_target_constant.canonical_name FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"):
        g = r["geo_target_constant"]; out[g["name"]] = (g["resource_name"], g["canonical_name"])
    return out


def current(camp):
    return {r["campaign_criterion"]["location"]["geo_target_constant"] for r in run_query(CID, f"""SELECT campaign.id, campaign_criterion.location.geo_target_constant
FROM campaign_criterion WHERE campaign.id = {camp} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE""")}


def run(validate):
    in_account = lsa_geos(CID)
    all_lsa = dict(in_account); all_lsa.update(lsa_geos("7261668241")); all_lsa.update(lsa_geos("6621969129"))
    for n, (rn, canon) in sorted(all_lsa.items()):
        assert canon.endswith("Texas,United States"), canon
    missing = [c for c in CORE if c not in all_lsa]
    assert not missing, f"core cities not in LSA lists: {missing}"
    plan = {BRANDED: sorted(in_account), HVAC: CORE, PLUMB: CORE}
    ops = []; summary = {}
    for camp, cities in plan.items():
        have = current(camp)
        add = [c for c in cities if all_lsa[c][0] not in have]
        summary[camp] = (len(have), len(add))
        for c in add:
            o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
            cc.campaign = f"{C}/campaigns/{camp}"; cc.location.geo_target_constant = all_lsa[c][0]; ops.append(o)
    for camp in (HVAC, PMAX_ELEC):
        o = client.get_type("MutateOperation"); u = o.campaign_operation.update
        u.resource_name = f"{C}/campaigns/{camp}"
        u.geo_target_type_setting.positive_geo_target_type = E.PositiveGeoTargetTypeEnum.PRESENCE
        o.campaign_operation.update_mask.paths.append("geo_target_type_setting.positive_geo_target_type"); ops.append(o)
    print("plan (existing → adding):", {k: v for k, v in summary.items()}, "| + PRESENCE on HVAC + PMax Electrical")
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK" if validate else "APPLIED") + f": {len(ops)} ops")
    if not validate:
        for camp, label in ((BRANDED, "Branded"), (HVAC, "Search HVAC"), (PLUMB, "Search Plumbing")):
            print(f"READ-BACK {label}: {len(current(camp))} location targets")
        for r in run_query(CID, f"SELECT campaign.name, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id IN ({HVAC}, {PMAX_ELEC}, {BRANDED}, {PLUMB})"):
            print("READ-BACK mode:", r["campaign"]["name"], r["campaign"].get("geo_target_type_setting", {}).get("positive_geo_target_type"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    run(validate=not a.apply)
