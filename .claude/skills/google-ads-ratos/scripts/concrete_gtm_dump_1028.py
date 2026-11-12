"""Concrete Adventures GTM-53FXJRN4: full JSON dump of live version + workspaces (read-only)."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
path = "accounts/6382574349/containers/267158903"
live = svc.accounts().containers().versions().live(parent=path).execute()
ws = svc.accounts().containers().workspaces().list(parent=path).execute()
json.dump({"live": live, "workspaces": ws}, open(sys.argv[1], "w"), indent=1)
print("live", live.get("containerVersionId"), live.get("name"))
for w in ws.get("workspace", []):
    st = svc.accounts().containers().workspaces().getStatus(path=w["path"]).execute()
    print("ws", w["workspaceId"], w["name"], "changes:", len(st.get("workspaceChange", [])), "conflicts:", len(st.get("mergeConflict", [])))
