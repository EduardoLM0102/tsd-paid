---
name: tsd-landing-page-rollout
description: "Oct 2026 TSD landing page rollout Edu owns: 1 page per service on client go. subdomain, template v1 + Cool Hand panel model page, 5-step ask"
metadata:
  node_type: memory
  type: project
  originSessionId: 3a8163b9-f75e-457b-bb5e-f2a7f5d2c859
  modified: 2026-10-08T20:50:15.773Z
---

Assigned to Edu 2026-10-08 by Ryan (COO), in the group DM with JB, Ryan and Edu. Edu sent step 1 at 18:12 BRT. Edu owns the rollout and can task Sha or anyone else.

**The 5 steps:**
1. List every active Cool Hand ad group and the pages needed, 1 per service.
2. Fill the service fields for each page from its ad group.
3. Build Cool Hand's other pages from the panel upgrade model page.
4. Do the same inventory for every client running paid ads, ranked by ad spend.
5. Flag anything missing (logos, photos, CallRail numbers) and he routes the asks.

**Rules:**
- 1 service per page.
- H1 = exact ad keyword + "in [City, ST]".
- The CallRail number for that ad group is the biggest element on the page, never the main line.
- Real logo, reviews and photos only.
- The brand block (brand line, owner story, stand for/against, video) is on every page. JB signs off the brand line and the stand-against list.
- Production pages live on the client's go. subdomain in WordPress.
- GTM events are `lp_call_click` and `lp_form_submit`, and the GHL form passes gclid/fbclid/utm.

**Owners, per the template's swap table:**
- Edu: message match (service, city, subhead, promo) and checking content against search terms.
- Sara: writes content.
- Sha: builds.
- Johnny/Sha: CallRail.
- Alex: GHL and conversions.
- Angela Moyer/Marlo: collect photos and logos.

**Cool Hand (10-08 pull, last 30 days):** about 80% of non-brand Search spend sits in 3 services: Electrician (General+Broad, $1,564), AC repair ($677) and HVAC repair (Furnace-Heating, $368). Panel-Upgrade, the model page, spent only $7.

**Flags on the model page:**
- It says "Luke and Christine"; the owners are Luke and Kristen.
- Phone 469-436-5467 is the same number as on the current go. LP, while the site and call asset use 469-550-1102.
- It claims "Emergency service available" while the hours conflict is unresolved.
- The logo and photo placeholders are still showing.
- The form is a demo, not wired to GHL.

The current YouTube LP combines electrical and HVAC, which breaks rule 1.

**Cool Hand phones (10-08):**
- Edu confirmed the Google Ads CallRail number is **469-351-1738**. It's the only Google Ads number so far; no per-ad-group numbers yet.
- The model page and the current YouTube LP use 469-436-5467, which is unexplained.
- The Google call asset dials the main line 469-550-1102, so CallRail misses ad-button calls. Switching it was offered; it's a live change, so only on Edu's go.
- CallRail swap.js runs in GTM-KWZDRBVQ tag 26 on All Pages, live, including the go. LP.

**Edu's decisions, 10-08:**
- YouTube ads will go to a main page copied from an existing one.
- No per-ad-group CallRail numbers: 469-351-1738 goes on every Cool Hand page.
- Edu will get the logo, job photos and GHL form himself.
- The 4.8/175 and $25k guarantee claims are still unverified; check them quietly before the build.

**Step 2 draft, 10-08 (message-match fields for the top 3, from live RSAs):**
- The Electrician page covers both Electrician-General and Electrician-Broad. Its promo is the $37 inspection, which is in the Electrician-Broad ad but wasn't found on /specials/ in static HTML on 10-08, so confirm it's still running.
- AC Repair and HVAC Repair (Furnace-Heating) have no offer.
- Every one of these RSAs says "Book Online in Minutes" or "Book your visit online", but the LP is call plus a callback form. That's a message-match conflict, and Edu decides how to handle it.
- Search terms are mostly Fort Worth, Dallas and Arlington plus competitor names, i.e. the open 09-24 geo/negatives issue. See [[tsd-cool-hand-electric]].

