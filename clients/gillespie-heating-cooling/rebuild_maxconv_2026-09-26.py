#!/usr/bin/env python3
"""Rebuild Gillespie's two Search campaigns from scratch on Maximize Conversions.

2026-09-26. Replicates the live structure captured in
google-ads-snapshot_2026-09-26.md (raw data in google-ads-snapshot_2026-09-26_raw/):
same ad groups, keywords, RSA copy, final URLs, negatives, geo, language, and the
12 campaign-level assets, on new campaigns with Maximize Conversions (no target).

Everything is created PAUSED (create.py's rule) and nothing existing is touched.
Resumable: every created object is recorded in STATE, re-running skips finished steps.

Budgets: create.py --budget is CENTAVOS ($65/day = 6500). Same daily budgets as the
old campaigns ($65 non-branded, $1 branded), so total account budget is unchanged.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "google-ads-ratos", "scripts")
sys.path.insert(0, SCRIPTS)

RAW = os.path.join(HERE, "google-ads-snapshot_2026-09-26_raw")
STATE_PATH = os.environ.get("REBUILD_STATE", os.path.join(HERE, "rebuild_maxconv_state.json"))
CID = "7410489772"

CAMPAIGNS = {
    "NB": {"name": "TSD_09.26_Search_NonBranded_Evergreen", "budget_centavos": 6500, "old_name": "TSD_08.18_Search_NonBranded_Evergreen"},
    "B": {"name": "TSD_09.26_Search_Branded_Evergreen", "budget_centavos": 100, "old_name": "TSD_08.18_Search_Branded_Evergreen"},
}
AD_GROUPS = {
    "NB": ["HVAC-General-Company", "Furnace-Heating-Repair", "AC-Repair-Install", "Heat-Pump-Services"],
    "B": ["Brand-Terms"],
}
GEO_IDS = [1017681, 1017704, 1017733, 1017738, 1017751, 1017759, 1017760, 1017768, 1017832, 1017851, 1023626]
ASSETS = [  # the 12 campaign-level assets that were live on both old campaigns
    ("409474614430", "SITELINK"), ("409474971790", "SITELINK"), ("409474971793", "SITELINK"), ("409474992694", "SITELINK"),
    ("409372567529", "CALLOUT"), ("409372568783", "CALLOUT"), ("409474919764", "CALLOUT"), ("409474971418", "CALLOUT"),
    ("409474971421", "CALLOUT"), ("409549613946", "CALLOUT"), ("409549613949", "CALLOUT"), ("409549623915", "CALLOUT"),
]

state = json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {}


def save():
    json.dump(state, open(STATE_PATH, "w"), indent=1)


def create(*args):
    """Run tsd.sh create.py <args>, return the parsed JSON it prints."""
    p = subprocess.run(["./tsd.sh", "create.py", *args], cwd=SCRIPTS, capture_output=True, text=True)
    out = p.stdout
    i = out.find("{")
    if p.returncode != 0 or i < 0:
        raise RuntimeError(f"create.py {args[0]} failed rc={p.returncode}\nSTDOUT:{out[-800:]}\nSTDERR:{p.stderr[-800:]}")
    return json.JSONDecoder().raw_decode(out[i:])[0]


def step(key, fn):
    if key in state:
        return state[key]
    state[key] = fn()
    save()
    return state[key]


def tail_id(res):
    return res["resource_name"].split("/")[-1]


ads = json.load(open(os.path.join(RAW, "ads.json")))
kws = json.load(open(os.path.join(RAW, "keywords.json")))
negs = json.load(open(os.path.join(RAW, "negative_keywords.json")))

# ---- 1. campaigns (PAUSED, Maximize Conversions, Google Search only) -------------------------
for k, c in CAMPAIGNS.items():
    step(f"campaign:{k}", lambda c=c: tail_id(create(
        "campaign", "--customer-id", CID, "--name", c["name"], "--type", "SEARCH",
        "--budget", str(c["budget_centavos"]), "--maximize-conversions")))
    print("campaign", k, state[f"campaign:{k}"], flush=True)

# ---- 2. direct mutates create.py doesn't expose: PRESENCE geo type, language, asset links -----
from lib import init_client  # noqa: E402
from google.protobuf import field_mask_pb2  # noqa: E402

client = init_client()
camp_svc = client.get_service("CampaignService")
crit_svc = client.get_service("CampaignCriterionService")
asset_svc = client.get_service("CampaignAssetService")

for k in CAMPAIGNS:
    cid = state[f"campaign:{k}"]
    path = camp_svc.campaign_path(CID, cid)

    def presence():
        op = client.get_type("CampaignOperation")
        op.update.resource_name = path
        op.update.geo_target_type_setting.positive_geo_target_type = client.enums.PositiveGeoTargetTypeEnum.PRESENCE
        op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["geo_target_type_setting.positive_geo_target_type"]))
        camp_svc.mutate_campaigns(customer_id=CID, operations=[op])
        return "PRESENCE"

    def language():
        op = client.get_type("CampaignCriterionOperation")
        op.create.campaign = path
        op.create.language.language_constant = "languageConstants/1000"
        crit_svc.mutate_campaign_criteria(customer_id=CID, operations=[op])
        return "en"

    def assets():
        ops = []
        for aid, ftype in ASSETS:
            op = client.get_type("CampaignAssetOperation")
            op.create.campaign = path
            op.create.asset = f"customers/{CID}/assets/{aid}"
            op.create.field_type = getattr(client.enums.AssetFieldTypeEnum, ftype)
            ops.append(op)
        asset_svc.mutate_campaign_assets(customer_id=CID, operations=ops)
        return len(ops)

    step(f"presence:{k}", presence)
    step(f"language:{k}", language)
    step(f"assets:{k}", assets)
    print("presence/language/assets", k, flush=True)

# ---- 3. locations (11 cities) -----------------------------------------------------------------
for k in CAMPAIGNS:
    for gid in GEO_IDS:
        step(f"loc:{k}:{gid}", lambda k=k, gid=gid: create(
            "location", "--customer-id", CID, "--campaign-id", state[f"campaign:{k}"], "--geo-target-id", str(gid)).get("status", "ok"))
    print("locations", k, flush=True)

# ---- 4. ad groups, keywords, RSAs -------------------------------------------------------------
for k, groups in AD_GROUPS.items():
    for g in groups:
        agid = step(f"adgroup:{k}:{g}", lambda k=k, g=g: tail_id(create(
            "ad-group", "--customer-id", CID, "--campaign-id", state[f"campaign:{k}"], "--name", g)))
        print("ad group", g, agid, flush=True)

        for r in [r for r in kws if r["ad_group"]["name"] == g]:
            kw = r["ad_group_criterion"]["keyword"]
            step(f"kw:{g}:{kw['match_type']}:{kw['text']}", lambda kw=kw, agid=agid: create(
                "keyword", "--customer-id", CID, "--ad-group-id", agid, "--text", kw["text"], "--match-type", kw["match_type"]).get("status", "ok"))

        ad = [a for a in ads if a["ad_group"]["name"] == g][0]["ad_group_ad"]["ad"]
        rsa = ad["responsive_search_ad"]
        step(f"rsa:{g}", lambda ad=ad, rsa=rsa, agid=agid: tail_id(create(
            "rsa", "--customer-id", CID, "--ad-group-id", agid,
            "--headlines", "|".join(h["text"] for h in rsa["headlines"]),
            "--descriptions", "|".join(d["text"] for d in rsa["descriptions"]),
            "--url", ad["final_urls"][0])))
        print("keywords + rsa", g, flush=True)

# ---- 5. negatives (live list is campaign-level on Non-Branded only) ---------------------------
for r in negs:
    kw = r["campaign_criterion"]["keyword"]
    step(f"neg:NB:{kw['match_type']}:{kw['text']}", lambda kw=kw: create(
        "negative", "--customer-id", CID, "--campaign-id", state["campaign:NB"], "--text", kw["text"], "--match-type", kw["match_type"]).get("status", "ok"))
print("negatives done", flush=True)
print("BUILD COMPLETE")
