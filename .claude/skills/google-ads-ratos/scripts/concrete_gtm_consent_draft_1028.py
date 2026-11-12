"""Concrete Adventures GTM-53FXJRN4: Meta tags require ad_storage (Alex's 10-28 7:20pm ask 3). Default Workspace 5, NO publish.
Run: ./gtm.sh concrete_gtm_consent_draft_1028.py
New site moved to US opt-out: consent default granted, denied on "Opt out" or GPC/DNT. With ad_storage required, Meta
PageView (6) / Lead (22) / ViewContent (23) follow that choice. Google Ads tags (24/28/29) left on built-in consent
(ad_storage denied = cookieless ping; requiring it would kill the ping, same lesson as Spencer v10).
Then creates a version (NOT published) + user env for the headless test."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
A, CID = "6382574349", "267158903"
C = f"accounts/{A}/containers/{CID}"
WS = f"{C}/workspaces/5"
T = svc.accounts().containers().workspaces().tags()
AD_CONSENT = {"consentStatus": "needed", "consentType": {"type": "list", "list": [{"type": "template", "value": "ad_storage"}]}}
st = svc.accounts().containers().workspaces().getStatus(path=WS).execute()
if st.get("workspaceChange"):
    sys.exit(f"ABORT: workspace 5 already has {len(st['workspaceChange'])} unpublished changes")
for tid in ("6", "22", "23"):
    t = T.get(path=f"{WS}/tags/{tid}").execute()
    t["consentSettings"] = AD_CONSENT
    T.update(path=t["path"], body=t).execute()
    print("updated", tid, t["name"])
r = svc.accounts().containers().workspaces().create_version(path=WS, body={"name": "TSD 10-28 Meta tags require ad_storage",
    "notes": "Meta PageView/Lead/ViewContent need ad_storage (new site = US opt-out, consent default granted, denied on Opt out/GPC). Ads tags unchanged (built-in consent)."}).execute()
v = r["containerVersion"]["containerVersionId"]
env = svc.accounts().containers().environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v, "type": "user", "containerVersionId": v}).execute()
print(json.dumps({"version": v, "envId": env["environmentId"], "auth": env["authorizationCode"], "compilerError": r.get("compilerError")}))
