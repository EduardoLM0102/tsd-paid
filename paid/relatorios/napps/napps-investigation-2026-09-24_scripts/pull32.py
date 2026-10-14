from h import *
q="""SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.negative
FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION' AND campaign.status IN ('ENABLED') """
ids=set(); by={}
for r in run_query(CID,q):
    g=r["campaign_criterion"]["location"]["geo_target_constant"]; ids.add(g); by.setdefault(r["campaign"]["name"],[]).append((g, r["campaign_criterion"].get("negative")))
print({k:len(v) for k,v in by.items()})
# resolve names
names={}
for g in ids|{f"geoTargetConstants/{x}" for x in ["1026224","1026336","1026428","1026429","1026450","1026527","1026572","1026597","1026855","9053151","9059512"]}:
    gid=g.split("/")[-1]
    q2=f"SELECT geo_target_constant.id, geo_target_constant.name, geo_target_constant.canonical_name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.id = {gid}"
    for r in run_query(CID,q2): names[g]=r["geo_target_constant"].get("canonical_name")
for k,v in by.items():
    print("\n",k); print("   ", "; ".join(f"{names.get(g,g)}{' (NEG)' if n else ''}" for g,n in v))
# PMax campaign
q3="""SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign_criterion.type='LOCATION' AND campaign.id = 23590336249"""
print("\nPMax Plumbing:", "; ".join(names.get(r["campaign_criterion"]["location"]["geo_target_constant"], r["campaign_criterion"]["location"]["geo_target_constant"]) for r in run_query(CID,q3)))
