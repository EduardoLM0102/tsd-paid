#!/usr/bin/python3
"""tsd_funnel: tiny local MCP server (stdio, JSON-RPC 2.0, no SDK; Python 3.9) for the Command Center's "Refresh now" button.

One tool, refresh_funnel({client}): runs paid/funnels/funnel_build.py --client <slug> through tsd.sh (read-only pulls from Google Ads +
CallRail), then returns the built JSON document. The page writes it into its own database (funnels/<client>).
Registered in the Claude desktop app (claude_desktop_config.json -> mcpServers.tsd_funnel) and in Claude Code (user scope).
The page calls it as host:tsd_funnel. Only the artifact owner, in the Claude desktop app, can reach host servers.
"""
import json, os, subprocess, sys

WS = os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace"
TSD = f"{WS}/.claude/skills/google-ads-ratos/scripts/tsd.sh"
BUILDER = f"{WS}/paid/funnels/funnel_build.py"
CLIENTS = sorted(json.load(open(f"{WS}/paid/funnels/clients.json"))["clients"])   # every client with a funnel config
TOOL = {
    "name": "refresh_funnel",
    "description": "Pull fresh lead-funnel data (Google Ads + CallRail, read-only) for one client and return it as JSON.",
    "inputSchema": {"type": "object", "properties": {"client": {"type": "string", "enum": CLIENTS}}, "required": ["client"]},
    "annotations": {"title": "Refresh lead funnel", "readOnlyHint": True, "openWorldHint": True},
}


def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n"); sys.stdout.flush()


def run(client):
    if client not in CLIENTS: raise ValueError(f"No funnel set up for '{client}'.")
    p = subprocess.run([TSD, BUILDER, "--client", client], capture_output=True, text=True, timeout=110)
    out = (p.stdout or "") + (p.stderr or "")
    path = next((l.split(" ", 1)[1].split(" (")[0] for l in out.splitlines() if l.startswith("wrote ")), None)
    if p.returncode != 0 or not path or not os.path.exists(path):
        raise RuntimeError("The data pull failed: " + out.strip()[-600:])
    return open(path).read()


for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try: req = json.loads(line)
    except ValueError: continue
    mid, method = req.get("id"), req.get("method")
    if mid is None: continue                                   # notifications (initialized, cancelled)
    if method == "initialize":
        send({"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": (req.get("params") or {}).get("protocolVersion", "2025-06-18"),
              "capabilities": {"tools": {}}, "serverInfo": {"name": "tsd_funnel", "version": "1.0.0"}}})
    elif method == "tools/list":
        send({"jsonrpc": "2.0", "id": mid, "result": {"tools": [TOOL]}})
    elif method == "tools/call":
        params = req.get("params") or {}
        if params.get("name") != TOOL["name"]:
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "Unknown tool"}}); continue
        try:
            text = run((params.get("arguments") or {}).get("client", ""))
            send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": text}], "isError": False}})
        except Exception as e:
            send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": str(e)}], "isError": True}})
    elif method == "ping":
        send({"jsonrpc": "2.0", "id": mid, "result": {}})
    else:
        send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}})
