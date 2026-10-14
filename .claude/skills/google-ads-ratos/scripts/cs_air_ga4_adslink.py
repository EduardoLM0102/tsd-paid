import sys
sys.path.insert(0, ".")
from ga4_setup import admin_service

svc = admin_service()
PROPERTY = "310229049"

print("=== Google Ads links on this GA4 property ===")
try:
    resp = svc.properties().googleAdsLinks().list(parent=f"properties/{PROPERTY}").execute()
    links = resp.get("googleAdsLinks", [])
    if not links:
        print("  NONE — no Google Ads account is linked to this GA4 property.")
    for l in links:
        print(f"  customerId={l.get('customerId')} adsPersonalizationEnabled={l.get('adsPersonalizationEnabled')} "
              f"canManageClients={l.get('canManageClients')} creatorEmail={l.get('creatorEmail')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== Data streams (confirm measurement ID + default URI) ===")
streams = svc.properties().dataStreams().list(parent=f"properties/{PROPERTY}").execute().get("dataStreams", [])
for s in streams:
    web = s.get("webStreamData", {}) or {}
    print(f"  {s.get('displayName')}  measurementId={web.get('measurementId')}  url={web.get('defaultUri')}")

print("\n=== Key events configured (Admin API view, includes custom vs default) ===")
try:
    ke = svc.properties().keyEvents().list(parent=f"properties/{PROPERTY}").execute()
    for k in ke.get("keyEvents", []):
        print(f"  eventName={k.get('eventName')} custom={k.get('custom')} countingMethod={k.get('countingMethod')} "
              f"defaultValue={k.get('defaultValue')}")
except Exception as e:
    print(f"  ERROR: {e}")
