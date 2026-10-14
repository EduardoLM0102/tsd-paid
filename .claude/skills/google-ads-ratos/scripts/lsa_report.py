#!/usr/bin/env python3
"""
LSA lead report — todos os clientes TSD com presenca em Local Services Ads.

Roda local_services_lead.* (nao e metrics de PPC) em cada conta que carrega
LSA, seja dentro da mesma conta de PPC (campanha LOCAL_SERVICES) ou em uma
conta LSA dedicada. Lista vem de contas.yaml, curada manualmente abaixo —
atualizar aqui quando um cliente novo ligar LSA ou uma conta LSA fechar.

Uso:
    ./tsd.sh lsa_report.py                     # ultimos 30 dias, todas as contas
    ./tsd.sh lsa_report.py --days 7
    ./tsd.sh lsa_report.py --since 2026-08-01 --until 2026-08-25
    ./tsd.sh lsa_report.py --client "Watt's Right"   # filtra por nome (substring)
"""

import argparse
import sys
from datetime import date, timedelta

sys.path.insert(0, ".")
from lib import init_client

# ---------------------------------------------------------------------------
# Registro de contas com LSA (curado a partir de contas.yaml, 2026-08-25)
# ---------------------------------------------------------------------------
# mode: "same_account"  -> campanha LOCAL_SERVICES vive dentro da conta de PPC
#       "dedicated"      -> customer_id e uma conta so de LSA

LSA_ACCOUNTS = [
    {"client": "Cool Hand Electric", "customer_id": "9865206319", "mode": "same_account",
     "note": "LSA existe mas fora do escopo TSD (decisao do Edu) — leitura de dados ok."},
    {"client": "Mission Accomplished", "customer_id": "4904262993", "mode": "dedicated",
     "note": "PPC: 8634274092"},
    {"client": "Hawkins Siding and Exterior", "customer_id": "2198608170", "mode": "same_account",
     "note": "Campanha LSA 21211420266"},
    {"client": "Neon Monkey Services", "customer_id": "1219885876", "mode": "dedicated",
     "note": "PPC: 7953905280"},
    {"client": "Golden Plumbing", "customer_id": "4193142570", "mode": "same_account",
     "note": "Campanha LSA 21051260085, LSA ATIVA mesmo com PPC pausado"},
    {"client": "Zen Air Heating and Cooling", "customer_id": "3740502923", "mode": "dedicated",
     "note": "PPC: 4360840956"},
    {"client": "C&S Air", "customer_id": "5563867754", "mode": "same_account",
     "note": "Conta se chama '(LSA) C&S Air' mas tem PPC completo dentro"},
    {"client": "Gillespie's Heating and Cooling", "customer_id": "7410489772", "mode": "same_account",
     "note": "Campanha LSA 23940351598, near-zero volume, fora do escopo PPC"},
    {"client": "Watt's Right Electric", "customer_id": "3651667805", "mode": "same_account",
     "note": "~86% do spend/leads da conta"},
    {"client": "Watt's Right - Broken Arrow (sister)", "customer_id": "9261944882", "mode": "dedicated",
     "note": "Dormant, zero spend historicamente — checar mesmo assim"},
    {"client": "Proud Pops Plumbing, Air & Electric", "customer_id": "1051843378", "mode": "same_account",
     "note": "Campanha LOCAL_SERVICES:SystemGenerated dentro da conta PPC"},
    {"client": "Proud Pops - LSA San Antonio [1]", "customer_id": "7261668241", "mode": "dedicated",
     "note": "Eletricista, Boerne/Helotes/Seguin TX"},
    {"client": "Proud Pops - LSA San Antonio [2]", "customer_id": "6621969129", "mode": "dedicated",
     "note": "HVAC, Bandera/Converse/Kerrville TX"},
    {"client": "My Favorite Service Company - LSA New Braunfels", "customer_id": "4127524472", "mode": "dedicated",
     "note": "Sem spend desde fev/2026 — checar mesmo assim"},
    {"client": "My Favorite Service Company - LSA San Antonio", "customer_id": "4905286019", "mode": "dedicated",
     "note": "Sem spend desde fev/2026 — checar mesmo assim"},
    {"client": "All Seasons AC", "customer_id": "8655979348", "mode": "dedicated",
     "note": "PPC: 4467722415. LSA live sob o MCC desde 2026-10-14 (faltavam docs de verificacao)"},
]


