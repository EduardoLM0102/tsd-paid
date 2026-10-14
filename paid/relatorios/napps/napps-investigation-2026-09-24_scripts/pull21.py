from h import *
L="9239407401"
q="""SELECT local_services_lead.id, local_services_lead.category_id, local_services_lead.service_id, local_services_lead.lead_type,
 local_services_lead.lead_status, local_services_lead.creation_date_time, local_services_lead.lead_charged, local_services_lead.locale,
 local_services_lead.credit_details.credit_state, local_services_lead.credit_details.credit_state_last_update_date_time
FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '2025-01-01 00:00:00'"""
try:
    rows=list(run_query(L,q))
except Exception as e:
    print("ERR", str(e)[:800]); raise SystemExit
print(len(rows))
json.dump(rows, open(OUT+"lsa_leads.json","w"), default=str)
print(json.dumps(rows[0], default=str, indent=1))
