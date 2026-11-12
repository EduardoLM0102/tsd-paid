# READ-ONLY. fu-091 (11-09): where can C&S's spare ~$100/day go? Second heating week + LSA reach after insurance PASSED + Branded.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""C&S Air (5563867754). Approved total $238/day. Live: Branded, Heating Search 24383234148 ($30/d, Max Clicks $12 cap,
26 negatives added 11-02), LSA 15794404030 ($55/d since 11-02, insurance PASSED 11-02). PMax + Cooling paused 10-23."""
import sys, traceback
sys.path.insert(0, ".")
from lib import init_client

CID, HEAT, LSA = "5563867754", "24383234148", "15794404030"
c = init_client(); ga = c.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
m = lambda x: x / 1e6
pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"


def section(t, fn):
    print("\n=== " + t + " ===")
    try: fn()
    except Exception as e: print("ERROR:", str(e).splitlines()[0][:300]); traceback.print_exc(limit=1)


def campaigns():
    print("timezone:", q("SELECT customer.time_zone FROM customer")[0].customer.time_zone)
    for r in q("""SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
        campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros FROM campaign WHERE campaign.status = 'ENABLED'"""):
        print(f"  {r.campaign.id} {r.campaign.name[:44]:44s} {r.campaign.advertising_channel_type.name[:14]:14s} ${m(r.campaign_budget.amount_micros):6.2f}/d"
              f" {r.campaign.bidding_strategy_type.name} cap ${m(r.campaign.target_spend.cpc_bid_ceiling_micros):.0f} | {r.campaign.primary_status.name} {[x.name for x in r.campaign.primary_status_reasons]}")


def daily():
    rows = q("""SELECT segments.date, segments.day_of_week, campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.impressions,
        metrics.clicks, metrics.conversions, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2026-10-27' AND '2026-11-09'
        AND metrics.impressions > 0 ORDER BY segments.date""")
    day = {}
    for r in rows:
        n = "LSA" if r.campaign.advertising_channel_type.name == "LOCAL_SERVICES" else "Heat" if "Heating" in r.campaign.name else "Brand" if "Brand" in r.campaign.name else r.campaign.name[:12]
        day.setdefault((r.segments.date, r.segments.day_of_week.name[:3]), {})[n] = (m(r.metrics.cost_micros), r.metrics.impressions, r.metrics.clicks, r.metrics.conversions)
    for (d, dow), cs in day.items():
        print(f"  {d} {dow} total ${sum(v[0] for v in cs.values()):6.2f} | " + "  ".join(f"{n} ${v[0]:.0f}/{v[1]}i/{v[2]}c/{v[3]:.0f}cv" for n, v in sorted(cs.items())))


def windows():
    for lo, hi, tag in [("2026-10-27", "2026-11-02", "week 1  10-27..11-02"), ("2026-11-03", "2026-11-08", "week 2  11-03..11-08 (6 days, after the 26 negatives)")]:
        print("--", tag)
        for r in q(f"""SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc,
            metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_budget_lost_impression_share,
            metrics.search_rank_lost_impression_share, metrics.search_absolute_top_impression_share FROM campaign
            WHERE segments.date BETWEEN '{lo}' AND '{hi}' AND metrics.impressions > 0"""):
            x = r.metrics
            print(f"   {r.campaign.name[:40]:40s} ${m(x.cost_micros):7.2f} {x.impressions:5d} impr {x.clicks:3d} clk cpc ${m(x.average_cpc):5.2f} conv {x.conversions:3.1f} all {x.all_conversions:3.1f}"
                  f" | IS {pct(x.search_impression_share)} lostB {pct(x.search_budget_lost_impression_share)} lostR {pct(x.search_rank_lost_impression_share)} abs {pct(x.search_absolute_top_impression_share)}")


def heating():
    print("-- keywords, 11-03..11-09")
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score,
        metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc, metrics.conversions, metrics.search_impression_share,
        metrics.search_rank_lost_impression_share FROM keyword_view WHERE campaign.id = {HEAT} AND segments.date BETWEEN '2026-11-03' AND '2026-11-09'
        AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC"""):
        x = r.metrics; k = r.ad_group_criterion
        print(f"   {r.ad_group.name[:22]:22s} [{k.keyword.match_type.name[:3]}] {k.keyword.text[:34]:34s} QS {k.quality_info.quality_score:2d} ${m(x.cost_micros):6.2f} {x.impressions:4d} impr"
              f" {x.clicks:2d} clk cpc ${m(x.average_cpc):5.2f} conv {x.conversions:.0f} IS {pct(x.search_impression_share)} lostR {pct(x.search_rank_lost_impression_share)}")
    print("-- search terms, 11-03..11-09 (after the negatives)")
    rows = q(f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions FROM search_term_view
        WHERE campaign.id = {HEAT} AND segments.date BETWEEN '2026-11-03' AND '2026-11-09' AND metrics.impressions > 0""")
    print(f"   visible: {len(rows)} terms, ${sum(m(r.metrics.cost_micros) for r in rows):.2f}, {sum(r.metrics.clicks for r in rows)} clicks")
    for r in sorted(rows, key=lambda r: (-r.metrics.cost_micros, -r.metrics.impressions))[:45]:
        print(f"   ${m(r.metrics.cost_micros):6.2f} {r.metrics.clicks:2d} clk {r.metrics.impressions:3d} impr conv {r.metrics.conversions:.0f} | {r.search_term_view.search_term}")
    print("-- conversions by action, account, 10-27..11-09")
    agg = {}
    for r in q("""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM campaign
        WHERE segments.date BETWEEN '2026-10-27' AND '2026-11-09'"""):
        a = agg.setdefault((r.campaign.name[:40], r.segments.conversion_action_name), [0, 0]); a[0] += r.metrics.conversions; a[1] += r.metrics.all_conversions
    for k, v in sorted(agg.items()): print(f"   {k[0]:40s} {k[1]:36s} conv {v[0]:4.1f} all {v[1]:4.1f}")
    print("-- calls from ads since 10-27")
    rows = q("""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, campaign.name FROM call_view
        WHERE call_view.start_call_date_time >= '2026-10-27 00:00:00' ORDER BY call_view.start_call_date_time""")
    for r in rows: print(f"   {r.call_view.start_call_date_time} {r.call_view.call_duration_seconds}s {r.call_view.call_status.name} | {r.campaign.name}")
    print(f"   {len(rows)} calls from ads")


def branded():
    for r in q("""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status,
        ad_group_ad.policy_summary.review_status, ad_group_ad.primary_status, campaign.name FROM ad_group_ad
        WHERE campaign.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'"""):
        a = r.ad_group_ad
        print(f"   {r.campaign.name[:34]:34s} {r.ad_group.name[:22]:22s} ad {a.ad.id} {a.ad_strength.name:9s} {a.policy_summary.approval_status.name} {a.policy_summary.review_status.name} {a.primary_status.name}")


def lsa():
    s = q("SELECT customer.local_services_settings.granular_insurance_statuses, customer.local_services_settings.granular_license_statuses FROM customer")[0].customer.local_services_settings
    print("   insurance:", [(x.category_id, x.verification_status.name) for x in s.granular_insurance_statuses], "| license:", [(x.category_id, x.verification_status.name) for x in s.granular_license_statuses])
    rows = q(f"""SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM campaign
        WHERE campaign.id = {LSA} AND segments.date BETWEEN '2026-10-20' AND '2026-11-09' ORDER BY segments.date""")
    print("   impressions/day:", " ".join(f"{r.segments.date[5:]}:{r.metrics.impressions}" for r in rows))
    print("   cost/day:       ", " ".join(f"{r.segments.date[5:]}:${m(r.metrics.cost_micros):.0f}" for r in rows if r.metrics.cost_micros))
    leads = q("""SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.service_id,
        local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time FROM local_services_lead
        WHERE local_services_lead.creation_date_time >= '2026-10-20 00:00:00'""")
    for r in sorted(leads, key=lambda r: r.local_services_lead.creation_date_time):
        l = r.local_services_lead
        print(f"   {l.creation_date_time[:16]} {l.lead_type.name:11s} {l.service_id[:34]:34s} {l.lead_status.name:17s} charged={l.lead_charged}")
    print(f"   {len(leads)} leads since 10-20, {sum(bool(r.local_services_lead.lead_charged) for r in leads)} charged; since 11-02: "
          f"{sum(1 for r in leads if r.local_services_lead.creation_date_time >= '2026-11-02')} leads, "
          f"{sum(1 for r in leads if r.local_services_lead.creation_date_time >= '2026-11-02' and r.local_services_lead.lead_charged)} charged")
    for lo, hi in [("2026-08-01", "2026-09-10"), ("2026-09-11", "2026-11-01"), ("2026-11-02", "2026-11-09")]:
        r = q(f"SELECT metrics.impressions, metrics.cost_micros, metrics.clicks FROM campaign WHERE campaign.id = {LSA} AND segments.date BETWEEN '{lo}' AND '{hi}'")
        days = (__import__('datetime').date.fromisoformat(hi) - __import__('datetime').date.fromisoformat(lo)).days + 1
        imp = sum(x.metrics.impressions for x in r); cost = sum(m(x.metrics.cost_micros) for x in r)
        print(f"   {lo}..{hi}: {imp} impr ({imp/days:.0f}/day), ${cost:.2f} (${cost/days:.2f}/day)")


section("1. Enabled campaigns", campaigns)
section("2. Daily, all campaigns, 10-27..11-09 (cost / impr / clicks / conv)", daily)
section("3. Week 1 vs week 2", windows)
section("4. Heating detail", heating)
section("5. Search ads status", branded)
section("6. LSA", lsa)
