"""Concrete GTM-53FXJRN4 v4 test on staging: LIVE vs DRAFT gtm.js, fake lead pushes, fbq stubbed, every GA4/Ads/Meta hit aborted
(nothing is recorded). Each lead on a fresh page (lead tags are oncePerLoad).
Run: python3 concrete_gtm_headless_test_1028.py <envId> <auth>"""
import re, sys, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
GTM, SITE, LABEL = "GTM-53FXJRN4", "https://tsd-concreteadv.vercel.app/contact", "JisVCKOi8KQdEPiYyc8-"
env, auth = sys.argv[1], sys.argv[2]
JS = {"LIVE": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
STUB = "(function(){var f=window.fbq;window.__fbqlog=window.__fbqlog||[];(f&&f.queue||[]).forEach(function(a){window.__fbqlog.push(JSON.stringify(Array.from(a)))});if(f){f.queue=[];f.callMethod=function(){window.__fbqlog.push(JSON.stringify(Array.from(arguments)))};}})();"
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr")
H = "a" * 64
CASES = {
    "generate_lead raw flat": "{event:'generate_lead', event_id:'tsdtest-1028-raw', first_name:' Test ', last_name:'TSD', email:' TSD-Test@Example.com ', phone:'(662) 555-0100'}",
    "generate_lead hashed user_data": "{event:'generate_lead', event_id:'tsdtest-1028-hash', user_data:{sha256_email_address:'" + H + "', sha256_phone_number:'" + "b" * 64 + "'}}",
    "ghl_form_submit (old GHL)": "{event:'ghl_form_submit', ghl_user:{email:'tsd-test@example.com', phone_raw:'16625550100', first_name:'test', last_name:'tsd'}}",
    "lead_submitted (decoy)": "{event:'lead_submitted', event_id:'tsdtest-1028-decoy', email:'x@example.com'}",
}


def ga_events(urls_bodies):
    out = []
    for u, body in urls_bodies:
        if "/g/collect" not in u:
            continue
        for chunk in [u] + (body or "").split("\n"):
            m = re.search(r"(?:^|[?&])en=([^&]+)", chunk)
            if m:
                out.append(urllib.parse.unquote(m.group(1)))
    return out


with sync_playwright() as p:
    b = p.chromium.launch()
    for label, js in JS.items():
        for case, push in CASES.items():
            ctx = b.new_context(); page = ctx.new_page(); hits = []
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(re.compile(r".*connect\.facebook\.net/.*fbevents\.js.*"), lambda r: r.fulfill(status=200, content_type="application/javascript", body=STUB))
            page.route(BLOCK, lambda r: (hits.append((r.request.url, r.request.post_data)), r.abort()))
            page.goto(SITE, wait_until="load", timeout=60000); page.wait_for_timeout(4000)
            try:
                page.get_by_role("button", name=re.compile("accept", re.I)).first.click(timeout=3000); page.wait_for_timeout(2000)
            except Exception:
                pass
            m, n = len(hits), len(page.evaluate("window.__fbqlog||[]"))
            page.evaluate(f"window.dataLayer.push({push})"); page.wait_for_timeout(10000)
            new = hits[m:]
            ads = [u for u, _ in new if LABEL in u]
            fbq = [x for x in page.evaluate("window.__fbqlog||[]")[n:] if "Lead" in x or "init" in x]
            print(f"\n== {label} / {case}\n  Ads Lead hits: {len(ads)}\n  GA4 events: {ga_events(new)}")
            for x in fbq:
                print("  fbq:", x[:400])
            ctx.close()
    b.close()
