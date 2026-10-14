# All Heart Heating & Cooling — Google Ads Log

**Client:** All Heart Heating & Cooling (HVAC + Plumbing — Kern County / Lancaster / Antelope Valley, CA)
**Account:** All Heart Heating & Cooling -PPC — Customer ID `9205826499` (under MCC Topservdigital `4155514468`)
**Platform:** Google Ads

> Running log of paid-search work on this account. Newest entry on top. One entry per work session: what we looked at, what we found, what we changed, and what's still open. Meta Ads work lives in `meta-ads-log.md` in this same folder.

---

## ⚡ Quick access (read this first — don't re-discover the account)

- **Customer ID (no hyphens):** `9205826499`
- **MCC / login-customer-id:** `4155514468` (Topservdigital)
- **Skill:** `google-ads-ratos` — scripts at `~/.claude/skills/google-ads-ratos/scripts/`
- **Interpreter on this machine:** `python` (NOT `python3` — that alias isn't installed)

**Ready-to-run commands** (from `~/.claude/skills/google-ads-ratos/`):
```bash
python scripts/read.py campaigns   --customer-id 9205826499
python scripts/read.py keywords    --customer-id 9205826499 --campaign-id 23685938569
python scripts/read.py search-terms --customer-id 9205826499        # not campaign-filterable; filter by GAQL
python scripts/insights.py campaign --customer-id 9205826499 --date-range LAST_30_DAYS
python scripts/read.py negative-keywords --customer-id 9205826499
```

**Key campaign IDs:**
| Campaign | ID | Status |
|---|---|---|
| TSD_03.22_Search_NonBranded_Evergreen (the active Search non-branded) | `23685938569` | ENABLED |
| TSD_04.20_Calls_Pmax_Evergreen | `23800161039` | ENABLED |
| LocalServicesCampaign (LSA, system-gen) | `20996165007` | ENABLED |
| TSD_07.10_Search_Branded_Evergreen (staged, Phase 2) | `24016694610` | PAUSED |
| ⚠️ "HVAC (Lead Gen Unbranded) PHR Trial 317" — **ENABLED w/ $300/day budget**, only inert because `serving_status = ENDED` | `20250049817` | ENABLED/ENDED |

⚠️ **`20250049817` is a loaded gun.** Status ENABLED, budget `9963417338` = $300/day, zero spend ONLY because its serving status is ENDED (past end date). One date edit and it outspends everything else on the account combined. Pause it when convenient (not yet done as of 07-11).

**Account facts worth not re-discovering:**
- **Account timezone: `America/Los_Angeles`.** All `change_event` / `segments.hour` timestamps are PT. Edu's Mac is BRT (PT+4) — always reconcile before concluding "this happened after I closed."
- **No ad schedule and no bid modifiers exist** anywhere on the live campaigns (ad-schedule / device / location criteria all present but `bid_modifier = None`). Campaigns run 24/7 at full bid. Note Search is Maximize Conversions → **smart bidding ignores ad-schedule bid modifiers anyway**; the only working weekend lever is an ad-schedule *restriction*.
- **Primary conversion = "Calls from ads"** (48 primary / 30d). Everything else (page_view 843, Local actions, Clicks to call) is secondary/all-conversions noise. Call conversions carry a real reporting lag → same-day conversion data is structurally understated.
- 🔴 **THE ONE FACT THAT GOVERNS THIS ACCOUNT: the "NonBranded" Search campaign is ~86% brand-powered, and its actual non-brand half is dead.** 30d to 07-11: brand = 18 conv @ **$26.86** CPL; non-brand = 3 conv @ **$103.13** CPL (5.2% CVR). The campaign *blends* to $37.76, which is a lie. **Never quote the campaign's blended CPL** — to anyone, internally or to the client. Always split brand/non-brand before reading this campaign. Non-brand trend: Apr $25.50 → May $33.68 → Jun $50.23 → **Jul 1–11: ZERO conversions on $147**.
- **PMax `23800161039` — not Search — is the account's real non-brand lead engine.** ~$35 CPL, ~8 conv/wk, zero brand categories in its search-term insight. It was the genuinely budget-starved campaign. Search is the broken one.

**GAQL gotchas:** `LAST_90_DAYS` is NOT a valid date literal — use `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`. `search_term_view` has no campaign-id flag in the skill script → write a custom query filtered by `campaign.id = 23685938569`. `change_status` **requires a bounded range on both ends** (`>=` AND `<=`) or it throws `CHANGE_DATE_RANGE_INFINITE`. `campaign.start_date` / `campaign.end_date` are **not selectable** in this API version. **Impression-share metrics are NOT compatible with `segments.hour`** — IS is daily-only.

---

## 2026-09-29 — Offboarded, but 4 LSA accounts still spending under the MCC (read-only, NO changes)

**Found** (during the Growth Engine pull, `paid/relatorios/growth-engine-pull-2026-09/`): All Heart is
offboarded. Its Meta campaigns were paused 2026-08-20, and this PPC account (`9205826499`) had no spend
in the last 4 weeks (08-31 → 09-27). But four separate All Heart LSA accounts under the Topservdigital MCC are still
spending (all `LOCAL_SERVICES`, last spend in the week of 2026-09-21):

| Account | Customer ID | Weeks from 2026-08-17 | Last 4 weeks (08-31 → 09-27) |
|---|---|---|---|
| [Lancaster HVAC] | `9976029542` | $18,037.95 | $9,801.02 |
| [Lancaster Plumbing] | `8199337860` | $6,524.97 | $5,027.02 |
| [Kern County HVAC] | `5064174352` | $2,025.25 | $1,058.34 |
| [Kern County Plumbing] | `7662998005` | $2,118.89 | $1,695.74 |
| **Total** | | **$28,707.06** | **$17,582.12** |

**Did:** nothing on the accounts. They're marked `offboarded` in the Growth Engine `client_roster.csv`
and kept out of its headline numbers.

**Open:** confirm who manages and pays for these LSA accounts now, and whether they should be unlinked
from the TSD MCC.

---

## 2026-07-12 — Ramp read #2: the ramp is a MIRAGE. Non-brand Search is dead. (NO changes executed)

**Trigger:** Edu asked for a check. Sunday, so today is 8h old and useless — the real subject is **Saturday 07-11, the first FULL post-change day**, now closed.

### Headline: 07-11 looked like a triumph. It was 100% brand.
Search NonBranded on 07-11: 123 imp · 10 clicks · **$44.04 · 5 conversions · CPL $8.81** — against a 60-day history where *every* Saturday produced 0–1 conversions. On its face, the best Saturday the account has ever had, and apparent proof the tCPA fix worked.

**It isn't.** Pulled the converting search terms for 07-09 → 07-11:

| Term | Type | Clicks | Cost | Conv | CPL |
|---|---|---|---|---|---|
| `all heart heating and cooling` | **BRAND** | 8 | $34.55 | 4.0 | $8.64 |
| `all heart` | **BRAND** | 4 | $8.92 | 2.0 | $4.46 |
| *(everything non-brand)* | non-brand | ~15 | **$29.45** | **0.0** | — |

**Brand = 100% of conversions on 61% of spend. Non-brand spent $29 and returned nothing.** The $8.81 "Saturday CPL" is the cost of buying our own name.

### The real finding: non-brand hasn't just underperformed — it has flatlined, and it's been dying for 3 months
Brand/non-brand split of the *same campaign* by window:

| Window | NB clicks | NB spend | NB conv | **NB CPL** | NB CVR | Brand conv | Brand CPL |
|---|---|---|---|---|---|---|---|
| Apr (04-03→04-30) | 77 | $305.95 | 12.0 | $25.50 | 15.6% | 11.5 | $28.12 |
| May | 92 | $572.63 | 17.0 | $33.68 | 18.5% | 29.0 | $17.38 |
| Jun | 59 | $301.41 | 6.0 | $50.23 | 10.2% | 21.0 | $24.29 |
| Jul 1–9 (pre-change) | 21 | $129.22 | **0.0** | **NO CONV** | 0.0% | 0.0 | — |
| Jul 10–11 (post-change) | 6 | $18.10 | **0.0** | **NO CONV** | 0.0% | 6.0 | $5.60 |

**Non-brand CPL doubled Apr→Jun and then went to zero conversions across 11 straight days and $147 of spend — in the middle of peak HVAC season, when demand should be at its highest.** CVR fell 15.6% → 18.5% → 10.2% → 0%.

30-day rollup (06-12→07-11): brand **18 conv @ $26.86** · non-brand **3 conv @ $103.13**. Blended reads $37.76 and hides all of it.

### Consequences — this reframes the whole account
1. **The 07-10 tCPA raise ($29→$65) did NOT fix non-brand.** It bought more brand clicks (cheap, converting) and more *expensive* non-brand clicks (still converting at zero). It was aimed at rank-loss; rank-loss wasn't the binding constraint. IS did improve (21.1% → 32.7%, rank-lost 78.9% → 67.3%) — the auctions were won, the traffic just doesn't convert.
2. **The Saturday alarm from 07-11 is retired, but not for the reason we thought.** Saturday didn't "come good" — brand converted on Saturday (brand always would), and non-brand did what it does every day now: nothing. **Do NOT build an ad-schedule restriction on the weekend hypothesis.** Weekend isn't the variable. Non-brand is broken all seven days.
3. **PMax is the account's actual non-brand lead engine, and it's working.** 07-05→07-11: ~$279 · 8 conv · **~$35 CPL**, and its search-term insight shows **zero brand categories** — these are genuine non-brand leads. It is now spending its full $100/day (07-11: 769 imp · 16 clicks · $106.84). **The PMax budget raise was the correct call; the Search budget raise remains inert and the Search tCPA raise bought brand.** If anyone asks "what worked," the honest answer is PMax.
4. **Search's $250/day budget is fiction.** Budget-lost IS = 0.0% every single day. The campaign cannot spend it, and we would not want it to at a $103 non-brand CPL.

### Consequence for Phase 2 — still GO, but the rationale has changed and so must the expectation
Phase 2 (brand split + 5 themed ad groups, both built and PAUSED) was staged to "clean up the read." **We no longer need it to clean the read — we already have the read, and it's terrible.** What Phase 2 is now is a **rescue attempt on non-brand**, and it's well-aimed: the themed restructure targets exactly the plausible root cause (single mega ad group blending HVAC + plumbing + brand under one RSA → `plumber near me` at QS 3 → bad ad relevance → clicks that don't call).

**But expect the opposite of a scale-up.** The moment brand is negatived out of NonBranded, that campaign loses 86% of its conversions. Maximize Conversions with a $65 tCPA, bidding against a keyword set whose real CPL is $103, will **throttle itself back down hard** — i.e. it will look like it "stopped working." That is the throttle being *honest* for the first time. It is not a regression and it must not be panic-reverted.

- Brand leads (~18/mo @ ~$27) keep flowing — they just flow through the Branded campaign now.
- Give the themed restructure **2–3 weeks** before judging. A CVR fix takes longer to read than a bid fix.
- **Do not raise any Search budget.** Do not re-raise tCPA to "buy volume" — that is what bought brand.

### Unresolved, and now much more suspicious: the 07-02 tracking flag
The 07-02 audit flagged `allheart heating and cooling` — **brand intent, $97.60, zero conversions** — as a possible tracking / LP / routing bug, and **it was never investigated.** We now have a *total* non-brand conversion flatline sitting next to it. Argument that it's real (not a tracking bug): the primary conversion is "Calls from ads," which Google tracks at the ad level via number-forwarding — a broken landing page or GTM tag cannot suppress it, and **brand kept converting through the same conversion action all July**, so the action itself is alive. So the flatline is most likely genuine: non-brand clicks are landing and not calling. That points at relevance/LP-match, which is what Phase 2 fixes. **Still worth 20 minutes to close out**, because "non-brand doesn't call" and "we're not counting non-brand calls" have opposite fixes.

### State verified this session
- tCPA on `23685938569` confirmed **still $65** — Google did not auto-modify it. Budgets: Search $250/day, PMax $100/day.
- **No user changes on the account since the 07-10 work** (`change_event` clean 07-11 → 07-12). Account untouched.
- ⚠️ **`20250049817` STILL ENABLED** — $300/day, tCPA $73, MAXIMIZE_CONVERSIONS, inert only because `serving_status = ENDED`. Flagged 07-11, still not paused. **Third session running.**

### Open / next (in priority order)
1. **Pause `20250049817`.** Two sessions of "when convenient" is enough. Zero risk, zero spend impact, removes a $300/day accident.
2. **Phase 2 flip — GO, but brief it correctly first.** Gates are technically clear (6 RSAs APPROVED; ramp read done). Do NOT flip until the "NonBranded will go quiet and that's correct" expectation is written down for AM/client, or the first quiet week gets read as failure and reverted.
3. **AM ticket for the 07-10 budget increases — STILL OWED, now 2 days overdue.** MasterOps requires the written client record. This is the one governance item in the red.
4. **Never let the blended CPL reach the client.** If All Heart is told "$8.81 leads on Saturday," we have sold a number that is structurally unrepeatable — it is brand volume, capped by demand, not by bidding.
5. Close out the 07-02 tracking flag (above).
6. Decide on Google auto-asset generation (still silently editing live RSAs).

*Nothing was changed on the account in this session — read only.*

---

## 2026-07-11 — Change-history audit + first post-change read (NO changes executed)

**Trigger:** Edu closed on 07-10 unsure whether the day's work got logged. Audited the account's real change history against this log, then read the ramp.

### Audit result: the 07-10 log is complete and accurate — nothing was missing
Pulled all `change_event` rows for 07-10 → 07-11. **83 events, all between 19:08 and 19:49 PT on 07-10, all by `eduardo@topservdigital.com` via `GOOGLE_ADS_API`.** They map 1:1 onto the three 07-10 entries below:

| What the API shows | Matches log? |
|---|---|
| 2× CAMPAIGN UPDATE — `targetCpaMicros` 29M→50M→65M | ✓ |
| 6× AD_GROUP CREATE (5 themed + brand) | ✓ |
| 59× AD_GROUP_CRITERION CREATE (42 non-brand kws + 17 brand kws) | ✓ |
| 6× AD_GROUP_AD CREATE (the 6 RSAs) | ✓ |
| 1× CAMPAIGN CREATE (`24016694610`, PAUSED) | ✓ |
| 2× CAMPAIGN_BUDGET CREATE + 1× REMOVE (the orphan shared budget `15704720618`) | ✓ |
| 4× CAMPAIGN_CRITERION CREATE (3 proximity + 1 language) | ✓ |
| 2× CAMPAIGN_BUDGET UPDATE (PMax $50→$100; Search $150→$250) | ✓ |

The log file was saved 19:50 PT, one minute after the last mutation. **No unlogged work existed.**

### Google made automated changes overnight (NOT ours)
`change_event` only records *user* changes; `change_status` records system ones too. On **07-11** (00:30, 05:08, 05:57 PT) Google auto-modified PMax assets and **edited the live RSA in the old mega ad group `193307267686`**. That ad is still ENABLED / APPROVED / ad strength EXCELLENT, so no harm — but **Google's auto-asset generation is active and silently editing live ads on this account.** Worth deciding whether to turn that off.

### Finding: the Search budget increase was INERT
`search_budget_lost_impression_share = 0.0%` **every single day** for the last 21 days, while rank-lost ran 63–90%. Search was never budget-constrained (spending $8–40/day against $150). **Raising Search $150 → $250 could not and did not change anything** — it's headroom for later, not a lever. PMax's raise is the real one (it *was* budget-capped at 28% lost-to-budget). **Do not let anyone frame the Search budget bump to the client as the fix.**

### First post-change read (hour-matched, hours 00–13 PT, vs 4-day pre-change avg)
Changes landed 19:08 PT on 07-10, so 07-11 is the first post-change day. Compared like-for-like hours:

| | Search NonBranded | PMax |
|---|---|---|
| Impressions | 76 vs 81 (**−6%**) | 404 vs 163 (**+147%**) |
| Clicks | 4 vs 4 (**−11%**) | 8 vs 3 (**+167%**) |
| Spend | $24.62 vs $9.75 (**+152%**) | $52.79 vs $23.17 (**+128%**) |
| CPC | **$6.16 vs ~$2.65 (~2.3×)** | $6.60 vs ~$7 |
| Conversions | 0 | 0 |

- **Search: the tCPA raise is buying POSITION, not VOLUME.** Top-of-page IS jumped 11.7% → 33.3%, abs-top 10% → 16.7%, but impressions/clicks are flat-to-down while CPC ~2.3×'d. This is the normal day-1 signature (rank first, volume compounds) — **but if CPC stays ~$6–7 with no click growth for 2–3 days, dial tCPA back toward $50–55.**
- **PMax: working as intended.** Genuinely ramping on the budget it was actually starved of.
- **Intraday IS is unreliable** — same-day it read 10%, then 33.3%. Ignore until the day closes.

### Finding: SATURDAY is the account's worst day by far (day-of-week, 60d, NonBranded)
| Day | Clicks | Spend | Conv | CPL | Conv rate |
|---|---|---|---|---|---|
| Mon | 95 | $619.99 | 13.0 | $47.70 | 13.7% |
| Tue | 88 | $397.33 | 17.5 | $22.71 | 19.9% |
| Wed | 108 | $625.35 | 20.2 | $31.01 | 18.7% |
| Thu | 86 | $376.09 | 12.0 | $31.34 | 14.0% |
| Fri | 74 | $441.89 | 14.0 | $31.56 | 18.9% |
| **Sat** | **28** | **$118.98** | **1.0** | **$118.98** | **3.6%** |
| Sun | 16 | $26.94 | 1.0 | $26.94 | 6.2% |

**Saturday converts at 3.6% vs ~17% weekday — 1 conversion across ~9 Saturdays.**
- **This retires the "zero conversions today" alarm.** 07-11 was a Saturday; zero conv on a Saturday is this account's norm, not a tracking failure.
- **But it creates a new risk:** a normal Saturday spends ~$13 on Search. On 07-11 it had already spent **$24.62 by 2pm** — ~2× a full normal Saturday, half a day in. The $65 tCPA has unshackled bidding on the worst-converting day. Smart bidding was previously self-limiting there; it no longer is.
- **Open question for AM/client (ask BEFORE the Phase 2 flip): does All Heart answer phones on weekends?** Primary conv = "Calls from ads." If nobody picks up Saturday, weekend clicks *structurally cannot* convert and the fix is an ad-schedule **restriction** (bid modifiers are ignored under Max Conversions). If they *do* run weekend service, 3.6% is a real performance problem needing its own look.

### Open / next
1. **Monday is the decision point** — first two clean full days with landed call conversions. Re-run the hour-matched pull + `phase2_monitor.py`.
2. **Phase 2 flip: HOLD.** All 6 new RSAs are APPROVED (that gate is cleared), but do not flip until the ramp reads clean and the weekend question is answered.
3. **Pause `20250049817`** (ENABLED + $300/day, ENDED) — safety, not urgent. NOT done yet.
4. **AM ticket still owed** for the 07-10 budget increases — made on Edu's verbal authority ("I have the ok"); MasterOps requires the written client record. **This is the one overdue item.**
5. Decide whether to disable Google auto-asset generation (it's editing live ads).

*Nothing was changed on the account in this session — audit/read only.*

---

## 2026-07-10 — Search ramp: unthrottled the tCPA (the 70% rank-loss fix)

**Trigger:** Client (friends with the boss) pushing hard for faster results, esp. Search.

### Root cause found
Live Search campaign `TSD_03.22_Search_NonBranded_Evergreen` (`23685938569`) was **Maximize Conversions with a hard $29 target CPA**, but actual delivery = **~$43 CPL**. The target was a fiction the algorithm could never hit, so it refused to bid into auctions:
- **Search impression share lost to RANK = 70.4%**, lost to **budget = 0%**.
- Campaign spent only **~$40/day of its $150/day** budget (27%). Not budget-limited — **tCPA-throttled.**
- Diagnostic: 30d = 244 clicks · 27.7 primary conv (Calls from ads) · $1,199 · CPL $43 · IS 29.6%.

### What I changed (executed)
- **Raised `maximize_conversions.target_cpa_micros` $29 → $50 → $65** on `23685938569` via direct CampaignService mutate (skill `update.py` doesn't expose bidding). Confirmed before/after. Final = **$65** per client direction "go all in, but no $300 leads."
- **Why $65 and NOT removing the target:** actual CPL ~$43. A $65 target (≈+124% over the $29 throttle, +50% over achieved) pushes it to grab most of the lost 70% IS and spend the full $150/day, while the target still acts as a guardrail steering *average* CPL well below any runaway number. Removing the target entirely would strip that ceiling — client explicitly wanted a cap. Bounded, reversible. Changing the *target* (not the strategy type) does **not** reset learning.
- **Not a budget change** → no client budget-approval gate triggered. Pure efficiency-ceiling adjustment within existing $150/day.

### Expected effect
Impression share + spend + lead volume climb over ~3–7 days as the algo bids into previously-skipped auctions. **Monitor:** CPL should settle ~$55–65; if it stays there and the campaign starts hitting the $150/day budget ceiling, THAT is the trigger to request a client-approved budget increase (real demand, not throttle). If CPL runs hotter than ~$70, dial target back toward $55.

### Staged next (NOT yet executed — for go/no-go)
1. **Brand split** — pull `all heart *` EXACT terms into their own Branded campaign (brand QS 8–10, carrying ~40% of leads at $20 CPL inside "NonBranded", inflating the non-brand read). Do AFTER ramp settles (~1 wk) to keep attribution clean.
2. **Themed ad-group restructure** — the single live ad group ("All Hearth Plumbing - NonBranded") blends HVAC + plumbing + brand under one RSA → craters ad relevance (`plumber near me` QS 3). Split into AC Repair / Heating / AC Install / Plumbing, each with a matching RSA → lifts QS → compounds the rank fix. Final URL in use: `https://callallheart.com/`. Sitelinks/callouts already exist at account level to attach.
3. **Re-sweep negatives** in ~7 days once volume grows (23 negatives already live from 07-02 audit).

### Needs client approval (budget)
- **PMax `23800161039` is budget-limited** (28% IS lost to budget, only $50/day). If its leads verify as real, this is where *added* budget actually converts — route via AM ticket with written client sign-off.

*Reversibility: tCPA revert to $29 anytime via the same field.*

---

## 2026-07-10 (same day) — Budget increases (Search + PMax), client-approved per Edu

Per Edu direction ("bump to perform at its highest, I have the ok — Search + PMax only, DO NOT touch LSA"):
- **PMax `23800161039`: $50 → $100/day** (budget `15545416029`). Justified: was losing 28% IS to budget; primary conv = 19 real calls + form fills (verified not local-action fluff).
- **Search NonBranded `23685938569`: $150 → $250/day** (budget `15446396594`). Not budget-constrained today (0% budget-lost) but raised for headroom so the new $65 tCPA ramp isn't capped as it fills. Safe: the $65 tCPA governs efficiency, so extra budget removes the volume ceiling without letting spend run away.
- **LSA: NOT touched** (Edu explicit).
- Both budgets non-shared, reference_count 1 (verified before mutate). Combined capacity now $350/day vs ~$69/day account avg — spend will ramp, not jump. **Watch daily spend vs the call-reporting lag for 2-3 days; revert either budget in one mutate if CPL/spend outruns posted leads.**
- **Governance:** budget change made on Edu's authority ("I have the ok"). AM ticket to be papered for the written client record per MasterOps.

---

## 2026-07-10 (same day, later) — Phase 2 BUILT (staged PAUSED): brand split + themed ad-group restructure

Built the compounding structural fix that sits on top of the tCPA ramp. **Everything created PAUSED — nothing serves yet.** Old mega ad group left ENABLED so there is **no lead-flow gap** until cutover. Client wants aggressive ramp ("go all in, no $300 leads") so this is staged to flip ~48h after the tCPA ramp reads clean (2 changes, each attributable).

### A. Themed ad-group restructure — inside existing NonBranded campaign `23685938569`
Fixes the root QS problem: the single live ad group ("All Hearth Plumbing - NonBranded" `193307267686`) blends HVAC + plumbing + brand under one RSA → `plumber near me` QS 3, weak ad relevance → part of the rank loss. Split into 5 tight themed ad groups, each with a matching RSA (15 headlines / 4 descriptions) + PHRASE/EXACT keywords. Inherits campaign geo/bid/budget automatically. All PAUSED.

| Ad group | ID | KWs | RSA |
|---|---|---|---|
| AC Repair | `199017381820` | 8 | ✓ |
| Heating & Furnace | `203964394691` | 8 | ✓ |
| AC Installation | `196979638774` | 8 | ✓ |
| HVAC Service | `198469621179` | 8 | ✓ (kw `hvac service near me` EXACT rejected as near-dup; covered by `hvac service` PHRASE) |
| Plumbing | `198469621619` | 10 | ✓ |

### B. Brand split — new campaign `TSD_07.10_Search_Branded_Evergreen` `24016694610` (PAUSED)
Pulls brand out of "NonBranded" (brand = QS 8–10, ~40% of leads at ~$20 CPL, was inflating the non-brand read and sharing the $150/day). Settings replicated from NonBranded: **3 proximity circles** (Ridgecrest 40mi `35.620506,-117.671781`; Lancaster/Palmdale 20mi `34.703947,-118.148102`; Tehachapi/Mojave 20mi `35.047538,-118.170666`), English (1000), Search+partners, **Maximize Conversions (no target — brand converts cheap)**, budget **$30/day** (own non-shared budget `15714809452`).
- Ad group "Brand - All Heart" `198469690939` — **17 brand EXACT keywords** + brand RSA.
- Orphan shared budget from a first failed attempt (Max Conv rejects shared budgets) was deleted. Fix logged in aprendizados below.

### CUTOVER (run at flip, ~48h) — script ready: `clients/all-heart-heating-cooling/phase2_cutover.py`
Script does, in order: (1) ENABLE the 5 themed ad groups + their RSAs, (2) PAUSE old mega ad group `193307267686`, (3) ENABLE brand campaign + ad group + RSA, (4) add the 17 brand terms as EXACT **negatives** to NonBranded `23685938569` so brand queries route to the brand campaign. Has `DRY_RUN=True` guard — run once to preview, flip to `False` to execute.
**Pre-flip checklist:** confirm the 6 new RSAs show APPROVED (not disapproved on policy) and ad strength ≥ "Good"; confirm tCPA ramp is healthy (IS up, CPL ≤ ~$65). Brand campaign activation + its $30/day budget should get the AM/client nod (new spend line) even though it's a reallocation.

### Reversibility
Re-enable `193307267686`, pause the 5 themed groups + brand campaign, remove the brand negatives. All IDs above.

---

## 2026-07-02 — Non-branded search term audit + negative sweep

**Scope:** Campaign `TSD_03.22_Search_NonBranded_Evergreen` (ID `23685938569`) — the only enabled non-branded Search campaign with traffic. Budget $150/day. Window analyzed: **90 days (2026-04-03 → 2026-07-02)**.

### What we researched
- Pulled search terms + keywords for the campaign with cost & conversions, computed **CPL (cost per lead)** per term.
- Reference: campaign = **736 clicks · 140.7 conv · $3,811 → blended CPL ~$27**.
- Non-brand search terms alone: CPL **$26.38**.
- **$804 was spent on zero-conversion search terms** over 90 days.

### Key findings
- **Brand is carrying the campaign.** 8 brand EXACT keywords live *inside* this "NonBranded" campaign. Brand = **$1,365 · 61.5 conv · CPL $22.20 → 44% of all conversions** on 36% of spend. Strip brand out and true non-branded CPL is **~$31** (above the ~$27 target).
- **Brand standout:** `all heart heating and cooling` — **$19.74 CPL, 57 conv** (≈40% of the whole campaign's leads). Best performer in the account.
- **Two brand problems (NOT negatives — other action needed):**
  - `allheart heating and cooling` (one word) — **$97.60, 0 conv**. Brand intent converting at zero is a **tracking / landing-page / routing red flag**, not a bad term. Needs investigation.
  - `all heart` (bare) — **$54.70 CPL** (2× target); the phrase is generic and pulls junk.
- **Of the $804 zero-conv spend:** $128 was our own brand (excluded), leaving **~$660 of genuinely negatable waste** — competitors (~$218), generic/other (~$362), parts/DIY/research (~$97), out-of-area (~$0).

### What we did — 23 campaign-level negatives added (none existed before)
Applied to campaign `23685938569`, campaign level. Estimated recovery: **~$550–600/quarter**.

**14 PHRASE** (pattern killers): `cost` · `distributor` · `distribution` · `capacitor` · `goodman` · `lennox` · `ruud` · `ferguson` · `bradford white` · `los angeles` · `roto rooter` · `mr rooter` · `air ductors` · `arctic air`

**9 EXACT** (specific 0-conv spenders): `plumbing companies near me` · `campbell heating and air ridgecrest ca` · `water heater` · `positive energy air conditioning & heating` · `mechanical air conditioner` · `all temp heating and air` · `topline heating and air` · `arctic plumbing` · `hot water heater maintenance`

### Deliberately NOT touched
- **Brand terms** (own brand — leave to convert): `all heart heating and cooling`, `all heart heating`, `all heart heating cooling & plumbing`, `allheart heating and cooling`, `all heart`, `heart heating and cooling`.
- **Watch-list (good intent, too little data to judge):** `air conditioning near me` · `hvac near me` · `ac service near me` · `hvac contractors near me` — core service terms, 0 conv but only 1–7 clicks each. Give more volume before cutting.

### Open items / next steps
1. **Investigate `allheart` 0-conv anomaly** — check conversion tracking, ad→LP match, and routing for brand traffic ($97.60 wasted with brand intent).
2. **Split a dedicated Branded campaign** — move the 8 brand EXACT keywords out of NonBranded so brand doesn't inflate the campaign's CPL and doesn't compete with prospecting for the same $150/day budget.
3. **Re-run search-term sweep in ~7–14 days** — catch the long tail of ~30 small competitor terms ($1–8 each: schultz, a1 plumbing, louie's, hawley, trademasters, us air conditioning, etc.) that the phrase negatives don't fully cover.

*Reversibility: all negatives are campaign-level and can be removed anytime.*
