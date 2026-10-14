import sys, os, json
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6255217830/containers/198527160"
ws = svc.accounts().containers().workspaces().list(parent=C).execute().get("workspace", [])
print("WORKSPACES:", [(w["workspaceId"], w["name"]) for w in ws])
live = svc.accounts().containers().versions().live(parent=C).execute()
print("LIVE VERSION:", live.get("containerVersionId"), live.get("name"), "| tags", len(live.get("tag", [])), "triggers", len(live.get("trigger", [])))
trig = {t["triggerId"]: t for t in live.get("trigger", [])}
print("\n=== TRIGGERS")
for t in live.get("trigger", []):
    print(f"  [{t['triggerId']}] {t['name']} type={t['type']} customEventFilter={json.dumps(t.get('customEventFilter'))} filter={json.dumps(t.get('filter'))} autoEventFilter={json.dumps(t.get('autoEventFilter'))}")
print("\n=== TAGS")
for g in live.get("tag", []):
    params = {p["key"]: p.get("value", p.get("list", p.get("map"))) for p in g.get("parameter", [])}
    short = {k: (v if not isinstance(v, str) or len(v) < 120 else v[:120] + "...") for k, v in params.items() if k != "html"}
    print(f"  [{g['tagId']}] {g['name']} type={g['type']} paused={g.get('paused')} firing={[trig.get(i, {}).get('name', i) for i in g.get('firingTriggerId', [])]} blocking={[trig.get(i, {}).get('name', i) for i in g.get('blockingTriggerId', [])]}")
    print(f"        params={json.dumps(short)[:400]}")
print("\n=== CUSTOM HTML BODIES mentioning ghl / form / dataLayer")
for g in live.get("tag", []):
    if g["type"] == "html":
        html = next((p.get("value") for p in g.get("parameter", []) if p["key"] == "html"), "")
        if any(k in html for k in ("ghl", "form", "dataLayer", "message")):
            print(f"--- [{g['tagId']}] {g['name']}\n{html[:3000]}\n")
print("\n=== VARIABLES")
for v in live.get("variable", []):
    params = {p["key"]: p.get("value") for p in v.get("parameter", [])}
    print(f"  [{v['variableId']}] {v['name']} type={v['type']} {json.dumps(params)[:200]}")
print("BUILTIN:", [b["name"] for b in live.get("builtInVariable", [])])
