"""Nick's Heating 1854100356: rate every unrated LSA / pay-per-lead lead since 10-15 (fu-161). One shot per lead, no undo.
Bad charged first (Google's credit cap is first-come). Leads < ~1 day old get FAIL_NOT_ELIGIBLE for credit, so the 11-18 wood-stove lead waits.
Run from workspace root: python3 paid/lsa-rating/nicks_rate_1119.py [--apply]"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RATOS = os.path.join(ROOT, ".claude/skills/google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv")); sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import init_client, run_query
CID = "1854100356"
# (lead_id, answer, reason, comment)  answer: DISSATISFIED / VERY_DISSATISFIED / SATISFIED / VERY_SATISFIED
R = [
 # bad, charged
 ("347879829", "DISSATISFIED", "JOB_TYPE_MISMATCH", "Kitchen hood lights and cleaning, not HVAC"),
 ("350495734", "DISSATISFIED", "JOB_TYPE_MISMATCH", "Duct cleaning, service not offered"),
 # good, charged
 ("351390078", "VERY_SATISFIED", "BOOKED_CUSTOMER", ""),
 ("349817877", "SATISFIED", "SERVICE_RELATED", ""),
 ("351610828", "SATISFIED", "SERVICE_RELATED", ""),
 ("351585545", "SATISFIED", "SERVICE_RELATED", ""),
 ("352433446", "SATISFIED", "SERVICE_RELATED", ""),
 ("352475955", "SATISFIED", "SERVICE_RELATED", ""),
 ("352483132", "SATISFIED", "SERVICE_RELATED", ""),
 ("352113287", "SATISFIED", "SERVICE_RELATED", ""),
 ("352699704", "SATISFIED", "SERVICE_RELATED", ""),
 ("352636355", "SATISFIED", "SERVICE_RELATED", ""),
 # not charged
 ("346480974", "SATISFIED", "SERVICE_RELATED", ""),
 ("346785449", "VERY_SATISFIED", "BOOKED_CUSTOMER", ""),
 ("349427268", "VERY_SATISFIED", "BOOKED_CUSTOMER", ""),
 ("349628522", "VERY_SATISFIED", "BOOKED_CUSTOMER", ""),
 ("350866308", "DISSATISFIED", "OTHER_DISSATISFIED_REASON", "Greeting then silence twice, caller never spoke"),
]
HOLD = {"352634291": "wood-burning stove venting (JOB_TYPE_MISMATCH), created 11-18 15:49: rate on/after 11-20 so it is credit-eligible"}
apply = "--apply" in sys.argv
st = {r["local_services_lead"]["id"]: r["local_services_lead"] for r in run_query(CID, "SELECT local_services_lead.id, local_services_lead.lead_feedback_submitted, local_services_lead.lead_charged, local_services_lead.creation_date_time FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-10-15 00:00:00'")}
client = init_client(); svc = client.get_service("LocalServicesLeadService"); E = client.enums
for lid, ans, reason, note in R:
    l = st.get(lid) or st.get(int(lid)) or {}
    if l.get("lead_feedback_submitted"): print(f"skip {lid} already rated"); continue
    print(f"{lid} {str(l.get('creation_date_time',''))[:16]} charged={l.get('lead_charged')} {ans} {reason} {note}")
    if not apply: continue
    req = client.get_type("ProvideLeadFeedbackRequest")
    req.resource_name = f"customers/{CID}/localServicesLeads/{lid}"
    req.survey_answer = getattr(E.LocalServicesLeadSurveyAnswerEnum, ans)
    if "DISSATISFIED" in ans:
        req.survey_dissatisfied.survey_dissatisfied_reason = getattr(E.LocalServicesLeadSurveyDissatisfiedReasonEnum, reason)
        if reason.startswith("OTHER"): req.survey_dissatisfied.other_reason_comment = note[:200]
    else:
        req.survey_satisfied.survey_satisfied_reason = getattr(E.LocalServicesLeadSurveySatisfiedReasonEnum, reason)
    try:
        r = svc.provide_lead_feedback(request=req); print("   -> OK", r.credit_issuance_decision.name)
    except Exception as e: print("   -> FAIL", str(e).splitlines()[0][:200])
print("HOLD:", HOLD)
