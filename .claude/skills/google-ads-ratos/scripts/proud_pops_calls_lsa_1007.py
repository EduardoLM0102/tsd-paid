import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import defaultdict, Counter
CID = "1051843378"
f = lambda x: float(x or 0)

print("== Call assets: current status / policy")
for r in run_query(CID, """
SELECT campaign.name, campaign.status, campaign_asset.status, campaign_asset.primary_status, campaign_asset.primary_status_reasons,
       asset.call_asset.phone_number, asset.policy_summary.approval_status
FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' AND campaign.status = 'ENABLED'"""):
    print("  ", r['campaign']['name'][:45], r['asset'].get('call_asset', {}).get('phone_number'), r['campaign_asset'].get('primary_status'),
          r['campaign_asset'].get('primary_status_reasons'), r['asset'].get('policy_summary', {}).get('approval_status'))
for r in run_query(CID, """
SELECT customer_asset.status, customer_asset.primary_status, customer_asset.primary_status_reasons, asset.call_asset.phone_number
FROM customer_asset WHERE customer_asset.field_type = 'CALL'"""):
    print("   ACCOUNT-LEVEL", r['asset'].get('call_asset', {}).get('phone_number'), r['customer_asset'].get('primary_status'), r['customer_asset'].get('primary_status_reasons'))

print("\n== metrics.phone_calls by campaign (calls through Google forwarding numbers)")
for s, u in (("2026-09-01", "2026-09-30"), ("2026-09-30", "2026-10-06")):
    tot = 0
    for r in run_query(CID, f"""
SELECT campaign.name, metrics.phone_calls, metrics.phone_impressions
FROM campaign WHERE segments.date BETWEEN '{s}' AND '{u}' AND campaign.status = 'ENABLED'"""):
        pc = f(r['metrics'].get('phone_calls')); tot += pc
        if pc or f(r['metrics'].get('phone_impressions')):
            print(f"   {s}..{u} {r['campaign']['name'][:45]} calls={pc:.0f} phone_impr={r['metrics'].get('phone_impressions')}")
    print(f"   {s}..{u} TOTAL phone_calls = {tot:.0f}")

print("\n== call_view since 2026-05-01 (any call record at all)")
rows = run_query(CID, """
SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.type, campaign.name
FROM call_view WHERE call_view.start_call_date_time >= '2026-05-01 00:00:00' ORDER BY call_view.start_call_date_time DESC LIMIT 50""")
print("   rows:", len(rows))
for r in rows[:15]:
    cv = r['call_view']; print("   ", cv.get('start_call_date_time'), cv.get('call_duration_seconds'), cv.get('call_status'), r.get('campaign', {}).get('name'))

print("\n== LSA leads (all 3 Proud Pops LSA surfaces)")
for cid in ("1051843378", "7261668241", "6621969129"):
    for s, u in (("2026-09-01", "2026-09-30"), ("2026-09-30", "2026-10-06")):
        rows = run_query(cid, f"""
SELECT local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time
FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '{s} 00:00:00' AND local_services_lead.creation_date_time <= '{u} 23:59:59'""")
        c = Counter((str(r['local_services_lead'].get('lead_type')), bool(r['local_services_lead'].get('lead_charged'))) for r in rows)
        st = Counter(str(r['local_services_lead'].get('lead_status')) for r in rows)
        print(f"   {cid} {s}..{u}: total={len(rows)} by(type,charged)={dict(c)} status={dict(st)}")
    sp = run_query(cid, """SELECT metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-09-30' AND '2026-10-06'""")
    sp2 = run_query(cid, """SELECT metrics.cost_micros FROM customer WHERE segments.date BETWEEN '2026-09-01' AND '2026-09-30'""")
    print(f"   {cid} spend last7=${sum(f(r['metrics'].get('cost_micros')) for r in sp)/1e6:,.0f}  Sep=${sum(f(r['metrics'].get('cost_micros')) for r in sp2)/1e6:,.0f}")
