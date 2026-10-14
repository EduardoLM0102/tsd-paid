"""Zen Air deep dive 2026-09-30, part C: negatives, 'zen air' broad history, LSA status."""
import sys
from collections import defaultdict
from datetime import date, timedelta
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"
LSA = "3740502923"

print("=== C1) shared sets attached to enabled campaigns")
q = """
SELECT campaign.name, shared_set.name, shared_set.type, shared_set.member_count, campaign_shared_set.status
FROM campaign_shared_set WHERE campaign.id IN (23675783172, 24100030790)
"""
rows = run_query(CID, q)
for r in rows:
    print(f"  {r['campaign']['name'][:40]:40s} {r['shared_set']['name']:40s} {r['shared_set'].get('type')} members={r['shared_set'].get('member_count')} {r['campaign_shared_set'].get('status')}")
if not rows:
    print("  (none)")

print("\n=== C2) campaign-level negative keywords")
q = """
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion WHERE campaign.id IN (23675783172, 24100030790)
  AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE
"""
for r in run_query(CID, q):
    print(f"  {r['campaign']['name'][:40]:40s} -{r['campaign_criterion']['keyword']['text']} [{r['campaign_criterion']['keyword']['match_type']}]")
print("\n=== C2b) ad-group-level negatives")
q = """
SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
FROM ad_group_criterion WHERE campaign.id IN (23675783172, 24100030790)
  AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = TRUE
"""
n = 0
for r in run_query(CID, q):
    n += 1
    print(f"  {r['campaign']['name'][:40]:40s} -{r['ad_group_criterion']['keyword']['text']} [{r['ad_group_criterion']['keyword']['match_type']}]")
print(f"  total ad-group negatives: {n}")

print("\n=== C3) branded keywords by week since 08-03 (is 'zen air' BROAD the source of the impression jump?)")
q = """
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, segments.date,
       metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM keyword_view WHERE campaign.id = 23675783172 AND segments.date BETWEEN '2026-08-03' AND '2026-09-29'
"""
agg = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, q):
    k = r["ad_group_criterion"]["keyword"]
    d = date.fromisoformat(r["segments"]["date"])
    w = (d - timedelta(days=d.weekday())).isoformat()
    m = r.get("metrics", {})
    a = agg[(k["text"] + " [" + k["match_type"][:5] + "]", w)]
    a["imp"] += int(m.get("impressions", 0)); a["clk"] += int(m.get("clicks", 0))
    a["cost"] += int(m.get("cost_micros", 0)) / 1e6; a["conv"] += float(m.get("conversions", 0))
for (kw, w), a in sorted(agg.items()):
    if a["imp"]:
        print(f"  {kw:40s} {w} imp={a['imp']:5.0f} clk={a['clk']:3.0f} cost=${a['cost']:7.2f} conv={a['conv']:.0f}")

print("\n=== C4) LSA account status + last 90d by month")
q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.serving_status
FROM campaign
"""
for r in run_query(LSA, q):
    c = r["campaign"]
    print(f"  {c['id']} {c['name'][:50]:50s} {c['status']} {c.get('serving_status')}")
q = """
SELECT segments.month, metrics.cost_micros, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2026-01-01' AND '2026-09-29'
"""
for r in run_query(LSA, q):
    m = r.get("metrics", {})
    print(f"  {r['segments']['month']} cost=${int(m.get('cost_micros',0))/1e6:8.2f} conv={m.get('conversions',0)} all={m.get('all_conversions',0)}")
q = """
SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
       change_event.changed_fields, change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= '2026-09-01' AND change_event.change_date_time <= '2026-09-30'
ORDER BY change_event.change_date_time DESC LIMIT 50
"""
for r in run_query(LSA, q):
    ce = r["change_event"]
    print(f"  CHANGE {ce['change_date_time'][:16]} {ce.get('user_email','')} {ce.get('change_resource_type')} {ce.get('changed_fields')}")
