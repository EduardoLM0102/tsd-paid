"""Spencer new-site launch conversion test (Alex's 10-22 DM): submits ONE real TEST lead on spencers-tsd.vercel.app/contact
with cookies accepted, records dataLayer + every tracking request (nothing blocked). Output dir = argv[1]."""
import re, sys, json, time, datetime
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]
TRACK = re.compile(r"facebook\.com/tr|googleadservices\.com|google\.com/(pagead|ccm)|googlesyndication\.com/pagead|google-analytics\.com|analytics\.google\.com|doubleclick\.net|/api/track")
reqs = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=False)
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    pg = ctx.new_page()
    pg.on("request", lambda r: reqs.append({"t": time.time(), "method": r.method, "url": r.url, "post": (r.post_data or "")[:3000]}) if TRACK.search(r.url) else None)
    pg.goto("https://spencers-tsd.vercel.app/", wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.get_by_role("button", name=re.compile("accept all", re.I)).first.click(); pg.wait_for_timeout(3000)
    pg.goto("https://spencers-tsd.vercel.app/contact", wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.fill("#lead-name", "TEST Eduardo")
    pg.fill("#lead-phone", "214-555-0150")
    pg.fill("#lead-email", "eduardo.tsd.test@example.com")
    pg.fill("#lead-city", "Dallas")
    pg.select_option("#lead-trade", "Other")
    pg.fill("#lead-message", "conversion test, not a customer")
    mark = len(reqs)
    submitted = datetime.datetime.now().astimezone()
    pg.get_by_role("button", name=re.compile("send message", re.I)).first.click()
    pg.wait_for_timeout(12000)
    status = pg.locator("[role=status]").all_inner_texts()
    errors = pg.locator("[id$=-error]").all_inner_texts()
    dl = pg.evaluate("JSON.stringify(window.dataLayer.filter(x => x && x.event && !String(x.event).startsWith('gtm.')))")
    cookies = {c["name"]: c["value"][:40] for c in ctx.cookies() if c["name"] in ("_fbp", "_fbc", "_ga", "_gcl_aw", "_gcl_au")}
    b.close()
res = {"submitted_at": submitted.isoformat(), "status_text": status, "field_errors": errors, "dataLayer_events": json.loads(dl),
       "cookies": cookies, "requests_after_submit": reqs[mark:], "requests_before_submit": len(reqs[:mark])}
json.dump(res, open(f"{OUT}/test-result.json", "w"), indent=1)
print("submitted_at", res["submitted_at"]); print("status", status, "errors", errors)
print("dataLayer events:", [e.get("event") for e in res["dataLayer_events"]])
for e in res["dataLayer_events"]:
    if e.get("event") == "form_submitted": print("form_submitted:", e)
for r in reqs[mark:]:
    s = r["url"] + " " + r["post"]
    tag = ""
    if "facebook.com/tr" in s:
        tag = "META ev=%s id=%s eid=%s" % tuple((re.search(k + r"=([^&\s]+)", s) or [None, None])[1] for k in ("ev", "id", "eid"))
    elif "ZwC_CPnY8okcEPnggusC" in s: tag = "ADS Lead label"
    elif "761311353" in s: tag = "ADS other"
    elif re.search(r"[?&\s]en=([a-z_]+)", s): tag = "GA4 en=" + ",".join(re.findall(r"(?:^|[?&\s\n])en=([a-z_]+)", s))
    elif "/api/track" in s: tag = "site /api/track"
    print(f"  {tag or '-':55s} {r['url'][:110]}")
