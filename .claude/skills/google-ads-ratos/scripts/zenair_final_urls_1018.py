#!/usr/bin/env python3
"""Zen Air 2026-10-18 (read-only): final URLs of live ads, PMax asset groups and sitelinks."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query

CID = "4360840956"
print("== campaigns")
for r in run_query(CID, """SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
  campaign.primary_status FROM campaign WHERE campaign.status != 'REMOVED'"""):
    c = r["campaign"]; print(" ", c["id"], c["status"], c.get("primary_status"), c["advertising_channel_type"], c["name"])

print("== enabled ads in enabled ad groups / campaigns")
for r in run_query(CID, """SELECT campaign.name, campaign.status, ad_group.name, ad_group.status, ad_group_ad.status,
  ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status,
  metrics.impressions, metrics.clicks
  FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND segments.date DURING LAST_7_DAYS"""):
    print(" ", r["campaign"]["status"], "|", r["campaign"]["name"], "|", r["ad_group"]["status"], r["ad_group"]["name"],
          "| ad", r["ad_group_ad"]["ad"]["id"], r["ad_group_ad"]["ad"].get("type"), r["ad_group_ad"]["ad"].get("final_urls"),
          "| impr7d", r.get("metrics", {}).get("impressions", 0))

print("== enabled ads (no date segment, to catch 0-impression ones)")
for r in run_query(CID, """SELECT campaign.name, campaign.status, ad_group.name, ad_group.status, ad_group_ad.ad.id,
  ad_group_ad.ad.final_urls FROM ad_group_ad
  WHERE ad_group_ad.status = 'ENABLED' AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'"""):
    print(" ", r["campaign"]["name"], "|", r["ad_group"]["name"], "| ad", r["ad_group_ad"]["ad"]["id"], r["ad_group_ad"]["ad"].get("final_urls"))

print("== PMax asset groups")
for r in run_query(CID, """SELECT campaign.name, campaign.status, asset_group.name, asset_group.status, asset_group.final_urls
  FROM asset_group WHERE asset_group.status != 'REMOVED'"""):
    print(" ", r["campaign"]["status"], r["campaign"]["name"], "|", r["asset_group"]["status"], r["asset_group"]["name"], r["asset_group"].get("final_urls"))

print("== sitelink assets attached (campaign / account level)")
for r in run_query(CID, """SELECT campaign.name, campaign.status, campaign_asset.status, asset.sitelink_asset.link_text, asset.final_urls
  FROM campaign_asset WHERE campaign_asset.field_type = 'SITELINK' AND campaign_asset.status = 'ENABLED'"""):
    print(" ", r["campaign"]["status"], r["campaign"]["name"], "|", r["asset"].get("sitelink_asset", {}).get("link_text"), r["asset"].get("final_urls"))
for r in run_query(CID, """SELECT customer_asset.status, asset.sitelink_asset.link_text, asset.final_urls
  FROM customer_asset WHERE customer_asset.field_type = 'SITELINK' AND customer_asset.status = 'ENABLED'"""):
    print("  ACCOUNT |", r["asset"].get("sitelink_asset", {}).get("link_text"), r["asset"].get("final_urls"))

print("== landing pages with clicks, last 7 days")
for r in run_query(CID, """SELECT landing_page_view.unexpanded_final_url, metrics.clicks, metrics.impressions
  FROM landing_page_view WHERE segments.date DURING LAST_7_DAYS"""):
    print(" ", r["landing_page_view"]["unexpanded_final_url"], r["metrics"].get("clicks", 0), r["metrics"].get("impressions", 0))
