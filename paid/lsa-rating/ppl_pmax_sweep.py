# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path>. Weekly sweep (fu-135): which MCC accounts have Google's
# 'Pay-per-lead PMax' (asset group xcat:*) and which still run a classic LOCAL_SERVICES campaign. Detection per tsd-lsa-ppl-pmax-migration.md.
import sys; sys.path.insert(0, ".")
from lib import run_query
MCC = "4155514468"
accts = [(r["customer_client"]["id"], r["customer_client"].get("descriptive_name", "")) for r in run_query(MCC,
    "SELECT customer_client.id, customer_client.descriptive_name, customer_client.status, customer_client.manager FROM customer_client WHERE customer_client.status = 'ENABLED' AND customer_client.manager = FALSE")]
print(len(accts), "enabled accounts")
for cid, name in accts:
    cid = str(cid)
    try:
        ppl = run_query(cid, "SELECT campaign.id, campaign.name, campaign.status, campaign.start_date_time, campaign.bidding_strategy_type, asset_group.name FROM asset_group WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX' AND asset_group.name LIKE 'xcat:%'")
        lsa = run_query(cid, "SELECT campaign.id, campaign.status, campaign.bidding_strategy_type FROM campaign WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES' AND campaign.status != 'REMOVED'")
    except Exception as e:
        print(f"{cid} {name[:35]:<35} ERROR {str(e)[:80]}"); continue
    if not ppl and not lsa: continue
    p = "; ".join(f"PPL {r['campaign']['id']} {r['campaign']['status']} start {str(r['campaign'].get('start_date_time',''))[:10]} {r['campaign'].get('bidding_strategy_type')}" for r in {r['campaign']['id']: r for r in ppl}.values())
    l = "; ".join(f"LSA {r['campaign']['id']} {r['campaign']['status']} {r['campaign'].get('bidding_strategy_type')}" for r in lsa)
    print(f"{cid} {name[:35]:<35} {p} | {l}")
