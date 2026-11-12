"""Publish tested GTM-53FXJRN4 version 6 (11-02: tag 40 skips Meta capiParamBuilder), sync workspaces, delete test env 41."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "5": sys.exit("ABORT: live is not v5")
v6 = CC.versions().get(path=f"{C}/versions/6").execute()
if not any(t["tagId"] == "40" for t in v6.get("tag", [])): sys.exit("ABORT: v6 has no tag 40")
r = CC.versions().publish(path=f"{C}/versions/6").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["workspaceId"], w["name"], "conflicts:", len(s.get("mergeConflict", [])))
CC.environments().delete(path=f"{C}/environments/41").execute(); print("deleted env 41")
