"""Pull one LSA account's leads + call recordings straight from Google Ads. Read-only.
For clients whose LSA calls never touch CallRail (C&S, Napps, All Seasons, Cool Hand...).

  python pull_lsa.py <client-slug> <customer_id> <start YYYY-MM-DD> <end YYYY-MM-DD> [--no-audio]

<customer_id> = the account holding LSA (see LSA_ACCOUNTS in google-ads-ratos/scripts/lsa_report.py;
missing there: Napps 9239407401, Spencer 2524618054, King's 6769493219).
Uses the person's own Google Ads login (.env.topserv), no tsd.sh needed.
Writes into _pessoal/call-wins/<slug>/ (gitignored):
  lsa.json                  leads (type, status, charged) each with its conversations (calls + messages)
  audio/lsa_<conv id>.mp3   one file per recorded call
Google "BOOKED" = whatever the business tapped in the LSA app: report it beside the transcript outcome, never instead."""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
RATOS = os.path.join(ROOT, ".claude", "skills", "google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv"))
sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import init_client, run_query  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("slug"); ap.add_argument("customer_id"); ap.add_argument("start"); ap.add_argument("end")
ap.add_argument("--no-audio", action="store_true")
a = ap.parse_args()
cid = a.customer_id.replace("-", "")
out = os.path.join(ROOT, "_pessoal", "call-wins", a.slug)
os.makedirs(os.path.join(out, "audio"), exist_ok=True)

leads = {}
for r in run_query(cid, f"""
    SELECT local_services_lead.resource_name, local_services_lead.id, local_services_lead.lead_type,
      local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.category_id,
      local_services_lead.service_id, local_services_lead.creation_date_time
    FROM local_services_lead
    WHERE local_services_lead.creation_date_time >= '{a.start} 00:00:00'
      AND local_services_lead.creation_date_time <= '{a.end} 23:59:59'"""):
    l = r["local_services_lead"]
    leads[l["resource_name"]] = {**l, "conversations": []}

# Conversations can come days after the lead was created, so no upper date bound here
for r in run_query(cid, f"""
    SELECT local_services_lead_conversation.id, local_services_lead_conversation.lead,
      local_services_lead_conversation.event_date_time, local_services_lead_conversation.conversation_channel,
      local_services_lead_conversation.participant_type,
      local_services_lead_conversation.phone_call_details.call_duration_millis,
      local_services_lead_conversation.phone_call_details.call_recording_url,
      local_services_lead_conversation.message_details.text
    FROM local_services_lead_conversation
    WHERE local_services_lead_conversation.event_date_time >= '{a.start} 00:00:00'"""):
    c = r["local_services_lead_conversation"]
    if c["lead"] in leads:
        leads[c["lead"]]["conversations"].append(c)

json.dump(list(leads.values()), open(os.path.join(out, "lsa.json"), "w", encoding="utf-8"), indent=1)
calls = [c for l in leads.values() for c in l["conversations"] if c.get("phone_call_details", {}).get("call_recording_url")]
print(f"{len(leads)} LSA leads, {len(calls)} recorded calls -> {out}")
if a.no_audio or not calls:
    sys.exit()

# Recording URLs 302 to a login page without auth; with the Ads OAuth bearer token they return audio/mpeg
import requests  # noqa: E402
from google.auth.transport.requests import Request  # noqa: E402
creds = init_client().credentials
creds.refresh(Request())
new = 0
for c in calls:
    fn = os.path.join(out, "audio", f"lsa_{c['id']}.mp3")
    if os.path.exists(fn):
        continue
    resp = requests.get(c["phone_call_details"]["call_recording_url"],
                        headers={"Authorization": f"Bearer {creds.token}"}, timeout=120)
    if resp.ok and "audio" in (resp.headers.get("content-type") or ""):
        open(fn, "wb").write(resp.content)
        new += 1
        print(f"  lsa_{c['id']}  {c['event_date_time'][:16]}", flush=True)
    else:
        print(f"  lsa_{c['id']} FAILED: HTTP {resp.status_code} {resp.headers.get('content-type')}", flush=True)
    time.sleep(0.3)
print(f"{new} new recordings downloaded")
