# READ-ONLY. Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
"""Napps (PPC 9509605037, LSA 9239407401) Post Client Strategy Review alignment (AT 73c502b8), 2026-11-20.
Presented on the 11-19 review (0de4a6cc): keep every setting (~$5,300/mo: Google ~$3,200, LSA ~$2,000, Meta ~$150), split 65/35 HVAC/plumbing,
Tyler -50% on Heating (11-17), current_specials = $89 Diagnostic / $89 Fall Tune-Up (agreed 09-24).
Checks: budgets + bidding/cap, spend since the call, enabled ad groups, geo + Tyler modifier, ad copy offers + final URLs, primary conversions, LSA budget, change_event."""
import sys, re
sys.path.insert(0, ".")
from lib import run_query

CID, LSA = "9509605037", "9239407401"
BR, HT, PL = "23685615826", "24049055193", "23819717682"
IDS = f"campaign.id IN ({BR},{HT},{PL})"
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)

def safe(label, fn):
    try:
        fn()
    except BaseException as e:
        print(f"  !! {label} failed: {e}")

print("===== A. PPC campaigns: status, budget, bidding")
def a():
    for r in run_query(CID, """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.advertising_channel_type, campaign.bidding_strategy_type,
        campaign.target_spend.cpc_bid_ceiling_micros, campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.target_impression_share.location_fraction_micros,
        campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.status = 'ENABLED'"""):
        c = r["campaign"]
        ceil = M(c.get("target_spend", {}).get("cpc_bid_ceiling_micros") or c.get("target_impression_share", {}).get("cpc_bid_ceiling_micros"))
        print(f"  {c['id']} {c['name'][:44]:<44} {c['status']}/{c.get('primary_status')} {c['advertising_channel_type'][:6]} {c.get('bidding_strategy_type')} "
              f"bud ${M(r['campaign_budget'].get('amount_micros')):.2f} cap ${ceil:.2f} geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')}")
safe("A", a)

for label, win, days in (("B. spend 11-19..11-20 (since the call)", "segments.date BETWEEN '2026-11-19' AND '2026-11-20'", 2),
                         ("B2. spend 7d 11-13..11-19", "segments.date BETWEEN '2026-11-13' AND '2026-11-19'", 7),
                         ("B3. spend Nov 1-19", "segments.date BETWEEN '2026-11-01' AND '2026-11-19'", 19)):
    print(f"\n===== {label}")
    def b(win=win, days=days):
        sp = {}
        for r in run_query(CID, f"""SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.all_conversions,
            metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE {win} AND metrics.cost_micros > 0"""):
            c, m = r["campaign"], r["metrics"]; s = M(m.get("cost_micros")); sp[c["id"]] = s
            print(f"  {c['id']} {c['name'][:40]:<40} ${s:,.2f} (${s/days:,.0f}/d) clk {m.get('clicks',0)} conv {F(m.get('conversions')):.1f} all {F(m.get('all_conversions')):.1f} "
                  f"IS {F(m.get('search_impression_share'))*100:.0f} bud-lost {F(m.get('search_budget_lost_impression_share'))*100:.0f} rank-lost {F(m.get('search_rank_lost_impression_share'))*100:.0f}")
        nb = sp.get(HT, 0) + sp.get(PL, 0)
        print(f"  TOTAL ${sum(sp.values()):,.2f} | NB split Heating {sp.get(HT,0)/nb*100 if nb else 0:.0f}% / Plumbing {sp.get(PL,0)/nb*100 if nb else 0:.0f}% (target 65/35)")
    safe(label, b)

print("\n===== C. ad groups (non-removed) in the 3 campaigns")
def c():
    for r in run_query(CID, f"SELECT campaign.name, ad_group.name, ad_group.status FROM ad_group WHERE {IDS} AND ad_group.status != 'REMOVED'"):
        print(f"  {r['campaign']['name'][:36]:<36} {r['ad_group']['name'][:30]:<30} {r['ad_group']['status']}")
safe("C", c)

print("\n===== D. location targets + bid modifiers (enabled campaigns)")
def d():
    for r in run_query(CID, f"""SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.negative, campaign_criterion.bid_modifier,
        campaign_criterion.type, campaign_criterion.proximity.radius FROM campaign_criterion WHERE {IDS} AND campaign_criterion.type IN ('LOCATION','PROXIMITY')"""):
        cc = r["campaign_criterion"]
        print(f"  {r['campaign']['name'][:36]:<36} {'NEG' if cc.get('negative') else '   '} {cc.get('location',{}).get('geo_target_constant') or cc.get('proximity')} mod {cc.get('bid_modifier','-')}")
safe("D", d)

