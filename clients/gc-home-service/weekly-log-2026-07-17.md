# GC Home Service — Internal Optimization Log
## Week ending Friday 2026-07-17

**INTERNAL ONLY. Not client-facing.** Honest root cause lives here. The client version gets the
sanitized framing per `topserv-client-report-format` — but see "Claims we must not make" first,
because two of the obvious talking points are false and the client's own data would contradict them.

Data pulled 2026-07-17. Google Ads `2375064049`, Meta `1434273655098937`.
Google's newest complete day is **2026-07-16** — this week's Google numbers cannot include today.

---

## 1. Headline numbers

| | Spend | Leads / Conv | Cost per |
|---|---|---|---|
| **Google** (Jul 10–16) | $586.36 | 2 conv | **$293.18** |
| **Meta** (Jul 10–17, lead campaigns) | $1,500.00 | 11 leads | **$136.36** |
| Meta awareness (paused Jul 15) | $165.14 | 310 ad recall lift | $0.53 |
| **Combined** | **$2,251.50** | 13 | — |

Google: 25 clicks total. Conversions came from `Calls from ads` (3) and `[TSD] Website Call Link`
(1) across the last 14 days. Google CPL is high and the click volume is very thin.

---

## 2. What changed — Google (`2375064049`)

**Jul 13 — Edu (39 changes)**
- Rebuilt `TSD_PMAX_Calls` location criteria: 88 location targets created, 5 removed.
  PMax now carries **59 positive locations**, 0 negative.
- Set EU political advertising flag (housekeeping, not performance).

**Jul 16 ~01:30–01:44 account time — Andrea (156 changes)**

| Campaign | Budget | Change |
|---|---|---|
| `TSD_PMAX_Calls` | $50 → $135 → $155/day | Two steps, five minutes apart |
| `TSD_07.05_Search_Nonbranded_Cooling` | $60 → $85 → $110/day | Also **re-enabled** (PAUSED → ENABLED) |
| `TSD_Leads_Search_Branded_08.06` | $80 → **$30/day** | Cut |

- **`Cooling` geo setting: `PRESENCE_OR_INTEREST` → `PRESENCE`.** This is the real root-cause fix.
  "Presence or interest" is what served ads to someone in Makkah searching *about* Cincinnati.
  All three enabled campaigns now read `PRESENCE`. Only the long-`REMOVED` "Q1 2026 Search Ad"
  still carries `PRESENCE_OR_INTEREST`, which is harmless.
- **35 negative keywords added.**
  - Junk/intent: `diy`, `do it yourself`, `jobs`, `hiring`, `careers`, `salary`, `training`,
    `course`, `apprentice`, `used`, `rental`, `wholesale`, `supplier`, `for sale`, `amazon`,
    `home depot`, `lowes`, `reddit`, `youtube`
  - Competitors (phrase): `schneller`, `arlinghaus`, `apollo heating`, `apollo home`,
    `logan services`, `logan hvac`, `logan heating`, `knochelmann`
  - Competitor negatives applied to both `Cooling` and `Branded_08.06`.
- Assets: 14 new sitelink/callout assets created, 28 campaign-asset links created, 17 removed.

**Account structure now:** 12 campaigns, 3 enabled (`PMax_Calls`, `Cooling`, `Branded_08.06`),
8 paused, 1 removed. Consolidation is real — the June-era nonbranded and competitor campaigns
(`TSD_Search_Nonbranded_Competitorsattack_08Jun2026`, `TSD_Leads_Search_Nonbranded_07Jun2026`,
`TSD_03.04_Search_NonBranded_Calls`) are all paused.

---

## 3. What changed — Meta (`1434273655098937`)

202 events since Jul 10. 181 of them on **Jul 15**. Actors: "Claude ia" (103), Manuel
Lizarralde (57), Meta system (39), João Pedro Ventura (3).

**Jul 15 — new retargeting stack**
- Paused `TSD_2026-01_TOF_AWARENESS_CBO_Evergreen - Ad Recall Lift` (4:24 PM).
- `CBO | NEW CREATIVES | 8 JUL` daily budget **$150 → $135** (4:25 PM).
- **Created `BOF | RETARGETING | Warm Audiences`** ($30/day, 4:39 PM). Activated by Manuel 5:32 PM.
- **7 custom audiences created**: `RTG | Website Visitors 180d`, `RTG | IG Engagers 365d`,
  `RTG | FB Page Engagers 365d`, plus 4 lookalikes (US 1% and US broad off the RTG seeds).
