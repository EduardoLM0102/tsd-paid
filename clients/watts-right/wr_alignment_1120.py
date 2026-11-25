# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Watt's Right (3651667805) Post Client Strategy Review alignment (AT df7c0bbf), 2026-11-20.
Presented on the 11-16 review (f911c525): approved Push plan ~$26.9k/mo (Search ~$14k + LSA ~$13k), PMax paused 11-10, NB generic/generator/surge groups.
Since: Edu 11-17 Branded $145 -> $60, NB $320 -> $405 (tCPA $110), 3 negs. AM ticket 76e1df4a (11-19): WR charges extra after hours -> 'no extra fees' claim removed from the site.
Checks: live budgets + spend, enabled campaigns/ad groups, geo, ad copy (fee / 24/7 claims), assets, primary conversions, LSA PPL budget, change_event."""
import sys, re
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
BR, NB, PMAX, LSA = "23690645223", "23832838033", "23833205176", "24425981973"
q = lambda s: run_query(CID, s)
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
W7 = "segments.date BETWEEN '2026-11-13' AND '2026-11-19'"
SINCE = "segments.date BETWEEN '2026-11-17' AND '2026-11-19'"
MTD = "segments.date BETWEEN '2026-11-01' AND '2026-11-19'"

def safe(label, fn):
    try:
        fn()
    except BaseException as e:
        print(f"  !! {label} failed: {e}")

print("===== A. campaigns: status, budget, bidding")
def a():
    for r in q("""SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.advertising_channel_type, campaign.bidding_strategy_type,
        campaign.target_cpa.target_cpa_micros, campaign.maximize_conversions.target_cpa_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.status != 'REMOVED'"""):
        c = r["campaign"]
        tcpa = M(c.get("maximize_conversions", {}).get("target_cpa_micros") or c.get("target_cpa", {}).get("target_cpa_micros"))
        ceil = M(c.get("target_impression_share", {}).get("cpc_bid_ceiling_micros"))
        print(f"  {c['id']} {c['name'][:44]:<44} {c['status']}/{c.get('primary_status')} {c['advertising_channel_type'][:6]} {c.get('bidding_strategy_type')} "
              f"bud ${M(r['campaign_budget'].get('amount_micros')):.2f} tCPA ${tcpa:.0f} ceil ${ceil:.2f} geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')}")
safe("A", a)

for label, win, days in (("B. spend 11-17..11-19 (post 11-17 change)", SINCE, 3), ("B2. spend 7d 11-13..11-19", W7, 7), ("B3. spend Nov 1-19", MTD, 19)):
    print(f"\n===== {label}")
    def b(win=win, days=days):
        tot = 0
        for r in q(f"""SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.search_impression_share,
            metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND metrics.cost_micros > 0"""):
            c, m = r["campaign"], r["metrics"]; sp = M(m.get("cost_micros")); tot += sp
            print(f"  {c['id']} {c['name'][:40]:<40} ${sp:,.2f} (${sp/days:,.0f}/d) clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f} "
                  f"IS {F(m.get('search_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
        print(f"  TOTAL ${tot:,.2f} (${tot/days:,.0f}/d)")
    safe(label, b)

print("\n===== C. ad groups in enabled Search campaigns + 7d spend")
def c():
    sp = {}
    for r in q(f"SELECT ad_group.id, metrics.cost_micros, metrics.conversions FROM ad_group WHERE {W7} AND campaign.id IN ({BR},{NB})"):
        sp[r["ad_group"]["id"]] = (M(r["metrics"].get("cost_micros")), F(r["metrics"].get("conversions")))
    for r in q(f"SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id IN ({BR},{NB}) AND ad_group.status != 'REMOVED'"):
        g = r["ad_group"]; s = sp.get(g["id"], (0, 0))
        print(f"  {r['campaign']['name'][:28]:<28} {g['name'][:30]:<30} {g['status']:<8} 7d ${s[0]:,.2f} conv {s[1]:.1f}")
safe("C", c)

print("\n===== D. location targets (non-removed campaigns)")
def d():
    for r in q("""SELECT campaign.name, campaign.status, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius,
        campaign_criterion.proximity.radius_units, campaign_criterion.negative, campaign_criterion.type FROM campaign_criterion
        WHERE campaign.status = 'ENABLED' AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"""):
        cc = r["campaign_criterion"]
        print(f"  {r['campaign']['name'][:34]:<34} {cc.get('type')} {'NEG' if cc.get('negative') else '   '} {cc.get('location',{}).get('geo_target_constant') or cc.get('proximity')}")
safe("D", d)

FEE = re.compile(r"fee|24/7|24 hours|weekend|holiday|night|overtime", re.I)
print("\n===== E. enabled RSAs: approval, final URL, every fee/24-7/weekend line")
def e():
    for r in q(f"""SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.policy_summary.approval_status FROM ad_group_ad
        WHERE campaign.id IN ({BR},{NB}) AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'"""):
        a = r["ad_group_ad"]; rsa = a["ad"].get("responsive_search_ad", {})
        lines = [h.get("text", "") for h in rsa.get("headlines", [])] + [x.get("text", "") for x in rsa.get("descriptions", [])]
        hits = [l for l in lines if FEE.search(l)]
        print(f"  {r['campaign']['name'][:22]:<22} {r['ad_group']['name'][:24]:<24} ad {a['ad']['id']} {a['policy_summary'].get('approval_status')} {a['ad'].get('final_urls')}")
        for h in hits:
            print(f"      ! {h}")
