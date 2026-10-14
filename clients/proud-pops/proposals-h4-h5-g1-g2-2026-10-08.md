# Proud Pops — H4 / H5 / G1 / G2 findings and proposals (2026-10-08)

Read-only analysis. Nothing below is applied yet; each "Proposed action" needs Edu's OK.
Scripts: `scripts/proud_pops_h4_pricing.py`, `proud_pops_h5_youtube_brand.py`, `proud_pops_g1_geo.py`, `proud_pops_g2_qs.py`;
ad drafts: `clients/proud-pops/g2_rsa_drafts_2026-10-08.py` (validated by Google, nothing created).

---

## H4 — The "/pricing" clicks

**What it is:** a **"See Our Pricing" sitelink**. Sitelink clicks cost **$10,772 in 30 days**:

| Campaign | Sitelink spend (30d) | Share of campaign spend |
|---|---:|---:|
| Electrical | $5,996 | ~33% |
| HVAC | $2,657 | |
| Plumbing | $1,757 | |
| Branded | $362 | |

**Does /pricing lead to bookings?** Mostly yes. GA4, Google Ads Search sessions, last 30 days, customer leads only
(job applications excluded):

| Landing page | Sessions | Customer leads | Rate |
|---|---:|---:|---:|
| Homepage | 254 | 11 | 4.3% |
| /pricing | 126 | 4 | 3.2% |
| /proud-pops-hvac-services | 79 | 6 | 7.6% |
| /services/electrical | 30 | 0 | 0% (pre-B7, small sample) |

Only 16 of 126 /pricing sessions went on to /schedule.

**Problems found:**
1. **Account-level sitelink "Contact Us" points to the old domain** (txproblemsolvers.com/contact/contact-us/). With Google's click
   ID attached, the redirect **drops the click ID and lands on the homepage**, so those clicks (105 in 30d) can't be credited to
   the ads.
2. **3 more old-domain sitelinks are still ENABLED** (Air Conditioning Services, Bathroom Plumbing, Heat Pumps). 0 impressions,
   dead weight.
3. **There is no sitelink straight to the booking form (/schedule).**

**Proposed actions:**
- **H4a** Repoint "Contact Us" → https://proudpops.com/contact. Better: replace it with "Book a Free Pop-In" → https://proudpops.com/schedule.
- **H4b** Remove the 3 dead old-domain sitelinks.
- **H4c** Add a "Book a Free Pop-In" sitelink → /schedule on all 4 Search campaigns.
- Keep "See Our Pricing". It converts close to the homepage and price-checkers self-select into it.
- Optional client ask: a stronger "Schedule" button on /pricing.

---

## H5 — Is YouTube working?

**Spend since Aug 8: $12,298**

| Campaign | Spend | Impressions | Views | Cost per view | Watched to end |
|---|---:|---:|---:|---:|---:|
| San Antonio "VideoViews" | $6,147 | 819k | 547k | $0.011 | 65% |
| New Braunfels "Awareness" | $6,151 | 365k | 263k | $0.023 | 72% |

**Where the views play:**
- **San Antonio: largely kids' content.** Top channels: YouTube Movies, **Disney Jr., El Payaso Plim Plim, Bluey, Ms Rachel
  (toddler learning), Super Simple Songs**. That's why the views are so cheap. Kids aren't the ones hiring a plumber.
- **New Braunfels: 76% smart-TV apps** (Samsung TV Plus, LG Channels, Tubi, Pluto TV). Real home viewers, but no way to tie
  them to results.

**Brand lift can't be measured with what we have:**
- Branded Search was paused from late May to Aug 9, so there's no "before" period.
- GA4's Direct/Organic traffic is unusable as a proxy. Before August it was inflated by bot-like visits (Miami, Flower Mound,
  Wheaton, even France), then Direct dropped ~80% in late August, most likely when the cookie banner started blocking
  measurement.
- Estimated branded searches (impressions ÷ impression share) rose from ~130/week (mid-Aug) to ~290/week (mid-Sep), then
  ~170–220. That's suggestive only.
- **Branded doesn't target New Braunfels at all** (see G1), so New Braunfels brand searches that YouTube creates get no
  Branded ad.

**Proposed actions:**
- **H5a (now)** San Antonio YouTube: exclude kids / "made for kids" content and the kids channels above. Optionally move it to
  the same Awareness setup as New Braunfels.
- **H5b** Fix G1 first (Branded covers New Braunfels). Then run a **4-week geo test**: pause New Braunfels YouTube, keep San Antonio,
  and compare branded searches by city. Or ask the Google rep about a Brand Lift study with search lift.
