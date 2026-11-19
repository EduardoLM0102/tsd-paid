"""Concrete Adventures GTM-53FXJRN4: post-launch cleanup DRAFT (2026-11-19, fu-102). Default Workspace 7, NO publish.
go.concreteadventures.com (the old GHL pages) has no DNS any more and the new www site has no GHL embeds, so ghl_form_submit can never fire again.
 1. trigger 10 'cEvent - Lead (generate_lead + old GHL)' -> regex ^generate_lead$, renamed 'cEvent - Lead (generate_lead)'. Tags on it: Ads Lead 29 + Meta Lead 22 (unchanged).
 2. tag 7 '00 | cHTML - GHL Listener' PAUSED (listened to a GHL iframe that no longer exists).
 3. tag 11 '04 | GA4 - Lead' PAUSED (fired only on ghl_form_submit via trigger 37; GA4 generate_lead comes from Alex's server). Trigger 37 left in place.
Publish separately after Edu's go (concrete_gtm_publish_v6_1102.py pattern). Rollback: unpause 7 + 11, regex back to ^(generate_lead|ghl_form_submit)$.
Run: ./gtm.sh concrete_gtm_cleanup_draft_1119.py"""
import sys; sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6382574349/containers/267158903"; WS = f"{C}/workspaces/7"
W = svc.accounts().containers().workspaces()
def get(kind, i): return getattr(W, kind)().get(path=f"{WS}/{kind}/{i}").execute()
def put(kind, o):
    r = getattr(W, kind)().update(path=o["path"], body=o).execute(); print("updated", kind, r.get(kind[:-1] + "Id"), r["name"]); return r
t = get("triggers", "10"); assert t["name"].startswith("cEvent - Lead"), t["name"]
hit = 0
for f in t.get("customEventFilter", []):
    for p in f.get("parameter", []):
        if p.get("value") == "^(generate_lead|ghl_form_submit)$": p["value"] = "^generate_lead$"; hit += 1
assert hit == 1, hit
t["name"] = "cEvent - Lead (generate_lead)"; put("triggers", t)
for tid, name in (("7", "00 | cHTML - GHL Listener"), ("11", "04 | GA4 - Lead")):
    g = get("tags", tid); assert g["name"] == name, g["name"]; g["paused"] = True; put("tags", g)
st = W.getStatus(path=WS).execute()
print("workspace 7 changes:", [(c.get("changeStatus"), (c.get("trigger") or c.get("tag") or {}).get("name")) for c in st.get("workspaceChange", [])], "conflicts:", len(st.get("mergeConflict", [])))
live = svc.accounts().containers().versions().live(parent=C).execute(); print("live still v", live["containerVersionId"])
