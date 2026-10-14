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

H("CALL CONVERSION SETTINGS")
for r in q("ca", "SELECT conversion_action.name, conversion_action.phone_call_duration_seconds, conversion_action.counting_type, conversion_action.click_through_lookback_window_days FROM conversion_action WHERE conversion_action.status='ENABLED' AND conversion_action.category = 'PHONE_CALL_LEAD'"):
    print("  ", r["conversion_action"])

H("CALLS FROM ADS (call_view), since 09-08")
calls = q("call_view", """SELECT campaign.name, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
   call_view.caller_area_code, call_view.caller_country_code, call_view.type, call_view.call_tracking_display_location
   FROM call_view WHERE call_view.start_call_date_time >= '2026-09-08 00:00:00' ORDER BY call_view.start_call_date_time""")
for r in calls:
    v=r["call_view"]
    print(f"   {v['start_call_date_time'][:16]}  {r['campaign']['name'][:34]:<34} {v.get('call_status'):<9} {int(v.get('call_duration_seconds') or 0):>5}s  area {v.get('caller_area_code')} {v.get('caller_country_code')}  {v.get('type')} {v.get('call_tracking_display_location')}")
if calls:
    by=collections.defaultdict(lambda: collections.Counter())
    for r in calls:
        v=r["call_view"]; c=r["campaign"]["name"][:34]; d=int(v.get("call_duration_seconds") or 0)
        by[c]["total"]+=1; by[c]["missed"]+= v.get("call_status")=="MISSED"
        by[c][">=60s"]+= d>=60; by[c]["<30s answered"]+= (v.get("call_status")=="RECEIVED" and d<30)
        by[c]["area 985"]+= v.get("caller_area_code")=="985"
    for c,v in by.items(): print("  SUMMARY", c, dict(v))
    ac=collections.Counter(r["call_view"].get("caller_area_code") for r in calls); print("  area codes:", dict(ac.most_common()))

H("LSA LEADS + CONVERSATIONS, since 09-08")
leads = q("lsa", """SELECT local_services_lead.resource_name, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged,
   local_services_lead.creation_date_time, local_services_lead.service_id, local_services_lead.category_id, local_services_lead.credit_details.credit_state,
   local_services_lead.contact_details.phone_number FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-09-08 00:00:00'""")
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

H("GOOGLE-HOSTED LEAD FORM SUBMISSIONS, since 09-08 (masked)")
for r in q("lfs", """SELECT lead_form_submission_data.submission_date_time, lead_form_submission_data.lead_form_submission_fields, lead_form_submission_data.custom_lead_form_submission_fields,
   campaign.name FROM lead_form_submission_data WHERE lead_form_submission_data.submission_date_time >= '2026-08-01 00:00:00'"""):
    d=r["lead_form_submission_data"]; out=[]
    for f in d.get("lead_form_submission_fields") or []:
        t=f.get("field_type"); v=f.get("field_value") or ""
        if t=="EMAIL": out.append("email=*@"+v.split("@")[-1] if "@" in v else "email=?")
        elif t=="PHONE_NUMBER": dg=re.sub(r"\D","",v); out.append("phone area "+(dg[-10:-7] if len(dg)>=10 else dg))
        elif t in ("FULL_NAME","FIRST_NAME","LAST_NAME"): out.append(f"{t.lower()}={v[:1]}.. ({len(v)} chars)")
        elif t in ("POSTAL_CODE","ZIP_CODE"): out.append("zip="+v)
        else: out.append(f"{t}={v[:40]}")
    for f in d.get("custom_lead_form_submission_fields") or []:
        out.append(f"{f.get('question_text','')[:30]}={f.get('field_value','')[:50]}")
    print(f"   {d.get('submission_date_time','')[:16]} [{r['campaign']['name'][:25]}] " + " | ".join(out))

H("WEB FORM conversion ('Submit lead form - web') by day, last 90d")
for r in q("web", """SELECT segments.date, campaign.name, metrics.all_conversions FROM campaign WHERE segments.date DURING LAST_30_DAYS AND metrics.all_conversions > 0
   AND segments.conversion_action_name = 'Submit lead form - web'"""):
    print("  ", r["segments"]["date"], r["campaign"]["name"], r["metrics"]["all_conversions"])
for r in q("web90", """SELECT segments.month, metrics.all_conversions FROM customer WHERE segments.date BETWEEN '2026-04-01' AND '2026-10-07' AND segments.conversion_action_name = 'Submit lead form - web'"""):
    print("   month", r["segments"]["month"], r["metrics"]["all_conversions"])
