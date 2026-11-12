# Zen Air PPC: why nothing is working (diagnosis, 2026-10-29)

Account `4360840956`. Read-only, nothing changed. Window 2026-07-10 (PPC back on after the June billing stop) to 10-29
unless noted. Builds on `2026-07-09-geo-and-account-findings.md` and `2026-09-30-ppc-cost-deep-dive.md`; the leaks found
there (PMax on YouTube, broad keywords, competitor names, uncapped bidding, Display on NB) are already fixed. This is about
what is still broken after those fixes.

## Short answer

Generic HVAC search in Gwinnett costs more per click than Zen Air can make back, and Zen Air's ads are weaker than the
ones they compete against. Every version we ran failed for one of two reasons:

- **Uncapped (Jul–Sep):** we paid $28–33 a click and the only searches that turned into calls were other companies' names.
- **Capped at $18 (Sep 30–now):** we can't win the real service searches, so we buy leftovers (research, DIY, model numbers)
  that never call.

LSA, which sits above these ads on the same searches, books jobs at ~$28 each. PPC has never come close.

## 1. The real result since 07-10

| Month | Spend | 60s+ ad calls | Forms | Peach AI bookings | Real leads | Per lead |
|---|---|---|---|---|---|---|
| Jul (from 10th) | $7,292 | 12 | 4 | 0 | ~16 | ~$456 |
| Aug | $4,716 | 7 | 2 | 4 | 9–13 | $363–524 |
| Sep | $4,932 | 11 | 2 | 4 | 13–17 | $290–379 |
| Oct (to 29th) | $1,957 | 2 | 0 | 3 | 2–5 | $391–978 |
| **Total** | **$18,897** | **32** | **~8** | **~11** | **~40–51** | **~$370–470** |

Forms exclude the August Display junk (297 "forms" + 215 `ghl_contact_us` from $0.20 Display clicks). Peach AI bookings
may overlap with the calls, so the range's top end is generous.

- **Non-Branded has not produced one 60s+ call since 09-28**: $1,780 in October, 1 site tap.
- In September, 7 of NB's 10 real calls came from people searching other companies' names (shumate, zone heating, coolray,
  goodman...). Those names were blocked 09-30, and NB calls stopped the same week.
- Branded is the only part that works: October $177 → 2 real calls + 3 Peach AI bookings.

## 2. Why: the auction costs more than we bid

Keyword Planner, Gwinnett County, top-of-page bid range:

| Search | Monthly searches | Top-of-page bid (low–high) |
|---|---|---|
| ac repair | 880 | $36–93 |
| ac repair near me | 590 | $34–111 |
| hvac company near me | 320 | $19–89 |
| hvac contractors near me | 210 | $32–67 |
| hvac repair | 210 | $17–102 |
| heating and air near me | 70 | $50–168 |
| furnace repair / heating repair | 320 / 50 (Nov ~590 / 170) | no bid data (low competition) |

Our cap is $18. Since the 10-23 relaunch NB showed for only 16–29% of eligible searches, and the lost share was mostly
rank (43% → 76%), not budget. The low bid shows up in the search terms: the visible paid terms were gas fireplace repair,
furnace cost questions, mini split install costs, wall units and valve prices. The impression-only terms were model numbers,
error codes and competitor names. Google lets a low bid in where the competition isn't.

The math with no cap: in September we got ~1 real lead per 13 clicks. At a $40 click that is ~$520 per lead. At $28 (what
we paid in September) it is ~$365, and that was with competitor-name searches doing most of the work.

## 3. Why: our ads lose on Quality Score

Quality Score on the live NB keywords is 1–5. The breakdown is the same on almost every keyword:

- **Expected CTR: BELOW AVERAGE on every NB keyword with data.** Searchers pick other ads over ours.
- **Landing page experience: BELOW AVERAGE on most** (`ac repair`, `furnace repair`, `ac service`, `furnace installation`,
  `ac repair near me`...), average on a few.
- Ad relevance: above average. The keywords match the ads, so this is not a structure problem.

Low QS means we need an even higher bid than the table above to get the same spot. Why people skip our ad:

- **Page 1 is crowded.** LSA ads sit on top, then the big local names (Coolray, Estes, Reliable, Peachtree Service Experts)
  with review stars and a lot more brand recognition.
- **No location asset.** The account has sitelinks, callouts, snippets, a call asset and images, but nothing linked to the
  Google Business Profile, so our ad shows no address and no rating.
