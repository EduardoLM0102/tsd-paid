"""Submit LSA / Pay-per-lead lead ratings (ProvideLeadFeedback) for Watt's Right 3651667805.
Reads _pessoal/call-wins/watts-right-lsa-rate-1117/ratings.json (PII stays local).
A lead can be rated ONCE. No validate_only on this endpoint, so --apply writes for real.
  python3 wr_lsa_rate_1117.py            # print plan only
  python3 wr_lsa_rate_1117.py --apply    # submit, skipping leads Google already shows as rated"""
import json, os, sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
RATOS=os.path.join(ROOT,".claude/skills/google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS,".env.topserv")); sys.path.insert(0, os.path.join(RATOS,"scripts"))
from lib import init_client, run_query
CID="3651667805"
rows=json.load(open(os.path.join(ROOT,"_pessoal/call-wins/watts-right-lsa-rate-1117/ratings.json")))
STRONG={"BOOKED_CUSTOMER":"VERY_SATISFIED","SPAM":"VERY_DISSATISFIED","SOLICITATION":"VERY_DISSATISFIED"}
apply="--apply" in sys.argv
done={r["local_services_lead"]["id"] for r in run_query(CID,"SELECT local_services_lead.id, local_services_lead.lead_feedback_submitted FROM local_services_lead WHERE local_services_lead.creation_date_time >= '2026-11-04 00:00:00'") if r["local_services_lead"].get("lead_feedback_submitted")}
client=init_client(); svc=client.get_service("LocalServicesLeadService")
E=client.enums; ok=fail=skip=0
for r in rows:
    if r["lead_id"] in done: skip+=1; continue
    ans=STRONG.get(r["reason"], r["answer"])
    print(f'{r["lead_id"]} {r["created"]} ch={int(r["charged"])} {ans} {r["reason"]} | {r["note"]}')
    if not apply: continue
    req=client.get_type("ProvideLeadFeedbackRequest")
    req.resource_name=f"customers/{CID}/localServicesLeads/{r['lead_id']}"
    req.survey_answer=getattr(E.LocalServicesLeadSurveyAnswerEnum, ans)
    if r["answer"]=="SATISFIED":
        req.survey_satisfied.survey_satisfied_reason=getattr(E.LocalServicesLeadSurveySatisfiedReasonEnum, r["reason"])
        if r["reason"]=="OTHER_SATISFIED_REASON": req.survey_satisfied.other_reason_comment=r["note"][:200]
    else:
        req.survey_dissatisfied.survey_dissatisfied_reason=getattr(E.LocalServicesLeadSurveyDissatisfiedReasonEnum, r["reason"])
        if r["reason"]=="OTHER_DISSATISFIED_REASON": req.survey_dissatisfied.other_reason_comment=r["note"][:200]
    try:
        resp=svc.provide_lead_feedback(request=req); ok+=1
        print("   -> OK", resp.credit_issuance_decision.name if hasattr(resp,"credit_issuance_decision") else resp)
    except Exception as e:
        fail+=1; print("   -> FAIL", str(e).splitlines()[0][:200])
print(f"\nplan={len(rows)} already_rated_skip={skip} submitted_ok={ok} failed={fail} apply={apply}")
