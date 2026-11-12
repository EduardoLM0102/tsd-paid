# READ-ONLY. fu-054 November pacing check + "nothing broke" check after the 11-09 fixes.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""Accounts: PPC 1051843378, LSA SA [1] 7261668241, LSA SA [2] 6621969129 (+ My Favorite Service 9815330464 for info).
Caps since 11-09: Branded $50, Electrical $455, HVAC $230 (portfolio $30 CPC ceiling, tCPA $265), Plumbing $145 = $880/d.
Fixes applied 11-09 ~08:50 CT, so 11-10 is the first full day after them."""
import sys, traceback
sys.path.insert(0, ".")
from lib import init_client

PPC = "1051843378"
ACCOUNTS = [("PPC", PPC), ("LSA SA [1] electrician", "7261668241"), ("LSA SA [2] HVAC", "6621969129"),
            ("My Favorite Service PPC", "9815330464")]
MTD0, TODAY = "2026-11-01", "2026-11-11"
c = init_client(); ga = c.get_service("GoogleAdsService")
m = lambda x: x / 1e6
pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"
short = lambda n: ("Elec" if "Electrical" in n else "HVAC" if "HVAC" in n else "Plumb" if "Plumbing" in n
                   else "Brand" if "Branded" in n else "LSA" if ("LocalServices" in n or "Pay-per-lead" in n) else n[:14])


def q(cid, s):
    return list(ga.search(customer_id=cid, query=s))


def section(title, fn):
    print("\n=== " + title + " ===")
    try:
        fn()
    except Exception as e:
        print("ERROR:", str(e).splitlines()[0][:300]); traceback.print_exc(limit=1)


def daily_all():
    """Daily spend per account per campaign, Nov 1 to today (today partial)."""
    for label, cid in ACCOUNTS:
        try:
            rows = q(cid, f"""SELECT segments.date, segments.day_of_week, campaign.name, campaign.advertising_channel_type,
                metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign
                WHERE segments.date BETWEEN '{MTD0}' AND '{TODAY}' AND metrics.cost_micros > 0 ORDER BY segments.date""")
        except Exception as e:
            print(f"-- {label} ({cid}) ERROR: {str(e).splitlines()[0][:200]}"); continue
        day = {}
        for r in rows:
            d = day.setdefault((r.segments.date, r.segments.day_of_week.name[:3]), {})
            k = short(r.campaign.name)
            v = d.get(k, (0, 0)); d[k] = (v[0] + m(r.metrics.cost_micros), v[1] + r.metrics.conversions)
        tot = sum(sum(v[0] for v in cs.values()) for cs in day.values())
        print(f"-- {label} ({cid}) | MTD 11-01..{TODAY[5:]} ${tot:,.2f}")
        for (d, dow), cs in day.items():
            print(f"   {d} {dow} ${sum(v[0] for v in cs.values()):7.2f} | "
                  + "  ".join(f"{n} ${v[0]:.0f}/{v[1]:.0f}" for n, v in sorted(cs.items(), key=lambda kv: -kv[1][0])))


def campaign_state():
    """Status, serving, budget, bidding for every PPC-account campaign that's enabled."""
    rows = q(PPC, """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
        campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign_budget.amount_micros
        FROM campaign WHERE campaign.status = 'ENABLED'""")
    for r in rows:
        x = r.campaign
        print(f"   {x.id} {x.name[:50]:50s} {x.advertising_channel_type.name[:12]:12s} {x.bidding_strategy_type.name[:22]:22s}"
              f" bud ${m(r.campaign_budget.amount_micros):5.0f} | {x.primary_status.name} {[s.name for s in x.primary_status_reasons]}")


