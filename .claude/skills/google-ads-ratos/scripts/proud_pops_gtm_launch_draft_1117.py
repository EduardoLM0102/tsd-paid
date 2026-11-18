"""Proud Pops GTM-WBFDB6L8: launch DRAFT for Alex's new site (2026-11-17). Default Workspace 45 only, NO publish.
Run: ./gtm.sh proud_pops_gtm_launch_draft_1117.py
Changes (Alex's 11-17 asks to Edu):
 1. New trigger `cEvent - lead_submitted (site forms)` (/careers excluded, same guard as cEvent - Lead).
    Fires G.Ads - Lead (82), G.Ads - User-provided Data (94), Meta - Lead (111).
    GA4 - Lead (90) NOT added: the site sends generate_lead server-side (Measurement Protocol) -> no double count.
    GHL widgets (/schedule, trade pages) keep ghl_form_submit -> cEvent - Lead, unchanged.
 2. Meta - Lead (111) eventId = {{dlv - event_id}} (browser/CAPI dedup). Advanced matching reads the new site's
    keys too (cJS vars, same as Concrete v4: flat, user_data.*, ghl_user.*; 64-hex hashed values pass through).
 3. Consent: Meta tags (68, 71, 102, 111, 112, 114) + CallRail (104) require ad_storage.
    !! Publish only at the DNS switch: the current Lovable site defaults consent to DENIED, so on the old site
    this would silence Meta for everyone who doesn't click Accept.
"""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6255217830/containers/198527160"
WS = f"{C}/workspaces/45"
W = svc.accounts().containers().workspaces()
GTM_ID = "GTM-WBFDB6L8"

st = W.getStatus(path=WS).execute()
if st.get("workspaceChange"):
    sys.exit(f"ABORT: workspace 45 already has {len(st['workspaceChange'])} unpublished changes")


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
    print("updated", kind, r["tagId"] if kind == "tags" else "", r["name"])
    return r


def p(key, value, typ="template"):
    return {"type": typ, "key": key, "value": value}


def pick_js(keys, normalize):
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
    "['email', 'em', 'user_data.email', 'user_data.email_address', 'user_data.sha256_email_address', 'user_data.em', 'ghl_user.email']",
    NORM_LOWER))]})
v_ph = upsert("variables", {"name": "cJS - Lead Phone", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['phone', 'ph', 'user_data.phone', 'user_data.phone_number', 'user_data.sha256_phone_number', 'user_data.ph', 'ghl_user.phone_raw']",
    NORM_PHONE))]})
v_fn = upsert("variables", {"name": "cJS - Lead First Name", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['first_name', 'fn', 'user_data.first_name', 'user_data.address.first_name', 'user_data.fn', 'ghl_user.first_name']",
    NORM_LOWER))]})
v_ln = upsert("variables", {"name": "cJS - Lead Last Name", "type": "jsm", "parameter": [p("javascript", pick_js(
    "['last_name', 'ln', 'user_data.last_name', 'user_data.address.last_name', 'user_data.ln', 'ghl_user.last_name']",
    NORM_LOWER))]})

# --- trigger
t_ls = upsert("triggers", {"name": "cEvent - lead_submitted (site forms)", "type": "customEvent",
    "customEventFilter": [{"type": "equals", "parameter": [p("arg0", "{{_event}}"), p("arg1", "lead_submitted")]}],
    "filter": [{"type": "contains", "parameter": [p("arg0", "{{Page Path}}"), p("arg1", "/careers"),
                                                  p("negate", "true", "boolean")]}]})
TID = t_ls["triggerId"]

# --- tags: add trigger
for tid in ("82", "94", "111"):
    t = get("tags", tid)
    if TID not in t.get("firingTriggerId", []):
        t["firingTriggerId"] = t.get("firingTriggerId", []) + [TID]
    if tid == "111":
        t["parameter"] = [x for x in t["parameter"] if x["key"] != "eventId"] + [p("eventId", "{{dlv - event_id}}")]
        AM = {"fn": v_fn["name"], "ln": v_ln["name"], "ph": v_ph["name"], "em": v_em["name"]}
        for x in t["parameter"]:
            if x["key"] == "advancedMatchingList":
                for row in x["list"]:
                    m = {i["key"]: i for i in row["map"]}
                    if m["name"]["value"] in AM:
                        m["value"]["value"] = "{{" + AM[m["name"]["value"]] + "}}"
    put("tags", t)

# --- consent: Meta + CallRail need ad_storage
AD_CONSENT = {"consentStatus": "needed", "consentType": {"type": "list", "list": [{"type": "template", "value": "ad_storage"}]}}
for tid in ("68", "71", "102", "111", "112", "114", "104"):
    t = get("tags", tid)
    t["consentSettings"] = AD_CONSENT
    put("tags", t)

st = W.getStatus(path=WS).execute()
print("workspace changes:", len(st.get("workspaceChange", [])), "conflicts:", len(st.get("mergeConflict", [])))
qp = W.quick_preview(path=WS).execute()
print("compilerError:", qp.get("compilerError"), "| preview ok:", bool(qp.get("containerVersion")))
