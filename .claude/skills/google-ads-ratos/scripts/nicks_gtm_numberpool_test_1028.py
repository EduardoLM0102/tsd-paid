"""Headless test of Nick's GTM v9 (env 71) vs live: GHL number pool scripts load, no JS errors. Analytics hits aborted."""
import sys, re, urllib.request
from playwright.sync_api import sync_playwright
GTM = "GTM-5RH7XW36"
ENV = f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth=eyysltPgtcwO5YOzFcwSUQ&gtm_preview=env-71&gtm_cookies_win=x"
draft = urllib.request.urlopen(ENV).read().decode()
print("draft gtm.js has number_pool:", "number_pool.js" in draft)
BLOCK = re.compile(r"google-analytics\.com/g/collect|/ccm/collect|googleadservices|doubleclick|facebook\.com/tr|analytics\.google\.com")

def run(label, use_draft):
    hits, errs = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        def route(r):
            u = r.request.url
            if use_draft and "googletagmanager.com/gtm.js" in u and GTM in u:
                return r.fulfill(status=200, content_type="application/javascript", body=draft)
            if BLOCK.search(u): return r.abort()
            return r.continue_()
        pg.route("**/*", route)
        pg.on("response", lambda resp: hits.append((resp.status, resp.url)) if "leadconnectorhq.com/appengine" in resp.url else None)
        pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.goto("https://www.nicksac.com/", wait_until="load"); pg.wait_for_timeout(6000)
        tels = sorted(set(pg.eval_on_selector_all("a[href^='tel:']", "els => els.map(e => e.getAttribute('href'))")))
        b.close()
    print(f"[{label}] GHL requests:", hits or "none"); print(f"[{label}] tel links:", tels); print(f"[{label}] page errors:", errs or "none")

run("LIVE v8", False)
run("DRAFT v9", True)
