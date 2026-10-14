"""Zen Air deep dive 2026-09-30, part A2: conversion action config + biddable goals."""
import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"

print("=" * 110)
print("4) CONVERSION ACTIONS CONFIG")
print("=" * 110)
q = """
SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.origin, conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric, conversion_action.counting_type,
       conversion_action.phone_call_duration_seconds
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
"""
for r in run_query(CID, q):
    ca = r["conversion_action"]
    print(f"  {ca.get('id','')} {ca.get('name','')[:40]:40s} type={ca.get('type',''):24s} cat={ca.get('category',''):20s} "
          f"origin={ca.get('origin','')[:16]:16s} prim={ca.get('primary_for_goal')} incl={ca.get('include_in_conversions_metric')} "
          f"count={ca.get('counting_type')} dur={ca.get('phone_call_duration_seconds','')}")

print("\n" + "=" * 110)
print("5) CAMPAIGN CONVERSION GOALS (biddable) on serving campaigns")
print("=" * 110)
q = """
SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin,
       campaign_conversion_goal.biddable
FROM campaign_conversion_goal
WHERE campaign.id IN (23675783172, 24100030790)
"""
for r in run_query(CID, q):
    g = r["campaign_conversion_goal"]
    if g.get("biddable"):
        print(f"  {r['campaign']['name'][:40]:40s} {g['category']:22s} {g['origin']:16s} biddable=True")
