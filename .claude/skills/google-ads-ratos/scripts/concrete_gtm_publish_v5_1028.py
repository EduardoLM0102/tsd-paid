"""Publish tested GTM-53FXJRN4 version 5 (10-28: Meta tags 6/22/23 require ad_storage), sync workspaces, delete test env 39."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "4": sys.exit("ABORT: live is not v4")
r = CC.versions().publish(path=f"{C}/versions/5").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["workspaceId"], w["name"], "conflicts:", len(s.get("mergeConflict", [])))
CC.environments().delete(path=f"{C}/environments/39").execute(); print("deleted env 39")
