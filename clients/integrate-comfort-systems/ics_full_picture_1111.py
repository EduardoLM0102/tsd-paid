# READ-ONLY. 2026-11-11: whole-account picture for ICS before proposing a turnaround.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
import sys, collections
sys.path.insert(0, ".")
from lib import run_query

PPC = "4571881760"
LSA = {"2895702982": "LSA Belleville", "2175964343": "LSA 2175964343", "8323145223": "LSA 8323145223"}
PM, NB, BR = "22890783804", "24047025253", "23675636592"
M = lambda x: int(x or 0) / 1e6
F = lambda x: float(x or 0)
pct = lambda x: f"{F(x)*100:.0f}%"

if False: print("===== 1. LSA accounts, last 30 days (10-12..11-10): spend + leads")
for cid, name in ({} if True else LSA).items():
    try:
        camps = run_query(cid, """SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros,
            metrics.cost_micros, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2026-10-12' AND '2026-11-10'""")
        for r in camps:
            c = r["campaign"]
            print(f"  {name:16s} {c['id']} {c['name'][:40]:40s} {c.get('advertising_channel_type')} {c['status']} bud ${M(r['campaign_budget'].get('amount_micros')):.0f}/d"
                  f" spend ${M(r['metrics'].get('cost_micros')):.2f} impr {r['metrics'].get('impressions', 0)}")
        leads = run_query(cid, """SELECT local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.lead_status,
            local_services_lead.lead_charged, local_services_lead.creation_date_time FROM local_services_lead
            WHERE local_services_lead.creation_date_time >= '2026-10-12 00:00:00'""")
        st = collections.Counter(l["local_services_lead"]["lead_status"] for l in leads)
        ch = sum(1 for l in leads if l["local_services_lead"].get("lead_charged"))
        print(f"  {name:16s} leads {len(leads)}, charged {ch}, statuses {dict(st)}")
        for l in sorted(leads, key=lambda l: l["local_services_lead"]["creation_date_time"])[-8:]:
            x = l["local_services_lead"]
            print(f"     {x['creation_date_time'][:16]} {x['lead_type']:12s} {x['category_id'].replace('xcat:service_area_business_', ''):10s} {x['lead_status']:16s} charged={x.get('lead_charged', False)}")
    except Exception as e:
        print(f"  {name}: ERROR {str(e).splitlines()[0][:160]}")

print("\n===== 2. PPC campaigns: geo + location type + schedule")
for r in run_query(PPC, f"""SELECT campaign.id, campaign.name, campaign.geo_target_type_setting.positive_geo_target_type,
        campaign.network_settings.target_search_network, campaign.network_settings.target_content_network
        FROM campaign WHERE campaign.id IN ({PM},{NB},{BR})"""):
    c = r["campaign"]
    print(f"  {c['id']} {c['name'][:40]:40s} geo={c['geo_target_type_setting'].get('positive_geo_target_type')} partners={c['network_settings'].get('target_search_network')} display={c['network_settings'].get('target_content_network')}")
locs = collections.defaultdict(list)
for r in run_query(PPC, f"""SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant,
        campaign_criterion.proximity.radius, campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour, campaign_criterion.ad_schedule.end_hour
        FROM campaign_criterion WHERE campaign.id IN ({PM},{NB},{BR}) AND campaign_criterion.type IN ('LOCATION','PROXIMITY','AD_SCHEDULE')"""):
    cc = r["campaign_criterion"]; k = r["campaign"]["id"]; ct = cc.get("type") or cc.get("type_")
    if ct == "AD_SCHEDULE":
        locs[k].append(f"sched {cc['ad_schedule']['day_of_week']} {cc['ad_schedule']['start_hour']}-{cc['ad_schedule']['end_hour']}")
    elif ct == "PROXIMITY":
        locs[k].append(f"radius {cc['proximity'].get('radius')}")
    else:
        locs[k].append(("-" if cc.get("negative") else "+") + str(cc["location"]["geo_target_constant"]).split("/")[-1])
for k, v in locs.items():
    print(f"  {k}: {len(v)} criteria: {', '.join(v[:40])}")
ids = sorted({x[1:] for v in locs.values() for x in v if x[0] in "+-"})
if ids:
    names = {}
    for r in run_query(PPC, f"SELECT geo_target_constant.id, geo_target_constant.name, geo_target_constant.target_type FROM geo_target_constant WHERE geo_target_constant.id IN ({','.join(ids)})"):
        g = r["geo_target_constant"]; names[str(g["id"])] = f"{g['name']} ({g['target_type']})"
    print("  geo names:", "; ".join(f"{k}={v}" for k, v in names.items()))

