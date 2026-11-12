# READ-ONLY. Overview of the Proud Pops accounts since the 11-04 restore of Search Electrical / HVAC / Plumbing.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""Accounts: PPC 1051843378, LSA SA [1] 7261668241, LSA SA [2] 6621969129, My Favorite Service 9815330464 (+ its LSAs).
Window: 2026-11-04 .. 2026-11-09 (11-09 partial). 'Conversions' = real leads only since 11-04 (First Time Phone Call,
Calls from ads 60s, customer forms); taps live in all_conversions."""
import sys, traceback
sys.path.insert(0, ".")
from lib import init_client

PPC = "1051843378"
ACCOUNTS = [("PPC", PPC), ("LSA SA [1] electrician", "7261668241"), ("LSA SA [2] HVAC", "6621969129"),
            ("My Favorite Service PPC", "9815330464"), ("MFSC LSA New Braunfels", "4127524472"), ("MFSC LSA San Antonio", "4905286019")]
D0, D1, FULL = "2026-11-04", "2026-11-09", "2026-11-08"
c = init_client(); ga = c.get_service("GoogleAdsService")
m = lambda x: x / 1e6
pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"


def q(cid, s):
    return list(ga.search(customer_id=cid, query=s))


def section(title, fn):
    print("\n=== " + title + " ===")
    try:
        fn()
    except Exception as e:
        print("ERROR:", str(e).splitlines()[0][:300]); traceback.print_exc(limit=1)


def campaigns():
    for label, cid in ACCOUNTS:
        try:
            rows = q(cid, f"""SELECT campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros,
                metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions
                FROM campaign WHERE segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.impressions > 0""")
            mtd = q(cid, f"SELECT metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-11-01' AND '{D1}'")
            print(f"-- {label} ({cid}) | MTD 11-01..{D1[5:]} ${sum(m(r.metrics.cost_micros) for r in mtd):,.2f}"
                  f" | {D0[5:]}..{D1[5:]} ${sum(m(r.metrics.cost_micros) for r in rows):,.2f}")
            for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
                x = r.metrics
                print(f"   {r.campaign.name[:46]:46s} {r.campaign.advertising_channel_type.name[:14]:14s} {r.campaign.status.name:8s}"
                      f" bud ${m(r.campaign_budget.amount_micros):6.0f} | ${m(x.cost_micros):8.2f} {x.impressions:6d} impr {x.clicks:4d} clk"
                      f" conv {x.conversions:5.1f} all {x.all_conversions:5.1f}")
            if not rows:
                print("   (no impressions in the window)")
        except Exception as e:
            print(f"-- {label} ({cid}) ERROR: {str(e).splitlines()[0][:200]}")


def search_detail():
    for lo, hi, tag in [(D0, FULL, "11-04..11-08, 5 full days"), ("2026-11-04", "2026-11-06", "Wed-Fri 11-04..06"), ("2026-11-07", "2026-11-08", "Sat-Sun 11-07..08")]:
        rows = q(PPC, f"""SELECT campaign.name, campaign.bidding_strategy_type, metrics.cost_micros, metrics.impressions, metrics.clicks,
            metrics.average_cpc, metrics.conversions, metrics.all_conversions, metrics.search_impression_share,
            metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share, metrics.search_absolute_top_impression_share
            FROM campaign WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date BETWEEN '{lo}' AND '{hi}' AND metrics.impressions > 0""")
        print(f"-- {tag}")
        tc = tl = 0
        for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
            x = r.metrics; cost = m(x.cost_micros); tc += cost; tl += x.conversions
            print(f"   {r.campaign.name[20:46]:26s} ${cost:8.2f} {x.impressions:5d} impr {x.clicks:4d} clk ctr {x.clicks/max(x.impressions,1)*100:4.1f}% cpc ${m(x.average_cpc):6.2f}"
                  f" | leads {x.conversions:4.1f} cpl {('$%.0f' % (cost/x.conversions)) if x.conversions else 'n/a':>5s} cvr {x.conversions/max(x.clicks,1)*100:4.1f}%"
                  f" (all {x.all_conversions:4.1f}) | IS {pct(x.search_impression_share)} lostB {pct(x.search_budget_lost_impression_share)}"
                  f" lostR {pct(x.search_rank_lost_impression_share)} abs {pct(x.search_absolute_top_impression_share)}")
        print(f"   TOTAL Search ${tc:,.2f} | leads {tl:.1f} | cpl {('$%.0f' % (tc/tl)) if tl else 'n/a'}")


def by_action():
    rows = q(PPC, f"""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE segments.date BETWEEN '{D0}' AND '{D1}'""")
    agg = {}
    for r in rows:
        k = (r.campaign.name, r.segments.conversion_action_name)
        a = agg.setdefault(k, [0, 0]); a[0] += r.metrics.conversions; a[1] += r.metrics.all_conversions
    for (camp, act), (cv, al) in sorted(agg.items()):
        print(f"   {camp[20:48]:28s} {act:38s} conv {cv:4.1f}  all {al:4.1f}")


def daily():
    rows = q(PPC, f"""SELECT segments.date, segments.day_of_week, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM campaign WHERE segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.cost_micros > 0 ORDER BY segments.date""")
    day = {}
    for r in rows:
        d = day.setdefault((r.segments.date, r.segments.day_of_week.name[:3]), {})
        d[r.campaign.name] = (m(r.metrics.cost_micros), r.metrics.conversions)
    for (d, dow), cs in day.items():
        short = lambda n: ("Elec" if "Electrical" in n else "HVAC" if "HVAC" in n else "Plumb" if "Plumbing" in n else "Brand" if "Branded" in n else "LSA" if "LocalServices" in n else n[:10])
        print(f"   {d} {dow} total ${sum(v[0] for v in cs.values()):7.2f} leads {sum(v[1] for v in cs.values()):4.1f} | "
              + "  ".join(f"{short(n)} ${v[0]:.0f}/{v[1]:.0f}" for n, v in sorted(cs.items(), key=lambda kv: -kv[1][0])))


def ad_groups():
    rows = q(PPC, f"""SELECT campaign.name, ad_group.name, metrics.cost_micros, metrics.clicks, metrics.average_cpc, metrics.conversions,
        metrics.all_conversions FROM ad_group WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.name LIKE '%Nonbranded%'
        AND segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.cost_micros > 0""")
    for r in sorted(rows, key=lambda r: (r.campaign.name, -r.metrics.cost_micros)):
        x = r.metrics; cost = m(x.cost_micros)
        print(f"   {r.campaign.name[38:50]:12s} {r.ad_group.name[:38]:38s} ${cost:8.2f} {x.clicks:3d} clk cpc ${m(x.average_cpc):6.2f}"
              f" leads {x.conversions:4.1f} cpl {('$%.0f' % (cost/x.conversions)) if x.conversions else 'n/a':>5s} (all {x.all_conversions:4.1f})")


def terms():
    for name in ("Electrical", "HVAC", "Plumbing"):
        rows = q(PPC, f"""SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
            FROM search_term_view WHERE campaign.name LIKE '%Nonbranded_{name}%' AND segments.date BETWEEN '{D0}' AND '{D1}'
            AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 14""")
        print(f"-- {name}: top search terms by cost")
        for r in rows:
            x = r.metrics
            print(f"   ${m(x.cost_micros):7.2f} {x.clicks:2d} clk leads {x.conversions:3.1f} | {r.search_term_view.search_term}")


def calls():
    rows = q(PPC, f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.type,
        call_view.caller_area_code, campaign.name FROM call_view WHERE call_view.start_call_date_time >= '{D0} 00:00:00'
        ORDER BY call_view.start_call_date_time""")
    for r in rows:
        print(f"   {r.call_view.start_call_date_time} {r.call_view.call_duration_seconds:4d}s {r.call_view.call_status.name:9s}"
              f" {r.call_view.type_.name:24s} area {r.call_view.caller_area_code} | {r.campaign.name[20:]}")
    print(f"   {len(rows)} calls from ads since {D0}; 60s+: {sum(1 for r in rows if r.call_view.call_duration_seconds >= 60)}")