- New ad set `BOF | Warm | All Engagers` — optimization goal Conversion leads, auto bid,
  Advantage+ audience On.
- **9 new ads created**: `Beat the Heat`, `New System 2,500 Off`, `Quote Back 1,500`,
  `Quote back 1,500 v2`, `BOF | New System 2,500 + Financing`, `BOF | Quote Back 1,500`,
  `BOF | New System 2,500 Off`, `BOF | Free Diagnostic`, `BOF | 99 Tune-Up`, `BOF | Beat the Heat`.
- **Added metro exclusions** to `BROAD | +18 | M+F` and `BOF | Warm | All Engagers` (5:56–5:57 PM):
  `Exclude: Lexington (+20 mi), Louisville (+25 mi) KY; Columbus (+30 mi), Dayton (+20 mi) OH`.

**Meta performance, Jul 10–17**

| Campaign | Status | Budget | Spend | Impr | Clicks | CPC | CTR | Leads | CPL |
|---|---|---|---|---|---|---|---|---|---|
| `CBO \| NEW CREATIVES \| 8 JUL` | ACTIVE | $135/d | $1,073.66 | 26,956 | 237 | $4.53 | 0.88% | **11** | **$97.61** |
| `TSD_05.14_TOF_ABO_Evergreen` | ACTIVE | $50/d | $375.36 | 8,719 | 75 | $5.00 | 0.86% | **0** | — |
| `BOF \| RETARGETING \| Warm Audiences` | ACTIVE | $30/d | $50.98 | 1,288 | 7 | $7.28 | 0.54% | 0 | — |
| `TSD_2026-01_TOF_AWARENESS - Ad Recall Lift` | PAUSED Jul 15 | $30/d | $165.14 | 39,626 | 54 | $3.06 | 0.14% | 310 ARL | $0.53 |

---

## 4. Lead quality review

### Meta — City + ZIP is a LEAD FORM change, not targeting

Two forms are running:
- `GC Home Service – AC` (`1517970123189977`) — name, phone, email, service, timing. **12 leads**
  in the Jun 30–Jul 11 export.
- `GC Home Service – AC [City & ZIP]` (`1762410775201022`) — same fields **plus `city` and
  `zip_code`**. **1 lead.**

**The one lead the City & ZIP form captured was from Louisville, ZIP 40216 — out of service area.**
(2026-07-08, `ac_replacement`, `as_soon_as_possible`, via `TSD_05.14_TOF_ABO_Evergreen` / ad
"AC Summer".) Louisville is ~90 mi from Cincinnati.

This is the honest, genuinely good story of the week and it's a clean closed loop:
**instrument → detect → act.** We added City + ZIP capture, it immediately caught an out-of-area
lead from Louisville, and on Jul 15 we added a Louisville exclusion (plus Lexington, Columbus,
Dayton) to the live ad sets. That is a real, data-backed optimization we can show.

### Lead quality across the 20 exported leads (Jun 30 – Jul 11)

- Intent: `as_soon_as_possible` 12 (60%), `just_getting_a_quote` 6 (30%), `within_this_week` 2 (10%).
  **30% are self-declared tire-kickers.**
- Service: `ac_replacement` 5, `ac_tune-up` 4, `ac_repair` 4, **`other` 5 (25%)** — vague.
- Ads: `AC Summer` 13, `SEO 3 4:5 / 9:16` 7 (6 of its 7 = `just_getting_a_quote` or `other` —
  **worst-quality ad in the set**), `Welcome video` 1.
- **All 20 came from `TSD_05.14_TOF_ABO_Evergreen`** — the campaign that produced **0 leads on
  $375.36 this week.**
- Only 1 of 20 has city/zip, because the new form is barely deployed. **Coverage is the gap.**

### Google

Conversions are call-heavy (`Calls from ads`, `[TSD] Website Call Link`). The 14-day window shows
no `Repeat Phone Call`, but the Jun 1 – Jul 11 baseline had **4 `Repeat Phone Call`** conversions —
existing customers calling back, counted as new demand. Worth keeping an eye on.

Search terms this week are almost entirely branded: `gc home service` ($101.05, 12 clicks, 1 conv)
and `gc hvac` ($19.41, 2 clicks). We are largely paying for our own name.

---

## 5. Claims we must not make

