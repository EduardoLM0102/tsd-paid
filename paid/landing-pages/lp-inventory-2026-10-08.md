# Landing page inventory, all paid clients (2026-10-08)

**Rule:** one page per service. Each ad group points to the page for its service. Branded ad groups keep the homepage.

**Ranking:** clients are ranked by last-30-day spend on ads that send people to a website. That covers Google Search, Performance Max, Smart and Video/Demand Gen, plus Meta. LSA spend is listed separately and left out of the ranking, because LSA has no landing page.

**Sources and dates:** Google Ads API with `LAST_30_DAYS` through 10-07, and the Meta Ads API with `last_30d`.

**Status:** ad groups are listed if they spent in the window. Paused campaigns are noted.

| # | Client | Web-ad spend (30d) | Google (non-LSA) | Meta | LSA (not ranked) | Pages |
|---|---|---|---|---|---|---|
| — | Cool Hand Electric (in progress) | $5,190 | $4,593 | $597 | $706 | 14 (3 built) |
| 1 | Proud Pops | $59,604 | $59,604 | none found | $705 | 9 |
| 2 | Watt's Right | $11,497 | $5,023 | $6,474 | $12,787 | 4 |
| 3 | Zen Air | $10,014 | $5,267 | $4,747 | $107 | 2 |
| 4 | Neon Monkey | $9,195 | $8,430 | $765 | $898 | 3 |
| 5 | Napps | $6,254 | $4,589 | $1,665 | $1,592 | 6 |
| 6 | All Seasons AC | $6,156 | $5,561 | $595 | — | 5 |
| 7 | C&S Air | $4,688 | $4,688 | none found | $370 | 3 |
| 8 | Strickland Heating & Air | $4,404 | $4,404 | none found | — | 3 |
| 9 | Live Wire Electric | $4,315 | $4,315 | none found | $454 | 5 |
| 10 | King's Window | $3,267 | $1,615 | $1,652 | $1,343 | 3 |
| 11 | Nicks Heating and Cooling | $3,135 | $2,536 | $599 | $2,313 | 2 |
| 12 | Hawkins Siding | $2,833 | $2,833 | $0 | $4,647 | 3 |
| 13 | Integrate Comfort* | $2,820 | $2,820 | can't read (MCP off) | $24 | 3 |
| 14 | Spencer Air | $2,520 | $1,543 | $977 | $3,141 | 0 (Google is branded only) |
| 15 | Lily Pad Septic | $902 | $902 | $0 | — | 3 |
| 16 | Mission Accomplished | $742 | $0 | $742 (awareness) | $1,172 | 0 |
| — | On The Way (leaving 11/2) | $354 | access revoked | $354 | — | 0 |

\* ICS's Meta spend can't be read, so ICS was placed by comparing Google Ads + LSA only: $2,844 (PPC $2,214 + Belleville account $630). That puts it between King's Window ($2,958) and My Favorite Service Company ($1,832), the same 13th spot (Edu, 10-08).

**Total new pages outside Cool Hand: 54.** Proud Pops alone is about 45% of the web-ad spend in this list ($59.6k of $132.7k). My Favorite Service Company is Proud Pops' merged brand, so it's left out (Edu, 10-08).

**Not running, no pages for now:**
- **GC Home Service:** offboarded. Meta spent $153.
- **Gillespie's:** offboarded. Edu removed the campaigns.
- **Concrete Adventures:** not a client.
- **LSA only:** Golden Plumbing and Gray Duct.

---

## 1. Proud Pops (San Antonio). Plumbing, HVAC, electrical

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Electrician | AG1_Electrician_NearMe, AG2_Electrical_Services, + PMax Electrical | $6,671 + $5,835 + $6,889 | /services/electrical, / |
| Electrical Repair | AG3_Electrical_Repair | $6,090 | /services/electrical(/repair) |
| AC Repair | AG1_HVAC_ACRepair, + PMax HVAC | $5,012 + $9,808 | /proud-pops-hvac-services |
| AC Maintenance | AG3_HVAC_Maintenance | $5,634 | /proud-pops-hvac-services |
| Plumber | AG1_Plumbing_LeakDetection (plumber keywords) | $4,717 shared | /services/plumbing |
| Leak Detection | AG1_Plumbing_LeakDetection (leak keywords) | shared | /services/plumbing/leak-detection |
| AC Installation | AG2_HVAC_Installation | $507 | /proud-pops-hvac-services |
| Emergency Plumber | AG2_Plumbing_Emergency | $236 | /services/plumbing |
| Water Heater | AG3_Plumbing_WaterHeaters | $59 | /services/plumbing/water-heaters |

