"""
Proud Pops — LSA lead handling (checklist D3 / AM item P-6). Read-only.
Lead-level detail for the 3 live LSA surfaces, Jun 1 → today. NO consumer contact details, recordings or message text
are selected (PII stays out). Per lead: date, type, status, charged, credit/dispute state, job type, and from the
conversation log: call duration (0s = likely missed) and whether the business replied to messages.

Run: ./tsd.sh proud_pops_lsa_lead_handling.py
"""
import sys, os, datetime
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query

SURFACES = {"1051843378": "in-account (PPC acct)", "7261668241": "LSA [1] Electrician", "6621969129": "LSA [2] HVAC"}
SINCE = "2026-06-01 00:00:00"


def leads_for(cid):
    rows = run_query(cid, f"""SELECT local_services_lead.resource_name, local_services_lead.id, local_services_lead.creation_date_time,
local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.category_id,
local_services_lead.service_id, local_services_lead.credit_details.credit_state, local_services_lead.lead_feedback_submitted
FROM local_services_lead WHERE local_services_lead.creation_date_time >= '{SINCE}'""")
    return [r["local_services_lead"] for r in rows]


def convs_for(cid):
    try:
        rows = run_query(cid, f"""SELECT local_services_lead_conversation.lead, local_services_lead_conversation.conversation_channel,
local_services_lead_conversation.participant_type, local_services_lead_conversation.event_date_time,
local_services_lead_conversation.phone_call_details.call_duration_millis
FROM local_services_lead_conversation WHERE local_services_lead_conversation.event_date_time >= '{SINCE}'""")
    except SystemExit:
        return None
    by = defaultdict(list)
    for r in rows:
        c = r["local_services_lead_conversation"]; by[c.get("lead")].append(c)
    return by


def bucket(ms):
    if ms is None: return "n/a"
    s = int(ms) / 1000
    return "0s" if s == 0 else "<30s" if s < 30 else "30-60s" if s < 60 else "60s+"


all_rows = []
for cid, name in SURFACES.items():
    leads = leads_for(cid); convs = convs_for(cid)
    print(f"\n######## {cid} {name}: {len(leads)} leads since Jun 1  (conversation data: {'yes' if convs is not None else 'NOT AVAILABLE'})")
    for l in leads:
        conv = (convs or {}).get(l["resource_name"], [])
        calls = [c for c in conv if str(c.get("conversation_channel")) == "PHONE_CALL"]
        durs = [c.get("phone_call_details", {}).get("call_duration_millis") for c in calls]
        maxdur = max((int(d) for d in durs if d is not None), default=None)
        msgs = [c for c in conv if str(c.get("conversation_channel")) == "MESSAGE"]
        replied = any(str(c.get("participant_type")) == "ADVERTISER" for c in msgs) if msgs else None
        row = dict(cid=cid, surface=name, date=l["creation_date_time"][:16], month=l["creation_date_time"][:7], type=str(l.get("lead_type")),
                   status=str(l.get("lead_status")), charged=bool(l.get("lead_charged")),
                   credit=str(l.get("credit_details", {}).get("credit_state", "")), cat=str(l.get("category_id", "")).replace("xcat:service_area_business_", ""),
                   svc=str(l.get("service_id", "")), call=bucket(maxdur) if calls else "", n_calls=len(calls), replied=replied,
                   feedback=bool(l.get("lead_feedback_submitted")))
        all_rows.append(row)

print("\n\n==================== MONTHLY SUMMARY (all 3 surfaces) ====================")
by_m = defaultdict(list)
for r in all_rows: by_m[r["month"]].append(r)
for m in sorted(by_m):
    rs = by_m[m]
    calls = [r for r in rs if r["type"] == "PHONE_CALL"]
    print(f"{m}: leads {len(rs):3d} | calls {len(calls):3d} (call length: {dict(Counter(r['call'] for r in calls))}) "
          f"| status {dict(Counter(r['status'] for r in rs))} | charged {sum(r['charged'] for r in rs)} "
          f"| credit {dict(Counter(r['credit'] for r in rs if r['credit']))}")

print("\n==================== SEPTEMBER + OCTOBER, lead by lead (no contact details) ====================")
for r in sorted((r for r in all_rows if r["month"] >= "2026-09"), key=lambda r: r["date"]):
    extra = f"call {r['call']} ({r['n_calls']} call event(s))" if r["type"] == "PHONE_CALL" else (f"business replied: {r['replied']}" if r["type"] == "MESSAGE" else "")
    print(f"  {r['date']}  {r['surface']:22s} {r['type']:11s} {r['status']:10s} {'charged' if r['charged'] else 'not charged':11s} "
          f"credit={r['credit'] or '-':10s} job={r['cat']}/{r['svc']}  {extra}")

print("\n==================== SEPTEMBER: what needs explaining ====================")
sep = [r for r in all_rows if r["month"] == "2026-09"]
for label, cond in (("declined", lambda r: r["status"] == "DECLINED"),
                    ("not charged", lambda r: not r["charged"]),
                    ("calls 0s (likely missed)", lambda r: r["type"] == "PHONE_CALL" and r["call"] == "0s"),
                    ("calls under 30s", lambda r: r["type"] == "PHONE_CALL" and r["call"] == "<30s"),
                    ("messages with no business reply", lambda r: r["type"] == "MESSAGE" and r["replied"] is False)):
    hit = [r for r in sep if cond(r)]
    print(f"  {label:32s} {len(hit):2d}  " + ", ".join(f"{r['date'][5:10]} {r['surface'].split()[1] if ' ' in r['surface'] else r['surface']}" for r in hit))
