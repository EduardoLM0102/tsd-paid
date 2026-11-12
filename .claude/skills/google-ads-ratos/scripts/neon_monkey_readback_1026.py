"""Read-only: confirm neon_monkey_apply_1026.py landed."""
from collections import Counter
from lib import run_query
cid = "7953905280"
for r in run_query(cid, "SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id=23825900343 AND ad_group_criterion.keyword.text='remove tree stump from yard'"):
    a = r["ad_group_criterion"]; print("NB kw:", a["keyword"]["text"], a["keyword"].get("match_type_", a["keyword"].get("match_type")), a["status"])
print("NB negatives:", sorted(f"{r['campaign_criterion']['keyword']['text']}/{r['campaign_criterion']['keyword'].get('match_type_', r['campaign_criterion']['keyword'].get('match_type'))}" for r in run_query(cid, "SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign.id=23825900343 AND campaign_criterion.type='KEYWORD' AND campaign_criterion.negative=TRUE")))
for r in run_query(cid, "SELECT ad_group.cpc_bid_micros FROM ad_group WHERE ad_group.id=193951349406"):
    print("Branded ad group bid: $%.2f" % (int(r["ad_group"]["cpc_bid_micros"]) / 1e6))
rows = run_query(cid, "SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id=21225221220 AND campaign_criterion.type IN ('LOCATION','PROXIMITY')")
cnt = Counter((r["campaign_criterion"].get("type_", r["campaign_criterion"].get("type")), bool(r["campaign_criterion"].get("negative"))) for r in rows)
print("PMax geo criteria:", dict(cnt))
print("PMax negatives:", sorted(r["campaign_criterion"]["location"]["geo_target_constant"] for r in rows if r["campaign_criterion"].get("negative")))
print("Fort Worth city 1026411 still on PMax:", any(r["campaign_criterion"].get("location", {}).get("geo_target_constant") == "geoTargetConstants/1026411" for r in rows))
for r in run_query(cid, "SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign_budget.amount_micros FROM campaign WHERE campaign.status='ENABLED'"):
    c = r["campaign"]; print(" ", c["id"], c["name"][:36], c["primary_status"], c.get("primary_status_reasons"), "$%.0f/d" % (int(r["campaign_budget"]["amount_micros"]) / 1e6))