OFFER = re.compile(r"\$\d+|diagnostic|tune.?up|special|off\b|coupon|free|longview|tyler", re.I)
print("\n===== E. enabled RSAs: approval, final URL, offer/city lines")
def e():
    for r in run_query(CID, f"""SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.policy_summary.approval_status FROM ad_group_ad
        WHERE {IDS} AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'"""):
        a = r["ad_group_ad"]; rsa = a["ad"].get("responsive_search_ad", {})
        lines = [h.get("text", "") for h in rsa.get("headlines", [])] + [x.get("text", "") for x in rsa.get("descriptions", [])]
        print(f"  {r['campaign']['name'][:26]:<26} {r['ad_group']['name'][:22]:<22} ad {a['ad']['id']} {a['policy_summary'].get('approval_status')} {a['ad'].get('final_urls')}")
        for l in lines:
            if OFFER.search(l):
                print(f"      > {l}")
safe("E", e)

print("\n===== F. assets with offer text (callouts, sitelinks, promotions)")
def f():
    for lvl, res, extra in (("campaign", "campaign_asset", "campaign.id, campaign.name, "), ("customer", "customer_asset", "")):
        where = f"AND {IDS}" if lvl == "campaign" else ""
        for r in run_query(CID, f"""SELECT {extra}{res}.field_type, asset.callout_asset.callout_text, asset.sitelink_asset.link_text, asset.sitelink_asset.description1,
            asset.promotion_asset.promotion_target, asset.promotion_asset.money_amount_off.amount_micros, asset.promotion_asset.end_date FROM {res}
            WHERE {res}.status = 'ENABLED' {where}"""):
            a = r["asset"]; ft = r[res]["field_type"]
            txt = " | ".join(filter(None, [a.get("callout_asset", {}).get("callout_text"), a.get("sitelink_asset", {}).get("link_text"),
                                          a.get("sitelink_asset", {}).get("description1"), a.get("promotion_asset", {}).get("promotion_target")]))
            if ft == "PROMOTION" or OFFER.search(txt):
                print(f"  {lvl:<8} {r.get('campaign',{}).get('name','')[:26]:<26} {ft}: {txt} {a.get('promotion_asset',{}).get('end_date','')}")
safe("F", f)

print("\n===== G. conversion actions (enabled) + 14d")
def g():
    cnt = {}
    for r in run_query(CID, "SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-11-06' AND '2026-11-19'"):
        cnt[r["segments"]["conversion_action_name"]] = (F(r["metrics"].get("all_conversions")), F(r["metrics"].get("conversions")))
    for r in run_query(CID, "SELECT conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.status = 'ENABLED'"):
        a = r["conversion_action"]
        print(f"  {a['name'][:40]:<40} {a.get('category','')[:18]:<18} {'PRIMARY' if a.get('primary_for_goal') else 'secondary'} | 14d all/conv {cnt.get(a['name'],(0,0))}")
    print("  campaign conversion goals (biddable):")
    for r in run_query(CID, f"SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE {IDS}"):
        g = r["campaign_conversion_goal"]
        if g.get("biddable"):
            print(f"    {r['campaign']['name'][:36]:<36} {g.get('category')} {g.get('origin')}")
safe("G", g)

print("\n===== H. LSA 9239407401: budget, spend, leads since 11-13")
def h():
    for r in run_query(LSA, "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros FROM campaign WHERE campaign.status != 'REMOVED'"):
        c = r["campaign"]; print(f"  {c['id']} {c['name'][:40]} {c['status']} {c['advertising_channel_type']} ${M(r['campaign_budget'].get('amount_micros')):.2f}/d")
    for r in run_query(LSA, "SELECT segments.week, metrics.cost_micros, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2026-11-02' AND '2026-11-20' ORDER BY segments.week"):
        print(f"   week {r['segments']['week']} ${M(r['metrics'].get('cost_micros')):.2f} impr {r['metrics'].get('impressions')}")
    for r in run_query(LSA, "SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.lead_status, local_services_lead.lead_charged FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-13 00:00:00'"):
        l = r["local_services_lead"]; print(f"   {l['creation_date_time'][:16]} {l['lead_type'][:5]} {l.get('category_id','')[:30]} {l['lead_status']} {'charged' if l.get('lead_charged') else '-'}")
safe("H", h)

print("\n===== I. change_event since 11-17 (PPC)")
def i():
    for r in run_query(CID, """SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
        change_event.changed_fields, campaign.name FROM change_event WHERE change_event.change_date_time BETWEEN '2026-11-17 00:00:00' AND '2026-11-20 23:59:59'
        ORDER BY change_event.change_date_time LIMIT 100"""):
        c = r["change_event"]
        print(f"  {c['change_date_time']} {c.get('user_email')} {c.get('change_resource_type')} {c.get('resource_change_operation')} {r.get('campaign',{}).get('name','')[:30]} {str(c.get('changed_fields',''))[:100]}")
safe("I", i)
