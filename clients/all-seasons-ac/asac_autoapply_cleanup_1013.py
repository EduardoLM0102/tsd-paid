# APPLIED LIVE 2026-10-14 on Edu's go ("Execute that of All Seasons - GO"). Do NOT re-run with --live.
"""Staged 2026-10-13, applied 2026-10-14.
All Seasons AC (4467722415): undo Google auto-apply 'Add new keywords' run of 2026-10-11 and turn off auto-apply.
1) Pause the 156 BROAD keywords created 2026-10-11 by GOOGLE_ADS_RECOMMENDATIONS_SUBSCRIPTION (found via change_event).
2) Pause every ENABLED recommendation_subscription (auto-apply) on the account (SOP 7.8: auto-apply off).
   Types this SDK can't name (UNKNOWN) can't be mutated via API: they're printed for a UI pass.
Run from the skill scripts dir:  ./tsd.sh /abs/path/asac_autoapply_cleanup_1013.py          (validate only)
                                 ./tsd.sh /abs/path/asac_autoapply_cleanup_1013.py --live   (apply)
"""
import sys
sys.path.insert(0, ".")
from lib import run_query, init_client
from google.api_core import protobuf_helpers

CID = "4467722415"
LIVE = "--live" in sys.argv
client = init_client()

ce = run_query(CID, """
SELECT change_event.change_resource_name, change_event.client_type, change_event.resource_change_operation
FROM change_event
WHERE change_event.change_date_time >= '2026-10-11' AND change_event.change_date_time <= '2026-10-12 23:59:59'
  AND change_event.client_type = 'GOOGLE_ADS_RECOMMENDATIONS_SUBSCRIPTION'
  AND change_event.change_resource_type = 'AD_GROUP_CRITERION'
LIMIT 500""")
rns = sorted({r['change_event']['change_resource_name'] for r in ce if r['change_event'].get('resource_change_operation') == 'CREATE'})
inlist = ",".join("'%s'" % x for x in rns)
cur = run_query(CID, f"SELECT ad_group_criterion.resource_name, ad_group_criterion.status, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group_criterion.resource_name IN ({inlist})")
to_pause = [r['ad_group_criterion']['resource_name'] for r in cur if r['ad_group_criterion']['status'] == 'ENABLED']
print(f"auto-added keywords found: {len(rns)}, still ENABLED: {len(to_pause)}")

agc = client.get_service("AdGroupCriterionService")
ops = []
for rn in to_pause:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = rn
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, op.update._pb))
    ops.append(op)
for i in range(0, len(ops), 100):
    req = client.get_type("MutateAdGroupCriteriaRequest")
    req.customer_id = CID; req.operations.extend(ops[i:i+100]); req.validate_only = not LIVE
    agc.mutate_ad_group_criteria(request=req)
print(("PAUSED" if LIVE else "validated pause of"), len(ops), "keywords")

subs = run_query(CID, "SELECT recommendation_subscription.resource_name, recommendation_subscription.type, recommendation_subscription.status FROM recommendation_subscription")
rs = client.get_service("RecommendationSubscriptionService")
n = 0
for s in subs:
    sub = s['recommendation_subscription']
    if sub.get('status') != 'ENABLED': continue
    if 'UNKNOWN' in sub['resource_name']:
        print("SKIP (type unknown to this SDK, turn off in the UI: Recommendations > Auto-apply):", sub['resource_name']); continue
    op = client.get_type("RecommendationSubscriptionOperation")
    op.update.resource_name = sub['resource_name']
    op.update.status = client.enums.RecommendationSubscriptionStatusEnum.PAUSED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, op.update._pb))
    req = client.get_type("MutateRecommendationSubscriptionRequest")
    req.customer_id = CID; req.operations.append(op); req.validate_only = not LIVE
    rs.mutate_recommendation_subscription(request=req)
    n += 1
    print(("paused" if LIVE else "validated"), sub.get('type_', sub.get('type')), sub['resource_name'])
print(("PAUSED" if LIVE else "validated pause of"), n, "auto-apply subscriptions")
