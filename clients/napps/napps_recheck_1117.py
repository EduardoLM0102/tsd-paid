# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Napps (9509605037), 2026-11-17 week-3 read (Command Center fu-144). 11-10 applied: negs streety/water heater, taps secondary, Henderson county->city. 11-11: LP number = 903-289-7073. Was: 2026-11-10 week-2 read (Command Center fu-120) of the relaunched Nonbranded after the 11-03 Max Clicks cap $15 -> $25:
Heating 24049055193 ($65, Furnace Repair only) + Plumbing 23819717682 ($35, Emergency Plumber only), both Max Clicks $25 cap since 11-03 10:41.
Window 11-03 -> 11-09 (7d), vs week 1 10-28 -> 11-02 (6d). Forms not counted on new pages (fu-121): judge leads on calls only. Ad approval, spend vs budget, 65/35 split, terms, leads, QS/landing page, geo, changes."""
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

CID = "9509605037"
BR, HT, PL = "23685615826", "24049055193", "23819717682"
NAMES = {BR: "Branded", HT: "NB Heating", PL: "NB Plumbing"}
WIN, DAYS = "segments.date BETWEEN '2026-11-10' AND '2026-11-16'", 7
W1 = "segments.date BETWEEN '2026-11-03' AND '2026-11-09'"
IDS = f"campaign.id IN ({BR},{HT},{PL})"
NB = f"campaign.id IN ({HT},{PL})"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

print("===== A. campaigns 11-10..11-16")
sp_by = {}
for r in q(f"""SELECT campaign.id, campaign.status, campaign.primary_status, campaign.bidding_strategy_type, campaign_budget.amount_micros,
    metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions, metrics.search_impression_share,
    metrics.search_absolute_top_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
    FROM campaign WHERE {WIN} AND {IDS}"""):
    c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0)); sp_by[c["id"]] = sp
    print(f"  {NAMES[c['id']]:<12} {c['status']}/{c.get('primary_status')} {c.get('bidding_strategy_type')} bud ${M(r['campaign_budget'].get('amount_micros')):.0f} | "
          f"${sp:,.2f} ({sp/DAYS:.0f}/d) clk {cl} impr {m.get('impressions',0)} CPC ${sp/cl if cl else 0:.2f} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} | "
          f"IS {F(m.get('search_impression_share'))*100:.0f} abs-top {F(m.get('search_absolute_top_impression_share'))*100:.0f} "
          f"bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
nb = sp_by.get(HT, 0) + sp_by.get(PL, 0)
print(f"  NB split: Heating {sp_by.get(HT,0)/nb*100 if nb else 0:.0f}% / Plumbing {sp_by.get(PL,0)/nb*100 if nb else 0:.0f}% (target 65/35)")

print("\n===== B. conversions by action")
for r in q(f"""SELECT campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
    WHERE {WIN} AND {IDS} AND metrics.all_conversions > 0"""):
    print(f"  {NAMES[r['campaign']['id']]:<12} {r['segments']['conversion_action_name']:<40} conv {F(r['metrics'].get('conversions')):.1f} all {F(r['metrics'].get('all_conversions')):.1f}")

print("\n===== C. NB daily")
for r in q(f"""SELECT campaign.id, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions FROM campaign
    WHERE segments.date BETWEEN '2026-11-03' AND '2026-11-16' AND {NB} ORDER BY segments.date"""):
    m = r["metrics"]; print(f"  {r['segments']['date']} {NAMES[r['campaign']['id']]:<12} ${M(m.get('cost_micros')):6.2f} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>4}")

print("\n===== D. NB ads: approval + final URL")
for r in q(f"""SELECT campaign.id, ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls,
    ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status FROM ad_group_ad
    WHERE {NB} AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'"""):
    a = r["ad_group_ad"]
    print(f"  {NAMES[r['campaign']['id']]:<12} {r['ad_group']['name']:<20} ad {a['ad']['id']} {a['policy_summary'].get('approval_status')}/{a['policy_summary'].get('review_status')} {a['ad'].get('final_urls')}")

print("\n===== E. NB search terms (by cost)")
for r in q(f"""SELECT campaign.id, search_term_view.search_term, search_term_view.status, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.all_conversions
    FROM search_term_view WHERE {WIN} AND {NB} AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 40"""):
    m = r["metrics"]
    print(f"  {NAMES[r['campaign']['id']]:<12} {r['search_term_view']['search_term']:<42} impr {m.get('impressions',0):>3} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f} all {F(m.get('all_conversions')):.1f}")

