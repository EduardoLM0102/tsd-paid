# GC Home Service — Forward Marketing Calendar (Internal)
## August 2026 – February 2027

**INTERNAL ONLY.** Ticket ask: proactive forward planning instead of month-to-month reaction.
Built 2026-08-05 off the 2026-07-31 weekly close (`weekly-log-2026-07-31.md`, `google-ads-log.md`,
`README.md`). No client-supplied brief or marketing calendar exists — this is standard Zone 5/6
HVAC seasonal doctrine (cooling to Labor Day, fall maintenance Sept–Oct, winter emergency Nov–Feb)
layered onto this account's actual performance data. Flagging inference where it matters.

No total budget figure is on file anywhere in this repo — only individual campaign daily budgets
(Google PMax $50/day post-cut, Meta awareness $20/day, etc.). Dollar figures below are deliberately
left as sequence/ratio, not commitments — any real shift still needs the written client-approval
ticket per MasterOps hard rule #1. If a client-approved monthly number ever exists, redo this as
ratios against it (Lilypad Q4 precedent: `clients/lilypad-septic/media-plan-q4-2026.md`).

---

## The Season This Is Built Around

Cincinnati tri-state HVAC demand runs on a predictable clock: cooling carries through Labor Day,
September–October is the fall maintenance/tune-up window, and the first hard cold snap (usually
around Thanksgiving) flips demand to no-heat emergencies through the coldest months. Every phase
below is sequenced against that, not against whichever channel had a slow week.

---

## 30-Day Plan — Aug 5 to Sep 4

**Focus: close out cooling while the fall push's foundation lands.** This window leans on three
open items that are already blockers today, not new work:

1. **Landing page approval — still awaiting the client**, open since before 07-31. Blocks the
   Google quality/rank play (68.5% of PMax impression share lost to Ad Rank, not budget — landing
   page relevance is the lever) and is the only planned fix for the dead form path
   (`Form Submision [Landing Page]`, 0 fires/90d). **If this doesn't land inside 30 days, the fall
   Search relaunch slips with it** — don't launch fall creative onto an unapproved destination.
2. **Service area list reconciliation — unresolved since 2026-07-13.** Google's list and Meta's
   list don't match (`README.md` §Service area). "Amelia, KY" and "Williamsburg, KY" have been
   escalated twice with no answer. This also gates direct mail (below) and the still-live problem
   that Meta targeting is sitting on Manuel's Jul 8 dropped-pin overwrite (Newport KY +40km), not
   the city/ZIP list Edu adjudicated by hand on Jul 13 — that decision (real city list vs. formal
   radius rescope) needs to close here too.
3. **ServiceTitan / offline conversion import — not built, zero upload-origin conversion actions
   exist today** (same gap as Golden Plumbing, Proud Pops). Start the connection now so November's
   bidding — the highest-value month of the year — optimizes on booked jobs, not call-button
   clicks. This is also why weather-triggered budget response (below) is sequenced to the 90-day
   window and not sooner: reacting fast to a signal on top of a thin/dirty conversion base is the
   same mistake as the Jul 16 PMax 3x bump (Andrea raised it to $155/day while bidding on
   call-button clicks; it bled ~$963 for 1 conversion before the Jul 28 cut to $50). A weather
   trigger is a faster version of the same lever — don't hand it dirty signal.
4. **Paper the overdue AM ticket** for the Jul 28 PMax budget cut ($155→$50/day, executed on Edu's
   verbal authority, still undocumented as of 07-31). Should not still be open when this calendar
   starts generating its own budget-change tickets.

Seasonal/creative in parallel:
- Keep AC repair/replacement live through Labor Day (Sep 7) — last real cooling-demand week.
- Relaunch Meta lead gen on the consolidated offer: **quote-back ($1,500) leads the new batch** —
  it's the only creative in the account with real signal ($47.16 CPL, 2.67% CTR, though thin at
  5 leads/$235 spend). One DCT ad set per angle, per doctrine.
- Soft-launch early-bird fall tune-up messaging alongside cooling. **Do not sell the $99 tune-up
  standalone** — it pulled 1 lead at $432.52, the worst CPL in the account, when it ran alone in
  July. Bundle it into a fuller system-check offer this time.

**By day 30:** foundation closed (or explicitly flagged as still open, with a new date), fall
creative in production, quote-back-anchored Meta batch live.

---

## 60-Day Plan — Aug 5 to Oct 4

**Focus: fall maintenance live across every channel.**
- Furnace tune-up campaign live on Search — relaunch the paused nonbranded campaign
  (`TSD_07.05_Search_Nonbranded_Cooling` retired/replaced) themed to furnace/no-heat prevention
  terms, with the negatives list (competitors, junk-intent terms) carried over from the June/July
  cleanup rather than rebuilt from scratch.
- Meta tune-up ad set live, bundled offer per the 30-day note above.
- PMax asset groups refreshed to fall service lines; keep the $50/day budget as the floor until
  conversion signal (form path fixed, ServiceTitan connected) justifies moving it — don't repeat
  the Jul 16 bump-before-proof pattern.
- Direct mail creative and mail-house partner locked, targeted at the finalized service area list
  from the 30-day item. Vendor is not sourced yet — this is a real task for whoever picks it up.
- Weather-trigger logic built and run in **shadow mode only** (logging, no live budget changes)
  against the season's first cool nights.

---

