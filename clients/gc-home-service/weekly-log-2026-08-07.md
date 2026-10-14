# GC Home Service — Internal Optimization Log
## Week ending Friday 2026-08-07

**INTERNAL ONLY.** Honest root cause lives here. Client version is sanitized per
`topserv-client-report-format` (never signal something was wrong) but calibrated per
`tsd-client-message-style` (don't over-sanitize real underperformance).

Data pulled 2026-08-10. Google Ads `2375064049` (tz `Africa/Kampala`, ~1 day lag). Meta
`1434273655098937`. GTM `GTM-TQ8XNRKW` (account 6336963084, container 242276268).

---

## 1. Headline numbers, Aug 1–7 vs Jul 25–31

| | Jul 25–31 | Aug 1–7 |
|---|---|---|
| Google spend | $766.13 | $356.07 |
| Google clicks | 61 | 94 |
| Google calls tracked (all_conversions, "Calls from ads" @15s) | 2 | 3 |
| Google calls counted in Conversions column (biddable) | 1 | **0** |
| Meta lead gen | $1,048.83 / 6 leads | **PAUSED all week, $0, 0 leads** |
| Meta awareness | $70.81 / $0.71 per recall | $136.76 / ~$1.14 blended per recall |
| Meta hiring | $176.18 / 11 apps / $16.02 | $276.43 / 6 apps / $46.07 |
| Google YouTube awareness | did not exist | launched Aug 7, $11.05 day one |

Real story: zero customer leads landed anywhere this week. Google's biddable goals (60s call /
form, rebuilt Jul 28) still haven't caught a single conversion in 10 days. Meta's lead campaign
stayed dark the whole week, the "expected today" creative batch from last week's open items never
shipped.

---

## 2. What changed

### Google — landing page swap, early read (`google-ads-log.md` has full detail)
- Aug 5: branded search ad's final URL swapped to `/gc-heating-and-cooling/`. Aug 7 check-in:
  branded volume too thin (~1 click/day) to read anything yet.
- Aug 7: new YouTube/Video awareness campaign launched, ZIP-code targeted, same "build recall
  ahead of the mailer drop" logic as the Meta awareness ad set added Aug 6.

### Meta — no new lead creative, awareness expanded
- Lead campaign (`CBO | NEW CREATIVES | 8 JUL`) confirmed still PAUSED as of this pull. No relaunch,
  no new campaign built. This is the actual reason for the zero-lead week, not a tracking issue.
- New broad ZIP-code ad set added to the existing awareness campaign Aug 6 (João Pedro Ventura,
  Power Editor). Strong early CPA ($0.39/recall in first 2 days) but too small a slice (2 days,
  $7.72) to explain the account-wide awareness CPA rise on its own.
- Hiring cost-per-application nearly tripled ($16.02 → $46.07). Not diagnosed — flagged to Edu,
  left out of the client report rather than explained without a real cause.

### GTM tracking audit (2026-08-10, prompted by "why no conversions")
Checked the full chain for `[TSD] Lead Form [LP]` / the QUALIFIED_LEAD goal, since Google's own
form conversion has shown 0 in 90 days account-wide (pre-dates this week, not something we broke).

- Live published container version matches the draft workspace exactly — nothing stuck unpublished.
- Chain: `ghl_form_submit` (customEvent trigger) → fires `G.Ads - Lead` (tag 39) + `G.Ads - User
  Data` (tag 40). The event only gets pushed by `GHL - Listener` (tag 28, html, fires on All Pages),
  which listens for `postMessage` from `leadnurturemachine.com` / `leadconnectorhq.com` /
  `msgsndr.com` and needs **two** message halves (form data + an `inline-<formId>` ping) to arrive
  before it fires.
- Pulled the live `/gc-heating-and-cooling/` page source: the GHL form embed is at
  `link.leadnurturemachine.com`, iframe id `inline-BvebQQWePPwVg6tny9wr`. Matches the listener's
  whitelist and regex exactly. Real `gtm.js` loader confirmed present (not just the noscript
  fallback).
- **Conclusion: config looks structurally correct on paper. Can't confirm it actually fires without
  a live test.** Two explanations remain open: (a) genuinely nobody has completed the form yet —
  plausible, ~1 click/day on branded search and the page is 5 days old — or (b) GHL isn't sending
  both postMessage halves for this embed and the listener silently never fires.
