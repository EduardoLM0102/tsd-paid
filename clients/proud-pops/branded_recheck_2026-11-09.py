# READ-ONLY. fu-132 recheck: is Branded serving again at the $18 Target IS ceiling (applied 11-06)?
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path>
"""Proud Pops (1051843378) Branded 23853361615, recheck after ceiling $10 -> $18 (2026-11-06).
Prints: settings + status, daily delivery/IS since 11-01, hourly since 11-06, conversions by action,
calls from ads, top search terms, keyword IS, and all-campaign daily spend for context."""
import sys, datetime, traceback
sys.path.insert(0, ".")
from lib import init_client

CID, BR = "1051843378", "23853361615"
D0, D1 = "2026-11-01", "2026-11-09"
SINCE = "2026-11-06"
c = init_client(); ga = c.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
m = lambda x: x / 1e6
pct = lambda x: "  n/a" if x is None or x == 0 else f"{x*100:5.1f}"


def section(title, fn):
    print("\n=== " + title + " ===")
    try:
        fn()
    except Exception as e:  # keep going, one bad field must not hide the rest
        print("ERROR:", str(e).splitlines()[0][:300])
        traceback.print_exc(limit=1)


def settings():
    r = q(f"""SELECT campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
        campaign.bidding_strategy_type, campaign.target_impression_share.location,
        campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros FROM campaign WHERE campaign.id = {BR}""")[0]
    t = r.campaign.target_impression_share
    print(r.campaign.name, "|", r.campaign.status.name, "| primary:", r.campaign.primary_status.name,
          [x.name for x in r.campaign.primary_status_reasons])
    print(r.campaign.bidding_strategy_type.name, t.location.name, t.location_fraction_micros / 1e4, "% | ceiling $",
          m(t.cpc_bid_ceiling_micros), "| budget $", m(r.campaign_budget.amount_micros))
    print("now (local machine):", datetime.datetime.now().isoformat(timespec="minutes"))


def daily():
    rows = q(f"""SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.average_cpc,
        metrics.search_impression_share, metrics.search_top_impression_share, metrics.search_absolute_top_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share,
        metrics.search_rank_lost_absolute_top_impression_share, metrics.search_budget_lost_absolute_top_impression_share,
        metrics.conversions, metrics.all_conversions
        FROM campaign WHERE campaign.id = {BR} AND segments.date BETWEEN '{D0}' AND '{D1}' ORDER BY segments.date""")
    print("date        impr  clk   cost    cpc |   IS  top% abs% | lostB lostR | absLostR absLostB | conv allconv")
    for r in rows:
        x = r.metrics
        print(f"{r.segments.date} {x.impressions:5d} {x.clicks:4d} {m(x.cost_micros):7.2f} {m(x.average_cpc):6.2f} |"
              f" {pct(x.search_impression_share)} {pct(x.search_top_impression_share)} {pct(x.search_absolute_top_impression_share)} |"
              f" {pct(x.search_budget_lost_impression_share)} {pct(x.search_rank_lost_impression_share)} |"
              f" {pct(x.search_rank_lost_absolute_top_impression_share)}    {pct(x.search_budget_lost_absolute_top_impression_share)} |"
              f" {x.conversions:4.1f} {x.all_conversions:5.1f}")
    if not rows:
        print("(no rows)")


def hourly():
    rows = q(f"""SELECT segments.date, segments.hour, metrics.impressions, metrics.clicks, metrics.cost_micros
        FROM campaign WHERE campaign.id = {BR} AND segments.date BETWEEN '{SINCE}' AND '{D1}'
        ORDER BY segments.date, segments.hour""")
    by = {}
    for r in rows:
        by.setdefault(r.segments.date, []).append((r.segments.hour, r.metrics.impressions, r.metrics.clicks, m(r.metrics.cost_micros)))
    for d, hs in by.items():
        print(d, " ".join(f"{h:02d}h:{i}/{k}" for h, i, k, _ in hs if i), "| total impr", sum(i for _, i, _, _ in hs),
              "clicks", sum(k for _, _, k, _ in hs), f"cost ${sum(x for *_, x in hs):.2f}")
    if not rows:
        print("(no rows)")


