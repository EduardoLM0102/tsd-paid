import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service

svc = gtm_service()
ACCOUNT = "6004894582"
CONTAINER = "51924815"

live_path = f"accounts/{ACCOUNT}/containers/{CONTAINER}/versions/7"
v = svc.accounts().containers().versions().get(path=live_path).execute()
print(f"LIVE container version 7 — name={v.get('name')!r} fingerprint={v.get('fingerprint')}")
print(f"  tag count: {len(v.get('tag', []))}")
print(f"  trigger count: {len(v.get('trigger', []))}")
print(f"  variable count: {len(v.get('variable', []))}")
print()
print("Live tags:")
for t in v.get("tag", []):
    print(f"  [{t.get('tagId')}] {t.get('name')} ({t.get('type')})  firingTriggerId={t.get('firingTriggerId')}")
print()
print("Live triggers:")
for t in v.get("trigger", []):
    print(f"  [{t.get('triggerId')}] {t.get('name')} ({t.get('type')})")
