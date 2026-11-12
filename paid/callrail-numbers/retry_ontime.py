import json, urllib.request, time, subprocess, sys
env = dict(l.strip().split("=",1) for l in open("../../.env.callrail") if "=" in l and not l.startswith("#"))
H={"Authorization": f'Token token="{env["CALLRAIL_API_KEY"]}"'}
get=lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
for attempt in range(8):
    time.sleep(600)
    d=json.load(open("trackers_raw.json")); pending=[x for x in d if "error" in x]
    if not pending: break
    try:
        for x in pending:
            b=f"https://api.callrail.com/v3/a/{x['account']['id']}"
            x["companies"]=get(b+"/companies.json?per_page=250")["companies"]
            x["trackers"]=get(b+"/trackers.json?per_page=250")["trackers"]
            del x["error"]
        json.dump(d, open("trackers_raw.json","w"), indent=1)
        subprocess.run([sys.executable, "build_sheet.py"]); print("DONE attempt", attempt); break
    except Exception as e: print("attempt", attempt, e, flush=True)
