#!/usr/bin/env python3
"""
Growth Engine data pull (Alex, 2026-09-21) — Google Ads side. READ-ONLY.

Covers every non-manager client account under the TopServ MCC, same window
as the Meta pull (52 full Mon-Sun weeks, 2025-09-29 .. 2026-09-27):

  campaign_12mo      spend / impressions / clicks per campaign + channel type  (item 1)
  metro_12mo         delivery by Google "metro" (= Nielsen DMA) per channel     (item 2)
  youtube_adgroup    VIDEO / DEMAND_GEN delivery by ad_group.type (format)      (item 3)
  network_12mo       delivery by ad_network_type (splits PMax into YouTube etc) (item 3)
  device_12mo        delivery by device (CONNECTED_TV = CTV screens)            (item 4)
  video_weekly_freq  unique users + avg impression frequency per user, weekly,
                     for VIDEO / DEMAND_GEN / DISPLAY campaigns                  (item 5)

Uso:
    ./tsd.sh growth_engine_pull.py --out ../../../../paid/relatorios/growth-engine-pull-2026-09/raw/google
"""

import argparse
import csv
import os
import sys
import time
from datetime import date, timedelta

sys.path.insert(0, ".")
from lib import init_client

MCC = "4155514468"
SINCE, UNTIL = "2025-09-29", "2026-09-27"


def search(service, cid, q):
    rows = []
    for row in service.search(customer_id=cid, query=q):
        rows.append(row)
    return rows


def money(micros):
    return round(micros / 1_000_000, 2)


def enum_name(v):
    return getattr(v, "name", str(v))


