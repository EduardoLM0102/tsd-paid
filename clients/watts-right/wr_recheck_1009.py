# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805), 2026-10-09 recheck of the 09-29 overhaul (checklist in google-ads-log.md).
Post window = 09-30 -> 10-08 (first full days after the 09-29 changes). Baseline = 08-30 -> 09-28 (as logged).
"""
import sys, collections, re
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PM, EV = "23690645223", "23832838033", "23833205176", "24094882200"
NAMES = {BR: "Branded", NB: "Nonbranded", PM: "PMax", EV: "EV(paused)"}
POST = "segments.date BETWEEN '2026-09-30' AND '2026-10-08'"
BASE = "segments.date BETWEEN '2026-08-30' AND '2026-09-28'"
PRE9 = "segments.date BETWEEN '2026-09-20' AND '2026-09-28'"
DAYS = 9


def q(s):
    return run_query(CID, s)


def M(x):
    return int(x or 0) / 1e6


def F(x):
    return float(x or 0)


def H(t):
    print(f"\n===== {t} =====")


H("A. DAILY SPEND per campaign, 09-30..10-08")
daily = collections.defaultdict(dict)
budgets = {}
for r in q(f"""SELECT campaign.id, campaign.status, campaign_budget.amount_micros, segments.date, metrics.cost_micros
    FROM campaign WHERE {POST} AND campaign.id IN ({BR},{NB},{PM},{EV})"""):
    cid = r["campaign"]["id"]
    budgets[cid] = (M(r["campaign_budget"].get("amount_micros")), r["campaign"]["status"])
    daily[r["segments"]["date"]][cid] = M(r["metrics"].get("cost_micros"))
print("date        " + "".join(f"{NAMES[c]:>12}" for c in (BR, NB, PM, EV)))
for d in sorted(daily):
    print(d + "  " + "".join(f"{daily[d].get(c, 0):>12.2f}" for c in (BR, NB, PM, EV)))
for c in (BR, NB, PM, EV):
    tot = sum(daily[d].get(c, 0) for d in daily)
    b, st = budgets.get(c, (0, "?"))
    print(f"{NAMES[c]:<12} total ${tot:,.2f}  avg/d ${tot / DAYS:,.2f}  budget ${b:.0f}/d  {st}")


def camp_totals(win, label):
    H(f"B. CAMPAIGN TOTALS {label}")
    for r in q(f"""SELECT campaign.id, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions,
        metrics.all_conversions, metrics.search_impression_share, metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share, metrics.search_top_impression_share
        FROM campaign WHERE {win} AND campaign.id IN ({BR},{NB},{PM},{EV})"""):
        m = r["metrics"]
        cost, clk, conv = M(m.get("cost_micros")), int(m.get("clicks") or 0), F(m.get("conversions"))
        print(f"{NAMES[r['campaign']['id']]:<12} ${cost:>8,.2f} clk {clk:>4} impr {int(m.get('impressions') or 0):>6} "
              f"conv {conv:>5.1f} allconv {F(m.get('all_conversions')):>5.1f} "
              f"CPC ${cost / clk if clk else 0:>6.2f} CPL ${cost / conv if conv else 0:>7.2f} CVR {conv / clk * 100 if clk else 0:>5.1f}% "
              f"IS {F(m.get('search_impression_share')) * 100:>5.1f} budLost {F(m.get('search_budget_lost_impression_share')) * 100:>5.1f} "
              f"rankLost {F(m.get('search_rank_lost_impression_share')) * 100:>5.1f} topIS {F(m.get('search_top_impression_share')) * 100:>5.1f}")


camp_totals(POST, "POST 09-30..10-08")
camp_totals("segments.date BETWEEN '2026-10-02' AND '2026-10-08'", "LAST 7 (10-02..10-08)")
camp_totals(PRE9, "PRE 09-20..09-28 (for impression/presence compare)")

H("C. CONVERSIONS BY ACTION per campaign, POST")
for r in q(f"""SELECT campaign.id, segments.conversion_action_name, segments.conversion_action_category, metrics.conversions, metrics.all_conversions
    FROM campaign WHERE {POST} AND campaign.id IN ({BR},{NB},{PM},{EV}) AND metrics.all_conversions > 0"""):
    s = r["segments"]
    print(f"{NAMES[r['campaign']['id']]:<12} {s['conversion_action_name'][:40]:<40} {s['conversion_action_category']:<20} "
          f"conv {F(r['metrics'].get('conversions')):>5.1f} all {F(r['metrics'].get('all_conversions')):>5.1f}")

H("C2. CONVERSIONS BY ACTION, PPC total, BASELINE 08-30..09-28 vs POST (per day)")
for win, lab, days in [(BASE, "BASE", 30), (POST, "POST", DAYS)]:
    agg = collections.Counter()
    for r in q(f"""SELECT segments.conversion_action_name, metrics.conversions FROM campaign
        WHERE {win} AND campaign.id IN ({BR},{NB},{PM},{EV}) AND metrics.conversions > 0"""):
        agg[r["segments"]["conversion_action_name"]] += F(r["metrics"].get("conversions"))
    for k, v in agg.most_common():
        print(f"  {lab} {k[:45]:<45} {v:>5.1f}  ({v / days:.2f}/d)")

H("D. PMAX SEARCH CATEGORIES, POST")
for r in q(f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.impressions, metrics.conversions
    FROM campaign_search_term_insight WHERE {POST} AND campaign_search_term_insight.campaign_id = '{PM}' ORDER BY metrics.clicks DESC LIMIT 30"""):
    m = r["metrics"]
    print(f"  {str(r['campaign_search_term_insight'].get('category_label'))[:50]:<50} clk {m.get('clicks', 0):>4} impr {m.get('impressions', 0):>5} conv {F(m.get('conversions')):.1f}")

