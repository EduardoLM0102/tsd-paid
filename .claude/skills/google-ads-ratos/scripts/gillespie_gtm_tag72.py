import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service

svc = gtm_service()
parent = "accounts/6360204363/containers/255120208/workspaces/8"
ws_api = svc.accounts().containers().workspaces()

for tag_id in ["72", "46"]:
    path = parent + f"/tags/{tag_id}"
    t = ws_api.tags().get(path=path).execute()
    print("=" * 80)
    print(f"TAG {tag_id}: {t.get('name')} | type={t.get('type')} | paused={t.get('paused')}")
    print(f"firingTriggerId={t.get('firingTriggerId')}")
    print(json.dumps(t.get("parameter", []), indent=2))

print("=" * 80)
print("TRIGGER 42 detail")
tr = ws_api.triggers().get(path=parent + "/triggers/42").execute()
print(json.dumps(tr, indent=2))