## 90-Day Plan — Aug 5 to Nov 3

**Focus: pre-winter push and the first live weather-triggered campaign.**
- Financing-led messaging becomes the primary offer heading into the holidays.
- Thanksgiving week (Nov 26) no-heat/emergency positioning goes live — the tri-state's first real
  cold-snap-driven demand spike.
- First direct mail drop (EDDM to the finalized service area) lands early November, ahead of
  Thanksgiving week, carrying a furnace/no-heat offer. Trackable via a dedicated number or promo
  code — same measurement discipline as the paid channels, not "however it feels."
- Weather-triggered campaigns go live for real — budget/bid response, not just logging — *only if*
  the shadow-mode test came back clean and ServiceTitan/offline conversions are live by then.
  If either isn't ready, hold weather-triggers in shadow mode rather than force the date.
- Booked-job tracking should be live by this point, so November — the highest-value month before
  deep winter — is bidding on outcomes verifiable against GC's own books.

---

## Weather-Triggered Campaigns — Mechanism

Cincinnati weather is the best leading indicator this account has: a run of 90°+ days in cooling
season or a hard cold snap in heating season moves call volume before search volume catches up.
Mechanism: define trigger thresholds per season (e.g. sustained 90°+ for 2+ days May–Sept for AC
emergency; ≤20°F or a cold-snap/freeze advisory Nov–Mar for no-heat emergency), and when a public
forecast feed (NWS or a free-tier API like OpenWeatherMap — no vendor research done, small-account
scale, no enterprise weather-ad platform needed) crosses them, temporarily lift Search budget and
pin a weather-referencing RSA headline, mirrored with a short Meta budget lift on the live lead
campaign. Build as a Google Ads Script on a schedule, reviewed by hand before each seasonal window
rather than fully automatic from day one. **Deliberately sequenced behind the ServiceTitan/offline
conversion fix** — see the Jul 16 PMax lesson above. Fast reaction on dirty signal just buys faster
mistakes.

---

## Direct Mail — Future Opportunity

Three plays, sequenced by readiness, all gated on the service-area list reconciliation:

1. **EDDM neighborhood drop.** First run early November, ahead of Thanksgiving/first cold snap,
   furnace/no-heat offer. Needs a mail-house partner (not sourced) and finalized creative.
2. **Customer maintenance reminder.** Once ServiceTitan/booked-job history is connected, mail past
   customers due for a tune-up — cheapest per piece, warmest list, ties to the existing "Repeat
   Phone Call" demand already seen in the account's own conversion data.
3. **New-mover mailer.** Ongoing monthly drop to recent movers into the service area — standard,
   well-proven HVAC direct-mail trigger.

All three carry a dedicated phone number or promo code for attribution — don't launch a channel
that inherits the same measurement gap Google and Meta are currently working through.

---

## 180-Day Seasonal Roadmap — Aug 2026 to Feb 2027

| Month | Season Phase | Lead Offer / Angle | Google | Meta | Direct Mail / Other |
|---|---|---|---|---|---|
| **Aug** | Late cooling / foundation | AC repair & replacement; early-bird tune-up soft launch | Branded Search + PMax ($50/d floor); foundation work; nonbranded fall relaunch prepped | Lead gen relaunched on quote-back; awareness continues ($20/d) | Service area list reconciled; AM ticket for PMax cut papered |
| **Sep** | Fall maintenance opens | Furnace tune-up (bundled, never standalone $99) | Nonbranded fall terms live; PMax assets refreshed | Tune-up ad set live | Mail creative + mail house locked |
| **Oct** | Furnace tune-ups peak | Tune-up + financing intro | Full fall lineup live; weather-trigger shadow mode | Tune-up + financing test | First EDDM drop prepped |
| **Nov** | Pre-winter / first cold snap | No-heat emergency + financing; Thanksgiving week push | Weather-trigger live (if gates clear); branded + emergency terms | Emergency + financing | EDDM drop 1 lands (early Nov) |
| **Dec** | Winter promotions | Gift-of-comfort/financing early month; emergency through holidays | Emergency terms; weather-trigger active | Holiday financing + emergency | Customer maintenance reminder mailer (needs ServiceTitan live) |
| **Jan** | Peak winter emergency | No-heat, same-day, coldest-month positioning | Weather-trigger primary lever | Emergency-led | New-mover mailer ongoing |
| **Feb** | Transition | President's Day financing event; early AC tune-up pre-sell | Shift back toward cooling terms | Transition creative | Review results, draft spring calendar |

---

## Open items / next step

- [ ] Landing page approval (blocks fall Search relaunch)
- [ ] Service area reconciliation + Meta geo decision (blocks direct mail + accurate fall geo)
- [ ] ServiceTitan offline conversion import (blocks weather-trigger go-live + clean Nov bidding)
- [ ] AM ticket: paper the overdue PMax budget-cut record
- [ ] AM ticket: get this calendar in front of the client with explicit deadlines on the three
      gates above tied to the 30/60/90-day windows — nothing here is a commitment until they sign
      off, and no date should be treated as fixed if a gate slips.
- [ ] Source a direct-mail vendor/mail-house — not yet identified.
- [ ] If the *July Campaign Management, Budget Allocation & Lead Quality Review* doc ever surfaces
      (never supplied, searched 07-31, not found), check this calendar against it — it may already
      define seasonal commitments TSD is on the hook for.