def search_since_fix():
    for lo, hi, tag in [("2026-11-10", "2026-11-10", "11-10 (first full day after fixes)"),
                        ("2026-11-09", "2026-11-11", "11-09..11-11 (11-11 partial)"),
                        ("2026-11-04", "2026-11-08", "11-04..11-08 baseline")]:
        rows = q(PPC, f"""SELECT campaign.name, metrics.cost_micros, metrics.impressions, metrics.clicks,
            metrics.average_cpc, metrics.conversions, metrics.all_conversions, metrics.search_impression_share,
            metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share,
            metrics.search_absolute_top_impression_share, metrics.search_top_impression_share
            FROM campaign WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date BETWEEN '{lo}' AND '{hi}'
            AND metrics.impressions > 0""")
        print(f"-- {tag}")
        for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
            x = r.metrics; cost = m(x.cost_micros)
            print(f"   {short(r.campaign.name):6s} ${cost:8.2f} {x.impressions:5d} impr {x.clicks:3d} clk cpc ${m(x.average_cpc):6.2f}"
                  f" | leads {x.conversions:4.1f} (all {x.all_conversions:4.1f}) cpl {('$%.0f' % (cost/x.conversions)) if x.conversions else 'n/a':>5s}"
                  f" | IS {pct(x.search_impression_share)} lostB {pct(x.search_budget_lost_impression_share)}"
                  f" lostR {pct(x.search_rank_lost_impression_share)} top {pct(x.search_top_impression_share)} abs {pct(x.search_absolute_top_impression_share)}")


def branded_daily():
    rows = q(PPC, """SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.average_cpc,
        metrics.search_impression_share, metrics.search_absolute_top_impression_share, metrics.search_rank_lost_impression_share,
        metrics.conversions, campaign.bidding_strategy_system_status
        FROM campaign WHERE campaign.id = 23853361615 AND segments.date BETWEEN '2026-11-06' AND '2026-11-11' ORDER BY segments.date""")
    for r in rows:
        x = r.metrics
        print(f"   {r.segments.date} {x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):6.2f} cpc ${m(x.average_cpc):5.2f}"
              f" IS {pct(x.search_impression_share)} abs {pct(x.search_absolute_top_impression_share)} lostR {pct(x.search_rank_lost_impression_share)}"
              f" conv {x.conversions:3.1f} | {r.campaign.bidding_strategy_system_status.name}")


def hvac_cpc():
    rows = q(PPC, """SELECT segments.date, ad_group.name, metrics.clicks, metrics.cost_micros, metrics.average_cpc, metrics.impressions
        FROM ad_group WHERE campaign.id = 23848895678 AND segments.date BETWEEN '2026-11-09' AND '2026-11-11' AND metrics.impressions > 0
        ORDER BY segments.date""")
    for r in rows:
        x = r.metrics
        print(f"   {r.segments.date} {r.ad_group.name[:34]:34s} {x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):7.2f} cpc ${m(x.average_cpc):6.2f}")
    bs = q(PPC, """SELECT bidding_strategy.id, bidding_strategy.name, bidding_strategy.status, bidding_strategy.type,
        bidding_strategy.maximize_conversions.cpc_bid_ceiling_micros, bidding_strategy.maximize_conversions.target_cpa_micros
        FROM bidding_strategy WHERE bidding_strategy.id = 12308461252""")
    for r in bs:
        b = r.bidding_strategy
        print(f"   portfolio {b.id} {b.name} {b.status.name} ceiling ${m(b.maximize_conversions.cpc_bid_ceiling_micros):.2f}"
              f" tCPA ${m(b.maximize_conversions.target_cpa_micros):.2f}")
    top = q(PPC, """SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = 23848895678 AND segments.date BETWEEN '2026-11-09' AND '2026-11-11' AND metrics.clicks > 0
        ORDER BY metrics.cost_micros DESC LIMIT 10""")
    for r in top:
        print(f"   term ${m(r.metrics.cost_micros):6.2f} {r.metrics.clicks:2d} clk | {r.search_term_view.search_term}")


def plumbing_groups():
    rows = q(PPC, """SELECT ad_group.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.all_conversions
        FROM ad_group WHERE campaign.id = 23853484024 AND segments.date BETWEEN '2026-11-10' AND '2026-11-11' AND metrics.impressions > 0""")
    for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
        x = r.metrics
        print(f"   {r.ad_group.name[:38]:38s} {x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):7.2f} conv {x.conversions:3.1f} all {x.all_conversions:3.1f}")


