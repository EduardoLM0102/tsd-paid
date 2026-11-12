# READ-ONLY. Napps 11-10: hour of the NB Plumbing click-to-call + call assets / call reporting.
import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "9509605037"; PL = "23819717682"
q = lambda s: run_query(CID, s)
for r in q(f"""SELECT segments.hour, segments.device, segments.conversion_action_name, metrics.all_conversions FROM campaign
  WHERE segments.date = '2026-11-04' AND campaign.id = {PL} AND metrics.all_conversions > 0"""):
    print("conv", r["segments"], r["metrics"])
for r in q(f"""SELECT segments.hour, segments.device, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date = '2026-11-04' AND campaign.id = {PL} AND metrics.clicks > 0"""):
    print("click", r["segments"], r["metrics"])
for r in q(f"""SELECT segments.click_type, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-11-03' AND '2026-11-09' AND campaign.id IN ({PL},24049055193) AND metrics.clicks > 0"""):
    print("clicktype", r["segments"], r["metrics"])
print(q("SELECT customer.call_reporting_setting.call_reporting_enabled, customer.call_reporting_setting.call_conversion_reporting_enabled, customer.time_zone FROM customer"))
for r in q("""SELECT asset.id, asset.call_asset.phone_number, asset.call_asset.call_conversion_reporting_state, asset.call_asset.call_conversion_action FROM asset WHERE asset.type = 'CALL'"""):
    print("asset", r["asset"])
for lvl, res in (("campaign", "campaign_asset"), ("customer", "customer_asset")):
    for r in q(f"SELECT {res}.asset, {res}.status FROM {res} WHERE {res}.field_type = 'CALL'" + (f" AND campaign.id IN ({PL},24049055193)" if lvl=="campaign" else "")):
        print(lvl, r)
