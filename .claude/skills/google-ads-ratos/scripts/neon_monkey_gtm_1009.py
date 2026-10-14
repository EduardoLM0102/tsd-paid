import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
c = "accounts/6264215029/containers/203561665"
cont = svc.accounts().containers().get(path=c).execute()
print("container:", cont.get("publicId"), cont.get("name"), "domains:", cont.get("domainName"), "usage:", cont.get("usageContext"))
hdrs = svc.accounts().containers().version_headers().list(parent=c).execute().get("containerVersionHeader", [])
print("versions:", len(hdrs))
for h in hdrs[-8:]:
    print("  v", h.get("containerVersionId"), h.get("name"), "tags:", h.get("numTags"), "deleted:", h.get("deleted", False))
try:
    live = svc.accounts().containers().versions().live(parent=c).execute()
    print("LIVE version:", live.get("containerVersionId"), live.get("name"), "fingerprint ts:", live.get("fingerprint"))
    for t in live.get("tag", []):
        params = {p.get("key"): p.get("value") for p in t.get("parameter", []) if p.get("type") in ("template", "boolean", "integer")}
        print(f"  TAG [{t.get('tagId')}] {t.get('name')} ({t.get('type')}) paused={t.get('paused', False)} "
              f"{ {k: v for k, v in params.items() if k in ('tagId','measurementId','conversionId','conversionLabel','eventName')} } triggers={t.get('firingTriggerId')}")
    for tr in live.get("trigger", []):
        print(f"  TRG [{tr.get('triggerId')}] {tr.get('name')} ({tr.get('type')})")
except Exception as e:
    print("live failed:", str(e)[:300])
ws = svc.accounts().containers().workspaces().list(parent=c).execute().get("workspace", [])
for w in ws:
    st = svc.accounts().containers().workspaces().getStatus(path=w["path"]).execute()
    print("workspace", w.get("workspaceId"), w.get("name"), "pending changes:", len(st.get("workspaceChange", [])))
