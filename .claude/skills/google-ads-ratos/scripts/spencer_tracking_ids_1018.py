"""Spencer Air: pull every tracking ID (Google Ads conversion IDs/labels + GTM-KT5RPTP live tags). Read-only."""
import sys, json, re
sys.path.insert(0, ".")
from lib import run_query

CID = "2524618054"
GTM_PUBLIC_ID = "GTM-KT5RPTP"

print("=" * 100)
print("GOOGLE ADS account-level conversion tracking ID")
print("=" * 100)
q = """
SELECT customer.descriptive_name, customer.auto_tagging_enabled,
       customer.conversion_tracking_setting.conversion_tracking_id,
       customer.conversion_tracking_setting.google_ads_conversion_customer
FROM customer
"""
for r in run_query(CID, q):
    print(json.dumps(r, indent=2))

print("\n" + "=" * 100)
print("CONVERSION ACTIONS (status, primary, AW id + label from snippet)")
print("=" * 100)
q3 = """
SELECT conversion_action.id, conversion_action.name, conversion_action.type,
       conversion_action.category, conversion_action.status,
       conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
       conversion_action.tag_snippets
FROM conversion_action
"""
for r in run_query(CID, q3):
    ca = r.get("conversionAction") or r.get("conversion_action") or {}
    snips = ca.get("tagSnippets") or ca.get("tag_snippets") or []
    labels = set()
    for ts in snips:
        for field in ("eventSnippet", "globalSiteTag", "event_snippet", "global_site_tag"):
            for m in re.findall(r"AW-\d+(?:/[\w-]+)?", ts.get(field, "") or ""):
                labels.add(m)
    print(f"  [{ca.get('id')}] {str(ca.get('name')):55s} type={ca.get('type')} cat={ca.get('category')} "
          f"status={ca.get('status')} primary={ca.get('primary_for_goal', ca.get('primaryForGoal'))} in_conv={ca.get('include_in_conversions_metric', ca.get('includeInConversionsMetric'))} "
          f"send_to={sorted(labels)}")

print("\n" + "=" * 100)
print(f"GTM: find {GTM_PUBLIC_ID} and dump live version tags")
print("=" * 100)
try:
    from gtm_setup import gtm_service
    svc = gtm_service()
    found = None
    accts = svc.accounts().list().execute().get("account", [])
    for a in accts:
        try:
            cs = svc.accounts().containers().list(parent=a["path"]).execute().get("container", [])
        except Exception:
            continue
        for c in cs:
            if c.get("publicId") == GTM_PUBLIC_ID:
                found = (a, c)
                break
        if found:
            break
    if not found:
        print(f"  {GTM_PUBLIC_ID} NOT accessible with this GTM token ({len(accts)} accounts scanned)")
    else:
        a, c = found
        print(f"  account: {a.get('name')} ({a.get('accountId')})  container: {c.get('name')} ({c.get('containerId')})")
        live = svc.accounts().containers().versions().live(parent=c["path"]).execute()
        print(f"  LIVE version {live.get('containerVersionId')} name={live.get('name')!r}")
        print("  VARIABLES:")
        for v in live.get("variable", []):
            print(f"   - {v.get('name')} ({v.get('type')}) = {[(p.get('key'), p.get('value')) for p in v.get('parameter', [])]}")
        print("  TAGS:")
        for t in live.get("tag", []):
            params = {p.get("key"): p.get("value") for p in t.get("parameter", []) if p.get("value")}
            keep = {k: v for k, v in params.items() if k in (
                "tagId", "measurementId", "measurementIdOverride", "conversionId", "conversionLabel",
                "eventName", "html") }
            if "html" in keep:
                h = keep.pop("html")
                ids = sorted(set(re.findall(r"(?:AW-\d+|G-[A-Z0-9]{6,12}|fbq\('init',\s*'\d+'|\b\d{15,16}\b|calltrk\.com/companies/\d+/\w+)", h)))
                keep["html_ids"] = ids
            print(f"   - [{t.get('tagId')}] {t.get('name')} ({t.get('type')}) paused={t.get('paused', False)} {keep} all={[(p.get('key'), p.get('value')) for p in t.get('parameter', []) if p.get('value') and p.get('key')!='html']}")
        print("  TRIGGERS:")
        for tr in live.get("trigger", []):
            print(f"   - [{tr.get('triggerId')}] {tr.get('name')} ({tr.get('type')})")
        print("  live fingerprint/time:", live.get("fingerprint"))
except Exception as e:
    print(f"  GTM ERROR: {e}")
