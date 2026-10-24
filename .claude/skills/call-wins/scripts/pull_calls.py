"""Pull one client's CallRail calls + recordings for a date range. Read-only (GET only).

  python pull_calls.py <client-slug> <start YYYY-MM-DD> <end YYYY-MM-DD> [--no-audio]
  python pull_calls.py --account ACC... --company COM... --out <dir> <start> <end>

<client-slug> = a key in paid/funnels/clients.json (holds each client's CallRail account + company id).
Writes into _pessoal/call-wins/<slug>/ (gitignored: recordings carry customer PII):
  calls.json          every call in the range, with source/gclid/recording metadata
  audio/<call id>.mp3 one file per call that has a recording
Re-running skips recordings already downloaded.
Builds the URL by hand: urlencode turns the commas in `fields` into %2C, which CallRail rejects (400)."""
import argparse, json, os, sys, time, urllib.error, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
FIELDS = ("source,source_name,medium,campaign,keywords,gclid,first_call,answered,duration,start_time,"
          "landing_page_url,utm_source,utm_medium,utm_campaign,recording,recording_duration,"
          "customer_name,customer_city,customer_state,tracking_phone_number,business_phone_number,lead_status,tags")

env = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, ".env.callrail"), encoding="utf-8")
           if "=" in l and not l.startswith("#"))
KEY = env["CALLRAIL_API_KEY"]


def get(url, auth=True, raw=False, tries=6):
    headers = {"Authorization": f'Token token="{KEY}"'} if auth else {}
    for i in range(tries):
        try:
            resp = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120)
            return resp.read() if raw else json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                wait = 30 * (i + 1)
                print(f"  CallRail rate limit (429), waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            raise


ap = argparse.ArgumentParser()
ap.add_argument("args", nargs="+", help="<slug> <start> <end>, or <start> <end> with --account/--company/--out")
ap.add_argument("--account"); ap.add_argument("--company"); ap.add_argument("--out")
ap.add_argument("--no-audio", action="store_true", help="only calls.json, skip recordings")
a = ap.parse_args()

if a.account:
    start, end = a.args
    acc, comp, out = a.account, a.company, a.out
else:
    slug, start, end = a.args
    clients = json.load(open(os.path.join(ROOT, "paid", "funnels", "clients.json"), encoding="utf-8"))["clients"]
    if slug not in clients:
        sys.exit(f"'{slug}' not in paid/funnels/clients.json. Known: {', '.join(clients)}")
    acc, comp = clients[slug]["callrailAccount"], clients[slug]["callrailCompany"]
    out = os.path.join(ROOT, "_pessoal", "call-wins", slug)

os.makedirs(os.path.join(out, "audio"), exist_ok=True)

calls, page = [], 1
while True:
    d = get(f"https://api.callrail.com/v3/a/{acc}/calls.json?company_id={comp}&start_date={start}&end_date={end}"
            f"&per_page=250&page={page}&fields={FIELDS}")
    calls += d["calls"]
    if page >= d.get("total_pages", 1):
        break
    page += 1
    time.sleep(0.5)
json.dump(calls, open(os.path.join(out, "calls.json"), "w", encoding="utf-8"), indent=1)

recorded = [c for c in calls if c.get("recording") and (c.get("recording_duration") or 0)]
print(f"{len(calls)} calls, {len(recorded)} with a recording -> {out}")
if a.no_audio:
    sys.exit()

new = 0
for c in recorded:
    fn = os.path.join(out, "audio", f"{c['id']}.mp3")
    if os.path.exists(fn):
        continue
    try:
        link = get(c["recording"])["url"]  # API returns a pointer {"url": ...}, not the audio
        open(fn, "wb").write(get(link, auth=False, raw=True))
        new += 1
        print(f"  {c['id']}  {c.get('start_time', '')[:16]}  {c.get('source_name') or c.get('source')}", flush=True)
    except Exception as e:
        print(f"  {c['id']} FAILED: {e}", flush=True)
    time.sleep(0.3)
print(f"{new} new recordings downloaded")
