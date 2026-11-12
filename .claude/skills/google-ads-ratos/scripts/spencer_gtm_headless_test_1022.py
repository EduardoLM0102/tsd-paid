"""Headless test of GTM-KT5RPTP version vs live on spencers-tsd.vercel.app. All GA4/Ads/Meta hits are ABORTED (nothing recorded).
Usage: python3 spencer_gtm_headless_test_1022.py <env_id> <auth>"""
import re, sys, json, urllib.request
from playwright.sync_api import sync_playwright
GTM, SITE = "GTM-KT5RPTP", "https://spencers-tsd.vercel.app/"
env, auth = sys.argv[1], sys.argv[2]
draft_js = urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={auth}&gtm_preview=env-{env}&gtm_cookies_win=x").read()
live_js = urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read()
print("draft has 1258997717469696:", b"1258997717469696" in draft_js, "| live has it:", b"1258997717469696" in live_js)
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|googleads\.g\.doubleclick\.net|facebook\.com/(tr|privacy_sandbox)|connect\.facebook\.net/signals")
LEAD = "{event:'form_submitted', event_id:'tsdtest-1022-abc', first_name:'Test', last_name:'TSD', email:' TSD-Test@Example.com ', phone:'(972) 555-0100'}"

def classify(url, body):
    s = url + " " + (body or "")
    out = []
    for en in re.findall(r"(?:^|[?&\s\n])en=([a-z_]+)", s):
        if en not in ("page_view", "user_engagement", "scroll"): out.append("GA4:" + en)
    if "ZwC_CPnY8okcEPnggusC" in s:
        em = "em=" in s or "&em" in s
        out.append("ADS:Lead" + ("+userdata" if em else ""))
    if "facebook.com/tr" in url:
        ev = re.search(r"[?&]ev=(\w+)", s); pid = re.search(r"[?&]id=(\d+)", s); eid = re.search(r"[?&]eid=([\w-]+)", s)
        ph = "ph" if re.search(r"ud\[ph\]=", s) else ""
        out.append(f"META:{ev and ev.group(1)}@{pid and pid.group(1)}" + (f" eid={eid.group(1)}" if eid else "") + (" +ph" if ph else ""))
    return out

def run(label, js):
    print(f"\n== {label}")
    with sync_playwright() as p:
        b = p.chromium.launch()
        for scen in ("A no consent", "B consent stored (returning)", "C accept on banner"):
            ctx = b.new_context(viewport={"width": 1280, "height": 900})
            hits, callrail = [], []
            if scen.startswith("B"):
                ctx.add_init_script("localStorage.setItem('spencer_consent_v1', JSON.stringify({version:1,analytics:true,marketing:true,updatedAt:new Date().toISOString(),gpc:false}))")
            page = ctx.new_page()
            page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"),
                       lambda r: r.fulfill(status=200, content_type="application/javascript", body=js))
            page.route(BLOCK, lambda r: (hits.append((r.request.url, r.request.post_data)), r.abort()))
            page.on("request", lambda rq: callrail.append(rq.url) if "swap.js" in rq.url else None)
            page.goto(SITE, wait_until="load", timeout=60000); page.wait_for_timeout(4000)
            def show(step, mark):
                found = [c for (u, bd) in hits[mark:] for c in classify(u, bd)]
                print(f"  [{scen}] {step:22s} -> {found or 'nothing'}")
            show("page load", 0)
            if scen.startswith("C"):
                m = len(hits)
                btn = page.get_by_role("button", name=re.compile("accept all", re.I))
                print("    banner button found:", btn.count())
                if btn.count(): btn.first.click(); page.wait_for_timeout(4000)
                show("after Accept All", m)
            m = len(hits)
            page.evaluate(f"window.dataLayer.push({LEAD})"); page.wait_for_timeout(5000)
            show("form_submitted push", m)
            print(f"    CallRail swap.js requests: {len(callrail)} | fbq loaded: {page.evaluate('typeof window.fbq')}")
            ctx.close()
        b.close()

run("LIVE v8", live_js)
run("DRAFT version", draft_js)
