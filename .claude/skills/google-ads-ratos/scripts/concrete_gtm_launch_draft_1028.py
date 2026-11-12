"""Concrete Adventures GTM-53FXJRN4: launch-prep DRAFT for Alex's new site (2026-10-28). Default Workspace only, NO publish.
Run: ./gtm.sh concrete_gtm_launch_draft_1028.py
Changes (Alex's agent asks 2-4, Edu's go):
 1. trigger 10 `ghl_form_submit` -> `cEvent - Lead` regex ^(generate_lead|ghl_form_submit)$
    (new site pushes generate_lead; ghl_form_submit kept until launch so the live go. GHL pages keep counting;
    drop it after launch). Tags on it: Ads Lead (29) + Meta Lead (22).
 2. Meta Lead (22) eventId = {{dlv - event_id}} (browser/CAPI dedup); advanced matching reads the new site's
    keys too (cJS vars accept ghl_user.*, flat keys, user_data.*; already-hashed values pass through).
 3. GA4 Lead (11) moved to a ghl_form_submit-only trigger: on the new site GA4 gets generate_lead from the
    server only (no double), old GHL pages keep sending `lead` until launch.
"""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6382574349/containers/267158903"
WS = f"{C}/workspaces/4"
W = svc.accounts().containers().workspaces()
GTM_ID = "GTM-53FXJRN4"


def find(kind, name):
    items = getattr(W, kind)().list(parent=WS).execute().get(kind[:-1], [])
    return next((i for i in items if i["name"] == name), None)


def upsert(kind, body):
    cur = find(kind, body["name"])
    api = getattr(W, kind)()
    if cur:
        r = api.update(path=cur["path"], body={**cur, **body}).execute()
        print("updated", kind, r["name"])
        return r
    r = api.create(parent=WS, body=body).execute()
    print("created", kind, r["name"])
    return r


def get(kind, id_):
    return getattr(W, kind)().get(path=f"{WS}/{kind}/{id_}").execute()


def put(kind, obj):
    r = getattr(W, kind)().update(path=obj["path"], body=obj).execute()
    print("updated", kind, r["name"])
    return r


def p(key, value, typ="template"):
    return {"type": typ, "key": key, "value": value}


def pick_js(keys, normalize):
    """cJS: first non-empty data layer value among keys; 64-hex (already SHA-256) passes through untouched."""
    return ("function() {\n"
            f"  var g = window.google_tag_manager && window.google_tag_manager['{GTM_ID}'];\n"
            "  var dl = g && g.dataLayer;\n  if (!dl) return undefined;\n"
            f"  var keys = {keys};\n"
            "  for (var i = 0; i < keys.length; i++) {\n"
            "    var v = dl.get(keys[i]);\n"
            "    if (v === undefined || v === null || v === '') continue;\n"
            "    v = String(v).trim();\n"
            "    if (/^[a-f0-9]{64}$/i.test(v)) return v.toLowerCase();\n"
            f"{normalize}"
            "  }\n  return undefined;\n}")


NORM_LOWER = "    return v.toLowerCase();\n"
NORM_PHONE = ("    var d = v.replace(/\\D/g, '');\n    if (d.length === 10) d = '1' + d;\n"
              "    if (d.length >= 11 && d.length <= 15) return d;\n")

# --- variables
upsert("variables", {"name": "dlv - event_id", "type": "v", "parameter": [
    p("dataLayerVersion", "2", "integer"), p("setDefaultValue", "false", "boolean"), p("name", "event_id")]})
v_em = upsert("variables", {"name": "cJS - Lead Email", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['ghl_user.email', 'email', 'em', 'user_data.email', 'user_data.email_address', 'user_data.sha256_email_address', 'user_data.em']",
    NORM_LOWER))]})
v_ph = upsert("variables", {"name": "cJS - Lead Phone", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['ghl_user.phone_raw', 'phone', 'ph', 'user_data.phone', 'user_data.phone_number', 'user_data.sha256_phone_number', 'user_data.ph']",
    NORM_PHONE))]})
v_fn = upsert("variables", {"name": "cJS - Lead First Name", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['ghl_user.first_name', 'first_name', 'fn', 'user_data.first_name', 'user_data.address.first_name', 'user_data.fn']",
    NORM_LOWER))]})
v_ln = upsert("variables", {"name": "cJS - Lead Last Name", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['ghl_user.last_name', 'last_name', 'ln', 'user_data.last_name', 'user_data.address.last_name', 'user_data.ln']",
    NORM_LOWER))]})

# --- triggers
t10 = get("triggers", "10")
t10["name"] = "cEvent - Lead (generate_lead + old GHL)"
t10["customEventFilter"] = [{"type": "matchRegex", "parameter": [
    p("arg0", "{{_event}}"), p("arg1", "^(generate_lead|ghl_form_submit)$")]}]
t10.pop("filter", None)
put("triggers", t10)
t_ghl = upsert("triggers", {"name": "cEvent - ghl_form_submit (old GHL pages only)", "type": "customEvent",
    "customEventFilter": [{"type": "equals", "parameter": [p("arg0", "{{_event}}"), p("arg1", "ghl_form_submit")]}]})

# --- tags
AM = {"fn": v_fn["name"], "ln": v_ln["name"], "ph": v_ph["name"], "em": v_em["name"]}
t = get("tags", "22")
t["parameter"] = [x for x in t["parameter"] if x["key"] != "eventId"] + [p("eventId", "{{dlv - event_id}}")]
for x in t["parameter"]:
    if x["key"] == "advancedMatchingList":
        for row in x["list"]:
            m = {i["key"]: i for i in row["map"]}
            if m["name"]["value"] in AM:
                m["value"]["value"] = "{{" + AM[m["name"]["value"]] + "}}"
put("tags", t)

t = get("tags", "11")
t["firingTriggerId"] = [t_ghl["triggerId"]]
put("tags", t)

st = W.getStatus(path=WS).execute()
print("workspace changes:", len(st.get("workspaceChange", [])), "conflicts:", len(st.get("mergeConflict", [])))
