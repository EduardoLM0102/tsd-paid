"""Nick's GTM-5RH7XW36: add GHL number pool (Daniel Cutrim ask 2026-10-28) as cHTML on All Pages.
Default Workspace 9 -> create version (NOT published) -> user env for headless test. Publish is a separate script."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6294341662/containers/219605836"
WS = f"{C}/workspaces/9"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "8": sys.exit("ABORT: live is not v8")
HTML = ('<script src="https://backend.leadconnectorhq.com/appengine/loc/Zmp3utbcheKG9f82RxvT/pool/Gn998vfQnwx2jjozqjOA/number_pool.js"></script>\n'
        '<script src="https://backend.leadconnectorhq.com/appengine/js/user_session.js"></script>')
NAME = "cHTML - GHL Number Pool | All Pages"
T = CC.workspaces().tags()
if any(t["name"] == NAME for t in T.list(parent=WS).execute().get("tag", [])): sys.exit("ABORT: tag already exists")
tag = T.create(parent=WS, body={
    "name": NAME, "type": "html", "firingTriggerId": ["2147479553"], "tagFiringOption": "oncePerEvent",
    "parameter": [{"type": "template", "key": "html", "value": HTML},
                  {"type": "boolean", "key": "supportDocumentWrite", "value": "false"}]}).execute()
print("created tag", tag["tagId"], tag["name"])
v = CC.workspaces().create_version(path=WS, body={"name": "GHL Number Pool (call tracking)",
    "notes": "Daniel Cutrim ask 2026-10-28: GHL number_pool.js + user_session.js on All Pages"}).execute()
cv = v["containerVersion"]; print("version", cv["containerVersionId"], "compilerError:", v.get("compilerError"))
env = CC.environments().create(parent=C, body={"accountId": "6294341662", "containerId": "219605836",
    "name": "test-numberpool-1028", "type": "user", "containerVersionId": cv["containerVersionId"]}).execute()
print("env", env["environmentId"], env["authorizationCode"])
