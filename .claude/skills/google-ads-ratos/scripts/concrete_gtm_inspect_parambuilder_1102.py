"""Read-only: find Meta capiParamBuilder / parameter builder references in live GTM-53FXJRN4 (Alex 10-29 ask)."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"
live = CC.versions().live(parent=C).execute()
print("live version:", live["containerVersionId"], live.get("name"))
for kind in ("tag", "variable", "customTemplate", "trigger"):
    for o in live.get(kind, []):
        blob = json.dumps(o)
        hit = any(k in blob.lower() for k in ("parambuilder", "param_builder", "parameter builder", "capi"))
        print(f"{kind:14} {o.get(kind+'Id', o.get('templateId',''))!s:>4} {o.get('type',''):28} {o.get('name')}{'   <-- MATCH' if hit else ''}")
        if hit:
            for p in o.get("parameter", []):
                v = json.dumps(p)
                if any(k in v.lower() for k in ("parambuilder","param_builder","capi")):
                    print("      param:", v[:400])
            if kind == "customTemplate":
                src = o.get("templateData","")
                for line in src.splitlines():
                    if any(k in line.lower() for k in ("parambuilder","param_builder","capi")):
                        print("      tpl:", line.strip()[:300])
print("workspaces:", [(w["workspaceId"], w["name"]) for w in CC.workspaces().list(parent=C).execute()["workspace"]])
