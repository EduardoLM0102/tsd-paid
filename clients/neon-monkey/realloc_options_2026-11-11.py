# READ-ONLY. 2026-11-11: where could NB Trimming's budget go after the pause? (seasonal campaigns, PMax headroom, LSA)
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, LSA = "7953905280", "1219885876"
HL, LC, PMAX = 18787352551, 19146431184, 21225221220
c = init_client(); ga = c.get_service("GoogleAdsService")
m = lambda x: x / 1e6
pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"
q = lambda cid, s: list(ga.search(customer_id=cid, query=s))

print("=== Seasonal campaigns: settings ===")
for r in q(CID, f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type,
        campaign_budget.amount_micros, campaign.network_settings.target_search_network,
        campaign.network_settings.target_content_network, campaign.geo_target_type_setting.positive_geo_target_type
        FROM campaign WHERE campaign.id IN ({HL}, {LC})"""):
    x = r.campaign
    print(f"  {x.id} {x.name} {x.status.name} {x.advertising_channel_type.name} {x.bidding_strategy_type.name} bud ${m(r.campaign_budget.amount_micros):.0f}"
          f" partners={x.network_settings.target_search_network} display={x.network_settings.target_content_network}"
          f" geo={x.geo_target_type_setting.positive_geo_target_type.name}")

print("\n=== Seasonal campaigns: history by month (all time) ===")
for r in q(CID, f"""SELECT campaign.name, segments.month, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
        FROM campaign WHERE campaign.id IN ({HL}, {LC}) AND segments.date BETWEEN '2022-01-01' AND '2026-11-10' AND metrics.impressions > 0
        ORDER BY segments.month"""):
    x = r.metrics
    print(f"  {r.campaign.name[:30]:30s} {r.segments.month} ${m(x.cost_micros):8.2f} {x.impressions:6d} impr {x.clicks:4d} clk conv {x.conversions:4.1f}")

print("\n=== Seasonal campaigns: ads (final URLs, status) ===")
for r in q(CID, f"""SELECT campaign.name, ad_group.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls
        FROM ad_group_ad WHERE campaign.id IN ({HL}, {LC}) AND ad_group_ad.status != 'REMOVED'"""):
    a = r.ad_group_ad
    print(f"  {r.campaign.name[:24]:24s} {r.ad_group.name[:26]:26s} {a.status.name:8s} {a.policy_summary.approval_status.name:12s} {list(a.ad.final_urls)}")

print("\n=== Seasonal campaigns: keywords ===")
for r in q(CID, f"""SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
        FROM ad_group_criterion WHERE campaign.id IN ({HL}, {LC}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
        AND ad_group_criterion.status != 'REMOVED'"""):
    k = r.ad_group_criterion
    print(f"  {r.campaign.name[:24]:24s} {k.keyword.text} [{k.keyword.match_type.name}] {k.status.name}")

print("\n=== Seasonal campaigns: geo ===")
for r in q(CID, f"""SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.proximity.radius,
        campaign_criterion.negative, campaign_criterion.type FROM campaign_criterion WHERE campaign.id IN ({HL}, {LC})
        AND campaign_criterion.type IN ('LOCATION', 'PROXIMITY')"""):
    cc = r.campaign_criterion
    print(f"  {r.campaign.name[:24]:24s} {cc.type_.name} {cc.location.geo_target_constant or ''} {cc.proximity.radius or ''} neg={cc.negative}")

print("\n=== PMax + Branded headroom, last 14 days ===")
for r in q(CID, f"""SELECT campaign.name, campaign_budget.amount_micros, metrics.cost_micros, metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share, metrics.search_impression_share FROM campaign
        WHERE campaign.status = 'ENABLED' AND segments.date BETWEEN '2026-10-28' AND '2026-11-10'"""):
    x = r.metrics
    print(f"  {r.campaign.name[:40]:40s} bud ${m(r.campaign_budget.amount_micros):4.0f} spend/d ${m(x.cost_micros)/14:6.2f}"
          f" IS {pct(x.search_impression_share)} lostB {pct(x.search_budget_lost_impression_share)} lostR {pct(x.search_rank_lost_impression_share)}")

print("\n=== LSA last 30 days ===")
rows = q(LSA, """SELECT campaign.name, campaign.status, campaign_budget.amount_micros, metrics.cost_micros, metrics.impressions
        FROM campaign WHERE segments.date BETWEEN '2026-10-12' AND '2026-11-10'""")
for r in rows:
    print(f"  {r.campaign.name[:40]} {r.campaign.status.name} bud ${m(r.campaign_budget.amount_micros):.0f} spend ${m(r.metrics.cost_micros):.2f} ({m(r.metrics.cost_micros)/30:.2f}/d) impr {r.metrics.impressions}")
leads = q(LSA, """SELECT local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time
        FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-10-12 00:00:00'""")
print(f"  leads {len(leads)}, charged {sum(1 for l in leads if l.local_services_lead.lead_charged)}, booked {sum(1 for l in leads if l.local_services_lead.lead_status.name == 'BOOKED')}")

print("\n=== PPC account monthly spend 2026 ===")
for r in q(CID, """SELECT segments.month, metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-06-01' AND '2026-11-10'"""):
    print(f"  {r.segments.month} ${m(r.metrics.cost_micros):,.2f}")
