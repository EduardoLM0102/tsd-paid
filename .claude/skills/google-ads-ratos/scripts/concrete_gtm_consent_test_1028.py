"""Concrete GTM-53FXJRN4 v5 consent test: LIVE (v4) vs DRAFT (v5) gtm.js on old go. GHL pages (no consent mode) and
the new staging site (US opt-out). fbq stubbed + logged, every GA4/Ads/Meta hit aborted (nothing recorded).
Run: python3 concrete_gtm_consent_test_1028.py <envId> <auth>"""
import re, sys, urllib.request
from playwright.sync_api import sync_playwright
GTM, LABEL = "GTM-53FXJRN4", "JisVCKOi8KQdEPiYyc8-"
env, auth = sys.argv[1], sys.argv[2]
JS = {"LIVE": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
STUB = "(function(){var f=window.fbq;window.__fbqlog=window.__fbqlog||[];(f&&f.queue||[]).forEach(function(a){window.__fbqlog.push(JSON.stringify(Array.from(a)))});if(f){f.queue=[];f.callMethod=function(){window.__fbqlog.push(JSON.stringify(Array.from(arguments)))};}})();"
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr")
GPC = "Object.defineProperty(navigator, 'globalPrivacyControl', {get: function(){return true}});"
GEN = "{event:'generate_lead', event_id:'tsdtest-1028-consent', email:'tsd-test@example.com', phone:'(662) 555-0100'}"
GHL = "{event:'ghl_form_submit', ghl_user:{email:'tsd-test@example.com', phone_raw:'16625550100', first_name:'test', last_name:'tsd'}}"
CASES = [
    ("go. GHL page, no consent mode", "https://go.concrete-adventures.com/decorative-concrete/", None, GHL),
    ("staging, banner ignored", "https://tsd-concreteadv.vercel.app/contact", None, GEN),
    ("staging, clicked Opt out", "https://tsd-concreteadv.vercel.app/contact", "optout", GEN),
    ("staging, GPC browser", "https://tsd-concreteadv.vercel.app/contact", "gpc", GEN),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for case, url, mode, push in CASES:
        for label, js in JS.items():
            ctx = b.new_context(); page = ctx.new_page(); hits = []
            if mode == "gpc":
                page.add_init_script(GPC)
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(re.compile(r".*connect\.facebook\.net/.*fbevents\.js.*"), lambda r: r.fulfill(status=200, content_type="application/javascript", body=STUB))
            page.route(BLOCK, lambda r: (hits.append(r.request.url), r.abort()))
            page.goto(url, wait_until="load", timeout=60000); page.wait_for_timeout(5000)
            if mode == "optout":
                page.get_by_role("button", name=re.compile(r"^opt out$", re.I)).first.click(timeout=5000); page.wait_for_timeout(2000)
            ics = page.evaluate("(function(){var e=window.google_tag_data&&google_tag_data.ics&&google_tag_data.ics.entries&&google_tag_data.ics.entries.ad_storage;return e?[e.default,e.update]:null})()")
            pre = page.evaluate("window.__fbqlog||[]")
            m, n = len(hits), len(pre)
            page.evaluate(f"window.dataLayer.push({push})"); page.wait_for_timeout(8000)
            ads = [u for u in hits[m:] if LABEL in u]
            post = page.evaluate("window.__fbqlog||[]")[n:]
            pv = [x for x in pre if '"PageView"' in x]
            lead = [x for x in post if '"Lead"' in x]
            print(f"== {case} / {label}: ad_storage={ics} | Meta PageView={len(pv)} | Meta Lead={len(lead)} | Ads Lead hits={len(ads)}"
                  + (f" | eventID={re.findall(r'eventID[^,}]*', lead[0])[:1]}" if lead else ""))
            ctx.close()
    b.close()
