from h import *
# find Supreme in MCC
MCC="4155514468"
q="SELECT customer_client.id, customer_client.descriptive_name, customer_client.status FROM customer_client WHERE customer_client.manager = false"
try:
    rows=list(run_query(MCC,q))
    for r in rows:
        n=r["customer_client"].get("descriptive_name","")
        if any(k in n.lower() for k in ["supreme","napps"]): print(r["customer_client"]["id"], n, r["customer_client"]["status"])
except Exception as e: print("ERR", str(e)[:300])