- **No reason to pick us in the ad.** No price, no special, no review count. Headlines like "Inhale Zen, Exhale Comfort",
  "Stress Free HVAC" and "Your Neighborhood HVAC" use space a competitor fills with "$89 Furnace Repair" or "4.9★ 2,000 reviews".
  Heating ad strength is only AVERAGE.

## 4. Why: the pages don't convert the few clicks we get

GA4, google/cpc, 10-23..10-29:

| Landing page | Sessions | Engaged | Bounce | Avg time |
|---|---|---|---|---|
| /heating-repair-replacement-duluth-ga | 15 | 5 | 67% | 29s |
| /ac-repair-replacement-duluth-ga | 9 | 7 | 22% | 92s |
| /hvac-installation-in-duluth-ga (sitelink) | 5 | 0 | 100% | 0s |
| /hvac-replacement-in-duluth-ga (sitelink) | 4 | 2 | 50% | 22s |

- **0 form submits** from paid traffic on any page. 3 `phone_click` on the heating page, all phone users.
- **Google Ads shows 58 clicks; GA4 sees 37 paid sessions.** About a third of clickers leave before GA4 even loads, or are blocked by consent.
- **Slow first load:** a cold page takes 1.5–2.9s before the server starts sending anything to a phone (WordPress.com cache,
  ~4 min lifetime; on low-traffic pages most ad clicks hit a cold cache). Once warm it's ~0.1s. PageSpeed quota was used up today,
  so no full speed score yet.
- **Sitelinks still go to the old service pages**, which bounce 50–100%.
- Pages load fine for Google's ad crawler (AdsBot = 200). The 403 "Checking search engine crawler" is only for a fake Googlebot from
  our IP, not a real issue.

## 5. Why we can't steer it: the signal is too thin

- NB had 1 counted conversion in 4+ weeks. No bidding strategy can learn from that, and neither can we.
- GA4 shows 3 paid taps on the heating page this week; Google Ads counted 1. Some taps aren't reaching Ads (consent or tag timing).
- Calls to the site's number (Peach AI swaps it for ad visitors) are not "Calls from ads". We only see the tap, not whether
  the call connected or booked. No CallRail on Zen Air.
- Peach AI bookings are the closest thing to an outcome, and they are left out of the goal on purpose (double counting).
- The account was rebuilt or paused about 7 times since July (PMax off 07-31, split 08-03, Display fix 08-24, cap 09-30,
  pause 10-08, relaunch 10-23, paused 10-29). It never had a stable 30 days to learn.

## 6. Smaller factors

- **Small area:** 5 × 7-mile circles around Duluth/Suwanee/Johns Creek/Lawrenceville/Cumming, a part of the county volume above.
- **Season:** late Oct is the shoulder between AC and heating. Furnace searches roughly double in November, so volume will rise,
  but CPCs will too.
- **LSA covers the same searchers first,** and it is cheaper per booked job (~$28 vs ~$400+). LSA's limit is not budget
  (area of 15 cities, Sunday off, ranking; see `2026-10-14-lsa-review.md`).

## What this means

Another keyword or bid tweak won't fix NB. The gap is too big: we'd need to pay ~2–3× our cap AND get click-to-lead rates well
above what these pages have ever done. Options, in the order I'd pick them:

1. **Keep PPC = Branded only for now** (~$50/day; the one part that works), and put the effort into LSA reach: add the missing cities/ZIPs,
   Sunday hours if they answer, more reviews and fast lead responses for ranking. This is a budget shift and needs the AM ticket.
2. **If the client wants NB, run it as a real 30-day test, not a tweak:** heating only (season), exact match on the 5–6 highest-intent
   terms ("furnace repair", "heating repair near me", "furnace repair near me", "no heat"), cap ~$40–45, business hours only,
   location asset linked to the GBP, an offer in the ads (diagnostic price or special), CallRail or Peach call outcomes
   wired in, and the LP fixes below. Set the bar up front: < ~$250 per booked job or it stops.
3. **Fix the pages either way** (they also serve Branded and Meta): form and tap-to-call above the fold on phones, reviews/stars and
   an offer near the top, warm the cache or longer cache lifetime, and point the sitelinks at the new pages.

Open questions for the client (via Andrea): which of the 32 calls booked; whether Peach AI can send call outcomes for
ad visitors; what a booked job is worth to them (sets the real CPL ceiling).

Scripts (scratchpad, not kept): Google Ads pulls `diag1.py` / `diag2.py`, GA4 `ga4_lp.py`, Keyword Planner `historical-metrics`
on geo 9057375.
