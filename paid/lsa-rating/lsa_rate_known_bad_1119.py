"""Rate the LSA leads already judged BAD by transcript (fu-161 known list + Napps 11-19 review), across accounts.
Dry run prints each target's match (by lead id, or by creation minute + type). --apply submits (one shot per lead, no undo).
Run: python3 paid/lsa-rating/lsa_rate_known_bad_1119.py [--apply]"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RATOS = os.path.join(ROOT, ".claude/skills/google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv")); sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import init_client, run_query
# (client, cid, lead_id or None, created 'YYYY-MM-DD HH:MM' or None, type or None, reason, comment)
T = [
 ("Napps", "9239407401", None, "2026-10-23 07:48", "PHONE_CALL", "OTHER_DISSATISFIED_REASON", "No conversation: answering service greeting only, caller never spoke"),
 ("Napps", "9239407401", None, "2026-11-07 11:37", "PHONE_CALL", "OTHER_DISSATISFIED_REASON", "No conversation: garbled greeting, caller never spoke"),
 ("Spencer", "2524618054", None, "2026-10-29 12:11", None, "JOB_TYPE_MISMATCH", "Refrigerant (R410A) price check, not a service request"),
 ("King's", "6769493219", "348497405", None, None, "OTHER_DISSATISFIED_REASON", "Greeting only, caller never spoke (10-28 16:19, 35s)"),
 ("King's", "6769493219", "350495350", None, None, "OTHER_DISSATISFIED_REASON", "Greeting only, caller never spoke (11-06 12:42, 59s)"),
 ("King's", "6769493219", "350516187", None, None, "JOB_TYPE_MISMATCH", "Vehicle (SUV) windshield, they do house windows only"),
 ("Zen Air", "3740502923", None, "2026-10-28 14:04", "PHONE_CALL", "OTHER_DISSATISFIED_REASON", "Wrong number: New York caller looking for someone named David"),
 ("Proud Pops elec", "7261668241", "346547072", None, None, "OTHER_DISSATISFIED_REASON", "39s greeting only, caller never spoke"),
 ("Proud Pops elec", "7261668241", "351353602", None, None, "JOB_TYPE_MISMATCH", "Christmas lights for a car wash, service not offered"),
 ("Proud Pops main", "1051843378", "351579426", None, None, "SPAM", "Review-selling spam message"),
 ("All Seasons", "8655979348", None, "2026-10-12 08:59", "MESSAGE", "JOB_TYPE_MISMATCH", "Oil boiler maintenance, they don't service oil"),
 ("All Seasons", "8655979348", None, "2026-11-02 14:48", "PHONE_CALL", "JOB_TYPE_MISMATCH", "Heating oil delivery, service not offered"),
 ("All Seasons", "8655979348", None, "2026-11-05 16:15", "PHONE_CALL", "JOB_TYPE_MISMATCH", "Oil boiler checkup, they don't service oil"),
]
F = "local_services_lead.id, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.creation_date_time, local_services_lead.lead_feedback_submitted, local_services_lead.credit_details.credit_state"
apply = "--apply" in sys.argv
cache = {}
def leads(cid):
    if cid not in cache:
        cache[cid] = [r["local_services_lead"] for r in run_query(cid, f"SELECT {F} FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-10-10 00:00:00'")]
    return cache[cid]
plan = []
for (cl, cid, lid, created, typ, reason, note) in T:
    L = leads(cid)
    if lid: m = [l for l in L if str(l["id"]) == lid]
    elif typ in ("GREETING", "SUV"): m = [l for l in L if l["creation_date_time"].startswith(created)]
    else: m = [l for l in L if l["creation_date_time"].startswith(created) and (typ is None or l["lead_type"] == typ)]
    tag = "" if len(m) == 1 else f"  <-- {len(m)} MATCHES, SKIP"
    print(f"{cl:<16} {created or lid} {reason:<26}{tag}")
    for l in m: print(f"     id {l['id']} {l['creation_date_time'][:16]} {l['lead_type']} {l['lead_status']} charged={l.get('lead_charged')} rated={l.get('lead_feedback_submitted')} credit={l.get('credit_details',{}).get('credit_state')}")
    if len(m) == 1 and not m[0].get("lead_feedback_submitted"): plan.append((cl, cid, str(m[0]["id"]), reason, note, m[0].get("lead_charged")))
print(f"\nready to rate: {len(plan)}")
if apply:
    client = init_client(); svc = client.get_service("LocalServicesLeadService"); E = client.enums
    plan.sort(key=lambda p: not p[5])  # charged first
    for cl, cid, lid, reason, note, ch in plan:
        req = client.get_type("ProvideLeadFeedbackRequest")
        req.resource_name = f"customers/{cid}/localServicesLeads/{lid}"
        req.survey_answer = E.LocalServicesLeadSurveyAnswerEnum.VERY_DISSATISFIED if reason in ("SPAM", "SOLICITATION") else E.LocalServicesLeadSurveyAnswerEnum.DISSATISFIED
        req.survey_dissatisfied.survey_dissatisfied_reason = getattr(E.LocalServicesLeadSurveyDissatisfiedReasonEnum, reason)
        if reason == "OTHER_DISSATISFIED_REASON": req.survey_dissatisfied.other_reason_comment = note[:200]
        try:
            r = svc.provide_lead_feedback(request=req); print(f"OK   {cl} {lid} charged={ch} -> {r.credit_issuance_decision.name}")
        except Exception as e: print(f"FAIL {cl} {lid}: {str(e).splitlines()[0][:200]}")
