"""Cool Hand 2026-10-10: PAUSE GTM tag 32 (Google 'Calls from website' awcc) -> version (tested before publish).
ALREADY APPLIED 2026-10-10 (built here, published by the follow-up publish step), don't re-run.
Why: the CallRail Website pool now swaps 469-351-1738 on go. pages (Edu changed its swap target 10-10). Two scripts replacing the
same number = race. CallRail pool wins (per-visitor gclid/UTM/keyword + recordings + upload to Google). Tag kept PAUSED, not deleted;
rollback = unpause and republish.
Run: ./gtm.sh <abs path to this file>
"""
import os
import sys, json
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from gtm_setup import gtm_service
svc = gtm_service(); C = "accounts/6370314680/containers/260649558"
W = svc.accounts().containers().workspaces()
ws = W.create(parent=C, body={"name": "TSD 10-10 pause Google website call tag", "description": "CallRail pool takes over number swapping on go. pages"}).execute()
tag = W.tags().get(path=f"{ws['path']}/tags/32").execute()
assert tag["type"] == "awcc", tag["type"]
tag["paused"] = True
t = W.tags().update(path=tag["path"], body=tag).execute()
print("ws", ws["workspaceId"], "| tag", t["tagId"], t["name"], "| paused:", t.get("paused"))
v = W.create_version(path=ws["path"], body={"name": "Pause Google website call tag (CallRail pool takes over)",
     "notes": "Tag 32 awcc paused. CallRail Website pool now swaps 469-351-1738 on go. pages. 2026-10-10 Claude for Edu."}).execute()
if v.get("compilerError"): print("COMPILER ERROR", v); raise SystemExit(1)
cv = v["containerVersion"]["containerVersionId"]; print("version (NOT published):", cv)
env = svc.accounts().containers().environments().create(parent=C, body={"accountId": "6370314680", "containerId": "260649558",
      "name": "TSD test pause v" + cv, "type": "user", "containerVersionId": cv}).execute()
json.dump({"version": cv, "env": env["environmentId"], "auth": env["authorizationCode"]},
          open("/private/tmp/claude-501/-Users-eduardolarangeirasmarinho/8d65652d-12dc-48aa-a403-84348eb0d918/scratchpad/ch_env2.json", "w"))
print("env", env["environmentId"])
