"""Zen Air strategy review pull, cycle 2026-10-10..2026-11-08. READ-ONLY.
PPC 4360840956 (campaign spend, daily, conversions by action, call_view) + LSA 3740502923 (campaign cost, leads + notes).
Run: python3 clients/zen-air/strategy_review_pull_1112.py  (uses .env.topserv via GADS_ENV_PATH like pull_lsa.py)"""
import os, sys, json
ROOT = os.path.expanduser("~/Documents/GitHub/topserv-workspace")
RATOS = os.path.join(ROOT, ".claude", "skills", "google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv"))
sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import run_query  # noqa

PPC, LSA = "4360840956", "3740502923"
S, E = "2026-10-10", "2026-11-08"
D = f"segments.date BETWEEN '{S}' AND '{E}'"
def M(x): return round((float(x) if x else 0) / 1e6, 2)
def q(cid, s):
    try:
        r = run_query(cid, s)
        if isinstance(r, dict): print("QUERY FAILED:", str(r)[:300]); return []
        return r
    except Exception as ex: print("QUERY FAILED:", str(ex)[:400]); return []

out = {}
print("## PPC campaigns", S, E)
rows = q(PPC, f"SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions, metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share FROM campaign WHERE {D}")
camps = []
for r in rows:
    c, m = r["campaign"], r["metrics"]
    if M(m.get("cost_micros")) == 0 and not m.get("impressions"): continue
    camps.append({"id": c["id"], "name": c["name"], "status": c["status"], "type": c.get("advertising_channel_type"), "cost": M(m.get("cost_micros")), "impr": m.get("impressions"), "clicks": m.get("clicks"), "conv": m.get("conversions"), "all_conv": m.get("all_conversions"), "IS": m.get("search_impression_share"), "rank_lost": m.get("search_rank_lost_impression_share"), "budget_lost": m.get("search_budget_lost_impression_share")})
for c in camps: print(json.dumps(c))
out["ppc_campaigns"] = camps

print("\n## PPC daily by campaign")
rows = q(PPC, f"SELECT segments.date, campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions FROM campaign WHERE {D} AND metrics.impressions > 0 ORDER BY segments.date")
daily = [{"date": r["segments"]["date"], "camp": r["campaign"]["name"][:30], "cost": M(r["metrics"].get("cost_micros")), "clicks": r["metrics"].get("clicks"), "impr": r["metrics"].get("impressions"), "conv": r["metrics"].get("conversions"), "all_conv": r["metrics"].get("all_conversions")} for r in rows]
for d in daily: print(json.dumps(d))
out["ppc_daily"] = daily

print("\n## PPC conversions by action (all_conversions)")
rows = q(PPC, f"SELECT campaign.name, segments.conversion_action_name, segments.conversion_action_category, metrics.all_conversions, metrics.conversions FROM campaign WHERE {D} AND metrics.all_conversions > 0")
acts = [{"camp": r["campaign"]["name"][:30], "action": r["segments"]["conversion_action_name"], "cat": r["segments"].get("conversion_action_category"), "all_conv": r["metrics"].get("all_conversions"), "conv": r["metrics"].get("conversions")} for r in rows]
for a in acts: print(json.dumps(a))
out["ppc_actions"] = acts

print("\n## PPC conversions by action by DATE")
rows = q(PPC, f"SELECT segments.date, campaign.name, segments.conversion_action_name, metrics.all_conversions FROM campaign WHERE {D} AND metrics.all_conversions > 0 ORDER BY segments.date")
for r in rows: print(json.dumps({"date": r["segments"]["date"], "camp": r["campaign"]["name"][:20], "action": r["segments"]["conversion_action_name"], "n": r["metrics"].get("all_conversions")}))

print("\n## PPC call_view (ad calls)")
rows = q(PPC, "SELECT call_view.start_call_date_time, call_view.end_call_date_time, call_view.call_duration_seconds, call_view.caller_area_code, call_view.caller_country_code, call_view.call_status, call_view.type, call_view.call_tracking_display_location, campaign.name, ad_group.name FROM call_view")
rows = [r for r in (rows if isinstance(rows, list) else []) if S <= (r["call_view"].get("start_call_date_time") or "")[:10] <= E]
calls = [{"start": r["call_view"].get("start_call_date_time"), "dur_s": r["call_view"].get("call_duration_seconds"), "area": r["call_view"].get("caller_area_code"), "status": r["call_view"].get("call_status"), "type": r["call_view"].get("type"), "loc": r["call_view"].get("call_tracking_display_location"), "camp": r["campaign"]["name"][:30], "adgroup": r.get("ad_group", {}).get("name")} for r in rows]
for c in calls: print(json.dumps(c))
out["ppc_calls"] = calls

