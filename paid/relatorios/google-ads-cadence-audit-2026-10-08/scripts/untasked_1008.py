# READ-ONLY: per-campaign 30d/7d spend + conversions for accounts with no AT weekly task
import os
import sys
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
ACCTS=[("Proud Pops PPC","1051843378"),("PP LSA SA1","7261668241"),("PP LSA SA2","6621969129"),("PP LSA Roofing old","3477779749"),
("PP MFSC","9815330464"),("PP MFSC LSA NB","4127524472"),("PP MFSC LSA SA","4905286019"),
("Neon PPC","7953905280"),("Neon LSA","1219885876"),("Golden","4193142570"),("Integrate PPC","4571881760"),
("Integrate LSA Belleville","2895702982"),("Integrate LSA Carlstadt","2175964343"),("Integrate LSA Englewood","8323145223"),
("Strickland","9049508615"),("Nick's","1854100356"),("Cool Hand","9865206319"),("Eaglepoint","9005488539")]
for name,cid in ACTS if False else ACCTS:
    print(f"\n== {name} {cid}")
    agg={}
    for rng in ("LAST_30_DAYS","LAST_7_DAYS"):
        for r in run_query(cid, f"SELECT campaign.name, campaign.status, campaign.advertising_channel_type, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING {rng} AND metrics.cost_micros > 0"):
            c=r["campaign"]; m=r["metrics"]
            k=(c["name"][:50], c["status"], c["advertising_channel_type"])
            agg.setdefault(k,{})[rng]=(int(m.get("cost_micros") or 0)/1e6, float(m.get("conversions") or 0))
    for k,v in sorted(agg.items(), key=lambda x:-x[1].get("LAST_30_DAYS",(0,0))[0]):
        a=v.get("LAST_30_DAYS",(0,0)); b=v.get("LAST_7_DAYS",(0,0))
        print(f"   {k[0]:<50} {k[1]:<8} {k[2]:<16} 30d ${a[0]:>9,.0f} conv {a[1]:>5.1f} | 7d ${b[0]:>7,.0f} conv {b[1]:>4.1f}")
# Golden 09-17 change by Edu
for r in run_query("4193142570","SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation, change_event.changed_fields FROM change_event WHERE change_event.change_date_time >= '2026-09-16' AND change_event.change_date_time <= '2026-09-18' LIMIT 50"):
    print("GOLDEN 09-17:", r["change_event"])
