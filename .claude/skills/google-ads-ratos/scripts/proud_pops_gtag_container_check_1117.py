"""Read-only: GA4 Google tag container 6228503454/183775598 (internal traffic rule from Cowork 11-17), pending workspace changes."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6228503454/containers/183775598"
c = svc.accounts().containers().get(path=C).execute()
print(c.get("publicId"), c.get("name"), c.get("usageContext"))
for w in svc.accounts().containers().workspaces().list(parent=C).execute().get("workspace", []):
    st = svc.accounts().containers().workspaces().getStatus(path=w["path"]).execute()
    print("ws", w["workspaceId"], w["name"], "changes:", len(st.get("workspaceChange", [])))
    for ch in st.get("workspaceChange", []):
        print(json.dumps(ch)[:1200])
try:
    live = svc.accounts().containers().versions().live(parent=C).execute()
    print("live", live.get("containerVersionId"), live.get("name"))
except Exception as e:
    print("live err", str(e)[:200])
