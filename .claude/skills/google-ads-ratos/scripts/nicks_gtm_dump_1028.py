"""Nick's GTM-5RH7XW36: read-only dump (live version + workspaces) before adding GHL number pool (Daniel ask 10-28)."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
conts = CC.list(parent="accounts/6294341662").execute().get("container", [])
for c in conts: print(c["publicId"], c["path"], c["name"])
C = next(c["path"] for c in conts if c["publicId"] == "GTM-5RH7XW36")
live = CC.versions().live(parent=C).execute()
print("LIVE v", live["containerVersionId"], live.get("name"))
for t in live.get("tag", []):
    print("  tag", t["tagId"], t["type"], t["name"], "fire:", t.get("firingTriggerId"), "paused" if t.get("paused") else "")
for tr in live.get("trigger", []): print("  trig", tr["triggerId"], tr["type"], tr["name"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    st = CC.workspaces().getStatus(path=w["path"]).execute()
    print("WS", w["workspaceId"], w["name"], "changes:", len(st.get("workspaceChange", [])), "conflicts:", len(st.get("mergeConflict", [])))
    for ch in st.get("workspaceChange", []): print("   ", ch.get("changeStatus"), {k: v.get("name") for k, v in ch.items() if isinstance(v, dict)})
