"""H5 (read-only): who/where the YouTube ads reach. Kids channels by spend, age, parental status, device."""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID = "1051843378"; YT = {"24120440530": "SA VideoViews", "24120482524": "NB Awareness"}; S, U = "2026-08-08", "2026-10-07"
f = lambda x: float(x or 0)
KIDS = re.compile(r"disney jr|bluey|ms ?rachel|super simple|plim plim|cocomelon|peppa|blippi|pinkfong|baby shark|toddler|nursery|chuchu|little baby bum|moonbug|paw patrol|sesame|nick jr|mickey|gabby|kids|kid's|niños|ninos|infantil|bebé|bebe|baby|cartoon|lullab|spidey|hey bear|morphle|bebefinn|lellobee|toys|juguetes|vlad|niki|diana|ryan's|kidz|songs for|abc|phonics", re.I)
for camp, label in YT.items():
    rows = run_query(CID, f"""SELECT campaign.id, group_placement_view.placement, group_placement_view.display_name, group_placement_view.placement_type, metrics.cost_micros, metrics.impressions
FROM group_placement_view WHERE campaign.id = {camp} AND segments.date BETWEEN '{S}' AND '{U}' AND metrics.impressions > 0""")
    tot = sum(f(r["metrics"]["cost_micros"]) for r in rows) / 1e6
    kids = [r for r in rows if str(r["group_placement_view"].get("placement_type")) == "YOUTUBE_CHANNEL" and KIDS.search(r["group_placement_view"].get("display_name", ""))]
    ks = sum(f(r["metrics"]["cost_micros"]) for r in kids) / 1e6
    print(f"== {label}: ${tot:,.0f} total; kids-looking YouTube channels: {len(kids)} channels, ${ks:,.0f} ({ks / tot * 100:.0f}%) by name match")
    for r in sorted(kids, key=lambda r: -f(r["metrics"]["cost_micros"]))[:12]:
        g = r["group_placement_view"]; print(f"     ${f(r['metrics']['cost_micros']) / 1e6:5,.0f}  {g.get('display_name', '')[:45]:45s} {g.get('placement')}")
for view, field in (("age_range_view", "ad_group_criterion.age_range.type"), ("parental_status_view", "ad_group_criterion.parental_status.type"), ("gender_view", "ad_group_criterion.gender.type")):
    agg = defaultdict(lambda: defaultdict(float))
    for r in run_query(CID, f"SELECT campaign.id, {field}, metrics.cost_micros FROM {view} WHERE campaign.id IN ({','.join(YT)}) AND segments.date BETWEEN '{S}' AND '{U}'"):
        key = list(r["ad_group_criterion"].values())[0]; key = str(list(key.values())[0]) if isinstance(key, dict) else str(key)
        agg[YT[r["campaign"]["id"]]][key] += f(r["metrics"]["cost_micros"]) / 1e6
    print(f"\n== {view}")
    for c, d in agg.items():
        t = sum(d.values()) or 1
        print(f"   {c:14s} " + ", ".join(f"{k.replace('AGE_RANGE_', '').replace('PARENTAL_STATUS_', '').replace('GENDER_', '')} {v / t * 100:.0f}%" for k, v in sorted(d.items())))
dev = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, f"SELECT campaign.id, segments.device, metrics.cost_micros FROM campaign WHERE campaign.id IN ({','.join(YT)}) AND segments.date BETWEEN '{S}' AND '{U}'"):
    dev[YT[r["campaign"]["id"]]][str(r["segments"]["device"])] += f(r["metrics"]["cost_micros"]) / 1e6
print("\n== device"); [print(f"   {c:14s} " + ", ".join(f"{k} {v / (sum(d.values()) or 1) * 100:.0f}%" for k, v in sorted(d.items(), key=lambda x: -x[1]))) for c, d in dev.items()]
print("\n== current exclusions / targeting on the YouTube campaigns")
for r in run_query(CID, f"""SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.content_label.type, campaign_criterion.youtube_channel.channel_id
FROM campaign_criterion WHERE campaign.id IN ({','.join(YT)}) AND campaign_criterion.type IN ('CONTENT_LABEL', 'YOUTUBE_CHANNEL', 'PLACEMENT', 'KEYWORD', 'TOPIC')"""):
    print("   ", YT[r["campaign"]["id"]], r["campaign_criterion"])
for r in run_query(CID, f"""SELECT campaign.id, ad_group.name, ad_group_criterion.type, ad_group_criterion.negative FROM ad_group_criterion
WHERE campaign.id IN ({','.join(YT)}) AND ad_group_criterion.status = 'ENABLED'"""):
    print("   adgroup", YT[r["campaign"]["id"]], r["ad_group"]["name"], r["ad_group_criterion"].get("type"), "neg" if r["ad_group_criterion"].get("negative") else "")