H("D2. PMAX by network (POST)")
for r in q(f"""SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign
    WHERE {POST} AND campaign.id = {PM}"""):
    m = r["metrics"]
    print(f"  {r['segments']['ad_network_type']:<18} ${M(m.get('cost_micros')):>7.2f} clk {m.get('clicks', 0):>4} conv {F(m.get('conversions')):.1f}")

H("E. BRANDED keywords POST")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
    ad_group_criterion.approval_status, ad_group_criterion.system_serving_status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM keyword_view WHERE {POST} AND campaign.id = {BR}"""):
    k, m = r["ad_group_criterion"], r["metrics"]
    clk = int(m.get("clicks") or 0)
    print(f"  {k['keyword']['text'][:30]:<30} {k['keyword']['match_type']:<6} {k['status']:<7} {k.get('approval_status', '-'):<10} "
          f"{k.get('system_serving_status', '-'):<10} impr {m.get('impressions', 0):>4} clk {clk:>3} ${M(m.get('cost_micros')):>7.2f} "
          f"CPC ${M(m.get('cost_micros')) / clk if clk else 0:.2f} conv {F(m.get('conversions')):.1f}")
print("  -- keywords with zero impressions in window (not returned above):")
for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.approval_status
    FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE"""):
    k = r["ad_group_criterion"]
    print(f"     {k['keyword']['text']:<30} {k['keyword']['match_type']:<6} {k['status']:<7} {k.get('approval_status')}")
for r in q(f"SELECT campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location_fraction_micros FROM campaign WHERE campaign.id = {BR}"):
    print("  Target IS settings:", r["campaign"].get("target_impression_share"))

COMP = re.compile(r"sparky|waybright|jimmy jones|aspen|code red|bills? electric|firefly|harp|hayes|electric city|watts up|midtown|wyatt|bison|genesis|colburn|amp electrical|\bme electric|meeks|mr\.? electric|mission electric|tiger|murray|hot shot|quality electric|electric\b.*\b(llc|inc|co)\b")
BRAND = re.compile(r"watt|what'?s right|wattsright")
JOB = re.compile(r"job|hiring|apprentic|career|salary|employ")

