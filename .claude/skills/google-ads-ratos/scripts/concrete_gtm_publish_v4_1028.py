"""Publish tested GTM-53FXJRN4 version 4 (10-28: lead trigger -> generate_lead, Meta Lead eventID, GA4 lead old-GHL only), sync workspaces, delete test env 38."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "3": sys.exit("ABORT: live is not v3")
r = CC.versions().publish(path=f"{C}/versions/4").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["name"], "conflicts:", len(s.get("mergeConflict", [])))
CC.environments().delete(path=f"{C}/environments/38").execute(); print("deleted env 38")