def conv_by_action():
    rows = q(f"""SELECT segments.date, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
        FROM campaign WHERE campaign.id = {BR} AND segments.date BETWEEN '{D0}' AND '{D1}' ORDER BY segments.date""")
    for r in rows:
        print(r.segments.date, f"{r.segments.conversion_action_name:45s} conv {r.metrics.conversions:4.1f}  all {r.metrics.all_conversions:4.1f}")
    if not rows:
        print("(no conversions of any kind)")


def calls():
    rows = q(f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.type,
        call_view.caller_area_code, campaign.id, campaign.name FROM call_view
        WHERE call_view.start_call_date_time >= '{SINCE} 00:00:00' ORDER BY call_view.start_call_date_time""")
    n = 0
    for r in rows:
        tag = "BRANDED" if str(r.campaign.id) == BR else "other  "
        n += tag == "BRANDED"
        print(tag, r.call_view.start_call_date_time, f"{r.call_view.call_duration_seconds:4d}s", r.call_view.call_status.name,
              r.call_view.type_.name, "area", r.call_view.caller_area_code, "|", r.campaign.name)
    print(f"calls from ads since {SINCE}: {len(rows)} account-wide, {n} on Branded")


def terms():
    rows = q(f"""SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.average_cpc
        FROM search_term_view WHERE campaign.id = {BR} AND segments.date BETWEEN '{SINCE}' AND '{D1}'
        ORDER BY metrics.cost_micros DESC LIMIT 30""")
    for r in rows:
        x = r.metrics
        print(f"{x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):7.2f} cpc ${m(x.average_cpc):5.2f} | {r.search_term_view.search_term}")
    if not rows:
        print("(no search terms)")


def keywords():
    rows = q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
        metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.average_cpc,
        metrics.search_impression_share, metrics.search_absolute_top_impression_share, metrics.search_rank_lost_impression_share
        FROM keyword_view WHERE campaign.id = {BR} AND segments.date BETWEEN '{SINCE}' AND '{D1}'
        AND metrics.impressions > 0 ORDER BY metrics.impressions DESC LIMIT 25""")
    for r in rows:
        x = r.metrics; k = r.ad_group_criterion.keyword
        print(f"{x.impressions:4d} impr {x.clicks:3d} clk ${m(x.cost_micros):7.2f} cpc ${m(x.average_cpc):5.2f} | IS {pct(x.search_impression_share)}"
              f" abs {pct(x.search_absolute_top_impression_share)} lostR {pct(x.search_rank_lost_impression_share)} |"
              f" [{k.match_type.name}] {k.text} ({r.ad_group.name})")
    if not rows:
        print("(no keyword rows)")


def all_campaigns():
    rows = q(f"""SELECT segments.date, campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks,
        metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-11-04' AND '{D1}' AND metrics.cost_micros > 0
        ORDER BY segments.date, metrics.cost_micros DESC""")
    day = {}
    for r in rows:
        day.setdefault(r.segments.date, []).append((r.campaign.name, r.campaign.advertising_channel_type.name, m(r.metrics.cost_micros), r.metrics.conversions))
    for d, cs in day.items():
        search = sum(x for _, t, x, _ in cs if t == "SEARCH")
        print(f"{d}  Search ${search:8.2f} | all ${sum(x for _, _, x, _ in cs):8.2f} | " + "; ".join(f"{n[:28]} ${x:.0f}/{cv:.0f}cv" for n, _, x, cv in cs))
    mtd = q(f"SELECT metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-11-01' AND '{D1}'")
    print(f"MTD 11-01..{D1[5:]} in-account: ${sum(m(r.metrics.cost_micros) for r in mtd):,.2f}")


