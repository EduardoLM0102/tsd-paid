import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "8634274092"

# include flag per action (from conversion_action resource)
flags = {}
for r in run_query(CID, """
    SELECT conversion_action.name,
           conversion_action.category,
           conversion_action.origin,
           conversion_action.counting_type,
           conversion_action.include_in_conversions_metric
    FROM conversion_action
"""):
    ca = r.get("conversion_action", {})
    flags[ca.get("name")] = {
        "incl": ca.get("include_in_conversions_metric"),
        "cat": ca.get("category"),
        "origin": ca.get("origin"),
        "counting": ca.get("counting_type"),
    }

# counted vs all, segmented by action name (must come FROM customer)
agg = {}
for r in run_query(CID, """
    SELECT segments.conversion_action_name,
           metrics.conversions,
           metrics.conversions_value,
           metrics.all_conversions,
           metrics.all_conversions_value
    FROM customer
    WHERE segments.date DURING LAST_30_DAYS
"""):
    s = r.get("segments", {})
    m = r.get("metrics", {})
    name = s.get("conversion_action_name")
    d = agg.setdefault(name, {"conv": 0.0, "val": 0.0, "all": 0.0, "allval": 0.0})
    d["conv"] += float(m.get("conversions") or 0)
    d["val"] += float(m.get("conversions_value") or 0)
    d["all"] += float(m.get("all_conversions") or 0)
    d["allval"] += float(m.get("all_conversions_value") or 0)

print("=" * 126)
print("LAST 30 DAYS — 'conv' = COUNTED (drives Smart Bidding).  'all' = reporting only.")
print("=" * 126)
print(f"{'NAME':<48} {'CATEGORY':<17} {'ORIGIN':<14} {'COUNTING':<14} {'conv':>6} {'value':>9} {'all':>6}")
print("-" * 126)

tot_c = tot_v = 0.0
for name, d in sorted(agg.items(), key=lambda x: -x[1]["conv"]):
    f = flags.get(name, {})
    tot_c += d["conv"]; tot_v += d["val"]
    mark = "  " if d["conv"] > 0 else "· "
    print(f"{mark}{str(name)[:46]:<46} {str(f.get('cat'))[:16]:<17} {str(f.get('origin'))[:13]:<14} "
          f"{str(f.get('counting'))[:13]:<14} {d['conv']:>6.1f} {d['val']:>9.2f} {d['all']:>6.1f}")

print("-" * 126)
print(f"  {'TOTAL COUNTED (the bidding signal)':<46} {'':<17} {'':<14} {'':<14} {tot_c:>6.1f} {tot_v:>9.2f}")
print("\n  Rows marked '·' fired but are NOT counted (reporting only).")