H("F. NONBRANDED SEARCH TERMS POST (sorted by cost), split before/after 10-05 negatives")
rows = q(f"""SELECT search_term_view.search_term, search_term_view.status, ad_group.name, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
    FROM search_term_view WHERE {POST} AND campaign.id = {NB}""")
agg = {}
for r in rows:
    t = r["search_term_view"]["search_term"]
    a = agg.setdefault(t, {"cost": 0, "clk": 0, "conv": 0, "imp": 0, "late": 0, "ag": r["ad_group"]["name"], "st": r["search_term_view"].get("status")})
    a["cost"] += M(r["metrics"].get("cost_micros")); a["clk"] += int(r["metrics"].get("clicks") or 0)
    a["conv"] += F(r["metrics"].get("conversions")); a["imp"] += int(r["metrics"].get("impressions") or 0)
    if r["segments"]["date"] >= "2026-10-06":
        a["late"] += M(r["metrics"].get("cost_micros"))
tot = sum(a["cost"] for a in agg.values())
print(f"  {len(agg)} terms, ${tot:,.2f} total")
for t, a in sorted(agg.items(), key=lambda x: -x[1]["cost"])[:60]:
    flag = "BRAND" if BRAND.search(t) else "COMP?" if COMP.search(t) else "JOB" if JOB.search(t) else ""
    print(f"  ${a['cost']:>7.2f} (10-06+ ${a['late']:>6.2f}) clk {a['clk']:>3} conv {a['conv']:>3.1f} {a['st']:<9} {flag:<6} {t[:55]:<55} [{a['ag'][:20]}]")
print("  -- flagged brand/competitor/job terms (all):")
for t, a in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
    if BRAND.search(t) or COMP.search(t) or JOB.search(t):
        print(f"     ${a['cost']:>7.2f} (10-06+ ${a['late']:>6.2f}) clk {a['clk']:>3} conv {a['conv']:.1f} {t}")
print("  -- 'electric' terms that look like a business name (manual review):")
for t, a in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
    if "electric" in t and not BRAND.search(t) and not COMP.search(t) and a["clk"] > 0 and not re.search(r"electrician|electrical", t):
        print(f"     ${a['cost']:>7.2f} clk {a['clk']:>3} conv {a['conv']:.1f} {t}")

H("F2. 'quality electric' all campaigns, 08-10..10-08")
for r in q("""SELECT campaign.name, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM search_term_view WHERE segments.date BETWEEN '2026-08-10' AND '2026-10-08' AND search_term_view.search_term LIKE '%quality%'"""):
    m = r["metrics"]
    print(f"  {r['campaign']['name'][:30]:<30} {r['search_term_view']['search_term']:<40} ${M(m.get('cost_micros')):.2f} clk {m.get('clicks', 0)} conv {F(m.get('conversions')):.1f}")
print("  conv actions for 'quality' term rows:")
for r in q("""SELECT search_term_view.search_term, segments.conversion_action_name, metrics.conversions
    FROM search_term_view WHERE segments.date BETWEEN '2026-08-10' AND '2026-10-08' AND search_term_view.search_term LIKE '%quality%' AND metrics.conversions > 0"""):
    print("    ", r["search_term_view"]["search_term"], r["segments"]["conversion_action_name"], r["metrics"].get("conversions"))

H("G. NONBRANDED by AD GROUP, BASE (homepage era) vs POST (service pages)")
for win, lab in [(BASE, "BASE"), (POST, "POST")]:
    for r in q(f"""SELECT ad_group.name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.impressions FROM ad_group
        WHERE {win} AND campaign.id = {NB}"""):
        m = r["metrics"]; cost, clk, conv = M(m.get("cost_micros")), int(m.get("clicks") or 0), F(m.get("conversions"))
        print(f"  {lab} {r['ad_group']['name'][:28]:<28} ${cost:>8.2f} impr {m.get('impressions', 0):>5} clk {clk:>4} conv {conv:>4.1f} "
              f"CVR {conv / clk * 100 if clk else 0:>5.1f}% CPL ${cost / conv if conv else 0:>7.2f} CPC ${cost / clk if clk else 0:.2f}")
