"""Read-only: dump Meta Pixel template code section (live GTM-53FXJRN4) to see what gates the param builder injection."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); CC = svc.accounts().containers()
C = "accounts/6382574349/containers/267158903"
live = CC.versions().live(parent=C).execute()
t = [o for o in live["customTemplate"] if o["name"] == "Meta Pixel"][0]["templateData"]
code = t.split("___SANDBOXED_JS_FOR_WEB_TEMPLATE___")[1].split("___WEB_PERMISSIONS___")[0]
open(sys.argv[1], "w").write(code)
print(len(code))