print("\n## PPC search terms top (NB window) cost>0")
rows = q(PPC, f"SELECT campaign.name, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.all_conversions FROM search_term_view WHERE {D} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 40")
for r in rows: print(json.dumps({"camp": r["campaign"]["name"][:20], "term": r["search_term_view"]["search_term"], "cost": M(r["metrics"].get("cost_micros")), "clicks": r["metrics"].get("clicks"), "all_conv": r["metrics"].get("all_conversions")}))

print("\n## LSA campaigns", S, E)
rows = q(LSA, f"SELECT campaign.id, campaign.name, campaign.status, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions FROM campaign WHERE {D}")
lsa_c = [{"id": r["campaign"]["id"], "name": r["campaign"]["name"], "status": r["campaign"]["status"], "cost": M(r["metrics"].get("cost_micros")), "impr": r["metrics"].get("impressions"), "clicks": r["metrics"].get("clicks"), "conv": r["metrics"].get("conversions")} for r in rows]
for c in lsa_c: print(json.dumps(c))
out["lsa_campaigns"] = lsa_c

print("\n## LSA daily cost")
rows = q(LSA, f"SELECT segments.date, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions FROM campaign WHERE {D} AND metrics.impressions > 0 ORDER BY segments.date")
lsa_d = [{"date": r["segments"]["date"], "cost": M(r["metrics"].get("cost_micros")), "impr": r["metrics"].get("impressions"), "clicks": r["metrics"].get("clicks"), "conv": r["metrics"].get("conversions")} for r in rows]
for d in lsa_d: print(json.dumps(d))
out["lsa_daily"] = lsa_d

print("\n## LSA leads with notes + credit")
rows = q(LSA, f"SELECT local_services_lead.id, local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.service_id, local_services_lead.note.description, local_services_lead.credit_details.credit_state, local_services_lead.credit_details.credit_state_last_update_date_time FROM local_services_lead WHERE local_services_lead.creation_date_time >= '{S} 00:00:00' AND local_services_lead.creation_date_time <= '{E} 23:59:59' ORDER BY local_services_lead.creation_date_time")
if not rows:
    rows = q(LSA, f"SELECT local_services_lead.id, local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.service_id FROM local_services_lead WHERE local_services_lead.creation_date_time >= '{S} 00:00:00' AND local_services_lead.creation_date_time <= '{E} 23:59:59' ORDER BY local_services_lead.creation_date_time")
leads = []
for r in rows:
    l = r["local_services_lead"]
    leads.append({"id": l.get("id"), "created": l.get("creation_date_time"), "type": l.get("lead_type"), "status": l.get("lead_status"), "charged": l.get("lead_charged", False), "service": l.get("service_id"), "note": (l.get("note") or {}).get("description"), "credit": (l.get("credit_details") or {}).get("credit_state")})
for l in leads: print(json.dumps(l))
out["lsa_leads"] = leads

print("\n## LSA lead conversations (durations)")
rows = q(LSA, f"SELECT local_services_lead_conversation.id, local_services_lead_conversation.lead, local_services_lead_conversation.event_date_time, local_services_lead_conversation.conversation_channel, local_services_lead_conversation.participant_type, local_services_lead_conversation.phone_call_details.call_duration_millis, local_services_lead_conversation.message_details.text FROM local_services_lead_conversation WHERE local_services_lead_conversation.event_date_time >= '{S} 00:00:00' ORDER BY local_services_lead_conversation.event_date_time")
convs = []
for r in rows:
    c = r["local_services_lead_conversation"]
    convs.append({"id": c.get("id"), "lead": c.get("lead", "").split("/")[-1], "at": c.get("event_date_time"), "ch": c.get("conversation_channel"), "who": c.get("participant_type"), "dur_s": round(int((c.get("phone_call_details") or {}).get("call_duration_millis") or 0) / 1000), "msg": ((c.get("message_details") or {}).get("text") or "")[:160]})
for c in convs: print(json.dumps(c, ensure_ascii=False))
out["lsa_convs"] = convs

os.makedirs(os.path.join(ROOT, "_pessoal", "call-wins", "zen-air"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "_pessoal", "call-wins", "zen-air", "strategy_review_pull_1112.json"), "w"), indent=1)
print("\nsaved -> _pessoal/call-wins/zen-air/strategy_review_pull_1112.json")
