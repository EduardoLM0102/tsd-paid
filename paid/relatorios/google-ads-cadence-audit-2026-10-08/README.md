# Google Ads management cadence audit — 2026-10-08

**Why:** someone asked Edu for a list of our clients' Google Ads accounts, the management/optimization
work on each, and his weekly/daily cadence. This folder holds the evidence pull and the draft reply.

**Everything here is read-only.** No account was changed.

## Sources
- Google Ads API (`tsd.sh`, MCC 4155514468): `change_event` for 09-09 → 10-08 (the API keeps 30 days) and
  30d/7d spend for every current account. Scripts and raw JSON are in `scripts/`.
- Agency Titan: all "7-Day Google Search Ads Optimization" (`c31def07…`) and "7-Day Local Service Ads
  Optimization" (`2ecf5c07…`) tasks created since 08-01, plus the task lists of clients without them.
- Client logs in `clients/*/google-ads-log.md`.
- Drive sheet "Client Accounts - Audit (Master doc)" (`1E-hmY2oorLBq_Lx_OQgbDbPBWL8bie0cpJyU-iKbpa4`)
  for client status.

## Client status (Edu, 10-08; overrides the roster CSV)
- **Offboarded:** GC Home Service, Gillespie's. **Offboarding:** On The Way (AM note: terminates 11/2/2026;
  client revoked our Google access 10-05). **Frozen:** Golden Plumbing. **Active:** Nick's (audit sheet).
- On Time Service Pros terminates 10/16/2026 (Meta only).

## Weekly cadence: what the record shows
- 13 clients get an AT 7-Day Google Search task **and** a 7-Day LSA task every 7 days: All Seasons, C&S,
  Gillespie's, Hawkins, King's Window, Lilypad, Live Wire (stopped after 09-21), Mission Accomplished,
  Napps, On The Way, Spencer, Watt's Right, Zen Air.
- They're worked in one pass early in the week, usually Monday. Close dates: 08-10, 08-25, 08-31, 09-09,
  09-15, 09-21/22, 09-28, 10-05.
- **Slips:** the 08-17 tasks were closed with the next week's on 08-25. Six of the 09-28 tasks (C&S,
  Spencer, Gillespie's, All Seasons, MA, Zen Air) closed on 10-05.
- **Daily:** no fixed daily routine in the record. Mid-week work happens on accounts with a fresh change
  or an open ticket.

## Accounts with NO AT 7-day task (and the last real check)
| Account | Last check on record | 30d spend |
|---|---|---|
| Nick's Heating 1854100356 | Never, until the 10-08 first pass (see `clients/nicks-heating/`) | $4.8k |
| My Favorite Service Co 9815330464 (Proud Pops' merged brand) | 07-23 budget analysis | $1.8k |
| Neon Monkey LSA 1219885876 | 08-10 | $0.9k |
| ICS LSA Belleville 2895702982 (incl. "Mitsubishi YouTube") | 09-11 | $0.7k |
| Neon Monkey PPC 7953905280 | 09-28 (lawn care ticket) | $8.4k |
| Cool Hand 9865206319 (LSA out of scope) | 10-05 / 10-07 | $5.3k |
| ICS PPC 4571881760 (AT name "ICS") | 10-07 | $2.2k |
| Proud Pops PPC + LSA | 10-07 | $60.4k |

Not counted: Golden (frozen), GC (offboarded), Eaglepoint ($0, nothing built).

## Red flags from the change history
- **Live Wire 1056617442:** `brandon@tradevulcan.com` (Trade Vulcan) made ~690 changes since 09-16.
  He built "… | LWE V2 REVIEW 2026-09-16" copies of both Search campaigns and paused TSD's originals on
  10-05/06. AT tasks stopped after 09-21. **Confirm whether Live Wire is still a client.**
- **Strickland 9049508615:** every change is by `@onpurposemedia.com`. All TSD_ campaigns are paused;
  only "Cooling" and "Pmax - AC" run (~$4.4k/30d). Strickland isn't in AT or the audit sheet.
- **Pauses with no reason logged** (all made from Edu's login): Gillespie's 10-02, GC 09-15, Cool Hand
  HVAC 10-07.
- All Seasons and Zen Air change counts are inflated by ClickCease IP exclusions (~3,000 and ~230).
  Don't quote raw change counts.

## Housekeeping done 10-08
- `contas.yaml`: restored the missing `- nome:` line for All Heart. Without it, "Cool Hand Electric"
  resolved to All Heart's 9205826499. Registered Nick's.
- `clients/README.md`: added `nicks-heating/`.

## Draft reply (from Edu, Slack). Update the statuses before sending.
> Here is where every Google account stands. Weekly cycle in Titan (7-Day Google Search + 7-Day LSA task
> for each client, every week): Watt's Right, Hawkins, All Seasons, Zen Air, C&S, Spencer, Napps,
> King's Window, Lilypad, Mission Accomplished, plus Gillespie's and GC until offboarding and On The Way
> until it lost access. Worked when needed, no weekly task: Proud Pops, Neon Monkey, Cool Hand, ICS,
> Nick's (first full check done 10-08). Golden is on freeze.
>
> Cadence: one pass early in the week, usually Monday. For each account I pull the last 7 days (spend,
> CPL, CPC, leads, conversion rate, branded vs unbranded, impression share), check the conversions are
> real leads, go through search terms since the last change and add negatives, check budget pacing and
> disapproved ads. Then KPI entry in Titan and notes in the client log. After a change I set a recheck
> 7 to 14 days out. Mid-week: accounts with a fresh change or open problem, plus AM and client tickets.
> Deeper audits, media plans and reports when something moves.
>
> Next: I'm asking for weekly Titan tasks on Proud Pops, Neon Monkey, Cool Hand, ICS and Nick's so
> nothing depends on a ticket to get checked.

The per-account work detail (what changed when) is in each client's `google-ads-log.md`, 10-05 entries.
