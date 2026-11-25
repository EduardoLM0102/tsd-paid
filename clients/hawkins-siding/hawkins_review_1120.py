"""READ-ONLY. Hawkins strategy review pull (cycle 2026-10-24..2026-11-19, data through Nov 19).
Run: cd .claude/skills/google-ads-ratos/scripts && ./tsd.sh <abs path to this file> > out.json
Spend by campaign, conversions by action + campaign, ad calls (call_view), Google lead form submissions, LSA leads."""
import sys, json
sys.path.insert(0, '.')
from lib import run_query

CID = "2198608170"
A, B = "2026-10-24", "2026-11-19"
out = {}

def q(name, gaql):
    try:
        out[name] = list(run_query(CID, gaql))
    except BaseException as e:  # run_query exits on API error
        out[name] = {"error": repr(e)}

q("camp", f"""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
  metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions
  FROM campaign WHERE segments.date BETWEEN '{A}' AND '{B}' AND metrics.cost_micros > 0""")
q("camp_daily", f"""SELECT campaign.id, campaign.advertising_channel_type, segments.date, metrics.cost_micros
  FROM campaign WHERE segments.date BETWEEN '{A}' AND '{B}' AND metrics.cost_micros > 0""")
q("conv_by_action", f"""SELECT campaign.id, campaign.name, segments.conversion_action_name, segments.date,
  metrics.conversions, metrics.all_conversions
  FROM campaign WHERE segments.date BETWEEN '{A}' AND '{B}' AND metrics.all_conversions > 0""")
q("calls", f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
  call_view.type, campaign.id, campaign.name FROM call_view
  WHERE call_view.start_call_date_time >= '{A} 00:00:00' AND call_view.start_call_date_time <= '{B} 23:59:59'""")
q("lead_forms", f"""SELECT lead_form_submission_data.submission_date_time, lead_form_submission_data.campaign,
  lead_form_submission_data.ad_group_ad, lead_form_submission_data.gclid,
  lead_form_submission_data.lead_form_submission_fields
  FROM lead_form_submission_data
  WHERE lead_form_submission_data.submission_date_time >= '{A} 00:00:00'""")
q("lsa_leads", f"""SELECT local_services_lead.id, local_services_lead.lead_type, local_services_lead.lead_status,
  local_services_lead.lead_charged, local_services_lead.creation_date_time, local_services_lead.credit_details.credit_state
  FROM local_services_lead
  WHERE local_services_lead.creation_date_time >= '{A} 00:00:00' AND local_services_lead.creation_date_time <= '{B} 23:59:59'""")
json.dump(out, sys.stdout, default=str, indent=1)
