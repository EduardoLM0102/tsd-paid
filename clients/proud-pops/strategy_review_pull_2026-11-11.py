# READ-ONLY. AT Client Strategy Review "Oct Review" (task fc4041bd): cycle 2026-10-16 .. 2026-11-14.
# Pulled 2026-11-11: data through 11-10 (11-11 partial shown separately). Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""Accounts: PPC 1051843378 (has an in-account LOCAL_SERVICES campaign), LSA SA [1] 7261668241, LSA SA [2] 6621969129,
My Favorite Service 9815330464 (+ its LSAs) for info only. Since 11-04 PPC 'conversions' = real leads only
(First Time Phone Call, Calls from ads 60s, customer forms); before that they included call-button taps."""
import sys, traceback
from collections import defaultdict
sys.path.insert(0, ".")
from lib import init_client

PPC = "1051843378"
ACCOUNTS = [("PPC", PPC), ("LSA SA [1] electrician", "7261668241"), ("LSA SA [2] HVAC", "6621969129"),
            ("My Favorite Service PPC", "9815330464"), ("MFSC LSA New Braunfels", "4127524472"), ("MFSC LSA San Antonio", "4905286019")]
D0, D1, DP = "2026-10-16", "2026-11-10", "2026-11-11"
c = init_client(); ga = c.get_service("GoogleAdsService")
m = lambda x: x / 1e6


def q(cid, s):
    return list(ga.search(customer_id=cid, query=s))


def section(title, fn):
    print("\n=== " + title + " ===")
    try:
        fn()
    except Exception as e:
        print("ERROR:", str(e).splitlines()[0][:300]); traceback.print_exc(limit=1)


def spend_by_campaign():
    for label, cid in ACCOUNTS:
        try:
            rows = q(cid, f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
                metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions
                FROM campaign WHERE segments.date BETWEEN '{D0}' AND '{D1}' AND metrics.cost_micros > 0""")
            part = q(cid, f"SELECT metrics.cost_micros FROM customer WHERE segments.date = '{DP}'")
            tot = sum(m(r.metrics.cost_micros) for r in rows)
            lsa = sum(m(r.metrics.cost_micros) for r in rows if r.campaign.advertising_channel_type.name == "LOCAL_SERVICES")
            print(f"-- {label} ({cid}) | {D0}..{D1} ${tot:,.2f} (LOCAL_SERVICES ${lsa:,.2f}) | {DP} partial ${sum(m(r.metrics.cost_micros) for r in part):,.2f}")
            for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
                x = r.metrics
                print(f"   {r.campaign.id} {r.campaign.name[:48]:48s} {r.campaign.advertising_channel_type.name[:14]:14s} {r.campaign.status.name:8s}"
                      f" ${m(x.cost_micros):9.2f} {x.impressions:6d} impr {x.clicks:4d} clk conv {x.conversions:5.1f} all {x.all_conversions:6.1f}")
        except Exception as e:
            print(f"-- {label} ({cid}) ERROR: {str(e).splitlines()[0][:200]}")


def spend_by_period():
    for lo, hi, tag in [(D0, "2026-11-03", "10-16..11-03 (Branded only, service campaigns off)"), ("2026-11-04", D1, "11-04..11-10 (services restored, $880/d caps)")]:
        print(f"-- {tag}")
        for label, cid in ACCOUNTS[:3]:
            rows = q(cid, f"""SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.conversions
                FROM campaign WHERE segments.date BETWEEN '{lo}' AND '{hi}' AND metrics.cost_micros > 0""")
            tot = sum(m(r.metrics.cost_micros) for r in rows)
            print(f"   {label:24s} ${tot:9,.2f} | " + "; ".join(f"{r.campaign.name[20:46]} ${m(r.metrics.cost_micros):,.0f}/{r.metrics.conversions:.0f}"
                                                            for r in sorted(rows, key=lambda r: -r.metrics.cost_micros)))


def daily_totals():
    day = defaultdict(float)
    for label, cid in ACCOUNTS[:3]:
        for r in q(cid, f"SELECT segments.date, segments.day_of_week, metrics.cost_micros FROM customer WHERE segments.date BETWEEN '{D0}' AND '{DP}'"):
            day[(r.segments.date, r.segments.day_of_week.name[:3])] += m(r.metrics.cost_micros)
    for (d, dow), v in sorted(day.items()):
        print(f"   {d} {dow} ${v:8.2f}")
    print(f"   TOTAL {D0}..{DP}: ${sum(day.values()):,.2f}")