**1. "Our geo refinements eliminated out-of-area traffic." FALSE.**
The last out-of-area click on Google was **2026-06-16** — a month before the Jul 13 geo work.
All 22 out-of-area clicks ($317: Andalusia/Opp/Florala/Theodore AL, Canton Township MI, Makkah SA,
Owensboro KY, Indianapolis, Williamsburg KY) came from campaigns paused back in June. The client
can pull this themselves.

*Honest framing that is still strong:* `Cooling` was one of the campaigns that historically leaked
(Indianapolis, Theodore AL, Canton Township MI, Makkah). Before putting it back live at $110/day
we diagnosed and corrected the root cause — `PRESENCE_OR_INTEREST` → `PRESENCE` — so the leak
cannot recur. Prevention before relaunch, not cleanup.

**2. "Meta service area is now restricted to the city + ZIP list." FALSE.**
As of Jul 15 5:57 PM the live Meta targeting on **both** serving ad sets is still a dropped pin:
- `BROAD | +18 | M+F` → `2001 Monmouth St, Newport (+40 km) Kentucky`
- `BOF | Warm | All Engagers` → `Latitude 39.08 Longitude -84.48 Newport (+40 km) Kentucky`

That is **Manuel's Jul 8 Power Editor overwrite, still in place**. The city list Edu adjudicated
by hand on Jul 13 **did not stick**. What actually shipped on Jul 15 was a *radius + metro
exclusions* approach, which is a different (and weaker) strategy than the city/ZIP list we told
the client we'd implement.

A +40 km radius from Newport still overshoots Hamilton / Mason / Lebanon, and still *undershoots*
Ghent, Sparta, Glencoe, Falmouth, Dry Ridge and Vevay IN — all on the client's list. The exclusions
only patch the four biggest metros.

**This is the single biggest gap between what was promised and what is live.** It needs a decision
before Friday's send, not a sentence that papers over it.

---

## 6. Open items / risks

1. **`Cooling` has zero impressions since re-enabling.** Reads `SERVING` / `LEARNING`
   (`BIDDING_STRATEGY_LEARNING`), 3 ad groups `ELIGIBLE`, 3 ads `APPROVED`, 109 keywords,
   $110/day — and **0 impressions, $0 spend** on its first full day (Jul 16). Probably Maximize
   Conversions in learning with no conversion history. **If it's still dark Jul 18, escalate.**
   Do not promise the client Cooling results yet.
2. **`Cooling` is 109 keywords, heavily BROAD, on Maximize Conversions.** Broad + a thin conversion
   signal is exactly how the June junk traffic happened. This is the lead-quality risk to watch now.
3. **`TSD_05.14_TOF_ABO_Evergreen`: $375.36, 0 leads this week** after producing all 20 leads in the
   prior window. Either kill it or find out what broke.
4. **`BOF | RETARGETING`: $50.98, 0 leads, $7.28 CPC, 0.54% CTR** — 2 days old, too early to judge,
   but the CTR is the worst in the account.
5. **OTP phone verification: no evidence found.** Not in the Meta activity log, not a field on
   either lead form. If it's a form setting it won't show in the log — **Edu must confirm status
   before it goes in the report.** Cannot write this section from data.
6. **Google account timezone `Africa/Kampala`** (see README).
7. **The two service-area lists still don't match** (see README).
8. **"Amelia, KY" and "Williamsburg, KY"** still unresolved — twice escalated, never answered.

---

## 7. Proposed next steps (for the Next Steps section)

- Decide the Meta geo approach: implement the actual city/ZIP list, or formally re-scope to
  radius + exclusions and tell the client that's what we're doing. **Do not leave this implicit.**
- Roll the `[City & ZIP]` form out to **all** lead ads — 1 of 20 leads carrying city/zip is not
  enough coverage to run a lead-quality review on. This is the highest-leverage change available.
- Watch `Cooling` delivery daily; if still zero, check bid strategy and conversion signal.
- Watch the Jul 16 Google budget increases (PMax $50 → $155 is a 3x jump — CPL was already $293).
- Kill or fix `TSD_05.14_TOF_ABO_Evergreen`.
- Pause or rework the `SEO 3 4:5 / 9:16` ad — 6 of its 7 leads were low intent.
- Get an answer on Amelia KY / Williamsburg KY.

---

## 8. Blockers

- **The *July Campaign Management, Budget Allocation & Lead Quality Review* document has never
  been provided.** It defines the report structure and the exact commitments this update is
  supposed to honor. Everything above is reconstructed from account data.
- **OTP phone verification status unknown** (item 5).
