# READ-ONLY lead-quality check, Nick's 1854100356, 30d (since 2026-09-08). PII masked in output.
import os
import sys, collections, re
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="1854100356"
def q(label, gaql):
    try: return run_query(CID, gaql)
    except SystemExit: print(f"   !! query failed: {label}"); return []
    except Exception as e: print(f"   !! {label}: {str(e)[:300]}"); return []
def H(t): print("\n"+"="*100+f"\n{t}\n"+"="*100)

H("LSA LEADS + CONVERSATIONS, since 09-08")
leads = q("lsa", """SELECT local_services_lead.resource_name, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged,
   local_services_lead.creation_date_time, local_services_lead.service_id, local_services_lead.category_id, local_services_lead.credit_details.credit_state FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-09-08 00:00:00'""")
conv = q("lsa conv", """SELECT local_services_lead_conversation.lead, local_services_lead_conversation.conversation_channel, local_services_lead_conversation.participant_type,
   local_services_lead_conversation.event_date_time, local_services_lead_conversation.phone_call_details.call_duration_millis,
   local_services_lead_conversation.message_details.text FROM local_services_lead_conversation
   WHERE local_services_lead_conversation.event_date_time >= '2026-09-08 00:00:00'""")
cmap=collections.defaultdict(list)
for r in conv:
    c=r["local_services_lead_conversation"]; cmap[c.get("lead")].append(c)
seen_phones=collections.Counter()
for r in leads:
    p=(r["local_services_lead"].get("contact_details") or {}).get("phone_number") or ""
    seen_phones[re.sub(r"\D","",p)]+=1
for r in sorted(leads, key=lambda x: x["local_services_lead"]["creation_date_time"]):
    l=r["local_services_lead"]; cs=cmap.get(l["resource_name"], [])
    durs=[int((c.get("phone_call_details") or {}).get("call_duration_millis") or 0)//1000 for c in cs if c.get("conversation_channel")=="PHONE_CALL"]
    msgs=[(c.get("message_details") or {}).get("text","")[:70].replace("\n"," ") for c in cs if c.get("conversation_channel")=="MESSAGE" and c.get("participant_type")=="CONSUMER"]
    p=re.sub(r"\D","",(l.get("contact_details") or {}).get("phone_number") or "")
    area=p[-10:-7] if len(p)>=10 else "?"
    dup=" REPEAT-CALLER" if p and seen_phones[p]>1 else ""
    print(f"   {l['creation_date_time'][:16]} {l.get('lead_type'):<10} {l.get('lead_status'):<9} charged={str(l.get('lead_charged')):<5} credit={(l.get('credit_details') or {}).get('credit_state')!s:<8} "
          f"svc={l.get('service_id')!s:<22} area {area} calls(s)={durs}{dup} {('msg: '+msgs[0]) if msgs else ''}")
stat=collections.Counter()
for r in leads:
    l=r["local_services_lead"]; cs=cmap.get(l["resource_name"], [])
    durs=[int((c.get("phone_call_details") or {}).get("call_duration_millis") or 0)//1000 for c in cs if c.get("conversation_channel")=="PHONE_CALL"]
    mx=max(durs) if durs else None
    bucket="no call record" if mx is None else ("<30s" if mx<30 else ("30-119s" if mx<120 else "2min+"))
    stat[(l.get("lead_status"), bool(l.get("lead_charged")), bucket)]+=1
for k,v in sorted(stat.items()): print("  SUMMARY", v, k)
print("  repeat callers (same phone >1 lead):", sum(1 for k,v in seen_phones.items() if k and v>1))

H("WEB FORM conversion ('Submit lead form - web') by day, last 90d")
for r in q("web", """SELECT segments.date, segments.conversion_action_name, campaign.name, metrics.all_conversions FROM campaign WHERE segments.date BETWEEN '2026-04-01' AND '2026-10-07' AND metrics.all_conversions > 0
   AND segments.conversion_action_name = 'Submit lead form - web'"""):
    print("  ", r["segments"]["date"], r["campaign"]["name"], r["metrics"]["all_conversions"])
for r in q("web90", """SELECT segments.month, segments.conversion_action_name, metrics.all_conversions FROM customer WHERE segments.date BETWEEN '2026-04-01' AND '2026-10-07' AND segments.conversion_action_name = 'Submit lead form - web'"""):
    print("   month", r["segments"]["month"], r["metrics"]["all_conversions"])