**Built 10-08:** `clients/cool-hand-electric/landing-pages/` contains:
- electrician.html, ac-repair.html and hvac-repair.html, from Edu's approved H1s, subheads and promo.
- `build_pages.py`, which regenerates from Ryan's model (`_model-panel-upgrade-ryan.html`). Add the next pages as entries in PAGES.

These are kept as files, NOT published as artifacts, because they carry real-client branding.

**Placeholders still in the pages:** logo, hero photos, AC/HVAC reviews (Sha), and the HVAC license (TACLA) number.

**Still unverified:** "4.8 from 175" and the $25k Good Contractors guarantee.

**Content changes from Ryan's model:**
- The AC and HVAC pages also show the electrical brand line "Cool hands on live wires.", which still needs JB's approval.
- The step "Call or book online" became "Call or send the form".

**Mobile pass, 10-08 (Edu asked for a round fixed call button, bottom left):**
- `build_pages.py` swaps Ryan's full-width bottom bar for a 66px round yellow call button (bottom left, pulse ring, white border) plus a quote pill on the right. The builder toggle moved to the right.
- It also fixes 2 bugs that are in Ryan's TEMPLATE too: at 320px the 4:3 `.map-slot` overflowed the page by 20px, and the top bar logo collided with the call pill.
- Small text links now have 44px tap areas.
- Tested 320/360/390/430: no horizontal scroll, no overlaps.
- Not yet told to Ryan: the bottom-bar replacement and the template bugs.

**Step 4 done, 10-08:** `paid/landing-pages/lp-inventory-2026-10-08.md`.
- 16 clients ranked by 30-day web-ad spend (Google non-LSA + Meta), 57 pages outside Cool Hand.
- Proud Pops is $59.6k / 9 pages, about 44% of the spend.
- No pages needed: Spencer Air (Google is branded only), Mission Accomplished and On The Way (Meta only), GC Home and Concrete Adventures (paused).
- Next pass: missing assets per client.

**Step 5 check, 10-08:** results are in the inventory file.
- No client except Cool Hand has a go. subdomain.
- Proud Pops' site is a custom Vite + Supabase app, and Live Wire's is a custom site, so neither is WordPress.
- No GHL form on Proud Pops, Watt's Right, Strickland, Live Wire or Lily Pad.
- No CallRail found on All Seasons, Live Wire or Neon Monkey. Unknown for Zen Air, Napps and Strickland (no GTM access).
- TSD's GTM login can't see the containers for Proud Pops, Zen Air, Napps, Strickland or Hawkins.

