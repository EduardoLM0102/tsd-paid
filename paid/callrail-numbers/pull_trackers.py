"""Pull every CallRail tracking number across all accounts the key can see -> trackers_raw.json (GET only)."""
import json, os, urllib.request, urllib.parse, time

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(l.strip().split("=", 1) for l in open(os.path.join(HERE, "..", "..", ".env.callrail")) if "=" in l and not l.startswith("#"))
KEY = env["CALLRAIL_API_KEY"]


def get(url, **params):
    url += ("?" + urllib.parse.urlencode(params)) if params else ""
    req = urllib.request.Request(url, headers={"Authorization": f'Token token="{KEY}"'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_all(url, key, **params):
    out, page = [], 1
    while True:
        d = get(url, per_page="250", page=str(page), **params)
        out += d.get(key, [])
        if page >= d.get("total_pages", 1):
            return out
        page += 1
        time.sleep(0.5)


accounts = get_all("https://api.callrail.com/v3/a.json", "accounts")
result = []
for a in accounts:
    base = f"https://api.callrail.com/v3/a/{a['id']}"
    try:
        companies = get_all(base + "/companies.json", "companies")
        trackers = get_all(base + "/trackers.json", "trackers")
    except Exception as e:
        print("ERR", a["name"], e)
        result.append({"account": a, "error": str(e)})
        continue
    print(a["name"], len(companies), "companies", len(trackers), "trackers")
    result.append({"account": a, "companies": companies, "trackers": trackers})
    time.sleep(1)

json.dump(result, open(os.path.join(HERE, "trackers_raw.json"), "w"), indent=1)
