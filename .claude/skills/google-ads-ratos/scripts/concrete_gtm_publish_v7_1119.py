"""Create + publish GTM-53FXJRN4 v7 from Default Workspace 7 (11-19 post-launch cleanup, Edu: "Publish the concrete change"), then sync workspaces.
Guards: live must be v6; the new version must have trigger 10 on ^generate_lead$ and tags 7 + 11 paused."""
import sys; sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"; WS = f"{C}/workspaces/7"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "6": sys.exit("ABORT: live is not v6")
r = CC.workspaces().create_version(path=WS, body={"name": "TSD 11-19 post-launch cleanup: lead trigger generate_lead only, GHL Listener + GA4 Lead paused",
    "notes": "go. GHL pages gone (no DNS). Trigger 10 regex ^generate_lead$; tags 7 and 11 paused. Script concrete_gtm_cleanup_draft_1119.py / concrete_gtm_publish_v7_1119.py"}).execute()
if r.get("compilerError"): sys.exit(f"ABORT: compiler error {r}")
v = r["containerVersion"]; vid = v["containerVersionId"]; print("created version", vid, v["name"])
t10 = next(t for t in v["trigger"] if t["triggerId"] == "10")
rx = [p["value"] for f in t10.get("customEventFilter", []) for p in f.get("parameter", []) if p["key"] == "arg1"]
paused = {t["tagId"]: t.get("paused", False) for t in v["tag"]}
print("trigger 10:", t10["name"], rx, "| tag 7 paused:", paused.get("7"), "tag 11 paused:", paused.get("11"))
if rx != ["^generate_lead$"] or not (paused.get("7") and paused.get("11")): sys.exit("ABORT: version content not as staged")
p = CC.versions().publish(path=f"{C}/versions/{vid}").execute()
print("published:", p["containerVersion"]["containerVersionId"], "compilerError:", p.get("compilerError"))
print("live now:", CC.versions().live(parent=C).execute()["containerVersionId"])
for w in CC.workspaces().list(parent=C).execute()["workspace"]:
    s = CC.workspaces().sync(path=w["path"]).execute(); print("synced", w["workspaceId"], w["name"], "conflicts:", len(s.get("mergeConflict", [])))
