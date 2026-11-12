"""Zen Air: lead outcomes since last check (LSA leads since 09-20 w/ status/notes/call length; PPC call_view since 10-14). Read-only."""
from lib import run_query

LSA = "3740502923"
PPC = "4360840956"

print("=== LSA leads since 2026-09-20 ===")
q = """
SELECT local_services_lead.id, local_services_lead.creation_date_time,
  local_services_lead.lead_type, local_services_lead.lead_status,
  local_services_lead.lead_charged, local_services_lead.service_id,
  local_services_lead.note.description, local_services_lead.note.edit_date_time
FROM local_services_lead
WHERE local_services_lead.creation_date_time >= '2026-09-20 00:00:00'
ORDER BY local_services_lead.creation_date_time
"""
for r in run_query(LSA, q):
    l = r["local_services_lead"]
    note = l.get("note", {})
    print(l.get("id"), l.get("creation_date_time"), l.get("lead_type"), l.get("lead_status"),
          "charged" if l.get("lead_charged") else "free", l.get("service_id"),
          "| note:", (note.get("description") or "").replace("\n", " "), note.get("edit_date_time", ""))

print("=== LSA conversations since 2026-09-20 ===")
q = """
SELECT local_services_lead_conversation.lead, local_services_lead_conversation.event_date_time,
  local_services_lead_conversation.conversation_channel,
  local_services_lead_conversation.participant_type,
  local_services_lead_conversation.phone_call_details.call_duration_millis
FROM local_services_lead_conversation
WHERE local_services_lead_conversation.event_date_time >= '2026-09-20 00:00:00'
"""
for r in run_query(LSA, q):
    c = r["local_services_lead_conversation"]
    ms = int(c.get("phone_call_details", {}).get("call_duration_millis", 0) or 0)
    print(c.get("lead", "").split("/")[-1], c.get("event_date_time"), c.get("conversation_channel"),
          c.get("participant_type"), f"{ms/1000:.0f}s")

print("=== LSA daily cost 10-14..today ===")
q = """
SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.conversions
FROM campaign WHERE segments.date BETWEEN '2026-10-14' AND '2026-10-23' ORDER BY segments.date
"""
tot = 0
for r in run_query(LSA, q):
    m = r["metrics"]; c = int(m.get("cost_micros", m.get("costMicros", 0)))/1e6; tot += c
    print(r["segments"]["date"], f"${c:.2f}", m.get("impressions"), m.get("conversions", 0))
print(f"total ${tot:.2f}")

print("=== PPC call_view since 2026-10-14 ===")
q = """
SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status,
  call_view.type, campaign.name
FROM call_view WHERE call_view.start_call_date_time >= '2026-10-14 00:00:00'
"""
rows = run_query(PPC, q)
if not rows: print("(no calls)")
for r in rows:
    print(r["callView"] if "callView" in r else r)

print("=== PPC conversions by action since 10-14 ===")
q = """
SELECT segments.date, segments.conversion_action_name, campaign.name, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2026-10-14' AND '2026-10-23' AND metrics.all_conversions > 0
"""
for r in run_query(PPC, q):
    print(r["segments"]["date"], r["segments"].get("conversion_action_name"), r["campaign"]["name"],
          r["metrics"].get("conversions"), r["metrics"].get("all_conversions"))
