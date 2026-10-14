#!/usr/bin/env python3
"""
Proud Pops, read-only: before/after pull for the 2026-10-13 budget cut (see budget-cut-2026-10-13.md).
Same metrics for any window, so the after-period is compared apples to apples with the saved baseline.
  ./tsd.sh <this file> --since 2026-09-13 --until 2026-10-12 --label pre30
  ./tsd.sh <this file> --since 2026-10-14 --until 2026-10-27 --label post14
Writes clients/proud-pops/budget-cut-2026-10-13/<label>.json and prints a per-campaign table.
Oct 13 is a mixed day (cut applied ~17:20 CT): leave it out of both windows.
Website lead before 2026-10-07 10:32 CT includes /careers job applications: compare forms only on post-fix windows.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import defaultdict
CID = "1051843378"
OUT = os.path.expanduser("~/Documents/GitHub/topserv-workspace/clients/proud-pops/budget-cut-2026-10-13")
CUT = {"23853595615": (295, 50), "23866982084": (230, 75), "23848895678": (375, 300), "23866999121": (600, 500)}
PENDING_UI = {"YT - VideoViews (San Antonio)": (100, 0)}   # Edu to pause in UI (fu-046)
ACTIONS = ("Website lead", "TSD - Website Call", "Calls from ads", "TSD - Email Click")


def pull(since, until):
    w = f"segments.date BETWEEN '{since}' AND '{until}'"
    camps = {}
    for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
        campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros,
        metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE {w} AND metrics.impressions > 0"""):
        c, m = r["campaign"], r["metrics"]
        cost = int(m.get("cost_micros", 0)) / 1e6; clicks = int(m.get("clicks", 0))
        camps[c["id"]] = {
            "name": c["name"], "type": c["advertising_channel_type"], "bidding": c.get("bidding_strategy_type"),
            "tcpa": int(c.get("maximize_conversions", {}).get("target_cpa_micros", 0)) / 1e6 or None,
            "budget_now": int(r.get("campaign_budget", {}).get("amount_micros", 0)) / 1e6,
            "cost": round(cost, 2), "clicks": clicks, "impressions": int(m.get("impressions", 0)),
            "cpc": round(cost / clicks, 2) if clicks else None,
            "is": m.get("search_impression_share"), "budget_lost": m.get("search_budget_lost_impression_share"),
            "rank_lost": m.get("search_rank_lost_impression_share"),
            "conv": defaultdict(float), "taps_by_network": defaultdict(float), "cost_by_network": defaultdict(float),
            "daily_cost": {},
        }
    for r in run_query(CID, f"""SELECT campaign.id, segments.conversion_action_name, metrics.all_conversions
        FROM campaign WHERE {w} AND metrics.all_conversions > 0"""):
        if r["campaign"]["id"] in camps:
            camps[r["campaign"]["id"]]["conv"][r["segments"]["conversion_action_name"]] += float(r["metrics"]["all_conversions"])
    for r in run_query(CID, f"""SELECT campaign.id, segments.ad_network_type, segments.conversion_action_name, metrics.all_conversions
        FROM campaign WHERE {w} AND metrics.all_conversions > 0"""):
        if r["campaign"]["id"] in camps and r["segments"]["conversion_action_name"] == "TSD - Website Call":
            camps[r["campaign"]["id"]]["taps_by_network"][r["segments"]["ad_network_type"]] += float(r["metrics"]["all_conversions"])
    for r in run_query(CID, f"""SELECT campaign.id, segments.ad_network_type, metrics.cost_micros
        FROM campaign WHERE {w} AND metrics.cost_micros > 0"""):
        if r["campaign"]["id"] in camps:
            camps[r["campaign"]["id"]]["cost_by_network"][r["segments"]["ad_network_type"]] += int(r["metrics"]["cost_micros"]) / 1e6
    for r in run_query(CID, f"""SELECT campaign.id, segments.date, metrics.cost_micros FROM campaign WHERE {w} AND metrics.cost_micros > 0"""):
        if r["campaign"]["id"] in camps:
            camps[r["campaign"]["id"]]["daily_cost"][r["segments"]["date"]] = round(int(r["metrics"]["cost_micros"]) / 1e6, 2)
    for c in camps.values():
        c["conv"] = {k: round(v, 1) for k, v in c["conv"].items()}
        c["taps_by_network"] = {k: round(v, 1) for k, v in c["taps_by_network"].items()}
        c["cost_by_network"] = {k: round(v, 2) for k, v in c["cost_by_network"].items()}
    return camps


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--since", required=True); ap.add_argument("--until", required=True)
    ap.add_argument("--label", required=True); a = ap.parse_args()
    camps = pull(a.since, a.until)
    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/{a.label}.json"
    json.dump({"window": [a.since, a.until], "campaigns": camps}, open(path, "w"), indent=1, sort_keys=True)
    from datetime import date
    days = (date.fromisoformat(a.until) - date.fromisoformat(a.since)).days + 1
    pct = lambda v: f"{float(v) * 100:.0f}%" if v not in (None, "") else "-"
    print(f"{a.label}: {a.since} to {a.until} ({days} days) -> {path}")
    for cid, c in sorted(camps.items(), key=lambda x: -x[1]["cost"]):
        tag = "CUT" if cid in CUT else ("UI" if any(k in c["name"] for k in PENDING_UI) else "ctl")
        forms = c["conv"].get("Website lead", 0); taps = c["conv"].get("TSD - Website Call", 0)
        disp = sum(v for k, v in c["taps_by_network"].items() if k in ("CONTENT", "YOUTUBE"))
        print(f" {tag:3} {c['name'][:44]:44} ${c['cost']:>9,.0f} (${c['cost'] / days:>5,.0f}/d)  clk {c['clicks']:>6}  cpc {c['cpc'] or 0:>6.2f}"
              f"  forms {forms:5.1f}  taps {taps:6.1f} (disp/yt {disp:5.1f})  calls {c['conv'].get('Calls from ads', 0):4.1f}"
              f"  IS {pct(c['is'])} bud {pct(c['budget_lost'])} rank {pct(c['rank_lost'])}")


if __name__ == "__main__":
    main()
