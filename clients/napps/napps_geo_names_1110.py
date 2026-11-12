import sys
sys.path.insert(0, ".")
from lib import run_query
for r in run_query("9509605037", "SELECT geo_target_constant.id, geo_target_constant.canonical_name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.id IN (9053151,9059512,1026429,1026468,1026558,1026627,1026224,1026336,1026428,1026450,1026527,1026572,1026597,1026855)"):
    g = r.get("geo_target_constant") or r.get("geoTargetConstant"); print(g["id"], g["canonical_name"], g.get("target_type"))
for r in run_query("9509605037", "SELECT segments.conversion_action_name, campaign.name, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2026-08-12' AND '2026-11-09' AND segments.conversion_action_name = 'Click to call' AND metrics.all_conversions > 0"):
    print("tap90d:", r["campaign"]["name"], r["metrics"])
