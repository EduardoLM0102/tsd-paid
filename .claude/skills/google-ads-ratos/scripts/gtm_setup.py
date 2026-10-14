#!/usr/bin/env python3
"""
GTM Setup interativo — gera o refresh token do Google Tag Manager.

Reaproveita o MESMO OAuth client Desktop do Google Ads (GOOGLE_ADS_CLIENT_ID/SECRET),
mas com os escopos do Tag Manager e um refresh token SEPARADO (GTM_REFRESH_TOKEN),
pra nao encostar no token do Ads que ja funciona.

Uso:
  GADS_ENV_PATH=<.env> python3 gtm_setup.py oauth   # gera GTM_REFRESH_TOKEN
  GADS_ENV_PATH=<.env> python3 gtm_setup.py test     # lista contas GTM acessiveis
  GADS_ENV_PATH=<.env> python3 gtm_setup.py check     # verifica .env

Ou via wrapper: ./gtm.sh gtm_setup.py oauth
"""

import hashlib
import os
import re
import socket
import sys
import webbrowser
from urllib.parse import unquote

# O OAuth client ja tem o escopo 'adwords' autorizado (Google Ads). Com
# include_granted_scopes, o Google devolve GTM + adwords juntos, e o oauthlib
# trata "scope mudou" como erro. Relaxa essa checagem.
os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ENV_PATH = os.environ.get("GADS_ENV_PATH") or os.path.join(SKILL_DIR, ".env")
SERVER = "127.0.0.1"

# Escopos: ler + editar containers + editar/criar versoes + publicar.
SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.readonly",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
]

sys.path.insert(0, SCRIPT_DIR)
from lib import _load_env_file, mask_token


# ---------------------------------------------------------------------------
# Credenciais do GTM (usadas por gtm.py tambem)
# ---------------------------------------------------------------------------

def gtm_credentials():
    """Monta Credentials do GTM a partir do .env (client do Ads + GTM_REFRESH_TOKEN)."""
    from google.oauth2.credentials import Credentials

    _load_env_file()
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "").strip()
    refresh_token = os.environ.get("GTM_REFRESH_TOKEN", "").strip()

    missing = [n for n, v in [
        ("GOOGLE_ADS_CLIENT_ID", client_id),
        ("GOOGLE_ADS_CLIENT_SECRET", client_secret),
        ("GTM_REFRESH_TOKEN", refresh_token),
    ] if not v]
    if missing:
        print(f"ERRO: falta no .env ({ENV_PATH}): {', '.join(missing)}", file=sys.stderr)
        if missing == ["GTM_REFRESH_TOKEN"]:
            print("  Rode: python3 gtm_setup.py oauth", file=sys.stderr)
        sys.exit(1)

    return Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )


def gtm_service():
    """Retorna o service tagmanager v2 autenticado."""
    from googleapiclient.discovery import build
    return build("tagmanager", "v2", credentials=gtm_credentials(), cache_discovery=False)


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

def check_dependencies():
    missing = []
    try:
        import googleapiclient  # noqa: F401
    except ImportError:
        missing.append("google-api-python-client")
    try:
        import google_auth_oauthlib  # noqa: F401
    except ImportError:
        missing.append("google-auth-oauthlib")
    if missing:
        print(f"FALTAM: {', '.join(missing)}")
        print(f"  Instale com: pip3 install --user {' '.join(missing)}")
        return False
    print("OK: Dependencias instaladas")
    return True


def cmd_check():
    print("=== Dependencias ===")
    check_dependencies()
    print()
    print("=== .env ===")
    if not os.path.isfile(ENV_PATH):
        print(f"  FALTA: .env nao encontrado em {ENV_PATH}")
        return
    _load_env_file()
    for key in ["GOOGLE_ADS_CLIENT_ID", "GOOGLE_ADS_CLIENT_SECRET", "GTM_REFRESH_TOKEN"]:
        val = os.environ.get(key)
        present = bool(val and val.strip())
        icon = "OK" if present else "FALTA"
        display = mask_token(val) if present and "TOKEN" in key else ("OK" if present else "")
        print(f"  {icon}: {key} {display}")
    if not (os.environ.get("GTM_REFRESH_TOKEN") or "").strip():
        print("\nPROXIMO PASSO: python3 gtm_setup.py oauth")


# ---------------------------------------------------------------------------
# oauth
# ---------------------------------------------------------------------------

