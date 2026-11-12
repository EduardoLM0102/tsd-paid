"""Deeper check: stub fbevents.js to log fbq calls; dump raw Ads/GA hits for no-consent scenario. Nothing is recorded (hits aborted)."""
import re, sys, urllib.request
from playwright.sync_api import sync_playwright
GTM, SITE = "GTM-KT5RPTP", "https://spencers-tsd.vercel.app/"
env, auth = sys.argv[1], sys.argv[2]
JS = {"LIVE": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
STUB = "(function(){var f=window.fbq;window.__fbqlog=window.__fbqlog||[];(f&&f.queue||[]).forEach(function(a){window.__fbqlog.push(JSON.stringify(Array.from(a)))});if(f){f.queue=[];f.callMethod=function(){window.__fbqlog.push(JSON.stringify(Array.from(arguments)))};}})();"
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr")
LEAD = "{event:'form_submitted', event_id:'tsdtest-1022-abc', first_name:'Test', last_name:'TSD', email:' TSD-Test@Example.com ', phone:'(972) 555-0100'}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, js in JS.items():
        for scen in ("A no consent", "C accept on banner"):
            ctx = b.new_context(); page = ctx.new_page(); hits = []
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(re.compile(r".*connect\.facebook\.net/.*fbevents\.js.*"), lambda r: r.fulfill(status=200, content_type="application/javascript", body=STUB))
            page.route(BLOCK, lambda r: (hits.append(r.request.url[:160]), r.abort()))
            page.goto(SITE, wait_until="load", timeout=60000); page.wait_for_timeout(4000)
            log = lambda: page.evaluate("window.__fbqlog||[]")
            print(f"\n== {label} / {scen}\n  fbq after load: {log()}")
            if scen.startswith("C"):
                page.get_by_role("button", name=re.compile("accept all", re.I)).first.click(); page.wait_for_timeout(4000)
                print("  fbq after Accept:", log())
            m = len(hits); n = len(log())
            page.evaluate(f"window.dataLayer.push({LEAD})"); page.wait_for_timeout(5000)
            print("  fbq after lead:", log()[n:])
            ads = [u for u in hits[m:] if "761311353" in u or "ZwC_" in u]
            print(f"  Ads hits after lead ({len(ads)}):", *ads[:4], sep="\n    ")
            ctx.close()
    b.close()
