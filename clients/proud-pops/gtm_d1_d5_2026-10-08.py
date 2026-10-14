#!/usr/bin/env python3
"""GTM D-1 + D-5 (Edu OK 2026-10-08). Container GTM-WBFDB6L8.
  prepare  In the Default Workspace: trigger [73] cEvent - Appointment Scheduled += Page Path not contains /careers (D-1);
           tag [111] 05 | Meta - Lead: standardEventName PageView -> Lead (D-5). Compile check. Create an UNPUBLISHED version
           + a private 'user' environment pointing at it, for the headless test.
  publish  Publish that version (only after the headless test passes), verify live, delete the test environment.
"""
import sys, os, json
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from gtm_setup import gtm_service
svc = gtm_service(); C = "accounts/6255217830/containers/198527160"; W = svc.accounts().containers().workspaces()
STATE = os.path.expanduser("~/Documents/GitHub/topserv-workspace/clients/proud-pops/.gtm_d1_d5_state.json")
step = sys.argv[1]

if step == "prepare":
    live = svc.accounts().containers().versions().live(parent=C).execute()
    ws = W.list(parent=C).execute()["workspace"]; assert len(ws) == 1, ws
    WS = ws[0]["path"]; st = W.getStatus(path=WS).execute()
    print("live:", live["containerVersionId"], "| workspace:", ws[0]["workspaceId"], "| pending:", st.get("workspaceChange", []), "| conflicts:", st.get("mergeConflict", []))
    assert live["containerVersionId"] == "42" and not st.get("workspaceChange") and not st.get("mergeConflict")
    t73 = W.triggers().get(path=f"{WS}/triggers/73").execute()
    t73["filter"] = (t73.get("filter") or []) + [{"type": "contains", "parameter": [
        {"type": "template", "key": "arg0", "value": "{{Page Path}}"}, {"type": "template", "key": "arg1", "value": "/careers"},
        {"type": "boolean", "key": "negate", "value": "true"}]}]
    t73 = W.triggers().update(path=f"{WS}/triggers/73", body=t73, fingerprint=t73["fingerprint"]).execute()
    print("D-1 trigger 73 filter:", json.dumps(t73["filter"]))
    tag = W.tags().get(path=f"{WS}/tags/111").execute()
    for p in tag["parameter"]:
        if p["key"] == "standardEventName":
            print("D-5 tag 111 standardEventName:", p["value"], "-> Lead"); p["value"] = "Lead"
    tag = W.tags().update(path=f"{WS}/tags/111", body=tag, fingerprint=tag["fingerprint"]).execute()
    print("   now:", [p["value"] for p in tag["parameter"] if p["key"] in ("eventName", "standardEventName")])
    st = W.getStatus(path=WS).execute()
    print("changes:", [(c.get("changeStatus"), ("tag " + c["tag"]["name"]) if "tag" in c else ("trigger " + c["trigger"]["name"])) for c in st.get("workspaceChange", [])])
    qp = W.quick_preview(path=WS).execute(); print("compilerError:", qp.get("compilerError"))
    assert not qp.get("compilerError") and len(st.get("workspaceChange", [])) == 2
    cv = W.create_version(path=WS, body={"name": "TSD - Careers guard on Appointment Scheduled + Meta Lead event (2026-10-08)",
        "notes": "D-1: trigger 73 Page Path not contains /careers. D-5: tag 111 Meta standard event PageView -> Lead. Rollback = republish v42."}).execute()
    vid = cv["containerVersion"]["containerVersionId"]; print("UNPUBLISHED version created:", vid)
    env = svc.accounts().containers().environments().create(parent=C, body={"name": "TSD headless test v" + vid, "type": "user",
        "containerVersionId": vid, "enableDebug": False}).execute()
    json.dump({"vid": vid, "env": env["environmentId"], "auth": env["authorizationCode"]}, open(STATE, "w"))
    print("test environment:", env["environmentId"], "| live still:", svc.accounts().containers().versions().live(parent=C).execute()["containerVersionId"])

elif step == "publish":
    s = json.load(open(STATE))
    svc.accounts().containers().versions().publish(path=f"{C}/versions/{s['vid']}").execute()
    live = svc.accounts().containers().versions().live(parent=C).execute()
    t73 = next(t for t in live["trigger"] if t["triggerId"] == "73"); t111 = next(t for t in live["tag"] if t["tagId"] == "111")
    print("LIVE:", live["containerVersionId"], live.get("name"))
    print("   trigger 73 filter:", json.dumps(t73.get("filter")))
    print("   tag 111:", [p["value"] for p in t111["parameter"] if p["key"] in ("eventName", "standardEventName")])
    svc.accounts().containers().environments().delete(path=f"{C}/environments/{s['env']}").execute()
    print("test environment deleted; workspaces now:", [(w["workspaceId"], w["name"]) for w in W.list(parent=C).execute()["workspace"]])
