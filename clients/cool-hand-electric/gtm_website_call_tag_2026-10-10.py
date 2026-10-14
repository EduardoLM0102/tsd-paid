"""Cool Hand 2026-10-10: GTM tag for Google 'Calls from website' on go.coolhandelectric.com only.
ALREADY APPLIED in workspace 9 on 2026-10-10, don't re-run.
Tag type awcc (Google Ads Calls from Website Conversion): AW-16750381108 / 1SZGCMuRj5gdELSQmrM- (action 7835207883),
replaces 469-351-1738 with a Google forwarding number for ad visitors. Trigger = Page View where Page Hostname = go.coolhandelectric.com
(the same container runs on the main site, which shows 469-550-1102 and must not get this tag).
Run: ./gtm.sh <abs path to this file>
"""
import os
import sys, json
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from gtm_setup import gtm_service
svc = gtm_service(); WS = "accounts/6370314680/containers/260649558/workspaces/9"
W = svc.accounts().containers().workspaces()
def tp(k, v): return {"type": "template", "key": k, "value": v}
trg = W.triggers().create(parent=WS, body={
    "name": "Page View - go. subdomain", "type": "pageview",
    "filter": [{"type": "equals", "parameter": [tp("arg0", "{{Page Hostname}}"), tp("arg1", "go.coolhandelectric.com")]}],
}).execute()
print("trigger", trg["triggerId"], trg["name"])
tag = W.tags().create(parent=WS, body={
    "name": "05 | G Ads - Calls from Website (go.)", "type": "awcc",
    "parameter": [tp("conversionId", "16750381108"), tp("conversionLabel", "1SZGCMuRj5gdELSQmrM-"), tp("phoneConversionNumber", "469-351-1738")],
    "firingTriggerId": [trg["triggerId"]], "tagFiringOption": "oncePerEvent",
}).execute()
print("tag", tag["tagId"], tag["name"], json.dumps(tag["parameter"]))
