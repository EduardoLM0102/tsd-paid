"""All Heart — post-change ramp read (hour-matched, day-of-week, IS).

Written 2026-07-11. Re-run this Monday (or any day) for the clean read on the
2026-07-10 changes (tCPA $29->$65; PMax budget $50->$100; Search budget $150->$250).

WHY hour-matched: comparing a still-running day against full days is a false read.
This cuts every day at the same hour so today vs prior days is like-for-like.
Set CUT to the current hour in ACCOUNT time (America/Los_Angeles), or leave None to
auto-derive it. Set CUT=24 once the day has fully closed.

GOTCHAS baked in (see skill aprendizados.md):
  - impression share is NOT compatible with segments.hour -> IS is queried daily only
  - intraday IS is noise; only trust it once the day closes
  - "Calls from ads" (the primary conv) has a reporting lag -> same-day conv is understated
  - Saturday on this account converts at ~3.6% vs ~17% weekday. Zero conv on a Sat is NORMAL.

Run (from anywhere):
  cd ~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts
  GADS_ENV_PATH=../.env.topserv python3 ~/Documents/GitHub/topserv-workspace/clients/all-heart-heating-cooling/ramp_check.py
"""
import os
import sys, datetime, zoneinfo
from collections import defaultdict

sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query

CID = "9205826499"
SEARCH, PMAX = "23685938569", "23800161039"
CAMPS = {SEARCH: "Search NonBranded", PMAX: "PMax Calls"}

CHANGE_DAY = "2026-07-10"          # changes landed 19:08-19:49 PT this day
PRE_DAYS = ["2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]

CUT = None   # None = auto (current hour in account tz). Set 24 for a closed day.
if CUT is None:
    CUT = datetime.datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles")).hour
TODAY = datetime.datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")

print("=" * 78)
print(f"ALL HEART — RAMP CHECK   (today={TODAY} PT, comparing hours 00..{CUT-1:02d})")
print(f"Baseline = avg of {PRE_DAYS[0]}..{PRE_DAYS[-1]} (pre-change mornings)")
print("=" * 78)

rows = run_query(CID, f"""SELECT campaign.id, segments.date, segments.hour, metrics.impressions,
 metrics.clicks, metrics.cost_micros, metrics.conversions FROM campaign
 WHERE campaign.id IN ({SEARCH},{PMAX})
 AND segments.date BETWEEN '{PRE_DAYS[0]}' AND '{TODAY}'""")

agg = defaultdict(lambda: defaultdict(float))
for r in rows:
    if int(r["segments"]["hour"]) >= CUT:
        continue
    k = (str(r["campaign"]["id"]), r["segments"]["date"])
    m = r["metrics"]
    agg[k]["imp"] += int(m.get("impressions", 0))
    agg[k]["clk"] += int(m.get("clicks", 0))
    agg[k]["cost"] += int(m.get("cost_micros", 0)) / 1e6
    agg[k]["conv"] += float(m.get("conversions", 0))

def pct(a, b):
    return f"{((a-b)/b*100):+.0f}%" if b else "n/a"

for cid, name in CAMPS.items():
    print(f"\n### {name} ({cid}) — hours 00..{CUT-1:02d}")
    print(f"  {'date':12}{'imp':>7}{'clk':>6}{'spend':>10}{'conv':>7}{'CPC':>8}{'CPL':>9}")
    for d in PRE_DAYS + [TODAY]:
        a = agg[(cid, d)]
        cpc = a["cost"] / a["clk"] if a["clk"] else 0
        cpl = a["cost"] / a["conv"] if a["conv"] else 0
        tag = "  <-- POST-CHANGE" if d > CHANGE_DAY else ""
        print(f"  {d:12}{int(a['imp']):>7}{int(a['clk']):>6}${a['cost']:>9.2f}{a['conv']:>7.1f}${cpc:>7.2f}${cpl:>8.2f}{tag}")
    base = {k: sum(agg[(cid, d)][k] for d in PRE_DAYS) / len(PRE_DAYS) for k in ("imp", "clk", "cost", "conv")}
    now = agg[(cid, TODAY)]
    print(f"  {'baseline':12}{base['imp']:>7.0f}{base['clk']:>6.0f}${base['cost']:>9.2f}{base['conv']:>7.1f}")
    print(f"  {'vs baseline':12}{pct(now['imp'],base['imp']):>7}{pct(now['clk'],base['clk']):>6}"
          f"{pct(now['cost'],base['cost']):>10}{pct(now['conv'],base['conv']):>7}")

print("\n" + "=" * 78)
print("IMPRESSION SHARE (Search) — DAILY ONLY. Today's row is partial; do not trust it.")
print("=" * 78)
rows = run_query(CID, f"""SELECT segments.date, metrics.search_impression_share,
 metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share,
 metrics.search_top_impression_share FROM campaign
 WHERE campaign.id={SEARCH} AND segments.date BETWEEN '2026-07-04' AND '{TODAY}' ORDER BY segments.date""")
print(f"  {'date':12}{'IS%':>8}{'rankLost%':>11}{'budgLost%':>11}{'topIS%':>9}")
for r in rows:
    m, d = r["metrics"], r["segments"]["date"]
    f = lambda k: float(m.get(k, 0)) * 100
    tag = "  <-- partial" if d == TODAY else ""
    print(f"  {d:12}{f('search_impression_share'):>8.1f}{f('search_rank_lost_impression_share'):>11.1f}"
          f"{f('search_budget_lost_impression_share'):>11.1f}{f('search_top_impression_share'):>9.1f}{tag}")
print("\n  budgLost% == 0.0 every day => Search is NOT budget-constrained. More budget does nothing.")

print("\n" + "=" * 78)
print("DAY OF WEEK (Search, 60d pre-change) — context for weekend reads")
print("=" * 78)
rows = run_query(CID, f"""SELECT segments.day_of_week, metrics.impressions, metrics.clicks,
 metrics.cost_micros, metrics.conversions FROM campaign
 WHERE campaign.id={SEARCH} AND segments.date BETWEEN '2026-05-12' AND '{CHANGE_DAY}'""")
dow = defaultdict(lambda: defaultdict(float))
for r in rows:
    d, m = r["segments"]["day_of_week"], r["metrics"]
    dow[d]["clk"] += int(m.get("clicks", 0))
    dow[d]["cost"] += int(m.get("cost_micros", 0)) / 1e6
    dow[d]["conv"] += float(m.get("conversions", 0))
print(f"  {'day':11}{'clk':>6}{'spend':>10}{'conv':>7}{'CPL':>9}{'convRate':>10}")
for d in ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]:
    a = dow.get(d)
    if not a:
        continue
    cpl = a["cost"] / a["conv"] if a["conv"] else 0
    cr = a["conv"] / a["clk"] * 100 if a["clk"] else 0
    print(f"  {d:11}{int(a['clk']):>6}${a['cost']:>9.2f}{a['conv']:>7.1f}${cpl:>8.2f}{cr:>9.1f}%")
print("\n  Sat converts ~3.6% vs ~17% weekday. Zero conv on a Saturday is NORMAL here — not a tracking bug.")
