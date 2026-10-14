#!/usr/bin/env python3
"""
H5a + "show the ads to the right people" (Edu, 2026-10-08). YouTube campaigns 24120440530 (SA VideoViews), 24120482524 (NB Awareness).
  1. Content exclusion BRAND_SUITABILITY_CONTENT_FOR_FAMILIES ("content suitable for families": made-for-kids / family) on both.
  2. Negative YouTube channels: every kids-named channel with >= $5 spend (Aug 8 – Oct 7) in either campaign, on both campaigns.
Not done on purpose: excluding "age undetermined" (44% SA / 25% NB). On connected TVs (84% of spend) that's mostly shared household
screens, i.e. the homeowner household; excluding it would cut most of the TV inventory. Ages 18–24 are already excluded.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, re, argparse
from collections import defaultdict
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"; C = f"customers/{CID}"; YT = ["24120440530", "24120482524"]
KIDS = re.compile(r"disney jr|bluey|ms ?rachel|super simple|plim plim|cocomelon|peppa|blippi|pinkfong|baby shark|toddler|nursery|chuchu|little baby bum|moonbug|paw patrol|sesame|nick jr|mickey|gabby|kids|kid's|niños|ninos|infantil|bebé|bebe|baby|cartoon|lullab|spidey|hey bear|morphle|bebefinn|lellobee|toys|juguetes|vlad|ryan's|kidz|songs for|phonics", re.I)
client = init_client(); E = client.enums


def kids_channels():
    spend = defaultdict(float); names = {}
    for r in run_query(CID, f"""SELECT campaign.id, group_placement_view.placement, group_placement_view.display_name, group_placement_view.placement_type, metrics.cost_micros
FROM group_placement_view WHERE campaign.id IN ({','.join(YT)}) AND segments.date BETWEEN '2026-08-08' AND '2026-10-07' AND metrics.impressions > 0"""):
        g = r["group_placement_view"]
        if str(g.get("placement_type")) == "YOUTUBE_CHANNEL" and KIDS.search(g.get("display_name", "")) and g.get("placement"):
            spend[g["placement"]] += float(r["metrics"]["cost_micros"]) / 1e6; names[g["placement"]] = g.get("display_name", "")
    return {ch: (names[ch], s) for ch, s in spend.items() if s >= 5}


def run(validate):
    chans = kids_channels()
    print(f"kids channels with >= $5: {len(chans)} (${sum(s for _, s in chans.values()):,.0f}); top: " +
          ", ".join(f"{n[:22]} ${s:.0f}" for n, s in sorted(chans.values(), key=lambda x: -x[1])[:10]))
    # Video campaign criteria are read-only via the API (MUTATE_NOT_ALLOWED) and the families label is invalid at campaign level
    # (INVALID_EXCLUDED_CATEGORY), so both go in as ACCOUNT-LEVEL exclusions (customer_negative_criterion). That covers both
    # YouTube campaigns and the YouTube inventory PMax uses.
    have = run_query(CID, """SELECT customer_negative_criterion.type, customer_negative_criterion.youtube_channel.channel_id,
customer_negative_criterion.content_label.type FROM customer_negative_criterion""")
    have_ch = {r["customer_negative_criterion"].get("youtube_channel", {}).get("channel_id") for r in have}
    have_lab = {str(r["customer_negative_criterion"].get("content_label", {}).get("type_")) for r in have}
    print("existing account-level exclusions:", len(have), "| labels:", sorted(x for x in have_lab if x != "None"))
    ops = []
    if "BRAND_SUITABILITY_CONTENT_FOR_FAMILIES" not in have_lab and INCLUDE_LABEL:
        o = client.get_type("MutateOperation"); cn = o.customer_negative_criterion_operation.create
        cn.content_label.type_ = E.ContentLabelTypeEnum.BRAND_SUITABILITY_CONTENT_FOR_FAMILIES; ops.append(o)
    for ch in chans:
        if ch not in have_ch:
            o = client.get_type("MutateOperation"); cn = o.customer_negative_criterion_operation.create
            cn.youtube_channel.channel_id = ch; ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = validate
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("VALIDATE-ONLY OK" if validate else "APPLIED") + f": {len(ops)} account-level exclusions (families label: {INCLUDE_LABEL})")
    if not validate:
        rows = run_query(CID, """SELECT customer_negative_criterion.type, customer_negative_criterion.youtube_channel.channel_id,
customer_negative_criterion.content_label.type FROM customer_negative_criterion""")
        print("READ-BACK account exclusions: channels", sum(1 for r in rows if r["customer_negative_criterion"].get("youtube_channel", {}).get("channel_id") in chans),
              "of", len(chans), "| labels", sorted({str(r["customer_negative_criterion"].get("content_label", {}).get("type_")) for r in rows} - {"None"}))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); ap.add_argument("--no-label", action="store_true"); a = ap.parse_args()
    INCLUDE_LABEL = not a.no_label
    run(validate=not a.apply)
