"""Concrete GTM-53FXJRN4 v6 test: LIVE (v5) vs DRAFT (v6) gtm.js. fbq stubbed (gateCheck -> pass callback, so the
template tries the param builder like Meta's real gate would), all GA4/Ads/Meta hits + the param builder bundle aborted.
Run: python3 concrete_gtm_parambuilder_test_1102.py <envId> <auth>"""
import re, sys, urllib.request
from playwright.sync_api import sync_playwright
GTM, LABEL = "GTM-53FXJRN4", "JisVCKOi8KQdEPiYyc8-"
env, auth = sys.argv[1], sys.argv[2]
JS = {"LIVE v5": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT v6": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
STUB = ("(function(){var f=window.fbq;window.__fbqlog=window.__fbqlog||[];"
        "function h(a){if(a[0]==='gateCheck'){if(typeof a[2]==='function')a[2](a[1],a[4]);return;}window.__fbqlog.push(JSON.stringify(a));}"
        "(f&&f.queue||[]).forEach(function(a){h(Array.from(a))});if(f){f.queue=[];f.callMethod=function(){h(Array.from(arguments))};}})();")
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr")
PB = re.compile(r".*capi-automation\.s3.*")
GEN = "{event:'generate_lead', event_id:'tsdtest-1102-pb', email:'tsd-test@example.com', phone:'(662) 555-0100'}"
GHL = "{event:'ghl_form_submit', ghl_user:{email:'tsd-test@example.com', phone_raw:'16625550100', first_name:'test', last_name:'tsd'}}"
CASES = [("go. GHL page", "https://go.concrete-adventures.com/decorative-concrete/", GHL),
         ("staging /contact", "https://tsd-concreteadv.vercel.app/contact", GEN)]
with sync_playwright() as p:
    b = p.chromium.launch()
    for case, url, push in CASES:
        for label, js in JS.items():
            ctx = b.new_context(); page = ctx.new_page(); hits = []; pb = []
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(re.compile(r".*connect\.facebook\.net/.*fbevents\.js.*"), lambda r: r.fulfill(status=200, content_type="application/javascript", body=STUB))
            page.route(PB, lambda r: (pb.append(r.request.url), r.abort()))
            page.route(BLOCK, lambda r: (hits.append(r.request.url), r.abort()))
            page.goto(url, wait_until="load", timeout=60000); page.wait_for_timeout(6000)
            page.mouse.click(5, 5); page.wait_for_timeout(3000)  # first tap starts GTM on the new site
            pre = page.evaluate("window.__fbqlog||[]"); m, n = len(hits), len(pre)
            page.evaluate(f"window.dataLayer.push({push})"); page.wait_for_timeout(8000)
            post = page.evaluate("window.__fbqlog||[]")[n:]
            st = page.evaluate("window._fbq_param_builder_status||null")
            pv = [x for x in pre + post if '"PageView"' in x]; lead = [x for x in post if '"Lead"' in x]
            ads = [u for u in hits[m:] if LABEL in u]
            print(f"== {case} / {label}: paramBuilder requests={len(pb)} status={st} | Meta PageView={len(pv)} | Meta Lead={len(lead)} | Ads Lead hits={len(ads)}"
                  + (f" | {re.findall(r'eventID[^}]*', lead[0])[:1]}" if lead else ""))
            ctx.close()
    b.close()
