# Gillespie's Heating and Cooling: Meta ads snapshot (2026-09-26)

Internal reference. Copy below is verbatim from the live creatives, pulled via the Ads MCP (`ads_get_creatives`, `ads_get_ad_entities`). Nothing on the account was changed to produce this.

- **Ad account:** `2014320269203822` (Gillespie's own business `1728244028382959`, TSD-managed), USD
- **Page:** `547202205134211` Gillespie's Heating and Cooling
- **Lifetime metrics window:** `maximum` (account life through 2026-09-26)

**Not exposed by the API, so not captured here:** the link description line, the Instant Form ID/questions, the destination URL (the lead ads are on-Meta forms, `destination_type = ON_AD`), and any Advantage+ creative enhancement toggles. Pull these from Ads Manager if the rebuild needs them.

**Ad-to-creative mapping** was matched by ad/creative name (including the Jul/Aug suffix), not by `ads_get_creative_ads`.

---

## 1. Account state at snapshot

| Campaign | ID | Objective | Status | Budget | Bid strategy | Lifetime |
|---|---|---|---|---|---|---|
| `TSD_2026-08_TOF_AWARENESS_CBO_Evergreen - Ad Recall Lift` | `7000989212234` | OUTCOME_AWARENESS | ACTIVE | $40/day, campaign level (CBO) | Highest volume | $594.54, 126,109 impr, 617 clicks, 1,450 est. ad recallers ($0.41 each) |
| `Lead Gen \| HVAC \| NKY & Cincinnati \| Jul 2026` | `6992159403634` | OUTCOME_LEADS | PAUSED (since ~09-09) | $50/day at **ad set** level (ABO) | Highest volume | $2,024.13, 80,903 impr, 1,330 clicks, 27 leads, $74.97 CPL |

| Ad set | ID | Campaign | Optimization | Destination |
|---|---|---|---|---|
| `08/24/2026 - ZIP Codes \| Broad` | `7000989216434` | Awareness | AD_RECALL_LIFT | none |
| `NKY & Cincinnati \| 30+ \| Instant Form \| $50/day` | `6992159408234` | Lead Gen | LEAD_GENERATION | ON_AD (Instant Form) |

**Tracking on the account:** zero datasets/pixels (`ads_get_datasets` returns empty), zero custom conversions. `promoted_object.pixel_id` is null on both ad sets. The Meta Pixel ID in the site's GTM container is still filler (see `gtm-log.md`). Lead ad set was never pixel-optimized.

**Page lead-gen ToS:** `ads_get_ad_account_pages` reports `leadgen_tos_accepted: false` for the Page, even though lead ads have been running. Check this before building any new LEAD_GENERATION ad set.

## 2. Targeting (identical on both ad sets)

- Ages 30 to 65, **Advantage+ Audience off** (`advantage_audience: 0`, so the age range is a hard cap)
- Location type: people living in ("home")
- Placements: Advantage+ (automatic)
- No interests or behaviors
- 32 ZIP codes:
  - **KY (14):** 41001, 41002, 41004, 41006, 41007, 41017, 41018, 41040, 41042, 41051, 41056, 41075, 41076, 41091
  - **OH (18):** 45101, 45118, 45121, 45130, 45144, 45154, 45167, 45168, 45171, 45176, 45616, 45650, 45657, 45660, 45679, 45684, 45693, 45697

---

## 3. Awareness campaign: 4 video ads (all ACTIVE)

All four: CTA `LEARN_MORE`, object type VIDEO.

### Video 01 - What to Expect
- Ad `7000989420834` · Creative `3598361010319985` · Video `2217014302196184` · Post `547202205134211_122167093772695083`
- **Headline:** What to Expect from Gillespie's
- **Primary text:**
```
Wondering what happens when you call Gillespie's Heating and Cooling? 👋

We walk you through it step by step — from the first call to the finished job.

Family-owned in Brooksville, KY and serving Northern Kentucky and Greater Cincinnati.
```
- Lifetime: $30.17, 6,766 impr, 170 est. recallers

### Video 02 - Testimonial Liz Dykes
- Ad `7000989462434` · Creative `1592892819042360` · Video `2130416247866031` · Post `547202205134211_122167093796695083`
- **Headline:** Why Neighbors Choose Gillespie's
- **Primary text:**
```
Hear from Liz, one of our Northern Kentucky neighbors, about her experience with Gillespie's Heating and Cooling. 🏡

Family-owned, licensed and insured in KY and OH.
```
- Lifetime: $24.02, 5,090 impr, 150 est. recallers

### Video 03 - Testimonial Ken Perry
- Ad `7000989535634` · Creative `1067227182861800` · Video `2127994665260862` · Post `547202205134211_122167093814695083`
- **Headline:** A Local Customer's Experience
- **Primary text:**
```
Ken called Gillespie's Heating and Cooling — here's how it went. 🔧

Honest work from a family-owned team serving Northern Kentucky and Greater Cincinnati.
```
- Lifetime: $485.43, 102,345 impr, 1,270 est. recallers (82% of campaign spend)

### Video 04 - Testimonial TJ Burton
- Ad `7000989607234` · Creative `2987788484899408` · Video `1043881185051295` · Post `547202205134211_122167093856695083`
- **Headline:** Real Customers, Real Comfort
- **Primary text:**
```
TJ shares his experience with Gillespie's Heating and Cooling. 🧰

Locally owned in Brooksville, KY, licensed and insured in KY and OH, and proud to serve our Northern Kentucky and Greater Cincinnati neighbors.
```
- Lifetime: $54.92, 11,908 impr, 270 est. recallers

---

## 4. Lead Gen campaign: Aug 2026 creative set (6 ads, created 08-24)

All: object type SHARE (static image), CTA `GET_QUOTE`. Ad status ACTIVE except where noted, but the parent campaign is PAUSED so none deliver.

### Heat Pump & Mini-Split | Aug 2026
- Ad `7000987766834` · Creative `2186219518591656` · Image hash `8a765c72571c3d5143584bfea572e7bb` · Post `547202205134211_122167092578695083`
- **Headline:** One System. Both Seasons.
- **Primary text:**
```
Northern Kentucky weather swings hard — freezing mornings, sweltering afternoons. ❄️☀️ A heat pump or ductless mini-split gives you efficient heating AND cooling from a single system, and Gillespie's Heating and Cooling installs the setup that handles both.

✅ Free estimate
✅ Financing available
✅ NATE-certified & licensed in KY & OH

👉 Request your free estimate below.
```
- Lifetime: $624.69, 27,478 impr, **13 leads**

### Top Notch Value | Aug 2026
- Ad `7000987803634` · Creative `1381178853469421` · Image hash `ac22abab78a318212fc48b4a1f28e0bf` · Post `547202205134211_122167092626695083`
- **Headline:** Top Notch Work. Top Notch Price.
- **Primary text:**
```
Big-name HVAC quality without the big-name markup. 🛠️ Gillespie's Heating and Cooling brings NATE-certified workmanship and honest, upfront pricing to homeowners across Northern Kentucky & Greater Cincinnati.

✅ Licensed in KY & OH
✅ NATE-certified
⭐ 5.0 on Google

👉 Get your free estimate below.
```
- Lifetime: $3.89, 209 impr, 0 leads

### Repair vs Replace | Aug 2026
- Ad `7000987842234` · Creative `1048701564663970` · Image hash `7d5946db4a591ee35250dc1642453353` · Post `547202205134211_122167092692695083`
- **Headline:** Broken? Or Just Dirty?
- **Primary text:**
```
Before you spend money replacing your AC — is it actually broken, or just dirty? 🤔 A quick, honest check from Gillespie's Heating and Cooling could save you a full repair or replacement bill. No pressure, no guesswork.

✅ Free estimate
✅ Honest, upfront recommendations
✅ Family-owned & 5.0 on Google

👉 Book your free estimate below.
```
- Lifetime: $15.02, 700 impr, 0 leads

### Seasonal Tune-Up | Aug 2026
- Ad `7000987720034` · Creative `3938001576495400` · Image hash `14776b71feebecc6c9a81438a000d46e` · Post `547202205134211_122167092494695083`
- **Headline:** Don't Wait for the Breakdown
- **Primary text:**
```
Your AC always seems to quit on the hottest day of the year. 🔧 Get ahead of it with a seasonal tune-up from Gillespie's Heating and Cooling — Northern Kentucky & Greater Cincinnati's NATE-certified, family-owned HVAC team. Catch the small stuff before it becomes an expensive breakdown.

✅ Free estimate
✅ NATE-certified technicians
✅ Licensed in KY & OH

👉 Request your free estimate below.
```
- Lifetime: $15.26, 620 impr, 0 leads

### 2nd Opinion Testimonial | Aug 2026
- Ad `7000987740834` · Creative `1784238102571782` · Image hash `01de72a1cae85429c9580aa3378d81ec` · Post `547202205134211_122167092512695083`
- **Headline:** Get an Honest Second Opinion
- **Primary text:**
```
Before you say yes to a big repair bill, get a second opinion. 💬 One local homeowner was quoted $4,000 elsewhere — then called Gillespie's Heating and Cooling for an honest look. Fair, straightforward, and back up and running fast.

⭐ 5.0 on Google
✅ Free estimate
✅ Family-owned & trusted

👉 Get your free estimate below.
```
- Lifetime: $72.49, 3,787 impr, 1 lead

### Heating Season Prep | Aug 2026 (ad status PAUSED)
- Ad `7000987877234` · Creative `1604050597758682` · Image hash `6b3ca01ee065ed54bd188e4c8f98cc59` · Post `547202205134211_122167092728695083`
- **Headline:** Get Ahead of Heating Season
- **Primary text:**
```
The first cold night always shows up before you're ready. 🍂 A pre-season heating check from Gillespie's Heating and Cooling catches the small stuff now — so you're not calling for heat on the coldest morning of the year.

✅ Free estimate
✅ NATE-certified technicians
✅ Licensed in KY & OH
✅ Financing available

👉 Book your free estimate below.
```
- Lifetime: $55.62, 4,444 impr, 0 leads reported

---

## 5. Lead Gen campaign: Jul 2026 creative set (5 ads, created 07-30, all ad status PAUSED)

Same headlines and CTA (`GET_QUOTE`) as the Aug versions. Primary text is **identical to Aug** except the Heat Pump ad (see section 6).

| Ad | Ad ID | Creative ID | Image hash | Post ID | Lifetime |
|---|---|---|---|---|---|
| Heat Pump & Mini-Split \| Jul 2026 | `6992159425434` | `4643294095892245` | `f0206c8ead4291f037537964652f2d9e` | `547202205134211_122165384150695083` | $656.53, 21,655 impr, 6 leads |
| Top Notch Value \| Jul 2026 | `6992159436434` | `1583878479958538` | `e85bc2270c432c1f6ac5b778a4b0cb47` | `547202205134211_122165384186695083` | $107.44, 3,480 impr, 2 leads |
| Repair vs Replace \| Jul 2026 | `6992159448034` | `2844549025912700` | `beefa0bfc6c7efda5e7148dc35069321` | `547202205134211_122165384354695083` | $86.13, 3,143 impr, 1 lead |
| Seasonal Tune-Up \| Jul 2026 | `6992159414434` | `1578723263883737` | `bf1f014e283decffc97ea77d3bc1b799` | `547202205134211_122165384072695083` | $101.15, 3,825 impr, 2 leads |
| 2nd Opinion Testimonial \| Jul 2026 | `6992159418634` | `2247721989347144` | `7310e4f4d9e484f3d5941235ef4c6107` | `547202205134211_122165384108695083` | $285.91, 11,562 impr, 2 leads |

Heat Pump & Mini-Split | Jul 2026, the one text that differs (headline "One System. Both Seasons."):
```
Northern Kentucky weather swings hard — freezing mornings, sweltering afternoons. ❄️☀️ A heat pump or ductless mini-split gives you efficient heating AND cooling from a single system, and Gillespie's Heating and Cooling installs the setup that handles both.

✅ Free estimate
✅ Financing available
✅ Day & Night Elite Dealer

👉 Request your free estimate below.
```

---

## 6. Things to know before reusing any of this

1. **Jul vs Aug copy differs in one line.** On the Heat Pump ad, "✅ Day & Night Elite Dealer" (Jul) became "✅ NATE-certified & licensed in KY & OH" (Aug). Reason not logged. Confirm the dealer claim against the client's site before it goes back in anywhere.
2. **Claims that appear across the set and should be re-verified against the live site/Google profile before a rebuild:** "5.0 on Google", "NATE-certified", "Financing available", "Free estimate", "Licensed in KY & OH", and the "$4,000 quote" story in the 2nd Opinion ad.
3. **Aug is the freshest set** (created 08-24). Jul creatives are the earlier versions of the same five ads.
4. **Performance by angle, lifetime lead gen (27 leads, $2,024.13):**
   - Heat Pump & Mini-Split, Jul + Aug combined: $1,281.22, **19 leads, $67.43 per lead** (70% of all leads, 63% of spend). Aug version alone: 13 leads at $48.05. Jul version alone: 6 leads at $109.42.
   - Everything else combined (Top Notch, Repair vs Replace, Seasonal, 2nd Opinion, Heating Season Prep): $742.91, 8 leads, $92.86 per lead.
   - Aug Top Notch, Seasonal and Repair vs Replace barely spent ($3.89, $15.26, $15.02) because the algorithm favored Heat Pump.
5. **Existing structure differs from the Meta doctrine** ([[tsd-meta-ads-methodology]]): Lead Gen was ABO ($50/day on the ad set), one ad set carrying all angles, Advantage+ Audience off with a hard 30 to 65 age cap and ZIP-list geo. Awareness was CBO.
6. **Existing copy contains em dashes** in most primary texts. Live as-is; flagging in case the rebuild should follow the client-facing voice rule.