Notes:
- AG1_Plumbing_LeakDetection mixes plumber and leak detection keywords, so it needs splitting before it can point to 2 pages.
- The YouTube spend ($6,029) needs a brand page, same as Cool Hand's YouTube.

## 2. Watt's Right (Tulsa). Electrical

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Emergency Electrician | Emergency Electrician | $979 | /emergency-electric/ |
| EV Charger Installation | EV charger (+ paused EV campaign) | $704 + $888 | /upgrades/ev-charger-installation/ |
| Panel Upgrade | Panel Upgrade | $306 | /upgrades/electrical-panel-upgrades/ |
| Electrician (general) | PMax Evergreen | $1,626 | / |

Meta ($6,474) runs a TOF/MOF/BOF funnel. Check whether its ads use instant forms or the site before counting Meta pages.

## 3. Zen Air (Duluth, GA). HVAC

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| HVAC Contractor | Zen Air HVAC Nonbranded (hvac contractor keywords) | $4,528 shared | /book-hvac-service/ |
| AC Repair | same ad group (ac repair keywords) | shared | /book-hvac-service/ |

There's only one non-brand ad group, mixing HVAC contractor and AC repair keywords. Split it to get 2 pages.

**2026-10-14 update (Edu):** start with 2 broad pages, not single-service ones. Heating: "Heating Repair, Replacement & Tune-Ups in Duluth, GA". Cooling: "AC Repair, Replacement & Tune-Ups in Duluth, GA". Subheads, open items and brand rules in `clients/zen-air/landing-pages/2026-10-14-lp-plan.md`.

## 4. Neon Monkey (Fort Worth). Tree service

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Tree Trimming | Tree Trimming | $3,254 | / |
| Stump Removal | Stump Removal | $1,350 | / |
| Tree Service (general) | PMax | $3,278 | / |

## 5. Napps (Longview, TX). HVAC and plumbing

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| AC Repair | AC Repair | $1,305 | /schedule-now/ |
| Emergency Plumber | Emergency Plumber | $951 | / |
| AC Tune-Up | AC Tune-Up | $368 | /schedule-now/ |
| AC Replacement | AC Replacement | $242 | /schedule-now/ |
| Leak Detection | Leak Detection | $118 | / |
| Drain Cleaning | Drain and Sewer | $75 | / |

## 6. All Seasons AC. HVAC and Mitsubishi ductless

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Heating and Cooling Services | residential hvac | $1,076 | /ac-installations/ |
| AC Installation | Ac Installation | $903 | / |
| AC Repair | Ac Repair, air conditioning repair | $849 + $434 | /, /ac-repairs |
| Ductless Mini Split | AG1 Install & Replacement, AG2 Cost & Ductless Heating, PMax ductless | $378 + $395 + $437 | /ductless-mitsubishi-electric-hvac-systems/ |
| Mitsubishi Mini Split | AG1 Mitsubishi Brand Core, AG2 Mitsubishi + Installation | $174 + $105 | same |

Notes:
- The "Ac Repair" ad group is spending on off-topic terms (duct cleaning, portable ac). Clean it up before giving it a page.
- The dynamic search ad group ($412) picks its own pages, so it doesn't need one.

## 7. C&S Air. HVAC

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| AC Repair | AC Repair | $1,209 | /services/residential/air-conditioning/ac-repair/ |
| AC Maintenance | AC Maintenance | $391 | /ac-maintenance/ |
| Emergency AC Repair | AC Emergency | $39 | /emergency-ac-repair/ |

The Smart campaign ($2,454) uses its own landing setting. Point it at AC Repair once that page exists.

## 8. Strickland Heating & Air (Fort Worth). HVAC

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| AC Repair | AC Repair, + PMax AC | $1,635 + $1,852 | /air-conditioning-fort-worth/ac-repair/ |
| AC Maintenance | AC Maintenance | $319 | /ac-maintenance/ |
| Emergency AC Repair | AC Emergency | $234 | / |

## 9. Live Wire Electric (Lynnwood, WA). Electrical

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Electrician | 03 Residential Electrician | $1,156 | /services/category/electrical-repairs |
| Generator Installation | 01 Generator Installation | $103 | /generator-offer |
| Breaker Repair | 04 Breaker Repair | $101 | /services/circuit-breaker-repair |
| Outlet Repair | 05 Outlets & GFCI | $49 | /services/electrical-outlet-repair |
| EV Charger Installation | 08 Home EV Charger Installation | $28 | /free-ev-charger-estimate |

The older nonbranded campaign is paused. Its ad groups (Electrician near me, EV, Emergency, Panel, Electrical Repair) aren't counted.

