"""Spencer Air: Alex's 10-20 launch checklist (Ads side). Read-only."""
import sys, json
sys.path.insert(0, ".")
from lib import run_query
CID = "2524618054"

print("== CUSTOMER conversion tracking setting ==")
for r in run_query(CID, """SELECT customer.conversion_tracking_setting.conversion_tracking_id,
 customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled,
 customer.conversion_tracking_setting.accepted_customer_data_terms,
 customer.conversion_tracking_setting.google_ads_conversion_customer,
 customer.conversion_tracking_setting.conversion_tracking_status
 FROM customer"""):
    print(json.dumps(r.get("customer", {}), indent=1))

print("\n== CONVERSION ACTIONS (non-removed) ==")
for r in run_query(CID, """SELECT conversion_action.id, conversion_action.name, conversion_action.type,
 conversion_action.category, conversion_action.origin, conversion_action.status,
 conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
 conversion_action.counting_type
 FROM conversion_action WHERE conversion_action.status != 'REMOVED'"""):
    ca = r["conversion_action"]
    print(f" {ca.get('id')} | {ca.get('name')} | {ca.get('type')} | cat={ca.get('category')} | {ca.get('status')} | primary={ca.get('primary_for_goal')} | in_metric={ca.get('include_in_conversions_metric')} | count={ca.get('counting_type')}")

print("\n== CAMPAIGN GOALS (enabled campaigns, biddable only) ==")
for r in run_query(CID, """SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin,
 campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.status = 'ENABLED'"""):
    g = r["campaign_conversion_goal"]
    if g.get("biddable"):
        print(f" {r['campaign']['name']} | {g.get('category')} | {g.get('origin')}")

print("\n== CONVERSIONS BY ACTION, LAST 30 DAYS ==")
for r in run_query(CID, """SELECT segments.conversion_action_name, metrics.conversions, metrics.all_conversions
 FROM customer WHERE segments.date DURING LAST_30_DAYS"""):
    m = r.get("metrics", {})
    print(f" {r['segments']['conversion_action_name']} | conv={m.get('conversions')} | all={m.get('all_conversions')}")
