# READ-ONLY: change_event (last 30 days) + 30d spend per current TSD Google account
import os
import sys, json, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query

ACCTS = [
 ("Proud Pops - PPC","1051843378"),("Proud Pops - LSA SA 1","7261668241"),("Proud Pops - LSA SA 2","6621969129"),
 ("Proud Pops - LSA Roofing (old PS)","3477779749"),("Proud Pops - MFSC","9815330464"),("Proud Pops - MFSC LSA NB","4127524472"),
 ("Proud Pops - MFSC LSA SA","4905286019"),
 ("Watt's Right","3651667805"),("On The Way","3454686129"),("Strickland","9049508615"),("Hawkins Siding","2198608170"),
 ("Neon Monkey - PPC","7953905280"),("Neon Monkey - LSA","1219885876"),("Golden Plumbing","4193142570"),
 ("All Seasons AC","4467722415"),("King's Window","6769493219"),("Zen Air - PPC","4360840956"),("Zen Air - LSA","3740502923"),
 ("Napps - PPC","9509605037"),("Napps - LSA","9239407401"),("Spencer Air","2524618054"),("Nick's Heating","1854100356"),
 ("Integrate Comfort - PPC","4571881760"),("Integrate - LSA Belleville","2895702982"),("Integrate - LSA Carlstadt","2175964343"),
 ("Integrate - LSA Englewood Cliffs","8323145223"),("Live Wire Electric","1056617442"),("C&S Air","5563867754"),
 ("Mission Accomplished - PPC","8634274092"),("Mission Accomplished - LSA","4904262993"),("GC Home Service - PPC","2375064049"),
 ("GC Home Service - LSA","2974002658"),("Cool Hand Electric","9865206319"),("Lilypad Septic","3797438623"),
 ("Gillespie's","7410489772"),("Eaglepoint Roofing","9005488539"),
]
START, END = "2026-09-09", "2026-10-08 23:59:59"
out = {}
for name, cid in ACCTS:
    rec = {"cid": cid}
    try:
        sp = run_query(cid, "SELECT metrics.cost_micros, metrics.conversions FROM customer WHERE segments.date DURING LAST_30_DAYS")
        rec["spend30"] = sum(int(r["metrics"].get("cost_micros") or 0) for r in sp)/1e6
        sp7 = run_query(cid, "SELECT metrics.cost_micros FROM customer WHERE segments.date DURING LAST_7_DAYS")
        rec["spend7"] = sum(int(r["metrics"].get("cost_micros") or 0) for r in sp7)/1e6
        ch = run_query(cid, f"""
          SELECT change_event.change_date_time, change_event.user_email, change_event.client_type,
                 change_event.change_resource_type, change_event.resource_change_operation, change_event.campaign
          FROM change_event
          WHERE change_event.change_date_time >= '{START}' AND change_event.change_date_time <= '{END}'
          ORDER BY change_event.change_date_time DESC LIMIT 10000""")
        rows = []
        for r in ch:
            e = r["change_event"]
            rows.append({"t": e.get("change_date_time"), "u": e.get("user_email"), "c": e.get("client_type"),
                         "res": e.get("change_resource_type"), "op": e.get("resource_change_operation")})
        rec["changes"] = rows
    except SystemExit as ex:
        rec["error"] = f"SystemExit {ex}"
    except Exception as ex:
        rec["error"] = str(ex)[:300]
    out[name] = rec
    print(name, cid, "spend30=%.0f" % rec.get("spend30", -1), "changes=%d" % len(rec.get("changes", [])), rec.get("error",""), flush=True)
json.dump(out, open("/private/tmp/claude-501/-Users-eduardolarangeirasmarinho/1f8861ac-a9d4-4159-9b75-834135105dca/scratchpad/change_audit_1008.json","w"), indent=1, default=str)
