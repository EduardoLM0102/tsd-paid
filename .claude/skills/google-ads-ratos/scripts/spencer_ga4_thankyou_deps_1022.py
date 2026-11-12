"""Spencer GA4 313187998: key events, audiences, event create/modify rules mentioning thank-you (read-only)."""
import sys, json
sys.path.insert(0, ".")
from googleapiclient.discovery import build
from ga4_setup import ga4_credentials
a = build("analyticsadmin", "v1alpha", credentials=ga4_credentials(), cache_discovery=False)
P = "properties/313187998"
for k in a.properties().keyEvents().list(parent=P).execute().get("keyEvents", []):
    print("KEY EVENT", k["eventName"], k.get("countingMethod"))
for au in a.properties().audiences().list(parent=P, pageSize=200).execute().get("audiences", []):
    s = json.dumps(au)
    print("AUDIENCE", au["displayName"], "| thank-you in rule:", "thank" in s.lower())
    if "thank" in s.lower() or "Lead" in au["displayName"]: print("   ", json.dumps(au.get("filterClauses"))[:900])
for st in a.properties().dataStreams().list(parent=P).execute().get("dataStreams", []):
    for kind in ("eventCreateRules", "eventEditRules"):
        try:
            items = getattr(a.properties().dataStreams(), kind)().list(parent=st["name"]).execute()
            for it in items.get(kind, []):
                print(kind.upper(), st.get("displayName"), json.dumps(it)[:500])
        except Exception as e:
            print(kind, "err", str(e)[:120])