print("  -- POST conv by action per ad group")
for r in q(f"""SELECT ad_group.name, segments.conversion_action_name, metrics.conversions FROM ad_group
    WHERE {POST} AND campaign.id = {NB} AND metrics.conversions > 0"""):
    print(f"     {r['ad_group']['name'][:28]:<28} {r['segments']['conversion_action_name'][:40]:<40} {F(r['metrics'].get('conversions')):.1f}")

H("H. NONBRANDED ADS (old vs new RSA), POST")
for r in q(f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status,
    ad_group_ad.ad_strength, ad_group_ad.ad.final_urls, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM ad_group_ad WHERE {POST} AND campaign.id = {NB} AND ad_group_ad.status != 'REMOVED'"""):
    a, m = r["ad_group_ad"], r["metrics"]
    imp, clk, conv = int(m.get("impressions") or 0), int(m.get("clicks") or 0), F(m.get("conversions"))
    new = "NEW" if a["ad"]["id"] in ("826560998576", "826560998579", "826560998582") else "old"
    print(f"  {r['ad_group']['name'][:22]:<22} {a['ad']['id']} {new} {a['status']:<7} {a['policy_summary'].get('approval_status', '-'):<9} "
          f"{a.get('ad_strength', '-'):<8} impr {imp:>5} clk {clk:>3} CTR {clk / imp * 100 if imp else 0:>5.2f}% conv {conv:.1f} {a['ad'].get('final_urls', [''])[0][-40:]}")
print("  -- all ad approval (Branded/PMax search ads, no metrics filter)")
for r in q(f"""SELECT campaign.id, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status
    FROM ad_group_ad WHERE campaign.id IN ({BR},{NB}) AND ad_group_ad.status = 'ENABLED'"""):
    a = r["ad_group_ad"]
    print(f"     {NAMES[r['campaign']['id']]:<11} {a['ad']['id']} {a['status']} {a['policy_summary'].get('approval_status')}")

H("I. NONBRANDED keywords POST (cost-sorted) with QS")
for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score,
    ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.post_click_quality_score,
    metrics.cost_micros, metrics.clicks, metrics.conversions FROM keyword_view WHERE {POST} AND campaign.id = {NB} ORDER BY metrics.cost_micros DESC LIMIT 20"""):
    k, m = r["ad_group_criterion"], r["metrics"]; qi = k.get("quality_info", {})
    print(f"  ${M(m.get('cost_micros')):>7.2f} clk {m.get('clicks', 0):>3} conv {F(m.get('conversions')):>3.1f} QS {qi.get('quality_score', '-')!s:>2} "
          f"ctr {qi.get('search_predicted_ctr', '-')[:7]:<7} ad {qi.get('creative_quality_score', '-')[:7]:<7} lp {qi.get('post_click_quality_score', '-')[:7]:<7} "
          f"{k['keyword']['match_type']:<6} {k['keyword']['text'][:35]:<35} [{r['ad_group']['name'][:16]}]")

H("J. GEO (POST): country + location type")
for r in q(f"""SELECT campaign.id, geographic_view.country_criterion_id, geographic_view.location_type, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM geographic_view WHERE {POST} AND campaign.id IN ({BR},{NB},{PM})"""):
    g, m = r["geographic_view"], r["metrics"]
    print(f"  {NAMES[r['campaign']['id']]:<11} country {g.get('country_criterion_id')} {g.get('location_type'):<22} clk {m.get('clicks', 0):>4} ${M(m.get('cost_micros')):>7.2f} conv {F(m.get('conversions')):.1f}")

H("K. LSA context POST")
for r in q(f"""SELECT campaign.name, metrics.cost_micros, metrics.conversions FROM campaign WHERE {POST} AND campaign.advertising_channel_type = 'LOCAL_SERVICES'"""):
    print(f"  {r['campaign']['name'][:50]} ${M(r['metrics'].get('cost_micros')):,.2f} conv {F(r['metrics'].get('conversions')):.1f}")
