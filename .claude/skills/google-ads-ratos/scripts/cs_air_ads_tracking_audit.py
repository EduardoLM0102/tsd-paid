import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "5563867754"

print("=" * 100)
print("ACCOUNT-LEVEL: auto-tagging, conversion tracking setting")
print("=" * 100)
q = """
SELECT customer.auto_tagging_enabled, customer.conversion_tracking_setting.conversion_tracking_id,
       customer.conversion_tracking_setting.google_ads_conversion_customer,
       customer.conversion_tracking_setting.cross_account_conversion_tracking_id,
       customer.tracking_url_template, customer.final_url_suffix
FROM customer
"""
for r in run_query(CID, q):
    print(r)

print("\n" + "=" * 100)
print("CAMPAIGN-LEVEL: tracking_url_template / final_url_suffix (can strip gclid or break landing)")
print("=" * 100)
q2 = """
SELECT campaign.id, campaign.name, campaign.tracking_url_template, campaign.final_url_suffix
FROM campaign
WHERE campaign.status != 'REMOVED'
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    print(f"  [{c.get('id')}] {c.get('name'):45s} tracking_template={c.get('trackingUrlTemplate')!r} "
          f"final_url_suffix={c.get('finalUrlSuffix')!r}")

print("\n" + "=" * 100)
print("CONVERSION ACTIONS: full detail (type, category, counting, windows, status)")
print("=" * 100)
q3 = """
SELECT conversion_action.id, conversion_action.name, conversion_action.type,
       conversion_action.category, conversion_action.status,
       conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
       conversion_action.counting_type, conversion_action.click_through_lookback_window_days,
       conversion_action.value_settings.default_value,
       conversion_action.phone_call_duration_seconds,
       conversion_action.tag_snippets
FROM conversion_action
"""
for r in run_query(CID, q3):
    ca = r.get("conversionAction") or r.get("conversion_action") or {}
    if not ca:
        print("  RAW ROW (no conversionAction key found):", r)
        continue
    tag_snips = ca.get("tagSnippets") or ca.get("tag_snippets") or []
    aw_ids = set()
    for ts in tag_snips:
        gs = ts.get("globalSiteTag", "") or ""
        for token in gs.split("'"):
            if token.startswith("AW-"):
                aw_ids.add(token)
    name = str(ca.get('name'))
    print(f"  [{ca.get('id')}] {name:40s} type={ca.get('type')} category={ca.get('category')} "
          f"status={ca.get('status')} primary_for_goal={ca.get('primaryForGoal')} "
          f"include_in_conv={ca.get('includeInConversionsMetric')} counting={ca.get('countingType')} "
          f"lookback={ca.get('clickThroughLookbackWindowDays')}d phone_dur={ca.get('phoneCallDurationSeconds')} "
          f"aw_ids_in_snippet={aw_ids}")

print("\n" + "=" * 100)
print("GOOGLE ADS <-> GA4 / MERCHANT / THIRD-PARTY LINKS")
print("=" * 100)
q4 = """
SELECT customer_client_link.client_customer, customer_client_link.status
FROM customer_client_link
"""
try:
    for r in run_query(CID, q4):
        print(r)
except Exception as e:
    print(f"(no customer_client_link data or error: {e})")

# GA4 link is exposed via google_ads_field? Try the dedicated resource.
q5 = "SELECT third_party_app_analytics_link.resource_name FROM third_party_app_analytics_link"
try:
    for r in run_query(CID, q5):
        print(r)
except Exception as e:
    print(f"(no third_party_app_analytics_link / not applicable: {e})")
