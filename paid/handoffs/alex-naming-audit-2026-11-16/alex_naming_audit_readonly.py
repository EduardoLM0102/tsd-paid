#!/usr/bin/env python3
"""READ-ONLY audit for Alex's 2026-11-14 naming / portal questions.
Run from the google-ads-ratos scripts dir via:  ./tsd.sh /abs/path/alex_naming_audit.py --out DIR
Nothing here mutates anything.
"""
import argparse, csv, json, os, sys, time
sys.path.insert(0, ".")
from lib import init_client, run_query

MCC = "4155514468"
Y0, Y1 = "2026-01-01", "2026-11-15"
CALLS0 = "2026-08-01"


def g(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def safe(cid, q, errors, tag):
    try:
        return run_query(cid, q)
    except (Exception, SystemExit) as e:  # run_query sys.exits on API errors
        msg = str(e).replace("\n", " ")[:300]
        errors.append([cid, tag, msg])
        print(f"  !! {cid} {tag}: {msg[:160]}", file=sys.stderr)
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="", help="comma list of customer ids to restrict to")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    errors = []

    acc = run_query(MCC, """
        SELECT customer_client.id, customer_client.descriptive_name, customer_client.status,
               customer_client.manager, customer_client.level
        FROM customer_client""")
    accounts = []
    for r in acc:
        c = r["customer_client"]
        if c.get("manager"):
            continue
        if c.get("status") != "ENABLED":
            continue
        accounts.append((str(c["id"]), c.get("descriptive_name", "")))
    if a.only:
        keep = set(a.only.split(","))
        accounts = [x for x in accounts if x[0] in keep]
    print(f"{len(accounts)} client accounts", file=sys.stderr)
    with open(os.path.join(a.out, "accounts.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["customer_id", "name"]); w.writerows(accounts)

    out = {k: [] for k in ["campaigns", "first_spend", "customer", "call_assets", "asset_sets",
                           "pmax_brand", "brand_lists", "mix_keywords", "video_conv", "call_view"]}

    for cid, name in accounts:
        print(f"-- {cid} {name}", file=sys.stderr)
        # 1. campaigns that spent in 2026
        rows = safe(cid, f"""
            SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status,
                   campaign.advertising_channel_type, campaign.advertising_channel_sub_type,
                   campaign.bidding_strategy_type, campaign.tracking_url_template,
                   campaign.final_url_suffix, metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{Y0}' AND '{Y1}' AND metrics.cost_micros > 0""", errors, "campaigns")
        for r in rows:
            c, m = r["campaign"], r.get("metrics", {})
            out["campaigns"].append([cid, name, c["id"], c["name"], c.get("status"), c.get("primary_status"),
                                     c.get("advertising_channel_type"), c.get("advertising_channel_sub_type", ""),
                                     c.get("bidding_strategy_type"), c.get("tracking_url_template", ""),
                                     c.get("final_url_suffix", ""),
                                     round(int(m.get("cost_micros", 0)) / 1e6, 2), m.get("conversions", 0)])
        if not rows:
            continue
        # 2. first spend date per campaign (daily rows, cost>0) since 2025
        rows = safe(cid, f"""
            SELECT campaign.id, segments.date, metrics.cost_micros
            FROM campaign
            WHERE segments.date BETWEEN '2025-01-01' AND '{Y1}' AND metrics.cost_micros > 0""", errors, "first_spend")
        first = {}
        for r in rows:
            k = r["campaign"]["id"]; d = r["segments"]["date"]
            if k not in first or d < first[k]:
                first[k] = d
        for k, d in first.items():
            out["first_spend"].append([cid, k, d])
        # 3. customer settings
        rows = safe(cid, """
            SELECT customer.id, customer.descriptive_name, customer.auto_tagging_enabled,
                   customer.tracking_url_template, customer.final_url_suffix,
                   customer.call_reporting_setting.call_reporting_enabled,
                   customer.call_reporting_setting.call_conversion_reporting_enabled
            FROM customer""", errors, "customer")
        for r in rows:
            c = r["customer"]; crs = c.get("call_reporting_setting", {})
            out["customer"].append([cid, name, c.get("auto_tagging_enabled", False),
                                    c.get("tracking_url_template", ""), c.get("final_url_suffix", ""),
                                    crs.get("call_reporting_enabled", ""), crs.get("call_conversion_reporting_enabled", "")])
        # 4. call assets (campaign / customer / ad group level)
        for level, tbl, extra in [("campaign", "campaign_asset", "campaign.id, campaign.name, campaign_asset.status"),
                                  ("customer", "customer_asset", "customer_asset.status"),
                                  ("ad_group", "ad_group_asset", "campaign.id, campaign.name, ad_group.name, ad_group_asset.status")]:
            rows = safe(cid, f"""
                SELECT {extra}, asset.id, asset.call_asset.phone_number, asset.call_asset.country_code,
                       asset.call_asset.call_conversion_reporting_state
                FROM {tbl}
                WHERE {tbl}.field_type = 'CALL' AND {tbl}.status != 'REMOVED'""", errors, f"call_{level}")
            for r in rows:
                ca = r["asset"].get("call_asset", {})
                out["call_assets"].append([cid, name, level, g(r, "campaign", "id", default=""),
                                           g(r, "campaign", "name", default=""), g(r, "ad_group", "name", default=""),
                                           g(r, tbl, "status", default=""), r["asset"]["id"],
                                           ca.get("phone_number", ""), ca.get("country_code", ""),
                                           ca.get("call_conversion_reporting_state", "")])
        # 4b. location asset sets (GBP-linked numbers can't carry gclid)
        rows = safe(cid, """
            SELECT campaign.id, campaign.name, asset_set.id, asset_set.type, campaign_asset_set.status
            FROM campaign_asset_set WHERE campaign_asset_set.status != 'REMOVED'""", errors, "asset_sets")
        for r in rows:
            out["asset_sets"].append([cid, name, r["campaign"]["id"], r["campaign"]["name"],
                                      r["asset_set"]["id"], r["asset_set"].get("type", "")])
        # 5. PMax brand exclusions (negative campaign_criterion brand_list) + brand lists
        rows = safe(cid, """
            SELECT campaign.id, campaign.name, campaign.status, campaign_criterion.negative,
                   campaign_criterion.brand_list.shared_set, campaign_criterion.status
            FROM campaign_criterion
            WHERE campaign_criterion.type = 'BRAND_LIST'""", errors, "pmax_brand")
        for r in rows:
            cc = r["campaign_criterion"]
            out["pmax_brand"].append([cid, name, r["campaign"]["id"], r["campaign"]["name"], r["campaign"].get("status"),
                                      cc.get("negative", False), g(cc, "brand_list", "shared_set", default=""), cc.get("status", "")])
        rows = safe(cid, """
            SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.status, shared_set.member_count
            FROM shared_set WHERE shared_set.type = 'BRANDS' AND shared_set.status != 'REMOVED'""", errors, "brand_lists")
        for r in rows:
            s = r["shared_set"]
            out["brand_lists"].append([cid, name, s["id"], s.get("name", ""), s.get("member_count", "")])
        # 6. keywords of *_Mix campaigns
        rows = safe(cid, """
            SELECT campaign.id, campaign.name, ad_group.name, ad_group_criterion.keyword.text,
                   ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.negative
            FROM ad_group_criterion
            WHERE ad_group_criterion.type = 'KEYWORD' AND campaign.name LIKE '%Mix%'""", errors, "mix_keywords")
        for r in rows:
            k = r["ad_group_criterion"]
            out["mix_keywords"].append([cid, name, r["campaign"]["id"], r["campaign"]["name"], r["ad_group"]["name"],
                                        k["keyword"]["text"], k["keyword"].get("match_type", ""), k.get("status", ""),
                                        k.get("negative", False)])
        # 7. conversions by action on VIDEO / DEMAND_GEN campaigns in 2026
        rows = safe(cid, f"""
            SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
                   segments.conversion_action_name, segments.conversion_action_category, metrics.conversions
            FROM campaign
            WHERE campaign.advertising_channel_type IN ('VIDEO','DEMAND_GEN')
              AND segments.date BETWEEN '{Y0}' AND '{Y1}' AND metrics.conversions > 0""", errors, "video_conv")
        for r in rows:
            s = r["segments"]
            out["video_conv"].append([cid, name, r["campaign"]["id"], r["campaign"]["name"],
                                      r["campaign"]["advertising_channel_type"], s.get("conversion_action_name", ""),
                                      s.get("conversion_action_category", ""), r["metrics"].get("conversions", 0)])
        # 8. Google-tracked calls (call assets / call-only) since Aug: attributed by Google, not CallRail
        rows = safe(cid, f"""
            SELECT campaign.id, campaign.name, call_view.type, call_view.call_tracking_display_location,
                   call_view.call_status, call_view.call_duration_seconds, call_view.start_call_date_time
            FROM call_view
            WHERE call_view.start_call_date_time BETWEEN '{CALLS0} 00:00:00' AND '{Y1} 23:59:59'""", errors, "call_view")
        for r in rows:
            v = r["call_view"]
            out["call_view"].append([cid, name, r["campaign"]["id"], r["campaign"]["name"], v.get("type", ""),
                                     v.get("call_tracking_display_location", ""), v.get("call_status", ""),
                                     v.get("call_duration_seconds", 0), v.get("start_call_date_time", "")])
        time.sleep(0.2)

    headers = {
        "campaigns": ["customer_id", "account", "campaign_id", "campaign", "status", "primary_status", "channel", "sub_type",
                      "bidding", "tracking_template", "final_url_suffix", "cost_2026", "conversions_2026"],
        "first_spend": ["customer_id", "campaign_id", "first_spend_date"],
        "customer": ["customer_id", "account", "auto_tagging", "tracking_template", "final_url_suffix",
                     "call_reporting", "call_conv_reporting"],
        "call_assets": ["customer_id", "account", "level", "campaign_id", "campaign", "ad_group", "link_status", "asset_id",
                        "phone", "country", "call_conv_state"],
        "asset_sets": ["customer_id", "account", "campaign_id", "campaign", "asset_set_id", "asset_set_type"],
        "pmax_brand": ["customer_id", "account", "campaign_id", "campaign", "campaign_status", "negative", "shared_set", "crit_status"],
        "brand_lists": ["customer_id", "account", "shared_set_id", "name", "member_count"],
        "mix_keywords": ["customer_id", "account", "campaign_id", "campaign", "ad_group", "keyword", "match", "status", "negative"],
        "video_conv": ["customer_id", "account", "campaign_id", "campaign", "channel", "conversion_action", "category", "conversions"],
        "call_view": ["customer_id", "account", "campaign_id", "campaign", "type", "display_location", "status", "duration_s", "start"],
    }
    for k, rows in out.items():
        with open(os.path.join(a.out, f"{k}.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(headers[k]); w.writerows(rows)
        print(f"  wrote {len(rows):>6} rows -> {k}.csv", file=sys.stderr)
    with open(os.path.join(a.out, "errors.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["customer_id", "step", "error"]); w.writerows(errors)
    print(f"{len(errors)} errors", file=sys.stderr)


if __name__ == "__main__":
    main()
