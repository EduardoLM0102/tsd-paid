"""Cool Hand lead funnel -> Command Center (funnels/cool-hand-electric). Read-only on Google Ads + CallRail.

Builds one row per DAY per campaign from START to today, so the page can sum any range (today, yesterday, last N days, custom):
  website path : ad clicks -> number taps ('Click to call', GTM tel: tag) -> website calls (CallRail Website pool)
                 -> answered -> 60s+ ; plus calls uploaded back to Google ('Phone Call', All conv.)
  button path  : calls placed from the ad call button (Google phone_calls) -> answered (CallRail 'Google Ads' tracker)
                 -> 60s+ ('Calls from ads')
  forms        : [TSD] Contact Form + [TSD] Book Now Form
Website calls are tied to a campaign by matching the call's gclid against Google's click_view (call day and the 3 days
before); calls without a match are kept as 'unattributed'. Days are America/Chicago (the account's time zone).

Run:   ./tsd.sh <abs path to this file>          (writes funnel/funnel_<today>.json next to this file)
Then:  ArtifactData set funnels/cool-hand-electric with file_path = that JSON (Command Center artifact 1gah5xuCXDADf4kYVYp95q)
"""
import sys, os, json, datetime as dt, urllib.request, urllib.parse
from zoneinfo import ZoneInfo
SCRIPTS = os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"
sys.path.insert(0, SCRIPTS)
from lib import init_client
import callrail

CID = "9865206319"
CR_ACC, CR_CO = "ACC019e095affd97f04849c939538f341f1", "COM019e095b00b772089f5a2f01ffb837bc"
START = "2026-08-10"                       # Search campaigns launched
CALLRAIL_FROM = "2026-10-10"               # pool swapping + call asset on 469-351-1738 from this day
TAPS, BTN60, UPLOAD = "Click to call", "Calls from ads", "Phone Call"
FORMS = {"[TSD] Contact Form", "[TSD] Book Now Form"}
BUTTON_NUMBER = "+14693511738"
KEYS = ("spend", "clicks", "taps", "webCalls", "webAnswered", "webQualified", "uploaded", "btnPlaced", "btnQualified", "forms")

now_ct = dt.datetime.now(ZoneInfo("America/Chicago"))
today = now_ct.date().isoformat()
ga = init_client().get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))


def cr_get(path, **p):
    url = f"https://api.callrail.com/v3/a/{CR_ACC}{path}?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"Authorization": f'Token token="{callrail.KEY}"'})
    return json.load(urllib.request.urlopen(req, timeout=60))


days = {}   # date -> {"campaigns": {name: row}, "unattributed": {...}, "button": {...}}
def day(d):
    return days.setdefault(d, {"campaigns": {}, "unattributed": {"webCalls": 0, "webAnswered": 0, "webQualified": 0},
                               "button": {"calls": 0, "answered": 0, "qualified": 0}})
def row(d, name, ctype):
    return day(d)["campaigns"].setdefault(name, dict({"name": name, "type": ctype}, **{k: 0 for k in KEYS}))
ctype = lambda ch: "youtube" if ch in ("DEMAND_GEN", "VIDEO") else "search"
types = {}

# Google Ads, daily
for r in q(f"""SELECT segments.date, campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.phone_calls
    FROM campaign WHERE segments.date BETWEEN '{START}' AND '{today}' AND campaign.advertising_channel_type != 'LOCAL_SERVICES'"""):
    m = r.metrics
    if not (m.cost_micros or m.clicks or m.phone_calls): continue
    t = ctype(r.campaign.advertising_channel_type.name); types[r.campaign.name] = t
    x = row(r.segments.date, r.campaign.name, t)
    x["spend"] += m.cost_micros / 1e6; x["clicks"] += m.clicks; x["btnPlaced"] += m.phone_calls
for r in q(f"""SELECT segments.date, campaign.name, campaign.advertising_channel_type, segments.conversion_action_name, metrics.all_conversions
    FROM campaign WHERE segments.date BETWEEN '{START}' AND '{today}' AND metrics.all_conversions > 0 AND campaign.advertising_channel_type != 'LOCAL_SERVICES'"""):
    a, v = r.segments.conversion_action_name, r.metrics.all_conversions
    key = {TAPS: "taps", BTN60: "btnQualified", UPLOAD: "uploaded"}.get(a) or ("forms" if a in FORMS else None)
    if not key: continue
    t = ctype(r.campaign.advertising_channel_type.name); types[r.campaign.name] = t
    row(r.segments.date, r.campaign.name, t)[key] += v