**10-09:**
- JB asked at 14:31 BRT to confirm all Cool Hand LPs are live with CallRail tracking. Edu replied "by EOD".
- Edu told Sha to skip photos (no real job photos). Sha has the logo.
- AT Internal Request for Sha created: task `bd47275a-1a17-4239-9a20-61f482b18915`, WebDev, Execution = Sha (high priority, due 10-09 23:00Z), Review & Close = Edu. The brief follows the template build guide (non-negotiables, swap list by group, production notes, QA).
- Ryan's source Google Doc (`10KyW9g6e08RIyJDUPOtn4MwQ_bybnmRxq4PyzqS-GPo`) is NOT readable: the Drive connector is Edu's gmail and export returns 401. Ryan's artifacts aren't shared with this login either. Local copies are in ~/Downloads: `TSD Landing Page Template v1 (Copy).html` (has the build guide) and the panel-upgrade copy.
- $25k Good Contractors guarantee is VERIFIED: badge in the coolhandelectric.com footer. "4.8 from 175" is still unverified, and Sha was told to match the live GBP numbers.
- The main site returns 403 to curl, but WebFetch works.
- Edu asked for a copy of the home page at go.coolhandelectric.com/home/ for the BRANDED Search campaign, and it was added to the same AT task (Sha). Instructions: same content, every phone number swapped to 469-351-1738, GTM-KWZDRBVQ on the page, Book Now and the contact form kept working, noindex (Claude added noindex to avoid duplicating the main home page). The pattern for other clients is go.<clientsite>/home.
- **Division of labor (Edu, 10-09):** everything GTM related (tags, triggers, conversions, Preview testing) is Edu's. WebDev/Sha ONLY installs the container snippet. Never put GTM QA in a WebDev brief. **ALL testing (test calls, test leads, tracking) is also Edu's.** WebDev only puts the right number on the page and checks that it's correct. The brief was updated to match, plus the 2-GBP rating rule, and the $37 promo was VERIFIED live on /specials/ 10-09.
- **10-09 QA of Sha's build:** all 3 service pages LIVE and match the brief (/electrician/, /ac-repair/, /hvac-repair/).
  - Every page shows 4.9 from 420, which is the Mansfield GBP. The Red Oak GBP is 4.8/186.
  - Mo's GHL form "Electrician, AC Repair, HVAC Repair" (id S86ShApLGYxXYu8HSzHK, link.leadnurturemachine.com) is embedded. The page script appends gclid/utm to the iframe src. There are no hidden gclid inputs in the GHL form DOM. lp_form_submit no longer fires, so Edu needs a GHL submit trigger in GTM.
  - The homepage copy is at the go. ROOT (https://go.coolhandelectric.com/), not /home/. It is noindex, and every number is 469-351-1738.
  - It does NOT load the RecreateAI script. On the main site, "Book Online" opens the RecreateAI booking modal (form.recreateai.com) and fires dataLayer `schedule_bot_form_stage_click`, which is the "Book Now" conversion; the same script runs the chat bubble. On the copy, Book Online only scrolls to the GHL form.
  - The copy also swapped the Elementor contact form for the GHL form and has no FB pixel 787560649972471. Playwright desktop runs get bot-blocked unless a Safari UA is used plus --disable-blink-features=AutomationControlled.
- **10-09 ad changes (Edu's go):** paused Smoke-CO, Ceiling-Fan, Generator and Outlet ad groups. HVAC-General-Broad → go./hvac-repair/. YouTube (4 Demand Gen ads) → go. homepage root. Logged in the client google-ads-log.md. The main 5 ad groups still wait on Edu's test lead + GHL GTM trigger before their URL swap. Book Online fix on the go. homepage was NOT live at 10-09 re-check.
- **10-09 GTM (Cool Hand container 6370314680/260649558):**
  - Edu's v6 added the GHL Listener (tag 27) and the trigger GHL Lead (28, `ghl_form_submit`). But it also detached the main-site Contact Form trigger and deleted the Book Now lead tags.
  - Claude published v7 on Edu's go: Contact Form tags 15/20 fire on trigger 11 + 28, and the Book Now tags were restored as 29/30.
  - Logged in clients/cool-hand-electric/gtm-log.md.
  - When the main ad groups move to go., keep both triggers: sitelinks + organic still hit the main site.
- **10-09 evening: ALL 17 serving Cool Hand ads now land on go.** (Edu's go)
  - Branded goes to go./. Electrician/panel/breaker/surge go to /electrician/. AC repair/install go to /ac-repair/. HVAC/furnace/heat pump go to /hvac-repair/.
  - The 12 edited ads were in review at 10-09; ⚑ check they're APPROVED ~10-10.
  - Still on the main site: sitelinks, AC-Repair's 3 ad-group sitelinks, and the call asset (469-550-1102).
- **10-09 sitelinks:** Google requires every sitelink in a campaign to go to a different page AND not to the ad's own page. That caps how many go. sitelinks a campaign can use (4 go. pages total).
  - Branded + YouTube got 3 new go. sitelinks (assets 428923086331/079863/086340). The AC-Repair ad-group sitelinks were unlinked.
  - Electrical (8) + HVAC (7) sitelinks are still on the main site, pending Edu's choice. The real fix is more go. service pages (panel, generator, EV, $37 inspection, etc).
