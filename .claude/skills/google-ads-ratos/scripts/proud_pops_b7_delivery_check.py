"""Proud Pops checklist B7a/B7b (read-only): approval of the 6 edited Search ads + hourly delivery of Electrical/Plumbing
today vs yesterday, plus Plumbing diagnostics (status reasons, bid strategy, budget, IS)."""
import sys, os, datetime
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID = "1051843378"
today = datetime.date.today().isoformat(); yday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
print("== B7a ad review status")
for r in run_query(CID, """SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.primary_status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status
FROM ad_group_ad WHERE ad_group_ad.ad.id IN (809528123698,809490621054,809490671193,808814916930,808929407402,808929711767)"""):
    a = r["ad_group_ad"]; print(f"   {r['ad_group']['name']:28s} {a.get('primary_status')}  {a.get('policy_summary')}")
print("\n== B7b hourly impressions (account tz America/Chicago)")
d = defaultdict(lambda: defaultdict(int))
for r in run_query(CID, f"""SELECT campaign.name, segments.date, segments.hour, metrics.impressions FROM campaign
WHERE campaign.id IN (23866999121, 23853484024) AND segments.date BETWEEN '{yday}' AND '{today}'"""):
    d[(r["campaign"]["name"][24:], r["segments"]["date"])][int(r["segments"]["hour"])] += int(r["metrics"].get("impressions", 0))
for (n, day), hrs in sorted(d.items()):
    print(f"   {n:24s} {day}  " + " ".join(f"{h:02d}:{hrs.get(h, 0)}" for h in range(24)) + f"  | total {sum(hrs.values())}")
print("\n== Plumbing 23853484024 diagnostics")
for r in run_query(CID, """SELECT campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type,
campaign.bidding_strategy_system_status, campaign_budget.amount_micros, campaign_budget.has_recommended_budget FROM campaign WHERE campaign.id = 23853484024"""):
    print("   ", r["campaign"], "budget $", int(r["campaign_budget"]["amount_micros"]) / 1e6)
for r in run_query(CID, f"""SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.search_impression_share,
metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign
WHERE campaign.id = 23853484024 AND segments.date BETWEEN '{(datetime.date.today() - datetime.timedelta(days=7)).isoformat()}' AND '{today}'"""):
    m = r["metrics"]; f = lambda k: f"{float(m.get(k) or 0) * 100:.0f}%" if m.get(k) is not None else "-"
    print(f"   {r['segments']['date']}  impr {m.get('impressions', 0):>4} clk {m.get('clicks', 0):>3} ${int(m.get('cost_micros', 0)) / 1e6:>6.0f}  IS {f('search_impression_share')} lostBudget {f('search_budget_lost_impression_share')} lostRank {f('search_rank_lost_impression_share')}")