def write(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {len(rows):>5} rows -> {os.path.basename(path)}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    client = init_client()
    svc = client.get_service("GoogleAdsService")
    errors = []

    # --- accounts under the MCC -------------------------------------------
    acc_rows = search(svc, MCC, """
        SELECT customer_client.id, customer_client.descriptive_name, customer_client.status,
               customer_client.manager, customer_client.level, customer_client.currency_code,
               customer_client.time_zone
        FROM customer_client""")
    accounts = []
    for r in acc_rows:
        c = r.customer_client
        accounts.append([str(c.id), c.descriptive_name, enum_name(c.status), c.manager,
                         c.level, c.currency_code, c.time_zone])
    write(os.path.join(args.out, "google_accounts.csv"),
          ["customer_id", "name", "status", "is_manager", "level", "currency", "time_zone"], accounts)

    targets = [a for a in accounts if not a[3] and a[2] == "ENABLED"]
    print(f"{len(targets)} enabled client accounts", file=sys.stderr)

    camp, metro, ytag, net, dev = [], [], [], [], []
    video_campaigns = {}  # cid -> [campaign ids]
    metro_ids = set()
    date_clause = f"segments.date BETWEEN '{SINCE}' AND '{UNTIL}'"

    for cid, name, *_ in targets:
        print(f"- {cid} {name}", file=sys.stderr)

        # 1) campaign totals
        try:
            for r in search(svc, cid, f"""
                SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
                       campaign.advertising_channel_sub_type, campaign.status,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM campaign WHERE {date_clause} AND metrics.impressions > 0"""):
                ch = enum_name(r.campaign.advertising_channel_type)
                camp.append([cid, name, r.campaign.id, r.campaign.name, ch,
                             enum_name(r.campaign.advertising_channel_sub_type),
                             enum_name(r.campaign.status), r.metrics.impressions,
                             r.metrics.clicks, money(r.metrics.cost_micros)])
                if ch in ("VIDEO", "DEMAND_GEN", "DISPLAY"):
                    video_campaigns.setdefault(cid, []).append((r.campaign.id, r.campaign.name, ch))
        except Exception as e:
            errors.append([cid, name, "campaign_12mo", str(e)[:300]])
            continue  # account unreadable, skip the rest

        # 2) metro (DMA) by channel
        try:
            for r in search(svc, cid, f"""
                SELECT campaign.advertising_channel_type, segments.geo_target_metro,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM user_location_view WHERE {date_clause} AND metrics.impressions > 0"""):
                m = r.segments.geo_target_metro
                metro_ids.add(m) if m else None
                metro.append([cid, name, enum_name(r.campaign.advertising_channel_type), m or "(none)",
                              r.metrics.impressions, r.metrics.clicks, money(r.metrics.cost_micros)])
        except Exception as e:
            errors.append([cid, name, "metro_12mo", str(e)[:300]])

        # 3) YouTube formats (VIDEO / DEMAND_GEN ad group types)
        try:
            for r in search(svc, cid, f"""
                SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
                       campaign.advertising_channel_sub_type, ad_group.id, ad_group.type,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM ad_group WHERE {date_clause} AND metrics.impressions > 0
                  AND campaign.advertising_channel_type IN ('VIDEO', 'DEMAND_GEN')"""):
                ytag.append([cid, name, r.campaign.id, r.campaign.name,
                             enum_name(r.campaign.advertising_channel_type),
                             enum_name(r.campaign.advertising_channel_sub_type), r.ad_group.id,
                             enum_name(r.ad_group.type), r.metrics.impressions, r.metrics.clicks,
                             money(r.metrics.cost_micros)])
        except Exception as e:
            errors.append([cid, name, "youtube_adgroup", str(e)[:300]])

        # 4) network split
        try:
            for r in search(svc, cid, f"""
                SELECT campaign.id, campaign.advertising_channel_type, segments.ad_network_type,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM campaign WHERE {date_clause} AND metrics.impressions > 0"""):
                net.append([cid, name, r.campaign.id, enum_name(r.campaign.advertising_channel_type),
                            enum_name(r.segments.ad_network_type), r.metrics.impressions,
                            r.metrics.clicks, money(r.metrics.cost_micros)])
        except Exception as e:
            errors.append([cid, name, "network_12mo", str(e)[:300]])

        # 5) device split
        try:
            for r in search(svc, cid, f"""
                SELECT campaign.id, campaign.advertising_channel_type, segments.device,
                       metrics.impressions, metrics.clicks, metrics.cost_micros
                FROM campaign WHERE {date_clause} AND metrics.impressions > 0"""):
                dev.append([cid, name, r.campaign.id, enum_name(r.campaign.advertising_channel_type),
                            enum_name(r.segments.device), r.metrics.impressions,
                            r.metrics.clicks, money(r.metrics.cost_micros)])
        except Exception as e:
            errors.append([cid, name, "device_12mo", str(e)[:300]])

    out = args.out
    write(os.path.join(out, "google_campaign_12mo.csv"),
          ["customer_id", "account", "campaign_id", "campaign", "channel_type", "channel_sub_type",
           "status", "impressions", "clicks", "spend_usd"], camp)
    write(os.path.join(out, "google_youtube_adgroup_12mo.csv"),
          ["customer_id", "account", "campaign_id", "campaign", "channel_type", "channel_sub_type",
           "ad_group_id", "ad_group_type", "impressions", "clicks", "spend_usd"], ytag)
    write(os.path.join(out, "google_network_12mo.csv"),
          ["customer_id", "account", "campaign_id", "channel_type", "ad_network_type",
           "impressions", "clicks", "spend_usd"], net)
    write(os.path.join(out, "google_device_12mo.csv"),
          ["customer_id", "account", "campaign_id", "channel_type", "device",
           "impressions", "clicks", "spend_usd"], dev)

    # metro names
    names = {}
    ids = sorted(metro_ids)
    for i in range(0, len(ids), 200):
        chunk = ", ".join(f"'{x}'" for x in ids[i:i + 200])
        try:
            for r in search(svc, targets[0][0], f"""
                SELECT geo_target_constant.resource_name, geo_target_constant.name,
                       geo_target_constant.canonical_name, geo_target_constant.target_type
                FROM geo_target_constant WHERE geo_target_constant.resource_name IN ({chunk})"""):
                g = r.geo_target_constant
                names[g.resource_name] = (g.name, g.canonical_name)
        except Exception as e:
            errors.append(["-", "-", "metro_names", str(e)[:300]])
    for row in metro:
        n = names.get(row[3], ("", ""))
        row[4:4] = [n[0], n[1]]
    write(os.path.join(out, "google_metro_12mo.csv"),
          ["customer_id", "account", "channel_type", "metro_resource", "metro_name",
           "metro_canonical", "impressions", "clicks", "spend_usd"], metro)

    # 6) weekly unique-user frequency for video/display/demand-gen campaigns
    freq = []
    weeks = []
    d = date.fromisoformat(SINCE)
    while d <= date.fromisoformat(UNTIL):
        weeks.append((d, d + timedelta(days=6)))
        d += timedelta(days=7)
    for cid, camps in video_campaigns.items():
        ids_sql = ", ".join(str(c[0]) for c in camps)
        for ws, we in weeks:
            try:
                for r in search(svc, cid, f"""
                    SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
                           metrics.impressions, metrics.cost_micros, metrics.unique_users,
                           metrics.average_impression_frequency_per_user
                    FROM campaign
                    WHERE segments.date BETWEEN '{ws}' AND '{we}'
                      AND campaign.id IN ({ids_sql}) AND metrics.impressions > 0"""):
                    freq.append([cid, r.campaign.id, r.campaign.name,
                                 enum_name(r.campaign.advertising_channel_type), ws, we,
                                 r.metrics.impressions, money(r.metrics.cost_micros),
                                 r.metrics.unique_users,
                                 round(r.metrics.average_impression_frequency_per_user, 6)])
            except Exception as e:
                errors.append([cid, "-", f"video_weekly_freq {ws}", str(e)[:300]])
                break
            time.sleep(0.2)
    write(os.path.join(out, "google_video_weekly_frequency.csv"),
          ["customer_id", "campaign_id", "campaign", "channel_type", "week_start", "week_stop",
           "impressions", "spend_usd", "unique_users", "avg_impression_frequency_per_user"], freq)

    write(os.path.join(out, "google_errors.csv"), ["customer_id", "account", "query", "error"], errors)


if __name__ == "__main__":
    main()
