"""Read-only: Neon Monkey GTM-WM9CDGPT live version + tag list + Default Workspace pending changes."""
from gtm_setup import gtm_service

svc = gtm_service()
c = "accounts/6264215029/containers/203561665"
live = svc.accounts().containers().versions().live(parent=c).execute()
print("LIVE version:", live.get("containerVersionId"), "| name:", live.get("name"), "| fingerprint ts:", live.get("fingerprint"))
for t in live.get("tag", []):
    st = "PAUSED" if t.get("paused") else "on"
    print(f"  [{st}] {t['type']:<10} {t['name']}")
ws = svc.accounts().containers().workspaces().getStatus(path=f"{c}/workspaces/12").execute()
print("Default Workspace pending changes:", len(ws.get("workspaceChange", [])))
hdrs = svc.accounts().containers().version_headers().list(parent=c).execute()
for h in hdrs.get("containerVersionHeader", [])[-3:]:
    print("  version", h.get("containerVersionId"), h.get("name", ""), "tags:", h.get("numTags"))
