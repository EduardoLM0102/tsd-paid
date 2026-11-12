"""TopServ site GTM-PR3DRB45 v4 test: LIVE vs DRAFT gtm.js on staging + live site, real clicks on each book.topservdigital.com
link type, book.* stubbed, every GA4/Meta/UET hit aborted (nothing is recorded).
Run: python3 topserv_site_booking_click_test_1028.py <envId> <auth>"""
import re, sys, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
GTM = "GTM-PR3DRB45"
env, auth = sys.argv[1], sys.argv[2]
JS = {"LIVE": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read(),
      "DRAFT": urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()}
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/tr|bat\.bing\.com/action")
ST, LV = "https://topservstaging.vercel.app", "https://topservdigital.com"
CASES = [  # (page, link selector, expect booking_click)
    (ST + "/", 'a[href="https://book.topservdigital.com/discovery-calendar"]', True),
    (ST + "/programs-pricing/success-stories", 'a[href="https://book.topservdigital.com"], a[href="https://book.topservdigital.com/"]', True),
    (ST + "/jonathan", 'a[href="https://book.topservdigital.com/FDM"]', False),
    (LV + "/", 'a[href="https://book.topservdigital.com/discovery-calendar"]', True),
    (LV + "/", 'a[href="https://book.topservdigital.com/FDM"] >> visible=true', False),  # inside the ebook pop-up, keep it up
]


def ga_hits(hits):
    out = []
    for u, body in hits:
        if "/g/collect" not in u:
            continue
        tid = (re.search(r"[?&]tid=([^&]+)", u) or [None, "?"])[1]
        for chunk in [u] + (body or "").split("\n"):
            m = re.search(r"(?:^|[?&])en=([^&]+)", chunk)
            if m:
                lu = re.search(r"(?:^|&)ep\.link_url=([^&]+)", chunk)
                out.append((urllib.parse.unquote(m.group(1)), tid, urllib.parse.unquote(lu.group(1)) if lu else None))
    return out


fails = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, js in JS.items():
        for url, sel, expect in CASES:
            ctx = b.new_context(); page = ctx.new_page(); hits = []
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), (lambda body: (lambda r: r.fulfill(status=200, content_type="application/javascript", body=body)))(js))
            page.route(BLOCK, lambda r: (hits.append((r.request.url, r.request.post_data)), r.abort()))
            # stub the booking page (aborting the navigation kills the page before GA4 flushes = false FAIL)
            page.route(re.compile(r".*book\.topservdigital\.com.*"), lambda r: (hits.append((r.request.url, None)), r.fulfill(status=200, content_type="text/html", body="<html>book stub</html>")))
            page.goto(url, wait_until="load", timeout=60000); page.wait_for_timeout(3000)
            try:
                page.get_by_role("button", name=re.compile("accept", re.I)).first.click(timeout=2000); page.wait_for_timeout(1500)
            except Exception:
                pass
            if "FDM" not in sel or ST in url: page.add_style_tag(content='[class*="pop-up"]{display:none !important}')  # live site's Webflow pop-up blocks clicks
            m = len(hits)
            loc = page.locator(sel).first
            if "FDM" in sel and LV in url: page.wait_for_timeout(6000)  # let the pop-up open
            loc.scroll_into_view_if_needed(); loc.click(); page.wait_for_timeout(5000)
            new = hits[m:]
            evs = ga_hits(new)
            nav = [u for u, _ in new if "book.topservdigital.com" in u]
            got = any(e[0] == "booking_click" for e in evs)
            ok = got == (expect if label == "DRAFT" else False)
            fails += not ok
            print(f"{'OK ' if ok else 'FAIL'} {label:5} {url.replace('https://','')} -> {sel.split('href=')[1].split(']')[0]}  (page-load GA4 events: {[e[0] for e in ga_hits(hits[:m])]})\n"
                  f"     GA4: {evs}\n     navigation to book.* attempted: {bool(nav)}")
            ctx.close()
    b.close()
print("\nFAILS:", fails)
