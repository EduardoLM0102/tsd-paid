import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service

svc = gtm_service()
ACCOUNT = "6004894582"
CONTAINER = "51924815"
WORKSPACE = "8"
parent = f"accounts/{ACCOUNT}/containers/{CONTAINER}/workspaces/{WORKSPACE}"
ws_api = svc.accounts().containers().workspaces()

TAG_IDS = ["39", "43", "52", "15", "9", "36", "32", "37", "41", "44", "46"]
TRIGGER_IDS = ["16", "42", "45"]

print("=" * 100)
print("TAGS (detail)")
print("=" * 100)
for tid in TAG_IDS:
    path = f"{parent}/tags/{tid}"
    try:
        t = ws_api.tags().get(path=path).execute()
        print(f"\n--- [{tid}] {t.get('name')} ({t.get('type')}) ---")
        print(f"  firingTriggerId: {t.get('firingTriggerId')}")
        print(f"  blockingTriggerId: {t.get('blockingTriggerId')}")
        print(f"  paused: {t.get('paused')}")
        for p in t.get("parameter", []):
            print(f"  param: {p.get('key')} = {p.get('value') or p.get('list') or p.get('map')}")
    except Exception as e:
        print(f"[{tid}] ERROR: {e}")

print("\n" + "=" * 100)
print("TRIGGERS (detail)")
print("=" * 100)
for trid in TRIGGER_IDS:
    path = f"{parent}/triggers/{trid}"
    try:
        tr = ws_api.triggers().get(path=path).execute()
        print(f"\n--- [{trid}] {tr.get('name')} ({tr.get('type')}) ---")
        print(json.dumps(tr, indent=2)[:1500])
    except Exception as e:
        print(f"[{trid}] ERROR: {e}")

print("\n" + "=" * 100)
print("CONTAINER VERSIONS (is workspace 8 == live?)")
print("=" * 100)
try:
    versions = svc.accounts().containers().versions().list(
        parent=f"accounts/{ACCOUNT}/containers/{CONTAINER}").execute()
    for v in versions.get("containerVersion", [])[:5]:
        print(f"  version {v.get('containerVersionId')}  name={v.get('name')!r}  "
              f"published={v.get('fingerprint')}  deleted={v.get('deleted')}")
except Exception as e:
    print(f"ERROR listing versions: {e}")

try:
    live = svc.accounts().containers().versions().live(
        parent=f"accounts/{ACCOUNT}/containers/{CONTAINER}").execute()
    print(f"\nLIVE version: {live.get('containerVersionId')}  name={live.get('name')!r}")
except Exception as e:
    print(f"ERROR getting live version: {e}")

# compare workspace status
try:
    status = ws_api.getStatus(path=parent).execute()
    print(f"\nWorkspace 8 status vs live: {json.dumps(status, indent=2)[:2000]}")
except Exception as e:
    print(f"ERROR getStatus: {e}")
