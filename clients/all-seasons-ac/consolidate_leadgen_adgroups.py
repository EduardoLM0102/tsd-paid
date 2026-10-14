#!/usr/bin/env python3
"""Consolidate LeadGen's 22 ad groups down to the ~7 that actually carry
traffic, by URL/theme grouping proposed to and approved by Edu 2026-08-31.

Mechanism: Google Ads has no "merge ad group" operation. A merge here means:
copy each source ad group's ENABLED keyword criteria into the target anchor
ad group (skipping exact text+match_type duplicates already present there),
then flip ad-group status so only the anchor stays live.

Groups:
  AC Install & Replace   <- residential hvac (anchor, stays ENABLED)
    absorbs: commercial hvac, air conditioning replacement, hvac installation,
             air conditioning installation
  Heating & HVAC Repair  <- heating repair (anchor, stays ENABLED)
    absorbs: hvac repair, hvac services, industrial hvac, furnace maintenance,
             queens hvac, hvac contractor, hvac contractor #2
  AC Repair & Contractor <- air conditioning repair (anchor, re-ENABLED --
             it was paused but already has EXCELLENT-rated RSAs live)
    absorbs: air conditioning contractor, air conditioner repair queens
  Furnace                <- furnace repair (anchor, stays ENABLED)
    absorbs: furnace replacement, furnace repair queens

Status changes needed (rest of the source groups were already PAUSED):
  - commercial hvac: ENABLED -> PAUSED (absorbed into residential hvac)
  - furnace replacement: ENABLED -> PAUSED (absorbed into furnace repair)
  - air conditioning repair: PAUSED -> ENABLED (becomes new anchor)

Left untouched: ductless air conditioner installation (separate product
line, cannibalization question still open), All Seasons AC (BRAND) and
HVAC (Lead Gen) dynamic ad group (both structurally different, discussed
separately).
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude", "skills", "google-ads-ratos", "scripts"))

from lib import init_client, run_query

CUSTOMER_ID = "4467722415"
CAMPAIGN_ID = "11803942938"

MERGE_MAP = {
    "115563974075": ["115563974115", "115563973835", "115563974635", "115563974835"],  # -> residential hvac
    "115563974555": ["112010777222", "115563973915", "115563974315", "115563974355", "115563974795", "115563973875", "121605420144"],  # -> heating repair
    "115563974395": ["115563974595", "115563974875"],  # -> air conditioning repair
    "115563973675": ["115563973635", "115563975035"],  # -> furnace repair
}

STATUS_CHANGES = {
    "115563974115": "PAUSED",   # commercial hvac (absorbed)
    "115563973635": "PAUSED",   # furnace replacement (absorbed)
    "115563974395": "ENABLED",  # air conditioning repair (new anchor)
}

with open("/tmp/leadgen_kw_by_group.json") as f:
    by_group = json.load(f)

client = init_client()
gads_service = client.get_service("GoogleAdsService")
criterion_service = client.get_service("AdGroupCriterionService")
ad_group_service = client.get_service("AdGroupService")

match_type_enum = client.enums.KeywordMatchTypeEnum

def fresh_keywords(target_id):
    q = f"""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM keyword_view
    WHERE ad_group.id = {target_id} AND ad_group_criterion.status = 'ENABLED'
    """
    out = set()
    for r in run_query(CUSTOMER_ID, q):
        kw = r["ad_group_criterion"]["keyword"]
        out.add((kw["text"].lower(), kw["match_type"]))
    return out

create_ops = []
plan_summary = []
for target_id, source_ids in MERGE_MAP.items():
    target_name = by_group.get(target_id, {}).get("name", "?")
    existing = fresh_keywords(target_id)
    added_for_target = 0
    for src_id in source_ids:
        src = by_group.get(src_id, {"name": "?", "kws": []})
        for kw in src["kws"]:
            key = (kw["text"].lower(), kw["match_type"])
            if key in existing:
                continue
            existing.add(key)
            added_for_target += 1
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = gads_service.ad_group_path(CUSTOMER_ID, target_id)
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw["text"]
            crit.keyword.match_type = getattr(match_type_enum, kw["match_type"])
            create_ops.append(op)
    plan_summary.append((target_name, target_id, added_for_target))

print("Migration plan:")
for name, tid, n in plan_summary:
    print(f"  -> {name} ({tid}): +{n} new keyword criteria")
print(f"\nTotal create operations: {len(create_ops)}")

# Batch in chunks of 300, with partial_failure so one bad keyword (policy
# violations etc.) doesn't block the rest of the batch.
from google.ads.googleads.errors import GoogleAdsException

CHUNK = 300
created_count = 0
failed = []
for i in range(0, len(create_ops), CHUNK):
    chunk = create_ops[i:i + CHUNK]
    request = client.get_type("MutateAdGroupCriteriaRequest")
    request.customer_id = CUSTOMER_ID
    request.operations.extend(chunk)
    request.partial_failure = True
    resp = criterion_service.mutate_ad_group_criteria(request=request)
    n_ok = sum(1 for r in resp.results if r.resource_name)
    n_fail = len(chunk) - n_ok
    created_count += n_ok
    print(f"  Chunk {i}-{i+len(chunk)}: {n_ok} created, {n_fail} failed")
    if n_fail:
        for j, r in enumerate(resp.results):
            if not r.resource_name:
                op = chunk[j]
                failed.append(op.create.keyword.text)

print(f"\nTotal keyword criteria created: {created_count}")
if failed:
    print(f"Failed texts ({len(failed)}): {failed}")

# Status changes.
ag_ops = []
for gid, status in STATUS_CHANGES.items():
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = gads_service.ad_group_path(CUSTOMER_ID, gid)
    ag.status = getattr(client.enums.AdGroupStatusEnum, status)
    op.update_mask.paths.append("status")
    ag_ops.append(op)

resp = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ag_ops)
print(f"\nApplied {len(resp.results)} ad-group status changes:")
for r in resp.results:
    print(" ", r.resource_name)

# Read-back verification.
print("\n--- Verification ---")
q = f"""
SELECT ad_group.id, ad_group.name, ad_group.status
FROM ad_group
WHERE campaign.id = {CAMPAIGN_ID} AND ad_group.id IN ({",".join(MERGE_MAP.keys())}, {",".join(STATUS_CHANGES.keys())})
"""
for r in run_query(CUSTOMER_ID, q):
    ag = r["ad_group"]
    print(f"  {ag['id']:15s} {ag['status']:10s} {ag['name']}")

q2 = f"""
SELECT ad_group.id, ad_group.name, ad_group_criterion.status
FROM ad_group_criterion
WHERE campaign.id = {CAMPAIGN_ID} AND ad_group_criterion.type = 'KEYWORD' AND ad_group.id IN ({",".join(MERGE_MAP.keys())})
"""
counts = {}
for r in run_query(CUSTOMER_ID, q2):
    ag = r["ad_group"]
    st = r["ad_group_criterion"]["status"]
    key = (ag["id"], ag["name"], st)
    counts[key] = counts.get(key, 0) + 1
print("\nKeyword counts per anchor ad group after merge:")
for (gid, name, st), n in sorted(counts.items()):
    print(f"  {name:30s} {st:10s} {n}")
