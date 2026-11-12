# READ-ONLY. Napps 11-10 follow-up: what was the NB Plumbing 'Click to call' conversion, which kw matched the competitor terms, city names.
import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "9509605037"; HT, PL = "24049055193", "23819717682"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
WIN = "segments.date BETWEEN '2026-11-03' AND '2026-11-09'"
print("== conv by date/action (NB)")
for r in q(f"""SELECT campaign.id, segments.date, segments.conversion_action, segments.conversion_action_name, metrics.all_conversions, metrics.conversions
  FROM campaign WHERE {WIN} AND campaign.id IN ({HT},{PL}) AND metrics.all_conversions > 0"""):
    print(" ", r["campaign"]["id"], r["segments"]["date"], r["segments"]["conversion_action_name"], r["segments"]["conversion_action"], r["metrics"])
print("== conversion actions")
for r in q("""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.status,
  conversion_action.primary_for_goal, conversion_action.counting_type, conversion_action.phone_call_duration_seconds, conversion_action.origin
  FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""):
    print(" ", r["conversion_action"])
print("== campaign goals NB")
for r in q(f"""SELECT campaign.id, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
  FROM campaign_conversion_goal WHERE campaign.id IN ({HT},{PL}) AND campaign_conversion_goal.biddable = TRUE"""):
    print(" ", r["campaign"]["id"], r["campaign_conversion_goal"])
print("== search term -> keyword (NB, clicks>0)")
for r in q(f"""SELECT campaign.id, search_term_view.search_term, segments.keyword.info.text, segments.keyword.info.match_type, metrics.clicks, metrics.cost_micros
  FROM search_term_view WHERE {WIN} AND campaign.id IN ({HT},{PL}) AND metrics.clicks > 0"""):
    k = r["segments"].get("keyword", {}).get("info", {})
    print(" ", "HT" if r["campaign"]["id"]==HT else "PL", r["search_term_view"]["search_term"], "<-", k.get("text"), k.get("match_type"), r["metrics"].get("clicks"), f"${M(r['metrics'].get('cost_micros')):.2f}")
print("== geo names")
ids = "1026855,1026572,1026428,1026224,1026597,1026527,1026198,9175440,1026450,9214985,1026282,1026336,9221494"
for r in q(f"SELECT geo_target_constant.id, geo_target_constant.canonical_name FROM geo_target_constant WHERE geo_target_constant.id IN ({ids})"):
    print(" ", r["geoTargetConstant"]["id"] if "geoTargetConstant" in r else r["geo_target_constant"]["id"], (r.get("geoTargetConstant") or r.get("geo_target_constant"))["canonical_name"])
