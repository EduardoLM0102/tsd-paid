#!/usr/bin/env python3
"""
Growth Engine pull — weekly delivery by channel type AND ad network (Mon-Sun weeks). READ-ONLY.

Splits every campaign type's weekly impressions into YouTube / Display / Search networks, so the
YouTube and Display impressions that Performance Max buys can be counted per client per week
alongside Meta. Same window as the rest of the pull.

Uso:
    ./tsd.sh growth_engine_weekly_network.py --raw ../../../../paid/relatorios/growth-engine-pull-2026-09/raw/google
"""

import argparse
import csv
import os
import sys

sys.path.insert(0, ".")
from lib import init_client

SINCE, UNTIL = "2025-09-29", "2026-09-27"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    args = ap.parse_args()

    accounts = {}
    with open(os.path.join(args.raw, "google_campaign_12mo.csv")) as f:
        for r in csv.DictReader(f):
            accounts[r["customer_id"]] = r["account"]

    svc = init_client().get_service("GoogleAdsService")
    out = []
    for cid, name in sorted(accounts.items()):
        q = f"""
            SELECT segments.week, campaign.advertising_channel_type, segments.ad_network_type,
                   metrics.impressions, metrics.clicks, metrics.cost_micros
            FROM campaign
            WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}' AND metrics.impressions > 0"""
        try:
            for r in svc.search(customer_id=cid, query=q):
                out.append([cid, name, r.segments.week, r.campaign.advertising_channel_type.name,
                            r.segments.ad_network_type.name, r.metrics.impressions, r.metrics.clicks,
                            round(r.metrics.cost_micros / 1_000_000, 2)])
        except Exception as e:
            f = getattr(e, "failure", None)
            print(f"ERR {cid} {name}: " + ("; ".join(x.message for x in f.errors) if f else str(e)[:300]),
                  file=sys.stderr)

    with open(os.path.join(args.raw, "google_weekly_by_network.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["customer_id", "account", "week_start", "channel_type", "ad_network_type",
                    "impressions", "clicks", "spend_usd"])
        w.writerows(out)
    print(f"{len(out)} rows", file=sys.stderr)


if __name__ == "__main__":
    main()
