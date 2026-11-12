"""Read-only: which Meta pixel ID does live GTM-KT5RPTP fire (Alex 10-29 asked for test code on 3027702340698908)."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6000941581/containers/31091984"
live = CC.versions().live(parent=C).execute()
print("live:", live["containerVersionId"], live.get("name"))
for v in live.get("variable", []):
    b = json.dumps(v)
    if "3027702340698908" in b or "1258997717469696" in b: print("var", v["variableId"], v["name"], [p.get("value") for p in v.get("parameter", [])])
for t in live.get("tag", []):
    b = json.dumps(t)
    if t.get("type","").startswith("cvt") or "fbq" in b:
        pid = [p.get("value") for p in t.get("parameter", []) if p.get("key") == "pixelId"]
        print("tag", t["tagId"], t["name"], "pixelId:", pid, "paused" if t.get("paused") else "")
