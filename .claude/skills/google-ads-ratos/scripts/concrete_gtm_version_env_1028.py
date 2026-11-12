"""Concrete GTM-53FXJRN4: create a version from Default Workspace (NOT published) + a user env serving it, for headless test."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
A, CID = "6382574349", "267158903"
C = f"accounts/{A}/containers/{CID}"
r = svc.accounts().containers().workspaces().create_version(path=f"{C}/workspaces/4",
    body={"name": "TSD 10-28 new-site lead event (generate_lead)", "notes": "Lead trigger = generate_lead (+ ghl_form_submit until launch) for Ads Lead + Meta Lead; Meta Lead eventID = event_id + advanced matching reads new-site keys; GA4 lead only on old GHL ghl_form_submit (server sends generate_lead on new site)"}).execute()
v = r["containerVersion"]
print("version", v["containerVersionId"], "compilerError:", r.get("compilerError"))
env = svc.accounts().containers().environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v["containerVersionId"], "type": "user", "containerVersionId": v["containerVersionId"]}).execute()
print(json.dumps({"version": v["containerVersionId"], "envId": env["environmentId"], "auth": env["authorizationCode"]}))
