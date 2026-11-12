"""Spencer GTM-KT5RPTP follow-up to spencer_gtm_launch_draft_1022.py (headless test findings 2026-10-22):
 - Meta PageView (65) oncePerLoad -> oncePerEvent (consent-blocked load attempt used up the once-per-load slot, so the
   consent_marketing_granted trigger never fired)
 - Ads Lead (72): drop setupTag (sequencing killed the cookieless conversion ping when consent is denied; live v8
   already sends user data without it)
Then create a new version + test env (NOT published)."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
A, CID = "6000941581", "31091984"
C = f"accounts/{A}/containers/{CID}"
WS = svc.accounts().containers().workspaces().list(parent=C).execute()["workspace"][0]["path"]
print("workspace", WS)
T = svc.accounts().containers().workspaces().tags()
t = T.get(path=f"{WS}/tags/65").execute(); t["tagFiringOption"] = "oncePerEvent"; T.update(path=t["path"], body=t).execute()
t = T.get(path=f"{WS}/tags/72").execute(); t.pop("setupTag", None); T.update(path=t["path"], body=t).execute()
print("72 setupTag now:", T.get(path=f"{WS}/tags/72").execute().get("setupTag"))
r = svc.accounts().containers().workspaces().create_version(path=WS, body={"name": "TSD 10-22 new-site launch prep",
    "notes": "Meta Lead eventId=event_id; pixel 1258997717469696; Meta tags need ad_storage + PageView on consent grant (spencer:consent-change); GA4 generate_lead paused (server MP); EC email/phone normalized; CallRail tag blocked on new site (boot loads it)"}).execute()
v = r["containerVersion"]["containerVersionId"]
env = svc.accounts().containers().environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v, "type": "user", "containerVersionId": v}).execute()
print(json.dumps({"version": v, "envId": env["environmentId"], "auth": env["authorizationCode"], "compilerError": r.get("compilerError")}))
