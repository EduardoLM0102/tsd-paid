"""Read-only: diff GTM-WM9CDGPT v10 vs v11 (tags/triggers/variables) + details of new items."""
import json
from gtm_setup import gtm_service
svc = gtm_service()
c = "accounts/6264215029/containers/203561665"
V = svc.accounts().containers().versions()
v10 = V.get(path=f"{c}/versions/10").execute()
v11 = V.get(path=f"{c}/versions/11").execute()
for kind, key in (("tag","tagId"),("trigger","triggerId"),("variable","variableId")):
    a = {x[key]: x for x in v10.get(kind, [])}
    b = {x[key]: x for x in v11.get(kind, [])}
    for k in b.keys() - a.keys():
        print(f"ADDED {kind}:", json.dumps({f: b[k].get(f) for f in ("name","type","parameter","firingTriggerId","filter","customEventFilter")}, indent=1))
    for k in a.keys() - b.keys():
        print(f"REMOVED {kind}:", a[k]["name"])
    for k in a.keys() & b.keys():
        x = {f: v for f, v in a[k].items() if f not in ("fingerprint","path","tagManagerUrl","workspaceId")}
        y = {f: v for f, v in b[k].items() if f not in ("fingerprint","path","tagManagerUrl","workspaceId")}
        if x != y:
            print(f"CHANGED {kind}: {b[k]['name']}")
            for f in set(x) | set(y):
                if x.get(f) != y.get(f):
                    print("   ", f, ":", json.dumps(x.get(f))[:300], "->", json.dumps(y.get(f))[:300])
print("v11 name/description:", v11.get("name"), "|", v11.get("description"))