def by_action():
    for lo, hi, tag in [(D0, D1, "FULL 10-16..11-10"), (D0, "2026-11-03", "10-16..11-03"), ("2026-11-04", D1, "11-04..11-10")]:
        rows = q(PPC, f"""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
            FROM campaign WHERE segments.date BETWEEN '{lo}' AND '{hi}'""")
        agg = defaultdict(lambda: [0, 0]); tot = defaultdict(lambda: [0, 0])
        for r in rows:
            k = (r.segments.conversion_action_name, r.campaign.name[20:46])
            agg[k][0] += r.metrics.conversions; agg[k][1] += r.metrics.all_conversions
            tot[r.segments.conversion_action_name][0] += r.metrics.conversions; tot[r.segments.conversion_action_name][1] += r.metrics.all_conversions
        print(f"-- {tag}")
        for act, (cv, al) in sorted(tot.items(), key=lambda kv: -kv[1][1]):
            if al:
                print(f"   {act:42s} conv {cv:5.1f}  all {al:6.1f}  | " + "; ".join(f"{camp} {v[1]:.0f}" for (a, camp), v in sorted(agg.items(), key=lambda kv: -kv[1][1]) if a == act and v[1]))


def calls():
    rows = q(PPC, f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
        call_view.caller_area_code, campaign.name FROM call_view
        WHERE call_view.start_call_date_time >= '{D0} 00:00:00' AND call_view.start_call_date_time <= '{DP} 23:59:59'
        ORDER BY call_view.start_call_date_time""")
    n60 = 0
    for r in rows:
        v = r.call_view; f = "*" if v.call_duration_seconds >= 60 else " "; n60 += v.call_duration_seconds >= 60
        print(f"   {f} {v.start_call_date_time} {v.call_duration_seconds:4d}s {v.call_status.name:9s} area {v.caller_area_code} | {r.campaign.name[20:46]}")
    print(f"   {len(rows)} call-asset calls {D0}..{DP}, {n60} of 60s+")


def lsa_leads():
    for label, cid in ACCOUNTS[:3]:
        try:
            rows = q(cid, f"""SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.category_id,
                local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time,
                local_services_lead.credit_details.credit_state FROM local_services_lead
                WHERE local_services_lead.creation_date_time >= '{D0} 00:00:00' AND local_services_lead.creation_date_time <= '{DP} 23:59:59'""")
            st = defaultdict(int)
            for r in rows:
                st[r.local_services_lead.lead_status.name] += 1
            print(f"-- {label} ({cid}): {len(rows)} leads, charged {sum(1 for r in rows if r.local_services_lead.lead_charged)}, by status {dict(st)}")
            for r in sorted(rows, key=lambda r: r.local_services_lead.creation_date_time):
                l = r.local_services_lead
                print(f"   {l.creation_date_time[:16]} {l.lead_type.name:12s} {l.category_id.replace('xcat:service_area_business_', ''):12s}"
                      f" {l.lead_status.name:16s} charged={l.lead_charged} credit={l.credit_details.credit_state.name}")
        except Exception as e:
            print(f"-- {label} ({cid}) ERROR: {str(e).splitlines()[0][:200]}")


def search_quality():
    rows = q(PPC, f"""SELECT campaign.name, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc,
        metrics.conversions, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date BETWEEN '2026-11-04' AND '{D1}' AND metrics.impressions > 0""")
    pct = lambda x: " n/a" if not x else f"{x*100:4.0f}"
    for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
        x = r.metrics; cost = m(x.cost_micros)
        print(f"   {r.campaign.name[20:46]:26s} ${cost:8.2f} {x.clicks:4d} clk cpc ${m(x.average_cpc):6.2f} leads {x.conversions:4.1f}"
              f" cpl {('$%.0f' % (cost/x.conversions)) if x.conversions else 'n/a':>5s} | IS {pct(x.search_impression_share)} lostB {pct(x.search_budget_lost_impression_share)} lostR {pct(x.search_rank_lost_impression_share)}")


section("1. Spend by account and campaign, 10-16..11-10 (+ 11-11 partial)", spend_by_campaign)
section("2. Spend split: Branded-only stretch vs restored", spend_by_period)
section("3. Daily totals, 3 accounts, 10-16..11-11", daily_totals)
section("4. PPC conversions by action (conv = biddable, all = incl. secondary/taps)", by_action)
section("5. Call-asset calls (Google call_view)", calls)
section("6. LSA leads by account, with status/charged", lsa_leads)
section("7. Search campaigns 11-04..11-10: CPC, leads, impression share", search_quality)
