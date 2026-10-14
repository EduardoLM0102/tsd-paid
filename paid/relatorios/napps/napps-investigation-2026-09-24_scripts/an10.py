import json
from collections import defaultdict
def f(x):
    try: return float(x)
    except: return 0.0
rows=json.load(open("call_view.json"))
calls=[(r["call_view"]["start_call_date_time"][:10], int(r["call_view"].get("call_duration_seconds") or 0), r["call_view"]["call_status"], r["campaign"]["name"]) for r in rows]
daily=json.load(open("daily_all.json"))
spend=defaultdict(float); clicks=defaultdict(float)
for r in daily:
    spend[r["segments"]["date"]]+=f(r["metrics"].get("cost_micros"))/1e6; clicks[r["segments"]["date"]]+=f(r["metrics"].get("clicks"))
W=[("2025-03-24","2025-09-23","LY window"),("2025-09-24","2026-03-23","prior 6mo"),("2026-03-24","2026-09-23","LAST 6mo"),
   ("2025-06-01","2025-08-31","Summer 2025 (Jun-Aug)"),("2026-06-01","2026-08-31","Summer 2026 (Jun-Aug)"),
   ("2025-06-01","2025-09-23","Jun1-Sep23 2025"),("2026-06-01","2026-09-23","Jun1-Sep23 2026"),
   ("2025-01-01","2025-12-31","CY2025"),("2026-01-01","2026-09-23","2026 YTD"),("2025-01-01","2025-09-23","2025 YTD (same days)"),
   ("2024-05-01","2024-12-31","2024 May-Dec (BC era)")]
print(f"{'window':28s} {'spend':>9s} {'clicks':>7s} {'calls':>6s} {'>=30s':>6s} {'>=60s':>6s} {'missed':>6s} {'spend/call':>10s} {'spend/call>=60s':>15s}")
for lo,hi,l in W:
    c=[x for x in calls if lo<=x[0]<=hi]
    sp=sum(v for k,v in spend.items() if lo<=k<=hi); ck=sum(v for k,v in clicks.items() if lo<=k<=hi)
    n=len(c); n30=sum(1 for x in c if x[1]>=30); n60=sum(1 for x in c if x[1]>=60); ms=sum(1 for x in c if x[2]=="MISSED")
    print(f"{l:28s} {sp:9.0f} {ck:7.0f} {n:6d} {n30:6d} {n60:6d} {ms:6d} {sp/n if n else 0:10.0f} {sp/n60 if n60 else 0:15.0f}")