def electrical_groups():
    rows = q(PPC, """SELECT ad_group.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM ad_group WHERE campaign.id = 23866999121 AND segments.date BETWEEN '2026-11-09' AND '2026-11-11' AND metrics.impressions > 0""")
    for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
        x = r.metrics
        print(f"   {r.ad_group.name[:38]:38s} {x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):7.2f} conv {x.conversions:3.1f}")


def by_action():
    rows = q(PPC, """SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE segments.date BETWEEN '2026-11-09' AND '2026-11-11'""")
    agg = {}
    for r in rows:
        k = (short(r.campaign.name), r.segments.conversion_action_name)
        a = agg.setdefault(k, [0, 0]); a[0] += r.metrics.conversions; a[1] += r.metrics.all_conversions
    for (camp, act), (cv, al) in sorted(agg.items()):
        if cv or al:
            print(f"   {camp:6s} {act:40s} conv {cv:4.1f}  all {al:4.1f}")


def calls():
    rows = q(PPC, """SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
        call_view.caller_area_code, campaign.name FROM call_view WHERE call_view.start_call_date_time >= '2026-11-09 00:00:00'
        ORDER BY call_view.start_call_date_time""")
    for r in rows:
        print(f"   {r.call_view.start_call_date_time} {r.call_view.call_duration_seconds:4d}s {r.call_view.call_status.name:9s}"
              f" area {r.call_view.caller_area_code} | {short(r.campaign.name)}")
    print(f"   {len(rows)} ad calls since 11-09")


def lsa():
    for label, cid in ACCOUNTS[:3]:
        try:
            camps = q(cid, """SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros
                FROM campaign WHERE campaign.status != 'REMOVED'""")
            print(f"-- {label} ({cid}) campaigns: " + "; ".join(
                f"{r.campaign.id} {r.campaign.name[:40]} {r.campaign.advertising_channel_type.name} {r.campaign.status.name} ${m(r.campaign_budget.amount_micros):.0f}"
                for r in camps if r.campaign.advertising_channel_type.name in ("LOCAL_SERVICES", "PERFORMANCE_MAX")))
            rows = q(cid, """SELECT local_services_lead.lead_type, local_services_lead.category_id, local_services_lead.lead_status,
                local_services_lead.lead_charged, local_services_lead.creation_date_time
                FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-09 00:00:00'""")
            print(f"   leads since 11-09: {len(rows)}, charged {sum(1 for r in rows if r.local_services_lead.lead_charged)}")
            for r in sorted(rows, key=lambda r: r.local_services_lead.creation_date_time):
                l = r.local_services_lead
                print(f"   {l.creation_date_time[:16]} {l.lead_type.name:12s} {l.category_id.replace('xcat:service_area_business_', ''):12s}"
                      f" {l.lead_status.name:16s} charged={l.lead_charged}")
        except Exception as e:
            print(f"-- {label} ({cid}) ERROR: {str(e).splitlines()[0][:200]}")


section("1. Daily spend by account, Nov 1 to today (today partial)", daily_all)
section("2. PPC enabled campaigns: status / bidding / budget", campaign_state)
section("3. PPC Search: since the 11-09 fixes vs the 11-04..08 baseline", search_since_fix)
section("4. Branded daily (Target IS abs-top 95%, $18 ceiling)", branded_daily)
section("5. HVAC: CPC under the $30 ceiling + terms since 11-09", hvac_cpc)
section("6. Plumbing ad groups 11-10..11 (General picking up generic plumber?)", plumbing_groups)
section("7. Electrical ad groups 11-09..11", electrical_groups)
section("8. Conversions by action since 11-09", by_action)
section("9. Calls from ads since 11-09", calls)
section("10. LSA: campaign type (migrated?) + leads since 11-09", lsa)