def lsa_leads():
    for label, cid in ACCOUNTS:
        try:
            rows = q(cid, f"""SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.category_id,
                local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time
                FROM local_services_lead WHERE local_services_lead.creation_date_time >= '{D0} 00:00:00'""")
        except Exception as e:
            print(f"-- {label} ({cid}): {str(e).splitlines()[0][:140]}"); continue
        print(f"-- {label} ({cid}): {len(rows)} leads, {sum(1 for r in rows if r.local_services_lead.lead_charged)} charged")
        for r in sorted(rows, key=lambda r: r.local_services_lead.creation_date_time):
            l = r.local_services_lead
            print(f"   {l.creation_date_time[:16]} {l.lead_type.name:12s} {l.category_id.replace('xcat:service_area_business_', ''):12s}"
                  f" {l.lead_status.name:16s} charged={l.lead_charged}")


section("1. Every account: campaigns with impressions since 11-04, + MTD", campaigns)
section("2. PPC Search campaigns: spend, real leads, impression share", search_detail)
section("3. PPC: what the conversions are (by action, 11-04..11-09)", by_action)
section("4. PPC: daily spend/leads by campaign", daily)
section("5. PPC: nonbranded ad groups", ad_groups)
section("6. PPC: nonbranded search terms", terms)
section("7. PPC: calls from ads since 11-04", calls)
section("8. LSA leads since 11-04, every account", lsa_leads)
