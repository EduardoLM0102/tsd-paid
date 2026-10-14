"""Checklist G2 (read-only): Quality Score components by ad group (spend-weighted) + current RSA assets/labels, non-branded Search."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID = "1051843378"; CAMPS = ("23866999121", "23848895678", "23853484024"); S, U = "2026-09-08", "2026-10-07"
f = lambda x: float(x or 0)
print("== keywords by ad group (30d), QS components")
ag = defaultdict(lambda: {"cost": 0.0, "clk": 0.0, "kws": [], "ctr_below_cost": 0.0, "camp": ""})
for r in run_query(CID, f"""SELECT campaign.name, ad_group.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.creative_quality_score,
ad_group_criterion.quality_info.post_click_quality_score, metrics.cost_micros, metrics.clicks, metrics.impressions
FROM keyword_view WHERE campaign.id IN ({','.join(CAMPS)}) AND segments.date BETWEEN '{S}' AND '{U}' AND metrics.impressions > 0"""):
    k = r["ad_group_criterion"]; q = k.get("quality_info", {}); m = r["metrics"]; key = (r["campaign"]["name"][24:], r["ad_group"]["name"], r["ad_group"]["id"])
    a = ag[key]; c = f(m.get("cost_micros")) / 1e6; a["cost"] += c; a["clk"] += f(m.get("clicks"))
    if "BELOW" in str(q.get("search_predicted_ctr", "")): a["ctr_below_cost"] += c
    a["kws"].append((c, k["keyword"]["text"], str(k["keyword"]["match_type"]), q.get("quality_score", "-"), str(q.get("search_predicted_ctr", "-"))[:5],
                     str(q.get("creative_quality_score", "-"))[:5], str(q.get("post_click_quality_score", "-"))[:5], str(k.get("status"))))
for key, a in sorted(ag.items(), key=lambda x: -x[1]["cost"]):
    print(f"\n-- {key[0]} / {key[1]} ({key[2]}): ${a['cost']:,.0f}, {a['clk']:.0f} clk, {a['ctr_below_cost'] / a['cost'] * 100 if a['cost'] else 0:.0f}% of spend on 'expected CTR below average'")
    for c, t, mt, qs, ctr, ad, lp, st in sorted(a["kws"], reverse=True)[:8]:
        print(f"     ${c:6,.0f}  QS {qs}  ctr {ctr} ad {ad} lp {lp}  {mt:6s} {t}  [{st}]")
print("\n\n== current RSAs + asset performance labels")
for r in run_query(CID, f"""SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad_strength, ad_group_ad.ad.final_urls, ad_group_ad.status
FROM ad_group_ad WHERE campaign.id IN ({','.join(CAMPS)}) AND ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED'"""):
    a = r["ad_group_ad"]; print(f"\n-- {r['campaign']['name'][24:]} / {r['ad_group']['name']}  ad {a['ad']['id']}  strength {a.get('ad_strength')}  {a['ad'].get('final_urls')}")
    for x in run_query(CID, f"""SELECT ad_group_ad_asset_view.field_type, ad_group_ad_asset_view.performance_label, ad_group_ad_asset_view.pinned_field, asset.text_asset.text
FROM ad_group_ad_asset_view WHERE ad_group_ad.ad.id = {a['ad']['id']} AND ad_group_ad_asset_view.enabled = TRUE"""):
        v = x["ad_group_ad_asset_view"]; print(f"     {str(v.get('field_type'))[:4]} {str(v.get('performance_label', '-')):9s} {'PIN ' + str(v.get('pinned_field')) if v.get('pinned_field') else '':12s} {x['asset'].get('text_asset', {}).get('text', '')}")
