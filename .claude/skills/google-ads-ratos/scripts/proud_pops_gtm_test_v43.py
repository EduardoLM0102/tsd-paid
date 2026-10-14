"""Headless test: live v42 (control) vs unpublished v43 (D-1 + D-5) via private env. All tracking hits aborted."""
import re, json, os, urllib.request
from playwright.sync_api import sync_playwright
GTM = "GTM-WBFDB6L8"
s = json.load(open(os.path.expanduser("~/Documents/GitHub/topserv-workspace/clients/proud-pops/.gtm_d1_d5_state.json")))
v43 = urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}&gtm_auth={s['auth']}&gtm_preview=env-{s['env']}&gtm_cookies_win=x").read()
v42 = urllib.request.urlopen(f"https://www.googletagmanager.com/gtm.js?id={GTM}").read()
print("v43 js size", len(v43), "| v42 js size", len(v42), "| differ:", v43 != v42)
BLOCK = re.compile(r"google-analytics\.com|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|doubleclick\.net|facebook\.com/tr")

def classify(url, body):
    s_ = url + " " + (body or ""); out = set()
    for en in re.findall(r"(?:^|[?&\s\n])en=([a-z_]+)", s_):
        if en in ("generate_lead", "job_application"): out.add("GA4:" + en)
    if "u5lXCI2jk7kYEKrcxssp" in s_: out.add("ADS:lead")
    if "facebook.com/tr" in url:
        m = re.search(r"[?&]ev=([A-Za-z]+)", s_)
        if m: out.add("META:" + m.group(1))
    return out

def run(label, js):
    hits = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1280, "height": 900}); page = ctx.new_page()
        page.route(re.compile(r".*googletagmanager\.com/gtm\.js\?id=" + GTM + ".*"), lambda r: r.fulfill(status=200, content_type="application/javascript", body=js))
        page.route(BLOCK, lambda r: (hits.append((r.request.url, r.request.post_data)), r.abort()))
        def go(url):
            for _ in range(3):
                try: page.goto(url, wait_until="load", timeout=45000); break
                except Exception: page.wait_for_timeout(3000)
            page.wait_for_timeout(3000)
            btn = page.get_by_role("button", name=re.compile("Accept All", re.I))
            if btn.count() and btn.first.is_visible(): btn.first.click(); page.wait_for_timeout(1500)
        def push(name, payload):
            mark = len(hits); page.evaluate(f"window.dataLayer.push({payload})"); page.wait_for_timeout(5000)
            page.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); page.wait_for_timeout(1500)
            found = sorted(set().union(*[classify(u, b_) for u, b_ in hits[mark:]]) if hits[mark:] else set())
            print(f"  [{label}] {name:52s} path={page.url.split('proudpops.com')[-1]:12s} -> {found or 'nothing'}")
        go("https://proudpops.com/careers")
        push("1 /careers job form submit", "{event:'ghl_form_submit', ghl_form_id:'ThmcYYHImwSoYS9oBt3n'}")
        push("2 /careers 'Appointment Scheduled'", "{event:'Appointment Scheduled'}")
        go("https://proudpops.com/proud-pops-hvac-services")
        vis = page.locator('a[href$="/schedule"]:visible')
        if vis.count(): vis.first.click()
        else: page.evaluate("history.pushState({}, '', '/schedule'); window.dispatchEvent(new PopStateEvent('popstate'))")
        page.wait_for_timeout(3000)
        push("3 /schedule customer form submit", "{event:'ghl_form_submit', email:'tsd-test@example.com'}")
        push("4 /schedule 'Appointment Scheduled'", "{event:'Appointment Scheduled'}")
        b.close()

run("LIVE v42", v42)
run("DRAFT v43", v43)
