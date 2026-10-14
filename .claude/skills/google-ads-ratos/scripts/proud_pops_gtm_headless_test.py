import re, sys, time, urllib.request
from playwright.sync_api import sync_playwright

GTM = "GTM-WBFDB6L8"
DRAFT_URL = f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth=C4_q1dtWlmhRtqwO_YqNPQ&gtm_preview=env-6&gtm_cookies_win=x"
draft_js = urllib.request.urlopen(DRAFT_URL).read()
live_js = urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read()
print("draft js has job_application:", b"job_application" in draft_js, "| form id:", b"ThmcYYHImwSoYS9oBt3n" in draft_js)
print("live  js has job_application:", b"job_application" in live_js)

BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm)|googleads\.g\.doubleclick\.net|facebook\.com/tr|google\.com/rmkt")

def classify(url, body):
    s = url + " " + (body or "")
    out = []
    for en in re.findall(r"(?:^|[?&\s\n])en=([a-z_]+)", s):
        if en in ("generate_lead", "job_application"):
            out.append("GA4:" + en)
    if "u5lXCI2jk7kYEKrcxssp" in s:
        out.append("ADS:Website lead")
    if "facebook.com/tr" in url and "ev=PageView" in url:
        out.append("META:PageView")
    return out

def run(label, js):
    hits = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"),
                   lambda route: route.fulfill(status=200, content_type="application/javascript", body=js))
        def on_route(route):
            req = route.request
            hits.append((page.url, req.url, req.post_data))
            route.abort()
        page.route(BLOCK, on_route)

        def step(name, url_or_none, push, nav_click=None):
            mark = len(hits)
            if url_or_none:
                for attempt in range(3):
                    try:
                        page.goto(url_or_none, wait_until="load", timeout=45000); break
                    except Exception as ex:
                        print("      goto retry", attempt + 1, str(ex)[:80]); page.wait_for_timeout(3000)
                page.wait_for_timeout(3500)
            if nav_click:
                vis = page.locator('a[href$="/schedule"]:visible')
                if vis.count():
                    vis.first.click(); how = "clicked link"
                else:
                    page.evaluate("history.pushState({}, '', '/schedule'); window.dispatchEvent(new PopStateEvent('popstate'))"); how = "pushState+popstate"
                page.wait_for_timeout(3000)
                frames = [f.url for f in page.frames if 'leadnurturemachine' in f.url]
                print(f"      nav via {how}; GHL iframe on page: {bool(frames)}")
            mark = len(hits)
            page.evaluate(f"window.dataLayer.push({push})")
            page.wait_for_timeout(5000)
            page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
            page.wait_for_timeout(1500)
            found = sorted({c for (_, u, body) in hits[mark:] for c in classify(u, body)})
            print(f"  [{label}] {name:58s} path={page.url.split('proudpops.com')[-1]:28s} -> {found or 'nothing'}")

        step("1 /careers push WITH job form id", "https://proudpops.com/careers",
             "{event:'ghl_form_submit', ghl_form_id:'ThmcYYHImwSoYS9oBt3n'}")
        step("2 /careers push WITHOUT form id (listener [99] style)", "https://proudpops.com/careers",
             "{event:'ghl_form_submit', email:'tsd-test@example.com'}")
        step("3 HVAC page -> click to /schedule, push", "https://proudpops.com/proud-pops-hvac-services",
             "{event:'ghl_form_submit', email:'tsd-test@example.com'}", nav_click='a[href="/schedule"]')
        step("4 homepage -> click to /schedule, push", "https://proudpops.com/",
             "{event:'ghl_form_submit', email:'tsd-test@example.com'}", nav_click='a[href="/schedule"]')
        b.close()
    print(f"  [{label}] total tracking requests intercepted+aborted: {len(hits)}")

run("LIVE v42 (published)", live_js)
