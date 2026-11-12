# READ-ONLY. Napps 11-10: call assets linked to NB + Branded campaigns, and customer-level.
import sys
sys.path.insert(0, ".")
from lib import run_query
q = lambda s: run_query("9509605037", s)
for r in q("SELECT campaign.id, campaign.name, campaign_asset.asset, campaign_asset.status FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' AND campaign.id IN (23685615826,23819717682,24049055193)"):
    print("campaign", r["campaign"]["name"], r["campaign_asset"])
for r in q("SELECT customer_asset.asset, customer_asset.status FROM customer_asset WHERE customer_asset.field_type = 'CALL'"):
    print("customer", r["customer_asset"])
