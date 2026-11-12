"""Spencer GTM-KT5RPTP: create a version from Default Workspace (NOT published) + a user env serving it, for headless test."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
A, CID = "6000941581", "31091984"
C = f"accounts/{A}/containers/{CID}"
r = svc.accounts().containers().workspaces().create_version(path=f"{C}/workspaces/10",
    body={"name": "TSD 10-22 new-site launch prep", "notes": "Meta Lead eventId=event_id; pixel 1258997717469696; Meta tags need ad_storage + PageView on consent grant; GA4 generate_lead paused (server MP); EC normalized + Ads Lead sequenced after user data; CallRail tag blocked on new site"}).execute()
v = r["containerVersion"]
print("version", v["containerVersionId"], "compilerError:", r.get("compilerError"))
env = svc.accounts().containers().environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v["containerVersionId"], "type": "user", "containerVersionId": v["containerVersionId"]}).execute()
print(json.dumps({"version": v["containerVersionId"], "envId": env["environmentId"], "auth": env["authorizationCode"]}))
