#!/usr/bin/env python3
"""
Google Tag Manager — operacoes (Tag Manager API v2).

Toda edicao acontece num WORKSPACE (rascunho). Publicar e um comando separado
e explicito (publish), nunca junto da edicao.

Uso (via wrapper ./gtm.sh ou com GADS_ENV_PATH setado):
  gtm.py accounts
  gtm.py containers   --account <accountId>
  gtm.py workspaces   --account <accountId> --container <containerId>
  gtm.py list         --account <accountId> --container <containerId> [--workspace <id>]
                        (tags, triggers e variables do workspace; default = workspace 1)
  gtm.py create-tag   --account <a> --container <c> --workspace <w> --json <file.json>
  gtm.py update-tag   --account <a> --container <c> --workspace <w> --tag <tagId> --json <file.json>
  gtm.py publish      --account <a> --container <c> --workspace <w> [--name "..."] [--notes "..."]

--json aponta pra um arquivo com o corpo da Tag no formato da API v2
(ver https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/tags).
"""

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from gtm_setup import gtm_service  # reusa auth


def _p(account, container=None, workspace=None):
    """Monta o path no formato accounts/{a}/containers/{c}/workspaces/{w}."""
    path = f"accounts/{account}"
    if container:
        path += f"/containers/{container}"
    if workspace:
        path += f"/workspaces/{workspace}"
    return path


def cmd_accounts(svc, args):
    resp = svc.accounts().list().execute()
    for a in resp.get("account", []):
        print(f"{a.get('accountId'):>12}  {a.get('name')}")


def cmd_containers(svc, args):
    resp = svc.accounts().containers().list(parent=_p(args.account)).execute()
    for c in resp.get("container", []):
        pubid = c.get("publicId", "")
        print(f"{c.get('containerId'):>12}  {pubid:<16}  {c.get('name')}")


def cmd_workspaces(svc, args):
    parent = _p(args.account, args.container)
    resp = svc.accounts().containers().workspaces().list(parent=parent).execute()
    for w in resp.get("workspace", []):
        print(f"{w.get('workspaceId'):>6}  {w.get('name')}")


def cmd_list(svc, args):
    ws = args.workspace or "1"
    parent = _p(args.account, args.container, ws)
    ws_api = svc.accounts().containers().workspaces()

    print(f"== Workspace {ws} ==\n")
    print("-- TAGS --")
    for t in ws_api.tags().list(parent=parent).execute().get("tag", []):
        print(f"  [{t.get('tagId'):>4}] {t.get('name')}  ({t.get('type')})")
    print("\n-- TRIGGERS --")
    for t in ws_api.triggers().list(parent=parent).execute().get("trigger", []):
        print(f"  [{t.get('triggerId'):>4}] {t.get('name')}  ({t.get('type')})")
    print("\n-- VARIABLES --")
    for v in ws_api.variables().list(parent=parent).execute().get("variable", []):
        print(f"  [{v.get('variableId'):>4}] {v.get('name')}  ({v.get('type')})")


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_create_tag(svc, args):
    parent = _p(args.account, args.container, args.workspace)
    body = _load_json(args.json)
    res = svc.accounts().containers().workspaces().tags().create(
        parent=parent, body=body).execute()
    print(f"Tag criada: [{res.get('tagId')}] {res.get('name')} (workspace {args.workspace}, ainda NAO publicado)")


def cmd_update_tag(svc, args):
    path = _p(args.account, args.container, args.workspace) + f"/tags/{args.tag}"
    body = _load_json(args.json)
    res = svc.accounts().containers().workspaces().tags().update(
        path=path, body=body).execute()
    print(f"Tag atualizada: [{res.get('tagId')}] {res.get('name')} (workspace {args.workspace}, ainda NAO publicado)")


def cmd_publish(svc, args):
    parent = _p(args.account, args.container, args.workspace)
    ws_api = svc.accounts().containers().workspaces()
    # 1) cria a versao a partir do workspace
    cv = ws_api.create_version(
        path=parent,
        body={"name": args.name or "CLI publish", "notes": args.notes or ""},
    ).execute()
    version = cv.get("containerVersion")
    if not version:
        print(f"ERRO ao criar versao: {json.dumps(cv, indent=2)}")
        sys.exit(1)
    vid = version.get("containerVersionId")
    # 2) publica a versao
    ver_path = _p(args.account, args.container) + f"/versions/{vid}"
    pub = svc.accounts().containers().versions().publish(path=ver_path).execute()
    print(f"PUBLICADO: versao {vid} — '{version.get('name')}'  (container ao vivo atualizado)")


COMMANDS = {
    "accounts": cmd_accounts,
    "containers": cmd_containers,
    "workspaces": cmd_workspaces,
    "list": cmd_list,
    "create-tag": cmd_create_tag,
    "update-tag": cmd_update_tag,
    "publish": cmd_publish,
}


def main():
    ap = argparse.ArgumentParser(description="Google Tag Manager v2 CLI")
    ap.add_argument("command", choices=COMMANDS.keys())
    ap.add_argument("--account")
    ap.add_argument("--container")
    ap.add_argument("--workspace")
    ap.add_argument("--tag")
    ap.add_argument("--json")
    ap.add_argument("--name")
    ap.add_argument("--notes")
    args = ap.parse_args()

    svc = gtm_service()
    COMMANDS[args.command](svc, args)


if __name__ == "__main__":
    main()