- **November budget:** $6k/month with no measurable outcome. Keep it only with a measurement plan. If something gets cut first,
  cut the San Antonio campaign.

---

## G1 — Location targeting

**Today:**

| Campaign | Targets | Mode |
|---|---|---|
| Branded | San Antonio city only | presence |
| Search HVAC | San Antonio city only | **presence OR interest** |
| Search Plumbing | San Antonio city only | presence |
| PMax HVAC | San Antonio city only | presence |
| Search Electrical | San Antonio, Boerne, Fair Oaks Ranch, Helotes, New Braunfels | presence |
| PMax Electrical | same 5 | **presence OR interest** |
| LSA (client-declared service area) | 47–50 cities | |

**The gap:** Proud Pops serves (by its own LSA settings and site) New Braunfels, Boerne, Schertz, Cibolo, Converse, etc., but
Branded, HVAC and Plumbing don't show there. Branded missing New Braunfels is the costliest gap, because the YouTube campaign
drives brand searches there.

**Proposed actions** (budgets unchanged; this widens where the same money can be spent):
- **G1a Branded → the full in-account LSA service area (47 cities).** Brand searches are cheap (~$10 / click) and high intent.
- **G1b HVAC + Plumbing Search → core metro (20 cities, all from the client's LSA list):**
  - inner ring: San Antonio, Alamo Heights, Castle Hills, Leon Valley, Kirby, Windcrest, Live Oak
  - northeast: Universal City, Converse, Selma, Schertz, Cibolo, Garden Ridge, Timberwood Park, New Braunfels
  - northwest: Helotes, Fair Oaks Ranch, Boerne, Bulverde, Spring Branch
  - Leave the far rural LSA towns (Kerrville, Pleasanton, Hondo, San Marcos…) to LSA.
- **G1c** Switch Search HVAC and PMax Electrical from "presence or interest" to **"presence"**. PMax Electrical currently gets
  clicks from Canyon Lake, which it doesn't target.
- PMax HVAC: no change (pause pending client approval, P-2).

---

## G2 — Quality Score and new ads

**Expected CTR is "below average" on most spend:**

| Ad group | 30d spend | % of spend with expected CTR below average |
|---|---:|---:|
| HVAC AG3 Maintenance | $5,634 | 65% |
| Electrical AG1 Electrician Near Me | $5,577 | **91%** (ad relevance also below average) |
| Electrical AG2 Services | $5,052 | 83% |
| HVAC AG1 AC Repair | $5,012 | **100%** |
| Electrical AG3 Repair | $3,353 | 77% |

**The current ads also make claims the site doesn't support:** "5-Star" (it's 4.8), "Same-Day" on Electrical and Plumbing (the
site only promises same-day for HVAC), "Upfront Pricing", "Trusted", "Affordable", "We Answer Every Call", "Book Online in
Minutes". That's a quality problem and a client-trust problem.

**Drafts ready** (`g2_rsa_drafts_2026-10-08.py`): 5 new RSAs, 15 headlines + 4 descriptions each, keyword-led headlines for ad
relevance, homeowner voice, every claim verified on the site 10-08. **Google validate-only: all 5 accepted.**
- Electrical AG1 → /services/electrical. "Electrician in San Antonio", "Need an Electrician? Call Pops", "TECL Licensed
  Electricians", "Breaker Keeps Tripping?", "Rated 4.8 on Google", "A Real Person Picks Up"…
- Electrical AG2 → /services/electrical. "Electrical Contractor Near You", "Panel Upgrades and EV Chargers", "Whole-Home Surge
  Protection", "Safety Inspection With Report"…
- Electrical AG3 → **/services/electrical/repair** (a better match than the overview page). "Breaker Won't Reset?",
  "We Bring a Thermal Camera", "Written Repair Warranty"…
- HVAC AG3 → /proud-pops-hvac-services. "AC Tune-Up in San Antonio", "Same-Day HVAC Appointments", "Pop's Perks: 2 Tune-Ups a
  Year", "Don't Wait for a Breakdown"…
- HVAC AG1 → /proud-pops-hvac-services. "AC Quit? Same-Day Repair", "Flat-Rate Price Before Work", "We Fix Any Brand of AC",
  "Fix First, Replace if Needed"…

**Proposed actions:**
- **G2a** Create the 5 new RSAs next to the current ads (no downtime).
- **G2b** Once each is approved, pause the old ad in that ad group (removes the unverified claims).
- **G2c** Second batch, same treatment: Plumbing AG1 / AG2 / AG3, HVAC AG2 Installation and Branded (same unverified claims).
