"""Concrete GTM-53FXJRN4: stop Meta's capiParamBuilder (~37 KB) from loading (Alex 10-29 ask, Edu's go 11-02).
Default Workspace 6 only, then a version + test env. NO publish.
How: the gallery Meta Pixel template skips injecting clientParamBuilder.bundle.js when
window._fbq_param_builder_status is already 'complete'. A cHTML tag on Initialization - All Pages sets it before
any Meta tag runs. Template stays untouched (keeps gallery updates). Alex's server already sends fbc/fbp/IP via CAPI.
Run: ./gtm.sh concrete_gtm_parambuilder_draft_1102.py
"""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
A, CID = "6382574349", "267158903"
C = f"accounts/{A}/containers/{CID}"
WS = f"{C}/workspaces/6"
CC = svc.accounts().containers()
W = CC.workspaces()
if CC.versions().live(parent=C).execute()["containerVersionId"] != "5": sys.exit("ABORT: live is not v5")
NAME = "00 | cHTML - Skip Meta ParamBuilder"
tags = W.tags().list(parent=WS).execute().get("tag", [])
if any(t["name"] == NAME for t in tags): sys.exit("ABORT: tag already exists")
t = W.tags().create(parent=WS, body={
    "name": NAME, "type": "html",
    "parameter": [{"type": "template", "key": "html",
                   "value": "<script>window._fbq_param_builder_status = 'complete';</script>"},
                  {"type": "boolean", "key": "supportDocumentWrite", "value": "false"}],
    "firingTriggerId": ["2147479573"],  # built-in Initialization - All Pages
    "tagFiringOption": "oncePerLoad",
    "notes": "TSD 11-02: makes the Meta Pixel template skip loading capiParamBuilder (Alex: server CAPI already sends that data)."}).execute()
print("created tag", t["tagId"], t["name"])
r = W.create_version(path=WS, body={"name": "TSD 11-02 skip Meta capiParamBuilder",
    "notes": "cHTML on Initialization sets window._fbq_param_builder_status='complete' so the Meta Pixel template does not inject clientParamBuilder.bundle.js"}).execute()
v = r["containerVersion"]
print("version", v["containerVersionId"], "compilerError:", r.get("compilerError"))
env = CC.environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v["containerVersionId"], "type": "user", "containerVersionId": v["containerVersionId"]}).execute()
print(json.dumps({"version": v["containerVersionId"], "envId": env["environmentId"], "auth": env["authorizationCode"]}))