- **Next action, not yet done:** open the page, GTM Preview on, submit one real test lead, confirm
  `ghl_form_submit` lands in the dataLayer. Two minutes, gives a definitive answer. Whoever has page
  access should run this before assuming the tracking is fine.

---

## 3. Budget ramp, 2026-08-10

Full detail and before/after table in `google-ads-log.md`. Summary: raised all 3 live campaigns
from $80/day combined to $242/day combined, targeting ~$5,530 total Google spend for August.
Split: PMax $135/day (was $20), Branded Search $50/day (was $40), Awareness/YouTube $57/day (was
$20).

**Flagged, not resolved:** PMax is getting the largest raise (6.75x) with zero biddable conversions
in the two weeks since the Jul 28 goal rebuild, and its asset group still points at the ServiceTitan
booking portal, not the new landing page. This buys reach, not proven efficiency. Sized to hit a
monthly total, not backed by a performance signal — flagged to Edu as the one needing a real
written client budget-approval ticket given the size of the jump.

**Also found while pulling current budgets:** PMax was actually running at $20/day, not the $50/day
set Jul 28 — no record anywhere of who/when dropped it further between Jul 28 and Aug 10. Not
chased down, just noted so it doesn't look like an unexplained discrepancy later.

**Question raised: will this need to come down for September?** Likely yes, at least on PMax — this
month's spend is sized to a total, not to proven ROI. Told Edu to treat August as a funded test of
the landing page + recall build, then reassess in September based on whether PMax actually starts
converting. Client report was given matching language: spend is intentionally elevated to fund the
landing page rollout and the pre-mailer recall push, and steps back toward the previously planned
level once that investment period has run its course.

---

## 4. Client report

Built as `GC Home Service Weekly Report (1st of August).pdf` (originally
`GC-Home-Service-Weekly-Update_2026-08-07.pdf`, renamed 2026-08-10 for sending). Plain Times New
Roman format, same as the Jul 31 report.

Went through several honest-framing passes with Edu before finalizing:
- Cut the raw "$X spent, N leads" headline once the real number was 0 Meta leads — led with the
  landing page deploy and the awareness/mailer recall build instead, since both are true, proactive,
  and don't require explaining a zero.
- Attributed the thin Google conversion count to the Jul 28 goal-rebuild re-learning window, **not**
  the landing page swap — the page swap only touches branded search, not PMax (most of the account's
  volume), so it can't honestly carry that explanation on its own.
- Added the YouTube awareness campaign after Edu caught that it was missing from the first draft.
- Dropped "launch new Meta lead creative" from Next Steps (not happening soon) and the "confirmed
  mail drop date" ask from Waiting On You (already have it internally, being used on Meta targeting;
  possible YouTube extension undecided, kept off for now).
- Added the budget note above once the Aug 10 ramp was executed.

**Status: built, not yet confirmed sent.**

---

## 5. Open items

- [ ] **GTM live-test not run.** Submit one real form lead on `/gc-heating-and-cooling/` with GTM
      Preview open to confirm `ghl_form_submit` actually fires. Highest-value two-minute task on the
      account right now — resolves whether the QUALIFIED_LEAD goal is dead or just unused.
- [ ] **AM ticket for the Aug 10 budget ramp** ($80/day → $242/day combined), executed on Edu's
      verbal authority. Same doctrine gap as Jul 28, now compounding.
- [ ] **ATRASADO carried over: AM ticket for the Jul 28 PMax budget cut** ($155 → $50/day, later
      found to actually be at $20/day by Aug 10 — still never papered).
- [ ] **Hiring CPA jump** ($16.02 → $46.07) not diagnosed. Left out of the client report; worth a
      look before it's asked about.
- [ ] **New Meta lead creative** still not live. Was "expected today" as of the Jul 31 report; still
      not shipped as of Aug 10.
- [x] **Mailer target area** — sorted, nothing pending here.
- [ ] ServiceTitan offline import — still zero upload-origin conversion actions. Unchanged from last
      week, still the real fix for the account's underlying attribution gap.
