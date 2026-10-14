import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service

svc = gtm_service()
ACCOUNT = "6004894582"
CONTAINER = "51924815"
WORKSPACE = "8"
parent = f"accounts/{ACCOUNT}/containers/{CONTAINER}/workspaces/{WORKSPACE}"
ws_api = svc.accounts().containers().workspaces()

for vid in ["30", "31", "38", "34"]:
    path = f"{parent}/variables/{vid}"
    v = ws_api.variables().get(path=path).execute()
    print(f"--- [{vid}] {v.get('name')} ({v.get('type')}) ---")
    for p in v.get("parameter", []):
        print(f"  {p.get('key')} = {p.get('value')}")
    print()

# also list ALL triggers (not just the 3 I inspected) to catch anything I missed
print("=== ALL triggers, raw ===")
for t in ws_api.triggers().list(parent=parent).execute().get("trigger", []):
    print(f"[{t.get('triggerId')}] {t.get('name')} type={t.get('type')}")

print("\n=== ALL variables, raw (for anything referencing CallRail/phone_call) ===")
for v in ws_api.variables().list(parent=parent).execute().get("variable", []):
    print(f"[{v.get('variableId')}] {v.get('name')} type={v.get('type')}")