safe("E", e)

print("\n===== F. assets linked (callout/sitelink/snippet) with fee/24-7 text")
def f():
    for lvl, res in (("campaign", "campaign_asset"), ("customer", "customer_asset"), ("ad_group", "ad_group_asset")):
        camp = "campaign.id, campaign.name, " if lvl in ("campaign", "ad_group") else ""
        where = f"AND campaign.id IN ({BR},{NB})" if lvl in ("campaign", "ad_group") else ""
        for r in q(f"""SELECT {camp}{res}.field_type, {res}.status, asset.callout_asset.callout_text, asset.sitelink_asset.link_text,
            asset.sitelink_asset.description1, asset.sitelink_asset.description2, asset.structured_snippet_asset.values FROM {res}
            WHERE {res}.status = 'ENABLED' {where}"""):
            a = r["asset"]
            txt = " | ".join(filter(None, [a.get("callout_asset", {}).get("callout_text"), a.get("sitelink_asset", {}).get("link_text"),
                                          a.get("sitelink_asset", {}).get("description1"), a.get("sitelink_asset", {}).get("description2"),
                                          ", ".join(a.get("structured_snippet_asset", {}).get("values", []) or [])]))
            if FEE.search(txt):
                print(f"  {lvl:<8} {r.get('campaign',{}).get('name','')[:24]:<24} {r[res]['field_type']}: {txt}")
safe("F", f)

print("\n===== G. conversion actions (enabled) + 7d / 14d")
def g():
    c7, c14 = {}, {}
    for win, dct in ((W7, c7), ("segments.date BETWEEN '2026-11-06' AND '2026-11-19'", c14)):
        for r in q(f"SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE {win}"):
            dct[r["segments"]["conversion_action_name"]] = (F(r["metrics"].get("all_conversions")), F(r["metrics"].get("conversions")))
    for r in q("SELECT conversion_action.name, conversion_action.type, conversion_action.primary_for_goal, conversion_action.category FROM conversion_action WHERE conversion_action.status = 'ENABLED'"):
        a = r["conversion_action"]
        print(f"  {a['name'][:42]:<42} {str(a.get('type'))[:24]:<24} {a.get('category','')[:18]:<18} {'PRIMARY' if a.get('primary_for_goal') else 'secondary'} | 7d all/conv {c7.get(a['name'],(0,0))} 14d {c14.get(a['name'],(0,0))}")
safe("G", g)

print("\n===== H. change_event since 11-16")
def h():
    for r in q("""SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
        change_event.changed_fields, campaign.name FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-16 00:00:00' AND '2026-11-20 23:59:59'
        ORDER BY change_event.change_date_time LIMIT 200"""):
        c = r["change_event"]
        print(f"  {c['change_date_time']} {c.get('user_email')} {c.get('change_resource_type')} {c.get('resource_change_operation')} {r.get('campaign',{}).get('name','')[:30]} {str(c.get('changed_fields',''))[:120]}")
safe("H", h)
