"""Publish tested GTM-KT5RPTP version 10 (TSD 10-22 new-site launch prep), sync Default Workspace, delete test envs 80/81."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6000941581/containers/31091984"
CC = svc.accounts().containers()
r = CC.versions().publish(path=f"{C}/versions/10").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute()
    print("synced", w["name"], "conflicts:", len(s.get("mergeConflict", [])))
for e in ("80", "81"):
    CC.environments().delete(path=f"{C}/environments/{e}").execute(); print("deleted env", e)
