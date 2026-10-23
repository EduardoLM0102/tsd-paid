"""Publish tested GTM-KT5RPTP version 11 (10-23: GA4 generate_lead tag 63 back on), sync workspaces, delete test env 82."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6000941581/containers/31091984"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "10": sys.exit("ABORT: live is not v10")
r = CC.versions().publish(path=f"{C}/versions/11").execute()
print("published:", r["containerVersion"]["containerVersionId"], r.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["name"], "conflicts:", len(s.get("mergeConflict", [])))
CC.environments().delete(path=f"{C}/environments/82").execute(); print("deleted env 82")
