import sys
sys.path.insert(0, ".")
from collections import defaultdict
from lib import run_query
CID = "7953905280"
NB, BR, PMAX = "23825900343", "23739724064", "21225221220"
LIVE = f"{NB}, {BR}, {PMAX}"
TAG = {NB: "NB", BR: "BR", PMAX: "PMAX"}
def f(m, k, t=float):
    v = m.get(k, 0) or 0
    return t(v)
def hdr(t): print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)
def safe(label, fn):
    try: fn()
    except Exception as e: print(f"  !! {label} failed: {str(e)[:500]}")
def g(d, k): return d.get(k, d.get(k + "_"))

def conv():
    hdr("1) CONVERSION ACTIONS (enabled)")
    q = """SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category,
           conversion_action.primary_for_goal, conversion_action.counting_type, conversion_action.include_in_conversions_metric,
           conversion_action.phone_call_duration_seconds, conversion_action.origin, conversion_action.status
           FROM conversion_action WHERE conversion_action.status = 'ENABLED'"""
    for r in run_query(CID, q):
        c = r["conversion_action"]
        print(f"  {c['name'][:50]:50s} {g(c,'type'):26s} {c['category']:20s} primary={c.get('primary_for_goal')} incl={c.get('include_in_conversions_metric')} "
              f"count={c.get('counting_type')} dur={c.get('phone_call_duration_seconds','-')} origin={c.get('origin')}")
    hdr("1b) BIDDABLE GOALS per campaign")
    q = f"""SELECT campaign.id, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable
            FROM campaign_conversion_goal WHERE campaign.id IN ({LIVE})"""
    for r in run_query(CID, q):
        x = r["campaign_conversion_goal"]
        if x.get("biddable"): print(f"  {TAG[r['campaign']['id']]:5s} {x['category']:22s} {x['origin']}")

def ads():
    hdr("5) ADS (enabled)")
    q = f"""SELECT campaign.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad_strength,
           ad_group_ad.policy_summary.approval_status, ad_group_ad.primary_status, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
           FROM ad_group_ad WHERE campaign.id IN ({NB}, {BR}) AND ad_group_ad.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS"""
    for r in run_query(CID, q):
        a, m = r["ad_group_ad"], r["metrics"]
        imp, clk = f(m, "impressions", int), f(m, "clicks", int)
        print(f"  {TAG[r['campaign']['id']]:3s} {r['ad_group']['name'][:16]:16s} {a.get('ad_strength'):9s} {a.get('policy_summary',{}).get('approval_status'):10s} "
              f"{a.get('primary_status'):10s} ${f(m,'cost_micros',int)/1e6:7.2f} imp={imp:4d} ctr={(clk/imp*100 if imp else 0):4.1f}% conv={f(m,'conversions'):3.1f} {a['ad'].get('final_urls')}")
    q = f"""SELECT asset_group.name, asset_group.status, asset_group.final_urls, asset_group.ad_strength, asset_group.primary_status
            FROM asset_group WHERE campaign.id = {PMAX}"""
    for r in run_query(CID, q):
        x = r["asset_group"]; print(f"  PMAX AG {x['name'][:30]:30s} {x['status']} {x.get('ad_strength')} {x.get('primary_status')} {x.get('final_urls')}")
    q = f"""SELECT asset_group_signal.audience.audience, asset_group_signal.search_theme.text FROM asset_group_signal WHERE campaign.id = {PMAX}"""
    rows = run_query(CID, q)
    print(f"  PMAX signals: {len(rows)} ->", [r["asset_group_signal"].get("search_theme", {}).get("text") or "audience" for r in rows][:25])

def pmax_negs():
    hdr("7) PMAX negative criteria types + shared list contents")
    q = f"""SELECT campaign_criterion.type, campaign_criterion.negative FROM campaign_criterion WHERE campaign.id = {PMAX} AND campaign_criterion.negative = TRUE"""
    c = defaultdict(int)
    for r in run_query(CID, q): c[g(r["campaign_criterion"], "type")] += 1
    print("  ", dict(c))
    q = """SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion
           WHERE shared_set.id = 11433552108"""
    kws = [f"{r['shared_criterion']['keyword']['text']}({r['shared_criterion']['keyword']['match_type'][0]})" for r in run_query(CID, q)]
    print(f"  CSMS_Negatives {len(kws)}:")
    print("  " + ", ".join(sorted(kws)))

