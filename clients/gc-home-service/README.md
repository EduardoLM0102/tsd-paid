# GC Home Service (Greater Comfort)

HVAC / home services, Greater Cincinnati tri-state (Northern KY + southwest OH + southeast IN).
TSD client. Not previously in `contas.yaml` — folder created 2026-07-17.

## Accounts

| Platform | ID | Notes |
|---|---|---|
| Google Ads | `2375064049` | Under Topservdigital MCC `4155514468`. Access via `google-ads-ratos` skill, `scripts/tsd.sh`. |
| Meta ad account | `1434273655098937` | Business "Greater Comfort" `362393681555340`. Ads MCP enabled + queryable. |

Meta activity log is readable via the connector. Meta **targeting is NOT readable** via the
connector (`Unsupported field(s) at level 'adset': targeting`) — read targeting changes out of
the activity log instead, or check Ads Manager directly.

## Account gotchas

- **Google Ads account timezone is `Africa/Kampala`.** Cincinnati client. Every reporting day is
  shifted ~7h and the daily budget resets around 5pm local. Changing it requires Google support
  and resets historical stats. Not client-facing; decide internally whether it's worth it.
- Google Ads data lags ~1 day. On 2026-07-17 the newest complete day was 2026-07-16.
- `audit_history.py` in the skill is hardcoded to Mission Accomplished (`8634274092`) — don't
  reuse it for GC without editing.
- `campaign.start_date` / `campaign.end_date` are not valid fields in the v24 GAQL `campaign`
  resource. Don't select them.

## Service area

Two different service-area lists were supplied on 2026-07-13 (one for Meta, a longer one for
Google) and **they do not match**. The Google list adds Villa Hills, Park Hills, Erlanger,
Elsmere, Highland Heights, Taylor Mill, Latonia, Southgate, Crestview Hills, Wilder,
Fort Mitchell, Blue Ash, Hyde Park, Oakley, Madisonville, Mason, Norwood; it drops Ghent,
Sparta, Moscow. **Reconcile with the client before further geo work.**

Two entries on the client's own list are not real places and need a client answer:
- **"Amelia, KY"** — no such place. Amelia **OH** dissolved as a village in 2019.
- **"Williamsburg, KY"** — ambiguous: Williamstown KY or Williamsburg OH. Data can't decide.
  (Williamsburg KY is ~160 mi south, near the TN border, and did take 2 clicks in June.)

Verified poison entries removed from earlier Meta targeting (wrong autocomplete picks):
`Fairfield County OH` (near Columbus), `North Fairfield OH`, `Fairfield Beach OH`,
`Fairfield Acres OH` (Gallia County, zero population — confirmed via USGS GNIS),
`Butler County KY` (near Bowling Green), `Hebron Estates KY` (near Louisville).

## Known history

- **2026-06-16** — last out-of-area click on Google. All out-of-area traffic (Alabama, Michigan,
  Saudi Arabia, Owensboro KY, Indianapolis, Williamsburg KY = 22 clicks / $317) came from
  campaigns paused during June. **The July geo work did not cause this drop.** Do not claim it.
- **2026-07-08** — Manuel Lizarralde overwrote `BROAD | +18 | M+F` targeting via Power Editor to a
  single dropped pin: `2001 Monmouth St, Newport (+40 km) Kentucky`. That pin is **still live**
  as of 2026-07-15.
- **2026-07-13** — Edu rebuilt PMax location criteria (59 positive locations). Meta city list was
  adjudicated manually in Ads Manager; **it did not stick** — see the pin above.

## Weekly reporting

Committed to the client: a written update every Friday, per the *July Campaign Management,
Budget Allocation & Lead Quality Review* document.

**That document is not in this repo and has never been seen by Claude.** It defines the required
structure and the specific commitments. Get a copy before writing client-facing output.

Logs live in `weekly-log-YYYY-MM-DD.md` in this folder. Internal logs carry honest root cause;
the client-facing version is sanitized per `topserv-client-report-format` (never signal that
something was wrong — frame fixes as proactive optimization).

## Forward marketing calendar

`marketing-calendar-2026-h2.md` — 30/60/90-day plans + 180-day seasonal roadmap (Aug 2026–Feb
2027), built 2026-08-05 per the client's request for proactive planning instead of month-to-month
reaction. **Internal only, not yet built as a client deliverable.** Three open items gate most of
it: landing page approval, service-area list reconciliation, and the ServiceTitan offline
conversion import — see the doc's own "Open items" section before treating any date as fixed.