print("\n===== 3. NonBranded: ad groups, keywords, final URLs, QS")
for r in run_query(PPC, f"""SELECT ad_group.name, ad_group.status, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
        ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.post_click_quality_score,
        ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.position_estimates.first_page_cpc_micros, ad_group_criterion.position_estimates.top_of_page_cpc_micros,
        metrics.impressions, metrics.clicks, metrics.cost_micros FROM keyword_view WHERE campaign.id = {NB} AND ad_group_criterion.status != 'REMOVED'
        AND segments.date BETWEEN '2026-10-29' AND '2026-11-10'"""):
    k = r["ad_group_criterion"]; qi = k.get("quality_info", {}); pe = k.get("position_estimates", {}); m = r["metrics"]
    print(f"  {r['ad_group']['name'][:28]:28s} {r['ad_group']['status'][:7]:7s} | {k['keyword']['text'][:36]:36s} [{k['keyword']['match_type'][:6]}] {k['status'][:7]:7s}"
          f" QS {qi.get('quality_score', '-')} ctr={qi.get('search_predicted_ctr', '-')} lp={qi.get('post_click_quality_score', '-')} ad={qi.get('creative_quality_score', '-')}"
          f" 1st ${M(pe.get('first_page_cpc_micros')):.2f} top ${M(pe.get('top_of_page_cpc_micros')):.2f} | impr {m.get('impressions', 0)} clk {m.get('clicks', 0)} ${M(m.get('cost_micros')):.2f}")
for r in run_query(PPC, f"""SELECT ad_group.name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad WHERE campaign.id IN ({NB},{BR}) AND ad_group_ad.status != 'REMOVED'"""):
    a = r["ad_group_ad"]
    print(f"  AD {r['ad_group']['name'][:28]:28s} {a['status']:8s} {a.get('ad_strength', '-'):10s} {a['policy_summary']['approval_status']:10s} {a['ad'].get('final_urls')}")

print("\n===== 4. Branded: keywords + CPC vs $7 cap, last 13d")
for r in run_query(PPC, f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros,
        metrics.search_impression_share, metrics.search_absolute_top_impression_share FROM keyword_view WHERE campaign.id = {BR}
        AND segments.date BETWEEN '2026-10-29' AND '2026-11-10' AND metrics.impressions > 0"""):
    k = r["ad_group_criterion"]; m = r["metrics"]
    print(f"  {k['keyword']['text'][:36]:36s} [{k['keyword']['match_type'][:6]}] impr {m.get('impressions', 0):>3} clk {m.get('clicks', 0)} ${M(m.get('cost_micros')):.2f} IS {pct(m.get('search_impression_share'))} abs-top {pct(m.get('search_absolute_top_impression_share'))}")
for r in run_query(PPC, f"SELECT campaign.target_impression_share.location, campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros FROM campaign WHERE campaign.id = {BR}"):
    t = r["campaign"]["target_impression_share"]; print(f"  Target IS: {t.get('location')} {M(t.get('location_fraction_micros'))*100:.0f}% ceiling ${M(t.get('cpc_bid_ceiling_micros')):.2f}")

print("\n===== 5. PMax asset groups + final URLs + search themes")
for r in run_query(PPC, f"SELECT asset_group.id, asset_group.name, asset_group.status, asset_group.final_urls, asset_group.ad_strength FROM asset_group WHERE campaign.id = {PM}"):
    g = r["asset_group"]; print(f"  {g['id']} {g['name'][:40]:40s} {g['status']} {g.get('ad_strength', '-')} {g.get('final_urls')}")
for r in run_query(PPC, f"SELECT asset_group.name, asset_group_signal.search_theme.text, asset_group_signal.audience.audience FROM asset_group_signal WHERE campaign.id = {PM}"):
    s = r["asset_group_signal"]; print(f"     signal {r['asset_group']['name'][:24]:24s} theme={s.get('search_theme', {}).get('text')} aud={s.get('audience', {}).get('audience')}")

print("\n===== 6. PMax search categories last 13d (what Search it actually buys)")
try:
    for r in run_query(PPC, f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.impressions, metrics.conversions
            FROM campaign_search_term_insight WHERE campaign_search_term_insight.campaign_id = {PM} AND segments.date BETWEEN '2026-10-29' AND '2026-11-10'
            ORDER BY metrics.clicks DESC LIMIT 20"""):
        i = r["campaign_search_term_insight"]; m = r["metrics"]
        print(f"  {i['category_label'][:50]:50s} impr {m.get('impressions', 0):>4} clk {m.get('clicks', 0):>3} conv {F(m.get('conversions')):.1f}")
except Exception as e:
    print("  ERROR", str(e).splitlines()[0][:160])

print("\n===== 7. Account monthly spend 2026 + conversions by month (all_conversions excl. page_view)")
for r in run_query(PPC, "SELECT segments.month, metrics.cost_micros, metrics.conversions FROM customer WHERE segments.date BETWEEN '2026-01-01' AND '2026-11-10'"):
    print(f"  {r['segments']['month']} ${M(r['metrics'].get('cost_micros')):,.2f} conv {F(r['metrics'].get('conversions')):.0f}")
