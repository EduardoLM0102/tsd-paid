"""Read-only: Spencer GTM-KT5RPTP lead tags (63 GA4 generate_lead, 72 Ads Lead, 43 Meta Lead) + their triggers, 2026-10-23."""
import sys, json
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service(); C = "accounts/6000941581/containers/31091984"; W = C + "/workspaces/12"
CC = svc.accounts().containers()
print("live:", CC.versions().live(parent=C).execute()["containerVersionId"])
st = CC.workspaces().getStatus(path=W).execute(); print("workspace changes:", len(st.get("workspaceChange", [])))
tags = CC.workspaces().tags().list(parent=W).execute()["tag"]
trg = {t["triggerId"]: t for t in CC.workspaces().triggers().list(parent=W).execute()["trigger"]}
for t in tags:
    if t["tagId"] in ("63", "72", "43") or "lead" in t["name"].lower() or "ga4" in t["name"].lower():
        print(f'\n[{t["tagId"]}] {t["name"]} type={t["type"]} paused={t.get("paused", False)} consent={t.get("consentSettings")}')
        print("   firing:", [(i, trg[i]["name"], trg[i]["type"]) for i in t.get("firingTriggerId", [])], "blocking:", t.get("blockingTriggerId"))
        print("   params:", json.dumps([(p["key"], p.get("value", p.get("list", ""))) for p in t.get("parameter", [])])[:1200])
for i in sorted({i for t in tags if t["tagId"] in ("63", "72") for i in t.get("firingTriggerId", [])}):
    print("\nTRIGGER", i, json.dumps(trg[i])[:900])
