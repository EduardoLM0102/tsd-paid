"""READ-ONLY live test of Google tracking on the NEW spencerairconditioning.com (2026-10-27). Nothing is recorded: every Google/Meta/
CallRail-call hit is ABORTED in the browser, the gclid is fake, and no form is submitted (the lead is a synthetic dataLayer push).
Checks: GTM + Google tag load, gclid kept (URL / _gcl_aw), tel: tap -> Ads Click to call (Jm0cCOeMmpgdEPnggusC), form_submitted ->
Ads Submit lead form - Web (ZwC_CPnY8okcEPnggusC) + user data, CallRail swap, and whether the site's own JS pushes form_submitted.
  python3 spencer_live_google_test_1027.py"""
import re, urllib.request, urllib.parse
from playwright.sync_api import sync_playwright

SITE = "https://spencerairconditioning.com"
BLOCK = re.compile(r"google-analytics\.com/g/collect|analytics\.google\.com|googleadservices\.com|google\.com/(pagead|ccm|rmkt)|"
                   r"googleads\.g\.doubleclick\.net|facebook\.com/tr")
LEAD = "{event:'form_submitted', event_id:'tsdtest-1027', first_name:'Test', last_name:'TSD', email:'tsd-test@example.com', phone:'(972) 555-0100'}"
TAP, FORM, AW = "Jm0cCOeMmpgdEPnggusC", "ZwC_CPnY8okcEPnggusC", "761311353"


def kind(u):
    if TAP in u: return "ADS CLICK-TO-CALL"
    if FORM in u: return "ADS LEAD (form)"
    if "googleadservices" in u or "pagead" in u or "doubleclick" in u or "/ccm/" in u: return "ads other"
    if "collect" in u: return "ga4"
    return "meta"


with sync_playwright() as p:
    b = p.chromium.launch()
    for scen in ("A no consent (default)", "B Accept All"):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148")
        page = ctx.new_page(); hits = []; scripts = set()
        page.on("request", lambda r: scripts.add(r.url) if r.resource_type == "script" else None)
        page.route(BLOCK, lambda r: (hits.append(r.request.url), r.abort()))
        page.goto(f"{SITE}/?gclid=TSDtest1027abc", wait_until="load", timeout=60000); page.wait_for_timeout(5000)
        print(f"\n===== {scen}")
        gtm = sorted({re.search(r"id=([A-Z0-9-]+)", u).group(1) for u in scripts if "googletagmanager.com/gtm.js" in u or "gtag/js" in u})
        print("  tags loaded:", gtm, "| CallRail swap.js:", any("calltrk.com" in u and "swap" in u for u in scripts))
        if scen.startswith("B"):
            btn = page.get_by_role("button", name=re.compile("accept all", re.I))
            if btn.count(): btn.first.click(); page.wait_for_timeout(4000)
            else: print("  (no Accept All button found)")
        ck = {c["name"]: c["value"] for c in ctx.cookies()}
        print("  cookies: _gcl_aw =", ck.get("_gcl_aw", "-"), "| _gcl_au =", "yes" if "_gcl_au" in ck else "-", "| calltrk:", [k for k in ck if "calltrk" in k.lower()])
        dl = page.evaluate("JSON.stringify((window.dataLayer||[]).filter(e=>e&&e[0]==='consent').map(e=>[e[1],e[2]]))")
        print("  consent calls:", dl[:300])
        m = len(hits)
        print(f"  hits on load ({m}):", sorted({kind(u) for u in hits}))
        tels = page.eval_on_selector_all("a[href^='tel:']", "els=>els.map(e=>e.getAttribute('href'))")
        print("  tel: links on page:", sorted(set(tels))[:6])
        if tels:
            page.evaluate("""()=>{document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest("a[href^='tel:']");if(a)e.preventDefault();},true)}""")
            page.evaluate("()=>document.querySelector(\"a[href^='tel:']\").click()"); page.wait_for_timeout(4000)
            new = hits[m:]; print(f"  after tel tap: {[kind(u) for u in new]}")
            for u in new:
                if TAP in u:
                    qs = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
                    print("     click-to-call hit gclid/gcs:", qs.get("gclaw", qs.get("gclid", ["-"]))[0][:30], qs.get("gcs", ["-"])[0], qs.get("url", ["-"])[0][:80])
        m = len(hits)
        page.evaluate(f"window.dataLayer.push({LEAD})"); page.wait_for_timeout(5000)
        new = hits[m:]; print(f"  after synthetic form_submitted: {[kind(u) for u in new]}")
        for u in new:
            if FORM in u:
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
                print("     lead hit: gclid", qs.get("gclaw", ["-"])[0][:30], "| gcs", qs.get("gcs", ["-"])[0], "| user data (em/pn) present:", any(k in u for k in ("em=", "&em", "ecsid", "pn=")))
        ctx.close()

    # does the site's own code push form_submitted? grep its JS on the form pages
    print("\n===== site code: who pushes form_submitted?")
    found = {}
    for path in ("/", "/schedule", "/contact"):
        ctx = b.new_context(); page = ctx.new_page(); js = set()
        page.on("request", lambda r: js.add(r.url) if r.resource_type == "script" and "spencerairconditioning.com" in r.url else None)
        page.route(BLOCK, lambda r: r.abort())
        try:
            resp = page.goto(SITE + path, wait_until="load", timeout=60000); page.wait_for_timeout(2000)
            forms = page.eval_on_selector_all("form", "fs=>fs.map(f=>(f.getAttribute('action')||'')+' fields:'+Array.from(f.querySelectorAll('input,select,textarea')).map(i=>i.name||i.type).join(','))")
            iframes = page.eval_on_selector_all("iframe", "fs=>fs.map(f=>f.src)")
            print(f"  {path}: HTTP {resp.status if resp else '?'} forms={forms[:2]} iframes={[i[:70] for i in iframes][:3]}")
        except Exception as e:
            print(f"  {path}: {e}")
        for u in js:
            if u in found: continue
            try: src = urllib.request.urlopen(u, timeout=30).read().decode("utf-8", "ignore")
            except Exception: continue
            if "form_submitted" in src:
                i = src.find("form_submitted"); found[u] = src[max(0, i - 250):i + 200]
        ctx.close()
    for u, snip in found.items(): print(f"  FOUND in {u.split('/')[-1]}:\n    {snip}")
    if not found: print("  'form_submitted' NOT found in the site's JS")
    b.close()
