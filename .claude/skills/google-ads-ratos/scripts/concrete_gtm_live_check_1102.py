"""Read-only: print live GTM-53FXJRN4 version."""
import sys
sys.path.insert(0, ".")
from gtm_setup import gtm_service
v = gtm_service().accounts().containers().versions().live(parent="accounts/6382574349/containers/267158903").execute()
print(v["containerVersionId"], v.get("name"))
