"""Checklist G1 (read-only): location targeting per campaign vs the LSA service area, plus where Search leads/clicks come from."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
f = lambda x: float(x or 0)
PPC = "1051843378"
ACCTS = {"1051843378": "PPC account", "7261668241": "LSA [1] Electrician", "6621969129": "LSA [2] HVAC"}
names = {}
def name_of(rn):
    return names.get(rn, rn)
def resolve(rns, cid):
    ids = [r.split("/")[-1] for r in rns if r and r not in names]
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        if chunk:
            for r in run_query(cid, f"SELECT geo_target_constant.resource_name, geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(chunk)})"):
                g = r["geo_target_constant"]; names[g["resource_name"]] = f"{g['name']} ({str(g.get('target_type', ''))[:6].lower()})"

targets = {}
for cid, label in ACCTS.items():
    rows = run_query(cid, """SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.geo_target_type_setting.positive_geo_target_type,
campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius,
campaign_criterion.proximity.radius_units, campaign_criterion.proximity.address.city_name FROM campaign_criterion
WHERE campaign.status = 'ENABLED' AND campaign_criterion.type IN ('LOCATION', 'PROXIMITY')""")
    resolve([r["campaign_criterion"].get("location", {}).get("geo_target_constant") for r in rows], cid)
    by = defaultdict(lambda: {"inc": [], "exc": [], "mode": "", "ch": ""})
    for r in rows:
        c = r["campaign"]; cc = r["campaign_criterion"]; d = by[(cid, c["name"])]
        d["mode"] = str(c.get("geo_target_type_setting", {}).get("positive_geo_target_type", "")); d["ch"] = str(c.get("advertising_channel_type"))
        if str(cc.get("type")) == "PROXIMITY":
            p = cc.get("proximity", {}); item = f"radius {p.get('radius')} {str(p.get('radius_units', '')).lower()} around {p.get('address', {}).get('city_name', '?')}"
        else:
            item = name_of(cc.get("location", {}).get("geo_target_constant"))
        d["exc" if cc.get("negative") else "inc"].append(item)
    for (acct, cname), d in by.items():
        targets[(acct, cname)] = d
        print(f"\n[{ACCTS[acct]}] {cname}  ({d['ch']}, mode {d['mode']})\n   targets {len(d['inc'])}: {sorted(d['inc'])[:60]}")
        if d["exc"]: print(f"   excluded: {sorted(d['exc'])[:20]}")

print("\n\n== PPC Search + PMax clicks/cost by user city, last 60 days (where demand actually comes from)")
rows = run_query(PPC, """SELECT campaign.name, campaign.advertising_channel_type, segments.geo_target_city, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM geographic_view WHERE campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX') AND segments.date BETWEEN '2026-08-08' AND '2026-10-07' AND metrics.clicks > 0""")
resolve([r["segments"].get("geo_target_city") for r in rows], PPC)
agg = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))
for r in rows:
    c = r["campaign"]["name"]; key = "HVAC" if "HVAC" in c else "Plumbing" if "Plumbing" in c else "Electrical" if "Electrical" in c else "Branded"
    x = agg[name_of(r["segments"].get("geo_target_city"))][key]; m = r["metrics"]
    x[0] += f(m.get("clicks")); x[1] += f(m.get("cost_micros")) / 1e6; x[2] += f(m.get("all_conversions"))
print(f"   {'city':30s} {'Electrical':>18s} {'HVAC':>18s} {'Plumbing':>18s} {'Branded':>14s}")
for city, d in sorted(agg.items(), key=lambda x: -sum(v[1] for v in x[1].values()))[:25]:
    print(f"   {city[:30]:30s} " + " ".join(f"{d[k][0]:5.0f}clk ${d[k][1]:6,.0f}" if k in d else f"{'-':>18s}" for k in ("Electrical", "HVAC", "Plumbing")) + (f"  {d['Branded'][0]:4.0f}clk ${d['Branded'][1]:5,.0f}" if "Branded" in d else "            -"))