## 10. King's Window. Glass and windows

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Glass Replacement | Glass Replacement | $1,310 | /glass-replacement/ |
| Window Replacement | Window Replacement | $169 | /window-replacement/ |
| Frameless Shower Doors | Frameless Shower Enclosures | $87 | /frameless-shower-enclosures/ |

## 11. Nicks Heating and Cooling (Hammond, LA). HVAC

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| AC Repair | AC Repair, + PMax | $1,102 + $1,072 | /, /contact-us/ |
| AC Installation | AC Installation | $156 | / |

## 12. Hawkins Siding. Siding

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Siding Contractor | Siding - General, Vinyl Siding, + PMax | $1,032 + $354 + $398 | /services/siding-installation/, / |
| Siding Repair | Siding Repair | $679 | /services/siding-installation/ |
| Siding Replacement | Siding Replacement | $370 | /services/siding-installation/ |

## 13. Integrate Comfort. HVAC

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| AC Repair | AC Repair (ad group paused now), + PMax | $531 + $1,234 | /ac-repairs/, / |
| AC Installation | AC Installation & Replacement | $202 | /ac-installations/ |
| Furnace Repair | Heating & Furnace Repair | $39 | /furnace-repairs |

The Belleville YouTube spend ($606) needs a brand page.

## 14. Spencer Air

Google is branded Search only, so no service pages are needed. Meta ($977): check where its ads send people.

## 15. Lily Pad Septic (Salina/Hutchinson, KS)

| Page | Ad group(s) | 30d | Goes to today |
|---|---|---|---|
| Septic Pumping | Septic Pumping and Repair | $453 | /get-septic-services/ |
| Porta Potty Rental | Portable Restroom Rental | $224 | /get-septic-services/ |
| Septic Installation | Septic Installation | $88 | /get-septic-services/ |

---

## Flags found while pulling this

- **Meta accounts we can't read through the API:** ICS (ranked on Google + LSA instead), Gray Duct, Rhino FB Ads Account, Your New Door Ad Account. They're active, but their spend isn't counted here.
- **Proud Pops, C&S Air, Strickland, Live Wire:** no Meta ad account showed up in our access.
- **Checked against "Client Accounts - Audit (Master doc)" on 10-08:**
  - Strickland isn't in that sheet, and Live Wire's Google account is being edited by Trade Vulcan. Edu says to keep both in the list.
  - These clients are active in the sheet but no ads are running yet, so they have no pages for now: Eagle Point, Supreme Heating, Carey & Walsh, Cartwright, Climate Experts, JR Michalski, North Bay, Rockhard, Ryan Heating & Air and Sooner Heat.
- **Not covered yet:** missing assets per client (logo, job photos, CallRail number per campaign, GHL form). That's the next pass.

---

## Step 5: what's missing per client (checked 10-08)

**How each column was checked:**
- **go.:** whether `go.<domain>` resolves. Only Cool Hand's does.
- **CallRail:** `cdn.callrail.com` in the site HTML, in the rendered page, or as a live tag in the client's GTM container (TSD GTM login).
- **GHL form:** a `leadnurturemachine` or `leadconnector` form embed on the homepage.
- **Logo:** an image file with "logo" in its name on the homepage.
- **Photos:** can't be checked from outside, so every client needs to be asked.

| Client | Site | go. | CallRail | GHL form | GTM (TSD access) | Logo on site |
|---|---|---|---|---|---|---|
| Proud Pops | custom app (Vite + Supabase), not WP | no | yes (on page) | no (forms go to Supabase) | no access | yes |
| Watt's Right | WordPress | no | yes (GTM) | no | yes | yes |
| Zen Air | WordPress | no | not found | yes | no access | yes |
| Neon Monkey | WordPress | no | not found | yes | no GTM on site | not found (only a BBB badge) |
| Napps | WordPress | no | not found | yes | no access | yes |
| All Seasons AC | WordPress | no | none (GTM checked) | yes | yes | yes |
| C&S Air | WordPress | no | yes (GTM) | yes | yes | not found |
| Strickland | WordPress | no | not found | no | no access | yes |
| Live Wire | custom site, not WP | no | none | no | no GTM on site | yes |
| King's Window | WordPress | no | yes (GTM + page) | yes | yes | yes |
| Nicks | WordPress | no | yes (GTM) | yes | yes | not found (only a BBB badge) |
| Hawkins | WordPress | no | yes (page) | yes | no access | yes |
| Integrate Comfort | WordPress | no | yes (GTM + page) | yes | yes | yes |
| Lily Pad | WordPress | no | yes (GTM) | no | yes | yes |

Even where CallRail is installed, we still need the Google Ads tracking number for each client (like Cool Hand's 469-351-1738). That needs CallRail access, which TSD doesn't have through the API.
