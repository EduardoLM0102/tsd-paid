# READ-ONLY. ./tsd.sh <abs path>. Cool Hand 9865206319, fu-113: QS / LP / expected CTR recheck + Electrical/HVAC leads since the 11-06 changes.
import sys; sys.path.insert(0, ".")
from lib import run_query
CID = "9865206319"; M = lambda x: int(x or 0)/1e6; F = lambda x: float(x or 0)
q = lambda s: run_query(CID, s)
print("== campaigns 11-07..11-18 (12d) vs 10-26..11-06 (12d)")
for w in ("'2026-10-26' AND '2026-11-06'", "'2026-11-07' AND '2026-11-18'"):
    for r in q(f"SELECT campaign.name, campaign.bidding_strategy_type, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.ctr, metrics.search_impression_share FROM campaign WHERE segments.date BETWEEN {w} AND campaign.advertising_channel_type = 'SEARCH' AND metrics.impressions > 0"):
        c, m = r["campaign"], r["metrics"]; s = M(m.get("cost_micros")); cv = F(m.get("conversions"))
        print(f"  {w[:24]} {c['name'][:32]:<32} {c.get('bidding_strategy_type')[:14]:<14} ${s:8.2f} clk {m.get('clicks',0):>4} CTR {F(m.get('ctr'))*100:4.1f}% conv {cv:4.1f} CPL ${s/cv if cv else 0:6.0f} IS {F(m.get('search_impression_share'))*100:.0f}")
print("== conversions by action 11-07..11-18")
for r in q("SELECT campaign.name, segments.conversion_action_name, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-11-07' AND '2026-11-18' AND metrics.conversions > 0"):
    print(f"  {r['campaign']['name'][:32]:<32} {r['segments']['conversion_action_name'][:40]:<40} {F(r['metrics']['conversions']):.1f}")
print("== QS now (keywords with impr 10-20..11-18)")
for r in q("""SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.post_click_quality_score,
   ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.final_urls, metrics.impressions
   FROM keyword_view WHERE segments.date BETWEEN '2026-10-20' AND '2026-11-18' AND metrics.impressions > 20 AND campaign.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED' ORDER BY metrics.impressions DESC LIMIT 30"""):
    k = r["ad_group_criterion"]; qi = k.get("quality_info", {})
    print(f"  {r['campaign']['name'][:18]:<18} {k['keyword']['text'][:30]:<30} {k['keyword']['match_type'][:6]:<6} QS {qi.get('quality_score','-')} LP {str(qi.get('post_click_quality_score','-'))[:5]} ad {str(qi.get('creative_quality_score','-'))[:5]} eCTR {str(qi.get('search_predicted_ctr','-'))[:5]} impr {r['metrics']['impressions']}")
print("== RSA CTR 11-07..11-18 by ad")
for r in q("SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls, ad_group_ad.ad_strength, metrics.impressions, metrics.clicks, metrics.ctr, metrics.conversions FROM ad_group_ad WHERE segments.date BETWEEN '2026-11-07' AND '2026-11-18' AND ad_group_ad.status = 'ENABLED' AND metrics.impressions > 0"):
    a = r["ad_group_ad"]; m = r["metrics"]
    print(f"  {r['ad_group']['name'][:22]:<22} {a['ad']['id']} {a.get('ad_strength','')[:9]:<9} impr {m.get('impressions'):>5} CTR {F(m.get('ctr'))*100:4.1f}% conv {F(m.get('conversions')):.1f} {str(a['ad'].get('final_urls'))[:55]}")
