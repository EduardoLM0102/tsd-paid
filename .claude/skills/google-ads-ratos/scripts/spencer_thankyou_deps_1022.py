"""Spencer Ads 2524618054: anything depending on the /thank-you page? conversion actions + remarketing lists (read-only)."""
import sys, json
sys.path.insert(0, ".")
from lib import run_query
CID = "2524618054"
q = """SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.status,
 conversion_action.category, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric
 FROM conversion_action WHERE conversion_action.status != 'REMOVED'"""
for r in run_query(CID, q):
    c = r["conversion_action"]
    if not globals().get("_shown"): print("keys:", list(c.keys())); _shown = True
    print(f"CA {c['id']:>11} {str(c.get('type_', c.get('type'))):28s} {str(c.get('category','')):18s} primary={c.get('primary_for_goal')} inConv={c.get('include_in_conversions_metric')} {c['name']}")
q = """SELECT user_list.id, user_list.name, user_list.type, user_list.membership_status, user_list.size_for_search,
 user_list.rule_based_user_list.flexible_rule_user_list.inclusive_operands, user_list.rule_based_user_list.flexible_rule_user_list.exclusive_operands
 FROM user_list"""
for r in run_query(CID, q):
    u = r["user_list"]
    rules = json.dumps(u.get("rule_based_user_list", {}))
    print(f"UL {u['id']:>11} {str(u.get('type_', u.get('type',''))):12s} {str(u.get('membership_status','')):6s} {u['name'][:60]:60s} thankyou_rule={'thank' in rules.lower()}")
q = """SELECT campaign.name, campaign.status, ad_group_criterion.user_list.user_list, ad_group_criterion.negative
 FROM ad_group_audience_view WHERE campaign.status = 'ENABLED'"""
rows = list(run_query(CID, q))
print("enabled-campaign audience criteria:", len(rows), [ (r['campaign']['name'], r['ad_group_criterion'].get('negative')) for r in rows][:10])
