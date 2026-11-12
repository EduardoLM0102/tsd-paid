#!/usr/bin/env python3
"""Zen Air 2026-10-23 (read-only): NB campaign geo setting + negatives, before the LP rebuild."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, NB = "4360840956", "24100030790"
for r in run_query(CID, f"""SELECT campaign.geo_target_type_setting.positive_geo_target_type, campaign.ad_schedule_count
  FROM campaign WHERE campaign.id = {NB}""") if False else run_query(CID, f"""SELECT campaign.geo_target_type_setting.positive_geo_target_type
  FROM campaign WHERE campaign.id = {NB}"""):
    print("geo type:", r["campaign"]["geo_target_type_setting"])
locs = run_query(CID, f"""SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant,
  campaign_criterion.proximity.radius, campaign_criterion.ad_schedule.day_of_week
  FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type IN ('LOCATION','PROXIMITY','AD_SCHEDULE')""")
print("geo/schedule criteria:", len(locs))
for r in locs[:40]: print(" ", r["campaign_criterion"])
negs = run_query(CID, f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
  FROM campaign_criterion WHERE campaign.id = {NB} AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE""")
print("campaign negatives:", len(negs))
print(" ", "; ".join(f'{n["campaign_criterion"]["keyword"]["text"]}[{n["campaign_criterion"]["keyword"]["match_type"][0]}]' for n in negs))
sh = run_query(CID, f"""SELECT shared_set.name, shared_set.member_count FROM campaign_shared_set WHERE campaign.id = {NB} AND campaign_shared_set.status = 'ENABLED'""")
print("shared sets:", [(s["shared_set"]["name"], s["shared_set"].get("member_count")) for s in sh])
