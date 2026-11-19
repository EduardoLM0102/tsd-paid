"""C&S Air LSA (inside 5563867754): rate the 11-18 burst (fu-161). One shot per lead, no undo.
What happened (25 recordings transcribed 11-19): a Lennox app glitch sent "C&S Air technician requesting access to your
system" alerts to Lennox owners across the US and Canada; they googled C&S Air, hit the LSA listing and called to ask.
Not customers, mostly out of the service area. 2 real calls in the window (existing customers) are rated good.
Leads < ~24h old get FAIL_NOT_ELIGIBLE for credit, so run on/after 2026-11-20 01:00 UTC (burst was 22:09-00:27 UTC, i.e. 16:09-18:27 Central).
Run from workspace root: python3 paid/lsa-rating/cs_rate_1118_burst.py [--apply]"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RATOS = os.path.join(ROOT, ".claude/skills/google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv")); sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import init_client, run_query
CID = "5563867754"
GLITCH = "Not a lead: Lennox app glitch sent C&S Air remote-access alerts to Lennox owners nationwide; caller is not a customer and asked about the alert"
CHARGED_BAD = ["353016979", "352642316", "353019919", "353043471", "353050671", "353026663", "352655735"]
FREE_BAD = ["353039208", "353017633", "353018011", "352641386", "352641389", "353019400", "353040324", "352643015",
            "353041647", "353041878", "353022619", "353031067"]
ROBO = ["353038161", "352637969", "352639331"]  # 4s "Number of allowed calls has been reached" robocalls
GOOD = ["352872097", "353055798"]                 # existing commercial maintenance; existing customer, 2 new systems not holding temp
apply = "--apply" in sys.argv
st = {str(r["local_services_lead"]["id"]): r["local_services_lead"] for r in run_query(CID, "SELECT local_services_lead.id, local_services_lead.lead_charged, local_services_lead.lead_feedback_submitted, local_services_lead.creation_date_time FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-18 00:00:00'")}
plan = [(i, "DISSATISFIED", "OTHER_DISSATISFIED_REASON", GLITCH) for i in CHARGED_BAD + FREE_BAD] + \
       [(i, "DISSATISFIED", "OTHER_DISSATISFIED_REASON", "Robocall: 4-second automated message, no caller") for i in ROBO] + \
       [(i, "SATISFIED", "SERVICE_RELATED", "") for i in GOOD]
client = init_client(); svc = client.get_service("LocalServicesLeadService"); E = client.enums
for lid, ans, reason, note in plan:
    l = st.get(lid, {})
    if not l: print(f"?? {lid} not found"); continue
    if l.get("lead_feedback_submitted"): print(f"skip {lid} already rated"); continue
    print(f"{lid} {l['creation_date_time'][:16]} charged={l.get('lead_charged')} {ans} {reason}")
    if not apply: continue
    req = client.get_type("ProvideLeadFeedbackRequest"); req.resource_name = f"customers/{CID}/localServicesLeads/{lid}"
    req.survey_answer = getattr(E.LocalServicesLeadSurveyAnswerEnum, ans)
    if ans == "DISSATISFIED":
        req.survey_dissatisfied.survey_dissatisfied_reason = getattr(E.LocalServicesLeadSurveyDissatisfiedReasonEnum, reason)
        req.survey_dissatisfied.other_reason_comment = note[:200]
    else:
        req.survey_satisfied.survey_satisfied_reason = getattr(E.LocalServicesLeadSurveySatisfiedReasonEnum, reason)
    try: r = svc.provide_lead_feedback(request=req); print("   -> OK", r.credit_issuance_decision.name)
    except Exception as e: print("   -> FAIL" if "already exists" not in str(e) else "   -> already rated", str(e).splitlines()[0][:150])
