#!/usr/bin/env python3
"""
Google Analytics 4 — leitura (Admin API + Data API).

Uso (via ./gtm.sh, que carrega o perfil TopServ):
  ga4.py properties                       # contas + properties (id numerico pra usar em --property)
  ga4.py streams   --property <id>        # data streams (acha o Measurement ID G-XXXX)
  ga4.py events    --property <id> --start 2026-06-25 --end 2026-07-23
  ga4.py report    --property <id> --start ... --end ...
                   --dimensions date,sessionSource --metrics sessions,conversions
  ga4.py conversions --property <id> --start ... --end ...   # eventos marcados como key event

Datas: YYYY-MM-DD, ou atalhos do GA4 (NdaysAgo, yesterday, today).
"""

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ga4_setup import admin_service, data_service


def _rows(resp):
    """Normaliza a resposta do runReport em (headers, linhas)."""
    dims = [h["name"] for h in resp.get("dimensionHeaders", [])]
    mets = [h["name"] for h in resp.get("metricHeaders", [])]
    out = []
    for r in resp.get("rows", []):
        dv = [d.get("value") for d in r.get("dimensionValues", [])]
        mv = [m.get("value") for m in r.get("metricValues", [])]
        out.append(dv + mv)
    return dims + mets, out


def _print_table(headers, rows, limit=None):
    if not rows:
        print("  (sem dados no periodo)")
        return
    if limit:
        rows = rows[:limit]
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    print("  " + "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers)))
    print("  " + "  ".join("-" * widths[i] for i in range(len(headers))))
    for r in rows:
        print("  " + "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))


def run_report(prop, dimensions, metrics, start, end, order_desc=None, limit=100):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dimensions],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    if order_desc:
        body["orderBys"] = [{"metric": {"metricName": order_desc}, "desc": True}]
    return data_service().properties().runReport(
        property=f"properties/{prop}", body=body).execute()


def cmd_properties(args):
    svc = admin_service()
    accounts = svc.accounts().list().execute().get("accounts", [])
    for a in accounts:
        print(f"\n{a.get('displayName')}  ({a.get('name')})")
        try:
            props = svc.properties().list(
                filter=f"parent:{a.get('name')}").execute().get("properties", [])
            for p in props:
                pid = p.get("name", "").split("/")[-1]
                print(f"   property {pid:<14} {p.get('displayName')}")
        except Exception as e:
            print(f"   erro listando properties: {e}")


def cmd_streams(args):
    svc = admin_service()
    streams = svc.properties().dataStreams().list(
        parent=f"properties/{args.property}").execute().get("dataStreams", [])
    for s in streams:
        web = s.get("webStreamData", {}) or {}
        print(f"  {s.get('displayName')}  measurementId={web.get('measurementId')}  url={web.get('defaultUri')}")


def cmd_events(args):
    resp = run_report(args.property, ["eventName"], ["eventCount", "totalUsers"],
                      args.start, args.end, order_desc="eventCount", limit=args.limit or 100)
    h, rows = _rows(resp)
    print(f"=== Eventos {args.start} -> {args.end} (property {args.property}) ===")
    _print_table(h, rows)


def cmd_conversions(args):
    # key events (antigo "conversions") por nome
    resp = run_report(args.property, ["eventName"], ["keyEvents", "eventCount"],
                      args.start, args.end, order_desc="keyEvents", limit=args.limit or 100)
    h, rows = _rows(resp)
    rows = [r for r in rows if r[1] not in ("0", "0.0", None)]
    print(f"=== Key events (conversoes) {args.start} -> {args.end} ===")
    _print_table(h, rows)


def cmd_report(args):
    dims = [d.strip() for d in (args.dimensions or "date").split(",") if d.strip()]
    mets = [m.strip() for m in (args.metrics or "sessions").split(",") if m.strip()]
    resp = run_report(args.property, dims, mets, args.start, args.end,
                      order_desc=args.order, limit=args.limit or 200)
    h, rows = _rows(resp)
    print(f"=== {','.join(dims)} x {','.join(mets)} | {args.start} -> {args.end} ===")
    _print_table(h, rows)


COMMANDS = {
    "properties": cmd_properties,
    "streams": cmd_streams,
    "events": cmd_events,
    "conversions": cmd_conversions,
    "report": cmd_report,
}


def main():
    ap = argparse.ArgumentParser(description="GA4 (Admin + Data API) — leitura")
    ap.add_argument("command", choices=COMMANDS.keys())
    ap.add_argument("--property")
    ap.add_argument("--start", default="28daysAgo")
    ap.add_argument("--end", default="yesterday")
    ap.add_argument("--dimensions")
    ap.add_argument("--metrics")
    ap.add_argument("--order")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    if args.command != "properties" and not args.property:
        print("ERRO: --property e obrigatorio (rode 'ga4.py properties' pra achar o id)")
        sys.exit(1)
    COMMANDS[args.command](args)


if __name__ == "__main__":
    main()
