#!/usr/bin/env python3
"""Zen Air 2026-10-23 (read-only): non-branded campaign state before pointing it at the new heating/AC LPs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query

CID = "4360840956"
print("== campaigns (not removed)")
for r in run_query(CID, """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status,
  campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign_budget.amount_micros,
  campaign.target_spend.cpc_bid_ceiling_micros, campaign.network_settings.target_search_network
  FROM campaign WHERE campaign.status != 'REMOVED'"""):
    c = r["campaign"]
    print(" ", c["id"], c["status"], c.get("primary_status"), c["advertising_channel_type"], c.get("bidding_strategy_type"),
          "budget", int(r["campaign_budget"].get("amount_micros", 0)) / 1e6,
          "ceiling", int(c.get("target_spend", {}).get("cpc_bid_ceiling_micros", 0) or 0) / 1e6,
          "partners", c.get("network_settings", {}).get("target_search_network"), "|", c["name"])

NB = "24100030790"
print("== NB ad groups")
for r in run_query(CID, f"""SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group
  WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'"""):
    a = r["ad_group"]; print(" ", a["id"], a["status"], a["name"])

print("== NB keywords (positive)")
for r in run_query(CID, f"""SELECT ad_group.name, ad_group_criterion.criterion_id, ad_group_criterion.status,
  ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.final_urls
  FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'"""):
    k = r["ad_group_criterion"]
    print(" ", r["ad_group"]["name"], "|", k["status"], k["keyword"]["match_type"], k["keyword"]["text"], k.get("final_urls", ""))

print("== NB ads")
for r in run_query(CID, f"""SELECT ad_group.name, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.type,
  ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status,
  ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2
  FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.status != 'REMOVED'"""):
    ad = r["ad_group_ad"]["ad"]; rsa = ad.get("responsive_search_ad", {})
    print(" ", r["ad_group"]["name"], "|", r["ad_group_ad"]["status"], ad["id"], ad.get("type"),
          r["ad_group_ad"].get("policy_summary", {}).get("approval_status"), ad.get("final_urls"),
          "paths", rsa.get("path1"), rsa.get("path2"))
    print("     H:", " / ".join(h["text"] for h in rsa.get("headlines", [])))
