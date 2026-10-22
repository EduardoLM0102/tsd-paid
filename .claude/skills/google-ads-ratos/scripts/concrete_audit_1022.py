import sys
sys.path.insert(0, ".")
from lib import run_query

def q(cid, gaql, label):
    print("\n" + "=" * 90 + f"\n{label}  [{cid}]\n" + "=" * 90)
    try:
        rows = run_query(cid, gaql)
        for r in rows:
            print(r)
        if not rows:
            print("(no rows)")
    except Exception as e:
        print(f"ERROR: {e}")

for CID in ["9215192296", "2898153501"]:
    q(CID, """SELECT customer.descriptive_name, customer.currency_code, customer.time_zone, customer.status,
              customer.auto_tagging_enabled FROM customer""", "ACCOUNT")
    q(CID, """SELECT billing_setup.id, billing_setup.status, billing_setup.payments_account,
              billing_setup.payments_account_info.payments_account_name,
              billing_setup.payments_account_info.payments_profile_name FROM billing_setup""", "BILLING")
    q(CID, """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status,
              campaign.advertising_channel_type, campaign.bidding_strategy_type,
              campaign_budget.amount_micros
              FROM campaign WHERE campaign.status != 'REMOVED'""", "CAMPAIGNS")
    q(CID, """SELECT campaign.name, campaign.status, segments.date, metrics.cost_micros, metrics.clicks,
              metrics.impressions, metrics.conversions FROM campaign
              WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0""", "SPEND BY DAY, LAST 30")
    q(CID, """SELECT conversion_action.id, conversion_action.name, conversion_action.type,
              conversion_action.category, conversion_action.status, conversion_action.primary_for_goal,
              conversion_action.include_in_conversions_metric, conversion_action.phone_call_duration_seconds
              FROM conversion_action WHERE conversion_action.status != 'REMOVED'""", "CONVERSION ACTIONS")
    q(CID, """SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions
              FROM customer WHERE segments.date DURING LAST_30_DAYS""", "CONVERSIONS BY ACTION, LAST 30")

CID = "9215192296"
q(CID, """SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
          ad_group_criterion.keyword.match_type, ad_group_criterion.status
          FROM keyword_view WHERE campaign.status != 'REMOVED' AND ad_group_criterion.status != 'REMOVED'""", "KEYWORDS")
q(CID, """SELECT campaign.name, campaign.ai_max_setting.enable_ai_max FROM campaign
          WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.status != 'REMOVED'""", "AI MAX")
q(CID, """SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.negative
          FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION' AND campaign.status != 'REMOVED'""", "GEO")
q(CID, """SELECT shared_set.name, shared_set.type, shared_set.member_count FROM shared_set
          WHERE shared_set.status = 'ENABLED'""", "SHARED NEGATIVE LISTS")
q(CID, """SELECT asset.call_asset.phone_number, asset.type, asset.final_urls FROM asset
          WHERE asset.type IN ('CALL','SITELINK')""", "CALL + SITELINK ASSETS")
