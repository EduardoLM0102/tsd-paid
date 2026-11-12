"""Spencer Air GTM-KT5RPTP: launch-prep DRAFT for Alex's new site (2026-10-22). Edits Default Workspace only, NO publish.
Run: ./gtm.sh spencer_gtm_launch_draft_1022.py
Changes:
 1. new var `dlv - event_id`; Meta Lead (43) eventId = {{dlv - event_id}}  (browser/server dedup)
 2. pause GA4 generate_lead (63)  (server MP sends it)
 3. Meta pixel vars 39 + 11 -> 1258997717469696 (same pixel as CAPI)
 4. Meta tags 43/51/55/65 require ad_storage consent; listener tag pushes `consent_marketing_granted`
    on the site's `spencer:consent-change` event, added as 2nd trigger on Meta PageView (65)
 5. Enhanced conv: email/phone normalized before hashing (E.164 phone); Ads Lead (72) sequenced after
    User-provided Data (59); Meta `ph` uses the E.164 phone too
 6. CallRail tag (70) blocked on the new site (site boot script already loads swap.js)
"""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
C = "accounts/6000941581/containers/31091984"
WS = f"{C}/workspaces/10"
W = svc.accounts().containers().workspaces()
PIXEL = "1258997717469696"
AD_CONSENT = {"consentStatus": "needed", "consentType": {"type": "list", "list": [{"type": "template", "value": "ad_storage"}]}}


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


# --- variables
upsert("variables", {"name": "dlv - event_id", "type": "v", "parameter": [
    p("dataLayerVersion", "2", "integer"), p("setDefaultValue", "false", "boolean"), p("name", "event_id")]})
upsert("variables", {"name": "JS - spencerBoot callrail", "type": "j", "parameter": [p("name", "__spencerBoot.callrail")]})
upsert("variables", {"name": "cJS - Phone E164", "type": "jsm", "parameter": [p("javascript",
    "function() {\n  var p = {{dlv - Phone}};\n  if (!p) return undefined;\n  var d = String(p).replace(/\\D/g, '');\n"
    "  if (d.length === 10) d = '1' + d;\n  if (d.length < 11 || d.length > 15) return undefined;\n  return '+' + d;\n}")]})
for vid in ("39", "11"):
    v = get("variables", vid)
    for prm in v["parameter"]:
        if prm["key"] == "value":
            prm["value"] = PIXEL
    put("variables", v)
OLD_E = "var email= {{dlv - Email}};"
NEW_E = "var email= {{dlv - Email}};\n  if (!email) return undefined;\n  email = String(email).trim().toLowerCase();"
OLD_P = "var phone= {{dlv - Phone}};"
NEW_P = "var phone= {{cJS - Phone E164}};\n  if (!phone) return undefined;"
for vid, old, new in (("48", OLD_E, NEW_E), ("49", OLD_P, NEW_P)):
    v = get("variables", vid)
    js = v["parameter"][0]["value"]
    if old in js and new not in js:
        v["parameter"][0]["value"] = js.replace(old, new, 1)
        put("variables", v)
    else:
        print("skip var", vid, "(already normalized or pattern missing)")

# --- triggers
t_consent = upsert("triggers", {"name": "cEvent - Consent Marketing Granted", "type": "customEvent",
    "customEventFilter": [{"type": "equals", "parameter": [p("arg0", "{{_event}}"), p("arg1", "consent_marketing_granted")]}]})
t_newsite = upsert("triggers", {"name": "Block - New Site (boot loads CallRail)", "type": "pageview",
    "filter": [{"type": "equals", "parameter": [p("arg0", "{{JS - spencerBoot callrail}}"), p("arg1", "true")]}]})

# --- consent listener tag
upsert("tags", {"name": "cHTML - Spencer Consent Listener", "type": "html", "firingTriggerId": ["2147479553"],
    "tagFiringOption": "oncePerLoad", "parameter": [p("supportDocumentWrite", "false", "boolean"), p("html",
    "<script>\n(function () {\n  if (window.__tsdConsentListener) return;\n  window.__tsdConsentListener = true;\n"
    "  window.addEventListener('spencer:consent-change', function (e) {\n"
    "    if (e && e.detail && e.detail.marketing) {\n      window.dataLayer = window.dataLayer || [];\n"
    "      window.dataLayer.push({ event: 'consent_marketing_granted' });\n    }\n  });\n})();\n</script>")]})

# --- tags
for tid in ("43", "51", "55", "65"):
    t = get("tags", tid)
    t["consentSettings"] = AD_CONSENT
    if tid == "43":
        t["parameter"] = [x for x in t["parameter"] if x["key"] != "eventId"] + [p("eventId", "{{dlv - event_id}}")]
        for x in t["parameter"]:
            if x["key"] == "advancedMatchingList":
                for row in x["list"]:
                    m = {i["key"]: i for i in row["map"]}
                    if m["name"]["value"] == "ph":
                        m["value"]["value"] = "{{cJS - Phone E164}}"
    if tid == "65" and t_consent["triggerId"] not in t["firingTriggerId"]:
        t["firingTriggerId"].append(t_consent["triggerId"])
    put("tags", t)
t = get("tags", "63"); t["paused"] = True; put("tags", t)
t = get("tags", "72"); t["setupTag"] = [{"tagName": "Google Ads | Event | User-provided Data", "stopOnSetupFailure": False}]; put("tags", t)
t = get("tags", "70"); t["blockingTriggerId"] = [t_newsite["triggerId"]]; put("tags", t)

st = W.getStatus(path=WS).execute()
print("workspace changes:", len(st.get("workspaceChange", [])), "conflicts:", len(st.get("mergeConflict", [])))
