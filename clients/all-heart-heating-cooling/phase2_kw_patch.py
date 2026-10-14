"""All Heart — Phase 2 PRE-CUTOVER KEYWORD PATCH (2026-07-13).

WHY: the 5 staged themed ad groups are PHRASE/EXACT only (42 kw). The old mega ad group's
non-brand conversions come mostly from BROAD keywords that the new set does NOT cover.
Cross-check (90d, ad group 193307267686) found ~23 of 57.2 non-brand conversions (~40%)
would lose keyword coverage at cutover. This patch re-homes those proven converters into
the matching themed ad group BEFORE the cutover runs.

Run dry first (DRY_RUN=True), then set False.
"""
import os
import sys
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client, run_query

DRY_RUN = False   # executed 2026-07-13

CID = "9205826499"

# ad_group_id -> [(keyword_text, match_type), ...]
# each carries the 90d evidence from the mega ad group that justifies preserving it
PATCH = {
    "198469621179": [  # HVAC Service
        ("air conditioning contractor",       "PHRASE"),  # covers 'air conditioning contractors ca' — 8.5 conv, $32 CPL
        ("hvac repair",                       "PHRASE"),  # covers 'hvac repair lancaster'          — 1.0 conv, $55 CPL
        ("air conditioning local",            "EXACT"),   # 2.3 conv, $38 CPL
        ("ac and heating service and repair", "EXACT"),   # 4.0 conv, $48 CPL
    ],
    "203964394691": [  # Heating & Furnace
        ("heating and cooling repair",        "PHRASE"),  # covers 'home heating and cooling repair' — 3.0 conv, $32 CPL
    ],
    "198469621619": [  # Plumbing
        ("local plumbing companies",          "EXACT"),   # 2.0 conv, $16 CPL  (best non-brand CPL in the account)
        ("tankless water heater",             "PHRASE"),  # covers 'plumbing tankless water heater' — 2.0 conv, $17 CPL
    ],
}

client = init_client()
agcsvc = client.get_service("AdGroupCriterionService")
ga = client.get_service("GoogleAdsService")

print(("DRY RUN — " if DRY_RUN else "EXECUTING — ") + "Phase 2 keyword patch\n")

ops = []
for agid, kws in PATCH.items():
    name = run_query(CID, f"SELECT ad_group.name FROM ad_group WHERE ad_group.id = {agid}")[0]["ad_group"]["name"]
    print(f"{name}  (ad_group {agid})")
    for text, match in kws:
        op = client.get_type("AdGroupCriterionOperation")
        c = op.create
        c.ad_group = ga.ad_group_path(CID, agid)
        c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = text
        c.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match)
        ops.append(op)
        print(f"    + {text}  [{match}]")

print(f"\n{len(ops)} keywords to add")
if not DRY_RUN:
    resp = agcsvc.mutate_ad_group_criteria(customer_id=CID, operations=ops)
    print(f"ADDED {len(resp.results)} keywords:")
    for r in resp.results:
        print(f"    {r.resource_name}")
print("DONE." + ("  (dry run — nothing changed)" if DRY_RUN else ""))