def terms():
    hdr("8) ALL PAID SEARCH TERMS 30d (cost>0), NB+BR")
    q = f"""SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
            FROM search_term_view WHERE campaign.id IN ({NB}, {BR}) AND segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0"""
    agg = defaultdict(lambda: [0, 0, 0.0])
    for r in run_query(CID, q):
        m = r["metrics"]; k = (TAG[r["campaign"]["id"]], r["search_term_view"]["search_term"])
        agg[k][0] += f(m, "cost_micros", int); agg[k][1] += f(m, "clicks", int); agg[k][2] += f(m, "conversions")
    for k, v in sorted(agg.items(), key=lambda kv: -kv[1][0]):
        print(f"  {k[0]:3s} ${v[0]/1e6:7.2f} clk={v[1]:2d} conv={v[2]:3.1f} {k[1]}")

def outside():
    hdr("4b) SPEND FROM PEOPLE OUTSIDE TARGETS (interest match) + by campaign, 30d")
    q = f"""SELECT campaign.id, user_location_view.targeting_location, metrics.cost_micros, metrics.clicks, metrics.conversions
            FROM user_location_view WHERE campaign.id IN ({LIVE}) AND segments.date DURING LAST_30_DAYS"""
    agg = defaultdict(lambda: [0, 0, 0.0])
    for r in run_query(CID, q):
        m = r["metrics"]; k = (TAG[r["campaign"]["id"]], bool(r["user_location_view"].get("targeting_location")))
        agg[k][0] += f(m, "cost_micros", int); agg[k][1] += f(m, "clicks", int); agg[k][2] += f(m, "conversions")
    for k, v in sorted(agg.items()):
        print(f"  {k[0]:5s} in_target={k[1]!s:5s} ${v[0]/1e6:8.2f} clk={v[1]:4d} conv={v[2]:4.1f}")

def lsa():
    hdr("12) LSA leads 90d by week/type/status + area code bucket")
    q = """SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status,
           local_services_lead.lead_charged, local_services_lead.contact_details.phone_number
           FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-07-10'"""
    rows = run_query("1219885876", q)
    wk = defaultdict(lambda: defaultdict(int)); ac = defaultdict(int)
    from datetime import datetime
    for r in rows:
        l = r["local_services_lead"]
        d = datetime.strptime(l["creation_date_time"][:10], "%Y-%m-%d")
        key = d.strftime("%Y-%m") + ("a" if d.day <= 15 else "b")
        wk[key][l["lead_status"]] += 1
        ph = (l.get("contact_details", {}) or {}).get("phone_number", "") or ""
        digits = "".join(ch for ch in ph if ch.isdigit())[-10:]
        code = digits[:3] if len(digits) == 10 else "none"
        bucket = "FW 817/682" if code in ("817", "682") else ("Dallas 214/469/972" if code in ("214", "469", "972") else ("940" if code == "940" else ("none" if code == "none" else "other")))
        ac[bucket] += 1
    for k in sorted(wk): print(f"  {k}: {dict(wk[k])}")
    print("  area codes:", dict(ac), "total", len(rows))

def conv_hist():
    hdr("1c) ALL_CONVERSIONS BY ACTION BY MONTH, Apr-Oct 2026")
    q = """SELECT segments.month, segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer
           WHERE segments.date BETWEEN '2026-04-01' AND '2026-10-08' AND metrics.all_conversions > 0"""
    agg = defaultdict(dict)
    for r in run_query(CID, q):
        agg[r["segments"]["conversion_action_name"]][r["segments"]["month"][:7]] = (f(r["metrics"], "all_conversions"), f(r["metrics"], "conversions"))
    months = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
    print("  " + " " * 48 + "  ".join(m[2:] for m in months))
    for a, d in sorted(agg.items()):
        print(f"  {a[:46]:46s} " + "  ".join(f"{d.get(m,(0,0))[0]:5.0f}" for m in months))

for l, fn in [("7", pmax_negs), ("4b", outside), ("8", terms), ("12", lsa)]:
    safe(l, fn)
