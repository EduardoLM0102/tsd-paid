from h import *
L="9239407401"
# daily cost for exact windows
q="""SELECT segments.date, metrics.cost_micros, metrics.all_conversions, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2025-01-01' AND '2026-09-23'"""
rows=list(run_query(L,q))
json.dump(rows, open(OUT+"lsa_daily.json","w"), default=str)
def s(lo,hi):
    c=sum(f(r["metrics"].get("cost_micros")) for r in rows if lo<=r["segments"]["date"]<=hi)/1e6
    v=sum(f(r["metrics"].get("all_conversions")) for r in rows if lo<=r["segments"]["date"]<=hi)
    return round(c), round(v)
for lo,hi,l in [("2025-03-24","2025-09-23","LY window"),("2025-09-24","2026-03-23","prior 6mo"),("2026-03-24","2026-09-23","LAST 6mo"),("2025-01-01","2025-09-23","2025 YTD same days"),("2026-01-01","2026-09-23","2026 YTD"),("2025-06-01","2025-08-31","Sum25"),("2026-06-01","2026-08-31","Sum26")]:
    print(l, "LSA cost/all_conv:", s(lo,hi))
# conversations
q2="""SELECT local_services_lead_conversation.id, local_services_lead_conversation.conversation_channel, local_services_lead_conversation.participant_type,
 local_services_lead_conversation.event_date_time, local_services_lead_conversation.phone_call_details.call_duration_millis, local_services_lead_conversation.lead
FROM local_services_lead_conversation WHERE local_services_lead_conversation.event_date_time >= '2025-03-01 00:00:00'"""
try:
    conv=list(run_query(L,q2)); json.dump(conv, open(OUT+"lsa_conv.json","w"), default=str); print("conversations", len(conv)); print(json.dumps(conv[0],default=str))
except Exception as e: print("ERR conv", str(e)[:500])
