"""Read-only CallRail API v3 helper (TSD agency account "TopServ Digital Clients").

Key lives in topserv-workspace/.env.callrail (gitignored): CALLRAIL_API_KEY, CALLRAIL_ACCOUNT_ID.
GET only: the key carries the creating user's full rights, never use it to write.

  python3 callrail.py /companies.json per_page=250
  python3 callrail.py /integrations.json company_id=580688522
  python3 callrail.py /calls.json company_id=580688522 start_date=2026-09-15 fields=source,gclid,duration
"""
import json, os, sys, urllib.request, urllib.parse

ENV = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env.callrail")
env = dict(l.strip().split("=", 1) for l in open(os.path.abspath(ENV)) if "=" in l and not l.startswith("#"))
KEY, ACC = env["CALLRAIL_API_KEY"], env["CALLRAIL_ACCOUNT_ID"]


def get(path, **params):
    url = f"https://api.callrail.com/v3/a/{ACC}{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f'Token token="{KEY}"'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_all(path, key, **params):
    """Paginate a list endpoint (calls, trackers, companies) and return every record."""
    out, page = [], 1
    while True:
        d = get(path, per_page="250", page=str(page), **params)
        out += d.get(key, [])
        if page >= d.get("total_pages", 1):
            return out
        page += 1


if __name__ == "__main__":
    print(json.dumps(get(sys.argv[1], **dict(a.split("=", 1) for a in sys.argv[2:])), indent=1))
