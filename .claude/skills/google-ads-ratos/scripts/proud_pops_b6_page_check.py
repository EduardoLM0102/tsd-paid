"""Checklist B6 (read-only): check the service landing pages before swapping Search final URLs.
Real browser, all GA4/Ads/Meta/CallRail tracking requests aborted so the visits aren't recorded."""
import re, sys
from playwright.sync_api import sync_playwright
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
PAGES = ["/services/electrical", "/services/plumbing", "/services/plumbing/water-heaters", "/"]
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|doubleclick\.net|facebook\.com/tr|callrail|calltrk")
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, vp, mobile in (("desktop", {"width": 1280, "height": 900}, False), ("mobile", {"width": 390, "height": 844}, True)):
        ctx = b.new_context(viewport=vp, is_mobile=mobile, has_touch=mobile)
        page = ctx.new_page(); page.route(BLOCK, lambda r: r.abort())
        errors = []; page.on("pageerror", lambda e: errors.append(str(e)[:120]))
        for path in PAGES:
            errors.clear()
            for attempt in range(3):
                try:
                    page.goto("https://proudpops.com" + path, wait_until="load", timeout=45000); break
                except Exception as ex:
                    page.wait_for_timeout(3000)
            page.wait_for_timeout(3500)
            h1 = page.locator("h1").first.inner_text(timeout=3000) if page.locator("h1").count() else "(no h1)"
            notfound = page.locator("text=/not found|404/i").count()
            sched = page.locator('a[href$="/schedule"]:visible, a[href*="/schedule?"]:visible')
            sched_txt = [t.strip()[:40] for t in sched.all_inner_texts()][:4]
            above = page.evaluate("""() => [...document.querySelectorAll('a[href$="/schedule"]')].some(a => {const r=a.getBoundingClientRect(); return r.width>0 && r.top < window.innerHeight && r.bottom > 0})""")
            tels = sorted({a for a in page.eval_on_selector_all('a[href^="tel:"]', "els => els.filter(e => e.offsetParent !== null).map(e => e.getAttribute('href'))")})
            page.screenshot(path=f"{OUT}/{label}{path.replace('/', '_') or '_home'}.png")
            print(f"[{label:7s}] {path:34s} h1='{h1[:55]}' | 404-text={notfound} | schedule links visible={sched.count()} {sched_txt} | above fold={above} | tel={tels} | js errors={len(errors)}")
        ctx.close()
    b.close()
