from h import *
L="9239407401"
q="""SELECT campaign.name, campaign.status, campaign_budget.amount_micros, campaign.bidding_strategy_type FROM campaign"""
for r in run_query(L,q): print(json.dumps(r,default=str))
# Napps main account: call assets and their numbers
q2="""SELECT asset.id, asset.type, asset.call_asset.phone_number, asset.call_asset.country_code, asset.call_asset.call_conversion_reporting_state, asset.call_asset.call_conversion_action FROM asset WHERE asset.type = 'CALL'"""
for r in run_query(CID,q2): print(json.dumps(r,default=str))
q3="""SELECT campaign.name, campaign_asset.field_type, campaign_asset.status, asset.call_asset.phone_number FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' """
for r in run_query(CID,q3): print(r["campaign"]["name"], r["campaign_asset"].get("status"), r["asset"]["call_asset"].get("phone_number"))
q4="""SELECT customer_asset.field_type, customer_asset.status, asset.call_asset.phone_number FROM customer_asset WHERE customer_asset.field_type = 'CALL' """
for r in run_query(CID,q4): print("customer-level", r["customer_asset"].get("status"), r["asset"]["call_asset"].get("phone_number"))
