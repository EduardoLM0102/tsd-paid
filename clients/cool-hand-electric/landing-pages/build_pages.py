"""Build Cool Hand service landing pages from Ryan's panel upgrade model.

Usage: python3 build_pages.py
Reads _model-panel-upgrade-ryan.html, writes one HTML file per entry in PAGES.
Every swap must hit exactly the expected number of times, or the build stops.

Facts used here were checked against coolhandelectric.com and go.coolhandelectric.com on 2026-10-08:
TECL #31768, both shop addresses, hours (Mon-Fri 8-5, Sat 8-12, Sun closed), Voted Best in Ellis County,
BBB A+, Mansfield Area Chamber, easy payment plans, $37 electrical safety inspection (go. page FAQ),
AC warning signs (/ac-repair/), "leave your space as clean as we found it" (/ac-repair/),
furnace safety line (/furnace-repair/), service menus (site nav).
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
MODEL = (HERE / "_model-panel-upgrade-ryan.html").read_text()

PHONE_DISPLAY = "469-351-1738"   # Cool Hand Google Ads CallRail number (Edu, 2026-10-08)
PHONE_E164 = "+14693511738"

CHECK = re.search(r'<li data-var="SIGN_1">(<svg.*?</svg>)', MODEL, re.S).group(1)
AREAS_FAQ = ("What areas do you serve?",
             "Mansfield, Red Oak, Waxahachie, Midlothian, Burleson, Ennis, Fort Worth, South Arlington and Pantego, "
             "plus surrounding North Texas communities.")
TIMING_FAQ = ("How soon can you come out?",
              f"Call {PHONE_DISPLAY} and we will give you our first opening. Our office hours are Monday to Friday, "
              "8 AM to 5 PM, and Saturday, 8 AM to 12 PM.")
HVAC_LICENSE = '<span class="var">{{HVAC_LICENSE: TACLA number from client}}</span>'


def var(label):
    return f'<span class="var">{{{{{label}}}}}</span>'


def placeholder_reviews(service):
    cards = []
    for i in (1, 2, 3):
        cards.append(
            f'<article class="review" data-var="REVIEW_{i}"><span class="stars" aria-hidden="true">★★★★★</span>'
            f'<blockquote>{var(f"REVIEW_{i}: real Google review that mentions {service}")}</blockquote>'
            f'<footer><b>{var("NAME")}</b>, {var("TOWN")}</footer></article>')
    return '<div class="review-grid">' + "".join(cards) + "</div>"


PAGES = {
    "electrician.html": {
        "service": "Electrician",
        "service_lower": "an electrician",
        "title": "Cool Hand: Electrician in Mansfield, TX",
        "meta": f"Licensed, family-owned electricians in Mansfield, TX. TECL #31768. Straightforward pricing. Call {PHONE_DISPLAY}.",
        "promo": f'Ask about our $37 electrical safety inspection when you book. <a href="tel:{PHONE_E164}" data-call="promo">{PHONE_DISPLAY}</a>',
        "subhead": "Licensed, local electricians serving Mansfield and Red Oak. Family-owned, with straightforward pricing and quality work guaranteed.",
        "call_label": "Talk to a licensed electrician now",
        "hero_photo": "Real photo: a Cool Hand electrician on a job, Luke or a tech in frame",
        "form_head": "Get your electrical quote",
        "form_button": "Get my quote",
        "reviews_head": "Homeowners trust a cool hand with their wiring",
        "reviews_sub": None,      # keep Ryan's line and his 3 electrician reviews
        "reviews": None,
        "signs_sub": "If any of these sound like your house, get it checked before a small problem turns into a safety problem.",
        "signs": [
            ("Breakers trip again and again", "Especially when a few big appliances run at the same time."),
            ("Lights flicker or dim", "Loose connections and overloaded circuits are common causes."),
            ("Outlets or switches feel warm, spark, or stop working", "A warm or scorched outlet is a fire risk. Stop using it and call."),
            ("A burning smell or buzzing you can't trace", "Shut off that circuit at the panel if you can, then call."),
            ("You're adding something big", "An EV charger, generator, hot tub or remodel usually needs new circuits, and sometimes more panel capacity."),
            ("Older wiring or a house you just bought", "An electrical safety inspection shows what's safe and what needs work."),
        ],
        "steps_head": "How it works",
        "steps": [
            ("Call or send the form", "Tell us what's going on. We get you on the schedule."),
            ("A licensed electrician finds the problem", "We look at the issue, explain it in plain English, and give you options before any work starts."),
            ("We do the work to code and leave it clean", "Once you approve, the job is done to code and your home is left as clean as we found it."),
        ],
        "mid_head": "Breaker tripping or lights flickering? Talk to a licensed electrician.",
        "faq_head": "Electrician questions, answered straight",
        "faqs": [
            ("How much does an electrician cost in Mansfield?",
             "It depends on the job. We look at the problem first and give you options before any work starts. "
             "Ask about our $37 electrical safety inspection. Easy payment plans are available."),
            TIMING_FAQ,
            ("Are you licensed and insured?",
             "Yes. Licensed and insured, with Texas electrical contractor license TECL #31768. BBB A+ rated, "
             "and members of the Mansfield Area Chamber of Commerce."),
            ("What kind of electrical work do you do?",
             "Repairs, panel upgrades, outlets and switches, ceiling fans, lighting, surge protection, smoke and CO detectors, "
             "generators, EV chargers and electrical safety inspections."),
            AREAS_FAQ,
        ],
        "final_head": "Get it done right by a licensed electrician.",
        "final_sub": None,        # keep Ryan's line
    },
    "ac-repair.html": {
        "service": "AC Repair",
        "service_lower": "AC repair",
        "title": "Cool Hand: AC Repair in Mansfield, TX",
        "meta": f"AC repair in Mansfield, TX from a family-owned, licensed local team. Honest options before any work. Call {PHONE_DISPLAY}.",
        "promo": None,
        "subhead": "AC acting up? Our licensed techs diagnose it and fix it right the first time. Fast, honest AC repair from a family-owned local team.",
        "call_label": "Talk to a licensed AC tech now",
        "hero_photo": "Real photo: a Cool Hand tech working on an AC unit",
        "form_head": "Request AC repair",
        "form_button": "Request service",
        "reviews_head": "Homeowners trust a cool hand with their AC",
        "reviews_sub": "Real Google reviews from Cool Hand customers.",
        "reviews": "AC repair",
        "signs_sub": "If your AC is doing any of these, it's worth getting it checked before the problem gets worse.",
        "signs": [
            ("Warm or weak airflow", "The system runs, but the house never gets cool."),
            ("Unusual noises or smells", "Grinding, squealing, rattling or a burning smell from the unit or the vents."),
            ("It turns on and off too often", "Short cycling wears the system out and leaves rooms uncomfortable."),
            ("Energy bills keep going up", "A struggling AC works harder to do the same job."),
            ("Uneven cooling from room to room", "Some rooms stay hot no matter where the thermostat is set."),
            ("Ice on the unit or the lines", "Turn the system off and call. Running it frozen can damage it."),
        ],
        "steps_head": "How your AC repair works",
        "steps": [
            ("Call or send the form", "Tell us what your AC is doing. We get you on the schedule."),
            ("A licensed tech finds the real cause", "We diagnose the problem and give you honest options so you can decide what's best for your home and budget."),
            ("We fix it and leave it clean", "Once you approve the work, we get it done and leave your space as clean as we found it."),
        ],
        "mid_head": "AC blowing warm air? Talk to a licensed tech.",
        "faq_head": "AC repair questions, answered straight",
        "faqs": [
            ("How much does AC repair cost in Mansfield?",
             "It depends on what's wrong. We diagnose it first and give you options before any work starts. "
             "Easy payment plans are available."),
            TIMING_FAQ,
            ("Are you licensed?",
             f"Yes. Our HVAC work is done by licensed techs ({HVAC_LICENSE}). Cool Hand also holds Texas electrical "
             "contractor license TECL #31768, is BBB A+ rated, and is a member of the Mansfield Area Chamber of Commerce."),
            ("Should I repair my AC or replace it?",
             "If a repair makes sense, we will tell you. If your system is near the end of its life, we lay out both options "
             "so you can choose. We also install and replace AC systems."),
            AREAS_FAQ,
        ],
        "final_head": "Get your AC fixed right the first time.",
        "final_sub": "Honest options up front, work done right, your home left clean. Call now or send the form and we will call you.",
    },
    "hvac-repair.html": {
        "service": "HVAC Repair",
        "service_lower": "HVAC repair",
        "title": "Cool Hand: HVAC Repair in Mansfield, TX",
        "meta": f"HVAC repair in Mansfield, TX from a family-owned, licensed local team. AC, furnace and heat pump. Call {PHONE_DISPLAY}.",
        "promo": None,
        "subhead": "Family-owned HVAC company serving North Texas. From AC to furnace, our licensed techs handle it all.",
        "call_label": "Talk to a licensed HVAC tech now",
        "hero_photo": "Real photo: a Cool Hand tech on an HVAC job, AC unit or furnace",
        "form_head": "Request HVAC service",
        "form_button": "Request service",
        "reviews_head": "Homeowners trust a cool hand with their heating and cooling",
        "reviews_sub": "Real Google reviews from Cool Hand customers.",
        "reviews": "AC, heating or HVAC work",
        "signs_sub": "Heating or cooling, these are the signs your system needs a licensed tech.",
        "signs": [
            ("The air is the wrong temperature", "Warm air when you're cooling, or cool air when the heat is on."),
            ("Uneven temperatures from room to room", "Some rooms never get comfortable."),
            ("Unusual noises or smells", "Banging, squealing, rattling or a burning smell when the system runs."),
            ("It turns on and off too often", "Frequent cycling wears the system out and wastes energy."),
            ("Energy bills keep going up", "A struggling system works harder to do the same job."),
            ("Something seems off with the furnace", "Some furnace problems can be a safety risk. Shut the system down and call."),
        ],
        "steps_head": "How your HVAC repair works",
        "steps": [
            ("Call or send the form", "Tell us what your system is doing. We get you on the schedule."),
            ("A licensed tech finds the real cause", "We diagnose the problem and give you honest options so you can decide what's best for your home and budget."),
            ("We fix it and leave it clean", "Once you approve the work, we get it done and leave your space as clean as we found it."),
        ],
        "mid_head": "Heating or cooling acting up? Talk to a licensed tech.",
        "faq_head": "HVAC repair questions, answered straight",
        "faqs": [
            ("How much does HVAC repair cost in Mansfield?",
             "It depends on what's wrong. We diagnose it first and give you options before any work starts. "
             "Easy payment plans are available."),
            TIMING_FAQ,
            ("Are you licensed?",
             f"Yes. Our HVAC work is done by licensed techs ({HVAC_LICENSE}). Cool Hand also holds Texas electrical "
             "contractor license TECL #31768, is BBB A+ rated, and is a member of the Mansfield Area Chamber of Commerce."),
            ("What do you work on?",
             "AC repair and replacement, furnace repair and replacement, heat pumps, thermostats, duct cleaning "
             "and indoor air quality."),
            AREAS_FAQ,
        ],
        "final_head": "From AC to furnace, we handle it all.",
        "final_sub": "Honest options up front, work done right, your home left clean. Call now or send the form and we will call you.",
    },
}


PHONE_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2'
              'a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1'
              'c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>')

# Mobile: round call button fixed bottom left (Edu, 2026-10-08) replaces Ryan's full-width bottom bar.
# The quote link moves to a small pill on the right. The builder toggle moves right so nothing overlaps.
MOBILE_CSS = """/* ===== MOBILE FLOATING CALL BUTTON (round, bottom left) + QUOTE PILL ===== */
.fab-call,.fab-quote{display:none}
@media (max-width:819px){
  .fab-call{position:fixed;left:calc(16px + env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:50;width:66px;height:66px;border-radius:50%;display:grid;place-items:center;background:var(--brand-cta);color:var(--brand-cta-ink);text-decoration:none;border:3px solid #fff;box-shadow:0 10px 26px rgba(0,0,0,.32);-webkit-tap-highlight-color:transparent;transition:transform .15s ease}
  .fab-call:active{transform:scale(.93)}
  .fab-call svg{width:30px;height:30px}
  .fab-call::before{content:"";position:absolute;inset:-3px;border-radius:50%;background:var(--brand-cta);z-index:-1;animation:fab-pulse 2.4s ease-out infinite}
  .fab-quote{position:fixed;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(25px + env(safe-area-inset-bottom,0px));z-index:50;display:inline-flex;align-items:center;min-height:48px;padding:0 1.2rem;border-radius:999px;background:var(--brand-deep);color:#fff;border:1px solid rgba(255,255,255,.3);font-family:var(--font-display);font-weight:800;font-size:1.15rem;text-decoration:none;box-shadow:0 8px 20px rgba(0,0,0,.28);-webkit-tap-highlight-color:transparent}
  footer.site{padding-bottom:calc(2.5rem + 100px + env(safe-area-inset-bottom,0px))}
}
/* small phones: the 4:3 map box forced the page wider than 320px; also give small text links a 44px tap area */
@media (max-width:899px){.map-slot{aspect-ratio:auto;min-height:240px}.map-slot iframe{min-height:240px}}
@media (max-width:819px){
  .promo a,.midcta .alt a,.map-slot a,footer.site a{display:inline-block;padding-block:.7rem;margin-block:-.7rem}
  .text-call{display:inline-block;padding-block:.25rem}
}
/* small phones: top bar logo and call pill collided at 320px */
@media (max-width:380px){.top-call{font-size:1.1rem;padding:.5rem .8rem}.top-call svg{display:none}.logo-ph{min-width:0;padding:0 .6rem}.logo img{max-width:130px}}
@keyframes fab-pulse{0%{transform:scale(1);opacity:.55}70%{transform:scale(1.55);opacity:0}100%{transform:scale(1.55);opacity:0}}
@media (prefers-reduced-motion:reduce){.fab-call::before{animation:none;opacity:0}}
"""


def mobile_cta(h, p):
    h = swap(h, r"/\* ===== MOBILE STICKY BOTTOM BAR ===== \*/.*?@media \(max-width:819px\)\{body\{padding-bottom:calc\(72px \+ env\(safe-area-inset-bottom,0px\)\)\}\}\n",
             MOBILE_CSS, 1, "mobile bar css")
    h = swap(h, r"\.bt\{position:fixed;left:\.75rem;", ".bt{position:fixed;right:.75rem;", 1, "builder toggle side")
    nav = (f'<nav aria-label="Quick contact">'
           f'<a class="fab-call" href="tel:{PHONE_E164}" data-call="mobile-button" aria-label="Call Cool Hand at {PHONE_DISPLAY}">{PHONE_ICON}</a>'
           f'<a class="fab-quote" href="#quote">{p["form_button"]}</a></nav>')
    return swap(h, r'<nav class="mbar" aria-label="Quick contact">.*?</nav>', nav, 1, "mobile bar html")


def swap(html, pattern, repl, expected, label):
    new, n = re.subn(pattern, repl, html, flags=re.S)
    if n != expected:
        raise SystemExit(f"{label}: expected {expected} match(es), got {n}")
    return new


def span(name, text, expected=1):
    return (rf'(<span data-var="{name}">).*?(</span>)', lambda m: m.group(1) + text + m.group(2), expected, name)


def build(p):
    h = MODEL
    # fixes that apply to every page
    h = swap(h, r"Luke and Christine's", "Luke and Kristen's", 1, "owner name")
    h = swap(h, r'(<span data-var="HERO_META">).*?(</span>)',
             lambda m: m.group(1) + "Family-owned in Red Oak and Mansfield. Easy payment plans available." + m.group(2), 1, "HERO_META")
    h = swap(h, r"<br>Emergency service available</span>", "</span>", 1, "hours emergency line")

    h = swap(h, r"<title>.*?</title>", f"<title>{p['title']}</title>", 1, "title")
    h = swap(h, r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + p["meta"] + m.group(2), 1, "meta")
    if p["promo"]:
        h = swap(h, r'(<div class="promo" data-var="PROMO">).*?(</div>)', lambda m: m.group(1) + p["promo"] + m.group(2), 1, "promo")
    else:
        h = swap(h, r'<div class="promo" data-var="PROMO">.*?</div>\n*', "", 1, "promo")

    for args in [span("SERVICE", p["service"], 2), span("SUBHEAD", p["subhead"]), span("CALL_LABEL", p["call_label"], 2),
                 span("FORM_HEAD", p["form_head"], 2), span("FORM_BUTTON", p["form_button"], 2),
                 span("REVIEWS_HEAD", p["reviews_head"]), span("SERVICE_LOWER", p["service_lower"]),
                 span("SIGNS_SUB", p["signs_sub"]), span("STEPS_HEAD", p["steps_head"]), span("MID_HEAD", p["mid_head"]),
                 span("FAQ_HEAD", p["faq_head"]), span("FINAL_HEAD", p["final_head"])]:
        h = swap(h, *args)
    if p["reviews_sub"]:
        h = swap(h, *span("REVIEWS_SUB", p["reviews_sub"]))
    if p["final_sub"]:
        h = swap(h, *span("FINAL_SUB", p["final_sub"]))
    if p["reviews"]:
        h = swap(h, r'<div class="review-grid">.*?</div>', placeholder_reviews(p["reviews"]), 1, "reviews")

    h = swap(h, r'(<div class="photo-slot" data-var="HERO_PHOTO"><svg.*?</svg>).*?(</div>)',
             lambda m: m.group(1) + p["hero_photo"] + m.group(2), 1, "hero photo")

    signs = "".join(f'<li data-var="SIGN_{i}">{CHECK}<div><b>{b}</b><span>{s}</span></div></li>'
                    for i, (b, s) in enumerate(p["signs"], 1))
    h = swap(h, r'<ul class="sign-list">.*?</ul>', f'<ul class="sign-list">{signs}</ul>', 1, "signs")

    steps = "".join(f'<li data-var="STEP_{i}"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(p["steps"], 1))
    h = swap(h, r'<ol class="steps">.*?</ol>', f'<ol class="steps">{steps}</ol>', 1, "steps")

    faqs = "".join(f'<details{" open" if i == 1 else ""} data-var="FAQ_{i}"><summary>{q}</summary><p>{a}</p></details>'
                   for i, (q, a) in enumerate(p["faqs"], 1))
    h = swap(h, r'(<div class="faq" style="margin-top:1.5rem">).*?(</div>)', lambda m: m.group(1) + faqs + m.group(2), 1, "faqs")

    h = mobile_cta(h, p)
    h = swap(h, r'lp_service:"Electrical Panel Upgrade"', f'lp_service:"{p["service"]}"', 2, "lp_service")
    # phone last, so it also catches the promo and footer links
    h = swap(h, r"469-436-5467", PHONE_DISPLAY, h.count("469-436-5467"), "phone display")
    h = swap(h, r"\+14694365467", PHONE_E164, h.count("+14694365467"), "phone e164")
    for leftover in ["469-436-5467", "4694365467", "Christine", "Electrical Panel Upgrade", "Emergency service"]:
        if leftover in h:
            raise SystemExit(f"leftover '{leftover}' in {p['title']}")
    return h


if __name__ == "__main__":
    for name, page in PAGES.items():
        (HERE / name).write_text(build(page))
        print("wrote", name)
