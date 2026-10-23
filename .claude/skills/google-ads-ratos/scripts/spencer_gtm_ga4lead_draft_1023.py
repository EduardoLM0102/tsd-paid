"""Spencer GTM-KT5RPTP, 2026-10-23 (Alex/Johnny: form submit fires Ads Lead but no GA4 event): unpause tag 63 'GA4 | Event | Lead'
(generate_lead on trigger 35 'cEvent - Lead', same as Ads Lead 72) in Default Workspace 12, then create a version (NOT published)
+ a user environment serving it, for the headless test. Server MP generate_lead arrives with source/page (not set), so the browser
event is the one GA4 can attribute; Alex to stop the MP generate_lead to avoid double counting."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
A, CID = "6000941581", "31091984"; C = f"accounts/{A}/containers/{CID}"; W = C + "/workspaces/12"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "10": sys.exit("ABORT: live is not v10")
if CC.workspaces().getStatus(path=W).execute().get("workspaceChange"): sys.exit("ABORT: workspace has pending changes")
t = CC.workspaces().tags().get(path=f"{W}/tags/63").execute()
if t["name"] != "GA4 | Event | Lead" or not t.get("paused") or t.get("firingTriggerId") != ["35"]: sys.exit(f"ABORT: tag 63 unexpected: {t['name']} paused={t.get('paused')} {t.get('firingTriggerId')}")
t["paused"] = False
CC.workspaces().tags().update(path=f"{W}/tags/63", body=t).execute()
print("tag 63 unpaused in workspace")
r = CC.workspaces().create_version(path=W, body={"name": "TSD 10-23 GA4 generate_lead back on",
    "notes": "Tag 63 GA4 generate_lead unpaused (fires on cEvent - Lead with Ads Lead 72). Server MP generate_lead lands with (not set) source/page; Alex to drop the MP one."}).execute()
v = r["containerVersion"]; print("version", v["containerVersionId"], "compilerError:", r.get("compilerError"))
env = CC.environments().create(parent=C, body={"accountId": A, "containerId": CID, "name": "TSD test v" + v["containerVersionId"],
    "type": "user", "containerVersionId": v["containerVersionId"]}).execute()
print(json.dumps({"version": v["containerVersionId"], "envId": env["environmentId"], "auth": env["authorizationCode"]}))
