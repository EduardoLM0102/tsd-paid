from h import *
print("=== PMax Plumbing campaign criteria ===")
q = """
SELECT campaign_criterion.criterion_id, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type,
       campaign_criterion.location.geo_target_constant, campaign_criterion.status, campaign_criterion.display_name
FROM campaign_criterion
WHERE campaign.id = 23590336249
"""
for r in run_query(CID,q):
    c=r["campaign_criterion"]; print(c.get("type_") or c.get("type"), "neg=",c.get("negative"), c.get("keyword"), c.get("location"), c.get("display_name"), c.get("status"))
print("\n=== shared sets ===")
q = """
SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.status, shared_set.member_count, shared_set.reference_count
FROM shared_set
"""
for r in run_query(CID,q): print(json.dumps(r, default=str))
print("\n=== campaign_shared_set for PMax ===")
q = """
SELECT campaign.name, shared_set.name, campaign_shared_set.status
FROM campaign_shared_set
WHERE campaign.status != 'REMOVED'
"""
for r in run_query(CID,q): print(r["campaign"]["name"], "->", r["shared_set"]["name"], r["campaign_shared_set"].get("status"))
