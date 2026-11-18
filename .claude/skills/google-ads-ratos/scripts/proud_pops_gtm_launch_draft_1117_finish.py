"""Finish of proud_pops_gtm_launch_draft_1117.py (429 on tag 104): CallRail needs ad_storage, then status + quick_preview."""
import sys, time, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
time.sleep(65)
svc = gtm_service()
WS = "accounts/6255217830/containers/198527160/workspaces/45"
W = svc.accounts().containers().workspaces()
t = W.tags().get(path=f"{WS}/tags/104").execute()
t["consentSettings"] = {"consentStatus": "needed", "consentType": {"type": "list", "list": [{"type": "template", "value": "ad_storage"}]}}
W.tags().update(path=t["path"], body=t).execute(); print("updated 104", t["name"])
st = W.getStatus(path=WS).execute()
for c in st.get("workspaceChange", []):
    k = next(x for x in ("tag", "trigger", "variable") if x in c); print(c["changeStatus"], k, c[k]["name"])
print("conflicts:", len(st.get("mergeConflict", [])))
qp = W.quick_preview(path=WS).execute()
print("compilerError:", qp.get("compilerError"), "| preview ok:", bool(qp.get("containerVersion")))
v = qp["containerVersion"]
for tg in v["tag"]:
    if tg["tagId"] in ("82", "94", "111", "90", "104", "112"):
        print(tg["tagId"], tg["name"], tg.get("firingTriggerId"), tg.get("consentSettings", {}).get("consentStatus"),
              [p["value"] for p in tg.get("parameter", []) if p["key"] == "eventId"])