print("\n===== F. NB keywords: QS components (enabled kws in enabled ad groups)")
for r in q(f"""SELECT campaign.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score,
    ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.creative_quality_score,
    ad_group_criterion.quality_info.search_predicted_ctr, metrics.impressions, metrics.clicks, metrics.cost_micros
    FROM keyword_view WHERE {WIN} AND {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED'"""):
    k = r["ad_group_criterion"]; qi = k.get("quality_info", {}); m = r["metrics"]
    print(f"  {NAMES[r['campaign']['id']]:<12} {k['keyword']['text'][:34]:<34} {k['keyword']['match_type'][:6]:<6} QS {qi.get('quality_score','-')} "
          f"LP {qi.get('post_click_quality_score','-')} ad {qi.get('creative_quality_score','-')} eCTR {qi.get('search_predicted_ctr','-')} | impr {m.get('impressions',0)} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== G. call_view 11-10..11-16 (all campaigns)")
for r in q("""SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code
    FROM call_view WHERE call_view.start_call_date_time BETWEEN '2026-11-10 00:00:00' AND '2026-11-16 23:59:59'"""):
    c = r["call_view"]; print(f"  {r['campaign']['name'][:40]:<40} {c['start_call_date_time']} {c.get('call_duration_seconds')}s {c.get('call_status')} ({c.get('caller_area_code')})")

print("\n===== H. NB clicks by city")
for r in q(f"""SELECT campaign.id, segments.geo_target_city, metrics.clicks, metrics.cost_micros FROM geographic_view
    WHERE {WIN} AND {NB} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 20"""):
    m = r["metrics"]; print(f"  {NAMES[r['campaign']['id']]:<12} {r['segments'].get('geo_target_city')} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== I. changes since 11-10")
for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
    change_event.changed_fields, change_event.campaign FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-10' AND '2026-11-17'
    ORDER BY change_event.change_date_time DESC LIMIT 60"""):
    e = r["change_event"]; print(" ", e["change_date_time"][:19], e.get("user_email"), e["change_resource_type"], e["resource_change_operation"], (e.get("changed_fields") or "")[:80], (e.get("campaign") or "")[-11:])

print("\n===== J. week 2 (11-03..11-09, 7d) for comparison")
for r in q(f"""SELECT campaign.id, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share,
    metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share FROM campaign WHERE {W1} AND {IDS}"""):
    m = r["metrics"]; sp = M(m.get("cost_micros")); cl = int(m.get("clicks", 0))
    print(f"  {NAMES[r['campaign']['id']]:<12} ${sp:,.2f} ({sp/7:.0f}/d) clk {cl} impr {m.get('impressions',0)} CPC ${sp/cl if cl else 0:.2f} | IS {F(m.get('search_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f}")

print("\n===== K. current bidding config")
for r in q(f"""SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
    FROM campaign WHERE {IDS}"""):
    c = r["campaign"]
    print(f"  {NAMES[c['id']]:<12} {c['status']} {c.get('bidding_strategy_type')} cap ${M((c.get('target_spend') or {}).get('cpc_bid_ceiling_micros')):.2f} bud ${M(r['campaign_budget'].get('amount_micros')):.0f}")

print("\n===== L. NB clicks by user location (geographic_view = physical/interest), week 3")
for r in q(f"""SELECT campaign.id, geographic_view.location_type, segments.geo_target_city, metrics.clicks, metrics.impressions, metrics.cost_micros FROM geographic_view
    WHERE {WIN} AND {NB} AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 30"""):
    m = r["metrics"]; print(f"  {NAMES[r['campaign']['id']]:<12} {r['geographic_view']['location_type']:<26} {r['segments'].get('geo_target_city')} impr {m.get('impressions',0)} clk {m.get('clicks',0)} ${M(m.get('cost_micros')):.2f}")

print("\n===== M. LSA-PPL / other campaigns in acct, 11-10..11-16")
for r in q(f"""SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.status, metrics.cost_micros, metrics.conversions FROM campaign WHERE {WIN} AND metrics.cost_micros > 0"""):
    print(f"  {r['campaign']['name'][:45]:<45} {r['campaign']['advertising_channel_type']} {r['campaign']['status']} ${M(r['metrics'].get('cost_micros')):.2f} conv {F(r['metrics'].get('conversions')):.1f}")
print("\n===== N. cumulative NB since 10-27 relaunch")
for r in q(f"""SELECT campaign.id, metrics.cost_micros, metrics.clicks FROM campaign WHERE segments.date BETWEEN '2026-10-27' AND '2026-11-16' AND {NB}"""):
    print(f"  {NAMES[r['campaign']['id']]:<12} ${M(r['metrics'].get('cost_micros')):,.2f} clk {r['metrics'].get('clicks',0)}")
