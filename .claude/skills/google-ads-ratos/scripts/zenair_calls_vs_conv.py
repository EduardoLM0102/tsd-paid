import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"

print("=" * 100)
print("ZEN AIR — RAW PHONE_CALLS METRIC BY CAMPAIGN, LAST 7 DAYS")
print("=" * 100)
q1 = """
SELECT campaign.name, campaign.id, campaign.status,
       metrics.phone_calls, metrics.phone_impressions, metrics.phone_through_rate,
       metrics.conversions, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
"""
for r in run_query(CID, q1):
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    pc = m.get("phoneCalls") or m.get("phone_calls")
    pi = m.get("phoneImpressions") or m.get("phone_impressions")
    conv = m.get("conversions")
    cost = (m.get("costMicros") or m.get("cost_micros") or 0)
    if pc or conv:
        print(f"  {c.get('name'):40s} status={c.get('status'):10s} phone_calls={pc} phone_impr={pi} conversions={conv} cost_micros={cost}")

print("\n" + "=" * 100)
print("ZEN AIR — PHONE_CALL_LEAD CONVERSION ACTION BY CAMPAIGN, LAST 7 DAYS")
print("=" * 100)
q2 = """
SELECT campaign.name, segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND metrics.all_conversions > 0
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    seg = r.get("segments", {})
    m = r.get("metrics", {})
    aname = seg.get("conversionActionName") or seg.get("conversion_action_name")
    acat = seg.get("conversionActionCategory") or seg.get("conversion_action_category")
    conv = m.get("conversions")
    allconv = m.get("allConversions") or m.get("all_conversions")
    print(f"  {c.get('name'):40s} action={aname} cat={acat} conversions={conv} all_conversions={allconv}")

print("\n" + "=" * 100)
print("ZEN AIR — CALL ASSETS ON ACCOUNT (phone numbers, status)")
print("=" * 100)
q3 = """
SELECT asset.id, asset.call_asset.phone_number, asset.call_asset.country_code, asset.call_asset.call_conversion_reporting_state
FROM asset
WHERE asset.type = 'CALL'
"""
for r in run_query(CID, q3):
    a = r.get("asset", {})
    ca = a.get("callAsset") or a.get("call_asset") or {}
    print(f"  id={a.get('id')} phone={ca.get('phoneNumber') or ca.get('phone_number')} country={ca.get('countryCode') or ca.get('country_code')} convReporting={ca.get('callConversionReportingState') or ca.get('call_conversion_reporting_state')}")
