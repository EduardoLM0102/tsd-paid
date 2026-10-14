"""Lead funnel builder for the Command Center (funnels/<slug>). Read-only on Google Ads + CallRail. One config per client in clients.json.

Per DAY per campaign (account time zone, LSA excluded):
  website path : ad clicks -> number taps -> website calls from ad visitors (CallRail website trackers; gclid or Google Ads/CPC source)
                 -> answered -> 60s+ ; plus calls CallRail sent back to Google (upload actions)
  button path  : calls placed from the ad's call button (Google phone_calls) -> answered (CallRail ad-extension tracker, only when
                 the call asset dials it) -> counted by Google (AD_CALL / Smart call actions)
  forms        : one source only (TSD form tags, or GA4 form events when the tags show nothing), never both
Website calls tie to campaigns by matching the call's gclid against Google's click_view (call day and 3 days before).
Website calls from people who didn't come from an ad are counted per day as webOther (shown as a note, not in the funnel).

Run:   ./tsd.sh <abs path to this file> --client <slug>     (or --all)
Out:   paid/funnels/<slug>/funnel_<today>.json   -> ArtifactData set funnels/<slug> (Command Center 1gah5xuCXDADf4kYVYp95q)
"""
import argparse, sys, os, re, json, time, glob, datetime as dt, urllib.request, urllib.parse, urllib.error
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client
import callrail

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "clients.json")))["clients"]
CH_TYPE = {"SEARCH": "search", "PERFORMANCE_MAX": "pmax", "SMART": "smart", "DEMAND_GEN": "youtube", "VIDEO": "youtube", "DISPLAY": "display"}
KEYS = ("spend", "clicks", "taps", "webCalls", "webAnswered", "webQualified", "uploaded", "btnPlaced", "btnQualified", "forms")
EXT_SOURCES = {"google_ad_extension", "mobile_ad_extension"}
NOT_WEB = EXT_SOURCES | {"offline", "facebook_all", "instagram_all", "google_my_business", "google_local_services_ads", "bing_ad_extension"}
DEFAULT_DAYS = 60
ga = init_client().get_service("GoogleAdsService")
digits = lambda n: re.sub(r"\D", "", n or "")[-10:]
ename = lambda v: getattr(v, "name", str(v))   # LSA action types come back as bare ints


def cr_get(acc, path, **p):
    url = f"https://api.callrail.com/v3/a/{acc}{path}?" + urllib.parse.urlencode(p)
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f'Token token="{callrail.KEY}"'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 1: time.sleep(10); continue   # one short retry, then fall back to the last CallRail numbers
            raise


