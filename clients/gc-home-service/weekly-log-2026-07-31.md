# GC Home Service — Internal Optimization Log
## Week ending Friday 2026-07-31

**INTERNAL ONLY.** Honest root cause lives here. Client version is sanitized per
`topserv-client-report-format` (never signal something was wrong) but calibrated per
`tsd-client-message-style` (don't over-sanitize real underperformance).

Data pulled 2026-07-31. Google Ads `2375064049` (tz `Africa/Kampala`, ~1 day lag, so Jul 31 is partial).
Meta `1434273655098937`.

---

## 1. Headline numbers

| | Spend | Leads | Cost per |
|---|---|---|---|
| **Google** (Jul 25–31) | $766.13 | 2 tracked calls | **$383.06** |
| **Meta lead gen** (Jul 25–31, paused Jul 30) | $1,048.83 | 6 | **$174.81** |
| Meta awareness (back on Jul 28) | $54.32 | 80 ad recall lift | $0.68 |
| Meta recruiting (launched Jul 27) | $146.03 | 9 applications | $16.23 |
| **Combined** | **$2,015.31** | 8 customer leads | **$226.87** blended |

Blended customer CPL excludes recruiting and awareness spend (neither is a customer-lead channel).

### Google week over week

| | Jul 18–24 | Jul 25–31 | Δ |
|---|---|---|---|
| Spend | $1,658.86 | $766.13 | **−54%** |
| Clicks | 68 | 61 | −10% |
| Avg CPC | $24.39 | $12.56 | **−49%** |
| Calls (all conv) | 2 | 2 | flat |
| Cost per call | $829.43 | $383.06 | **−54%** |

### The four days since the Jul 28 rebuild (the real read)

| | Jul 25–27 (before) | Jul 28–31 (after) | Δ |
|---|---|---|---|
| Spend | $490.15 | $275.98 | −44% |
| Clicks | 20 | 41 | **+105%** |
| Avg CPC | $24.51 | **$6.73** | **−73%** |

Four days is not proof, but the direction is unambiguous and it's the strongest single
data point we have to take to the client. Watch it through next week before repeating it.

---

## 2. What changed

### Google (`2375064049`) — executed Jul 28, detailed in `google-ads-log.md`
- **PMax budget $155 → $50/day** (`TSD_PMAX_Calls` 23511318927, budget 15337617979).
- **Conversion goals rebuilt on both live campaigns.** `DEFAULT/WEBSITE` (First Time + Repeat
  Phone Call) and `QUALIFIED_LEAD/WEBSITE` (Form) made biddable; `PHONE_CALL_LEAD/CALL_FROM_ADS`
  turned off. Re-verified live on 2026-07-31, still in place on both campaigns.

**CORRECTION to the 2026-07-27 audit.** The audit called `Calls from ads [1]` a "call-extension
click." It isn't. Pulled the action definitions on 07-31:

| Action | Category / Origin | Call duration threshold | 90d |
|---|---|---|---|
| `Calls from ads [1]` | PHONE_CALL_LEAD / CALL_FROM_ADS | **15s** | 27 |
| `First Time Phone Call` | DEFAULT / WEBSITE | **60s** | 13 |
| `Repeat Phone Call` | DEFAULT / WEBSITE | **60s** | 8 |
| `Form Submision [Landing Page]` | QUALIFIED_LEAD / WEBSITE | n/a | 0 |
| `[TSD] Website Call Link` | PHONE_CALL_LEAD / CALL_FROM_ADS | n/a (tel: link) | 4 |

`Calls from ads` is a genuine connected call, just held to a 15-second bar. The "tap, not a call"
description only fits `[TSD] Website Call Link`, which is 4 of 31 firings. **What we actually did
was move bidding from a 15-second bar to a 60-second bar plus the form.** That's a lead-quality
upgrade and it survives the client opening their own account. Do not repeat the "call button" line.

Tradeoff: biddable signal went from 31 events/90d to 21, which is why both campaigns re-entered
learning thin.
- `TSD_07.05_Search_Nonbranded_Cooling` last spent Jul 25 ($61.71), paused since. Stays off.

### Meta (`1434273655098937`)
- **Jul 30, 7:28am — `CBO | NEW CREATIVES | 8 JUL` paused** (Edu, Power Editor). It ran
  $1,048.83 for 6 leads that week = $174.81, against $110.91 over its full Jul 8–31 run.
  Deteriorating, so it came off while new creative is produced.
- **Jul 27, 3:27pm — that campaign's budget had been raised $185 → $200/day** (Manuel) three days
  before the pause. Worth flagging internally; it raised the burn right before we killed it.
- **Jul 28, 12:57pm — awareness CBO re-enabled**, budget $30 → $20/day (Manuel).
- **Jul 27, 4:08–4:16pm — new recruiting campaign built and launched**
  (`TSD_07.27_Hiring_ABO_KY_Journeyman_HVAC_Lead_Installer`, $40/day, Newport KY +20mi,
  Advantage+ audience, lead form). 9 applications at $16.23 in 4 days.

---

## 3. Creative read — `CBO | NEW CREATIVES | 8 JUL`, full run Jul 8–31

$3,660.11 / 33 leads / **$110.91 blended CPL**

| Ad | Spend | Leads | CPL | CTR |
|---|---|---|---|---|
| Quote back 1,500 | $235.81 | 5 | **$47.16** | **2.67%** |
| Ad_B1 | $843.66 | 10 | $84.37 | 0.94% |
| Ad_B2 | $1,731.73 | 17 | $101.87 | 0.86% |
| Tune up 99 | $432.52 | 1 | **$432.52** | 0.75% |
| New System 2,500 Off | $103.77 | 0 | — | 0.99% |
| Ad_A3, Ad_B3, Quote back v2, Ad_C3, Free diagnostic | $312.62 | 0 | — | — |

**The offer is doing the work, not the format.** The quote-back offer pulled leads at $47 with the
highest CTR in the account. The $99 tune-up pulled one lead for $432. That's the evidence base for
the offer consolidation the client asked for, and it should shape the new batch: lead with the
quote-back mechanic, drop the tune-up as a standalone hook.

Caveat before anyone repeats $47.16 to the client: it's 5 leads on $235 of spend. Directionally
right, statistically thin. Report it as a signal, not a benchmark.

---

## 4. Landing page — the Google argument

PMax impression share, rank-lost vs budget-lost:

| | Jul 18–24 | Jul 25–31 |
|---|---|---|
| Search IS | 14.3% | 20.3% |
| Lost to **Ad Rank** | **78.0%** | **68.5%** |
| Lost to budget | 7.7% | 11.2% |

Rank loss, not money, is the ceiling. Rank is bid × quality, and quality is landing page
relevance + asset relevance. We're sending paid HVAC traffic to the generic site. A dedicated
page matched to the ad is the highest-leverage move available: better destination quality → lower
CPC → more clicks for the same money → lower CPL.

Second reason, not for the client deck: **we have no working form path.**
`Form Submision [Landing Page]` (QUALIFIED_LEAD) fired **0 times in 90 days** and
`[TSD] Lead Form [LP]` fires 0 and isn't even counted. Every conversion this account has ever
recorded is a phone-call event. A new page we control gives us a form we can actually instrument.
Frame to the client as "adds a measurable form path," never as "the current tag is dead."

**Status: awaiting client approval.**

---

## 5. Reporting artifact to be aware of

Turning off `PHONE_CALL_LEAD/CALL_FROM_ADS` as a biddable goal also removed it from the
**Conversions** column. Jul 28–31 shows `counted = 0` but `all_conversions = 1` — a real call
happened, it just reports under All Conversions now.

Use **all conversions** for any week-over-week call comparison that spans Jul 28, or the numbers
will look like the account fell off a cliff when it didn't. Both weeks = 2 calls on that basis.

---

## 6. Open items

- [ ] **ATRASADO: AM ticket for the PMax budget cut** ($155 → $50/day, Jul 28, done on Edu's verbal
      authority). MasterOps requires written client record. Now a week old.
- [ ] **New Meta creative batch** built on the consolidated offer — requested, expected today.
      Once in: one DCT ad set per angle, quote-back leads the batch.
- [ ] **Landing page approval** from the client. Blocks the Google quality play.
- [ ] ServiceTitan offline import — GC still has zero upload-origin conversion actions. The real fix.
- [ ] Budget raise on `CBO | NEW CREATIVES` to $200/day on Jul 27 (Manuel) three days before we
      paused it. Worth a word so it doesn't repeat.
- [ ] Blocker still open: *July Campaign Management, Budget Allocation & Lead Quality Review* has
      never been supplied. Searched Drive and Gmail on Jul 31, not there. This week's report was
      built to the section structure Edu specified. Get the doc before the next one.
