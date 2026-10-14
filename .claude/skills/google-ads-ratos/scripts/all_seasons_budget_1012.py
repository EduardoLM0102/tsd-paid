import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"

def g(d, *keys):
    for k in keys:
        if k in d:
            return d[k]
    return None

q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
       campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '2026-09-12' AND '2026-10-11'
"""
tot = 0
print("== Spend 09-12 -> 10-11 (30d) ==")
for r in run_query(CID, q):
    c = r.get("campaign", {}); m = r.get("metrics", {}); b = g(r, "campaignBudget", "campaign_budget") or {}
    cost = int(g(m, "costMicros", "cost_micros") or 0) / 1e6
    if cost == 0 and g(c, "status") != "ENABLED":
        continue
    tot += cost
    print(f"{g(c,'status'):8} {g(c,'advertisingChannelType','advertising_channel_type'):16} ${int(g(b,'amountMicros','amount_micros') or 0)/1e6:>6.2f}/d  spent ${cost:>9.2f}  conv {float(g(m,'conversions') or 0):5.1f}  {g(c,'name')}")
print(f"TOTAL ${tot:.2f}")

q2 = """
SELECT campaign.name, campaign.status, campaign_budget.amount_micros
FROM campaign WHERE campaign.status = 'ENABLED'
"""
print("\n== Enabled now ==")
s = 0
for r in run_query(CID, q2):
    c = r.get("campaign", {}); b = g(r, "campaignBudget", "campaign_budget") or {}
    amt = int(g(b,'amountMicros','amount_micros') or 0)/1e6; s += amt
    print(f"${amt:>6.2f}/d {g(c,'name')}")
print(f"SUM ${s:.2f}/d")

q3 = """
SELECT change_event.change_date_time, change_event.change_resource_type, change_event.resource_change_operation,
       change_event.changed_fields, change_event.user_email, change_event.campaign,
       change_event.old_resource, change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= '2026-09-09 00:00:00' AND change_event.change_date_time <= '2026-10-12 23:59:59'
  AND change_event.change_resource_type IN ('CAMPAIGN_BUDGET', 'CAMPAIGN')
ORDER BY change_event.change_date_time
LIMIT 200
"""
print("\n== Budget / campaign status changes since 09-09 ==")
for r in run_query(CID, q3):
    e = r.get("changeEvent", r.get("change_event", {}))
    fields = str(g(e, "changedFields", "changed_fields"))
    rt = g(e, "changeResourceType", "change_resource_type")
    if rt == "CAMPAIGN" and "status" not in fields:
        continue
    old = g(e, "oldResource", "old_resource") or {}
    new = g(e, "newResource", "new_resource") or {}
    def amt(x):
        cb = x.get("campaignBudget", x.get("campaign_budget", {})) if isinstance(x, dict) else {}
        v = cb.get("amountMicros", cb.get("amount_micros"))
        return None if v is None else int(v)/1e6
    def st(x):
        cc = x.get("campaign", {}) if isinstance(x, dict) else {}
        return cc.get("status")
    print(g(e, "changeDateTime", "change_date_time"), rt, g(e,"resourceChangeOperation","resource_change_operation"), g(e,"userEmail","user_email"), g(e,"campaign"), "budget", amt(old), "->", amt(new), "status", st(old), "->", st(new), fields[:80])