def find_free_port(start=8080, end=8090):
    for port in range(start, end + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((SERVER, port))
            s.close()
            return port
        except OSError:
            continue
    return None


def run_oauth():
    try:
        from google_auth_oauthlib.flow import Flow
    except ImportError:
        print("ERRO: google-auth-oauthlib nao instalado.")
        print("  pip3 install --user google-auth-oauthlib")
        sys.exit(1)

    _load_env_file()
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        print("ERRO: GOOGLE_ADS_CLIENT_ID e GOOGLE_ADS_CLIENT_SECRET precisam estar no .env")
        print(f"  Arquivo: {ENV_PATH}")
        sys.exit(1)

    port = find_free_port()
    if not port:
        print("ERRO: Nenhuma porta livre entre 8080-8090.")
        sys.exit(1)
    redirect_uri = f"http://{SERVER}:{port}"

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = Flow.from_client_config(client_config, scopes=SCOPES)
    flow.redirect_uri = redirect_uri

    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )

    print()
    print("=" * 60)
    print("  AUTORIZACAO GOOGLE TAG MANAGER")
    print("=" * 60)
    print()
    print("Abre esta URL no browser (ou ela vai abrir sozinha):")
    print()
    print(f"  {authorization_url}")
    print()
    print(f"Aguardando callback em {redirect_uri} ...")
    print()

    webbrowser.open(authorization_url)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER, port))
    sock.listen(1)

    try:
        connection, _ = sock.accept()
        data = connection.recv(4096).decode("utf-8")
    except KeyboardInterrupt:
        print("\nCancelado pelo usuario.")
        sock.close()
        sys.exit(1)

    match = re.search(r"GET\s\/\?(.*?)\s", data)
    if not match:
        print("ERRO: Callback invalido recebido do Google.")
        connection.close()
        sock.close()
        sys.exit(1)

    params = {}
    for pair in match.group(1).split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k] = unquote(v)

    if "error" in params:
        print(f"ERRO do Google: {params['error']}")
        connection.close()
        sock.close()
        sys.exit(1)

    code = params.get("code", "")
    if not code:
        print("ERRO: Nenhum authorization code recebido.")
        connection.close()
        sock.close()
        sys.exit(1)

    html = (
        "<html><head><meta charset='utf-8'></head><body style='font-family:sans-serif;"
        "display:flex;align-items:center;justify-content:center;height:100vh;background:#FAF7F2;'>"
        "<div style='text-align:center;'>"
        "<h1 style='color:#4CAF50;'>Pronto!</h1>"
        "<p style='color:#57534E;font-size:1.2rem;'>GTM autorizado. Pode fechar esta aba.</p>"
        "</div></body></html>"
    )
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html}"
    connection.sendall(response.encode())
    connection.close()
    sock.close()

    flow.fetch_token(code=code)
    refresh_token = flow.credentials.refresh_token
    if not refresh_token:
        print("ERRO: Google nao retornou refresh token.")
        print("  Va em https://myaccount.google.com/permissions, revogue o app, e tente de novo.")
        sys.exit(1)

    print(f"Refresh token gerado: {mask_token(refresh_token)}")
    return refresh_token


def save_refresh_token(token):
    if not os.path.isfile(ENV_PATH):
        print(f"ERRO: .env nao encontrado em {ENV_PATH}")
        sys.exit(1)
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if "GTM_REFRESH_TOKEN=" in content:
        content = re.sub(r'GTM_REFRESH_TOKEN=.*', f'GTM_REFRESH_TOKEN="{token}"', content)
    else:
        content = content.rstrip("\n") + f'\nGTM_REFRESH_TOKEN="{token}"\n'
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Salvo em {ENV_PATH}")


def cmd_oauth():
    token = run_oauth()
    print()
    save_refresh_token(token)
    print()
    print("Proximo passo: python3 gtm_setup.py test")


# ---------------------------------------------------------------------------
# test
# ---------------------------------------------------------------------------

def cmd_test():
    print("Testando conexao com o GTM...")
    try:
        service = gtm_service()
        resp = service.accounts().list().execute()
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)
    accounts = resp.get("account", [])
    print(f"\nConexao OK! {len(accounts)} conta(s) GTM acessivel(is):")
    for a in accounts:
        print(f"  {a.get('name')}  (accountId {a.get('accountId')})")


COMMANDS = {"check": cmd_check, "oauth": cmd_oauth, "test": cmd_test}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Uso: python3 gtm_setup.py <check|oauth|test>")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
