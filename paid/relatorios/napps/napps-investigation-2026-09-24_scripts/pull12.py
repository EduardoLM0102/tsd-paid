from h import *
q = """
SELECT campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type,
       campaign.maximize_conversions.target_cpa_micros, campaign.advertising_channel_type
FROM campaign WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
"""
for r in run_query(CID,q): print(json.dumps(r, default=str))
q = """
SELECT asset_group.name, asset_group.status, asset_group.primary_status, asset_group.primary_status_reasons, asset_group.ad_strength, campaign.name
FROM asset_group
"""
for r in run_query(CID,q): print(json.dumps(r, default=str))
for q in ["SELECT customer.status, customer.descriptive_name, customer.time_zone, customer.currency_code, customer.manager FROM customer",
          "SELECT billing_setup.status, billing_setup.start_date_time, billing_setup.end_date_time FROM billing_setup",
          "SELECT account_budget.status, account_budget.approved_spending_limit_micros, account_budget.amount_served_micros, account_budget.approved_start_date_time, account_budget.approved_end_date_time, account_budget.total_adjustments_micros FROM account_budget"]:
    try:
        for r in run_query(CID,q): print(json.dumps(r, default=str))
    except Exception as e: print("ERR", str(e)[:200])
