from h import *
for r in run_query(CID,"SELECT geo_target_constant.id, geo_target_constant.canonical_name FROM geo_target_constant WHERE geo_target_constant.canonical_name = 'Longview,Texas,United States'"): print(r["geo_target_constant"]["id"], r["geo_target_constant"]["canonical_name"])