def build(slug):
    c = CFG[slug]; cid = c["cid"]; acc, co = c["callrailAccount"], c["callrailCompany"]
    q = lambda s: list(ga.search(customer_id=cid, query=s))
    tz = q("SELECT customer.time_zone FROM customer")[0].customer.time_zone
    now = dt.datetime.now(ZoneInfo(tz)); today = now.date().isoformat()
    start = c.get("dataFrom") or (now.date() - dt.timedelta(days=DEFAULT_DAYS)).isoformat()
    cr_from = c.get("callrailFrom") or start

    # --- which conversion actions mean what -----------------------------------------------------------------------------------
    acts = q("""SELECT conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.phone_call_duration_seconds
        FROM conversion_action WHERE conversion_action.status = 'ENABLED'""")
    vol = {r.segments.conversion_action_name: r.metrics.all_conversions for r in q(
        "SELECT segments.conversion_action_name, metrics.all_conversions FROM customer WHERE segments.date DURING LAST_30_DAYS AND metrics.all_conversions > 0")}
    A = [{"name": r.conversion_action.name, "type": ename(r.conversion_action.type_), "cat": ename(r.conversion_action.category),
          "sec": r.conversion_action.phone_call_duration_seconds} for r in acts]
    sum30 = lambda names: sum(vol.get(n, 0) for n in names)
    web_types = {"WEBPAGE", "WEBPAGE_CODELESS", "GOOGLE_ANALYTICS_4_CUSTOM"}
    taps = [a["name"] for a in A if a["type"] == "CLICK_TO_CALL"] or \
           [a["name"] for a in A if a["type"] in web_types and re.search(r"phone|click.?to.?call|\btel\b", a["name"], re.I)]
    tag_forms = [a["name"] for a in A if a["type"] in ("WEBPAGE", "WEBPAGE_CODELESS") and a["cat"] in ("SUBMIT_LEAD_FORM", "BOOK_APPOINTMENT", "REQUEST_QUOTE")]
    ga4_forms = [a["name"] for a in A if a["type"] == "GOOGLE_ANALYTICS_4_CUSTOM" and re.search(r"ghl_|form_submit|request_|generate_lead", a["name"], re.I)
                 and not re.search(r"link_click|page_view|phone|mailto", a["name"], re.I)]
    forms = tag_forms if (tag_forms and sum30(tag_forms) >= sum30(ga4_forms)) or not ga4_forms else ga4_forms
    button = [a["name"] for a in A if a["type"] in ("AD_CALL", "SMART_CAMPAIGN_TRACKED_CALLS")]
    uploads = [a["name"] for a in A if a["type"] in ("UPLOAD_CLICKS", "UPLOAD_CALLS") and re.search(r"call", a["name"], re.I)]
    for k, v in (("taps", taps), ("forms", forms), ("button", button), ("uploads", uploads)):
        if c.get(k) is not None: locals()[k][:] = c[k]
    key_of = {**{n: "uploaded" for n in uploads}, **{n: "forms" for n in forms}, **{n: "btnQualified" for n in button}, **{n: "taps" for n in taps}}
    btn_secs = sorted({a["sec"] for a in A if a["name"] in button and a["sec"]})

    days = {}
    def day(d):
        return days.setdefault(d, {"campaigns": {}, "unattributed": {"webCalls": 0, "webAnswered": 0, "webQualified": 0},
                                   "button": {"calls": 0, "answered": 0, "qualified": 0}, "webOther": 0})
    types = {}
    def row(d, name, t):
        return day(d)["campaigns"].setdefault(name, dict({"name": name, "type": t}, **{k: 0 for k in KEYS}))

    for r in q(f"""SELECT segments.date, campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.phone_calls
        FROM campaign WHERE segments.date BETWEEN '{start}' AND '{today}' AND campaign.advertising_channel_type != 'LOCAL_SERVICES'"""):
        m = r.metrics
        if not (m.cost_micros or m.clicks or m.phone_calls): continue
        t = CH_TYPE.get(ename(r.campaign.advertising_channel_type), "other"); types[r.campaign.name] = t
        x = row(r.segments.date, r.campaign.name, t); x["spend"] += m.cost_micros / 1e6; x["clicks"] += m.clicks; x["btnPlaced"] += m.phone_calls
    for r in q(f"""SELECT segments.date, campaign.name, campaign.advertising_channel_type, segments.conversion_action_name, metrics.all_conversions
        FROM campaign WHERE segments.date BETWEEN '{start}' AND '{today}' AND metrics.all_conversions > 0 AND campaign.advertising_channel_type != 'LOCAL_SERVICES'"""):
        k = key_of.get(r.segments.conversion_action_name)
        if not k: continue
        t = CH_TYPE.get(ename(r.campaign.advertising_channel_type), "other"); types[r.campaign.name] = t
        row(r.segments.date, r.campaign.name, t)[k] += r.metrics.all_conversions

    # --- CallRail (may be rate-limited: then keep the last CallRail numbers, refresh everything from Google) -----------------
    asset_nums = sorted({r.asset.call_asset.phone_number for lvl in ("campaign_asset", "ad_group_asset", "customer_asset") for r in q(
        f"SELECT {'' if lvl == 'customer_asset' else 'campaign.status, '}asset.call_asset.phone_number FROM {lvl} WHERE {lvl}.field_type = 'CALL' AND {lvl}.status = 'ENABLED'"
        + ("" if lvl == "customer_asset" else " AND campaign.status = 'ENABLED'"))})
    cr_asof, cr_error = now.isoformat(timespec="minutes"), None
    calls = []
    try:
        trs = cr_get(acc, "/trackers.json", company_id=co, per_page=100, status="active", fields="id,name,type,tracking_numbers,source")["trackers"]
        ext_nums = {digits(n) for t in trs if (t.get("source") or {}).get("type") in EXT_SOURCES for n in t.get("tracking_numbers") or []}
        web_ids = {t["id"] for t in trs if t["type"] == "session" or (t["type"] == "source" and (t.get("source") or {}).get("type") not in NOT_WEB)}
        button_tracked = bool(asset_nums) and any(digits(n) in ext_nums for n in asset_nums)
        calls, page = [], 1
        while True:
            d = cr_get(acc, "/calls.json", company_id=co, start_date=cr_from, end_date=today, per_page=250, page=page,
                       fields="tracking_phone_number,tracker_id,answered,duration,gclid,start_time,source,medium")
            calls += d.get("calls", [])
            if page >= d.get("total_pages", 1): break
            page += 1
        for x in calls: x["_day"] = dt.datetime.fromisoformat(x["start_time"]).astimezone(ZoneInfo(tz)).date().isoformat()
        # gclid -> campaign, one click_view query per click day
        want = {}
        for x in calls:
            if x.get("gclid") and x.get("tracker_id") in web_ids:
                for back in range(4):
                    want.setdefault((dt.date.fromisoformat(x["_day"]) - dt.timedelta(days=back)).isoformat(), set()).add(x["gclid"])
        cache_path = os.path.join(HERE, slug, "gclid_campaigns.json")   # gclid -> campaign never changes; only look up new ones
        try: g2c = json.load(open(cache_path))
        except (OSError, ValueError): g2c = {}
        for d, gs in sorted(want.items()):
            gs = [g for g in gs if g not in g2c and re.fullmatch(r"[A-Za-z0-9_\-]+", g)]
            if not gs: continue
            for i in range(0, len(gs), 200):
                chunk = "','".join(gs[i:i + 200])
                for r in q(f"SELECT click_view.gclid, campaign.name FROM click_view WHERE segments.date = '{d}' AND click_view.gclid IN ('{chunk}')"):
                    g2c[r.click_view.gclid] = r.campaign.name
        settled = (dt.date.fromisoformat(today) - dt.timedelta(days=2)).isoformat()
        for x in calls:   # remember misses too once the call is 2+ days old, so they aren't looked up again
            if x.get("gclid") and x.get("tracker_id") in web_ids and x["_day"] <= settled: g2c.setdefault(x["gclid"], None)
        os.makedirs(os.path.dirname(cache_path), exist_ok=True); json.dump(g2c, open(cache_path, "w"))
        for x in calls:
            num, dur, ans, d = digits(x.get("tracking_phone_number")), x.get("duration") or 0, int(bool(x.get("answered"))), x["_day"]
            if num in ext_nums:
                b = day(d)["button"]; b["calls"] += 1; b["answered"] += ans; b["qualified"] += int(dur >= 60)
            elif x.get("tracker_id") in web_ids:
                src, med = (x.get("source") or "").lower(), (x.get("medium") or "").lower()
                ad = c.get("adsOnlySite") or x.get("gclid") or ("google" in src and ("ads" in src or "paid" in src or med in ("cpc", "ppc", "paid")))
                if not ad: day(d)["webOther"] += 1; continue
                name = g2c.get(x.get("gclid"))
                tgt = row(d, name, types.get(name, "search")) if name else day(d)["unattributed"]
                tgt["webCalls"] += 1; tgt["webAnswered"] += ans; tgt["webQualified"] += int(dur >= 60)
        web_tracked = bool(web_ids)
    except Exception as e:
        cr_error = str(e)[:120]
        prev = None
        for p in sorted(glob.glob(os.path.join(HERE, slug, "funnel_*.json")), reverse=True):
            try: prev = json.load(open(p)); break
            except (OSError, ValueError): continue
        web_tracked, button_tracked, cr_asof = (prev or {}).get("tracked", {}).get("website", False), (prev or {}).get("tracked", {}).get("button", False), None
        if prev:
            cr_asof = prev.get("callrailAsOf") or prev.get("updatedAt")
            for pd in prev.get("days", []):
                if pd["date"] < start: continue
                dd = day(pd["date"]); dd["button"] = pd.get("button", dd["button"]); dd["unattributed"] = pd.get("unattributed", dd["unattributed"]); dd["webOther"] = pd.get("webOther", 0)
                for r in pd.get("campaigns", []):
                    if r.get("webCalls") or r.get("webAnswered") or r.get("webQualified"):
                        x = row(pd["date"], r["name"], r["type"])
                        x["webCalls"], x["webAnswered"], x["webQualified"] = r["webCalls"], r["webAnswered"], r["webQualified"]

    out_days = []
    for d in sorted(days):
        rows = list(days[d]["campaigns"].values())
        for x in rows:
            for k in ("spend", "taps", "uploaded", "btnQualified", "forms"): x[k] = round(x[k], 2)
        out_days.append({"date": d, "campaigns": rows, "unattributed": days[d]["unattributed"], "button": days[d]["button"], "webOther": days[d]["webOther"]})

    sec = btn_secs[0] if len(btn_secs) == 1 else None
    win_clicks = sum(r["clicks"] for d in out_days for r in d["campaigns"])
    ga4_taps = bool(taps) and all(a["type"] == "GOOGLE_ANALYTICS_4_CUSTOM" for a in A if a["name"] in taps)   # a direct tag can be brand new; only judge GA4 imports
    taps_dead = ga4_taps and sum(r["taps"] for d in out_days for r in d["campaigns"]) == 0 and win_clicks >= 200
    notes = ["Taps and calls don't match one to one: some people tap and hang up, others read the number and dial by hand.",
             "Website calls tie to a campaign through the visitor's Google click ID. Calls without a match show as not tied to a campaign (under All)."]
    if not button_tracked:
        notes.append(("The ad's call button dials " + ", ".join(asset_nums) + ", which isn't a CallRail number, so answered ad-button calls can't be tracked.")
                     if asset_nums else "Couldn't find the call button's number in this account, so answered ad-button calls can't be matched to CallRail.")
    if cr_error: notes.insert(0, "CallRail didn't answer at this refresh (" + cr_error + "), so the CallRail call numbers are from " + (cr_asof or "no earlier pull") + ". Google Ads numbers are current.")
    if not web_tracked: notes.append("No CallRail website tracking numbers, so calls from the website aren't tracked.")
    if not taps: notes.append("No conversion action tracks taps on the phone number.")
    if taps_dead: notes.append(f"The tap action ({', '.join(taps)}) recorded nothing since {start} despite {win_clicks:,} clicks, so taps likely aren't firing.")
    notes.append("Counted as taps: " + (", ".join(taps) or "nothing") + ". Forms: " + (", ".join(forms) or "nothing") +
                 ". Ad-button calls: " + (", ".join(button) or "nothing") + (f" ({sec}s+)" if sec else "") + ". Sent back to Google: " + (", ".join(uploads) or "nothing") + ".")
    notes.append("Google Ads numbers for today and yesterday can still change for a few hours as Google finishes processing.")
    notes += c.get("notes", [])
    doc = {"client": slug, "title": "Lead funnel", "updatedAt": now.isoformat(timespec="minutes"), "dataFrom": start, "dataThrough": today,
           "callrailFrom": cr_from, "timeZone": tz, "websiteLabel": c.get("websiteLabel", "website"), "buttonMinSec": sec,
           "tracked": {"taps": bool(taps) and not taps_dead, "website": web_tracked, "button": button_tracked}, "callrailAsOf": cr_asof,
           "actionsUsed": {"taps": taps, "forms": forms, "button": button, "uploads": uploads}, "callAssetNumbers": asset_nums,
           "source": f"Google Ads API ({cid}) + CallRail API ({c['callrailName']}). Refreshed by Claude and from the Command Center.",
           "notes": notes, "days": out_days}
    out = os.path.join(HERE, slug, f"funnel_{today}.json"); os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(doc, open(out, "w"), separators=(",", ":"))
    s30 = [r for d in out_days[-30:] for r in d["campaigns"]]
    tot = lambda k: round(sum(r[k] for r in s30))
    print(f"wrote {out} ({os.path.getsize(out) // 1024} KB, {len(out_days)} days, {len(calls)} CallRail calls) | 30d: clicks {tot('clicks')} taps {tot('taps')} "
          f"webCalls {tot('webCalls')}+{sum(d['unattributed']['webCalls'] for d in out_days[-30:])}u other {sum(d['webOther'] for d in out_days[-30:])} | "
          f"btn placed {tot('btnPlaced')} counted {tot('btnQualified')} CRans {sum(d['button']['answered'] for d in out_days[-30:])} | forms {tot('forms')} | "
          f"tracked {doc['tracked']}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--client"); g.add_argument("--all", action="store_true")
    a = ap.parse_args()
    for s in (CFG if a.all else [a.client]):
        try: build(s)
        except Exception as e: print(f"FAILED {s}: {str(e)[:400]}")
