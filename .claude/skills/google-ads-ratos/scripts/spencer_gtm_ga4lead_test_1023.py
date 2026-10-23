"""Headless test of the 10-23 draft vs LIVE: GA4 hits with en=generate_lead after a fake form_submitted push. Hits are aborted, nothing recorded."""
import re, sys, urllib.request
from playwright.sync_api import sync_playwright
GTM = "GTM-KT5RPTP"; env, auth = sys.argv[1], sys.argv[2]
SITES = ["https://spencers-tsd.vercel.app/schedule", "https://spencers-tsd.vercel.app/contact"]
JS = {"LIVE": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr|connect\.facebook\.net")
LEAD = "{event:'form_submitted', event_id:'tsdtest-1023-ga4', first_name:'Test', last_name:'TSD', email:'tsd-test@example.com', phone:'(972) 555-0100'}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, js in JS.items():
        for site in SITES:
            ctx = b.new_context(); page = ctx.new_page(); hits = []
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(BLOCK, lambda r: (hits.append(r.request.url + "\n" + (r.request.post_data or "")), r.abort()))
            page.goto(site, wait_until="load", timeout=60000); page.wait_for_timeout(4000)
            ga_before = [u for u in hits if "/g/collect" in u and "en=generate_lead" in u]
            allga = [u for u in hits if "/g/collect" in u]
            m = len(hits); page.evaluate(f"window.dataLayer.push({LEAD})"); page.wait_for_timeout(10000); page.evaluate("document.dispatchEvent(new Event(\"visibilitychange\"))"); page.wait_for_timeout(2000)
            after = hits[m:]
            ga = [u for u in after if "/g/collect" in u and "en=generate_lead" in u]
            ads = [u for u in after if "ZwC_CPnY8okcEPnggusC" in u or "761311353" in u]
            print(f"{label:5} {site.split('/')[-1]:9} GA4 generate_lead before={len(ga_before)} after={len(ga)} | Ads lead hits={len(ads)} | GA4 hits on load={len(allga)} after-lead GA4 hits={len([u for u in after if '/g/collect' in u])}")
            for u in [u for u in after if "/g/collect" in u][:3]: print("      ", re.findall(r"en=([a-z_]+)", u))
            for u in ga[:1]:
                q = dict(x.split("=", 1) for x in u.split("?", 1)[1].split("&") if "=" in x)
                print("      tid", q.get("tid"), "dl", urllib.parse.unquote(q.get("dl", ""))[:70], "gcs", q.get("gcs"))
            ctx.close()
    b.close()