def build_query(since, until):
    return f"""
        SELECT
            local_services_lead.id,
            local_services_lead.lead_type,
            local_services_lead.lead_status,
            local_services_lead.lead_charged,
            local_services_lead.credit_details.credit_state
        FROM local_services_lead
        WHERE local_services_lead.creation_date_time >= '{since} 00:00:00'
            AND local_services_lead.creation_date_time <= '{until} 23:59:59'
    """


def fetch_leads(client, customer_id, query):
    """Roda a query numa conta, sem derrubar o loop se a conta der erro."""
    service = client.get_service("GoogleAdsService")
    try:
        response = service.search(customer_id=customer_id, query=query)
        rows = []
        for row in response:
            lead = row.local_services_lead
            rows.append({
                "lead_type": lead.lead_type.name if lead.lead_type else "UNSPECIFIED",
                "lead_status": lead.lead_status.name if lead.lead_status else "UNSPECIFIED",
                "lead_charged": bool(lead.lead_charged),
                "credit_state": lead.credit_details.credit_state.name if lead.credit_details.credit_state else None,
            })
        return rows, None
    except Exception as e:
        return None, str(e).splitlines()[0][:180]


def summarize(rows):
    total = len(rows)
    charged = sum(1 for r in rows if r["lead_charged"])
    by_type = {}
    by_status = {}
    credited = 0
    for r in rows:
        by_type[r["lead_type"]] = by_type.get(r["lead_type"], 0) + 1
        by_status[r["lead_status"]] = by_status.get(r["lead_status"], 0) + 1
        if r["credit_state"] and r["credit_state"] not in ("UNSPECIFIED", "UNKNOWN", None):
            credited += 1
    return total, charged, by_type, by_status, credited


def main():
    ap = argparse.ArgumentParser(description="Relatorio global de leads LSA — todas as contas TSD")
    ap.add_argument("--days", type=int, default=30, help="Janela em dias a partir de hoje (default: 30)")
    ap.add_argument("--since", help="Data inicio (YYYY-MM-DD)")
    ap.add_argument("--until", help="Data fim (YYYY-MM-DD)")
    ap.add_argument("--client", help="Filtra por nome do cliente (substring, case-insensitive)")
    args = ap.parse_args()

    if args.since and args.until:
        since, until = args.since, args.until
    else:
        until_d = date.today()
        since_d = until_d - timedelta(days=args.days)
        since, until = since_d.isoformat(), until_d.isoformat()

    accounts = LSA_ACCOUNTS
    if args.client:
        needle = args.client.lower()
        accounts = [a for a in accounts if needle in a["client"].lower()]
        if not accounts:
            print(f"Nenhuma conta LSA cadastrada bate com '{args.client}'.")
            sys.exit(1)

    client = init_client()
    query = build_query(since, until)

    print("=" * 100)
    print(f"LSA LEAD REPORT — {since} a {until}  ({len(accounts)} conta(s))")
    print("=" * 100)

    grand_total = 0
    grand_charged = 0
    grand_credited = 0
    errors = []

    for acc in accounts:
        rows, err = fetch_leads(client, acc["customer_id"], query)
        print(f"\n{acc['client']}  (customer_id {acc['customer_id']}, {acc['mode']})")
        if acc.get("note"):
            print(f"  note: {acc['note']}")
        if err:
            print(f"  ERRO: {err}")
            errors.append((acc["client"], err))
            continue

        total, charged, by_type, by_status, credited = summarize(rows)
        grand_total += total
        grand_charged += charged
        grand_credited += credited

        if total == 0:
            print("  0 leads no periodo.")
            continue

        type_str = ", ".join(f"{k}={v}" for k, v in sorted(by_type.items(), key=lambda x: -x[1]))
        status_str = ", ".join(f"{k}={v}" for k, v in sorted(by_status.items(), key=lambda x: -x[1]))
        print(f"  total={total}  charged={charged} ({charged/total:.0%})  credited/disputed={credited}")
        print(f"  by_type: {type_str}")
        print(f"  by_status: {status_str}")

    print("\n" + "=" * 100)
    print(f"TOTAL (todas as contas listadas): {grand_total} leads, {grand_charged} charged, {grand_credited} credited/disputed")
    if errors:
        print(f"\n{len(errors)} conta(s) com erro (ver acima) — provavel CUSTOMER_NOT_ENABLED ou sem campanha LOCAL_SERVICES ativa.")
    print("=" * 100)


if __name__ == "__main__":
    main()