# CallRail, per call
trackers = cr_get("/trackers.json", company_id=CR_CO, per_page=100, status="all", fields="id,name,type,tracking_numbers")["trackers"]
pool_ids = {t["id"] for t in trackers if t["type"] == "session"}
pool_numbers = {n for t in trackers if t["type"] == "session" for n in t.get("tracking_numbers", [])}
gclid_cache = {}
def campaign_for_gclid(gclid, call_day):
    if gclid not in gclid_cache:
        gclid_cache[gclid] = None
        for back in range(4):
            d = (dt.date.fromisoformat(call_day) - dt.timedelta(days=back)).isoformat()
            rows = q(f"SELECT campaign.name, click_view.gclid FROM click_view WHERE segments.date = '{d}' AND click_view.gclid = '{gclid}'")
            if rows: gclid_cache[gclid] = rows[0].campaign.name; break
    return gclid_cache[gclid]

page, calls = 1, []
while True:
    d = cr_get("/calls.json", company_id=CR_CO, start_date=CALLRAIL_FROM, end_date=today, per_page=250, page=page,
               fields="tracking_phone_number,tracker_id,answered,duration,gclid,start_time")
    calls += d.get("calls", [])
    if page >= d.get("total_pages", 1): break
    page += 1
for c in calls:
    cday = dt.datetime.fromisoformat(c["start_time"]).astimezone(ZoneInfo("America/Chicago")).date().isoformat()
    num, dur, ans = c.get("tracking_phone_number"), c.get("duration") or 0, int(bool(c.get("answered")))
    if num == BUTTON_NUMBER:
        b = day(cday)["button"]; b["calls"] += 1; b["answered"] += ans; b["qualified"] += int(dur >= 60)
    elif c.get("tracker_id") in pool_ids or num in pool_numbers:
        name = campaign_for_gclid(c["gclid"], cday) if c.get("gclid") else None
        tgt = row(cday, name, types.get(name, "search")) if name else day(cday)["unattributed"]
        tgt["webCalls"] += 1; tgt["webAnswered"] += ans; tgt["webQualified"] += int(dur >= 60)

out_days = []
for d in sorted(days):
    camps = []
    for x in days[d]["campaigns"].values():
        for k in ("spend", "taps", "uploaded", "btnQualified", "forms"): x[k] = round(x[k], 2)
        camps.append(x)
    out_days.append({"date": d, "campaigns": camps, "unattributed": days[d]["unattributed"], "button": days[d]["button"]})

doc = {
    "client": "cool-hand-electric",
    "title": "Lead funnel",
    "updatedAt": now_ct.isoformat(timespec="minutes"),
    "dataFrom": START,
    "dataThrough": today,
    "callrailFrom": CALLRAIL_FROM,
    "timeZone": "America/Chicago",
    "source": "Google Ads API (9865206319) + CallRail API (Coolhand Electrics). Refreshed by Claude on request and during checks.",
    "notes": [
        "Taps and calls don't match one to one: some people tap and hang up, others read the number and dial by hand.",
        "Website calls are tied to a campaign through the visitor's Google click ID. Calls without one show as not tied to a campaign.",
        "Ad-button calls answered come from CallRail and can't be split by campaign.",
        "Google Ads numbers for today and yesterday can still change for a few hours as Google finishes processing.",
    ],
    "days": out_days,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "funnel", f"funnel_{today}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(doc, open(out, "w"), separators=(",", ":"))
print("wrote", out, f"({os.path.getsize(out) // 1024} KB, {len(out_days)} days, {len(calls)} CallRail calls)")
for d in out_days[-4:]:
    s = [c for c in d["campaigns"] if c["type"] == "search"]
    print(f"  {d['date']} Search clicks {sum(c['clicks'] for c in s)} taps {sum(c['taps'] for c in s):.0f} btn placed {sum(c['btnPlaced'] for c in s)}"
          f" 60s {sum(c['btnQualified'] for c in s):.0f} | web calls {sum(c['webCalls'] for c in d['campaigns'])}+{d['unattributed']['webCalls']}u | CR button {d['button']}")
