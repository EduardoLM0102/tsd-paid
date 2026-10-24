"""CallRail calls pull for one company (agency account). Read-only.
  python3 callrail_calls_pull.py <company_id> <start YYYY-MM-DD> <end> <out.json>
Builds the URL by hand: callrail.py's urlencode turns the commas in `fields` into %2C, which CallRail rejects (400)."""
import json, os, sys, time, urllib.request
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
env = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, ".env.callrail")) if "=" in l and not l.startswith("#"))
KEY, ACC = env["CALLRAIL_API_KEY"], env["CALLRAIL_ACCOUNT_ID"]
FIELDS = ("source,source_name,gclid,first_call,duration,answered,landing_page_url,utm_source,utm_medium,utm_campaign,"
          "recording,recording_duration,customer_city,customer_name,tracking_phone_number,keywords,campaign,medium,lead_status,tags")
comp, start, end, out = sys.argv[1:5]
calls, page = [], 1
while True:
    url = (f"https://api.callrail.com/v3/a/{ACC}/calls.json?company_id={comp}&start_date={start}&end_date={end}"
           f"&per_page=250&page={page}&fields={FIELDS}")
    req = urllib.request.Request(url, headers={"Authorization": f'Token token="{KEY}"'})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    calls += d["calls"]
    if page >= d.get("total_pages", 1): break
    page += 1; time.sleep(0.5)
json.dump(calls, open(out, "w"), indent=1)
print(len(calls), "calls ->", out)
