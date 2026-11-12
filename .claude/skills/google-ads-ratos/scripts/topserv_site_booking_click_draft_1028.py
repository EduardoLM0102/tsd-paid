"""TopServ's own site GTM-PR3DRB45: booking_click GA4 event (plain event, not a key event) on every click to a
book.topservdigital.com link except /FDM (ebook). Built in a NEW workspace off live v3, because the Default Workspace holds
someone's unpublished Jan/Feb 2026 draft (Conversion Linker + Ads 'Diagnostic Call' conversion + deletes 3 paused Book Now
tags) that must not go live with this. Creates a version (NOT published) + a user env serving it, for the headless test.
AT task 0092f797 (Internal Request, 10-27)."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
A, CID = "6273170749", "208573125"
C = f"accounts/{A}/containers/{CID}"
if CC.versions().live(parent=C).execute()["containerVersionId"] != "3":
    sys.exit("ABORT: live is not v3")

ws = CC.workspaces().create(parent=C, body={"name": "TSD 10-28 booking_click",
    "description": "booking_click GA4 event on book.topservdigital.com links (excl /FDM)"}).execute()
W = ws["path"]
print("workspace", ws["workspaceId"])

trig = CC.workspaces().triggers().create(parent=W, body={
    "name": "Link Click - Booking (book.topservdigital.com, excl /FDM)",
    "type": "linkClick",
    "filter": [
        {"type": "contains", "parameter": [
            {"type": "template", "key": "arg0", "value": "{{Click URL}}"},
            {"type": "template", "key": "arg1", "value": "book.topservdigital.com"}]},
        {"type": "matchRegex", "parameter": [
            {"type": "template", "key": "arg0", "value": "{{Click URL}}"},
            {"type": "template", "key": "arg1", "value": "book\\.topservdigital\\.com/fdm"},
            {"type": "boolean", "key": "ignore_case", "value": "true"},
            {"type": "boolean", "key": "negate", "value": "true"}]},
    ],
    # links open in the same tab, so hold navigation (max 2s) until the GA4 hit is out
    "waitForTags": {"type": "boolean", "value": "true"},
    "waitForTagsTimeout": {"type": "template", "value": "2000"},
    "checkValidation": {"type": "boolean", "value": "false"},
}).execute()
print("trigger", trig["triggerId"])

tag = CC.workspaces().tags().create(parent=W, body={
    "name": "GA4 - booking_click",
    "type": "gaawe",
    "parameter": [
        {"type": "boolean", "key": "sendEcommerceData", "value": "false"},
        {"type": "boolean", "key": "enhancedUserId", "value": "false"},
        {"type": "template", "key": "eventName", "value": "booking_click"},
        {"type": "template", "key": "measurementIdOverride", "value": "{{Constant - Measurement id}}"},
        {"type": "list", "key": "eventSettingsTable", "list": [
            {"type": "map", "map": [
                {"type": "template", "key": "parameter", "value": "link_url"},
                {"type": "template", "key": "parameterValue", "value": "{{Click URL}}"}]}]},
    ],
    "firingTriggerId": [trig["triggerId"]],
    "tagFiringOption": "oncePerEvent",
}).execute()
print("tag", tag["tagId"])

r = CC.workspaces().create_version(path=W, body={"name": "TSD 10-28 booking_click",
    "notes": "GA4 event booking_click (plain event) on clicks to book.topservdigital.com links except /FDM. link_url param = Click URL. AT task 0092f797."}).execute()
v = r["containerVersion"]
print("version", v["containerVersionId"], "compilerError:", r.get("compilerError"))
env = CC.environments().create(parent=C, body={"accountId": A, "containerId": CID,
    "name": "TSD test v" + v["containerVersionId"], "type": "user", "containerVersionId": v["containerVersionId"]}).execute()
print(json.dumps({"version": v["containerVersionId"], "envId": env["environmentId"], "auth": env["authorizationCode"]}))
