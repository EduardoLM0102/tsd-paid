"""Publish tested Nick's GTM-5RH7XW36 v9 (GHL number pool, Daniel ask 10-28), sync workspaces, delete test env 71."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6294341662/containers/219605836"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "8": sys.exit("ABORT: live is not v8")
r = CC.versions().publish(path=f"{C}/versions/9").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["name"], "conflicts:", len(s.get("mergeConflict", [])))
CC.environments().delete(path=f"{C}/environments/71").execute(); print("deleted env 71")
