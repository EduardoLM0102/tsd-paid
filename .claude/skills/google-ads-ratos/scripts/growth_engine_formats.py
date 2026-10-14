#!/usr/bin/env python3
"""
Growth Engine pull — YouTube format split (in-stream vs in-feed vs Shorts). READ-ONLY.

VIDEO campaigns here are all VIDEO_RESPONSIVE ad groups (multi-format), so
ad_group.type can't separate in-stream from in-feed. segments.ad_format_type can.
Runs over every account that had VIDEO / DEMAND_GEN / PERFORMANCE_MAX delivery in
google_campaign_12mo.csv.

Uso:
    ./tsd.sh growth_engine_formats.py --raw ../../../../paid/relatorios/growth-engine-pull-2026-09/raw/google
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
            if r["channel_type"] in ("VIDEO", "DEMAND_GEN", "PERFORMANCE_MAX"):
                accounts[r["customer_id"]] = r["account"]

    svc = init_client().get_service("GoogleAdsService")
    out, errors = [], []
    # ad_format_type can't be combined with ad_network_type, and PMax may reject it,
    # so each channel group runs as its own query.
    groups = ["'VIDEO', 'DEMAND_GEN'", "'PERFORMANCE_MAX'"]
    for cid, name in sorted(accounts.items()):
        for grp in groups:
            q = f"""
                SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
                       segments.ad_format_type,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM campaign
                WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
                  AND campaign.advertising_channel_type IN ({grp})
                  AND metrics.impressions > 0"""
            try:
                for r in svc.search(customer_id=cid, query=q):
                    out.append([cid, name, r.campaign.id, r.campaign.name,
                                r.campaign.advertising_channel_type.name,
                                r.segments.ad_format_type.name,
                                r.metrics.impressions, r.metrics.clicks,
                                round(r.metrics.cost_micros / 1_000_000, 2)])
            except Exception as e:
                f = getattr(e, "failure", None)
                msg = "; ".join(x.message for x in f.errors) if f else str(e)[:400]
                errors.append([cid, name, grp, msg])
                print(f"ERR {cid} {name} [{grp}]: {msg}", file=sys.stderr)

    with open(os.path.join(args.raw, "google_youtube_format_12mo.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["customer_id", "account", "campaign_id", "campaign", "channel_type",
                    "ad_format_type", "impressions", "clicks", "spend_usd"])
        w.writerows(out)
    print(f"{len(out)} rows, {len(errors)} errors", file=sys.stderr)
    for e in errors[:5]:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