def bid_estimates():
    rows = q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
        ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score,
        ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr,
        ad_group_criterion.position_estimates.first_page_cpc_micros, ad_group_criterion.position_estimates.top_of_page_cpc_micros,
        ad_group_criterion.position_estimates.first_position_cpc_micros, ad_group_criterion.effective_cpc_bid_micros
        FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")
    print("QS (ad/LP/ctr) | est. bid: first page / top of page / first position | effective bid | keyword")
    for r in rows:
        k = r.ad_group_criterion; qi = k.quality_info; pe = k.position_estimates
        print(f"QS {qi.quality_score:2d} ({qi.creative_quality_score.name[:5]}/{qi.post_click_quality_score.name[:5]}/{qi.search_predicted_ctr.name[:5]}) |"
              f" ${m(pe.first_page_cpc_micros):6.2f} / ${m(pe.top_of_page_cpc_micros):6.2f} / ${m(pe.first_position_cpc_micros):6.2f} |"
              f" ${m(k.effective_cpc_bid_micros):6.2f} | [{k.keyword.match_type.name}] {k.keyword.text} ({r.ad_group.name})")


def changes():
    rows = q(f"""SELECT change_event.change_date_time, change_event.user_email, change_event.client_type,
        change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields
        FROM change_event WHERE change_event.change_date_time >= '2026-11-04 00:00:00'
        AND change_event.change_date_time <= '2026-11-09 23:59:59'
        AND change_event.campaign = 'customers/{CID}/campaigns/{BR}' ORDER BY change_event.change_date_time LIMIT 200""")
    for r in rows:
        e = r.change_event
        print(e.change_date_time[:19], e.user_email, e.client_type.name, e.change_resource_type.name,
              e.resource_change_operation.name, ",".join(e.changed_fields.paths)[:110])
    if not rows:
        print("(no change events)")


def ads():
    rows = q(f"""SELECT ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength,
        ad_group_ad.policy_summary.approval_status, ad_group_ad.primary_status FROM ad_group_ad
        WHERE campaign.id = {BR} AND ad_group_ad.status != 'REMOVED'""")
    for r in rows:
        a = r.ad_group_ad
        print(f"{r.ad_group.name:20s} ({r.ad_group.status.name}) ad {a.ad.id} {a.status.name:8s} strength {a.ad_strength.name:10s}"
              f" {a.policy_summary.approval_status.name} primary {a.primary_status.name}")


def headroom():
    rows = q("""SELECT campaign.name, campaign.id, campaign.bidding_strategy_type, campaign_budget.amount_micros, metrics.cost_micros,
        metrics.clicks, metrics.average_cpc, metrics.conversions, metrics.search_impression_share,
        metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
        FROM campaign WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'
        AND segments.date BETWEEN '2026-11-04' AND '2026-11-08'""")
    print("11-04..11-08 (5 days) | budget/d | spend/d | clicks | cpc | conv (real leads) | cost/conv | IS | lost budget | lost rank")
    for r in sorted(rows, key=lambda r: -r.metrics.cost_micros):
        x = r.metrics; cost = m(x.cost_micros)
        print(f"{r.campaign.name[:44]:44s} ${m(r.campaign_budget.amount_micros):6.0f} ${cost/5:7.2f} {x.clicks:4d} ${m(x.average_cpc):6.2f}"
              f" {x.conversions:5.1f} {('$%.0f' % (cost / x.conversions)) if x.conversions else '   n/a':>7s} | IS {pct(x.search_impression_share)}"
              f" lostB {pct(x.search_budget_lost_impression_share)} lostR {pct(x.search_rank_lost_impression_share)} | {r.campaign.bidding_strategy_type.name}")


if "--headroom" in sys.argv:
    section("12. Search campaigns 11-04..11-08: budget vs spend, real leads, IS lost to budget/rank", headroom)
    sys.exit(0)

if "--extra" in sys.argv:
    section("9. Branded keywords: quality score + bid estimates", bid_estimates)
    section("10. Change history on Branded since 11-04", changes)
    section("11. Branded ads", ads)
    sys.exit(0)

section("1. Settings + status", settings)
section("2. Branded daily delivery + impression share", daily)
section("3. Branded hourly impressions/clicks since 11-06", hourly)
section("4. Branded conversions by action", conv_by_action)
section("5. Calls from ads since 11-06", calls)
section("6. Branded search terms since 11-06", terms)
section("7. Branded keywords since 11-06", keywords)
section("8. All campaigns, daily spend since 11-04", all_campaigns)
